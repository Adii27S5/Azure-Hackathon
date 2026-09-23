# Azure Load Testing for a Web Application Capacity Study — Presentation Content

**Project ID:** 24CC3046-P056  
**Team:** T158

## Team Members
- 2400032012 — KORADA TEJA
- 2400032102 — GUBBALA LAKSHMI SAI TEJA
- 2400032152 — ADITYA SINGH
- 2400032605 — GOLLA MANIKANTA

## 1. Objective
Determine the observed capacity boundary of the current application configuration and recommend a scalable Azure configuration based on measured results.

## 2. Problem Statement
A web application may perform well at normal traffic but become slow or resource-constrained as concurrent workload increases. The study identifies where the tested configuration approaches its resource boundary and evaluates horizontal scaling.

## 3. Architecture
Azure Load Testing → Azure App Service → Azure PostgreSQL  
Application Insights + Azure Monitor → Metrics and telemetry  
Azure Autoscale → Scale-out / scale-in

## 4. Services
- Azure Resource Group
- Azure App Service
- App Service Plan — Standard S1
- Azure Load Testing
- Apache JMeter
- Application Insights
- Azure Monitor
- Azure Autoscale
- Azure Database for PostgreSQL Flexible Server
- Log Analytics Workspace

## 5. Virtual-User Workload
- 40% — GET /api/products?limit=20
- 20% — GET /api/search?q=laptop
- 15% — GET /api/products/1
- 10% — GET /api/dashboard
- 10% — GET /api/orders + POST /api/orders
- 5% — GET /api/heavy-operation
- Continuous — GET /health

## 6. Progressive Results
Single Standard S1 instance:
- 10 users: 130.4 RPS, P95 258 ms, 0% errors, CPU 23%
- 50 users: 129.6 RPS, P95 229 ms, 0% errors, CPU 38%
- 100 users: 118.1 RPS, P95 251 ms, 0% errors, CPU 52%
- 250 users: 116.8 RPS, P95 250 ms, 0% errors, CPU 68%
- 500 users: 109.9 RPS, P95 272 ms, 0% errors, CPU 80%

## 7. Bottleneck
The main observed bottleneck was CPU utilization on the single Standard S1 instance. At 500 users CPU reached 80%, while error rate remained 0% and memory was 76%.

## 8. Scaling Comparison
| Configuration | RPS | Avg ms | P95 ms | P99 ms | Errors | CPU |
|---|---:|---:|---:|---:|---:|---:|
| 1 Instance | 109.9 | 82.6 | 272 | 527 | 0.00% | 80.0% |
| 2 Instances | 73.9 | 122.8 | 436 | 855 | 0.00% | 73.5% |
| 4 Instances | 139.8 | 64.8 | 239 | 513 | 0.01% | 52.3% |

## 9. Autoscale Evidence
- Scale up: 2 → 3, Succeeded
- Scale down: 3 → 2, Succeeded
- Scale down: 2 → 1, Succeeded

## 10. Conclusion
The study demonstrates an end-to-end Azure capacity-testing workflow: generate controlled load, measure performance, identify the CPU boundary, scale the App Service horizontally, repeat the same workload, compare actual measurements, and verify autoscaling through Azure Monitor Activity Logs.