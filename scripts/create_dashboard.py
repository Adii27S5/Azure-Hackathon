import json
import subprocess

def generate_dashboard():
    dashboard = {
        "lenses": [
            {
                "order": 0,
                "parts": [
                    {
                        "position": {"x": 0, "y": 0, "colSpan": 12, "rowSpan": 3},
                        "metadata": {
                            "inputs": [],
                            "type": "Extension/HubsExtension/PartType/MarkdownPart",
                            "settings": {
                                "content": {
                                    "settings": {
                                        "title": "Azure Capacity Study Dashboard (Project 24CC3046-P056)",
                                        "subtitle": "Microsoft Azure Cloud Load Testing & Empirical Capacity Analysis",
                                        "content": "## Project ID: 24CC3046-P056 — Azure Load Testing for a Web Application Capacity Study\n\n### Verified Production Resources in Resource Group `rg-loadtest` (Central India):\n1. **Azure App Service**: `app-loadtest-101` (Node.js 24 LTS, Linux)\n2. **App Service Plan**: `plan-loadtest` (Standard S1: 1 vCPU, 1.75 GB RAM, Autoscale 1-4 instances)\n3. **PostgreSQL Flexible Server**: `app-loadtest-101-server` (VNet Integrated, Private DNS)\n4. **Azure Load Testing**: `alt-loadtest-101` (Apache JMeter Distributed Test: `capacity-study-test`)\n5. **Application Insights**: `appi-loadtest-101` (APM, Live Metrics, Dependency Telemetry)\n6. **Azure Autoscale**: `autoscale-plan-loadtest` (Scale-out at CPU > 70%, Scale-in at CPU < 30%)\n7. **Virtual Network**: `vnet-qkjgcmgm` (Subnets: `subnet-aaahsuqi` for App, `subnet-ejdigsdaswpw4` for DB)\n8. **Log Analytics Workspace**: `law-loadtest-101` (Log Ingestion)\n\n**Live App URL:** https://app-loadtest-101-byh7hsbwbyemh7bg.centralindia-01.azurewebsites.net  \n**Live Health Probe:** https://app-loadtest-101-byh7hsbwbyemh7bg.centralindia-01.azurewebsites.net/health"
                                    }
                                }
                            }
                        }
                    },
                    {
                        "position": {"x": 0, "y": 3, "colSpan": 6, "rowSpan": 4},
                        "metadata": {
                            "inputs": [
                                {
                                    "name": "ComponentId",
                                    "value": {
                                        "SubscriptionId": "e6d4fcf4-96d4-4e9c-a00e-929a1c623bb4",
                                        "ResourceGroup": "rg-loadtest",
                                        "Name": "plan-loadtest"
                                    }
                                }
                            ],
                            "type": "Extension/Microsoft_Azure_Monitoring/PartType/MetricsChartPart",
                            "settings": {
                                "content": {
                                    "version": "1.0",
                                    "chartType": 2,
                                    "title": "App Service Plan — CPU & Memory %",
                                    "metrics": [
                                        {
                                            "resourceMetadata": {
                                                "id": "/subscriptions/e6d4fcf4-96d4-4e9c-a00e-929a1c623bb4/resourceGroups/rg-loadtest/providers/Microsoft.Web/serverFarms/plan-loadtest"
                                            },
                                            "name": "CpuPercentage",
                                            "aggregationType": 4
                                        },
                                        {
                                            "resourceMetadata": {
                                                "id": "/subscriptions/e6d4fcf4-96d4-4e9c-a00e-929a1c623bb4/resourceGroups/rg-loadtest/providers/Microsoft.Web/serverFarms/plan-loadtest"
                                            },
                                            "name": "MemoryPercentage",
                                            "aggregationType": 4
                                        }
                                    ]
                                }
                            }
                        }
                    },
                    {
                        "position": {"x": 6, "y": 3, "colSpan": 6, "rowSpan": 4},
                        "metadata": {
                            "inputs": [
                                {
                                    "name": "ComponentId",
                                    "value": {
                                        "SubscriptionId": "e6d4fcf4-96d4-4e9c-a00e-929a1c623bb4",
                                        "ResourceGroup": "rg-loadtest",
                                        "Name": "app-loadtest-101"
                                    }
                                }
                            ],
                            "type": "Extension/Microsoft_Azure_Monitoring/PartType/MetricsChartPart",
                            "settings": {
                                "content": {
                                    "version": "1.0",
                                    "chartType": 2,
                                    "title": "Web App Requests & Average Response Time",
                                    "metrics": [
                                        {
                                            "resourceMetadata": {
                                                "id": "/subscriptions/e6d4fcf4-96d4-4e9c-a00e-929a1c623bb4/resourceGroups/rg-loadtest/providers/Microsoft.Web/sites/app-loadtest-101"
                                            },
                                            "name": "Requests",
                                            "aggregationType": 1
                                        },
                                        {
                                            "resourceMetadata": {
                                                "id": "/subscriptions/e6d4fcf4-96d4-4e9c-a00e-929a1c623bb4/resourceGroups/rg-loadtest/providers/Microsoft.Web/sites/app-loadtest-101"
                                            },
                                            "name": "AverageResponseTime",
                                            "aggregationType": 4
                                        },
                                        {
                                            "resourceMetadata": {
                                                "id": "/subscriptions/e6d4fcf4-96d4-4e9c-a00e-929a1c623bb4/resourceGroups/rg-loadtest/providers/Microsoft.Web/sites/app-loadtest-101"
                                            },
                                            "name": "Http5xx",
                                            "aggregationType": 1
                                        }
                                    ]
                                }
                            }
                        }
                    },
                    {
                        "position": {"x": 0, "y": 7, "colSpan": 6, "rowSpan": 4},
                        "metadata": {
                            "inputs": [
                                {
                                    "name": "ComponentId",
                                    "value": {
                                        "SubscriptionId": "e6d4fcf4-96d4-4e9c-a00e-929a1c623bb4",
                                        "ResourceGroup": "rg-loadtest",
                                        "Name": "appi-loadtest-101"
                                    }
                                }
                            ],
                            "type": "Extension/Microsoft_Azure_Monitoring/PartType/MetricsChartPart",
                            "settings": {
                                "content": {
                                    "version": "1.0",
                                    "chartType": 2,
                                    "title": "Application Insights — Request Rate & Failed Requests",
                                    "metrics": [
                                        {
                                            "resourceMetadata": {
                                                "id": "/subscriptions/e6d4fcf4-96d4-4e9c-a00e-929a1c623bb4/resourceGroups/rg-loadtest/providers/microsoft.insights/components/appi-loadtest-101"
                                            },
                                            "name": "requests/count",
                                            "aggregationType": 1
                                        },
                                        {
                                            "resourceMetadata": {
                                                "id": "/subscriptions/e6d4fcf4-96d4-4e9c-a00e-929a1c623bb4/resourceGroups/rg-loadtest/providers/microsoft.insights/components/appi-loadtest-101"
                                            },
                                            "name": "requests/failed",
                                            "aggregationType": 1
                                        }
                                    ]
                                }
                            }
                        }
                    },
                    {
                        "position": {"x": 6, "y": 7, "colSpan": 6, "rowSpan": 4},
                        "metadata": {
                            "inputs": [
                                {
                                    "name": "ComponentId",
                                    "value": {
                                        "SubscriptionId": "e6d4fcf4-96d4-4e9c-a00e-929a1c623bb4",
                                        "ResourceGroup": "rg-loadtest",
                                        "Name": "app-loadtest-101-server"
                                    }
                                }
                            ],
                            "type": "Extension/Microsoft_Azure_Monitoring/PartType/MetricsChartPart",
                            "settings": {
                                "content": {
                                    "version": "1.0",
                                    "chartType": 2,
                                    "title": "PostgreSQL Flexible Server — CPU & Active Connections",
                                    "metrics": [
                                        {
                                            "resourceMetadata": {
                                                "id": "/subscriptions/e6d4fcf4-96d4-4e9c-a00e-929a1c623bb4/resourceGroups/rg-loadtest/providers/Microsoft.DBforPostgreSQL/flexibleServers/app-loadtest-101-server"
                                            },
                                            "name": "cpu_percent",
                                            "aggregationType": 4
                                        },
                                        {
                                            "resourceMetadata": {
                                                "id": "/subscriptions/e6d4fcf4-96d4-4e9c-a00e-929a1c623bb4/resourceGroups/rg-loadtest/providers/Microsoft.DBforPostgreSQL/flexibleServers/app-loadtest-101-server"
                                            },
                                            "name": "active_connections",
                                            "aggregationType": 4
                                        }
                                    ]
                                }
                            }
                        }
                    },
                    {
                        "position": {"x": 0, "y": 11, "colSpan": 12, "rowSpan": 5},
                        "metadata": {
                            "inputs": [],
                            "type": "Extension/HubsExtension/PartType/MarkdownPart",
                            "settings": {
                                "content": {
                                    "settings": {
                                        "title": "Empirical Capacity Study Matrix & Scale-Out Analysis",
                                        "content": "### Real Azure Load Testing Results Across Progressive Workloads & Scale Configurations\n\n| Test Run ID | Users | Inst | RPS | Avg Latency | P50 (ms) | P95 (ms) | P99 (ms) | Errors | Error % | CPU % | Operational Assessment |\n|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|\n| `run-1-baseline-10u-v2` | 10 | 1 | 110.7 | 83.0 ms | 33.0 | 310.0 | 580.0 | 0 | 0.00% | 17.7% | **PASS - Optimal Capacity** |\n| `run-2-light-50u-v2` | 50 | 1 | 144.9 | 285.0 ms | 122.0 | 1022.0 | 1943.0 | 0 | 0.00% | 38.0% | **PASS - Linear Scaling** |\n| `run-3-medium-100u-v2` | 100 | 1 | 175.9 | 489.0 ms | 227.0 | 1800.0 | 4530.0 | 0 | 0.00% | 58.2% | **PASS - Safe Operating Knee** |\n| `run-4-heavy-250u-v2` | 250 | 1 | 177.2 | 1176.0 ms | 341.0 | 7257.0 | 15010.0 | 549 | 2.42% | 78.5% | **BREACH - Queueing & Degradation** |\n| `run-5-stress-500u-v2` | 500 | 1 | 184.5 | 2365.0 ms | 291.0 | 15010.0 | 15010.0 | 1305 | 5.66% | **96.4%** | **SATURATION BREAKING POINT** |\n| `run-6-scaled-2inst-500u` | 500 | 2 | 137.2 | 3046.0 ms | 1428.0 | 15010.0 | 15020.0 | 1783 | 9.92% | **49.1%** | **CPU RELIEVED / COLD-START QUEUE** |\n\n> **Observed Safe Limit (1 Instance):** 100 Concurrent Virtual Users on Standard S1 (0% errors, 58.2% CPU).\n> **Saturation Breaking Point:** At 500 Virtual Users on 1 instance, CPU reached 96.4% utilization and P95 latency saturated at 15.01s (JMeter socket timeout limit).\n> **Scale-Out Investigation:** Scaling from 1 to 2 instances halved per-instance CPU (96.4% down to 49.1%), but initial ARR routing during instance warmup contributed to a 9.92% error rate."
                                    }
                                }
                            }
                        }
                    }
                ]
            }
        ],
        "metadata": {
            "model": {
                "timeRange": {
                    "value": {
                        "relative": {
                            "duration": 24,
                            "timeUnit": 1
                        }
                    },
                    "type": "MsPortalFx.Composition.Configuration.ValueTypes.TimeRange"
                }
            }
        }
    }
    
    with open("deploy/dashboard.json", "w", encoding="utf-8") as f:
        json.dump(dashboard, f, indent=2)
    print("deploy/dashboard.json updated with live rg-loadtest resources.")

if __name__ == "__main__":
    generate_dashboard()
