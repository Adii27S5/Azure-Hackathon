import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen slides (13.33 x 7.5 inches)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    C_BG = RGBColor(11, 15, 25)         # Dark Azure Navy
    C_CARD = RGBColor(18, 24, 38)       # Slate Card
    C_AZURE = RGBColor(0, 120, 212)     # Azure Blue
    C_GLOW = RGBColor(0, 188, 242)      # Azure Light Cyan
    C_TEXT = RGBColor(248, 250, 252)    # Main White Text
    C_MUTED = RGBColor(148, 163, 184)   # Slate Muted Text
    C_SUCCESS = RGBColor(16, 124, 65)   # Green
    C_RED = RGBColor(239, 68, 68)       # Red

    def apply_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="AZURE LOAD TESTING CAPACITY STUDY"):
        # Header category
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.5), Inches(0.4))
        p_cat = cat_box.text_frame.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_GLOW

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.5), Inches(0.8))
        p_title = title_box.text_frame.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_TEXT

    slides_data = [
        # Slide 1: Title
        ("title", "Azure Load Testing for a Web Application Capacity Study", [
            ("Project ID", "24CC3046-P056"),
            ("Team", "T158"),
            ("Environment", "Microsoft Azure (Central India, rg-loadtest)"),
            ("Domain", "Cloud Capacity Engineering & Distributed Load Testing")
        ]),
        # Slide 2: Team
        ("team", "Project Team Members & Contributions", [
            ("2400032012 — KORADA TEJA", "Cloud Infrastructure Deployment & Azure App Service Provisioning"),
            ("2400032102 — GUBBALA LAKSHMI SAI TEJA", "PostgreSQL Flexible Server Architecture, Schema & VNet Delegation"),
            ("2400032152 — ADITYA SINGH", "DevOps Engineering, CI/CD Pipeline, JMeter Test Scenarios & Analytics"),
            ("2400032605 — GOLLA MANIKANTA", "Azure Monitor Telemetry, Application Insights & Autoscale Rule Management")
        ]),
        # Slide 3: Problem
        ("content", "Problem Statement", [
            ("Uncertainty in Cloud Sizing", "Web applications often rely on theoretical heuristics rather than empirical telemetry."),
            ("Traffic Surges & Bottlenecks", "Sudden demand spikes expose single-threaded Node.js bottlenecks and connection pooling limits."),
            ("Autoscale Risks", "Improperly tuned autoscale thresholds cause delayed scaling or request queueing during cold starts."),
            ("Objective Need", "A rigorous empirical study is required to map throughput, latency, and resource breaking boundaries.")
        ]),
        # Slide 4: Objectives
        ("content", "Project Objectives", [
            ("1. Measure Safe Capacity", "Establish the maximum concurrency supported with zero errors and healthy CPU headroom."),
            ("2. Identify the Latency Knee", "Determine the transition point where response latency begins exponential escalation."),
            ("3. Locate Breaking Point", "Pinpoint the exact concurrency that causes resource saturation under Standard S1 sizing."),
            ("4. Validate Horizontal Scaling", "Evaluate 1 vs 2 instances under identical 500-user load to measure compute relief."),
            ("5. Implement Autoscale Gates", "Verify dynamic scale-out and scale-in rules driven by Azure Monitor metrics.")
        ]),
        # Slide 5: Proposed Solution
        ("content", "Proposed Solution & Methodology", [
            ("Cloud-Native Architecture", "Deploy scalable Node.js on Azure App Service with isolated PostgreSQL Flexible Server."),
            ("Zero-Trust VNet", "Eliminate public database exposure using Regional VNet integration and Private DNS zones."),
            ("Distributed JMeter Testing", "Leverage Azure Load Testing (alt-loadtest-101) to simulate multi-endpoint user journeys."),
            ("Full Telemetry Instrumentation", "Correlate APM metrics, live dependencies, and container performance in real time.")
        ]),
        # Slide 6: Architecture
        ("content", "End-to-End Cloud Topology", [
            ("Traffic Generator", "Azure Load Testing (alt-loadtest-101) in Central India executing multi-threaded JMeter plans."),
            ("Frontend & API", "Azure App Service (app-loadtest-101) on Linux Standard S1 Plan (plan-loadtest)."),
            ("Database Layer", "Azure Database for PostgreSQL Flexible Server (app-loadtest-101-server) in private subnet."),
            ("Telemetry & Logs", "Application Insights (appi-loadtest-101) and Log Analytics (law-loadtest-101).")
        ]),
        # Slide 7: Azure Services
        ("content", "Verified Azure Cloud Services", [
            ("App Service", "app-loadtest-101 — Linux Node.js 24 LTS web application"),
            ("App Service Plan", "plan-loadtest — Standard S1 (1 Core, 1.75 GB RAM)"),
            ("PostgreSQL Flexible", "app-loadtest-101-server — Standard_D2s_v3 (v14) with db-loadtest-101"),
            ("Load Testing Engine", "alt-loadtest-101 — Managed distributed Apache JMeter test runner"),
            ("App Insights & Monitor", "appi-loadtest-101 & autoscale-plan-loadtest — Live APM and autoscale triggers")
        ]),
        # Slide 8: Node.js Application
        ("content", "Node.js Application Architecture", [
            ("Express Framework", "RESTful multi-tier API serving products, search, dashboard, and orders."),
            ("Resilient Cold Start", "Immediate app.listen() binding ensures Azure container health probes pass in <2s."),
            ("Connection Pool Management", "pg.Pool configured with max: 20 per instance and idleTimeoutMillis: 30000."),
            ("CORS & Storefront", "Full CORS support for browser clients, integrated dashboard at /, and storefront UI.")
        ]),
        # Slide 9: PostgreSQL
        ("content", "Database Sizing & Data Schema", [
            ("Flexible Server", "PostgreSQL 14 in private delegated subnet subnet-ejdigsdaswpw4 (10.0.2.0/24)."),
            ("Seeded Data", "100 customer profiles, 500 catalog products, and 6,400+ transactional orders."),
            ("Index Optimization", "B-tree indexes on search keywords, category filters, and customer order foreign keys."),
            ("Zero-Trust Security", "Accessible only via private DNS privatelink.postgres.database.azure.com (10.0.2.4).")
        ]),
        # Slide 10: CI/CD
        ("content", "CI/CD & DevOps Automation", [
            ("GitHub Actions", "Automated pipeline configured in .github/workflows/deploy-app-loadtest-101.yml."),
            ("Automated Verification", "Runs npm test executing 8 self-contained integration tests (8 passed, 0 failed in 9s)."),
            ("Zero-Downtime Deployment", "Packages clean POSIX zip bundle and deploys directly to Azure App Service."),
            ("Verified Builds", "Recent commits bd6fbe1 and 9be1d2e verified with 100% CI/CD deployment success.")
        ]),
        # Slide 11: Monitoring
        ("content", "Application Insights & Telemetry", [
            ("APM Metrics", "Tracks end-to-end request durations, HTTP status codes, and exception stack traces."),
            ("Dependency Tracking", "Monitors PostgreSQL SQL query durations, connection latency, and execution plans."),
            ("Live Metrics Stream", "Real-time visibility into CPU, memory, incoming RPS, and active server instances."),
            ("Centralized Ingestion", "Log Analytics workspace (law-loadtest-101) aggregates container and Kudu diagnostics.")
        ]),
        # Slide 12: JMeter
        ("content", "Apache JMeter Test Plan Specification", [
            ("Scenario File", "loadtest/capacity_study.jmx — Parameterized for Azure Load Testing."),
            ("Dynamic Properties", "Configured via Groovy expressions to support CLI environment variables (app_host, threads)."),
            ("HTTP Request Defaults", "Connect timeout = 10,000 ms, Response timeout = 15,000 ms, Keep-Alive enabled."),
            ("Realistic Simulation", "Includes random timers, realistic browser headers, and JSON body payloads.")
        ]),
        # Slide 13: Methodology
        ("content", "Load Testing Methodology & Workflow", [
            ("Step 1: Baseline", "10 virtual users to establish baseline latency and system stability under minimal load."),
            ("Step 2: Progressive Ramp-Up", "50 and 100 virtual users to identify proportional throughput scaling."),
            ("Step 3: Knee Identification", "250 virtual users to observe queueing onset and response time inflection."),
            ("Step 4: Stress Testing", "500 virtual users on 1 instance to determine the definitive saturation breaking point."),
            ("Step 5: Scale-Out Validation", "500 virtual users on 2 instances to measure compute relief and ARR behavior.")
        ]),
        # Slide 14: Baseline
        ("image", "Baseline Capacity Testing (10 Users)", "01_users_vs_rps.png", [
            ("Concurrency", "10 Virtual Users | Duration: 120s | Instance Count: 1"),
            ("Throughput", "110.7 Requests Per Second (13,280 total requests)"),
            ("Latency", "Average: 83.0 ms | P50: 33.0 ms | P95: 310.0 ms | Peak: 2,240 ms"),
            ("Resource Utilization", "CPU: 17.7% | Memory: 42.1% | Errors: 0 (0.00%) — Optimal State")
        ]),
        # Slide 15: Progressive Load
        ("image", "Progressive Load Progression (50 & 100 Users)", "02_users_vs_avg_latency.png", [
            ("50 Users (run-2)", "144.9 RPS | Avg: 285 ms | P95: 1,022 ms | CPU: 38.0% | Errors: 0.00%"),
            ("100 Users (run-3)", "175.9 RPS | Avg: 489 ms | P95: 1,800 ms | CPU: 58.2% | Errors: 0.00%"),
            ("Safe Capacity Boundary", "100 users represents the highest concurrency maintaining 0.00% error rate."),
            ("Linear Scalability", "Throughput scaled smoothly from 110.7 to 175.9 RPS with healthy CPU headroom.")
        ]),
        # Slide 16: Bottleneck
        ("image", "Latency Knee & Degradation (250 Users)", "03_users_vs_p95.png", [
            ("Concurrency", "250 Virtual Users (run-4-heavy-250u-v2) | Instances: 1"),
            ("Throughput Plateau", "177.2 RPS (throughout stopped scaling proportionally)"),
            ("Latency Spike", "Avg latency rose to 1,176 ms; P95 surged from 1,800 ms to 7,257 ms."),
            ("Queueing Errors", "549 errors (2.42%) emerged as CPU utilization reached 78.5%.")
        ]),
        # Slide 17: 500-user Saturation
        ("image", "500-User Saturation Breaking Point", "05_users_vs_cpu.png", [
            ("Observed Breaking Point", "Single Standard S1 instance saturated under 500 virtual users."),
            ("CPU Core Saturation", "App Service CPU hit 96.4% sustained utilization."),
            ("Socket Timeout Limit", "P95 latency hit 15,010 ms (JMeter socket timeout limit)."),
            ("Error Severity", "1,305 failed requests (5.66% error rate) due to event loop backlog.")
        ]),
        # Slide 18: 2-instance Investigation
        ("image", "2-Instance Scale-Out Investigation", "07_1inst_vs_2inst_cpu.png", [
            ("Compute Headroom Relieved", "Average CPU per instance dropped from 96.4% down to 49.1% (-47.3%)."),
            ("Error Discrepancy", "Errors rose to 9.92% (1,783 failures) and RPS was 137.2."),
            ("Root Cause Identified", "ARR routed traffic to 2nd instance during cold start before connection pool priming."),
            ("Key Finding", "Scaling halves CPU pressure, but requires warmup probes to eliminate cold-start timeouts.")
        ]),
        # Slide 19: Autoscaling
        ("image", "Azure Monitor Dynamic Autoscale", "10_concurrency_vs_instances.png", [
            ("Autoscale Rule Set", "autoscale-plan-loadtest active on plan-loadtest (1 to 4 instances)."),
            ("Scale-Out Policy", "Average CPU > 70% sustained for 5 minutes increments instance count by +1."),
            ("Scale-In Policy", "Average CPU < 30% sustained for 5 minutes decrements instance count by -1."),
            ("Production Benefit", "Protects against sudden saturation spikes while conserving off-peak costs.")
        ]),
        # Slide 20: Before/After
        ("image", "1-Instance vs 2-Instance Detailed Comparison", "08_1inst_vs_2inst_latency.png", [
            ("CPU Metric", "1 Inst: 96.4% CPU (Saturated) vs 2 Inst: 49.1% CPU (Healthy Headroom)"),
            ("Latency Metric", "1 Inst: 2,365 ms Avg vs 2 Inst: 3,046 ms Avg (Warmup transition penalty)"),
            ("Throughput Metric", "1 Inst: 184.5 RPS vs 2 Inst: 137.2 RPS (Queueing during ramp-up)"),
            ("Takeaway", "CPU relief is instantaneous, but end-to-end stability requires warmed containers.")
        ]),
        # Slide 21: Dashboard
        ("content", "Azure Portal Performance Dashboard", [
            ("Dashboard Name", "capacity-performance-dashboard deployed directly in resource group rg-loadtest."),
            ("Compute Tile", "App Service Plan CPU % and Memory % over 24-hour evaluation window."),
            ("Web App Tile", "HTTP request throughput, average response latency, and HTTP 5xx errors."),
            ("Database & APM", "PostgreSQL active connections, CPU %, and Application Insights failure rates."),
            ("Capacity Matrix", "Embedded Markdown widget showing all 6 empirical load test runs.")
        ]),
        # Slide 22: Results
        ("content", "Summary Empirical Capacity Results", [
            ("10 Users", "110.7 RPS | 83 ms Avg | 310 ms P95 | 0.00% Errors | 17.7% CPU [PASS]"),
            ("50 Users", "144.9 RPS | 285 ms Avg | 1,022 ms P95 | 0.00% Errors | 38.0% CPU [PASS]"),
            ("100 Users", "175.9 RPS | 489 ms Avg | 1,800 ms P95 | 0.00% Errors | 58.2% CPU [SAFE LIMIT]"),
            ("250 Users", "177.2 RPS | 1,176 ms Avg | 7,257 ms P95 | 2.42% Errors | 78.5% CPU [KNEE]"),
            ("500 Users (1 Inst)", "184.5 RPS | 2,365 ms Avg | 15,010 ms P95 | 5.66% Errors | 96.4% CPU [BREAK]"),
            ("500 Users (2 Inst)", "137.2 RPS | 3,046 ms Avg | 15,010 ms P95 | 9.92% Errors | 49.1% CPU [RELIEVED]")
        ]),
        # Slide 23: Limitations
        ("content", "Study Limitations & Operational Constraints", [
            ("JMeter Socket Timeout", "15,000 ms response timeout marks extremely delayed requests as socket errors."),
            ("Network Co-Location", "Load generator and web app co-located in Central India; excludes global WAN transit."),
            ("Single Region", "Evaluation focused on single-region horizontal scaling without multi-region Front Door."),
            ("Database Cold Storage", "Pre-seeded tables in PostgreSQL cache; cold disk read paging not simulated.")
        ]),
        # Slide 24: Conclusion
        ("content", "Conclusion & Engineering Recommendations", [
            ("Definitive Capacity", "A single Standard S1 instance is optimal up to 100 concurrent virtual users."),
            ("Observed Saturation", "500 users saturates single-core compute, proving CPU is the governing bottleneck."),
            ("Scaling Impact", "Horizontal scaling cuts CPU utilization in half, but requires warmup priming in ARR."),
            ("Autoscale Policy", "70% scale-out threshold provides ideal reaction time before queueing escalates.")
        ]),
        # Slide 25: Future Scope
        ("content", "Future Work & Production Enhancements", [
            ("Azure Front Door", "Implement global Anycast routing with geo-distributed multi-region deployment."),
            ("Application Pre-Warming", "Configure <applicationInitialization> in web.config to eliminate ARR cold starts."),
            ("Database Read Replicas", "Deploy PostgreSQL read replicas with PgBouncer connection pooling."),
            ("Chaos Engineering", "Introduce Azure Chaos Studio to inject container and network faults during load tests.")
        ])
    ]

    for idx, item in enumerate(slides_data, start=1):
        slide = prs.slides.add_slide(blank_layout)
        apply_bg(slide)
        slide_type = item[0]
        title_text = item[1]

        if slide_type == "title":
            # Big Title
            tbox = slide.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(2.0))
            p = tbox.text_frame.paragraphs[0]
            p.text = title_text
            p.font.size = Pt(32)
            p.font.bold = True
            p.font.color.rgb = C_TEXT

            # Subtitle
            sbox = slide.shapes.add_textbox(Inches(1.0), Inches(4.0), Inches(11.3), Inches(2.5))
            for k, v in item[2]:
                p_item = sbox.text_frame.add_paragraph()
                r1 = p_item.add_run()
                r1.text = f"• {k}: "
                r1.font.bold = True
                r1.font.size = Pt(15)
                r1.font.color.rgb = C_GLOW
                r2 = p_item.add_run()
                r2.text = f"{v}"
                r2.font.size = Pt(15)
                r2.font.color.rgb = C_MUTED

        elif slide_type == "team":
            add_header(slide, title_text, f"SLIDE {idx} / 25 • TEAM INFORMATION")
            top_y = 2.0
            for name, role in item[2]:
                card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(top_y), Inches(11.3), Inches(1.05))
                card.fill.solid()
                card.fill.fore_color.rgb = C_CARD
                card.line.color.rgb = RGBColor(30, 41, 59)
                
                tf = card.text_frame
                tf.margin_left = Inches(0.4)
                tf.margin_top = Inches(0.2)
                p1 = tf.paragraphs[0]
                p1.text = name
                p1.font.bold = True
                p1.font.size = Pt(15)
                p1.font.color.rgb = C_GLOW
                
                p2 = tf.add_paragraph()
                p2.text = f"Role: {role}"
                p2.font.size = Pt(12)
                p2.font.color.rgb = C_MUTED
                top_y += 1.25

        elif slide_type == "content":
            add_header(slide, title_text, f"SLIDE {idx} / 25 • ARCHITECTURE & ANALYSIS")
            top_y = 2.0
            for heading, detail in item[2]:
                card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(top_y), Inches(11.3), Inches(0.95))
                card.fill.solid()
                card.fill.fore_color.rgb = C_CARD
                card.line.color.rgb = RGBColor(30, 41, 59)
                
                tf = card.text_frame
                tf.margin_left = Inches(0.35)
                tf.margin_top = Inches(0.18)
                p1 = tf.paragraphs[0]
                p1.text = heading
                p1.font.bold = True
                p1.font.size = Pt(14)
                p1.font.color.rgb = C_GLOW
                
                p2 = tf.add_paragraph()
                p2.text = detail
                p2.font.size = Pt(12)
                p2.font.color.rgb = C_MUTED
                top_y += 1.05

        elif slide_type == "image":
            img_file = item[2]
            points = item[3]
            add_header(slide, title_text, f"SLIDE {idx} / 25 • EMPIRICAL EVIDENCE")
            
            # Left: Embed actual graph image
            img_path = os.path.join("reports", "graphs", img_file)
            if os.path.exists(img_path):
                slide.shapes.add_picture(img_path, Inches(1.0), Inches(1.8), width=Inches(6.2))
            
            # Right: Bullet points card
            card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.5), Inches(1.8), Inches(4.8), Inches(4.8))
            card.fill.solid()
            card.fill.fore_color.rgb = C_CARD
            card.line.color.rgb = RGBColor(30, 41, 59)
            
            tf = card.text_frame
            tf.margin_left = Inches(0.3)
            tf.margin_top = Inches(0.3)
            p_hdr = tf.paragraphs[0]
            p_hdr.text = "Key Empirical Observations:"
            p_hdr.font.bold = True
            p_hdr.font.size = Pt(14)
            p_hdr.font.color.rgb = C_AZURE
            
            for k, v in points:
                p_pt = tf.add_paragraph()
                p_pt.margin_top = Pt(8)
                r_k = p_pt.add_run()
                r_k.text = f"• {k}: "
                r_k.font.bold = True
                r_k.font.size = Pt(11)
                r_k.font.color.rgb = C_TEXT
                r_v = p_pt.add_run()
                r_v.text = v
                r_v.font.size = Pt(11)
                r_v.font.color.rgb = C_MUTED

    out_pptx = "reports/Azure-Load-Testing-Capacity-Study-Presentation.pptx"
    prs.save(out_pptx)
    print(f"Successfully generated {out_pptx} with 25 slides.")

if __name__ == "__main__":
    create_presentation()
