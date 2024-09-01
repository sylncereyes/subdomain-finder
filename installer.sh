#!/bin/bash

# Periksa apakah pengguna menjalankan skrip sebagai root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit
fi

echo "Updating and installing prerequisites..."
sudo apt-get update

# Install prerequisites
sudo apt-get install -y curl git jq awk sed grep build-essential

# Install Go (Golang)
if ! command -v go &> /dev/null
then
    echo "Go not found, installing..."
    wget https://go.dev/dl/go1.23.0.linux-amd64.tar.gz
    sudo tar -C /usr/local -xzf go1.23.0.linux-amd64.tar.gz
    rm go1.20.7.linux-amd64.tar.gz
    export PATH=$PATH:/usr/local/go/bin
    echo "export PATH=$PATH:/usr/local/go/bin" >> ~/.bashrc
    source ~/.bashrc
else
    echo "Go is already installed"
fi

# Install Subfinder
echo "Installing Subfinder..."
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Install Anew
echo "Installing Anew..."
go install -v github.com/tomnomnom/anew@latest

# Install Findomain
echo "Installing Findomain..."
curl -LO https://github.com/Findomain/Findomain/releases/latest/download/findomain-linux
chmod +x findomain-linux
sudo mv findomain-linux /usr/local/bin/findomain

# Install Cero
echo "Installing Cero..."
go install github.com/glebarez/cero@latest

# Install Shosubgo
echo "Installing Shosubgo..."
go install -v github.com/incogbyte/shosubgo/cmd/shosubgo@latest

# Install Gau (Get All URLs)
echo "Installing Gau..."
go install github.com/lc/gau/v2/cmd/gau@latest

# Install Unfurl
echo "Installing Unfurl..."
go install github.com/tomnomnom/unfurl@latest

# Install Waybackurls
echo "Installing Waybackurls..."
go install github.com/tomnomnom/waybackurls@latest

# Install Dnsx
echo "Installing Dnsx..."
go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest

# Install Seclists
echo "Installing Seclists..."
sudo apt-get install -y seclists

# Install Assetfinder
echo "Installing Assetfinder..."
go install github.com/tomnomnom/assetfinder@latest

# Install Nuclei
echo "Installing Nuclei..."
go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest

# Install Httpx
echo "Installing Httpx..."
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

echo "All tools installed successfully!"
