Berikut penjelasan tiap section dari Loki config minimal yang tadi 👇 (dengan emoji biar lebih enak dibaca):

---

```yaml
auth_enabled: false
```

🔓 **auth\_enabled**

* Disable autentikasi HTTP.
* Cocok untuk dev/local.
* Kalau production → pakai `true` + proxy dengan auth.

---

```yaml
server:
  http_listen_port: 3100
  grpc_listen_port: 9095
```

🖥️ **server**

* `http_listen_port`: port REST API Loki, default 3100.
* `grpc_listen_port`: port komunikasi internal antar komponen (tidak wajib 9095, asal konsisten).

---

```yaml
ingester:
  lifecycler:
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1
  chunk_idle_period: 5m
  max_chunk_age: 1h
  chunk_retain_period: 30s
```

📦 **ingester**

* Menangani penerimaan dan buffering log sebelum disimpan.
* `kvstore: inmemory`: cocok untuk single instance.
* `replication_factor: 1`: gak ada cluster/HA.
* `chunk_idle_period`: chunk di-flush kalau idle 5m.
* `max_chunk_age`: chunk di-flush maksimal 1 jam.
* `chunk_retain_period`: waktu tunggu sebelum chunk dihapus (agar client sempat ambil ulang jika perlu).

---

```yaml
schema_config:
  configs:
    - from: 2022-01-01
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h
```

📘 **schema\_config**

* Format & sistem penyimpanan log/index.
* `boltdb-shipper` + `filesystem`: cocok untuk local.
* `v11`: versi schema terbaru.
* `index.period: 24h`: Loki bikin index harian.

---

```yaml
storage_config:
  boltdb_shipper:
    active_index_directory: /loki/index
    cache_location: /loki/index_cache
    shared_store: filesystem

  filesystem:
    directory: /loki/chunks
```

💾 **storage\_config**

* Tempat simpan index dan data log.
* Simpan semua ke folder `/loki` (pastikan dimount di Docker).
* **Notes**:

  * `index`: buat nyari log cepat.
  * `chunks`: log sebenarnya.

---

```yaml
limits_config:
  reject_old_samples: true
  reject_old_samples_max_age: 168h
```

⛔ **limits\_config**

* Menolak log yang timestamp-nya terlalu lama (>7 hari).
* Biar tidak ada "backfill" data yang bisa merusak konsistensi index.

---

```yaml
chunk_store_config:
  max_look_back_period: 168h
```

🔍 **chunk\_store\_config**

* Batas maksimal pencarian log ke belakang (7 hari).
* Sesuaikan dengan retention yang kamu mau.

---

```yaml
table_manager:
  retention_deletes_enabled: true
  retention_period: 168h
```

🗑️ **table\_manager**

* Aktifkan auto delete log yang udah lewat 7 hari.
* Ini "retention policy" beneran — log lama dihapus otomatis.

---

Kalau kamu mount volume ke `./loki-data:/loki` di Docker Compose, maka semua data Loki (index & chunk) akan persistent.

---

Siap pakai untuk:

* Dev
* Demo
* POC
* Logging 1–3 container

Kalau udah skala besar, nanti naikkan ke HA + S3 atau GCS.
