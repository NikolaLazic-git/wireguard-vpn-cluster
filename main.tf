terraform {
  required_providers {
    hcloud = {
      source = "hetznercloud/hcloud"
      version = "~> 1.31"
    }
  }
}

provider "hcloud" {
  token = var.api_token
}


