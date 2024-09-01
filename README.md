# Subdomain Enumeration Script

## Deskripsi
Skrip ini melakukan enumerasi subdomain menggunakan berbagai alat dan sumber data publik. Skrip ini dirancang untuk membantu dalam mengidentifikasi subdomain dari sebuah domain dan mendeteksi potensi kerentanannya.

## Prerequisites
Sebelum menjalankan skrip, pastikan Anda memiliki alat-alat berikut terinstal:

- `subfinder`: Untuk menemukan subdomain menggunakan berbagai sumber.
- `curl`: Untuk mengambil data dari URL.
- `jq`: Untuk memproses data JSON.
- `anew`: Untuk menghapus entri duplikat dari file.
- `findomain`: Untuk menemukan subdomain dari berbagai sumber.
- `cero`: Untuk menemukan subdomain dari sumber publik.
- `shosubgo`: Untuk menemukan subdomain.
- `gau`: Untuk mengambil URL dari berbagai sumber.
- `waybackurls`: Untuk mengambil URL dari Archive.org.
- `dnsx`: Untuk melakukan pencarian DNS.
- `assetfinder`: Untuk menemukan subdomain.
- `nuclei`: Untuk mendeteksi kerentanan.
- `httpx`: Untuk memeriksa subdomain yang aktif.

## Instalasi

1. **Clone repository ini:**
    ```bash
    git clone https://github.com/username/repository.git
    cd repository
    ```

2. **Instal alat yang dibutuhkan:**
    Anda dapat menginstal alat-alat yang diperlukan melalui package manager atau dengan mengikuti petunjuk instalasi masing-masing alat. Contoh instalasi dengan Homebrew untuk macOS:

    ```bash
    brew install subfinder jq anew findomain cero shosubgo gau waybackurls dnsx assetfinder nuclei httpx
    ```

3. **Pastikan semua alat telah terinstal dan tersedia di PATH Anda.**

## Cara Menggunakan

1. **Jalankan skrip dengan parameter domain:**
    ```bash
    ./subdomain_enum.sh example.com
    ```

    Gantilah `example.com` dengan domain yang ingin Anda lakukan enumerasi subdomainnya.

2. **Skrip ini akan melakukan langkah-langkah berikut:**
    - Membuat direktori dengan nama domain dan berpindah ke dalamnya.
    - Melakukan enumerasi subdomain menggunakan berbagai alat dan sumber data.
    - Mengidentifikasi potensi kerentanan dan mengumpulkan hasilnya di file.

3. **Hasil akan disimpan di file sebagai berikut:**
    - `domains.txt`: Daftar subdomain yang ditemukan.
    - `vulns/takeovers.txt`: Hasil deteksi kerentanan takeover.
    - `vhosts.txt`: Daftar virtual host.
    - `hosts.txt`: Daftar subdomain aktif.

## Contoh Penggunaan

```bash
./subdomain_enum.sh example.com
