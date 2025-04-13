### Generates client config in txt file that needs to be placed and adjusted slightly

import os
import importlib.util
from servers import ip_list
from clients import client_peers
def load_public_keys():
    spec = importlib.util.spec_from_file_location("public_keys", "./public_keys.py")
    public_keys_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(public_keys_module)
    return public_keys_module.public_keys

public_keys = load_public_keys()

# IP list and public keys for servers


# Configuration details
client_private_key = 'PostUp = wg set %i private-key /etc/wireguard/%i.key'  # Replace with actual private key
listen_port = 51000

# Generate client config for a single interface with a single server as peer
def generate_client_interface_config(interface_id, server_name, server_ip, server_pub_key, client_ip):
    config = f"""
[Interface]
Address = {client_ip}/24
PrivateKey = {client_private_key}
ListenPort = {listen_port}
Interface = wg{interface_id}

[Peer]
# {server_name}
PublicKey = {public_keys[server_name]}
Endpoint = {server_ip}:{listen_port}
AllowedIPs = 10.0.0.0/24
PersistentKeepalive = 25
"""
    return config

# Generate config files for each client interface (wg1.conf, wg2.conf, etc.) dynamically based on ip_list
for interface_id, (server_name, server_ip) in enumerate(ip_list.items(), start=1):  # Dynamically iterate through ip_list
    # Assign a unique IP address for each client interface (10.0.100.1, 10.0.100.2, etc.)
    client_ip = f"10.0.100.{interface_id}"

    server_pub_key = public_keys[server_name]

    # Generate configuration content for each interface
    config_content = generate_client_interface_config(interface_id, server_name, server_ip, server_pub_key, client_ip)

    # Write to a file with the appropriate name (client_vpn_interface1_conf.txt, etc.)
    filename = f"client_vpn_interface{interface_id}_conf.txt"
    with open(filename, 'w') as config_file:
        config_file.write(config_content)

    print(f"Configuration for interface {interface_id} written to {filename}")