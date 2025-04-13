import paramiko
from servers import ip_list
#from public_keys import public_keys 
from clients import client_peers

import importlib.util

#Making sure public_key are up to date
def load_public_keys():
    spec = importlib.util.spec_from_file_location("public_keys", "./public_keys.py")
    public_keys_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(public_keys_module)
    return public_keys_module.public_keys

# def load_clients():
#     spec = importlib.util.spec_from_file_location("clients", "./clients.py")
#     clients_module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(clients_module)
#     return clients_module.clients   

public_keys = load_public_keys()
#clients = load_clients()

# Config
port = 22
username = 'root'
key_path = '/home/nikola/.ssh/id_ed25519'
listen_port = 51000
subnet = "10.0.0."

# Function to generate wg0.conf content
def generate_wg_conf_content(this_server, this_ip, this_index):
    lines = []

    # Interface block
    lines.append("[Interface]")
    lines.append(f"Address = {subnet}{this_index}/24")
    lines.append(f"PostUp = wg set %i private-key /etc/wireguard/%i.key")
    lines.append(f"ListenPort = {listen_port}")
    lines.append(f"PostUp = /etc/wireguard/nft-postup.sh")
    lines.append(f"PostDown = /etc/wireguard/nft-postdown.sh")
    lines.append("")
    
    # Peer blocks
    for peer_index, (peer_name, peer_ip) in enumerate(ip_list.items(), start=1):
        if peer_name == this_server:
            continue  # Skip self
        lines.append("[Peer]")
        lines.append(f"# {peer_index} - {peer_name}")
        lines.append(f"PublicKey = {public_keys[peer_name]}")
        lines.append(f"AllowedIPs = {subnet}{peer_index}/32")
        lines.append(f"Endpoint = {peer_ip}:{listen_port}")
        lines.append("")
    
    for client_id, client_info in client_peers.items():
        lines.append("[Peer]")
        lines.append(f"# Client {client_id}")
        lines.append(f"PublicKey = {client_info['public_key']}")
        lines.append(f"AllowedIPs = {client_info['ip']}/32")
        lines.append("")  # Add empty line to separate peers

    return "\n".join(lines)

# Deploy the config to each server
for idx, (server_name, public_ip) in enumerate(ip_list.items(), start=1):
    config_content = generate_wg_conf_content(server_name, public_ip, idx)

    print(f"\nConnecting to {server_name} ({public_ip}) to write wg0.conf...")

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key = paramiko.Ed25519Key.from_private_key_file(key_path)
        ssh.connect(public_ip, port=port, username=username, pkey=private_key)

        # Write config content to the remote file
        sftp = ssh.open_sftp()
        remote_file_path = "/etc/wireguard/wg0.conf"
        with sftp.file(remote_file_path, 'w') as remote_file:
            remote_file.write(config_content)
        sftp.close()

        print(f"{server_name}: wg0.conf deployed.")
        ssh.close()

    except Exception as e:
        print(f"{server_name}: Failed to deploy config - {e}")