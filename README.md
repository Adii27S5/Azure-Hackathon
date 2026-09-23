# Azure Load Testing for a Web Application Capacity Study

Project ID: 24CC3046-P056

This repository contains the Azure capacity-study implementation, load-testing artifacts, technical documentation, presentation, and abstract for the hackathon project.

## Core project
- Azure App Service web application
- Azure Database for PostgreSQL
- Azure Load Testing with Apache JMeter
- Application Insights
- Azure Monitor
- Azure Autoscale
- Log Analytics
- Custom Azure Portal dashboard

## Capacity-study results
The implemented study progressively tested 10, 50, 100, 250, and 500 virtual users on one Standard S1 instance, then repeated the same 500-user workload with 2 and 4 instances.

Observed single-instance boundary:
- 500 virtual users
- CPU reached 80%
- 0% errors

4-instance result:
- 500 virtual users
- 139.8 requests/second
- P95 latency: 239 ms
- Average CPU: 52.3%

Actual Azure Monitor Activity Log entries verified scale-out and scale-in events.

## Repository documents
- `capacity_study_report.md` — technical implementation and empirical results
- `azure_portal_guide.md` — Azure setup/portal guidance
- `loadtest/capacity_study.jmx` — Apache JMeter workload
- `docs/Azure_Load_Testing_Capacity_Study_Hackathon_Report.docx` — final report
- `docs/Azure_Load_Testing_Capacity_Study_Presentation.pptx` — presentation
- `docs/Abstract_Azure_Load_Testing_Capacity_Study.docx` — abstract

## Team T158
- 2400032012 — KORADA TEJA
- 2400032102 — GUBBALA LAKSHMI SAI TEJA
- 2400032152 — ADITYA SINGH
- 2400032605 — GOLLA MANIKANTA

## Important
Do not commit Azure secrets, passwords, tokens, or production credentials.