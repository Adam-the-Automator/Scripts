#!*/bin/bash*

# update VM apt repository
apt-get update

# install docker-dependent packages
apt-get -y install apt-transport-https ca-certificates lsb-release

# add docker GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \

$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# update VM apt repository after adding docker
apt-get update

# install docker community edition and cli
apt-get -y install docker-ce docker-ce-cli containerd.io

# download docker-compose executable file
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# change permission of docker-compose to become executable
chmod +x /usr/local/bin/docker-compose