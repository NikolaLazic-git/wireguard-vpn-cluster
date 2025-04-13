### Load Balancer Setup - Initial Idea
### Load Balancer in Hetzner does not support the UDP traffic. 
### Needed to abandon the idea with Load Balancer as an entry point of a cluster.

### Code left for reference


# resource "hcloud_load_balancer" "lb1" {
#   name               = "lb1"
#   load_balancer_type = "lb11"
#   network_zone       = "eu-central"
#   algorithm{
#     type     = "least_connections"
#   }
# }

# ### Target servers
# resource "hcloud_load_balancer_target" "load_balancer_target" {
#   type             = "server"
#   load_balancer_id = hcloud_load_balancer.lb1.id
#   server_id        = hcloud_server.example.id
# }

# resource "hcloud_load_balancer_target" "load_balancer_target1" {
#   type             = "server"
#   load_balancer_id = hcloud_load_balancer.lb1.id
#   server_id        = hcloud_server.example1.id
# }


# ##### LB Services - Test was done for SSH
# resource "hcloud_load_balancer_service" "load_balancer_service" {
#   load_balancer_id = hcloud_load_balancer.lb1.id
#   protocol         = "udp"
#   listen_port      = 5100
#   destination_port = 5100

#   health_check {
#     protocol = "tcp"
#     port     = 5100
#     interval = 10
#     timeout  = 5
#   }
# }



### Network settings that are not relevant for the task I have been worked on. 
### Each requirment by the task text can be met by VPN service setting up + internal networks are forbidden.
### At some point I was looking into vSwitch but then double checked requirments for internal networks.

#  resource "hcloud_network" "vpn_serv_network" {
#   name     = "my-net"
#   ip_range = "10.0.0.0/16"
#   expose_routes_to_vswitch  = true
# }

# resource "hcloud_network_subnet" "vpn_serv_subnet" {
#   network_id   = hcloud_network.vpn_serv_network.id
#   type         = "cloud"
#   network_zone = "eu-central"
#   ip_range     = "10.0.0.0/24"
# }

# resource "hcloud_load_balancer_network" "load_balancer_network" {
#   load_balancer_id = hcloud_load_balancer.lb1.id
#   network_id       = hcloud_network.vpn_serv_network.id
#   ip               = "10.0.0.100"
#   depends_on = [
#     hcloud_network_subnet.vpn_serv_subnet
#   ]
# }



# resource "hcloud_network_subnet" "subnet" {
#   network_id   = hcloud_network.vpn_serv_network.id
#   type         = "server"
#   network_zone = "eu-central"
#   ip_range     = "10.0.99.0/24"
#   #vswitch_id   = 4040
# }



