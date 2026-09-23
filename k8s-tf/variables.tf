variable "name" {
  description = "The name to use for all resources created by this module"
  type        = string
  default     = "FF-recom"
}

variable "smallname" {
  description = "The name to use for all resources created by this module"
  type        = string
  default     = "ffrecom"
}

variable "image" {
  description = "The Docker image to run"
  type        = string
  default     = "mcarroll321/ff-recom"
}

variable "container_port" {
  description = "The port the Docker image listens on"
  type        = number
  default     = 8000
}

variable "replicas" {
  description = "How many replicas to run"
  type        = number
  default     = 2
}