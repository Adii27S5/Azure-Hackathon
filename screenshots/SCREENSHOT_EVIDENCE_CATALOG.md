# Evidence & Screenshots Verification Catalog
## Project ID: 24CC3046-P056 — Azure Load Testing for a Web Application Capacity Study
**Team:** T158 | **Environment:** Microsoft Azure (`rg-loadtest`, Central India)

This catalog indexes all 24 required evidence items with their exact verified Azure resource IDs, portal navigation paths, CLI queries, and metric values.

---

### Evidence Inventory Matrix (01 to 24)

| # | Item Name | Target Resource / Artifact | Verification CLI / Portal Path | Status |
|:---|:---|:---|:---|:---:|
| **01** | `01-resource-group` | `rg-loadtest` (Central India) | `az group show -n rg-loadtest` | **VERIFIED** |
| **02** | `02-app-service` | `app-loadtest-101` | `az webapp show -g rg-loadtest -n app-loadtest-101` | **VERIFIED** |
| **03** | `03-app-service-plan` | `plan-loadtest` (Standard S1) | `az appservice plan show -g rg-loadtest -n plan-loadtest` | **VERIFIED** |
| **04** | `04-postgresql` | `app-loadtest-101-server` | `az postgres flexible-server show -g rg-loadtest -n app-loadtest-101-server` | **VERIFIED** |
| **05** | `05-database` | `db-loadtest-101` | Seeded tables: `users`, `products`, `orders`, `order_items` | **VERIFIED** |
| **06** | `06-vnet` | `vnet-qkjgcmgm` | Subnets: `subnet-aaahsuqi` & `subnet-ejdigsdaswpw4` | **VERIFIED** |
| **07** | `07-private-dns` | `privatelink.postgres.database.azure.com` | Zone A Record: `10.0.2.4` linked to `vnet-qkjgcmgm` | **VERIFIED** |
| **08** | `08-github-actions` | CI/CD Workflows | Runs `36271169628`, `36271744461` (100% Succeeded) | **VERIFIED** |
| **09** | `09-api-tests` | `test/api.test.js` | `npm test` -> 8 passed, 0 failed in 9s | **VERIFIED** |
| **10** | `10-health` | `GET /health` | Live HTTP 200 OK: `{"status":"healthy","database":{"status":"connected"}}` | **VERIFIED** |
| **11** | `11-application-insights`| `appi-loadtest-101` | Live Metrics, Dependency Map, Request Telemetry | **VERIFIED** |
| **12** | `12-log-analytics` | `law-loadtest-101` | Centralized container log ingestion & diagnostics | **VERIFIED** |
| **13** | `13-jmeter` | `loadtest/capacity_study.jmx` | Multi-threaded test plan with Groovy environment expressions | **VERIFIED** |
| **14** | `14-load-testing` | `alt-loadtest-101` | Test: `capacity-study-test` (App Service, Plan, & DB linked) | **VERIFIED** |
| **15** | `15-10-users` | `run-1-baseline-10u-v2` | 110.7 RPS, 83 ms avg latency, 0% errors, 17.7% CPU | **VERIFIED** |
| **16** | `16-50-users` | `run-2-light-50u-v2` | 144.9 RPS, 285 ms avg latency, 0% errors, 38.0% CPU | **VERIFIED** |
| **17** | `17-100-users` | `run-3-medium-100u-v2` | 175.9 RPS, 489 ms avg latency, 0% errors, 58.2% CPU | **VERIFIED** |
| **18** | `18-250-users` | `run-4-heavy-250u-v2` | 177.2 RPS, 1,176 ms avg latency, 2.42% errors, 78.5% CPU (Knee) | **VERIFIED** |
| **19** | `19-500-users` | `run-5-stress-500u-v2` | 184.5 RPS, 2,365 ms avg, 15.01s P95, 5.66% errors, 96.4% CPU (Break) | **VERIFIED** |
| **20** | `20-two-instance` | `run-6-scaled-2inst-500u` | 137.2 RPS, 3,046 ms avg, 9.92% errors, 49.1% CPU (CPU Relieved) | **VERIFIED** |
| **21** | `21-autoscale` | `autoscale-plan-loadtest` | Scale-out at CPU > 70%, Scale-in at CPU < 30% (1-4 instances) | **VERIFIED** |
| **22** | `22-dashboard` | `capacity-performance-dashboard`| Azure Portal Dashboard with 6 performance metric tiles | **VERIFIED** |
| **23** | `23-frontend` | Storefront & Telemetry | Live integration at `http://localhost:3000` & App Service `/` | **VERIFIED** |
| **24** | `24-final-results` | `results/final_capacity_matrix.csv`| Complete empirical matrix with all percentiles & assessments | **VERIFIED** |

---

### Detailed Resource Verification Links

1. **Azure App Service**:
   - URL: `https://app-loadtest-101-byh7hsbwbyemh7bg.centralindia-01.azurewebsites.net`
   - Health Probe: `https://app-loadtest-101-byh7hsbwbyemh7bg.centralindia-01.azurewebsites.net/health`
2. **Azure Portal Dashboard**:
   - Resource: `/subscriptions/e6d4fcf4-96d4-4e9c-a00e-929a1c623bb4/resourceGroups/rg-loadtest/providers/Microsoft.Portal/dashboards/capacity-performance-dashboard`
3. **Azure Load Testing Test**:
   - Resource: `/subscriptions/e6d4fcf4-96d4-4e9c-a00e-929a1c623bb4/resourceGroups/rg-loadtest/providers/Microsoft.LoadTestService/loadtests/alt-loadtest-101/testId/capacity-study-test`
4. **Generated Graphs Directory**:
   - All 10 high-resolution performance plots are stored in `reports/graphs/01_users_vs_rps.png` through `10_concurrency_vs_instances.png`.
