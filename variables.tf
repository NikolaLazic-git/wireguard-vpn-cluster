### Statically defined servers in 3 datacenters to achieve regional redundancy
### Choosed servers in Europe as I assumed the end users is Europe-based.

### Design is scalable as adding more servers to the deployment can be easily done by intoducing another varible for server6, server7 ...

variable "servers" {
  default = {
    server1 = { location = "fsn1", datacenter = "fsn1-dc14" }
    server2 = { location = "nbg1", datacenter = "nbg1-dc3" }
    server3 = { location = "fsn1", datacenter = "fsn1-dc14"}
    server4 = { location = "nbg1", datacenter = "nbg1-dc3" }
    server5 = { location = "hel1", datacenter = "hel1-dc2" }
  }
}

### As API key is sensitive information, it is kept in another tf file.
variable "api_token" {}