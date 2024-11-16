variable "region" {}
variable "ami" {}
variable "instance_type" {}
variable "instance_name" {}
variable "key_name" {}
variable "sg_id" {
    type = list(string)
}

