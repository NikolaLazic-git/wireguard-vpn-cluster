### Refreshes VPN servers config by shut/unshut inteface: needed when any config adjustment is done

import paramiko
from servers import ip_list

# SSH config
port = 22
username = 'root'
key_path = '/home/nikola/.ssh/id_ed25519'
commands = [
    'wg-quick down wg0',
    'wg-quick up wg0'
]

def execute_commands_on_host(ip, commands):
    try:
        print(f"\nConnecting to {ip}...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        key = paramiko.Ed25519Key.from_private_key_file(key_path)
        ssh.connect(ip, port=port, username=username, pkey=key)
        print(f"Connected to {ip}")

        for cmd in commands:
            print(f"Executing: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            out = stdout.read().decode().strip()
            err = stderr.read().decode().strip()

            if out:
                print(f"Output:\n{out}")
            if err:
                print(f"Error:\n{err}")

        ssh.close()
        print(f"Disconnected from {ip}")

    except Exception as e:
        print(f"Failed on {ip}: {e}")

# Run on all hosts
for name, ip in ip_list.items():
    execute_commands_on_host(ip, commands)
