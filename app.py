# =========================================================
# COMPRESSED AIR SYSTEM SIMULATOR ISO 8573
# + PDF REPORT GENERATOR
# =========================================================

import streamlit as st
import pandas as pd
import math
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.platypus.flowables import PageBreak
from io import BytesIO

# =========================================================
# PAGE CONFIG
# =========================================================

st.image("suto_logo.png", width=260)
st.set_page_config(page_title="Compressed Air Simulator", layout="wide")

st.title("Compressed Air System Simulator")

# =========================================================
# INPUT SECTION
# =========================================================

st.sidebar.header("Input Parameters")

compressor_kw = st.sidebar.number_input(
    "Compressor Power (kW)",
    min_value=1.0,
    value=37.0,
    step=1.0
)

pressure_barg = st.sidebar.number_input(
    "Working Pressure (barg)",
    min_value=1.0,
    value=7.0,
    step=0.5
)

ambient_temp = st.sidebar.number_input(
    "Ambient Temperature (°C)",
    value=35.0,
    step=1.0
)

compressor_type = st.sidebar.selectbox(
    "Compressor Type",
    [
        "Oil Injected Screw",
        "Oil Free / Oil Less"
    ]
)

dryer_type = st.sidebar.selectbox(
    "Dryer Type",
    [
        "Refrigerated Dryer",
        "Desiccant Dryer"
    ]
)

# =========================================================
# TYPICAL PDP
# =========================================================

if dryer_type == "Refrigerated Dryer":

    recommended_pdp = 3
    best_pdp = 0

else:

    recommended_pdp = -40
    best_pdp = -70

# =========================================================
# ACTUAL PDP
# =========================================================

actual_pdp = st.sidebar.number_input(
    "Actual Measured PDP (°C)",
    value=float(recommended_pdp),
    step=1.0
)

# =========================================================
# CALCULATIONS
# =========================================================

pressure_abs = pressure_barg + 1

flow_m3min = compressor_kw * 0.13

# Magnus formula
svp = 0.61094 * math.exp(
    (17.625 * actual_pdp) /
    (actual_pdp + 243.04)
)

# Water content
water_content = (
    2167 * svp /
    (actual_pdp + 273.15)
)

# Atmospheric equivalent
water_content_atm = (
    water_content * pressure_abs
)

# Oil estimation
if compressor_type == "Oil Injected Screw":

    if dryer_type == "Refrigerated Dryer":
        oil_content = "2 – 5 mg/m3"
    else:
        oil_content = "0.01 – 0.1 mg/m3"

else:

    oil_content = "<0.01 mg/m3"

# =========================================================
# RESULTS
# =========================================================

st.header("Simulation Results")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Estimated Flow",
        f"{flow_m3min:.2f} m3/min"
    )

    st.metric(
        "Pressure Absolute",
        f"{pressure_abs:.1f} barA"
    )

    st.metric(
        "Actual PDP",
        f"{actual_pdp:.1f} °C"
    )

with col2:

    st.metric(
        "Water Content",
        f"{water_content_atm:.2f} g/m3"
    )

    st.metric(
        "Estimated Oil Content",
        oil_content
    )

    st.metric(
        "Typical PDP Target",
        f"{recommended_pdp} °C"
    )

# =========================================================
# CONDITION ANALYSIS
# =========================================================

st.header("Condition Analysis")

analysis_text = ""

if dryer_type == "Desiccant Dryer":

    if actual_pdp <= -40:

        analysis_text = """
GOOD dryer performance.
Desiccant condition likely healthy.
Suitable for instrument air.
"""

        st.success(analysis_text)

    elif actual_pdp <= -20:

        analysis_text = """
Dryer performance degraded.
Possible partial desiccant saturation.
"""

        st.warning(analysis_text)

    else:

        analysis_text = """
BAD dryer performance.

Possible causes:
- saturated desiccant
- damaged molecular sieve
- purge failure
- valve leakage
"""

        st.error(analysis_text)

else:

    if actual_pdp <= 5:

        analysis_text = """
Refrigerated dryer operating normally.
"""

        st.success(analysis_text)

    else:

        analysis_text = """
Refrigerated dryer performance degraded.
"""

        st.warning(analysis_text)

# =========================================================
# PDF GENERATOR
# =========================================================

def generate_pdf():

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    elements = []

    # Title
    title = Paragraph(
        "Compressed Air System Report",
        styles['Title']
    )

    elements.append(title)
    elements.append(Spacer(1, 20))

    # Input Table
    input_data = [
        ["Parameter", "Value"],

        ["Compressor Power", f"{compressor_kw} kW"],
        ["Working Pressure", f"{pressure_barg} barg"],
        ["Ambient Temperature", f"{ambient_temp} °C"],
        ["Compressor Type", compressor_type],
        ["Dryer Type", dryer_type],
        ["Actual PDP", f"{actual_pdp} °C"]
    ]

    input_table = Table(input_data)

    input_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')
    ]))

    elements.append(
        Paragraph("Input Parameters", styles['Heading2'])
    )

    elements.append(input_table)
    elements.append(Spacer(1, 20))

    # Result Table
    result_data = [
        ["Result", "Value"],

        ["Estimated Flow", f"{flow_m3min:.2f} m3/min"],
        ["Pressure Absolute", f"{pressure_abs:.1f} barA"],
        ["Water Content", f"{water_content_atm:.2f} g/m3"],
        ["Estimated Oil Content", oil_content],
        ["Recommended PDP", f"{recommended_pdp} °C"]
    ]

    result_table = Table(result_data)

    result_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgreen),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')
    ]))

    elements.append(
        Paragraph("Calculation Results", styles['Heading2'])
    )

    elements.append(result_table)
    elements.append(Spacer(1, 20))

    # Analysis
    elements.append(
        Paragraph("Condition Analysis", styles['Heading2'])
    )

    elements.append(
        Paragraph(analysis_text, styles['BodyText'])
    )

    # Footer
    elements.append(Spacer(1, 40))

    footer = Paragraph(
        "Generated by Compressed Air Engineering Simulator",
        styles['Italic']
    )

    elements.append(footer)

    # Build PDF
    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf

# =========================================================
# DOWNLOAD PDF
# =========================================================

pdf_file = generate_pdf()

st.download_button(
    label="Download PDF Report",
    data=pdf_file,
    file_name="compressed_air_report.pdf",
    mime="application/pdf"
)

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")
st.caption("Compressed Air Engineering Simulator")
