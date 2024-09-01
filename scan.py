#!/bin/bash

# Periksa apakah domain disertakan
if [ -z "$1" ]; then
  echo "Usage: $0 <domain>"
  exit 1
fi

DOMAIN=$1

# Buat direktori dan pindah ke dalamnya
mkdir "$DOMAIN" && cd "$DOMAIN" || { echo "Failed to create directory"; exit 1; }

echo "### Subdomain Enumeration ###"
echo ""

# Jalankan enumerasi subdomain dengan berbagai alat
subfinder -silent -d "$DOMAIN" -o domains.txt
curl -s "https://crt.sh/?q=%25.$DOMAIN&output=json" | jq -r '.[].name_value' 2>/dev/null | sed 's/\*\.//g' | sort -u | grep -o "\w.*$DOMAIN" | anew -q domains.txt
curl -s "https://api.hackertarget.com/hostsearch/?q=$DOMAIN" | grep -o "\w.*$DOMAIN" | anew -q domains.txt
curl -s "https://riddler.io/search/exportcsv?q=pld:$DOMAIN" | grep -Po "(([\w.-]*)\.([\w]*)\.([A-z]))\w+" | grep -o "\w.*$DOMAIN" | anew -q domains.txt
curl -sk "http://web.archive.org/cdx/search/cdx?url=.$DOMAIN&output=txt&fl=original&collapse=urlkey&page=" | awk -F/ '{gsub(/:./, "", $3); print $3}' | sort -u | anew -q domains.txt
curl -s "https://dns.bufferover.run/dns?q=.$DOMAIN" | grep "$DOMAIN" | awk -F, '{gsub("\"", "", $2); print $2}' | anew -q domains.txt
curl -sk "https://api.certspotter.com/v1/issuances?domain=$DOMAIN&include_subdomains=true&expand=dns_names" | jq .[].dns_names | grep -Po "(([\w.-])\.([\w])\.([A-z]))\w+" | anew -q domains.txt
curl -sk "https://jldc.me/anubis/subdomains/$DOMAIN" | grep -Po "((http|https):\/\/)?(([\w.-])\.([\w])\.([A-z]))\w+" | anew -q domains.txt
curl -sk "https://jldc.me/anubis/subdomains/$DOMAIN" | jq -r '.' | grep -o "\w.*$DOMAIN" | anew -q domains.txt
curl -sk "https://api.threatminer.org/v2/domain.php?q=$DOMAIN&rt=5" | jq -r '.results[]' | grep -o "\w.*$DOMAIN" | sort -u | anew -q domains.txt
curl -sk "https://sonar.omnisint.io/subdomains/$DOMAIN" | cut -d "[" -f1 | cut -d "]" -f1 | cut -d "\"" -f 2 | sort -u | anew -q domains.txt
findomain --target "$DOMAIN" --quiet | anew -q domains.txt
cero "$DOMAIN" | anew -q domains.txt
shosubgo -d "$DOMAIN" -s "9udLd1dPtVRNVSu1Gh0YHJ8FxAZ4qW4X" | anew -q domains.txt
gau --subs "$DOMAIN" | unfurl -u domains | anew -q domains.txt
waybackurls "$DOMAIN" | unfurl -u domains | anew -q domains.txt
dnsx -silent -rc noerror -ro -nc -a -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt -d "$DOMAIN" | cut -d" " -f1 | anew -q domains.txt
assetfinder -subs-only "$DOMAIN" | anew -q domains2.txt

# Proses duplikat
sed '/^\*/d' domains2.txt | anew -q domains.txt
cat domains2.txt | grep '*.' | awk '{sub(/^\*./,"")}1' | subfinder -silent | anew -q domains.txt
rm -rf domains2.txt

# Deteksi kerentanan dan verifikasi subdomain
nuclei -silent -list domains.txt -t dns/azure-takeover-detection.yaml -t dns/elasticbeanstalk-takeover.yaml -t http/takeovers/ -c 30 -o vulns/takeovers.txt
cat domains.txt | httpx -silent -p 80,443,8080,8443 -vhost | grep vhost | cut -d" " -f1 | anew -q vhosts.txt
cat vhosts.txt | httpx -silent -sc | grep 200 | cut -d" " -f1 | anew -q hosts.txt
