# 🔍 LogQL Query Reference

Este arquivo contém exemplos de queries LogQL úteis para analisar os logs da aplicação Python no Grafana.

## 📋 Queries Básicas

### Ver todos os logs
```logql
{job="python_app_logs"}
```

### Ver logs por nível
```logql
# Apenas errors
{job="python_app_logs"} | json | level = "ERROR"

# Warnings e errors
{job="python_app_logs"} | json | level =~ "WARNING|ERROR"

# Excluir debug logs
{job="python_app_logs"} | json | level != "DEBUG"
```

## 🔍 Queries por Contexto

### Requests HTTP
```logql
# Requests específicos
{job="python_app_logs"} | json | method = "POST"

# Por endpoint
{job="python_app_logs"} | json | path =~ "/api/v1/users.*"

# Por status code
{job="python_app_logs"} | json | status_code != "200"

# Requests lentos (>2 segundos)
{job="python_app_logs"} | json | response_time_ms > 2000
```

### Business Operations
```logql
# User operations
{job="python_app_logs"} | json | msg =~ ".*user.*"

# Order processing
{job="python_app_logs"} | json | operation =~ ".*order.*"

# Authentication events
{job="python_app_logs"} | json | msg =~ ".*authentication.*"

# File uploads
{job="python_app_logs"} | json | filename != ""
```

### Error Analysis
```logql
# Errors específicos
{job="python_app_logs"} | json | error =~ ".*database.*"

# Por user
{job="python_app_logs"} | json | level = "ERROR" | user_id = "1234"

# Security alerts
{job="python_app_logs"} | json | security_alert = "true"
```

## 📊 Queries para Métricas

### Contadores
```logql
# Count por status code
count by (status_code) (
  {job="python_app_logs"} | json | status_code != ""
)

# Count por método HTTP
count by (method) (
  {job="python_app_logs"} | json | method != ""
)

# Error rate
sum(rate(
  {job="python_app_logs"} | json | level = "ERROR" [5m]
))
```

### Performance
```logql
# Average response time
avg(
  avg_over_time(
    {job="python_app_logs"} | json | unwrap response_time_ms [5m]
  )
)

# 95th percentile response time
quantile(0.95,
  {job="python_app_logs"} | json | unwrap response_time_ms
)

# Response time histogram
histogram_quantile(0.95,
  sum(rate(
    {job="python_app_logs"} | json | unwrap response_time_ms [5m]
  )) by (le)
)
```

## 🕐 Queries por Tempo

### Range queries
```logql
# Last 5 minutes
{job="python_app_logs"} | json [5m]

# Last hour
{job="python_app_logs"} | json [1h]

# Specific time range (use Grafana time picker)
{job="python_app_logs"} | json
```

### Rate queries
```logql
# Request rate per second
rate({job="python_app_logs"} | json | path != "" [1m])

# Error rate per minute  
rate({job="python_app_logs"} | json | level = "ERROR" [5m])
```

## 🔧 Queries Avançadas

### Multi-line logs
```logql
# Logs com stack traces
{job="python_app_logs"} | json | msg =~ "(?s).*Traceback.*"
```

### Pattern matching
```logql
# Extract order IDs
{job="python_app_logs"} | json | line_format "Order: {{.order_id}}"

# Extract user patterns
{job="python_app_logs"} | json | 
  regexp "user_(?P<user_type>\\w+)_(?P<user_id>\\d+)"
```

### Complex filtering
```logql
# Failed orders with high value
{job="python_app_logs"} | json |
  operation =~ ".*order.*" |
  level = "ERROR" |
  unwrap amount | amount > 100
```

## 📋 Alerting Queries

### Error thresholds
```logql
# Error rate > 5%
(
  sum(rate({job="python_app_logs"} | json | level = "ERROR" [5m]))
  /
  sum(rate({job="python_app_logs"} | json [5m]))
) > 0.05
```

### Performance alerts
```logql
# Average response time > 2 seconds
avg(
  avg_over_time(
    {job="python_app_logs"} | json | unwrap response_time_ms [5m]
  )
) > 2000
```

### Security alerts
```logql
# Failed authentication attempts
increase(
  {job="python_app_logs"} | json |
  msg =~ ".*authentication.*" |
  level = "WARNING" [10m]
) > 5
```

## 💡 Tips para Grafana

### Dashboard Variables
- `$interval`: Para rate queries dinâmicas
- `$__range`: Para ranges automáticos  
- `$container`: Para filtrar por container

### Panel Types
- **Time Series**: Para métricas ao longo do tempo
- **Logs**: Para visualizar logs raw
- **Stat**: Para valores únicos (error count, etc)
- **Table**: Para dados tabulares
- **Heatmap**: Para distribuições

### Best Practices
1. Use labels eficientemente
2. Evite regex complexos em queries frequentes
3. Use rate() para métricas de throughput
4. Combine múltiplas queries para dashboards ricos
5. Configure alertas baseados em SLIs/SLOs

## 🚀 Queries de Exemplo para Dashboard

### Overview Panel
```logql
# Total requests
sum(rate({job="python_app_logs"} | json | path != "" [5m]))

# Error rate %
(
  sum(rate({job="python_app_logs"} | json | level = "ERROR" [5m]))
  /
  sum(rate({job="python_app_logs"} | json [5m]))
) * 100
```

### Business Metrics
```logql
# Successful user registrations
sum(rate(
  {job="python_app_logs"} | json |
  msg =~ ".*registration successful.*" [5m]
))

# Order conversion rate
(
  sum(rate({job="python_app_logs"} | json | msg =~ ".*order.*successful.*" [5m]))
  /
  sum(rate({job="python_app_logs"} | json | operation =~ ".*order.*" [5m]))
) * 100
```

---

## 📖 Referências

- [LogQL Documentation](https://grafana.com/docs/loki/latest/logql/)
- [Grafana Dashboard Best Practices](https://grafana.com/docs/grafana/latest/best-practices/)
- [Loki Query Examples](https://grafana.com/docs/loki/latest/logql/query_examples/)
