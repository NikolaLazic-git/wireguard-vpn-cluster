### Connectes to each server and takes public key storing it in public_keys.py list for later usage

import paramiko
from servers import ip_list
import pprint

# Config
port = 22
username = 'root'
key_path = '/home/nikola/.ssh/id_ed25519'


# The list that hold collected public keys
public_keys = {}

def execute_ssh_session(ip, name, port, username, key_path):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key = paramiko.Ed25519Key.from_private_key_file(key_path)

        print(f"Connecting to {name} ({ip})...")
        ssh.connect(ip, port=port, username=username, pkey=private_key)
        print(f"Connected to {name}")

        stdin, stdout, stderr = ssh.exec_command("cat /etc/wireguard/wg0.pub")
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
    key = execute_ssh_session(ip, name, port, username, key_path)
    if key:
        public_keys[name] = key
with open("public_keys.py", "w") as f:
    f.write("public_keys = ")
    pprint.pprint(public_keys, stream=f)

print("\nPublic keys saved in public_keys.py")
