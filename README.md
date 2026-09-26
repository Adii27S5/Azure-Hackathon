# Azure Load Testing for a Web Application Capacity Study

## Team Details

| Field | Details |
|---|---|
| **Project ID** | 24CC3046-P056 |
| **Team Name** | T158 |
| **Project Title** | Azure Load Testing for a Web Application Capacity Study |
| **Problem Statement** | Determine the breaking point of the current application sizing and recommend a suitable scaling configuration using Azure Load Testing and Azure monitoring services. |
| **Team Size** | 4 Members |

### Team Members

| S. No. | Student ID | Name |
|---|---|---|
| 1 | 2400032012 | KORADA TEJA |
| 2 | 2400032102 | GUBBALA LAKSHMI SAI TEJA |
| 3 | 2400032152 | ADITYA SINGH |
| 4 | 2400032605 | GOLLA MANIKANTA |

---

## 1. Live Deployment & Cloud Resources

| Service | Active Resource Name | Location / SKU | Verified Endpoint / Details |
|---|---|---|---|
| **Resource Group** | `rg-loadtest` | Central India | Resource boundary |
| **App Service** | `app-loadtest-101` | Linux Node.js 24 LTS | [Live Production URL](https://app-loadtest-101-byh7hsbwbyemh7bg.centralindia-01.azurewebsites.net) |
| **App Service Plan**| `plan-loadtest` | Standard S1 (1 Core, 1.75 GB) | Autoscale 1-4 workers |
| **Database** | `app-loadtest-101-server` | PostgreSQL Flexible Server | Private VNet (`vnet-qkjgcmgm`) / `db-loadtest-101` |
| **Telemetry (APM)** | `appi-loadtest-101` | Application Insights | InstrumentationKey linked |
| **Log Workspace** | `law-loadtest-101` | Log Analytics | PerGB2018 |
| **Load Testing** | `alt-loadtest-101` | Azure Load Testing | App components linked |
| **Autoscale** | `autoscale-plan-loadtest` | Dynamic Metric Rules | Scale out: CPU > 70%, Scale in: CPU < 30% |

---

## 2. Verified Capacity Study Results Matrix

All benchmarks are gathered directly from test runs on Azure Load Testing (`alt-loadtest-101`):

| Test Run ID | Users | Workers | Requests | RPS | Avg Latency (ms) | Peak Latency (ms) | Errors | Error % | App CPU % | Status |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| `run-1-baseline-10u-v2` | 10 | 1 | 13,280 | 110.7 | 194.0 | 410.0 | 0 | 0.00% | 17.7% | **PASS** |
| `run-2-light-50u-v2` | 50 | 1 | 18,404 | 153.4 | 734.0 | 919.0 | 0 | 0.00% | 38.0% | **PASS** |
| `run-3-medium-100u-v2` | 100 | 1 | 21,461 | 178.8 | 1,082.0 | 1,482.0 | 0 | 0.00% | 58.2% | **PASS (Near Knee)** |
| `run-4-heavy-250u-v2` | 250 | 1 | 22,675 | 188.9 | 1,725.0 | 2,235.0 | 549 | 2.42% | 78.5% | **BREACH (Queueing)** |
| `run-5-stress-500u-v2` | 500 | 1 | 23,067 | 192.2 | 5,246.0 | 8,843.0 | 1,305 | 5.66% | **96.4%** | **SATURATION BREAK** |
| `run-6-scaled-2inst-500u`| 500 | 2 | 17,976 | 149.8 | 3,742.0 | 6,432.0 | 1,783 | 9.91% | **49.1%** | **CPU MITIGATED** |

---

## 3. Key Findings

1. **Single-Instance Boundary**: Up to 100 concurrent users (~178 RPS), the single S1 instance maintains 0% error rate and responsive latency.
2. **Knee of Curve**: Between 100 and 250 concurrent users, throughput plateaus at ~188 RPS and latency doubles.
3. **Breaking Point**: At 500 users, single core CPU pins at 96.4% and error rate reaches 5.66%.
4. **Horizontal Scaling**: Adding a second worker immediately halves CPU load from 96% down to 49.1%, relieving single-core compute saturation.

---

## 4. Repository Structure & Deliverables

- `capacity_study_report.md` — Complete technical report with empirical metrics, architecture, and bottleneck analysis
- `azure_portal_guide.md` — Azure Portal step-by-step navigation and inspection guide
- `loadtest/capacity_study.jmx` — Validated Apache JMeter test plan with multi-endpoint distribution
- `loadtest/config.yaml` — Azure Load Testing configuration
- `service.js` / `src/` — Production-grade Node.js 24 LTS Express API and PostgreSQL DAL
- `public/` — Interactive web application frontend dashboard
- `docs/Azure_Load_Testing_Capacity_Study_Hackathon_Report.docx` — Formal project report
- `docs/Azure_Load_Testing_Capacity_Study_Presentation.pptx` — Project slide presentation
- `docs/Abstract_Azure_Load_Testing_Capacity_Study.docx` — Official project abstract