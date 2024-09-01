import subprocess
import sys
import os

def run_command(command):
    """Run a shell command and return the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

def main(domain):
    # Buat direktori dan pindah ke dalamnya
    try:
        os.makedirs(domain)
        os.chdir(domain)
    except Exception as e:
        print(f"Failed to create or change to directory: {e}")
        sys.exit(1)

    print("### Subdomain Enumeration ###")
    print("")

    # Jalankan enumerasi subdomain dengan berbagai alat
    commands = [
        f"subfinder -silent -d {domain} -o domains.txt",
        f"curl -s 'https://crt.sh/?q=%25.{domain}&output=json' | jq -r '.[].name_value' 2>/dev/null | sed 's/\\*\\.//g' | sort -u | grep -o '\\w.*{domain}' | anew -q domains.txt",
        f"curl -s 'https://api.hackertarget.com/hostsearch/?q={domain}' | grep -o '\\w.*{domain}' | anew -q domains.txt",
        f"curl -s 'https://riddler.io/search/exportcsv?q=pld:{domain}' | grep -Po '(([\w.-]*)\\.([\\w]*)\\.([A-z]))\\w+' | grep -o '\\w.*{domain}' | anew -q domains.txt",
        f"curl -sk 'http://web.archive.org/cdx/search/cdx?url=.{domain}&output=txt&fl=original&collapse=urlkey&page=' | awk -F/ '{{gsub(/:./, \"\", $3); print $3}}' | sort -u | anew -q domains.txt",
        f"curl -s 'https://dns.bufferover.run/dns?q=.{domain}' | grep {domain} | awk -F, '{{gsub(\"\\\"\", \"\", $2); print $2}}' | anew -q domains.txt",
        f"curl -sk 'https://api.certspotter.com/v1/issuances?domain={domain}&include_subdomains=true&expand=dns_names' | jq .[].dns_names | grep -Po '(([\w.-])\\.([\\w])\\.([A-z]))\\w+' | anew -q domains.txt",
        f"curl -sk 'https://jldc.me/anubis/subdomains/{domain}' | grep -Po '((http|https):\\/\\/)?(([\w.-])\\.([\\w])\\.([A-z]))\\w+' | anew -q domains.txt",
        f"curl -sk 'https://jldc.me/anubis/subdomains/{domain}' | jq -r '.' | grep -o '\\w.*{domain}' | anew -q domains.txt",
        f"curl -sk 'https://api.threatminer.org/v2/domain.php?q={domain}&rt=5' | jq -r '.results[]' | grep -o '\\w.*{domain}' | sort -u | anew -q domains.txt",
        f"curl -sk 'https://sonar.omnisint.io/subdomains/{domain}' | cut -d '[' -f1 | cut -d ']' -f1 | cut -d '\"' -f 2 | sort -u | anew -q domains.txt",
        f"findomain --target {domain} --quiet | anew -q domains.txt",
        f"cero {domain} | anew -q domains.txt",
        f"shosubgo -d {domain} -s '9udLd1dPtVRNVSu1Gh0YHJ8FxAZ4qW4X' | anew -q domains.txt",
        f"gau --subs {domain} | unfurl -u domains | anew -q domains.txt",
        f"waybackurls {domain} | unfurl -u domains | anew -q domains.txt",
        f"dnsx -silent -rc noerror -ro -nc -a -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt -d {domain} | cut -d' ' -f1 | anew -q domains.txt",
        f"assetfinder -subs-only {domain} | anew -q domains2.txt"
    ]

    for command in commands:
        print(f"Running command: {command}")
        run_command(command)

    # Proses duplikat
    dedup_commands = [
        "sed '/^\\*/d' domains2.txt | anew -q domains.txt",
        "cat domains2.txt | grep '*.' | awk '{sub(/^\\*./,\"\")}' | subfinder -silent | anew -q domains.txt",
        "rm -rf domains2.txt"
    ]

    for command in dedup_commands:
        print(f"Running command: {command}")
        run_command(command)

    # Deteksi kerentanan dan verifikasi subdomain
    final_commands = [
        "nuclei -silent -list domains.txt -t dns/azure-takeover-detection.yaml -t dns/elasticbeanstalk-takeover.yaml -t http/takeovers/ -c 30 -o vulns/takeovers.txt",
        "cat domains.txt | httpx -silent -p 80,443,8080,8443 -vhost | grep vhost | cut -d' ' -f1 | anew -q vhosts.txt",
        "cat vhosts.txt | httpx -silent -sc | grep 200 | cut -d' ' -f1 | anew -q hosts.txt"
    ]

    for command in final_commands:
        print(f"Running command: {command}")
        run_command(command)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scan.py <domain>")
        sys.exit(1)
    
    domain = sys.argv[1]
    main(domain)
