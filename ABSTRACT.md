# Azure Load Testing for a Web Application Capacity Study

**Project ID:** 24CC3046-P056  
**Team:** T158

## Team Members
| Student ID | Team Member |
|---|---|
| 2400032012 | KORADA TEJA |
| 2400032102 | GUBBALA LAKSHMI SAI TEJA |
| 2400032152 | ADITYA SINGH |
| 2400032605 | GOLLA MANIKANTA |

## Use Cases
- Determine the observed breaking point of the current application sizing.
- Measure performance under increasing concurrent virtual-user workloads.
- Identify CPU, memory, latency, throughput, and error-rate bottlenecks.
- Recommend and validate horizontal scaling using Azure App Service instances.
- Verify Azure Autoscale through actual scale-out and scale-in events.

## Bottlenecks Students May Encounter
- Test traffic patterns may not perfectly represent real-world user behavior.
- High concurrent traffic can increase CPU utilization and expose capacity limits.
- Aggressive load testing against production can affect real users; a staging environment or deployment slot is safer.
- Scaling does not guarantee improvement in every metric; results must be measured and compared.

## Abstract
The project “Azure Load Testing for a Web Application Capacity Study” focuses on evaluating the performance, reliability, and scalability of a web application using Microsoft Azure cloud services. The main objective is to determine the workload that the current application configuration can handle before response time increases, errors occur, or system resources become heavily utilized. The web application is deployed on Azure App Service (`app-loadtest-101`) backed by Azure Database for PostgreSQL Flexible Server (`app-loadtest-101-server`) with private VNet integration, and tested using Azure Load Testing (`alt-loadtest-101`) with Apache JMeter, where simulated virtual users generate realistic multi-endpoint traffic across product browsing, search, product details, dashboard aggregations, order transactions, and cryptographic compute operations.

The application was progressively tested with 10, 50, 100, 250, and 500 virtual users while monitoring throughput, response time, latency, error percentage, CPU utilization, and application availability through Azure Application Insights and Azure Monitor. In the single-instance configuration (Standard S1), performance remained stable up to 100 concurrent users (178.8 RPS, 0% errors, 58.2% CPU). At 250 users, request queueing emerged (78.5% CPU, 2.42% errors). At 500 users, CPU hit 96.4% sustained saturation with 5,246 ms average latency and 5.66% errors, identifying CPU compute headroom as the definitive breaking point. Horizontally scaling to 2 App Service instances under the same 500-user workload cut per-instance CPU utilization to 49.1%, successfully mitigating the single-core bottleneck. Azure Autoscale (`autoscale-plan-loadtest`) was configured for dynamic 1 to 4 instance scaling (scale-out at CPU > 70%, scale-in at CPU < 30%).

The final outcome provides a measured capacity comparison rather than an assumption-based result. The project demonstrates an end-to-end cloud performance-testing workflow in which workload is generated, performance is monitored, bottlenecks are identified, infrastructure is scaled, and the workload is re-tested to evaluate the effect of scaling. A unified Azure Portal dashboard and Application Insights telemetry provide centralized visibility into application performance, infrastructure utilization, load-test results, and scaling activity.