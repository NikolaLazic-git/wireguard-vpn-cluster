### Only one key can be imported into VM during VM creation
resource "hcloud_ssh_key" "ssh_key" {
  name       = "my-key"
  public_key = file("../.ssh/id_ed25519.pub")
}

### Creates servers based on servers list within variables.tf
resource "hcloud_server" "servers" {
  for_each    = var.servers
  name        = each.key
  image       = "ubuntu-24.04"
  server_type = "cx22"
  location    = each.value.location
  ssh_keys    = [hcloud_ssh_key.ssh_key.name]

  public_net {
    ipv4_enabled = true
    ipv4         = hcloud_primary_ip.public_ips[each.key].id
    ipv6_enabled = false
  }
}

### Wanted to have floating IP / static IP that is not dependant on server creation/destroying
### Benefit from permanent IP usage would be ease of redeployment of one of servers in case of crash
resource "hcloud_primary_ip" "public_ips" {
  for_each       = var.servers
  name           = "pip-${each.key}"
  type           = "ipv4"
  assignee_type  = "server"
  auto_delete    = false
  datacenter     = each.value.datacenter
}





