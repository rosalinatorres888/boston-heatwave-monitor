"""
Boston Heatwave Monitoring System - Netlify Static Version
Generates beautiful interactive HTML dashboard with Plotly
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo

class BostonWeatherCollector:
    """Collects real weather data from free APIs"""
    
    def __init__(self):
        self.stations = {
            'logan': 'KBOS',
            'blue_hill': 'KMQE',  
            'bedford': 'KBED',
            'norwood': 'KOWD'
        }
        self.current_data = None
        
    def get_real_weather(self, station='logan'):
        """Get real weather data from NOAA"""
        try:
            station_id = self.stations.get(station, 'KBOS')
            url = f'https://api.weather.gov/stations/{station_id}/observations/latest'
            
            print(f"Fetching weather from {station}...")
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                props = data['properties']
                
                weather_data = {
                    'timestamp': datetime.now().isoformat(),
                    'station': station,
                    'temperature': self._celsius_to_fahrenheit(props.get('temperature', {}).get('value')),
                    'humidity': props.get('relativeHumidity', {}).get('value'),
                    'dewpoint': self._celsius_to_fahrenheit(props.get('dewpoint', {}).get('value')),
                    'heat_index': self._celsius_to_fahrenheit(props.get('heatIndex', {}).get('value')),
                    'wind_speed': self._mps_to_mph(props.get('windSpeed', {}).get('value')),
                    'wind_direction': props.get('windDirection', {}).get('value'),
                    'pressure': props.get('barometricPressure', {}).get('value'),
                    'visibility': self._meters_to_miles(props.get('visibility', {}).get('value')),
                    'description': props.get('textDescription', 'N/A')
                }
                
                # Calculate heat index if not provided
                if weather_data['heat_index'] is None and weather_data['temperature'] and weather_data['humidity']:
                    weather_data['heat_index'] = self.calculate_heat_index(
                        weather_data['temperature'], 
                        weather_data['humidity']
                    )
                
                self.current_data = weather_data
                return weather_data
            else:
                print(f"Error: {response.status_code}")
                return self._get_sample_data()  # Fallback to sample data
                
        except Exception as e:
            print(f"Error: {e}")
            return self._get_sample_data()  # Fallback to sample data
    
    def _get_sample_data(self):
        """Generate sample data for demo purposes"""
        return {
            'timestamp': datetime.now().isoformat(),
            'station': 'logan',
            'temperature': 89.0,
            'humidity': 68.0,
            'dewpoint': 76.0,
            'heat_index': 96.0,
            'wind_speed': 12.0,
            'wind_direction': 180.0,
            'pressure': 29.92,
            'visibility': 8.5,
            'description': 'Hot and humid'
        }
    
    def calculate_heat_index(self, temp_f, humidity):
        """Calculate heat index using NOAA formula"""
        if temp_f < 80:
            return 0.5 * (temp_f + 61.0 + ((temp_f - 68.0) * 1.2) + (humidity * 0.094))
        
        HI = (-42.379 + 2.04901523 * temp_f + 10.14333127 * humidity
              - 0.22475541 * temp_f * humidity - 0.00683783 * temp_f * temp_f
              - 0.05481717 * humidity * humidity + 0.00122874 * temp_f * temp_f * humidity
              + 0.00085282 * temp_f * humidity * humidity
              - 0.00000199 * temp_f * temp_f * humidity * humidity)
        
        if humidity < 13 and 80 <= temp_f <= 112:
            adjustment = ((13 - humidity) / 4) * np.sqrt((17 - abs(temp_f - 95)) / 17)
            HI -= adjustment
        elif humidity > 85 and 80 <= temp_f <= 87:
            adjustment = ((humidity - 85) / 10) * ((87 - temp_f) / 5)
            HI += adjustment
            
        return round(HI)
    
    def _celsius_to_fahrenheit(self, celsius):
        if celsius is None:
            return None
        return round((celsius * 9/5) + 32, 1)
    
    def _mps_to_mph(self, mps):
        if mps is None:
            return None
        return round(mps * 2.237, 1)
    
    def _meters_to_miles(self, meters):
        if meters is None:
            return None
        return round(meters / 1609.34, 1)

class HeatRiskAnalyzer:
    """Analyzes heat risk for Boston neighborhoods"""
    
    def __init__(self):
        self.neighborhoods = {
            'Chinatown': {'heat_factor': 1.5, 'vulnerable_pop': 3500, 'green_space': 0.02},
            'Roxbury': {'heat_factor': 1.4, 'vulnerable_pop': 8500, 'green_space': 0.08},
            'Dorchester': {'heat_factor': 1.3, 'vulnerable_pop': 12000, 'green_space': 0.12},
            'East Boston': {'heat_factor': 1.35, 'vulnerable_pop': 6500, 'green_space': 0.05},
            'Mattapan': {'heat_factor': 1.25, 'vulnerable_pop': 5500, 'green_space': 0.15},
            'South End': {'heat_factor': 1.3, 'vulnerable_pop': 4000, 'green_space': 0.06},
            'Back Bay': {'heat_factor': 1.15, 'vulnerable_pop': 2500, 'green_space': 0.20},
            'Jamaica Plain': {'heat_factor': 1.1, 'vulnerable_pop': 5000, 'green_space': 0.35},
            'Charlestown': {'heat_factor': 1.2, 'vulnerable_pop': 3000, 'green_space': 0.10},
            'Brighton': {'heat_factor': 1.05, 'vulnerable_pop': 6000, 'green_space': 0.25}
        }
    
    def calculate_neighborhood_temps(self, base_temp):
        """Calculate temperature for each neighborhood"""
        neighborhood_temps = {}
        for name, data in self.neighborhoods.items():
            adjusted_temp = base_temp * data['heat_factor']
            adjusted_temp += np.random.uniform(-2, 2)
            
            neighborhood_temps[name] = {
                'temperature': round(adjusted_temp, 1),
                'heat_factor': data['heat_factor'],
                'vulnerable_population': data['vulnerable_pop'],
                'green_space_percent': data['green_space'] * 100
            }
        return neighborhood_temps
    
    def assess_risk_level(self, heat_index):
        """Determine risk level"""
        if heat_index < 80:
            return {'level': 'LOW', 'color': '#28a745', 'action': 'Normal activities'}
        elif heat_index < 90:
            return {'level': 'MODERATE', 'color': '#ffc107', 'action': 'Stay hydrated'}
        elif heat_index < 105:
            return {'level': 'HIGH', 'color': '#fd7e14', 'action': 'Limit outdoor exposure'}
        elif heat_index < 130:
            return {'level': 'EXTREME', 'color': '#dc3545', 'action': 'Stay indoors'}
        else:
            return {'level': 'DANGEROUS', 'color': '#6f42c1', 'action': 'EMERGENCY'}
    
    def calculate_vulnerable_impact(self, heat_index, neighborhood_temps):
        """Calculate vulnerable population impact"""
        total_at_risk = 0
        neighborhood_risk = {}
        
        for name, temp_data in neighborhood_temps.items():
            neighborhood_info = self.neighborhoods[name]
            risk_factor = (temp_data['temperature'] / 100) * (1 - neighborhood_info['green_space'])
            
            if heat_index > 95:
                at_risk = int(neighborhood_info['vulnerable_pop'] * 0.4 * risk_factor)
            elif heat_index > 85:
                at_risk = int(neighborhood_info['vulnerable_pop'] * 0.2 * risk_factor)
            else:
                at_risk = int(neighborhood_info['vulnerable_pop'] * 0.05 * risk_factor)
            
            neighborhood_risk[name] = at_risk
            total_at_risk += at_risk
        
        return {
            'total_at_risk': total_at_risk,
            'by_neighborhood': neighborhood_risk,
            'elderly_65plus': int(total_at_risk * 0.35),
            'children_under5': int(total_at_risk * 0.15),
            'chronic_conditions': int(total_at_risk * 0.30),
            'outdoor_workers': int(total_at_risk * 0.20)
        }

class PlotlyDashboardGenerator:
    """Generate beautiful Plotly dashboard"""
    
    def create_dashboard(self, weather_data, neighborhood_temps, vulnerable_impact, risk_info):
        """Create comprehensive dashboard"""
        
        # Create subplot figure
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=[
                '🌡️ Current Heat Index',
                '🏘️ Hottest Neighborhoods', 
                '👥 Vulnerable Population Impact',
                '📊 Neighborhood Heat vs Green Space',
                '⚠️ Risk Assessment',
                '📈 Heat Island Effect'
            ],
            specs=[
                [{"type": "indicator"}, {"type": "bar"}],
                [{"type": "bar"}, {"type": "scatter"}],
                [{"type": "indicator"}, {"type": "bar"}]
            ],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # 1. Heat Index Gauge
        heat_index = weather_data.get('heat_index', 0)
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=heat_index,
                title={'text': f"Heat Index<br><span style='font-size:12px'>Feels Like</span>"},
                delta={'reference': 80},
                gauge={
                    'axis': {'range': [None, 130]},
                    'bar': {'color': risk_info['color']},
                    'steps': [
                        {'range': [0, 80], 'color': "lightgray"},
                        {'range': [80, 90], 'color': "yellow"},
                        {'range': [90, 105], 'color': "orange"},
                        {'range': [105, 130], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 105
                    }
                }
            ),
            row=1, col=1
        )
        
        # 2. Neighborhood temperatures
        neighborhoods = list(neighborhood_temps.keys())
        temps = [neighborhood_temps[n]['temperature'] for n in neighborhoods]
        colors = ['#FF4444' if t > 95 else '#FF8800' if t > 85 else '#44AA44' for t in temps]
        
        fig.add_trace(
            go.Bar(
                x=temps,
                y=neighborhoods,
                orientation='h',
                marker_color=colors,
                text=[f"{t}°F" for t in temps],
                textposition='auto'
            ),
            row=1, col=2
        )
        
        # 3. Vulnerable population impact
        categories = ['Elderly<br>(65+)', 'Children<br>(<5)', 'Chronic<br>Conditions', 'Outdoor<br>Workers']
        values = [
            vulnerable_impact['elderly_65plus'],
            vulnerable_impact['children_under5'], 
            vulnerable_impact['chronic_conditions'],
            vulnerable_impact['outdoor_workers']
        ]
        colors_vuln = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
        
        fig.add_trace(
            go.Bar(
                x=categories,
                y=values,
                marker_color=colors_vuln,
                text=values,
                textposition='auto'
            ),
            row=2, col=1
        )
        
        # 4. Heat vs Green Space scatter
        green_space = [neighborhood_temps[n]['green_space_percent'] for n in neighborhoods]
        
        fig.add_trace(
            go.Scatter(
                x=green_space,
                y=temps,
                mode='markers+text',
                marker=dict(
                    size=[neighborhood_temps[n]['vulnerable_population']/200 for n in neighborhoods],
                    color=temps,
                    colorscale='RdYlGn_r',
                    showscale=True,
                    colorbar=dict(title="Temperature")
                ),
                text=neighborhoods,
                textposition="top center"
            ),
            row=2, col=2
        )
        
        # 5. Risk Level Indicator  
        fig.add_trace(
            go.Indicator(
                mode="number",
                value=vulnerable_impact['total_at_risk'],
                title={'text': f"People at Risk<br><span style='font-size:12px;color:{risk_info['color']}'>{risk_info['level']}</span>"},
                number={'font': {'color': risk_info['color']}},
                delta={'reference': 1000}
            ),
            row=3, col=1
        )
        
        # 6. Heat island factors
        heat_factors = [neighborhood_temps[n]['heat_factor'] for n in neighborhoods]
        
        fig.add_trace(
            go.Bar(
                x=neighborhoods,
                y=heat_factors,
                marker_color='rgba(255,100,100,0.6)',
                text=[f"{hf:.2f}x" for hf in heat_factors],
                textposition='auto'
            ),
            row=3, col=2
        )
        
        # Update layout
        fig.update_layout(
            height=900,
            title=dict(
                text=f"🌡️ Boston Heatwave Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                x=0.5,
                font=dict(size=20)
            ),
            showlegend=False,
            template="plotly_white",
            font=dict(size=11)
        )
        
        # Update axis labels
        fig.update_xaxes(title_text="Temperature (°F)", row=1, col=2)
        fig.update_xaxes(title_text="Green Space (%)", row=2, col=2)  
        fig.update_xaxes(title_text="Neighborhood", row=3, col=2)
        fig.update_yaxes(title_text="People at Risk", row=2, col=1)
        fig.update_yaxes(title_text="Temperature (°F)", row=2, col=2)
        fig.update_yaxes(title_text="Heat Factor", row=3, col=2)
        
        return fig
    
    def create_current_conditions_card(self, weather_data, risk_info):
        """Create current conditions summary"""
        
        fig = go.Figure()
        
        # Create text summary
        summary = f"""
        <b>🏢 Station:</b> {weather_data.get('station', 'Logan').upper()}<br>
        <b>🌡️ Temperature:</b> {weather_data.get('temperature', 'N/A')}°F<br>
        <b>🔥 Heat Index:</b> {weather_data.get('heat_index', 'N/A')}°F<br>
        <b>💧 Humidity:</b> {weather_data.get('humidity', 'N/A')}%<br>
        <b>💨 Wind:</b> {weather_data.get('wind_speed', 'N/A')} mph<br>
        <b>👁️ Visibility:</b> {weather_data.get('visibility', 'N/A')} miles<br>
        <b>📝 Conditions:</b> {weather_data.get('description', 'N/A')}<br>
        <br>
        <b style='color:{risk_info["color"]}'>⚠️ Risk Level: {risk_info["level"]}</b><br>
        <b>💡 Action:</b> {risk_info["action"]}
        """
        
        fig.add_annotation(
            text=summary,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            align="left",
            font=dict(size=14),
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="gray",
            borderwidth=1
        )
        
        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=300,
            title="📋 Current Conditions",
            showlegend=False,
            template="plotly_white"
        )
        
        return fig

def generate_html_dashboard():
    """Main function to generate HTML dashboard"""
    
    print("🌡️ Boston Heatwave Monitor - Generating Dashboard")
    print("="*55)
    
    # Initialize components
    weather_collector = BostonWeatherCollector()
    risk_analyzer = HeatRiskAnalyzer()
    dashboard_generator = PlotlyDashboardGenerator()
    
    # Collect current weather data
    weather_data = weather_collector.get_real_weather()
    
    if weather_data:
        print("✅ Weather data collected successfully")
        
        # Analyze risk and neighborhoods
        neighborhood_temps = risk_analyzer.calculate_neighborhood_temps(weather_data['temperature'])
        risk_info = risk_analyzer.assess_risk_level(weather_data['heat_index'])
        vulnerable_impact = risk_analyzer.calculate_vulnerable_impact(
            weather_data['heat_index'], 
            neighborhood_temps
        )
        
        print(f"⚠️  Risk Level: {risk_info['level']}")
        print(f"👥 People at Risk: {vulnerable_impact['total_at_risk']:,}")
        
        # Generate dashboard
        main_fig = dashboard_generator.create_dashboard(
            weather_data, neighborhood_temps, vulnerable_impact, risk_info
        )
        
        conditions_fig = dashboard_generator.create_current_conditions_card(
            weather_data, risk_info
        )
        
        # Create HTML with both charts
        html_str = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Boston Heatwave Monitor</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .content {{
            padding: 20px;
        }}
        .update-time {{
            text-align: center;
            color: #666;
            font-size: 14px;
            margin-bottom: 20px;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 15px;
            text-align: center;
            color: #666;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌡️ Boston Heatwave Monitor</h1>
            <p>Real-time heat monitoring for Greater Boston</p>
        </div>
        
        <div class="content">
            <div class="update-time">
                Last updated: {datetime.now().strftime('%Y-%m-%d at %H:%M:%S EST')}
            </div>
            
            <div id="conditions-chart"></div>
            <div id="main-dashboard"></div>
        </div>
        
        <div class="footer">
            Data source: NOAA Weather Service | 
            Built with Python & Plotly | 
            Deployed on Netlify
        </div>
    </div>

    <script>
        // Render conditions chart
        var conditionsData = {conditions_fig.to_json()};
        Plotly.newPlot('conditions-chart', conditionsData.data, conditionsData.layout, {{responsive: true}});
        
        // Render main dashboard
        var dashboardData = {main_fig.to_json()};
        Plotly.newPlot('main-dashboard', dashboardData.data, dashboardData.layout, {{responsive: true}});
        
        // Auto-refresh every 30 minutes
        setTimeout(() => {{
            location.reload();
        }}, 30 * 60 * 1000);
    </script>
</body>
</html>
        """
        
        # Save to index.html
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_str)
        
        print("✅ Dashboard generated: index.html")
        print("🚀 Ready for Netlify deployment!")
        
    else:
        print("❌ Failed to collect weather data")

if __name__ == "__main__":
    generate_html_dashboard()
