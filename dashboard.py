import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from modules.pdf_generator import generate_pdf_report

st.set_page_config(layout="wide", page_title="AI Calling Live Monitor")
st.title("📊 AI Telephony Dashboard (Local Database Monitor)")

def load_database_data():
    try:
        conn = sqlite3.connect("call_logs.db")
        df = pd.read_sql_query("SELECT * FROM calls ORDER BY timestamp DESC", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame(columns=["id", "sim_slot", "phone_number", "status", "duration", "citizen_speech", "timestamp"])

df = load_database_data()

if df.empty:
    st.info("⏳ Waiting for database input data. Execute 'python app_dialer.py' first in your terminal.")
else:
    # Render operational high-level metrics cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Dial Attempts", len(df))
    col2.metric("Connected Calls", len(df[df["duration"] > 0]))
    col3.metric("Blocked / No Answer", len(df[df["duration"] == 0]))
    col4.metric("Avg Duration", f"{int(df[df['duration'] > 0]['duration'].mean())}s" if len(df[df['duration'] > 0]) > 0 else "0s")

    st.markdown("---")

    # Plotly Graph Grid Elements
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "domain"}, {"type": "bar"}]],
                        subplot_titles=("Call Status Summary", "Hardware Channel Time Capacity"))

    status_metrics = df["status"].value_counts()
    fig.add_trace(go.Pie(labels=status_metrics.index, values=status_metrics.values, hole=0.4), row=1, col=1)

    bar_colors = ['#E74C3C' if d == 0 else ('#3498DB' if d < 60 else '#2ECC71') for d in df["duration"]]
    fig.add_trace(go.Bar(x=df["sim_slot"], y=df["duration"], text=df["duration"].astype(str) + "s", marker_color=bar_colors), row=1, col=2)

    fig.update_layout(template="plotly_dark", height=450)
    st.plotly_chart(fig, use_container_width=True)

    # Automated Escalation Filtering logic blocks
    st.markdown("---")
    st.subheader("🚨 Automated Escalation Tracker")
    escalation_df = df[df['citizen_speech'].str.contains('No|late|error', case=False, na=False)]

    if not escalation_df.empty:
        st.warning(f"Found {len(escalation_df)} active citizen complaints requiring follow-up action:")
        st.dataframe(escalation_df[["timestamp", "phone_number", "sim_slot", "citizen_speech"]], use_container_width=True)
    else:
        st.success("✅ Clean Record: No unresolved grievances found.")

    # Executive Export Tool Hooks
    if st.button("Generate Executive PDF Report"):
        generate_pdf_report(df)
        st.success("📝 Success: Compiled document and written file to 'call_summary_report.pdf'.")
