### Configures wireguard service at each server
### Cautiousness required: Script generates new keys for all servers so the setup must be redpeloyed after this script is being run
### Run get_public_keys.py then run config_vpn.py and generate_client_config.py to get updated status

import paramiko
from servers import ip_list
import pprint

# Config
port = 22
username = 'root'
key_path = '/home/nikola/.ssh/id_ed25519'


# Commands to run per host
commands = [
    "apt-get update",
    "apt-get install -y wireguard",
    "umask 077",
    "wg genkey | tee /etc/wireguard/wg0.key",
    "cat /etc/wireguard/wg0.key | wg pubkey | tee /etc/wireguard/wg0.pub",
    "echo -e '#!/bin/bash\nnft delete table inet mynat' | tee /etc/wireguard/nft-postdown.sh > /dev/null && chmod +x /etc/wireguard/nft-postdown.sh",
    "echo -e '#!/bin/bash\n\nnft add table inet mynat\nnft add chain inet mynat postrouting { type nat hook postrouting priority 100 \\; }\nnft add rule inet mynat postrouting ip saddr 10.0.100.0/24 ip daddr 10.0.0.0/24 oif wg0 masquerade' | tee /etc/wireguard/nft-postup.sh > /dev/null && chmod +x /etc/wireguard/nft-postup.sh"
]

# The list that hold collected public keys
public_keys = {}

def execute_ssh_session(ip, name, port, username, key_path, commands):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key = paramiko.Ed25519Key.from_private_key_file(key_path)

        print(f"Connecting to {name} ({ip})...")
        ssh.connect(ip, port=port, username=username, pkey=private_key)
        print(f"Connected to {name}")

        for cmd in commands:
            print(f"[{name}] Executing: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            exit_code = stdout.channel.recv_exit_status()

            out = stdout.read().decode().strip()
            err = stderr.read().decode().strip()

            if out:
                print(f"[{name}] Output:\n{out}")
            if err:
                print(f"[{name}] Error:\n{err}")

            if exit_code != 0:
                print(f"[{name}] Command failed: {cmd}")
                break

        # After all commands, retrieve the public key
        stdin, stdout, stderr = ssh.exec_command("cat /etc/wireguard/wg0.key")
        priv_key = stdout.read().decode().strip()
        error_output = stderr.read().decode().strip()

        ssh.close()

        if error_output:
            print(f"[{name}] Error fetching public key: {error_output}")
            return None

        print(f"[{name}] Public key retrieved.")
        return priv_key

    except Exception as e:
        print(f"[{name}] SSH error: {e}")
        return None

# Execute for each host
for name, ip in ip_list.items():
    key = execute_ssh_session(ip, name, port, username, key_path, commands)
    if key:
        public_keys[name] = key
with open("public_keys.py", "w") as f:
    f.write("public_keys = ")
    pprint.pprint(public_keys, stream=f)

print("\nPublic keys saved in public_keys.py")
