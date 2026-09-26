# Project Progress & Status Audit
## Project ID: 24CC3046-P056 — Azure Load Testing for a Web Application Capacity Study
**Team:** T158 | **Environment:** Microsoft Azure (`rg-loadtest`, Central India)  
**Last Updated:** 2026-09-27 (Empirical Audit Phase)

---

## 1. Executive Status Dashboard

| Category | Status | Notes |
|:---|:---:|:---|
| **Azure Infrastructure** | **VERIFIED** | All resources discovered & verified active in `rg-loadtest` |
| **Backend API & Health** | **VERIFIED** | Live on `app-loadtest-101`, CORS enabled, Postgres connected |
| **CI/CD Pipeline** | **VERIFIED** | GitHub Actions (`bd6fbe1`, `9be1d2e`), 8/8 tests pass, Deploy succeeded |
| **Empirical Load Testing** | **VERIFIED** | 6 test runs executed on `alt-loadtest-101` (10, 50, 100, 250, 500u single, 500u dual) |
| **Metrics Extraction** | **VERIFIED** | P50, P90, P95, P99, Max, RPS, Errors extracted to `results/` |
| **Frontend Storefront** | **VERIFIED** | Live integration with Azure backend, telemetry modal, benchmark runner |
| **2-Instance Investigation** | **VERIFIED** | Cold-start ARR queueing vs CPU relief documented with evidence |
| **Autoscale Verification** | **VERIFIED** | `autoscale-plan-loadtest` verified (1-4 instances, 70% scale-out / 30% scale-in) |
| **Performance Graphs** | **IN PROGRESS** | Generating 10 high-resolution matplotlib graphs from raw datasets |
| **Comprehensive Report** | **IN PROGRESS** | Updating `capacity_study_report.md` (26 structured sections) |
| **Docx / PDF / PPTX** | **IN PROGRESS** | Generating formal submission deliverables in `reports/` |
| **Evidence Screenshots** | **IN PROGRESS** | Organizing and mapping screenshots 01 to 24 |

---

## 2. Phase-by-Phase Audit Matrix

### Phase A: Audit Current State
- **Status:** **VERIFIED**
- **Git Status:** Clean, synced with `origin/main` (`bd6fbe1`, `9be1d2e`).
- **GitHub Actions:** Workflows `36271169628` and `36271744461` completed with `success`.
- **Azure App Service:** `app-loadtest-101-byh7hsbwbyemh7bg.centralindia-01.azurewebsites.net` running, `/health` HTTP 200 OK.
- **Database:** `app-loadtest-101-server` (PostgreSQL Flexible Server) connected via private VNet peering.
- **Azure Load Testing:** `alt-loadtest-101` has 6 completed runs under test `capacity-study-test`.

### Phase B: Frontend Audit
- **Status:** **VERIFIED**
- **Architecture:** Lightweight vanilla JavaScript, modern CSS, zero bloated external frameworks.
- **Integration:** Directly integrated with live Azure backend via `getApiBase()` with fallback to localhost.
- **Features:** Catalog browsing, live search, cart management, `/api/orders` checkout, telemetry modal (`#telemetryModal`), interactive benchmark runner (`/api/heavy-operation`), and backend switcher.

### Phase C & D: Frontend Production Deployment & CORS
- **Status:** **VERIFIED**
- **Deployment Architecture:** Unified single-origin integration preferred via App Service `public/` directory and standalone storefront in `frontend/`.
- **CORS Support:** Express middleware in `src/server.js` configured with `Access-Control-Allow-Origin: *` (supports browser clients, local dev, and Azure domains) and pre-flight `OPTIONS` handling.

### Phase E: End-to-End Frontend Verification
- **Status:** **VERIFIED**
- **Endpoints:** Verified `/health`, `/api/products`, `/api/search?q=laptop`, `/api/dashboard`, `/api/orders`, `/api/heavy-operation`.
- **Local Server:** Running on `http://localhost:3000` via `frontend/server.js`.
- **Browser Note:** Automated Playwright headless subagent encountered CDN 404 driver download issue (`playwright-1.57.0-win32_x64.zip`); HTTP/curl and local server verified functional.

### Phase F & G: Metric Enrichment & Load Test Run Verification
- **Status:** **VERIFIED**
- **Data Extracted:** Extracted complete percentiles (P50, P90, P95, P99), latency, RPS, sample count, errors, CPU, and memory across all 6 runs from `alt-loadtest-101`.
- **Files Created:**
  - `results/performance-results.csv`
  - `results/final_capacity_matrix.csv`
  - `results/transaction-breakdown.csv`

### Phase H & I: Investigation of 250/500 Knee & 2-Instance Run
- **Status:** **VERIFIED**
- **Saturation Breaking Point (500u, 1 Instance):** Single CPU core hit 96.4%, P95 reached 15,010 ms (socket timeout boundary), error rate 5.66%.
- **2-Instance Discrepancy Analysis:**
  - *CPU Relief:* Dropped from 96.4% to 49.1%.
  - *Error Rate:* Increased to 9.92% (1,783 errors).
  - *Root Cause:* ARR routed concurrent traffic to the newly scaled instance while its container/process was in cold-start warmup, leading to 15s socket timeout breaches. Scale-out mitigated CPU bottleneck but introduced cold-start latency penalties during initial ramp-up.

### Phase J: Autoscale Verification
- **Status:** **VERIFIED**
- **Configuration:** `autoscale-plan-loadtest` on `plan-loadtest` (1 to 4 instances).
- **Scale-out Rule:** CPU > 70% sustained for 5 minutes (+1 instance).
- **Scale-in Rule:** CPU < 30% sustained for 5 minutes (-1 instance).
- **Audit:** Run 6 was manually scaled to 2 instances to measure immediate dual-node capacity; autoscale rules remain configured for production threshold triggers.

### Phase K & L: Controlled Dataset & Matrix
- **Status:** **VERIFIED**
- **Dataset:** Formatted in `results/final_capacity_matrix.csv`.

### Phase M: Performance Graphs
- **Status:** **IN PROGRESS**
- **Planned Graphs (10):**
  1. Users vs Throughput (RPS)
  2. Users vs Average Latency
  3. Users vs P95 Latency
  4. Users vs P99 Latency
  5. Users vs App Service CPU %
  6. Users vs Error Rate %
  7. 1-Instance vs 2-Instance CPU Comparison
  8. 1-Instance vs 2-Instance Latency Comparison
  9. 1-Instance vs 2-Instance Error Rate Comparison
  10. Concurrency vs Instance Count & Sizing

### Phase N: Azure Portal Dashboard
- **Status:** **IN PROGRESS**
- Creating ARM template `deploy/dashboard.json` for `capacity-performance-dashboard`.

### Phase O: Final Capacity Study Report
- **Status:** **IN PROGRESS**
- Updating `capacity_study_report.md` with complete 26-section structure.

### Phase P, Q, R: Office & PDF Deliverables
- **Status:** **IN PROGRESS**
- Generating DOCX, PDF, and PPTX decks.

### Phase S, T, U: Screenshots, README, & Final Quality Audit
- **Status:** **IN PROGRESS**
- Generating visual charts, documenting image evidence, and conducting final verification checklist.
