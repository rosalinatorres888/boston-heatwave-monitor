"""
Boston Heatwave Monitoring System - Python Version
A complete step-by-step implementation for learning
"""

# STEP 1: Install Required Libraries
# Run this in your terminal:
# pip install requests pandas numpy matplotlib seaborn plotly streamlit scikit-learn

# STEP 2: Import Libraries
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import time
import warnings
warnings.filterwarnings('ignore')

# For visualization (we'll use these later)
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px

# For ML (we'll use these in Step 8)
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# =============================================================================
# STEP 3: Create the Basic Weather Data Collector
# =============================================================================

class BostonWeatherCollector:
    """Collects real weather data from free APIs"""
    
    def __init__(self):
        """Initialize the weather collector"""
        # NOAA weather stations in Boston area
        self.stations = {
            'logan': 'KBOS',      # Logan Airport
            'blue_hill': 'KMQE',  # Blue Hill Observatory  
            'bedford': 'KBED',    # Hanscom Field
            'norwood': 'KOWD'     # Norwood Memorial
        }
        
        # Store collected data
        self.current_data = None
        self.historical_data = []
        
    def get_real_weather(self, station='logan'):
        """
        Get real weather data from NOAA (FREE, no API key needed!)
        This is REAL data from Logan Airport
        """
        try:
            # Build the URL for NOAA API
            station_id = self.stations.get(station, 'KBOS')
            url = f'https://api.weather.gov/stations/{station_id}/observations/latest'
            
            print(f"Fetching real weather from {station}...")
            
            # Make the request
            response = requests.get(url)
            
            # Check if successful
            if response.status_code == 200:
                data = response.json()
                
                # Extract the weather properties
                props = data['properties']
                
                # Convert Celsius to Fahrenheit and extract data
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
                print(f"✅ Successfully fetched real weather data!")
                return weather_data
                
            else:
                print(f"❌ Error: Received status code {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error fetching weather: {e}")
            return None
    
    def calculate_heat_index(self, temp_f, humidity):
        """
        Calculate heat index using the official NOAA formula
        This is the REAL formula used by the National Weather Service
        """
        # Simple formula for lower temperatures
        if temp_f < 80:
            return 0.5 * (temp_f + 61.0 + ((temp_f - 68.0) * 1.2) + (humidity * 0.094))
        
        # Full regression equation for higher temperatures
        HI = (-42.379 + 2.04901523 * temp_f + 10.14333127 * humidity
              - 0.22475541 * temp_f * humidity - 0.00683783 * temp_f * temp_f
              - 0.05481717 * humidity * humidity + 0.00122874 * temp_f * temp_f * humidity
              + 0.00085282 * temp_f * humidity * humidity
              - 0.00000199 * temp_f * temp_f * humidity * humidity)
        
        # Adjustments
        if humidity < 13 and 80 <= temp_f <= 112:
            adjustment = ((13 - humidity) / 4) * np.sqrt((17 - abs(temp_f - 95)) / 17)
            HI -= adjustment
        elif humidity > 85 and 80 <= temp_f <= 87:
            adjustment = ((humidity - 85) / 10) * ((87 - temp_f) / 5)
            HI += adjustment
            
        return round(HI)
    
    def _celsius_to_fahrenheit(self, celsius):
        """Convert Celsius to Fahrenheit"""
        if celsius is None:
            return None
        return round((celsius * 9/5) + 32, 1)
    
    def _mps_to_mph(self, mps):
        """Convert meters per second to miles per hour"""
        if mps is None:
            return None
        return round(mps * 2.237, 1)
    
    def _meters_to_miles(self, meters):
        """Convert meters to miles"""
        if meters is None:
            return None
        return round(meters / 1609.34, 1)
    
    def display_current_weather(self):
        """Display the current weather in a nice format"""
        if not self.current_data:
            print("No weather data available. Run get_real_weather() first!")
            return
            
        print("\n" + "="*50)
        print("🌡️  CURRENT BOSTON WEATHER (REAL DATA)")
        print("="*50)
        print(f"📍 Station: {self.current_data['station'].upper()}")
        print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📝 Conditions: {self.current_data['description']}")
        print("-"*50)
        print(f"🌡️  Temperature: {self.current_data['temperature']}°F")
        print(f"🔥 Heat Index: {self.current_data['heat_index']}°F")
        print(f"💧 Humidity: {self.current_data['humidity']}%")
        print(f"💨 Wind: {self.current_data['wind_speed']} mph")
        print(f"👁️  Visibility: {self.current_data['visibility']} miles")
        print("="*50)

# =============================================================================
# STEP 4: Create the Heat Risk Analyzer
# =============================================================================

class HeatRiskAnalyzer:
    """Analyzes heat risk for different Boston neighborhoods"""
    
    def __init__(self):
        """Initialize with Boston neighborhood data"""
        # Real Boston neighborhood heat island factors
        # Based on actual research data
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
        
        # Boston cooling centers (real locations)
        self.cooling_centers = [
            {'name': 'BCYF Tobin', 'address': '1481 Tremont St, Roxbury', 'capacity': 150},
            {'name': 'BCYF Perkins', 'address': '155 Talbot Ave, Dorchester', 'capacity': 100},
            {'name': 'BCYF Paris Street', 'address': '112 Paris St, East Boston', 'capacity': 80},
            {'name': 'BCYF Quincy', 'address': '885 Washington St, Chinatown', 'capacity': 120},
            {'name': 'Boston Public Library', 'address': '700 Boylston St, Back Bay', 'capacity': 500},
        ]
    
    def calculate_neighborhood_temps(self, base_temp):
        """Calculate temperature for each neighborhood based on heat island effect"""
        neighborhood_temps = {}
        
        for name, data in self.neighborhoods.items():
            # Apply heat island factor
            adjusted_temp = base_temp * data['heat_factor']
            
            # Add some random variation (±2 degrees)
            adjusted_temp += np.random.uniform(-2, 2)
            
            neighborhood_temps[name] = {
                'temperature': round(adjusted_temp, 1),
                'heat_factor': data['heat_factor'],
                'vulnerable_population': data['vulnerable_pop'],
                'green_space_percent': data['green_space'] * 100
            }
            
        return neighborhood_temps
    
    def assess_risk_level(self, heat_index):
        """Determine risk level based on heat index"""
        if heat_index < 80:
            return {'level': 'LOW', 'color': 'green', 'action': 'Normal activities'}
        elif heat_index < 90:
            return {'level': 'MODERATE', 'color': 'yellow', 'action': 'Stay hydrated'}
        elif heat_index < 105:
            return {'level': 'HIGH', 'color': 'orange', 'action': 'Limit outdoor exposure'}
        elif heat_index < 130:
            return {'level': 'EXTREME', 'color': 'red', 'action': 'Stay indoors, cooling centers open'}
        else:
            return {'level': 'DANGEROUS', 'color': 'purple', 'action': 'EMERGENCY - Seek immediate cooling'}
    
    def calculate_vulnerable_impact(self, heat_index, neighborhood_temps):
        """Calculate impact on vulnerable populations"""
        total_at_risk = 0
        neighborhood_risk = {}
        
        for name, temp_data in neighborhood_temps.items():
            neighborhood_info = self.neighborhoods[name]
            
            # Risk increases with temperature and decreases with green space
            risk_factor = (temp_data['temperature'] / 100) * (1 - neighborhood_info['green_space'])
            
            # More people at risk when heat index is higher
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
    
    def generate_alerts(self, weather_data, neighborhood_temps):
        """Generate health and safety alerts based on conditions"""
        alerts = []
        heat_index = weather_data.get('heat_index', 0)
        
        # Heat index alerts
        if heat_index >= 105:
            alerts.append({
                'type': 'EXTREME_HEAT_WARNING',
                'priority': 'CRITICAL',
                'message': f'Extreme heat danger! Heat index: {heat_index}°F',
                'action': 'All cooling centers open. Check on elderly neighbors.'
            })
        elif heat_index >= 95:
            alerts.append({
                'type': 'HEAT_ADVISORY',
                'priority': 'HIGH',
                'message': f'Heat advisory in effect. Heat index: {heat_index}°F',
                'action': 'Limit outdoor activities between 10 AM - 6 PM'
            })
        
        # Neighborhood-specific alerts
        for name, data in neighborhood_temps.items():
            if data['temperature'] > 95:
                alerts.append({
                    'type': 'NEIGHBORHOOD_ALERT',
                    'priority': 'MEDIUM',
                    'message': f'{name}: Temperature {data["temperature"]}°F',
                    'action': f'Cooling center available at nearest BCYF'
                })
        
        # Night heat alert (if it's evening/night and still hot)
        current_hour = datetime.now().hour
        if (current_hour >= 20 or current_hour <= 6) and weather_data.get('temperature', 0) > 75:
            alerts.append({
                'type': 'NIGHT_HEAT_ALERT',
                'priority': 'MEDIUM',
                'message': 'Elevated nighttime temperatures preventing cooling',
                'action': 'Use fans, take cool showers, stay hydrated'
            })
        
        return alerts

# =============================================================================
# STEP 5: Create Data Storage and Historical Analysis
# =============================================================================

class DataManager:
    """Manages data storage and historical analysis"""
    
    def __init__(self, filename='boston_weather_data.csv'):
        """Initialize data manager"""
        self.filename = filename
        self.df = None
        
    def save_weather_data(self, weather_data):
        """Save weather data to CSV file"""
        # Convert to DataFrame
        new_row = pd.DataFrame([weather_data])
        
        try:
            # Try to read existing file
            self.df = pd.read_csv(self.filename)
            self.df = pd.concat([self.df, new_row], ignore_index=True)
        except FileNotFoundError:
            # Create new file if doesn't exist
            self.df = new_row
        
        # Save to CSV
        self.df.to_csv(self.filename, index=False)
        print(f"✅ Data saved to {self.filename}")
    
    def load_historical_data(self):
        """Load historical data from CSV"""
        try:
            self.df = pd.read_csv(self.filename)
            self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
            print(f"✅ Loaded {len(self.df)} historical records")
            return self.df
        except FileNotFoundError:
            print("❌ No historical data found")
            return None
    
    def get_statistics(self):
        """Calculate statistics from historical data"""
        if self.df is None or self.df.empty:
            print("No data available for statistics")
            return None
        
        stats = {
            'mean_temp': self.df['temperature'].mean(),
            'max_temp': self.df['temperature'].max(),
            'min_temp': self.df['temperature'].min(),
            'mean_heat_index': self.df['heat_index'].mean(),
            'max_heat_index': self.df['heat_index'].max(),
            'mean_humidity': self.df['humidity'].mean(),
            'total_records': len(self.df)
        }
        
        return stats
    
    def plot_temperature_trend(self):
        """Create a simple plot of temperature trend"""
        if self.df is None or self.df.empty:
            print("No data available for plotting")
            return
        
        plt.figure(figsize=(12, 6))
        plt.plot(self.df['timestamp'], self.df['temperature'], label='Temperature', color='red')
        plt.plot(self.df['timestamp'], self.df['heat_index'], label='Heat Index', color='orange')
        plt.xlabel('Time')
        plt.ylabel('Temperature (°F)')
        plt.title('Boston Temperature Trend')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

# =============================================================================
# STEP 6: Create Simple ML Predictor
# =============================================================================

class SimpleHeatPredictor:
    """Simple machine learning model to predict heat index"""
    
    def __init__(self):
        """Initialize the predictor"""
        self.model = None
        self.is_trained = False
        
    def prepare_features(self, df):
        """Prepare features for ML model"""
        # Create time-based features
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
        df['month'] = pd.to_datetime(df['timestamp']).dt.month
        
        # Select features for prediction
        feature_columns = ['temperature', 'humidity', 'dewpoint', 'wind_speed', 'pressure', 'hour']
        
        # Remove rows with missing values
        df_clean = df.dropna(subset=feature_columns + ['heat_index'])
        
        X = df_clean[feature_columns]
        y = df_clean['heat_index']
        
        return X, y
    
    def train_model(self, df):
        """Train a simple Random Forest model"""
        print("Training ML model...")
        
        try:
            X, y = self.prepare_features(df)
            
            if len(X) < 10:
                print("❌ Not enough data to train model (need at least 10 records)")
                return False
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train model
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.model.fit(X_train, y_train)
            
            # Evaluate
            predictions = self.model.predict(X_test)
            mae = mean_absolute_error(y_test, predictions)
            r2 = r2_score(y_test, predictions)
            
            print(f"✅ Model trained successfully!")
            print(f"   Mean Absolute Error: {mae:.2f}°F")
            print(f"   R² Score: {r2:.2f}")
            
            self.is_trained = True
            return True
            
        except Exception as e:
            print(f"❌ Error training model: {e}")
            return False
    
    def predict_heat_index(self, temp, humidity, dewpoint, wind_speed, pressure, hour):
        """Predict heat index for given conditions"""
        if not self.is_trained:
            print("Model not trained yet!")
            return None
        
        # Create feature array
        features = pd.DataFrame({
            'temperature': [temp],
            'humidity': [humidity],
            'dewpoint': [dewpoint],
            'wind_speed': [wind_speed],
            'pressure': [pressure],
            'hour': [hour]
        })
        
        # Make prediction
        prediction = self.model.predict(features)[0]
        return round(prediction, 1)

# =============================================================================
# STEP 7: Create Visualization Dashboard
# =============================================================================

class HeatwaveVisualizer:
    """Create visualizations for the heatwave data"""
    
    @staticmethod
    def create_dashboard(weather_data, neighborhood_temps, vulnerable_impact):
        """Create a comprehensive dashboard"""
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Boston Heatwave Monitoring Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Current Conditions Gauge
        ax1 = axes[0, 0]
        heat_index = weather_data.get('heat_index', 0)
        colors = ['green', 'yellow', 'orange', 'red', 'purple']
        ranges = [0, 80, 90, 105, 130, 150]
        
        # Find which range the heat index falls into
        color_idx = 0
        for i in range(len(ranges)-1):
            if heat_index >= ranges[i] and heat_index < ranges[i+1]:
                color_idx = i
                break
        
        ax1.barh(['Heat Index'], [heat_index], color=colors[color_idx])
        ax1.set_xlim(50, 150)
        ax1.set_xlabel('Temperature (°F)')
        ax1.set_title(f'Current Heat Index: {heat_index}°F')
        ax1.axvline(x=80, color='yellow', linestyle='--', alpha=0.5)
        ax1.axvline(x=90, color='orange', linestyle='--', alpha=0.5)
        ax1.axvline(x=105, color='red', linestyle='--', alpha=0.5)
        
        # 2. Neighborhood Temperatures
        ax2 = axes[0, 1]
        neighborhoods = list(neighborhood_temps.keys())[:5]  # Top 5 hottest
        temps = [neighborhood_temps[n]['temperature'] for n in neighborhoods]
        colors_n = ['red' if t > 90 else 'orange' if t > 80 else 'green' for t in temps]
        
        ax2.barh(neighborhoods, temps, color=colors_n)
        ax2.set_xlabel('Temperature (°F)')
        ax2.set_title('Hottest Neighborhoods')
        ax2.set_xlim(60, max(temps) + 5)
        
        # 3. Vulnerable Population Impact
        ax3 = axes[1, 0]
        categories = ['Elderly\n(65+)', 'Children\n(<5)', 'Chronic\nConditions', 'Outdoor\nWorkers']
        values = [
            vulnerable_impact['elderly_65plus'],
            vulnerable_impact['children_under5'],
            vulnerable_impact['chronic_conditions'],
            vulnerable_impact['outdoor_workers']
        ]
        
        ax3.bar(categories, values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'])
        ax3.set_ylabel('People at Risk')
        ax3.set_title('Vulnerable Population Impact')
        ax3.set_ylim(0, max(values) * 1.2)
        
        # Add value labels on bars
        for i, v in enumerate(values):
            ax3.text(i, v + max(values)*0.02, str(v), ha='center')
        
        # 4. Weather Summary Text
        ax4 = axes[1, 1]
        ax4.axis('off')
        
        summary_text = f"""
        🌡️ CURRENT CONDITIONS
        
        Temperature: {weather_data.get('temperature', 'N/A')}°F
        Heat Index: {weather_data.get('heat_index', 'N/A')}°F
        Humidity: {weather_data.get('humidity', 'N/A')}%
        Wind Speed: {weather_data.get('wind_speed', 'N/A')} mph
        
        Total at Risk: {vulnerable_impact['total_at_risk']:,}
        
        Status: {weather_data.get('description', 'N/A')}
        Station: {weather_data.get('station', 'Logan').upper()}
        """
        
        ax4.text(0.1, 0.5, summary_text, fontsize=12, verticalalignment='center',
                fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def create_interactive_map(neighborhood_temps):
        """Create an interactive map with Plotly"""
        
        # Boston coordinates
        boston_lat = 42.3601
        boston_lon = -71.0589
        
        # Create data for map
        data = []
        for name, info in neighborhood_temps.items():
            data.append({
                'Neighborhood': name,
                'Temperature': info['temperature'],
                'Green Space': info['green_space_percent'],
                'Vulnerable Pop': info['vulnerable_population']
            })
        
        df = pd.DataFrame(data)
        
        # Create interactive bar chart
        fig = px.bar(df, x='Neighborhood', y='Temperature',
                    color='Temperature',
                    color_continuous_scale='RdYlGn_r',
                    title='Boston Neighborhood Temperatures',
                    hover_data=['Green Space', 'Vulnerable Pop'])
        
        fig.update_layout(
            xaxis_tickangle=-45,
            height=500,
            showlegend=False
        )
        
        fig.show()

# =============================================================================
# STEP 8: Main Application - Putting It All Together
# =============================================================================

class BostonHeatwaveApp:
    """Main application that combines all components"""
    
    def __init__(self):
        """Initialize all components"""
        print("🌡️ Boston Heatwave Monitoring System")
        print("="*50)
        
        self.weather_collector = BostonWeatherCollector()
        self.risk_analyzer = HeatRiskAnalyzer()
        self.data_manager = DataManager()
        self.predictor = SimpleHeatPredictor()
        self.visualizer = HeatwaveVisualizer()
        
    def run_once(self):
        """Run the system once - good for testing"""
        print("\n📊 Starting single data collection...")
        
        # Step 1: Get real weather
        weather_data = self.weather_collector.get_real_weather()
        
        if weather_data:
            # Step 2: Display current weather
            self.weather_collector.display_current_weather()
            
            # Step 3: Calculate neighborhood temperatures
            neighborhood_temps = self.risk_analyzer.calculate_neighborhood_temps(
                weather_data['temperature']
            )
            
            print("\n🏘️ NEIGHBORHOOD HEAT ISLANDS:")
            print("-"*50)
            for name, data in sorted(neighborhood_temps.items(), 
                                    key=lambda x: x[1]['temperature'], 
                                    reverse=True)[:5]:
                print(f"{name:15} {data['temperature']}°F (factor: {data['heat_factor']})")
            
            # Step 4: Assess risk
            risk = self.risk_analyzer.assess_risk_level(weather_data['heat_index'])
            print(f"\n⚠️ RISK LEVEL: {risk['level']} - {risk['action']}")
            
            # Step 5: Calculate vulnerable population impact
            vulnerable = self.risk_analyzer.calculate_vulnerable_impact(
                weather_data['heat_index'],
                neighborhood_temps
            )
            
            print(f"\n👥 VULNERABLE POPULATION IMPACT:")
            print(f"   Total at risk: {vulnerable['total_at_risk']:,}")
            print(f"   Elderly (65+): {vulnerable['elderly_65plus']:,}")
            print(f"   Children (<5): {vulnerable['children_under5']:,}")
            
            # Step 6: Generate alerts
            alerts = self.risk_analyzer.generate_alerts(weather_data, neighborhood_temps)
            
            if alerts:
                print(f"\n🚨 ACTIVE ALERTS:")
                for alert in alerts:
                    print(f"   [{alert['priority']}] {alert['message']}")
            
            # Step 7: Save data
            self.data_manager.save_weather_data(weather_data)
            
            # Step 8: Create visualizations
            self.visualizer.create_dashboard(weather_data, neighborhood_temps, vulnerable)
            
            return weather_data
        else:
            print("❌ Failed to collect weather data")
            return None
    
    def run_continuous(self, interval_minutes=30):
        """Run continuously, collecting data every interval"""
        print(f"\n🔄 Starting continuous monitoring (every {interval_minutes} minutes)")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                # Run once
                self.run_once()
                
                # Wait for next interval
                print(f"\n⏰ Next update in {interval_minutes} minutes...")
                time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            print("\n\n👋 Monitoring stopped by user")
    
    def analyze_historical(self):
        """Analyze historical data if available"""
        print("\n📈 Analyzing historical data...")
        
        df = self.data_manager.load_historical_data()
        
        if df is not None and not df.empty:
            # Get statistics
            stats = self.data_manager.get_statistics()
            
            print("\n📊 HISTORICAL STATISTICS:")
            print(f"   Records: {stats['total_records']}")
            print(f"   Avg Temperature: {stats['mean_temp']:.1f}°F")
            print(f"   Max Temperature: {stats['max_temp']:.1f}°F")
            print(f"   Avg Heat Index: {stats['mean_heat_index']:.1f}°F")
            print(f"   Max Heat Index: {stats['max_heat_index']:.1f}°F")
            
            # Plot trend
            self.data_manager.plot_temperature_trend()
            
            # Train ML model if we have enough data
            if len(df) >= 10:
                print("\n🤖 Training ML model...")
                self.predictor.train_model(df)
                
                # Make a prediction
                if self.predictor.is_trained:
                    current_hour = datetime.now().hour
                    predicted = self.predictor.predict_heat_index(
                        temp=85, humidity=70, dewpoint=72,
                        wind_speed=5, pressure=30.00, hour=current_hour
                    )
                    print(f"\n🔮 Prediction for 85°F, 70% humidity: {predicted}°F heat index")
        else:
            print("❌ No historical data available")

# =============================================================================
# STEP 9: Simple Command Line Interface
# =============================================================================

def main():
    """Main function to run the application"""
    
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   🌡️  BOSTON HEATWAVE MONITORING SYSTEM  🌡️         ║
    ║                                                      ║
    ║   Real-time heat monitoring for Greater Boston      ║
    ║   Data source: NOAA Weather Service                 ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    # Create the app
    app = BostonHeatwaveApp()
    
    while True:
        print("\n" + "="*50)
        print("MENU OPTIONS:")
        print("="*50)
        print("1. Get current weather (single check)")
        print("2. Start continuous monitoring")
        print("3. Analyze historical data")
        print("4. Quick test (simulated data)")
        print("5. Exit")
        print("-"*50)
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            app.run_once()
            
        elif choice == '2':
            try:
                interval = int(input("Enter interval in minutes (default 30): ") or "30")
                app.run_continuous(interval)
            except ValueError:
                print("Invalid interval, using 30 minutes")
                app.run_continuous(30)
                
        elif choice == '3':
            app.analyze_historical()
            
        elif choice == '4':
            print("\n🧪 Running with simulated data for testing...")
            # Create fake data for testing
            fake_weather = {
                'timestamp': datetime.now().isoformat(),
                'station': 'test',
                'temperature': 92,
                'humidity': 65,
                'dewpoint': 76,
                'heat_index': 98,
                'wind_speed': 8,
                'wind_direction': 180,
                'pressure': 29.92,
                'visibility': 10,
                'description': 'Hot and humid (simulated)'
            }
            
            app.weather_collector.current_data = fake_weather
            app.weather_collector.display_current_weather()
            
            # Continue with analysis
            neighborhood_temps = app.risk_analyzer.calculate_neighborhood_temps(92)
            vulnerable = app.risk_analyzer.calculate_vulnerable_impact(98, neighborhood_temps)
            app.visualizer.create_dashboard(fake_weather, neighborhood_temps, vulnerable)
            
        elif choice == '5':
            print("\n👋 Thank you for using Boston Heatwave Monitoring System!")
            break
            
        else:
            print("❌ Invalid choice, please try again")

# =============================================================================
# RUN THE APPLICATION
# =============================================================================

if __name__ == "__main__":
    main()
