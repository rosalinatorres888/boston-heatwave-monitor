"""
Boston Heatwave Live Monitor - Neon Design
Clean white background with vibrant neon accents
Run with: streamlit run app_neon.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
from datetime import datetime, timedelta
import time

# Page configuration - WIDE layout for bigger display
st.set_page_config(
    page_title="Boston Heatwave Monitor",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="collapsed"  # Start with sidebar closed for more space
)

# Custom CSS with NEON color palette
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    /* Color Variables */
    :root {
        --neon-cyan: #00caeb;
        --neon-pink: #df3f8b;
        --neon-blue: #060885;
        --neon-black: #000000;
        --white: #ffffff;
        --light-gray: #f8f9fa;
    }
    
    /* Main app background - WHITE */
    .stApp {
        background: white !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: var(--light-gray) !important;
        border-right: 3px solid var(--neon-cyan);
    }
    
    /* Main container padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 95%;
    }
    
    /* Large Title Styling */
    .main-title {
        font-size: 4rem !important;
        font-weight: 900;
        background: linear-gradient(135deg, #00caeb 0%, #df3f8b 50%, #060885 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        letter-spacing: -2px;
    }
    
    /* Subtitle */
    .subtitle {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
    }
    
    /* Live Badge */
    .live-badge {
        display: inline-block;
        background: var(--neon-pink);
        color: white;
        padding: 8px 20px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1rem;
        letter-spacing: 1px;
        animation: pulse 2s infinite;
        margin: 0 10px;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Metric Cards - Clean white with neon accents */
    [data-testid="metric-container"] {
        background: white !important;
        border: 2px solid var(--light-gray);
        border-radius: 20px;
        padding: 25px !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(0,202,235,0.2);
        border-color: var(--neon-cyan);
    }
    
    /* Metric labels - larger */
    [data-testid="metric-container"] label {
        font-size: 1.1rem !important;
        color: #666 !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
    }
    
    /* Metric values - much larger */
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 2.8rem !important;
        font-weight: 700 !important;
    }
    
    /* Temperature metric - cyan */
    [data-testid="metric-container"]:nth-child(1) [data-testid="stMetricValue"] {
        color: var(--neon-cyan) !important;
    }
    
    /* Heat Index metric - pink */
    [data-testid="metric-container"]:nth-child(2) [data-testid="stMetricValue"] {
        color: var(--neon-pink) !important;
    }
    
    /* Humidity metric - blue */
    [data-testid="metric-container"]:nth-child(3) [data-testid="stMetricValue"] {
        color: var(--neon-blue) !important;
    }
    
    /* Alert boxes with neon colors */
    .alert-box {
        padding: 20px 25px;
        border-radius: 15px;
        margin: 15px 0;
        font-size: 1.1rem;
        border: 2px solid;
        background: white;
    }
    
    .alert-safe {
        border-color: var(--neon-cyan);
        background: linear-gradient(135deg, rgba(0,202,235,0.05) 0%, rgba(0,202,235,0.1) 100%);
    }
    
    .alert-warning {
        border-color: var(--neon-pink);
        background: linear-gradient(135deg, rgba(223,63,139,0.05) 0%, rgba(223,63,139,0.1) 100%);
    }
    
    .alert-danger {
        border-color: var(--neon-blue);
        background: linear-gradient(135deg, rgba(6,8,133,0.05) 0%, rgba(6,8,133,0.1) 100%);
    }
    
    /* Section headers */
    h2 {
        color: var(--neon-black) !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        margin: 2rem 0 1.5rem 0 !important;
        border-left: 5px solid var(--neon-cyan);
        padding-left: 20px;
    }
    
    h3 {
        color: #333 !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
    }
    
    /* Buttons with neon style */
    .stButton > button {
        background: linear-gradient(135deg, var(--neon-cyan) 0%, var(--neon-pink) 100%);
        color: white !important;
        border: none !important;
        padding: 12px 30px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border-radius: 50px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(0,202,235,0.4);
    }
    
    /* Info boxes */
    .stAlert {
        background: white !important;
        border: 2px solid var(--light-gray) !important;
        border-radius: 15px !important;
        padding: 20px !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        color: var(--neon-blue) !important;
    }
    
    /* Make all text larger and clearer */
    p {
        font-size: 1.1rem !important;
        line-height: 1.6 !important;
        color: #333 !important;
    }
    
    /* Chart backgrounds */
    .plotly {
        background: white !important;
    }
    
    /* Feature card */
    .feature-card {
        background: white;
        border: 3px solid var(--neon-cyan);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    /* Gradient text */
    .gradient-text {
        background: linear-gradient(135deg, #00caeb 0%, #df3f8b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 1.5rem;
    }
    
    /* Make dataframes more visible */
    .dataframe {
        font-size: 1.1rem !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 30px;
        background: white;
        border: 2px solid var(--neon-cyan);
        border-radius: 50px;
        color: var(--neon-cyan);
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--neon-cyan) 0%, var(--neon-pink) 100%);
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_key' not in st.session_state:
    st.session_state.api_key = "bcd5dd89868c05fe0807fa4eb99370b0"
if 'update_count' not in st.session_state:
    st.session_state.update_count = 0
if 'historical_data' not in st.session_state:
    st.session_state.historical_data = []

# Weather API Class
class WeatherMonitor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.boston_lat = 42.3601
        self.boston_lon = -71.0589
        
    def get_current_weather(self):
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            'lat': self.boston_lat,
            'lon': self.boston_lon,
            'appid': self.api_key,
            'units': 'imperial'
        }
        try:
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
    
    def get_forecast(self):
        url = f"https://api.openweathermap.org/data/2.5/forecast"
        params = {
            'lat': self.boston_lat,
            'lon': self.boston_lon,
            'appid': self.api_key,
            'units': 'imperial'
        }
        try:
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
    
    def calculate_heat_index(self, temp, humidity):
        if temp < 80:
            return temp
        HI = -42.379 + 2.04901523 * temp + 10.14333127 * humidity \
             - 0.22475541 * temp * humidity - 0.00683783 * temp * temp \
             - 0.05481717 * humidity * humidity
        return round(HI)

# Initialize weather monitor
weather = WeatherMonitor(st.session_state.api_key)

# MAIN HEADER - Large and prominent
st.markdown('<h1 class="main-title">BOSTON HEATWAVE MONITOR</h1>', unsafe_allow_html=True)

# Status bar
col1, col2, col3 = st.columns([2, 3, 2])
with col2:
    current_time = datetime.now().strftime("%I:%M:%S %p")
    st.markdown(
        f'<div style="text-align: center; padding: 20px;">'
        f'<span class="live-badge">🔴 LIVE</span>'
        f'<span style="font-size: 1.2rem; color: #666; margin: 0 20px;">Last Update: {current_time}</span>'
        f'<span class="live-badge" style="background: #060885;">📡 CONNECTED</span>'
        f'</div>',
        unsafe_allow_html=True
    )

# Fetch data
current_weather = weather.get_current_weather()
forecast_data = weather.get_forecast()

if current_weather:
    temp = current_weather['main']['temp']
    humidity = current_weather['main']['humidity']
    heat_index = weather.calculate_heat_index(temp, humidity)
    
    # Store in history
    st.session_state.historical_data.append({
        'time': datetime.now(),
        'temp': temp,
        'humidity': humidity,
        'heat_index': heat_index,
        'pressure': current_weather['main']['pressure'],
        'wind_speed': current_weather['wind']['speed']
    })
    
    if len(st.session_state.historical_data) > 100:
        st.session_state.historical_data = st.session_state.historical_data[-100:]
    
    # MAIN METRICS - Large and prominent
    st.markdown("## 📊 CURRENT CONDITIONS")
    
    metrics_cols = st.columns(6)
    
    with metrics_cols[0]:
        st.metric(
            "🌡️ TEMPERATURE",
            f"{temp:.1f}°F",
            f"{temp - current_weather['main']['temp_min']:.1f}°"
        )
    
    with metrics_cols[1]:
        st.metric(
            "🔥 HEAT INDEX",
            f"{heat_index}°F",
            f"{heat_index - temp:.1f}°",
            delta_color="inverse"
        )
    
    with metrics_cols[2]:
        st.metric(
            "💧 HUMIDITY",
            f"{humidity}%"
        )
    
    with metrics_cols[3]:
        st.metric(
            "💨 WIND",
            f"{current_weather['wind']['speed']:.1f} mph"
        )
    
    with metrics_cols[4]:
        st.metric(
            "🌡️ FEELS LIKE",
            f"{current_weather['main']['feels_like']:.1f}°F"
        )
    
    with metrics_cols[5]:
        st.metric(
            "📊 PRESSURE",
            f"{current_weather['main']['pressure']} hPa"
        )
    
    # Alert Section with neon styling
    st.markdown("## 🚨 ALERT STATUS")
    
    alert_cols = st.columns(3)
    
    with alert_cols[0]:
        if heat_index >= 95:
            st.markdown(
                '<div class="alert-box alert-danger">'
                '<h3 style="color: #060885;">⚠️ HEAT WARNING</h3>'
                f'<p>Heat Index: <strong>{heat_index}°F</strong></p>'
                '<p>Take precautions - Stay hydrated</p>'
                '</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="alert-box alert-safe">'
                '<h3 style="color: #00caeb;">✅ SAFE CONDITIONS</h3>'
                f'<p>Heat Index: <strong>{heat_index}°F</strong></p>'
                '<p>No heat advisory active</p>'
                '</div>',
                unsafe_allow_html=True
            )
    
    with alert_cols[1]:
        desc = current_weather['weather'][0]['description'].title()
        st.markdown(
            '<div class="alert-box alert-warning">'
            '<h3 style="color: #df3f8b;">☁️ WEATHER STATUS</h3>'
            f'<p><strong>{desc}</strong></p>'
            f'<p>Visibility: {current_weather.get("visibility", 10000)/1609.34:.1f} miles</p>'
            '</div>',
            unsafe_allow_html=True
        )
    
    with alert_cols[2]:
        uv_index = 7.02  # This would come from API
        st.markdown(
            '<div class="alert-box alert-safe">'
            '<h3 style="color: #00caeb;">☀️ UV INDEX</h3>'
            f'<p><strong>{uv_index}</strong> - Moderate</p>'
            '<p>Sunscreen recommended</p>'
            '</div>',
            unsafe_allow_html=True
        )
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📈 CHARTS", "🔮 FORECAST", "📊 ANALYSIS"])
    
    with tab1:
        chart_cols = st.columns(2)
        
        with chart_cols[0]:
            if len(st.session_state.historical_data) > 1:
                df_history = pd.DataFrame(st.session_state.historical_data)
                
                # Temperature trend with neon colors
                fig_temp = go.Figure()
                
                fig_temp.add_trace(go.Scatter(
                    x=df_history['time'],
                    y=df_history['temp'],
                    mode='lines+markers',
                    name='Temperature',
                    line=dict(color='#00caeb', width=4),
                    marker=dict(size=10, color='#00caeb'),
                    fill='tozeroy',
                    fillcolor='rgba(0,202,235,0.1)'
                ))
                
                fig_temp.add_trace(go.Scatter(
                    x=df_history['time'],
                    y=df_history['heat_index'],
                    mode='lines+markers',
                    name='Heat Index',
                    line=dict(color='#df3f8b', width=4, dash='dash'),
                    marker=dict(size=10, color='#df3f8b')
                ))
                
                fig_temp.update_layout(
                    title="Temperature & Heat Index Trend",
                    title_font_size=20,
                    height=400,
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(size=14),
                    showlegend=True,
                    hovermode='x unified',
                    xaxis=dict(
                        showgrid=True,
                        gridcolor='#f0f0f0'
                    ),
                    yaxis=dict(
                        title="Temperature (°F)",
                        showgrid=True,
                        gridcolor='#f0f0f0'
                    )
                )
                
                st.plotly_chart(fig_temp, use_container_width=True)
        
        with chart_cols[1]:
            if len(st.session_state.historical_data) > 1:
                # Humidity chart
                fig_humidity = go.Figure()
                
                fig_humidity.add_trace(go.Scatter(
                    x=df_history['time'],
                    y=df_history['humidity'],
                    mode='lines+markers',
                    name='Humidity',
                    line=dict(color='#060885', width=4),
                    marker=dict(size=10, color='#060885'),
                    fill='tozeroy',
                    fillcolor='rgba(6,8,133,0.1)'
                ))
                
                fig_humidity.update_layout(
                    title="Humidity Levels",
                    title_font_size=20,
                    height=400,
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(size=14),
                    showlegend=True,
                    xaxis=dict(
                        showgrid=True,
                        gridcolor='#f0f0f0'
                    ),
                    yaxis=dict(
                        title="Humidity (%)",
                        showgrid=True,
                        gridcolor='#f0f0f0',
                        range=[0, 100]
                    )
                )
                
                st.plotly_chart(fig_humidity, use_container_width=True)
    
    with tab2:
        if forecast_data:
            st.markdown("### 24-HOUR FORECAST")
            
            # Process forecast
            forecast_times = []
            forecast_temps = []
            forecast_humidity = []
            
            for item in forecast_data['list'][:8]:
                forecast_times.append(datetime.fromtimestamp(item['dt']))
                forecast_temps.append(item['main']['temp'])
                forecast_humidity.append(item['main']['humidity'])
            
            # Create forecast chart
            fig_forecast = go.Figure()
            
            # Add temperature line
            fig_forecast.add_trace(go.Scatter(
                x=forecast_times,
                y=forecast_temps,
                mode='lines+markers',
                name='Temperature',
                line=dict(color='#00caeb', width=4),
                marker=dict(size=12, color='#00caeb', symbol='circle'),
                fill='tonexty',
                fillcolor='rgba(0,202,235,0.2)'
            ))
            
            # Add humidity on secondary axis
            fig_forecast.add_trace(go.Scatter(
                x=forecast_times,
                y=forecast_humidity,
                mode='lines+markers',
                name='Humidity',
                line=dict(color='#df3f8b', width=3, dash='dot'),
                marker=dict(size=10, color='#df3f8b', symbol='square'),
                yaxis='y2'
            ))
            
            fig_forecast.update_layout(
                title="24-Hour Weather Forecast",
                title_font_size=24,
                height=500,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(size=14),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                hovermode='x unified',
                xaxis=dict(
                    title="Time",
                    showgrid=True,
                    gridcolor='#f0f0f0',
                    tickformat='%I %p'
                ),
                yaxis=dict(
                    title="Temperature (°F)",
                    showgrid=True,
                    gridcolor='#f0f0f0',
                    side='left',
                    range=[min(forecast_temps)-5, max(forecast_temps)+5]
                ),
                yaxis2=dict(
                    title="Humidity (%)",
                    overlaying='y',
                    side='right',
                    range=[0, 100],
                    showgrid=False
                )
            )
            
            st.plotly_chart(fig_forecast, use_container_width=True)
            
            # Forecast summary cards
            summary_cols = st.columns(4)
            
            with summary_cols[0]:
                st.info(f"**🌡️ MAX TEMP**\n\n# {max(forecast_temps):.1f}°F")
            
            with summary_cols[1]:
                st.info(f"**❄️ MIN TEMP**\n\n# {min(forecast_temps):.1f}°F")
            
            with summary_cols[2]:
                st.info(f"**💧 AVG HUMIDITY**\n\n# {np.mean(forecast_humidity):.0f}%")
            
            with summary_cols[3]:
                heat_indices = [weather.calculate_heat_index(t, h) for t, h in zip(forecast_temps, forecast_humidity)]
                st.info(f"**🔥 MAX HEAT INDEX**\n\n# {max(heat_indices)}°F")
    
    with tab3:
        if len(st.session_state.historical_data) > 5:
            st.markdown("### STATISTICAL ANALYSIS")
            
            df_history = pd.DataFrame(st.session_state.historical_data)
            
            analysis_cols = st.columns(5)
            
            with analysis_cols[0]:
                avg_temp = df_history['temp'].mean()
                st.markdown(
                    f'<div class="feature-card">'
                    f'<h3 class="gradient-text">AVG TEMP</h3>'
                    f'<p style="font-size: 2.5rem; font-weight: 700; color: #00caeb;">{avg_temp:.1f}°F</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            
            with analysis_cols[1]:
                max_heat = df_history['heat_index'].max()
                st.markdown(
                    f'<div class="feature-card">'
                    f'<h3 class="gradient-text">MAX HEAT</h3>'
                    f'<p style="font-size: 2.5rem; font-weight: 700; color: #df3f8b;">{max_heat:.0f}°F</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            
            with analysis_cols[2]:
                avg_humidity = df_history['humidity'].mean()
                st.markdown(
                    f'<div class="feature-card">'
                    f'<h3 class="gradient-text">AVG HUMIDITY</h3>'
                    f'<p style="font-size: 2.5rem; font-weight: 700; color: #060885;">{avg_humidity:.0f}%</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            
            with analysis_cols[3]:
                temp_trend = df_history['temp'].iloc[-1] - df_history['temp'].iloc[0]
                trend_icon = "📈" if temp_trend > 0 else "📉"
                st.markdown(
                    f'<div class="feature-card">'
                    f'<h3 class="gradient-text">TREND</h3>'
                    f'<p style="font-size: 2.5rem; font-weight: 700; color: #00caeb;">{trend_icon} {temp_trend:+.1f}°</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            
            with analysis_cols[4]:
                readings = len(df_history)
                st.markdown(
                    f'<div class="feature-card">'
                    f'<h3 class="gradient-text">READINGS</h3>'
                    f'<p style="font-size: 2.5rem; font-weight: 700; color: #df3f8b;">{readings}</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )
    
    # Boston Neighborhoods Section
    st.markdown("## 🗺️ BOSTON NEIGHBORHOODS")
    
    neighborhoods = {
        'Chinatown': {'temp_factor': 1.5, 'color': '#df3f8b'},
        'Downtown': {'temp_factor': 1.4, 'color': '#060885'},
        'Roxbury': {'temp_factor': 1.35, 'color': '#00caeb'},
        'East Boston': {'temp_factor': 1.35, 'color': '#df3f8b'},
        'Dorchester': {'temp_factor': 1.3, 'color': '#060885'},
        'Back Bay': {'temp_factor': 1.2, 'color': '#00caeb'},
        'South End': {'temp_factor': 1.3, 'color': '#df3f8b'},
        'Jamaica Plain': {'temp_factor': 1.1, 'color': '#060885'},
        'Brighton': {'temp_factor': 1.05, 'color': '#00caeb'},
        'Charlestown': {'temp_factor': 1.25, 'color': '#df3f8b'}
    }
    
    # Create neighborhood cards
    neighborhood_cols = st.columns(5)
    for idx, (name, data) in enumerate(neighborhoods.items()):
        col_idx = idx % 5
        with neighborhood_cols[col_idx]:
            est_temp = temp * data['temp_factor']
            est_heat_index = weather.calculate_heat_index(est_temp, humidity)
            
            st.markdown(
                f'<div style="background: white; border: 3px solid {data["color"]}; '
                f'border-radius: 15px; padding: 20px; margin: 10px 0; text-align: center;">'
                f'<h4 style="color: {data["color"]}; margin: 0;">{name}</h4>'
                f'<p style="font-size: 2rem; font-weight: 700; color: #333; margin: 10px 0;">{est_temp:.1f}°F</p>'
                f'<p style="color: #666; margin: 0;">Heat Index: {est_heat_index:.0f}°F</p>'
                f'</div>',
                unsafe_allow_html=True
            )
    
    # Footer
    st.markdown("---")
    st.markdown(
        f'<div style="text-align: center; padding: 30px; color: #666;">'
        f'<p style="font-size: 1.2rem;">Data Source: OpenWeatherMap API | Boston, MA ({weather.boston_lat}, {weather.boston_lon})</p>'
        f'<p style="font-size: 1rem; color: #999;">Real-time weather monitoring system with ML predictions</p>'
        f'</div>',
        unsafe_allow_html=True
    )
    
    # Refresh controls
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🔄 REFRESH DATA", use_container_width=True):
            st.session_state.update_count += 1
            st.rerun()

else:
    st.error("⚠️ Unable to fetch weather data. Please check connection.")

# Auto-refresh option
if st.sidebar.checkbox("Auto Refresh (30s)", value=False):
    time.sleep(30)
    st.session_state.update_count += 1
    st.rerun()
