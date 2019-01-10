# terraform state holder

## Quickstart

- run app
- write config to it
  - `curl -XPOST -d'{"club-nyc1-prod": "https://v1-stage.cdn.33slona.com/7,7d151e257cd91a"}' 127.0.0.1:8080/config`
- use as terraform backend
  - `terraform {backend "http" {address = "http://127.0.0.1:8080/${var.name}-${var.region}-${var.env}/"}}`
