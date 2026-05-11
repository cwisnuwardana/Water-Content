# =========================================================
# COMPRESSED AIR QUALITY CALCULATOR
# Dew Point -> Water Content
# Oil Injected vs Oil Free Compressor
# =========================================================

import streamlit as st
import math
import pandas as pd

st.set_page_config(page_title="Compressed Air Quality", layout="wide")

st.title("Compressed Air Quality Calculator")
st.markdown("### Dew Point, Water Content & Oil Content Estimator")

# =========================================================
# INPUT
# =========================================================

st.sidebar.header("Input Parameters")

pressure_barg = st.sidebar.number_input(
    "Operating Pressure (barg)",
    min_value=0.0,
    value=7.0,
    step=0.5
)

dew_point = st.sidebar.number_input(
    "Pressure Dew Point (°C)",
    value=-20.0,
    step=1.0
)

compressor_type = st.sidebar.selectbox(
    "Compressor Type",
    [
        "Oil Injected Screw",
        "Oil Injected + Coalescing Filter",
        "Oil Free / Oil Less"
    ]
)

# =========================================================
# CALCULATION
# =========================================================

pressure_abs = pressure_barg + 1.01325

# Magnus formula for saturation vapor pressure (kPa)
svp = 0.61094 * math.exp((17.625 * dew_point) / (dew_point + 243.04))

# Water content approximation
water_content_line = 2167 * svp / (dew_point + 273.15)

# Atmospheric equivalent
water_content_atm = water_content_line * pressure_abs

# Oil estimation
if compressor_type == "Oil Injected Screw":
    oil_content = "2 – 5 mg/m3"
    iso_class = "ISO Class 3-4"

elif compressor_type == "Oil Injected + Coalescing Filter":
    oil_content = "0.01 – 0.1 mg/m3"
    iso_class = "ISO Class 1-2"

else:
    oil_content = "<0.01 mg/m3"
    iso_class = "ISO Class 0-1"

# =========================================================
# RESULTS
# =========================================================

st.header("Calculation Results")

col1, col2 = st.columns(2)

with col1:
    st.metric("Pressure Absolute", f"{pressure_abs:.2f} barA")
    st.metric("Saturation Vapor Pressure", f"{svp:.5f} kPa")
    st.metric("Water Content @ Line Pressure", f"{water_content_line:.3f} g/m3")

with col2:
    st.metric("Water Content Atmospheric Eq.", f"{water_content_atm:.3f} mg/m3")
    st.metric("Estimated Oil Content", oil_content)
    st.metric("Typical ISO 8573-1 Class", iso_class)

# =========================================================
# RULE OF THUMB TABLE
# =========================================================

st.header("Typical Oil Content Reference")

data = {
    "Compressor Type": [
        "Oil Injected Screw",
        "Oil Injected + Coalescing Filter",
        "Oil Free / Oil Less"
    ],
    "Typical Oil Content": [
        "2 – 5 mg/m3",
        "0.01 – 0.1 mg/m3",
        "<0.01 mg/m3"
    ],
    "Typical ISO Class": [
        "Class 3-4",
        "Class 1-2",
        "Class 0-1"
    ]
}

df = pd.DataFrame(data)

st.dataframe(df, use_container_width=True)

# =========================================================
# ISO TABLE
# =========================================================

st.header("ISO 8573-1 Oil Class")

iso_table = pd.DataFrame({
    "ISO Class": ["Class 1", "Class 2", "Class 3", "Class 4"],
    "Total Oil Limit": [
        "≤0.01 mg/m3",
        "≤0.1 mg/m3",
        "≤1 mg/m3",
        "≤5 mg/m3"
    ]
})

st.table(iso_table)

# =========================================================
# CONDITION ANALYSIS
# =========================================================

st.header("Condition Analysis")

if water_content_atm > 100:
    st.error("High moisture detected → Risk of wet air / condensation.")
elif water_content_atm > 20:
    st.warning("Moderate moisture level.")
else:
    st.success("Dry compressed air condition.")

if compressor_type == "Oil Injected Screw":
    st.info("Oil injected compressor normally requires coalescing filter for instrument air.")
else:
    st.success("Oil free compressor suitable for critical clean air application.")

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")
st.caption("Created for compressed air & instrument air evaluation")
