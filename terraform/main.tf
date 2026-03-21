# 1. Configuration du fournisseur AWS
provider "aws" {
  region = "us-east-1" 
}

# 2. Déclaration de la clé SSH pour AWS
resource "aws_key_pair" "deployer" {
  key_name   = "devops-key-project"
  public_key = file("../ma-cle-devops.pub") 
}

# 3. Création du Groupe de Sécurité (Pare-feu)
resource "aws_security_group" "sg_devops" {
  name        = "sg_devops_project"
  description = "Autoriser SSH, HTTP et Kubernetes"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 6443
    to_port     = 6443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    self      = true
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 4. Instance Master
resource "aws_instance" "master" {
  ami           = "ami-04a81a99f5ec58529" # Ubuntu 24.04 LTS Officiel
  instance_type = "t3.small"
  key_name      = aws_key_pair.deployer.key_name
  vpc_security_group_ids = [aws_security_group.sg_devops.id]

  tags = { Name = "K8s-Master" }
}

# 5. Instance Worker
resource "aws_instance" "worker" {
  ami           = "ami-04a81a99f5ec58529" 
  instance_type = "t3.micro"
  key_name      = aws_key_pair.deployer.key_name
  vpc_security_group_ids = [aws_security_group.sg_devops.id]

  tags = { Name = "K8s-Worker" }
}

# 6. Affichage des adresses IP
output "master_public_ip" {
  value = aws_instance.master.public_ip
}

output "worker_public_ip" {
  value = aws_instance.worker.public_ip
}