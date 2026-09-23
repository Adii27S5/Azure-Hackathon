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
The project “Azure Load Testing for a Web Application Capacity Study” focuses on evaluating the performance, reliability, and scalability of a web application using Microsoft Azure cloud services. The main objective is to determine the workload that the current application configuration can handle before response time increases, errors occur, or system resources become heavily utilized. The web application is deployed on Azure App Service and tested using Azure Load Testing with Apache JMeter, where simulated virtual users generate realistic traffic across product browsing, search, product details, dashboard, order operations, and a CPU-intensive workload.

The application was progressively tested with 10, 50, 100, 250, and 500 virtual users while monitoring throughput, response time, P95/P99 latency, error percentage, CPU utilization, memory usage, and application availability through Azure monitoring tools. In the single-instance configuration, CPU reached the configured 80% boundary at 500 virtual users, identifying CPU utilization as the primary observed bottleneck under the tested workload. The application was then horizontally scaled to 2 and 4 App Service instances and the same 500-user workload was repeated. With 4 instances, the measured throughput reached 139.8 requests per second, P95 latency was 239 ms, and average CPU utilization was 52.3%. Azure Autoscale was configured and actual scale-out and scale-in events were verified using Azure Monitor Activity Logs.

The final outcome provides a measured capacity comparison rather than an assumption-based result. The project demonstrates an end-to-end cloud performance-testing workflow in which workload is generated, performance is monitored, bottlenecks are identified, infrastructure is scaled, and the same workload is re-tested to evaluate the effect of scaling. A custom Azure Portal dashboard provides centralized visibility into application performance, infrastructure utilization, load-test results, and scaling activity.