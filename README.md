The code builds VPN cluster that is run on a Hetzner cloud.

There is N servers in VPN cluster, VPN client can choose a server and connect to it. One server grants access to other servers in VPN cluster. Servers are building full mesh of WireGuard connections between themself, so if one servers dies it should not impact general service availablity.
Python has been used to automate WireGuard service initilaization. There are separate scripts for each of actions that can be combined within single bash script that will be calling other scripts.
Explanation of files used for VPN cluster creation:

Terraform:
•	main.tf: initializes tf
•	servers.tf: defines SSH key and importes it to each host; defines VPN servers based on variables.tf; defines public IP for each of servers
•	variables.tf: defines server that will be created, followed by datacenter ID
•	loadbalancer.tf: file not in use, leftover from the initial idea of using load balancer as an entry point to the vpn cluster
•	sensitive.tfvar: file that keeps record of API key, not published on git as it grants access to the environment

Python (scripts should be used in following order):
•	servers.py: manually defined list of servers and corresponding public IP (mannually filled out after servers creation)
•	config_servers.py: configures wireguard service at each server
•	get_public_keys.py: pulls out list of all public keys for all servers storing them in public_key.py
•	public_key.py: list of public keys for wireguard service from each server in cluster (automatically filled in by get_public_keys.py)
•	config_vpn.py: creates VPN cluster setup with servers being full-mesh peered between themselves and adds client peer config to each of servers
•	generate_client_config.py: creates config that vpn client needs for connecting to VPN cluster
•	refresh_vpn.py: refreshes all VPN tunnels in case when any adjustment in config is done
•	clients.py: list of all clients defined with corresponding public key that client generated and sent over for whitelist
