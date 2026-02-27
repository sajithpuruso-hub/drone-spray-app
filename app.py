import streamlit as st
import numpy as np
import pandas as pd

# 1. Mobile-First Page Config
st.set_page_config(
    page_title="Drone Swath Calc",
    layout="centered", # Better for vertical mobile screens
    initial_sidebar_state="collapsed"
)

# Custom CSS to make sliders easier to touch on mobile
st.markdown("""
    <style>
    .stSlider { margin-bottom: 20px; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚁 Spray Swath Pro")
st.subheader("Field Coverage Estimator")

# 2. Main Input Section (Vertical Stack)
with st.container():
    st.write("### ⚙️ Flight Settings")
    
    altitude = st.slider("Altitude (m)", 1.0, 10.0, 3.0, step=0.5)
    speed = st.slider("Ground Speed (m/s)", 1.0, 15.0, 5.0, step=0.5)
    spray_angle = st.select_slider(
        "Nozzle Angle (°)", 
        options=[40, 60, 80, 110, 120, 140], 
        value=110
    )

# 3. Logic & Physics
# Geometric Swath Calculation
angle_rad = np.radians(spray_angle)
theoretical_swath = 2 * altitude * np.tan(angle_rad / 2)

# Speed Compression Factor (Simulating aerodynamic drift/narrowing)
# At higher speeds, the spray column is slightly compressed by air resistance
speed_penalty = 1 - (speed * 0.015) 
effective_swath = theoretical_swath * speed_penalty
coverage_per_min = (effective_swath * speed * 60) / 10000 # Hectares per min

# 4. Mobile Optimized Metrics
st.write("### 📊 Live Results")
m1, m2 = st.columns(2)
m1.metric("Swath Width", f"{effective_swath:.1f} m")
m2.metric("Ha / Minute", f"{coverage_per_min:.2f}")

# 5. Visualizer (Using native Area Chart for mobile speed)
st.write("### 📐 Spray Profile")
# Create a simple "V" shape dataset to visualize the spray cone
chart_data = pd.DataFrame({
    'Width (m)': [-effective_swath/2, 0, effective_swath/2],
    'Spray Intensity': [0, altitude, 0]
})
st.area_chart(chart_data.set_index('Width (m)'), color="#0077ff")

# 6. Safety Warning
if altitude > 5.0:
    st.warning("⚠️ High Altitude: Drift risk increases significantly. Check wind speed!")
if speed > 10.0:
    st.error("🚨 High Speed: Uniformity may be compromised by wake turbulence.")

st.caption("Calculation assumes standard nozzle pressure and zero crosswind.")
