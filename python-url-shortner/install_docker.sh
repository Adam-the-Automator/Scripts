#!/bin/bash

# Update container Linux image APT repository data
apt-get update

# Install Docker required packages
apt-get -y install apt-transport-https ca-certificates lsb-release

# Add the Docker GPG key to trust the Docker APT repository
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update container Linux image APT repository data again after adding the Docker repository
apt-get update

# Install the Docker community edition and cli
apt-get -y install docker-ce docker-ce-cli containerd.io

# Download docker-compose executable file, replace the 1.29.2 listed below with the latest version you intend to use.
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Change permission of docker-compose to become executable
chmod +x /usr/local/bin/docker-compose