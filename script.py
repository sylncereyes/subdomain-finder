mkdir $1 && cd $1
echo "### Subdomain Enumeration ###"
echo ""
subfinder -silent -d $1 -o domains.txt
curl -s "https://crt.sh/?q=%25.$1&output=json" | jq -r '.[].name_value' 2>/dev/null | sed 's/\*\.//g' | sort -u | grep -o "\w.*$1" | anew -q domains.txt
curl -s "https://api.hackertarget.com/hostsearch/?q=$1" | grep -o "\w.*$1" | anew -q domains.txt
curl -s "https://riddler.io/search/exportcsv?q=pld:$1" | grep -Po "(([\w.-]*)\.([\w]*)\.([A-z]))\w+" | grep -o "\w.*$1" | anew -q domains.txt
curl -sk "http://web.archive.org/cdx/search/cdx?url=.$1&output=txt&fl=original&collapse=urlkey&page=" | awk -F/ '{gsub(/:./, "", $3); print $3}' | sort -u | anew -q domains.txt
curl -s "https://dns.bufferover.run/dns?q=.$1" | grep $1 | awk -F, '{gsub("\"", "", $2); print $2}' | anew -q domains.txt
curl -sk "https://api.certspotter.com/v1/issuances?domain=$1&include_subdomains=true&expand=dns_names" | jq .[].dns_names | grep -Po "(([\w.-])\.([\w])\.([A-z]))\w+" | anew -q domains.txt
curl -sk "https://jldc.me/anubis/subdomains/$1" | grep -Po "((http|https):\/\/)?(([\w.-])\.([\w])\.([A-z]))\w+" | anew -q domains.txt
curl -sk "https://jldc.me/anubis/subdomains/$1" | jq -r '.' | grep -o "\w.*$1" | anew -q domains.txt
curl -sk "https://api.threatminer.org/v2/domain.php?q=$1&rt=5" | jq -r '.results[]' |grep -o "\w.*$1" | sort -u   | anew -q domains.txt
curl -sk "https://sonar.omnisint.io/subdomains/$1" | cut -d "[" -f1 | cut -d "]" -f1 | cut -d "\"" -f 2 | sort -u | anew -q domains.txt
findomain --target $1 --quiet | anew -q domains.txt
cero $1 | anew -q domains.txt
shosubgo -d $1 -s "9udLd1dPtVRNVSu1Gh0YHJ8FxAZ4qW4X" | anew -q domains.txt
gau --subs $1 | unfurl -u domains | anew -q domains.txt
waybackurls $1 |  unfurl -u domains | anew -q domains.txt
dnsx -silent -rc noerror -ro -nc -a -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt -d $1 | cut -d" " -f1 | anew -q domains.txt
assetfinder -subs-only $1 | anew -q domains2.txt
sed '/^\*/d' domains2.txt | anew -q domains.txt
cat domains2.txt | grep '*.' | awk '{sub(/^\*./,"")}1' | subfinder -silent | anew -q domains.txt
rm -rf domains2.txt
nuclei -silent -list domains.txt -t dns/azure-takeover-detection.yaml -t dns/elasticbeanstalk-takeover.yaml -t http/takeovers/ -c 30 -o vulns/takeovers.txt
cat domains.txt | httpx -silent -p 80,443,8080,8443 -vhost | grep vhost | cut -d" " -f1 | anew -q vhosts.txt
cat vhosts.txt | httpx -silent -sc | grep 200 | cut -d" " -f1 | anew -q hosts.txt
