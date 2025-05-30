# 🐾 Promtail Config untuk Scrape Docker Logs dengan Label

Ini adalah penjelasan per bagian dari konfigurasi `promtail.yaml` kamu 👇

---

## 🧩 Bagian 1: Server & Posisi Log

```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml
````

* 🔌 **`http_listen_port: 9080`** → UI Promtail bisa diakses di port ini.
* 🚫 **`grpc_listen_port: 0`** → gRPC dinonaktifkan (nggak dipakai).
* 📍 **`positions`** → Menyimpan posisi terakhir yang dibaca (biar log nggak dibaca ulang terus).

---

## 📡 Bagian 2: Push Log ke Loki

```yaml
clients:
  - url: http://loki:3100/loki/api/v1/push
```

* 🚀 Promtail akan push log ke Loki melalui endpoint ini.

---

## 🕵️‍♂️ Bagian 3: Scrape Docker Log Berdasarkan Label

```yaml
scrape_configs:
  - job_name: flog_scrape
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
        filters:
          - name: label
            values: ["logging=promtail"]
```

* 🔍 **Docker autodiscovery** → Scan container lewat Docker socket.
* ⏱️ **refresh\_interval: 5s** → Cek container baru setiap 5 detik.
* 🏷️ **Filter label** → Hanya container dengan label `logging=promtail` yang discrape.

---

## 🏷️ Bagian 4: Relabel Metadata Container

```yaml
    relabel_configs:
      - source_labels: ['__meta_docker_container_name']
        regex: '/(.*)'
        target_label: 'container'

      - source_labels: ['__meta_docker_container_log_stream']
        target_label: 'logstream'

      - source_labels: ['__meta_docker_container_label_logging_jobname']
        target_label: 'job'

      - source_labels: ['__meta_docker_container_log_path']
        target_label: '__path__'

      - source_labels: ['__meta_docker_container_label_com_docker_compose_project']
        target_label: 'namespace'
```

* 🧠 Menyulap metadata Docker jadi label yang bisa di-query di Grafana:

  * 🆔 `container` → nama container
  * 💧 `logstream` → stdout/stderr
  * 🔨 `job` → dari label `logging_jobname`
  * 📁 `__path__` → lokasi log file container
  * 🧱 `namespace` → nama project dari docker-compose

---

## 🔬 Bagian 5: Pipeline Processing

#### 📌 Penjelasan Singkat

- json: → extract key-value dari log JSON
- timestamp: → gunakan timestamp di log sebagai waktu log
- match: → drop log kalau ada "GET /healthz" di log
- labels: → menjadikan event dan level sebagai label Loki, bisa kamu filter via {level="error"} di Grafana

```yaml
    pipeline_stages:
      - json:
          expressions:
            loop_id: ""
            event: ""
            endpoint: ""
            timestamp: ""

      - timestamp:
          source: timestamp
          format: RFC3339Nano
```

* 🪄 **`json`** → Ekstrak field dari log JSON (tanpa menjadikan label).
* ⏰ **`timestamp`** → Ambil waktu dari isi log (`timestamp`), bukan waktu scrape.

---

## 🧹 Bagian 6: Filter Log yang Tidak Penting

```yaml
      - match:
          selector: '{job="flog_scrape"}'
          stages:
            - drop:
                expression: "GET /healthz"
```

* 🧽 Buang log yang mengandung `GET /healthz` dari job `flog_scrape` → Biasanya noise dari health check.

---


* Mau bisa query log lebih granular? Tambahkan block `labels:` setelah `json` stage:

  ```yaml
  - labels:
      event: ""
      level: ""
  ```
* Hindari menjadikan `loop_id`, `timestamp`, atau data yang unik sebagai label → bikin cardinality tinggi dan Grafana/Loki jadi berat.


---

✅ **Final Thoughts:**
Konfigurasi ini **sudah clean, production-ready, dan scalable** buat observasi container Python yang logging structured JSON.
