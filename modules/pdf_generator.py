from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(df, filename="call_summary_report.pdf"):
    """Compiles a clean tabular analytical summary of call history metrics to a PDF file."""
    doc = SimpleDocTemplate(filename, pagesize=letter, title="AI Calling Suite Summary")
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=15
    )
    body_style = styles['Normal']
    
    story = []
    story.append(Paragraph("<b>AI Calling Suite Executive Summary</b>", title_style))
    story.append(Spacer(1, 10))
    
    # Calculate key aggregate metrics for header inclusion
    total_calls = len(df)
    connected = len(df[df["duration"] > 0])
    failed = len(df[df["duration"] == 0])
    
    summary_text = f"<b>Total Dial Attempts:</b> {total_calls} | <b>Connected:</b> {connected} | <b>Failed Lines:</b> {failed}"
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 20))
    
    # Setup structural tables for grid rows
    table_data = [["Timestamp", "SIM Slot", "Phone Number", "Status", "Duration", "Captured Input"]]
    
    for _, row in df.iterrows():
        table_data.append([
            str(row['timestamp'])[:19],
            str(row['sim_slot']),
            str(row['phone_number']),
            str(row['status']),
            f"{row['duration']}s",
            Paragraph(str(row['citizen_speech']), body_style)
        ])
        
    t = Table(table_data, colWidths=[110, 50, 90, 90, 50, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    
    story.append(t)
    doc.build(story)
