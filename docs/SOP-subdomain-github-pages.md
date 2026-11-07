# SOP Singkat: Menghubungkan Subdomain ke Situs GitHub Pages

**Situs:** Agromaterials Research Group, Politeknik ATI Makassar
**Subdomain yang diminta:** `material-research.atim.ac.id`
**Pemohon:** Dr. Massriyady Massaguni (Research Director)
**Tanggal:** ____ / ____ / 2026

## 1. Tujuan dan prinsip

Situs ini dihosting di **GitHub Pages** (file statis, tanpa database, tanpa WordPress, tanpa PHP).
Kampus hanya meminjamkan **nama alamat** lewat satu catatan DNS. Server kampus tidak dilewati
dan tidak terhubung ke situs ini.

**Yang diminta ke IT:** satu catatan DNS saja.
**Yang TIDAK perlu:** membuat hosting/folder subdomain, memasang WordPress, membuat database.

## 2. Data untuk catatan DNS

| Type | Name / Host | Target / Value | TTL |
|---|---|---|---|
| **CNAME** | `material-research` | `material-research.github.io` | 3600 |

- Cloudflare: set **Proxy status = DNS only** (awan abu-abu).
- Jika sudah ada subdomain `material-research` di hosting (A/CNAME/folder lama), hapus catatan lamanya dulu.
- Jika zona punya catatan **CAA**, izinkan penerbit `letsencrypt.org`.
- Cadangan bila DNS tidak mendukung CNAME: empat catatan **A** untuk `material-research`:
  `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.

## 3. Langkah

**A. Tim IT**
1. Buka pengelola DNS `atim.ac.id` (Cloudflare atau DNS hosting).
2. Hapus catatan lama bernama `material-research` bila ada.
3. Tambahkan catatan CNAME pada bagian 2, lalu simpan.
4. Cek: `nslookup material-research.atim.ac.id` harus menunjuk ke `material-research.github.io`.
5. Beri tahu pemohon bahwa DNS sudah aktif.

**B. Pemohon / tim web (setelah A5)**
6. Menambahkan file `CNAME` (isi: `material-research.atim.ac.id`) dan mengubah `url`/`baseurl` di repo, lalu push ke `main`.
7. GitHub: Settings -> Pages -> Custom domain = `material-research.atim.ac.id`; tunggu centang hijau; centang **Enforce HTTPS**.

**C. Opsional (disarankan): verifikasi domain**
8. Organisasi GitHub `material-research` -> Settings -> Pages -> Add a domain -> salin catatan **TXT**
   (`_github-pages-challenge-material-research`) -> IT memasangnya di DNS -> klik Verify.

## 4. Checklist selesai

- [ ] `nslookup material-research.atim.ac.id` menunjuk ke `material-research.github.io`
- [ ] `https://material-research.atim.ac.id/` menampilkan situs dengan gaya lengkap
- [ ] Enforce HTTPS aktif (gembok di browser)
- [ ] Halaman `/team/`, `/publications/`, `/blog/` terbuka
- [ ] (Opsional) domain terverifikasi di GitHub

## 5. Jika ada kendala

| Gejala | Penyebab umum |
|---|---|
| "DNS check unsuccessful" | CNAME salah ketik / belum menyebar (tunggu hingga beberapa jam) |
| Enforce HTTPS tidak bisa dicentang | Sertifikat belum terbit; cek proxy Cloudflare dan catatan CAA |
| Situs tanpa gaya | `baseurl` belum dikosongkan di repo |
| 404 | File `CNAME` belum ada di `main` / custom domain belum disimpan |

## 6. Keamanan dan pemeliharaan

- Situs statis di server GitHub; tidak ada akses ke server, database, atau email kampus.
- Risiko utama adalah akun GitHub dibobol: aktifkan **2FA** pada semua pemilik repo.
- Pastikan cookie login sistem kampus tidak berlaku untuk seluruh `.atim.ac.id` (jika berlaku, beri tahu pemohon).
- Jika situs dihentikan, **hapus catatan CNAME** agar subdomain tidak bisa diklaim pihak lain.

Setelah aktif, setiap perubahan isi dilakukan di repo `github.com/material-research/web` (branch `main`) dan tayang otomatis dalam 1-3 menit.
