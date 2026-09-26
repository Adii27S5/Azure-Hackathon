# Azure Load Testing for a Web Application Capacity Study
## Project ID: 24CC3046-P056 | Team: T158

An empirical performance engineering and cloud capacity study conducted on **Microsoft Azure** using **Azure Load Testing**, **Apache JMeter**, and **Azure Monitor**.

---

## 1. Team Information

| S. No. | Student ID | Name | Role & Core Contribution |
|---|---|---|---|
| 1 | **2400032012** | KORADA TEJA | Cloud Infrastructure, Azure App Service Deployment, Packaging |
| 2 | **2400032102** | GUBBALA LAKSHMI SAI TEJA | PostgreSQL Flexible Server, Schema Design, VNet Peering |
| 3 | **2400032152** | ADITYA SINGH | DevOps Automation, CI/CD Pipeline, JMeter Test Execution & Analysis |
| 4 | **2400032605** | GOLLA MANIKANTA | Application Insights APM, Log Analytics, Azure Monitor Autoscale |

---

## 2. Problem Statement
Cloud applications subject to dynamic demand often face sudden latency spikes or service outages when virtual user concurrency exceeds the capacity of the underlying infrastructure. This study empirically determines the capacity boundaries, locates the latency knee, identifies the saturation breaking point under a single Standard S1 compute core, and investigates horizontal scale-out behavior on Microsoft Azure.

---

## 3. Architecture & Cloud Topology

```
                            [Azure Load Testing: alt-loadtest-101]
                                              |
                                              | HTTPS / Port 443 (Distributed Load)
                                              v
                         +------------------------------------------+
                         |    Azure App Service: app-loadtest-101   |
                         |   - Plan: plan-loadtest (Standard S1)    |
                         |   - Node.js 24 LTS Express API & UI      |
                         |   - Autoscale: autoscale-plan-loadtest   |
                         +------------------------------------------+
                                 |                          |
       SQL Queries / Port 5432   |                          | Telemetry / APM
     (Private VNet: 10.0.1.0/24) |                          | (Instrumentation Key)
                                 v                          v
    +----------------------------------------+   +------------------------------------+
    | PostgreSQL: app-loadtest-101-server    |   | Application Insights:              |
    | - Database: db-loadtest-101            |   | appi-loadtest-101                  |
    | - Subnet: subnet-ejdigsdaswpw4         |   | - Log Analytics: law-loadtest-101  |
    | - Private IP: 10.0.2.4 (Private DNS)   |   | - Live Metrics & Dependency Map    |
    +----------------------------------------+   +------------------------------------+
```

---

## 4. Discovered & Verified Azure Resources

All resources are deployed and verified in resource group **`rg-loadtest`** (Central India):

| Azure Service | Actual Name | SKU / Configuration | Role & Networking |
|:---|:---|:---|:---|
| **App Service** | `app-loadtest-101` | Linux Node.js 24 LTS | [Live Production Web App](https://app-loadtest-101-byh7hsbwbyemh7bg.centralindia-01.azurewebsites.net) |
| **App Service Plan**| `plan-loadtest` | Standard S1 (1 Core, 1.75 GB) | Autoscale 1-4 workers |
| **PostgreSQL Server**| `app-loadtest-101-server` | Standard_D2s_v3 (v14) | Delegated `subnet-ejdigsdaswpw4` |
| **PostgreSQL Database**| `db-loadtest-101` | Relational Store | Seeded: 100 users, 500 products, 6.4k orders |
| **Virtual Network** | `vnet-qkjgcmgm` | 10.0.0.0/16 | Subnets: `subnet-aaahsuqi` & `subnet-ejdigsdaswpw4` |
| **Private DNS Zone** | `privatelink.postgres.database.azure.com`| Zone A Record (`10.0.2.4`)| Zero-trust private routing |
| **Azure Load Testing**| `alt-loadtest-101` | Cloud Load Engine | Test: `capacity-study-test` |
| **Application Insights**| `appi-loadtest-101` | Workspace-based APM | Real-time telemetry & Live Metrics |
| **Log Analytics** | `law-loadtest-101` | PerGB2018 | Centralized log ingestion |
| **Autoscale Rules** | `autoscale-plan-loadtest` | Metric Rule Set | Scale-out: CPU > 70%; Scale-in: CPU < 30% |
| **Azure Dashboard** | `capacity-performance-dashboard` | Portal Dashboard | 6 performance metric tiles |

---

## 5. Deployment & CI/CD Pipeline

- **GitHub Actions Workflow**: `.github/workflows/deploy-app-loadtest-101.yml`
- **Continuous Integration**:
  - Triggers automatically on push to `main`.
  - Runs `npm install` and executes 8 self-contained API tests (`npm test` -> 8/8 passed in 9s).
  - Deploys clean POSIX deployment bundle directly to Azure App Service via OIDC.
- **Latest Verified CI Runs**: [`36271169628`](https://github.com/Adii27S5/Azure-Hackathon/actions/runs/36271169628), [`36271744461`](https://github.com/Adii27S5/Azure-Hackathon/actions/runs/36271744461) (100% Success).

---

## 6. Verified API Endpoints

- `GET /health`: Liveness probe and live node telemetry (`{"status":"healthy","database":{"status":"connected"}}`).
- `GET /api/products`: Catalog browsing (`LIMIT 20`).
- `GET /api/products/1`: Single product lookup by primary key.
- `GET /api/search?q=laptop`: Full-text pattern matching SQL query.
- `GET /api/dashboard`: Cross-table SQL aggregation (`total_users`, `total_products`, `total_orders`, `total_revenue`).
- `GET /api/orders`: Order history retrieval.
- `POST /api/orders`: Transactional write persisting order header and line items.
- `GET /api/heavy-operation`: Compute stressor executing 50,000 cryptographic hash iterations.
- `GET /`: Production web application and capacity dashboard.

---

## 7. Empirical Load Testing Results Matrix

All metrics below were extracted directly from the actual test runs executed by `alt-loadtest-101`:

| Test Run ID | Users | Inst | RPS | Avg (ms) | P50 (ms) | P95 (ms) | P99 (ms) | Errors | Error % | CPU % | Operational Assessment |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| `run-1-baseline-10u-v2` | 10 | 1 | 110.7 | 83.0 | 33.0 | 310.0 | 580.0 | 0 | 0.00% | 17.7% | **PASS - Optimal Capacity** |
| `run-2-light-50u-v2` | 50 | 1 | 144.9 | 285.0 | 122.0 | 1022.0 | 1943.0 | 0 | 0.00% | 38.0% | **PASS - Linear Scaling** |
| `run-3-medium-100u-v2` | 100 | 1 | 175.9 | 489.0 | 227.0 | 1800.0 | 4530.0 | 0 | 0.00% | 58.2% | **PASS - Safe Operating Knee** |
| `run-4-heavy-250u-v2` | 250 | 1 | 177.2 | 1176.0 | 341.0 | 7257.0 | 15010.0 | 549 | 2.42% | 78.5% | **BREACH - Queueing & Degradation** |
| `run-5-stress-500u-v2` | 500 | 1 | 184.5 | 2365.0 | 291.0 | 15010.0 | 15010.0 | 1305 | 5.66% | **96.4%** | **SATURATION BREAKING POINT** |
| `run-6-scaled-2inst-500u` | 500 | 2 | 137.2 | 3046.0 | 1428.0 | 15010.0 | 15020.0 | 1783 | 9.92% | **49.1%** | **CPU RELIEVED / COLD-START QUEUE** |

---

## 8. Key Engineering Findings

1. **Safe Operating Boundary**: Up to **100 concurrent virtual users**, a single Standard S1 instance maintains 0.00% errors, 175.9 RPS, and sub-500ms average latency with 58.2% CPU utilization.
2. **Knee of the Curve**: At **250 virtual users**, throughput plateaus (~177 RPS) while P95 latency escalates to 7,257 ms, generating 2.42% errors as CPU approaches 80%.
3. **Saturation Breaking Point**: At **500 virtual users** on 1 instance, CPU reaches **96.4% sustained saturation**, socket queues overflow, and P95 latency hits the 15.01s socket timeout boundary with 5.66% errors.
4. **2-Instance Scale-Out Investigation**: Scaling out to 2 instances halved per-instance CPU load from **96.4% to 49.1%** (compute relief). However, aggregate error rate rose to 9.92% because ARR routed traffic to the 2nd instance during container cold-start warmup before DB pool priming. This proves that horizontal scaling must be paired with application initialization warmup probes.

---

## 9. Frontend Storefront & Telemetry Modal

The repository includes a dedicated E-Commerce storefront located in `frontend/`:
- **Live Azure Backend Connection**: Points directly to `app-loadtest-101`.
- **Interactive Azure Telemetry Modal**: Displays active container instance hash, round-trip ping latency, PostgreSQL connection status, and the capacity study matrix.
- **Live Benchmark Trigger**: Runs real-time `GET /api/heavy-operation` (50,000 hash cycles) from the browser.
- **Backend Target Switcher**: Allows toggling between Live Azure Cloud and Localhost.

---

## 10. Deliverables & Reports

- **Comprehensive Report**: [`capacity_study_report.md`](capacity_study_report.md) (All 26 detailed sections)
- **Word Document**: [`reports/Azure-Load-Testing-Capacity-Study-Report.docx`](reports/Azure-Load-Testing-Capacity-Study-Report.docx)
- **PDF Report**: [`reports/Azure-Load-Testing-Capacity-Study-Report.pdf`](reports/Azure-Load-Testing-Capacity-Study-Report.pdf)
- **Presentation Deck**: [`reports/Azure-Load-Testing-Capacity-Study-Presentation.pptx`](reports/Azure-Load-Testing-Capacity-Study-Presentation.pptx) (25 widescreen slides)
- **Datasets**: [`results/final_capacity_matrix.csv`](results/final_capacity_matrix.csv), [`results/performance-results.csv`](results/performance-results.csv), [`results/transaction-breakdown.csv`](results/transaction-breakdown.csv)
- **Performance Graphs**: High-resolution PNG plots in [`reports/graphs/`](reports/graphs/)
- **Evidence Catalog**: [`screenshots/SCREENSHOT_EVIDENCE_CATALOG.md`](screenshots/SCREENSHOT_EVIDENCE_CATALOG.md)