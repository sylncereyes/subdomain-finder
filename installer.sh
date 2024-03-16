#!/bin/bash

# Update and Upgrade System
echo "Updating and Upgrading your System.."
sudo apt-get update && sudo apt-get upgrade -y

# Install Python3 and PIP
echo "Installing Python3 and PIP..."
sudo apt-get install python3 python3-pip -y

# Install curl and jq
echo "Installing curl and jq..."
sudo apt-get install curl jq -y

# Install GoLang
echo "Installing Go..."
wget https://golang.org/dl/go1.18.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.18.linux-amd64.tar.gz
echo "export PATH=$PATH:/usr/local/go/bin" >> $HOME/.profile
source $HOME/.profile
rm go1.18.linux-amd64.tar.gz

# Check Go installation
go version

# Install Subfinder
echo "Installing Subfinder..."
GO111MODULE=on go get -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder

# Install Assetfinder
echo "Installing Assetfinder..."
go get -u github.com/tomnomnom/assetfinder

# Install Chaos
echo "Installing Chaos..."
GO111MODULE=on go get -v github.com/projectdiscovery/chaos-client/cmd/chaos

# Install Findomain
echo "Installing Findomain..."
wget https://github.com/Edu4rdSHL/findomain/releases/latest/download/findomain-linux
chmod +x findomain-linux
sudo mv findomain-linux /usr/local/bin/findomain

# Install Gau
echo "Installing Gau..."
GO111MODULE=on go get -u -v github.com/lc/gau

# Install Unfurl
echo "Installing Unfurl..."
go get -u github.com/tomnomnom/unfurl

# Install Waybackurls
echo "Installing Waybackurls..."
go get github.com/tomnomnom/waybackurls

# Install httpx
echo "Installing httpx..."
GO111MODULE=on go get -v github.com/projectdiscovery/httpx/cmd/httpx

# Additional tools installation here...

# Final System Update and Clean
echo "Final System Update and Cleaning Up..."
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get autoremove -y

echo "All tools installed successfully!"
