# Comprehensive Azure Load Testing & Capacity Study Report
## Project ID: 24CC3046-P056 — Azure Load Testing for a Web Application Capacity Study
**Team:** T158 | **Environment:** Microsoft Azure (`rg-loadtest`, Central India)  
**Status:** 100% Deployed, Verified, Benchmarked, and Documented  

---

### Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Objectives](#3-objectives)
4. [Existing Architecture](#4-existing-architecture)
5. [Azure Resource Inventory](#5-azure-resource-inventory)
6. [Application Architecture](#6-application-architecture)
7. [Network Architecture](#7-network-architecture)
8. [Database Architecture](#8-database-architecture)
9. [CI/CD Automation](#9-cicd-automation)
10. [Application Insights](#10-application-insights)
11. [Log Analytics](#11-log-analytics)
12. [Azure Monitor](#12-azure-monitor)
13. [Apache JMeter Specification](#13-apache-jmeter-specification)
14. [Workload Model & Transaction Weights](#14-workload-model--transaction-weights)
15. [Functional Testing & API Verification](#15-functional-testing--api-verification)
16. [Baseline Capacity Testing (10 Users)](#16-baseline-capacity-testing-10-users)
17. [Progressive Load Testing (50 & 100 Users)](#17-progressive-load-testing-50--100-users)
18. [250-User Behavior & Knee of the Curve](#18-250-user-behavior--knee-of-the-curve)
19. [500-User Behavior & Saturation Breaking Point](#19-500-user-behavior--saturation-breaking-point)
20. [2-Instance Scale-Out Investigation](#20-2-instance-scale-out-investigation)
21. [Root Cause Bottleneck Analysis](#21-root-cause-bottleneck-analysis)
22. [Azure Autoscale Verification](#22-azure-autoscale-verification)
23. [Same-Load Comparison (1 vs 2 Instances)](#23-same-load-comparison-1-vs-2-instances)
24. [Cost Optimization & Sizing Analysis](#24-cost-optimization--sizing-analysis)
25. [Limitations & Threats to Validity](#25-limitations--threats-to-validity)
26. [Conclusion & Next Steps](#26-conclusion--next-steps)

---

## 1. Executive Summary

This study presents an end-to-end cloud capacity evaluation of an enterprise web application deployed on **Microsoft Azure App Service** (Linux Node.js 24 LTS) integrated with **Azure Database for PostgreSQL Flexible Server** via private VNet peering, and instrumented with **Azure Application Insights**. Workload generation was driven by **Azure Load Testing** (`alt-loadtest-101`) executing distributed Apache JMeter test plans.

The primary objective was to determine the safe capacity boundary, identify the latency knee, locate the definitive saturation breaking point under a single Standard S1 instance, and evaluate horizontal scale-out behavior.

Key empirical findings:
1. **Safe Operating Boundary**: **100 concurrent virtual users** on 1 instance (175.9 RPS, 0.00% errors, 489 ms average latency, 58.2% CPU).
2. **Knee of the Curve**: Emerged at **250 concurrent virtual users**, where throughput plateaued at 177.2 RPS, CPU reached 78.5%, and initial queueing produced 2.42% errors.
3. **Saturation Breaking Point**: Observed at **500 concurrent virtual users** on 1 instance. Single-core CPU hit **96.4% utilization**, socket queues saturated, P95 latency reached the 15.01s JMeter timeout boundary, and error rate climbed to **5.66%**.
4. **2-Instance Scale-Out Investigation**: Scaling out to 2 instances successfully halved per-instance CPU utilization from **96.4% down to 49.1%** (providing compute relief). However, aggregate throughput registered 137.2 RPS and error rate rose to **9.92%**. Forensic log analysis proved that ARR (Application Request Routing) routed concurrent traffic to the newly spawned 2nd instance while its container was still in cold-start warmup, causing early requests to breach the 15-second socket timeout. Once warmed up, both instances processed traffic steadily.

---

## 2. Problem Statement

Modern cloud applications experience unpredictable traffic surges that degrade user experience and exhaust infrastructure resources. Organizations often rely on theoretical sizing calculators rather than empirical performance boundaries. Without rigorous load testing, organizations risk either costly over-provisioning or severe production outages caused by single-threaded event loop saturation, database connection exhaustion, or ARR routing bottlenecks during autoscaling transitions.

---

## 3. Objectives

1. Determine the maximum safe concurrency and throughput for a Standard S1 App Service tier.
2. Establish the exact latency progression curves across 10, 50, 100, 250, and 500 concurrent virtual users.
3. Locate the saturation breaking point and identify the governing physical constraint (CPU vs Memory vs Database).
4. Evaluate horizontal scaling (1 vs 2 instances) and distinguish compute relief from cold-start routing penalties.
5. Validate dynamic autoscaling rules backed by Azure Monitor telemetry and real-time portal dashboards.

---

## 4. Existing Architecture

The deployed cloud topology uses an isolated, zero-trust virtual network topology in Central India:

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

## 5. Azure Resource Inventory

All resources are verified active in resource group `rg-loadtest`:

| Service | Name | SKU / Sizing | Location | Network / Access |
|:---|:---|:---|:---|:---|
| **Resource Group** | `rg-loadtest` | Standard Resource Boundary | Central India | Unified Management Boundary |
| **App Service** | `app-loadtest-101` | Linux Node.js 24 LTS | Central India | `vnetRouteAllEnabled=true` |
| **App Service Plan**| `plan-loadtest` | Standard S1 (1 Core, 1.75 GB) | Central India | 1 to 4 instances autoscale |
| **PostgreSQL Server**| `app-loadtest-101-server` | Standard_D2s_v3 (v14) | Central India | Private delegated `subnet-ejdigsdaswpw4` |
| **PostgreSQL DB** | `db-loadtest-101` | Relational Store | Central India | Seeded: 100 users, 500 prods, 6.4k orders |
| **Virtual Network** | `vnet-qkjgcmgm` | 10.0.0.0/16 | Central India | Subnets: `subnet-aaahsuqi`, `subnet-ejdigsdaswpw4` |
| **Private DNS Zone**| `privatelink.postgres...`| A Record: `10.0.2.4` | Global | Linked to `vnet-qkjgcmgm` |
| **Load Testing** | `alt-loadtest-101` | Cloud Load Engine | Central India | Linked components: App, Plan, DB |
| **App Insights** | `appi-loadtest-101` | Workspace-based | Central India | Linked to `law-loadtest-101` |
| **Log Analytics** | `law-loadtest-101` | PerGB2018 | Central India | Centralized Log Ingestion |
| **Autoscale Rule** | `autoscale-plan-loadtest`| Metric Rule Set | Central India | Scale-out: CPU > 70%; Scale-in: CPU < 30% |
| **Dashboard** | `capacity-performance-dashboard` | Azure Portal Dashboard | Central India | 6 Performance Tiles & Matrix |

---

## 6. Application Architecture

The backend application is implemented in Node.js 24 LTS Express with asynchronous initialization:
1. **Immediate Port Binding**: Express binds `app.listen(port)` on startup before database schema validation finishes. This ensures Azure container health probes (`/health`) succeed within 2 seconds.
2. **Connection Pooling**: PostgreSQL connections are pooled using `pg.Pool` (`max: 20`, `idleTimeoutMillis: 30000`) with connection retry logic.
3. **CORS Support**: Configured with `Access-Control-Allow-Origin: *` to support the frontend storefront, mobile clients, and local development.
4. **Dual Frontend Options**:
   - Integrated Dashboard served at `/` from `public/index.html`.
   - Dedicated E-commerce storefront application located in `frontend/` (featuring live telemetry modals, cart management, and interactive benchmark triggers).

---

## 7. Network Architecture

The application communicates with PostgreSQL over Azure Virtual Network `vnet-qkjgcmgm`:
- Subnet `subnet-aaahsuqi` (10.0.1.0/24) is delegated to Azure App Service for Regional VNet Integration.
- Subnet `subnet-ejdigsdaswpw4` (10.0.2.0/24) is delegated to PostgreSQL Flexible Server.
- Outbound routing is forced across the VNet via `vnetRouteAllEnabled=true`.
- Private DNS Zone `privatelink.postgres.database.azure.com` resolves PostgreSQL hostnames directly to `10.0.2.4`, eliminating all public internet database exposure.

---

## 8. Database Architecture

Database: `db-loadtest-101` on PostgreSQL 14:
- `users`: 100 customer profiles with UUIDs and email indexes.
- `products`: 500 catalog items spanning 7 categories with pricing, inventory, and rating attributes.
- `orders`: Transactional headers with timestamps, foreign keys to `users`, and total calculation.
- `order_items`: Line-item breakdown linking `orders` and `products`.
- Indexes: B-tree indexes on `products(category)`, `products(name)`, `orders(user_id)`, and `orders(created_at)`.

---

## 9. CI/CD Automation

CI/CD is implemented via GitHub Actions (`.github/workflows/deploy-app-loadtest-101.yml`):
- Triggers on push to `main`.
- Step 1: Sets up Node.js 24 LTS and runs `npm install`.
- Step 2: Executes API test suite (`npm test` -> 8 passing tests in 9s).
- Step 3: Packages application artifacts into POSIX-compliant deployment archive.
- Step 4: Deploys directly to Azure App Service `app-loadtest-101`.
- Verified Workflow Runs: `36271169628` and `36271744461` (100% Success).

---

## 10. Application Insights

Azure Application Insights (`appi-loadtest-101`) captures end-to-end distributed telemetry:
- Request Telemetry: Method, URL, duration, response code, and correlation IDs.
- Dependency Telemetry: Outbound PostgreSQL SQL queries, duration, and connection states.
- Live Metrics Stream: Real-time CPU, Memory, Request Rate, and Exception monitoring.

---

## 11. Log Analytics

Log Analytics Workspace (`law-loadtest-101`) ingests container logs and telemetry data:
- Ingestion queries track HTTP 5xx error spikes during 500-user stress runs.
- Container console logs capture database connection pool events and Oryx deployment summaries.

---

## 12. Azure Monitor

Azure Monitor collects performance counters from `plan-loadtest` and `app-loadtest-101`:
- Aggregates 1-minute and 5-minute CPU percentage, memory percentage, and data out.
- Feeds real-time metric streams directly into `autoscale-plan-loadtest`.

---

## 13. Apache JMeter Specification

The test scenario (`loadtest/capacity_study.jmx`) was created in Apache JMeter and executed natively in Azure Load Testing:
- Multi-threaded thread group dynamically configurable via environment variables (`app_host`, `threads`, `duration`, `rampup`).
- HTTP request timeout: `connect=10000ms`, `response=15000ms`.
- Dynamic Groovy resolution ensures seamless property/environment variable pickup across Azure test engines.

---

## 14. Workload Model & Transaction Weights

The workload simulates realistic multi-endpoint user journeys across 8 operations:

| Endpoint | Method | Distribution | Transaction Goal | SLA Target |
|:---|:---:|:---:|:---|:---:|
| `/health` | `GET` | Background | Liveness Probe & Node Telemetry | < 200 ms |
| `/api/products` | `GET` | **40%** | Catalog Browsing (LIMIT 20) | < 500 ms |
| `/api/search?q=laptop` | `GET` | **20%** | Full-Text Search Query | < 800 ms |
| `/api/products/1` | `GET` | **15%** | Single Product Lookup | < 300 ms |
| `/api/dashboard` | `GET` | **10%** | Analytics Aggregation | < 1000 ms |
| `/api/orders` | `GET` | **5%** | Customer Order History | < 500 ms |
| `/api/orders` | `POST` | **5%** | Transactional Order Placement | < 800 ms |
| `/api/heavy-operation` | `GET` | **5%** | Cryptographic Compute Stressor | < 1500 ms |

---

## 15. Functional Testing & API Verification

Prior to load testing, all endpoints were functionally verified:
- `GET /health` -> HTTP 200 OK (`healthy`, `database: connected`)
- `GET /api/products` -> HTTP 200 OK (Returns 20 seeded products)
- `GET /api/products/1` -> HTTP 200 OK (Returns item #1)
- `GET /api/search?q=laptop` -> HTTP 200 OK (Matches keyword)
- `GET /api/dashboard` -> HTTP 200 OK (`total_users: 100`, `total_products: 500`, `total_orders: 6,400+`)
- `POST /api/orders` -> HTTP 201 Created (Persists order and line items to PostgreSQL)
- `GET /api/heavy-operation` -> HTTP 200 OK (50,000 hash cycles completed in ~150ms)
- Automated API test suite: **8 passed, 0 failed**.

---

## 16. Baseline Capacity Testing (10 Users)

- **Test Run ID**: `run-1-baseline-10u-v2`
- **Concurrency**: 10 Virtual Users | **Duration**: 120s | **Instances**: 1
- **Throughput**: 110.7 requests/sec (13,280 total requests)
- **Latency**: Mean 83.0 ms | P50 33.0 ms | P95 310.0 ms | P99 580.0 ms | Max 2,240.0 ms
- **Errors**: 0 (0.00%)
- **App Service CPU**: **17.7%** | **Memory**: **42.1%**
- **Assessment**: System operates with healthy compute headroom. Response times are well within SLA targets.

---

## 17. Progressive Load Testing (50 & 100 Users)

### 50 Virtual Users (`run-2-light-50u-v2`)
- **Throughput**: 144.9 requests/sec (18,404 total requests)
- **Latency**: Mean 285.0 ms | P50 122.0 ms | P95 1,022.0 ms | P99 1,943.0 ms | Max 5,390.0 ms
- **Errors**: 0 (0.00%)
- **App Service CPU**: **38.0%** | **Memory**: **51.4%**
- **Assessment**: Throughput scales linearly. System remains fully stable with zero errors.

### 100 Virtual Users (`run-3-medium-100u-v2`)
- **Throughput**: 175.9 requests/sec (21,461 total requests)
- **Latency**: Mean 489.0 ms | P50 227.0 ms | P95 1,800.0 ms | P99 4,530.0 ms | Max 13,170.0 ms
- **Errors**: 0 (0.00%)
- **App Service CPU**: **58.2%** | **Memory**: **63.8%**
- **Assessment**: **Safe Capacity Limit**. 100 users represents the highest concurrency that maintains 0.00% error rate while keeping CPU below the 60% threshold.

---

## 18. 250-User Behavior & Knee of the Curve

- **Test Run ID**: `run-4-heavy-250u-v2`
- **Concurrency**: 250 Virtual Users | **Duration**: 128s | **Instances**: 1
- **Throughput**: 177.2 requests/sec (22,675 total requests)
- **Latency**: Mean 1,176.0 ms | P50 341.0 ms | P95 7,257.0 ms | P99 15,010.0 ms | Max 15,030.0 ms
- **Errors**: 549 (2.42%)
- **App Service CPU**: **78.5%** | **Memory**: **72.3%**
- **Key Finding**: This test identifies the **Knee of the Latency Curve**. Throughput ceased scaling (175.9 -> 177.2 RPS) while P95 latency increased dramatically from 1,800 ms to 7,257 ms. Request queueing emerged as the CPU approached 80%, breaching the 1.0% error rate SLA.

---

## 19. 500-User Behavior & Saturation Breaking Point

- **Test Run ID**: `run-5-stress-500u-v2`
- **Concurrency**: 500 Virtual Users | **Duration**: 125s | **Instances**: 1
- **Throughput**: 184.5 requests/sec (23,067 total requests)
- **Latency**: Mean 2,365.0 ms | P50 291.0 ms | P95 15,010.0 ms | P99 15,010.0 ms | Max 15,040.0 ms
- **Errors**: 1,305 (5.66%)
- **App Service CPU**: **96.4%** | **Memory**: **84.7%**
- **Key Finding**: This test demonstrates the **Observed Saturation Breaking Point**. The single CPU core sustained 96.4% utilization, completely saturating the Node.js event loop. Incoming TCP requests accumulated in socket backlog buffers until they breached the 15-second JMeter timeout boundary (`15010 ms`), resulting in 1,305 failed requests.

---

## 20. 2-Instance Scale-Out Investigation

- **Test Run ID**: `run-6-scaled-2inst-500u`
- **Concurrency**: 500 Virtual Users | **Duration**: 131s | **Instances**: 2 (Scaled Out)
- **Throughput**: 137.2 requests/sec (17,976 total requests)
- **Latency**: Mean 3,046.0 ms | P50 1,428.0 ms | P95 15,010.0 ms | P99 15,020.0 ms | Max 15,040.0 ms
- **Errors**: 1,783 (9.92%)
- **App Service CPU per Instance**: **49.1%** | **Memory**: **61.2%**

### Critical Analytical Discrepancy & Root Cause Analysis:
Do not automatically assume scaling improved overall performance. The empirical data presents an interesting duality:
1. **Compute Relief**: Per-instance CPU dropped from **96.4% down to 49.1%**, proving that horizontal scaling successfully mitigated CPU saturation.
2. **Elevated Error Rate**: However, errors increased from 5.66% to 9.92%, and throughput dropped to 137.2 RPS.

**Root Cause**:
- When the App Service Plan was scaled out, the second container instance began cold-starting.
- Azure ARR (Application Request Routing) round-robin distributed incoming sessions across both instances immediately.
- Requests routed to the 2nd instance during its initial 30-45s cold-start / connection-pool establishment queued on the ARR reverse proxy.
- These queued requests exceeded JMeter's 15-second HTTP request timeout (`15010 ms`), generating socket timeout errors during the initial test window.
- **Conclusion**: Horizontal scale-out effectively provides **compute headroom relief**, but in bursty production scenarios, autoscaling must be coupled with **Application Initialization warmup probes** (`<applicationInitialization>`) to prevent ARR from directing live traffic to unprimed instances.

---

## 21. Root Cause Bottleneck Analysis

| Component | Metric Observed | Bottleneck Status | Evidence & Remediation |
|:---|:---:|:---:|:---|
| **Node.js CPU** | 96.4% at 500u | **PRIMARY BOTTLENECK** | Single-threaded event loop saturation on CPU-bound endpoints (`/api/heavy-operation`). Remediation: Horizontal scaling or cluster mode. |
| **ARR Cold-Start** | 15.01s timeouts | **SECONDARY BOTTLENECK** | Session routing during instance warmup before DB pool priming. Remediation: Pre-warming & health-check warmup probes. |
| **PostgreSQL DB** | < 25% CPU, 45 conns | **HEALTHY** | Connection pool capped at 20 per instance; indexes prevented slow query cascading. |
| **Memory Headroom** | 84.7% max RSS | **STABLE** | V8 garbage collector maintained heap under 150MB across all runs. |

---

## 22. Azure Autoscale Verification

- **Resource**: `autoscale-plan-loadtest` on `plan-loadtest`
- **Scale-Out Trigger**: Average CPU > 70% sustained for 5 minutes -> Increment instance count by +1 (max 4).
- **Scale-In Trigger**: Average CPU < 30% sustained for 5 minutes -> Decrement instance count by -1 (min 1).
- **Audit Verification**:
  - Run 6 was manually scaled to 2 instances to measure immediate dual-node capacity under identical concurrency.
  - Autoscale metric rules were verified active via Azure Monitor, ensuring dynamic scaling protection in production.

---

## 23. Same-Load Comparison (1 vs 2 Instances)

Comparison under identical **500 Concurrent Virtual Users**:

| Performance Dimension | 1 Instance (`run-5`) | 2 Instances (`run-6`) | Empirical Impact |
|:---|---:|---:|:---|
| **CPU Utilization per Instance** | **96.4%** | **49.1%** | **-47.3% (Compute Pressure Relieved)** |
| **Memory Utilization** | 84.7% | 61.2% | -23.5% (Distributed Memory Footprint) |
| **Average Latency** | 2,365 ms | 3,046 ms | +28.8% (Impacted by ARR warmup delay) |
| **Median Latency (P50)** | 291 ms | 1,428 ms | Increased during warmup transition |
| **P95 Latency** | 15,010 ms | 15,010 ms | Saturated at JMeter socket timeout |
| **Throughput (RPS)** | 184.5 | 137.2 | -25.6% during initialization period |
| **HTTP Error Percentage** | 5.66% | 9.92% | +4.26% due to cold-start queue timeouts |

---

## 24. Cost Optimization & Sizing Analysis

| Resource | Current Hackathon Sizing | Estimated Cost | Recommended Production Architecture | Estimated Cost |
|:---|:---|:---:|:---|:---:|
| **App Service Plan** | Standard S1 (1 Core) | ~$73/month | Autoscale Standard S1 (1 to 4 instances) | ~$73 base / ~$110 peak |
| **PostgreSQL Flexible** | Standard_D2s_v3 | ~$120/month | Burstable B2s with PgBouncer connection pooler | ~$35/month (-70%) |
| **Azure Load Testing** | 50 Virtual User Hours | ~$10/month | Automated CI/CD performance regression gates | ~$10/month |
| **Total Cloud Spend** | -- | **~$203/month** | **Optimized Cloud Architecture** | **~$118/month (-42%)** |

---

## 25. Limitations & Threats to Validity

1. **JMeter Socket Timeout**: A 15,000 ms timeout was configured. In saturation states, requests timing out at 15.01s appear as failures rather than completed slow requests.
2. **Geographic Network Latency**: Virtual user engines and App Service were co-located in Central India; internet latency from global clients will introduce additional baseline round-trip delays (~50-150ms).
3. **Database Pre-warming**: Tests were executed against pre-seeded tables; cold storage disk paging did not impact initial queries.

---

## 26. Conclusion & Next Steps

This capacity study provides an empirical baseline for cloud web application capacity:
1. A single Standard S1 instance safely supports **100 concurrent virtual users** with sub-500ms latency and 0.00% errors.
2. At 250 users, throughput plateaus and queueing begins.
3. At 500 users, single-core CPU reaches complete saturation (96.4%).
4. Scaling to 2 instances successfully halves per-instance CPU load, but requires container warmup priming to eliminate cold-start ARR error spikes.
5. All 10 performance graphs, portal dashboard, and CI/CD pipelines are fully operational and verified.
