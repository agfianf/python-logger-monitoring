# 🚀 Logging Python ke Loki + Grafana

Sistem ini memungkinkan Anda melakukan logging aplikasi Python secara terpusat menggunakan stack modern:
- **Python** (dengan structlog)
- **Loki** (log aggregation)
- **Promtail** (log shipper)
- **Grafana** (visualisasi)

---

## 🗂️ Struktur Folder

```
.
├── config/
│   ├── loki-config.yml
│   ├── promtail-config.yml
│   ├── grafana-datasources.yml
│   └── grafana-dashboards.yml
├── dashboards/
│   └── structlog-dashboard.json
├── logs/
├── main.py
├── Dockerfile
├── docker-compose.yml
└── ...
```

---

## 🔗 Alur Logging

1. **Aplikasi Python** menulis log ke file di `logs/` dalam format JSON.
2. **Promtail** membaca log dari file/container Docker dan mengirim ke **Loki**.
3. **Loki** menyimpan dan mengindeks log.
4. **Grafana** mengambil log dari Loki dan menampilkannya di dashboard.

---

## 🏁 Cara Menjalankan

1. Pastikan semua file konfigurasi sudah ada di folder `config/` dan dashboard di folder `dashboards/`.
2. Jalankan perintah berikut:
   ```zsh
   docker-compose up --build
   ```
3. Buka browser ke [http://localhost:3000](http://localhost:3000) untuk melihat dashboard Grafana.

---

## ⚙️ Penjelasan Setiap Service

- **app**: Aplikasi Python yang menghasilkan log JSON. Log disimpan di `./logs` dan diambil oleh Promtail.
- **loki**: Sistem agregasi log. Konfigurasi di-mount dari `config/loki-config.yml`.
- **promtail**: Agen pengumpul log. Membaca log dari container Docker dan file log, lalu mengirim ke Loki. Konfigurasi di `config/promtail-config.yml`.
- **grafana**: Visualisasi log. Sudah terhubung otomatis ke Loki dan dashboard custom. Konfigurasi provisioning di `config/grafana-datasources.yml` dan `config/grafana-dashboards.yml`.

---

## 📝 Catatan Penting

- Pastikan path file log yang dibaca Promtail sesuai dengan path log aplikasi (`./logs`).
- Untuk pemula: cukup jalankan `docker-compose up --build` dan buka Grafana di browser.
- Login Grafana sudah diatur anonymous, jadi tidak perlu login.
- Untuk menambah/ubah dashboard, edit file di folder `dashboards/`.

---

## 📚 Referensi & Dokumentasi Lanjutan

- [Loki Documentation](https://grafana.com/docs/loki/latest/)
- [Promtail Documentation](https://grafana.com/docs/loki/latest/clients/promtail/)
- [Grafana Documentation](https://grafana.com/docs/grafana/latest/)

---

## 👀 Troubleshooting

- Jika log tidak muncul di Grafana:
  - Cek apakah file log aplikasi sudah terisi.
  - Cek status container Promtail dan Loki (`docker-compose logs promtail` / `loki`).
  - Pastikan konfigurasi path log di Promtail sudah benar.

---

Selamat mencoba! 🎉