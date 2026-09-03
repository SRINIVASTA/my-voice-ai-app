import streamlit as st
import sqlite3
import pandas as pd
import asyncio
import random
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from modules.pdf_generator import generate_pdf_report

st.set_page_config(layout="wide", page_title="AI Calling Live Monitor")
st.title("📊 AI Telephony Dashboard (Cloud Sandbox Mode)")

DB_NAME = "call_logs.db"

# 🗄️ 1. Database & Simulation Logic
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sim_slot TEXT,
            phone_number TEXT,
            status TEXT,
            duration INTEGER,
            citizen_speech TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_log(slot, phone, status, duration, speech):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO calls (sim_slot, phone_number, status, duration, citizen_speech) VALUES (?, ?, ?, ?, ?)",
        (slot, phone, status, duration, speech)
    )
    conn.commit()
    conn.close()

async def simulate_call_session(phone, slot_id):
    await asyncio.sleep(random.uniform(0.2, 0.8)) # Simulated network time
    is_answered = random.choices([True, False], weights=[0.85, 0.15])[0]
    
    if not is_answered:
        save_log(f"Slot {slot_id:02d}", phone, "No Answer", 0, "N/A")
        return

    telugu_citizen_inputs = [
        "Yes, I received the pension on time.",
        "No, the official came two days late.",
        "The process was smooth, thank you.",
        "I had to submit my documents twice.",
        "Everything is working perfectly fine.",
        "There was an error in my transaction."
    ]
    
    duration = random.choice([15, 30, 45, 60])
    status = "Completed (Max Limit)" if duration == 60 else "Citizen Hung Up Early"
    speech_captured = random.choice(telugu_citizen_inputs)
    
    save_log(f"Slot {slot_id:02d}", phone, status, duration, speech_captured)

async def run_batch_simulation():
    init_db()
    phone_list = [f"+9198765432{i:02d}" for i in range(1, 16)]
    tasks = [simulate_call_session(num, idx + 1) for idx, num in enumerate(phone_list)]
    await asyncio.gather(*tasks)

def load_database_data():
    try:
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query("SELECT * FROM calls ORDER BY timestamp DESC", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

# 🎛️ 2. Web Interface Controls
st.sidebar.header("🕹️ Simulation Control Tower")
st.sidebar.write("Click below to simulate generating call metrics on the cloud server.")

if st.sidebar.button("🚀 Launch 15 Concurrent Calls (1 Min Max)"):
    with st.spinner("Simulating live connections across hardware SIM channels..."):
        # Run the async loop inside the Streamlit context
        asyncio.run(run_batch_simulation())
    st.sidebar.success("🎉 Batch Completed & Archived!")

# --- RENDERING DASHBOARD DATA ---
df = load_database_data()

if df.empty:
    st.info("⏳ **Database is currently empty.** Click the **'Launch 15 Concurrent Calls'** button inside the left sidebar menu to run the simulation directly on Streamlit Cloud.")
else:
    # Render operational high-level metrics cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Dial Attempts", len(df))
    col2.metric("Connected Calls", len(df[df["duration"] > 0]))
    col3.metric("Blocked / No Answer", len(df[df["duration"] == 0]))
    col4.metric("Avg Duration", f"{int(df[df['duration'] > 0]['duration'].mean())}s" if len(df[df['duration'] > 0]) > 0 else "0s")

    st.markdown("---")

    # Plotly Graph UI Generation
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "domain"}, {"type": "bar"}]],
                        subplot_titles=("Call Status Summary", "Hardware Channel Time Capacity"))

    status_metrics = df["status"].value_counts()
    fig.add_trace(go.Pie(labels=status_metrics.index, values=status_metrics.values, hole=0.4), row=1, col=1)

    bar_colors = ['#E74C3C' if d == 0 else ('#3498DB' if d < 60 else '#2ECC71') for d in df["duration"]]
    fig.add_trace(go.Bar(x=df["sim_slot"], y=df["duration"], text=df["duration"].astype(str) + "s", marker_color=bar_colors), row=1, col=2)

    fig.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Automated Escalation Table Layout
    st.markdown("---")
    st.subheader("🚨 Automated Escalation Tracker")
    escalation_df = df[df['citizen_speech'].str.contains('No|late|error', case=False, na=False)]

    if not escalation_df.empty:
        st.warning(f"Found {len(escalation_df)} active complaints requiring follow-up action:")
        st.dataframe(escalation_df[["timestamp", "phone_number", "sim_slot", "citizen_speech"]], use_container_width=True)
        
        # Download filtered escalation list straight from the browser
        csv_data = escalation_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Escalation Spreadsheet (CSV)", csv_data, "escalation_list.csv", "text/csv")
    else:
        st.success("✅ Clean Record: No unresolved grievances found.")

    # PDF Generator Report Button Block
    st.markdown("---")
    if st.button("Generate Executive PDF Report Document"):
        generate_pdf_report(df, filename="call_summary_report.pdf")
        
        with open("call_summary_report.pdf", "rb") as pdf_file:
            st.download_button(
                label="📥 Download Compiled PDF Summary Report",
                data=pdf_file,
                file_name="executive_call_summary.pdf",
                mime="application/pdf"
            )
