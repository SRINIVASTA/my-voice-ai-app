# 🎙️ Mock AI Voice Telephony & Automation Sandbox Dashboard

⚠️ **PROJECT TYPE: 100% CONCEPTUAL MOCK SANDBOX SIMULATOR** ⚠️  
*This software is a simulation environment designed to safely run, evaluate, and stress-test concurrent calling workflows, timer controls, database logging, and data analytics. It does NOT make real phone calls, does NOT dial actual mobile numbers, and does NOT connect to physical telecommunications networks out-of-the-box.*

An asynchronous, cloud-hosted **mock conversational calling simulator** built with **Python**, **Streamlit**, and **Plotly**. This project simulates an independent, account-free outbound calling architecture capable of demonstrating how 10 to 100 concurrent lines run simultaneously, enforcing a strict 1-minute simulated call duration cap, archiving mock text responses into a local SQLite database, and auto-generating PDF reports.

---

## 🏛️ Simulated Architecture Layout

This sandbox mirrors the exact digital operational logic required to execute mass telephony, allowing developers to test systems without incurring billing fees or risking telecom spam blocks.

```text
[Simulated Mobile Target] 
          ▲
          │ (Mock Virtual Signals)
[Mock GSM VoIP Gateway Engine] ◄═══(Simulated SIP Pipeline)═══► [Your Python AI Server]
 (Simulated 10 to 100 Slots)                                      (Hosted Web Dashboard Engine)
                                                                            │
                                                  +─────────────────────────+─────────────────────────+
                                                  │                         │                         │
                                          1. Mock SQLite DB         2. Plotly Telemetry       3. ReportLab Compiler
                                            (Local File Archive)       (Subplot Dashboards)      (Automated PDF Export)
```

---

## 🚀 Mock Engine Capabilities & Features

* **Asynchronous Concurrency Loop:** Uses Python's `asyncio` to mock multiple calling channels taking lines off-hook at the exact same fraction of a second.
* **Strict 1-Minute Session Cap:** Simulates a hardware-level thread timer that forces a mock call drop at exactly 60 seconds to demonstrate bandwidth protection rules.
* **Automated Escalation Tracker:** An algorithmic text-parsing engine that automatically filters the mock text responses for citizen grievances (e.g., "no", "late", "error") and highlights them for follow-up.
* **Interactive Telemetry Visualizations:** Generates immediate data dashboards using dark-themed Plotly charts mapping channel durations and virtual pickup statistics.
* **On-Demand Management Exports:** Packages the simulated calling metrics into immediate `CSV` spreadsheets and formal `PDF` executive report layouts.

---

## 📂 Project Repository Tree

```text
my-voice-ai-app/
├── .streamlit/
│   └── config.toml          # Custom theme settings and server profile configurations
├── modules/
│   ├── __init__.py          # Marks the folder as an importable package module
│   └── pdf_generator.py     # Compiles ReportLab canvas elements into formatted PDFs
├── dashboard.py             # Main entry point (Handles mock simulation logic & Streamlit UI)
├── README.md                # Comprehensive documentation and setup guides
└── requirements.txt         # Core project library dependencies
```

---

## 🕹️ Cloud Sandbox Operational Guide

When deployed to **Streamlit Community Cloud**, the project operates in a zero-hardware simulation loop:

1. Locate the **Simulation Control Tower** panel inside the left-hand sidebar menu.
2. Click the **"🚀 Launch 15 Concurrent Calls (1 Min Max)"** execution button.
3. The background cloud container will instantly spin up parallel asynchronous mock tasks, populate the local `call_logs.db` file, and update the interactive Plotly graphs automatically.
4. Scroll to the base of the webpage to access your **Automated Escalation Spreadsheet** and downloadable **Executive PDF Reports**.

---

## 🛠️ Local System Installation & Setup

If you wish to host this mock sandbox locally on your workstation for testing purposes:

### 1. Clone the Repository
```bash
git clone https://github.com/srinivasta/my-voice-ai-app.git
cd my-voice-ai-app
```

### 2. Install Project Dependencies
Ensure you have Python 3.10+ installed, then populate the missing library wrappers:
```bash
pip install -r requirements.txt
```

### 3. Initialize the Local Workspace
Launch the dashboard compiler framework inside your terminal window:
```bash
streamlit run dashboard.py
```
