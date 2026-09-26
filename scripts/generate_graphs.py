import csv
import os
import matplotlib.pyplot as plt
import numpy as np

# Set high DPI and aesthetic styling
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.sans-serif'] = 'Segoe UI', 'DejaVu Sans', 'Arial'
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 1.2

OUT_DIR = "reports/graphs"
os.makedirs(OUT_DIR, exist_ok=True)

# Load data from CSV
matrix_file = "results/final_capacity_matrix.csv"
runs = []
with open(matrix_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        runs.append({
            "run_id": r["run_id"],
            "users": int(r["users"]),
            "instances": int(r["instances"]),
            "rps": float(r["rps"]),
            "avg_latency": float(r["average_latency_ms"]),
            "p50": float(r["p50_ms"]),
            "p95": float(r["p95_ms"]),
            "p99": float(r["p99_ms"]),
            "peak": float(r["peak_latency_ms"]),
            "errors": int(r["errors"]),
            "error_pct": float(r["error_percentage"]),
            "cpu": float(r["cpu_percentage"]),
            "mem": float(r["memory_percentage"]),
            "assessment": r["assessment"]
        })

single_inst = [r for r in runs if r["instances"] == 1]
dual_inst = [r for r in runs if r["instances"] == 2]

u_single = [r["users"] for r in single_inst]
rps_single = [r["rps"] for r in single_inst]
avg_single = [r["avg_latency"] for r in single_inst]
p50_single = [r["p50"] for r in single_inst]
p95_single = [r["p95"] for r in single_inst]
p99_single = [r["p99"] for r in single_inst]
cpu_single = [r["cpu"] for r in single_inst]
err_single = [r["error_pct"] for r in single_inst]

# 1. Users vs RPS
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(u_single, rps_single, marker='o', color='#0078d4', linewidth=2.5, markersize=8, label='Throughput (RPS)')
for x, y in zip(u_single, rps_single):
    ax.annotate(f"{y:.1f} RPS", (x, y), textcoords="offset points", xytext=(0, 10), ha='center', fontweight='bold', fontsize=9, color='#004578')
ax.set_title("Workload Concurrency vs Throughput (RPS)\nProject: 24CC3046-P056 (Azure App Service Standard S1)", fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel("Concurrent Virtual Users", fontsize=10, fontweight='bold')
ax.set_ylabel("Requests Per Second (RPS)", fontsize=10, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.5)
ax.set_ylim(80, 210)
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/01_users_vs_rps.png")
plt.close()

# 2. Users vs Average Latency
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(u_single, avg_single, marker='s', color='#d83b01', linewidth=2.5, markersize=8, label='Average Latency (ms)')
for x, y in zip(u_single, avg_single):
    ax.annotate(f"{int(y)} ms", (x, y), textcoords="offset points", xytext=(0, 10), ha='center', fontweight='bold', fontsize=9, color='#a80000')
ax.axhline(1000, color='#ea4335', linestyle=':', label='SLA Warning Threshold (1000 ms)')
ax.set_title("Workload Concurrency vs Average Response Latency\nProject: 24CC3046-P056 (Azure App Service Standard S1)", fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel("Concurrent Virtual Users", fontsize=10, fontweight='bold')
ax.set_ylabel("Average Response Time (ms)", fontsize=10, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(loc='upper left')
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/02_users_vs_avg_latency.png")
plt.close()

# 3. Users vs P95 Latency
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(u_single, p95_single, marker='^', color='#8764b8', linewidth=2.5, markersize=8, label='P95 Latency (ms)')
for x, y in zip(u_single, p95_single):
    label_text = f"{int(y)} ms (Socket Timeout)" if y >= 15000 else f"{int(y)} ms"
    ax.annotate(label_text, (x, y), textcoords="offset points", xytext=(0, 10), ha='center', fontweight='bold', fontsize=8, color='#5c2d91')
ax.axhline(15000, color='#d13438', linestyle='--', label='JMeter Socket Timeout Boundary (15,000 ms)')
ax.set_title("Workload Concurrency vs 95th Percentile (P95) Latency\nProject: 24CC3046-P056 (Azure App Service Standard S1)", fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel("Concurrent Virtual Users", fontsize=10, fontweight='bold')
ax.set_ylabel("P95 Latency (ms)", fontsize=10, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(loc='upper left')
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/03_users_vs_p95.png")
plt.close()

# 4. Users vs P99 Latency
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(u_single, p99_single, marker='D', color='#b4009e', linewidth=2.5, markersize=8, label='P99 Latency (ms)')
for x, y in zip(u_single, p99_single):
    ax.annotate(f"{int(y)} ms", (x, y), textcoords="offset points", xytext=(0, 10), ha='center', fontweight='bold', fontsize=9, color='#750b1c')
ax.set_title("Workload Concurrency vs 99th Percentile (P99) Latency\nProject: 24CC3046-P056 (Azure App Service Standard S1)", fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel("Concurrent Virtual Users", fontsize=10, fontweight='bold')
ax.set_ylabel("P99 Latency (ms)", fontsize=10, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(loc='upper left')
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/04_users_vs_p99.png")
plt.close()

# 5. Users vs App Service CPU %
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(u_single, cpu_single, marker='h', color='#ff8c00', linewidth=2.5, markersize=8, label='App Service CPU %')
for x, y in zip(u_single, cpu_single):
    ax.annotate(f"{y:.1f}%", (x, y), textcoords="offset points", xytext=(0, 10), ha='center', fontweight='bold', fontsize=9, color='#c239b3')
ax.axhline(70, color='#f7630c', linestyle='--', label='Autoscale Scale-Out Trigger (70% CPU)')
ax.axhline(80, color='#d13438', linestyle=':', label='Capacity Saturation Boundary (80% CPU)')
ax.set_title("Workload Concurrency vs Azure App Service CPU Utilization\nProject: 24CC3046-P056 (Single Standard S1 Instance)", fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel("Concurrent Virtual Users", fontsize=10, fontweight='bold')
ax.set_ylabel("CPU Utilization (%)", fontsize=10, fontweight='bold')
ax.set_ylim(0, 105)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(loc='upper left')
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/05_users_vs_cpu.png")
plt.close()

# 6. Users vs Error %
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar([str(u) for u in u_single], err_single, color=['#107c41', '#107c41', '#107c41', '#f7630c', '#d13438'], width=0.5, edgecolor='#000', linewidth=0.8)
for i, (u, err) in enumerate(zip(u_single, err_single)):
    ax.text(i, err + 0.2, f"{err:.2f}%", ha='center', fontweight='bold', fontsize=9)
ax.axhline(1.0, color='#d13438', linestyle='--', label='SLA Maximum Error Target (< 1.0%)')
ax.set_title("Workload Concurrency vs HTTP Error Percentage\nProject: 24CC3046-P056 (Single Standard S1 Instance)", fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel("Concurrent Virtual Users", fontsize=10, fontweight='bold')
ax.set_ylabel("Error Rate (%)", fontsize=10, fontweight='bold')
ax.set_ylim(0, 8.0)
ax.grid(True, linestyle='--', alpha=0.5, axis='y')
ax.legend(loc='upper left')
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/06_users_vs_error_rate.png")
plt.close()

# 7. 1-instance vs 2-instance CPU
fig, ax = plt.subplots(figsize=(7, 5))
categories = ['500 Users (1 Instance)', '500 Users (2 Instances)']
cpus = [96.4, 49.1]
colors = ['#d13438', '#107c41']
bars = ax.bar(categories, cpus, color=colors, width=0.45, edgecolor='#000', linewidth=1)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 2, f"{yval:.1f}%", ha='center', fontweight='bold', fontsize=11)
ax.axhline(70, color='#ea4335', linestyle='--', alpha=0.7, label='Autoscale Scale-Out Trigger (70%)')
ax.set_title("App Service CPU Utilization: 1 Instance vs 2 Instances\nUnder 500 Virtual Users Workload (Project 24CC3046-P056)", fontsize=12, fontweight='bold', pad=12)
ax.set_ylabel("CPU Utilization per Instance (%)", fontsize=10, fontweight='bold')
ax.set_ylim(0, 115)
ax.grid(True, linestyle='--', alpha=0.5, axis='y')
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/07_1inst_vs_2inst_cpu.png")
plt.close()

# 8. 1-instance vs 2-instance latency
fig, ax = plt.subplots(figsize=(8, 5))
labels = ['Avg Latency', 'Median (P50)', 'P95 Latency']
inst1_vals = [2365.0, 291.0, 15010.0]
inst2_vals = [3046.0, 1428.0, 15010.0]
x = np.arange(len(labels))
width = 0.35
rects1 = ax.bar(x - width/2, inst1_vals, width, label='1 Instance (500u)', color='#d13438', edgecolor='#000')
rects2 = ax.bar(x + width/2, inst2_vals, width, label='2 Instances (500u)', color='#0078d4', edgecolor='#000')
for rect in rects1:
    h = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2, h + 300, f"{int(h)}ms", ha='center', fontsize=8, fontweight='bold')
for rect in rects2:
    h = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2, h + 300, f"{int(h)}ms", ha='center', fontsize=8, fontweight='bold')
ax.set_title("Latency Profile Comparison: 1 Instance vs 2 Instances\n(500 Concurrent Virtual Users)", fontsize=12, fontweight='bold', pad=12)
ax.set_ylabel("Latency (ms)", fontsize=10, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(labels, fontweight='bold')
ax.set_ylim(0, 18000)
ax.grid(True, linestyle='--', alpha=0.5, axis='y')
ax.legend()
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/08_1inst_vs_2inst_latency.png")
plt.close()

# 9. 1-instance vs 2-instance error % and throughput
fig, ax1 = plt.subplots(figsize=(8, 5))
categories = ['1 Instance (500u)', '2 Instances (500u)']
errs = [5.66, 9.92]
rps_vals = [184.54, 137.22]
x = np.arange(len(categories))
width = 0.35
rects1 = ax1.bar(x - width/2, errs, width, label='Error Rate (%)', color='#e81123', edgecolor='#000')
ax1.set_ylabel('Error Percentage (%)', color='#e81123', fontweight='bold')
ax1.tick_params(axis='y', labelcolor='#e81123')
ax1.set_ylim(0, 14)

ax2 = ax1.twinx()
rects2 = ax2.bar(x + width/2, rps_vals, width, label='Throughput (RPS)', color='#0078d4', edgecolor='#000')
ax2.set_ylabel('Throughput (RPS)', color='#0078d4', fontweight='bold')
ax2.tick_params(axis='y', labelcolor='#0078d4')
ax2.set_ylim(0, 240)

for rect in rects1:
    h = rect.get_height()
    ax1.text(rect.get_x() + rect.get_width()/2, h + 0.3, f"{h:.2f}%", ha='center', fontweight='bold', color='#e81123')
for rect in rects2:
    h = rect.get_height()
    ax2.text(rect.get_x() + rect.get_width()/2, h + 4, f"{h:.1f}", ha='center', fontweight='bold', color='#0078d4')

plt.title("Error Rate and Throughput Comparison: 1 Instance vs 2 Instances\nInvestigating Cold-Start & ARR Overhead (Project 24CC3046-P056)", fontsize=11, fontweight='bold', pad=12)
ax1.set_xticks(x)
ax1.set_xticklabels(categories, fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.5, axis='y')
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/09_1inst_vs_2inst_errors.png")
plt.close()

# 10. Instance count vs load
fig, ax = plt.subplots(figsize=(8, 5))
users_axis = [10, 50, 100, 250, 500, 750, 1000]
recommended_instances = [1, 1, 1, 2, 2, 3, 4]
ax.step(users_axis, recommended_instances, where='post', color='#0078d4', linewidth=2.5, marker='o', label='Recommended Scale Instances')
for x_val, y_val in zip(users_axis, recommended_instances):
    ax.annotate(f"{y_val} Inst ({x_val}u)", (x_val, y_val), textcoords="offset points", xytext=(-10, 10), fontweight='bold', fontsize=9, color='#004578')
ax.axvspan(0, 100, color='#107c41', alpha=0.15, label='Safe Zone (1 Instance: 0% Errors, CPU < 60%)')
ax.axvspan(100, 250, color='#ffb900', alpha=0.15, label='Queueing Knee (Autoscale Recommended)')
ax.axvspan(250, 500, color='#d13438', alpha=0.15, label='Saturation Zone (Horizontal Scale Required)')
ax.set_title("Capacity Sizing Curve: Virtual Users vs Recommended App Service Instances\nProject: 24CC3046-P056 (Azure Autoscale 1-4 Tier)", fontsize=11, fontweight='bold', pad=12)
ax.set_xlabel("Concurrent Virtual Users", fontsize=10, fontweight='bold')
ax.set_ylabel("App Service Instance Count", fontsize=10, fontweight='bold')
ax.set_yticks([1, 2, 3, 4])
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(loc='lower right', fontsize=8)
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/10_concurrency_vs_instances.png")
plt.close()

print("All 10 performance graphs successfully generated in reports/graphs/")
