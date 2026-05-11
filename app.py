# =========================================================
# COMPRESSED AIR SYSTEM SIMULATOR
# Compressor + Dryer + Dew Point + Oil Content
# =========================================================

import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Compressed Air System Simulator", layout="wide")

st.title("Compressed Air System Simulator")

st.markdown("""
Simulasi:
- Compressor Capacity
- Working Pressure
- Ambient Temperature
- Oil Injected vs Oil Free
- Refrigerated vs Desiccant Dryer
- Dew Point Achievement
- Water Content
- Oil Content
""")

# =========================================================
# INPUT SECTION
# =========================================================

st.sidebar.header("Input Parameters")

# Compressor Power
compressor_kw = st.sidebar.number_input(
    "Compressor Power (kW)",
    min_value=1.0,
    value=37.0,
    step=1.0
)

# Working Pressure
pressure_barg = st.sidebar.number_input(
    "Working Pressure (barg)",
    min_value=1.0,
    value=7.0,
    step=0.5
)

# Ambient Temperature
ambient_temp = st.sidebar.number_input(
    "Ambient Temperature (°C)",
    value=35.0,
    step=1.0
)

# Compressor Type
compressor_type = st.sidebar.selectbox(
    "Compressor Type",
    [
        "Oil Injected Screw",
        "Oil Free / Oil Less"
    ]
)

# Dryer Type
dryer_type = st.sidebar.selectbox(
    "Dryer Type",
    [
        "Refrigerated Dryer",
        "Desiccant Dryer"
    ]
)

# =========================================================
# COMPRESSOR ESTIMATION
# =========================================================

# Rough rule:
# 1 kW ≈ 0.12 - 0.15 m3/min
flow_m3min = compressor_kw * 0.13

# =========================================================
# DRYER PERFORMANCE
# =========================================================

if dryer_type == "Refrigerated Dryer":

    typical_pdp = 3
    achievable_pdp = 5
    dryer_desc = "Suitable for general plant air"

elif dryer_type == "Desiccant Dryer":

    typical_pdp = -40
    achievable_pdp = -70
    dryer_desc = "Suitable for instrument air / critical air"

# =========================================================
# WATER CONTENT CALCULATION
# =========================================================

pressure_abs = pressure_barg + 1.01325

# Magnus formula
svp = 0.61094 * math.exp((17.625 * typical_pdp) / (typical_pdp + 243.04))

# Water content
water_content = 2167 * svp / (typical_pdp + 273.15)

# Atmospheric equivalent
water_content_atm = water_content * pressure_abs

# =========================================================
# OIL CONTENT ESTIMATION
# =========================================================

if compressor_type == "Oil Injected Screw":

    if dryer_type == "Refrigerated Dryer":
        oil_content = "2 – 5 mg/m3"

    else:
        oil_content = "0.01 – 0.1 mg/m3"

else:
    oil_content = "<0.01 mg/m3"

# =========================================================
# OUTPUT SECTION
# =========================================================

st.header("Simulation Results")

col1, col2 = st.columns(2)

with col1:

    st.metric("Estimated Flow", f"{flow_m3min:.2f} m3/min")
    st.metric("Pressure Absolute", f"{pressure_abs:.2f} barA")
    st.metric("Typical Dew Point", f"{typical_pdp} °C")

with col2:

    st.metric("Best Achievable PDP", f"{achievable_pdp} °C")
    st.metric("Water Content", f"{water_content_atm:.2f} mg/m3")
    st.metric("Estimated Oil Content", oil_content)

# =========================================================
# SYSTEM INTERPRETATION
# =========================================================

st.header("System Interpretation")

if dryer_type == "Refrigerated Dryer":

    st.warning("""
    Refrigerated dryer typically only reaches +3°C PDP.
    
    Risk:
    - condensation in cold piping
    - not suitable for instrument air
    - not suitable for outdoor low temperature line
    """)

else:

    st.success("""
    Desiccant dryer suitable for:
    - instrument air
    - pneumatic control
    - analyzer system
    - critical process air
    """)

if compressor_type == "Oil Injected Screw":

    st.info("""
    Oil injected compressor normally requires:
    - separator
    - coalescing filter
    - activated carbon filter (critical air)
    """)

else:

    st.success("""
    Oil free compressor:
    - very low oil carry over
    - suitable for food/pharma/electronics
    """)

# =========================================================
# PERFORMANCE TABLE
# =========================================================

st.header("Typical Dryer Performance")

dryer_table = pd.DataFrame({
    "Dryer Type": [
        "Refrigerated Dryer",
        "Desiccant Dryer",
        "Heatless Desiccant",
        "Heated Desiccant"
    ],
    "Typical PDP": [
        "+3°C",
        "-40°C",
        "-40°C to -70°C",
        "-40°C to -100°C"
    ],
    "Application": [
        "General Plant Air",
        "Instrument Air",
        "Critical Instrument",
        "Ultra Dry Process"
    ]
})

st.dataframe(dryer_table, use_container_width=True)

# =========================================================
# OIL TABLE
# =========================================================

st.header("Typical Oil Content")

oil_table = pd.DataFrame({
    "System": [
        "Oil Injected Compressor",
        "Oil Injected + Coalescing Filter",
        "Oil Free Compressor"
    ],
    "Typical Oil Content": [
        "2 – 5 mg/m3",
        "0.01 – 0.1 mg/m3",
        "<0.01 mg/m3"
    ]
})

st.table(oil_table)

# =========================================================
# AMBIENT EFFECT
# =========================================================

st.header("Ambient Temperature Effect")

if ambient_temp > 40:

    st.error("""
    High ambient temperature detected.
    
    Possible impact:
    - lower dryer performance
    - higher moisture load
    - higher oil vapor carry over
    - reduced compressor efficiency
    """)

elif ambient_temp > 30:

    st.warning("""
    Moderate-high ambient temperature.
    
    Ensure:
    - proper ventilation
    - adequate aftercooler performance
    """)

else:

    st.success("Ambient temperature is acceptable.")

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")
st.caption("Compressed Air Engineering Simulator")
