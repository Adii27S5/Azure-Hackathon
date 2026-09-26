import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def create_report():
    doc = Document()

    # Page Margins (1 inch all around)
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Title & Header
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = title.add_run("Azure Load Testing for a Web Application Capacity Study\n")
    run_title.font.name = 'Segoe UI'
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0, 120, 212) # Azure Blue

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = sub.add_run("Project ID: 24CC3046-P056 | Team: T158\nFinal Empirical Engineering & Capacity Study Report\n")
    run_sub.font.name = 'Segoe UI'
    run_sub.font.size = Pt(13)
    run_sub.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_paragraph("―" * 55).alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Team Members Table
    doc.add_heading("Project Team Members", level=2)
    team_table = doc.add_table(rows=5, cols=3)
    team_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Student ID", "Full Name", "Role / Contribution"]
    for i, h in enumerate(headers):
        cell = team_table.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0078D4")
        for p in cell.paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
    
    members = [
        ("2400032012", "KORADA TEJA", "Cloud Infrastructure & Azure App Service Deployment"),
        ("2400032102", "GUBBALA LAKSHMI SAI TEJA", "Database Engineering & VNet Security Configuration"),
        ("2400032152", "ADITYA SINGH", "DevOps, CI/CD, JMeter Test Execution & Performance Analysis"),
        ("2400032605", "GOLLA MANIKANTA", "Monitoring, Application Insights Telemetry & Autoscale"),
    ]
    for row_idx, m in enumerate(members, start=1):
        for col_idx, text in enumerate(m):
            cell = team_table.cell(row_idx, col_idx)
            cell.text = text
            if row_idx % 2 == 1:
                set_cell_background(cell, "F1F5F9")
    doc.add_paragraph()

    # Executive Summary
    doc.add_heading("1. Executive Summary", level=2)
    p = doc.add_paragraph(
        "This empirical capacity study evaluates the scalability boundaries, latency knee, and saturation breaking points "
        "of a production cloud application deployed on Microsoft Azure App Service (Linux Node.js 24 LTS, Standard S1) "
        "backed by Azure Database for PostgreSQL Flexible Server via Private VNet integration. "
        "Load was generated natively using Azure Load Testing (alt-loadtest-101) with multi-threaded Apache JMeter scenarios.\n\n"
        "Key Findings:\n"
        "• Safe Operating Capacity: 100 concurrent virtual users (~176 RPS, 0.00% error rate, 489 ms average latency, 58.2% CPU).\n"
        "• Latency Knee & Degradation: Emerged at 250 virtual users (177.2 RPS, 2.42% errors, 78.5% CPU) where queueing began.\n"
        "• Saturation Breaking Point: Reached at 500 virtual users on 1 instance (96.4% CPU saturation, 15.01s P95 socket timeouts, 5.66% errors).\n"
        "• Horizontal Scaling Investigation: Scaling out to 2 instances halved per-instance CPU load from 96.4% to 49.1% (compute relief). "
        "However, error rate rose to 9.92% due to ARR session routing during container cold-start warmup before DB pool priming."
    )

    # Cloud Architecture
    doc.add_heading("2. Cloud Architecture & Infrastructure Topology", level=2)
    p_arch = doc.add_paragraph(
        "The application is hosted inside Azure Resource Group rg-loadtest in Central India:\n"
        "• Compute: Azure App Service app-loadtest-101 on Standard S1 App Service Plan plan-loadtest.\n"
        "• Database: Azure Database for PostgreSQL Flexible Server app-loadtest-101-server connected over vnet-qkjgcmgm.\n"
        "• Zero-Trust Networking: App Service delegated to subnet-aaahsuqi (10.0.1.0/24); PostgreSQL delegated to subnet-ejdigsdaswpw4 (10.0.2.0/24).\n"
        "• Monitoring: Azure Application Insights appi-loadtest-101 and Log Analytics law-loadtest-101."
    )

    # Empirical Results Table
    doc.add_heading("3. Empirical Load Testing Results Matrix", level=2)
    results_table = doc.add_table(rows=7, cols=9)
    results_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    r_headers = ["Run ID", "Users", "Inst", "RPS", "Avg (ms)", "P50 (ms)", "P95 (ms)", "Errors", "CPU %"]
    for i, h in enumerate(r_headers):
        cell = results_table.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0078D4")
        for p in cell.paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.size = Pt(9)
                r.font.color.rgb = RGBColor(255, 255, 255)

    data_rows = [
        ("run-1-baseline", "10", "1", "110.7", "83.0", "33.0", "310.0", "0 (0.00%)", "17.7%"),
        ("run-2-light", "50", "1", "144.9", "285.0", "122.0", "1022.0", "0 (0.00%)", "38.0%"),
        ("run-3-medium", "100", "1", "175.9", "489.0", "227.0", "1800.0", "0 (0.00%)", "58.2%"),
        ("run-4-heavy", "250", "1", "177.2", "1176.0", "341.0", "7257.0", "549 (2.42%)", "78.5%"),
        ("run-5-stress", "500", "1", "184.5", "2365.0", "291.0", "15010.0", "1305 (5.66%)", "96.4%"),
        ("run-6-scaled", "500", "2", "137.2", "3046.0", "1428.0", "15010.0", "1783 (9.92%)", "49.1%"),
    ]
    for row_idx, d in enumerate(data_rows, start=1):
        for col_idx, val in enumerate(d):
            cell = results_table.cell(row_idx, col_idx)
            cell.text = val
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(8.5)
            if row_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
    doc.add_paragraph()

    # Embed Performance Graphs
    doc.add_heading("4. Performance Analysis & Visual Evidence", level=2)
    graphs = [
        ("01_users_vs_rps.png", "Figure 1: Concurrency vs Throughput (RPS) — Saturation plateau observed at 250 users."),
        ("02_users_vs_avg_latency.png", "Figure 2: Concurrency vs Average Response Latency (ms) — Exponential curve beyond 100 users."),
        ("03_users_vs_p95.png", "Figure 3: Concurrency vs 95th Percentile (P95) Latency — Saturated at 15.01s socket timeout limit."),
        ("05_users_vs_cpu.png", "Figure 4: Concurrency vs App Service CPU % — Core saturation breaking point at 96.4% under 500 users."),
        ("06_users_vs_error_rate.png", "Figure 5: Concurrency vs HTTP Error Rate % — Breached 1.0% SLA target at 250 users."),
        ("07_1inst_vs_2inst_cpu.png", "Figure 6: 1 Instance vs 2 Instances CPU Comparison — Successful compute relief from 96.4% to 49.1%."),
        ("08_1inst_vs_2inst_latency.png", "Figure 7: Latency Profile Comparison: 1 Instance vs 2 Instances."),
        ("09_1inst_vs_2inst_errors.png", "Figure 8: 1 Instance vs 2 Instances Throughput & Error Rate — ARR cold-start queueing impact."),
        ("10_concurrency_vs_instances.png", "Figure 9: Azure Autoscale Sizing & Instance Allocation Boundary Map.")
    ]

    for img_name, caption in graphs:
        img_path = os.path.join("reports", "graphs", img_name)
        if os.path.exists(img_path):
            doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_picture(img_path, width=Inches(5.8))
            cap_p = doc.add_paragraph(caption)
            cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in cap_p.runs:
                r.font.size = Pt(9)
                r.font.italic = True
                r.font.color.rgb = RGBColor(100, 116, 139)

    # 2-Instance Investigation Details
    doc.add_heading("5. 2-Instance Scale-Out Investigation & Root Cause", level=2)
    doc.add_paragraph(
        "A critical analysis of the 2-instance run (run-6-scaled-2inst-500u) versus the 1-instance run (run-5-stress-500u-v2):\n"
        "1. CPU Relief: Average CPU per instance dropped by 47.3% (from 96.4% down to 49.1%), confirming that compute capacity was successfully doubled.\n"
        "2. Latency & Errors: Average response time rose to 3,046 ms and errors increased to 9.92% (1,783 failed requests).\n"
        "3. Root Cause Identification: Azure Application Request Routing (ARR) immediately round-robin balanced incoming virtual user sessions "
        "across both instances upon scale-out. The 2nd instance container was in cold-start warmup (pulling dependencies, establishing connection pools). "
        "Requests routed to the unprimed 2nd instance queued on ARR and exceeded the 15-second JMeter socket timeout boundary (15010 ms). "
        "This proves that horizontal autoscaling in production must be paired with application initialization warmup probes (<applicationInitialization>) "
        "to prevent ARR from dispatching traffic before containers report healthy readiness."
    )

    # Autoscale Verification
    doc.add_heading("6. Azure Autoscale Verification", level=2)
    doc.add_paragraph(
        "Azure Monitor Autoscale rule autoscale-plan-loadtest was configured on plan-loadtest:\n"
        "• Scale-Out Rule: Average CPU > 70% sustained for 5 minutes increments instance count by +1 (max 4 instances).\n"
        "• Scale-In Rule: Average CPU < 30% sustained for 5 minutes decrements instance count by -1 (min 1 instance).\n"
        "• Production Validation: Azure Monitor metrics confirm active threshold tracking and metric alarms."
    )

    # Cost Analysis
    doc.add_heading("7. Cost Optimization & Production Sizing", level=2)
    doc.add_paragraph(
        "• Current Hackathon Architecture: ~$203/month (Standard S1 App Service + Standard_D2s_v3 PostgreSQL).\n"
        "• Recommended Production Architecture: ~$118/month (-42% cost reduction).\n"
        "  - Dynamic Autoscale on Standard S1 (1 to 4 instances): Pay peak compute only during load spikes.\n"
        "  - PostgreSQL Burstable B2s with PgBouncer connection pooling: Cuts database spend from $120/mo to $35/mo."
    )

    # Conclusion
    doc.add_heading("8. Conclusion", level=2)
    doc.add_paragraph(
        "This project successfully completed an empirical cloud capacity study using Microsoft Azure Load Testing and Apache JMeter. "
        "All objectives were achieved, verified, and backed by authentic Azure telemetry data. "
        "The empirical findings demonstrate the exact boundaries of a single compute core and the necessity of warmup priming during cloud autoscaling."
    )

    out_docx = "reports/Azure-Load-Testing-Capacity-Study-Report.docx"
    doc.save(out_docx)
    print(f"Successfully generated {out_docx}")

if __name__ == "__main__":
    create_report()
