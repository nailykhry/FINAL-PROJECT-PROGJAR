POST /material HTTP/1.1
Host: localhost:9999
Connection: keep-alive
Content-Length: 3016
Cache-Control: max-age=0
sec-ch-ua: "Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: http://localhost:9999
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryWh5ncUZGGXbh8mcN
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: http://localhost:9999/addmaterial/6484ab7d96e103d43b7a5942
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,id;q=0.8

------WebKitFormBoundaryWh5ncUZGGXbh8mcN
Content-Disposition: form-data; name="filename"; filename="README.md"
Content-Type: application/octet-stream

# Live Coding - Ruang Anime

## Implementation technique

Siswa akan melaksanakan sesi live code di 20 menit terakhir dari sesi mentoring dan di awasi secara langsung oleh Mentor. Dengan penjelasan sebagai berikut:

- **Durasi**: 20 menit pengerjaan
- **Submit**: Maximum 10 menit setelah sesi mentoring menggunakan grader-cli submit
- **Obligation**: Wajib melakukan share screen di breakout room yang akan dibuatkan oleh Mentor pada saat mengerjakan Live Coding.

## NOTES

- Pada skeleton kode sudah disediakan beberapa component, tidak diperkenankan untuk mengubah struktur folder dan nama file serta tidak perlu membuat component baru.
- Dilarang mengganti nama component dan function yang diberikan.
- Wajib menjalankan `npm install` atau `pnpm install` sebelum mengerjakan project.

## Description

Pada live code kali ini, kalian akan diminta untuk melanjutkan sebuah project yang berjudul Ruang Anime.

Ruang Anime merupakan sebuah website yang bisa digunakan untuk mencari informasi anime. Website ini memiliki 2 halaman, yaitu halaman Home dan halaman list anime.

Pada halaman Home, user akan melihat sebuah search form, kemudian user bisa menginput term pencarian anime.

Ketika search form di-submit, maka tampilan akan berubah ke hasil pencarian anime yang sesuai dengan term yang diinput oleh user.

Pencarian data anime akan menggunakan API dari [Jikan](https://jikan.moe/).

Dokumentasi endpoint yang digunakan adalah:

`https://docs.api.jikan.moe/#tag/anime/operation/getAnimeSearch`

Silahkan dibaca lebih lanjut mengenai dokumentasi endpoint tersebut.

Jika tidak ada hasil pencarian, maka akan ditampilkan pesan "Tidak ada anime yang ditemukan.".

Pada tampilan hasil pencarian juga ada sebuah button yg digunakan untuk kembali ke form pencarian awal.

Pada halaman list anime, user akan melihat list anime dan menampilkan beberapa informasi seperti:

- Judul
- Type
- Source
- Synopsis
- Gambar

Sebagai catatan, untuk mempermudah pengerjaan sudah ditinggalkan beberapa clue di Component yang sudah disediakan.

Berikut adalah list dari Component yang perlu kalian kerjakan:

- `src/components/SearchBox.jsx`
  - Berisikan search form yang terdiri dari text input dan button
  - Placeholder dari text input adalah `Judul Anime...`
- `src/components/AnimeCardList.jsx`
  - Component yg akan melakukan fetching data berdasarkan term pencarian dari searchBox
- `src/components/AnimeCard.jsx`
  - Component yg akan merender data anime, data diterima melalui props
- `src/components/Content.jsx`
  - Component yg akan melakukan render component AnimeCardList atau SearchBox berdasarkan kondisi state
- `src/components/NoAnimeFound.jsx`
  - Compoennt yg akan merender pesan "Tidak ada anime yang ditemukan."

Berikut adalah demo dari Ruang Anime:

![Ruang Anime Demo](https://youtu.be/_5YoDfZlYHI)

------WebKitFormBoundaryWh5ncUZGGXbh8mcN--