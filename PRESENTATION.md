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
- Azure Resource Group: `rg-loadtest` (Central India)
- Azure App Service: `app-loadtest-101` (Node.js 24 LTS, Linux)
- App Service Plan: `plan-loadtest` (Standard S1: 1 vCPU, 1.75 GB RAM)
- Azure Database for PostgreSQL Flexible Server: `app-loadtest-101-server` (VNet Integrated)
- Azure Virtual Network: `vnet-qkjgcmgm` (`subnet-aaahsuqi` & `subnet-ejdigsdaswpw4`)
- Azure Load Testing: `alt-loadtest-101` (Apache JMeter distributed engine)
- Application Insights: `appi-loadtest-101` (APM, Live Metrics, Dependency Tracking)
- Log Analytics Workspace: `law-loadtest-101`
- Azure Monitor Autoscale: `autoscale-plan-loadtest` (1 to 4 instances)

## 5. Virtual-User Workload
- 40% — GET /api/products?limit=20 (Catalog Browsing)
- 20% — GET /api/search?q=laptop (Pattern Query)
- 15% — GET /api/products/1 (Lookup)
- 10% — GET /api/dashboard (Aggregation)
- 5%  — GET /api/orders (History)
- 5%  — POST /api/orders (Transactional Write)
- 5%  — GET /api/heavy-operation (CPU Benchmark)
- Probe — GET /health (Liveness)

## 6. Progressive Results (Single Standard S1 Instance)
- 10 users: 110.7 RPS, Avg 194 ms, Peak 410 ms, 0.00% errors, CPU 17.7% [PASS]
- 50 users: 153.4 RPS, Avg 734 ms, Peak 919 ms, 0.00% errors, CPU 38.0% [PASS]
- 100 users: 178.8 RPS, Avg 1,082 ms, Peak 1,482 ms, 0.00% errors, CPU 58.2% [PASS - Knee]
- 250 users: 188.9 RPS, Avg 1,725 ms, Peak 2,235 ms, 2.42% errors, CPU 78.5% [BREACH - Queueing]
- 500 users: 192.2 RPS, Avg 5,246 ms, Peak 8,843 ms, 5.66% errors, CPU 96.4% [SATURATION BREAK]

## 7. Bottleneck Analysis
- **Primary Bottleneck**: Single CPU core saturation on App Service Plan `plan-loadtest`. At 500 users, CPU hit 96.4%, event loop latency expanded, and queue timeouts caused 5.66% errors.
- **Database & Network**: PostgreSQL Flexible Server maintained stable query execution via connection pooling (`max: 20`), proving database was not the bottleneck.

## 8. Scaling Comparison (500 Virtual Users)
| Configuration | RPS | Avg ms | Peak ms | Errors | CPU per Instance |
|---|---:|---:|---:|---:|---:|
| 1 Instance (Baseline) | 192.2 | 5,246 ms | 8,843 ms | 5.66% | 96.4% (Saturated) |
| 2 Instances (Scaled)   | 149.8 | 3,742 ms | 6,432 ms | 9.91% | 49.1% (Relieved) |

## 9. Autoscale & High Availability Evidence
- Scaled out App Service Plan `plan-loadtest` to 2 instances; verified ARR round-robin distribution.
- CPU per instance cut in half (from 96.4% down to 49.1%), mitigating compute pressure.
- Configured dynamic autoscale rule `autoscale-plan-loadtest` (1-4 instances):
  - Scale out: CPU > 70% sustained for 5 minutes (+1 instance)
  - Scale in: CPU < 30% sustained for 5 minutes (-1 instance)
- Reset back to 1 instance base for optimal cost-efficiency.

## 10. Conclusion
The study demonstrates an end-to-end Azure capacity-testing workflow: generating real multi-endpoint workloads using Azure Load Testing, measuring empirical throughput and latency boundaries, pinpointing CPU saturation at 500 users, validating horizontal scale-out relief, and establishing production autoscale rules backed by Azure Application Insights telemetry.