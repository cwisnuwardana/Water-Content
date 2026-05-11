# =========================================================
# COMPRESSED AIR SYSTEM SIMULATOR
# WITH ACTUAL PDP INPUT
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
- ACTUAL Dew Point Performance
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
# TYPICAL PDP REFERENCE
# =========================================================

if dryer_type == "Refrigerated Dryer":

    recommended_pdp = 3
    best_pdp = 0
    dryer_desc = "General Plant Air"

else:

    recommended_pdp = -40
    best_pdp = -70
    dryer_desc = "Instrument Air / Critical Air"

# =========================================================
# ACTUAL PDP INPUT
# =========================================================

st.sidebar.markdown("### Actual Dryer Performance")

actual_pdp = st.sidebar.number_input(
    "Actual Measured PDP (°C)",
    value=float(recommended_pdp),
    step=1.0
)

# =========================================================
# FLOW ESTIMATION
# =========================================================

# Rule of thumb
flow_m3min = compressor_kw * 0.13

# =========================================================
# WATER CONTENT CALCULATION
# =========================================================

pressure_abs = pressure_barg + 1.01325

# Magnus formula
svp = 0.61094 * math.exp((17.625 * actual_pdp) / (actual_pdp + 243.04))

# Water content
water_content = 2167 * svp / (actual_pdp + 273.15)

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
# MAIN RESULTS
# =========================================================

st.header("Simulation Results")

col1, col2 = st.columns(2)

with col1:

    st.metric("Estimated Flow", f"{flow_m3min:.2f} m3/min")
    st.metric("Pressure Absolute", f"{pressure_abs:.2f} barA")
    st.metric("Actual PDP", f"{actual_pdp:.1f} °C")

with col2:

    st.metric("Water Content", f"{water_content_atm:.2f} mg/m3")
    st.metric("Estimated Oil Content", oil_content)
    st.metric("Dryer Typical Target", f"{recommended_pdp} °C")

# =========================================================
# PDP ANALYSIS
# =========================================================

st.header("Dryer Condition Analysis")

if dryer_type == "Desiccant Dryer":

    if actual_pdp <= -40:

        st.success("""
        Dryer performance GOOD.
        
        Molecular sieve / desiccant likely still healthy.
        Suitable for instrument air service.
        """)

    elif actual_pdp <= -20:

        st.warning("""
        Dryer performance degraded.
        
        Possible causes:
        - partial desiccant saturation
        - purge issue
        - switching valve leakage
        - insufficient regeneration
        """)

    elif actual_pdp > -10:

        st.error("""
        Dryer performance BAD.
        
        Possible causes:
        - damaged molecular sieve
        - saturated desiccant
        - purge failure
        - valve failure
        - heater problem
        
        Desiccant replacement likely required.
        """)

else:

    if actual_pdp <= 5:

        st.success("""
        Refrigerated dryer operating normally.
        """)

    else:

        st.warning("""
        Refrigerated dryer performance degraded.
        
        Possible causes:
        - refrigerant issue
        - condenser dirty
        - overloaded dryer
        - high ambient temperature
        """)

# =========================================================
# AMBIENT EFFECT
# =========================================================

st.header("Ambient Temperature Effect")

if ambient_temp > 40:

    st.error("""
    HIGH ambient temperature.
    
    Impact:
    - higher moisture load
    - reduced dryer efficiency
    - higher oil vapor carry over
    - compressor overheating risk
    """)

elif ambient_temp > 30:

    st.warning("""
    Moderate-high ambient temperature.
    
    Ensure:
    - proper ventilation
    - aftercooler clean
    - sufficient airflow
    """)

else:

    st.success("Ambient condition acceptable.")

# =========================================================
# REFERENCE TABLE
# =========================================================

st.header("Typical Dryer Performance Reference")

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

    "Typical Application": [
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

st.header("Typical Oil Content Reference")

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
# FOOTER
# =========================================================

st.markdown("---")
st.caption("Compressed Air Engineering Simulator")
