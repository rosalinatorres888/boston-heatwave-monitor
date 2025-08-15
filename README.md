# 🌡️ Boston Heatwave Monitor

**Real-time heat monitoring and risk assessment for Greater Boston**

A comprehensive heat monitoring system that tracks dangerous temperature conditions across Boston neighborhoods, analyzes vulnerable population impacts, and provides actionable public health insights.

![Boston Heatwave Monitor](https://img.shields.io/badge/Status-Live-brightgreen) ![Python](https://img.shields.io/badge/Python-3.9+-blue) ![Plotly](https://img.shields.io/badge/Plotly-Interactive-orange) ![NOAA](https://img.shields.io/badge/Data-NOAA%20Weather-lightblue)

## 🎯 **Live Demo**

🌐 **[View Live Dashboard](https://boston-weather-live.netlify.app)**

## ✨ **Features**

### 🌡️ **Real-Time Weather Monitoring**
- Live weather data from NOAA Weather Service API
- Current temperature, humidity, heat index, and conditions
- Multiple Boston-area weather stations (Logan, Blue Hill, Bedford, Norwood)
- No API key required - completely free data source

### 🏘️ **Neighborhood Heat Island Analysis**
- Heat impact analysis for 10 Boston neighborhoods
- Urban heat island effect modeling with realistic factors
- Green space correlation analysis
- Temperature variations across different areas

### 👥 **Vulnerable Population Assessment**
- Real-time risk calculation for at-risk populations:
  - Elderly residents (65+)
  - Children under 5
  - People with chronic conditions  
  - Outdoor workers
- Neighborhood-specific impact analysis
- Population-weighted risk factors

### 📊 **Interactive Visualizations**
- **Heat Index Gauge**: Color-coded risk levels (Low/Moderate/High/Extreme/Dangerous)
- **Neighborhood Temperature Map**: Horizontal bar chart of hottest areas
- **Population Impact Charts**: Breakdown by vulnerable groups
- **Heat vs Green Space Analysis**: Scatter plot showing correlation
- **Heat Island Effect Visualization**: Comparative factors across neighborhoods

### ⚠️ **Risk Level Assessment**
- **LOW** (< 80°F): Normal activities
- **MODERATE** (80-89°F): Stay hydrated  
- **HIGH** (90-104°F): Limit outdoor exposure
- **EXTREME** (105-129°F): Stay indoors, cooling centers open
- **DANGEROUS** (130°F+): Emergency - seek immediate cooling

### 🔄 **Real-Time Updates**
- Automatic refresh every 30 minutes
- Live data generation on each page visit (when deployed)
- Responsive design for mobile and desktop

## 🚀 **Quick Start**

### **Option 1: View Live Dashboard**
Simply visit the live dashboard URL above for real-time Boston heat data.

### **Option 2: Run Locally**

```bash
# Clone the repository
git clone https://github.com/rosalinatorres888/boston-heatwave-monitor.git
cd boston-heatwave-monitor

# Install dependencies
pip install -r requirements.txt

# Generate dashboard
python boston_heatwave_netlify.py

# Open in browser
open index.html
```

## 🛠️ **Installation**

### **Requirements**
- Python 3.9+
- Internet connection (for NOAA API)

### **Dependencies**
```bash
pip install requests pandas numpy plotly
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

## 📋 **Usage**

### **Generate Static Dashboard**
```bash
python boston_heatwave_netlify.py
```
Creates `index.html` with current weather data and interactive charts.

### **Run Original Analysis Tool**
```bash
python boston_heatwave.py
```
Command-line interface with detailed analysis and visualizations.

## 🌐 **Deployment**

### **Netlify (Recommended)**

1. **Fork/Clone this repository**
2. **Push to your GitHub account**  
3. **Connect to Netlify:**
   - Build command: `pip install -r requirements.txt && python boston_heatwave_netlify.py`
   - Publish directory: `.`
   - Branch: `main`

### **GitHub Pages + Actions**
Set up automated updates with GitHub Actions (see `.github/workflows/` for configuration).

### **Other Platforms**
- **Vercel**: Similar setup to Netlify
- **Railway**: For Python hosting
- **Heroku**: With buildpack for Python

## 📊 **Data Sources**

### **Weather Data: NOAA Weather Service API**
- **Endpoint**: `https://api.weather.gov/stations/{station_id}/observations/latest`
- **Stations**: 
  - KBOS (Logan International Airport)
  - KMQE (Blue Hill Observatory)
  - KBED (Hanscom Field, Bedford)
  - KOWD (Norwood Memorial Airport)
- **Data Points**: Temperature, humidity, heat index, wind speed, visibility, conditions
- **Update Frequency**: Real-time (typically every hour)
- **Cost**: Free, no API key required

### **Neighborhood Data**
Based on research from:
- Boston Public Health Commission heat vulnerability studies
- Urban heat island research for Greater Boston
- Census data for population demographics
- Green space analysis from city planning data

## 🏗️ **Technical Architecture**

### **Core Components**

1. **`BostonWeatherCollector`**: Fetches real-time weather data from NOAA
2. **`HeatRiskAnalyzer`**: Calculates risk levels and vulnerable population impacts  
3. **`PlotlyDashboardGenerator`**: Creates interactive visualizations
4. **Heat Index Calculation**: Official NOAA formula implementation

### **Key Features**

- **Fallback Data**: Sample data if API is unavailable
- **Error Handling**: Robust error handling for API failures
- **Responsive Design**: Mobile-friendly dashboard
- **Performance**: Efficient data processing and visualization
- **Accessibility**: Clear color coding and readable fonts

## 📈 **Monitored Neighborhoods**

| Neighborhood | Heat Factor | Vulnerable Population | Green Space % |
|--------------|-------------|----------------------|---------------|
| Chinatown | 1.5x | 3,500 | 2% |
| Roxbury | 1.4x | 8,500 | 8% |
| Dorchester | 1.3x | 12,000 | 12% |
| East Boston | 1.35x | 6,500 | 5% |
| Mattapan | 1.25x | 5,500 | 15% |
| South End | 1.3x | 4,000 | 6% |
| Back Bay | 1.15x | 2,500 | 20% |
| Jamaica Plain | 1.1x | 5,000 | 35% |
| Charlestown | 1.2x | 3,000 | 10% |
| Brighton | 1.05x | 6,000 | 25% |

## 🔮 **Future Enhancements**

- [ ] **Historical Data Analysis**: Trend analysis over time
- [ ] **Forecast Integration**: 5-day heat forecasts
- [ ] **Alert System**: Email/SMS notifications for extreme heat
- [ ] **More Cities**: Expand beyond Boston
- [ ] **API Endpoint**: Provide JSON API for other applications
- [ ] **Real-Time Air Quality**: Integrate air quality data
- [ ] **Cooling Centers**: Interactive map of available cooling centers
- [ ] **Mobile App**: Native mobile applications
- [ ] **Social Features**: Community reporting and alerts

## 📱 **Screenshots**

*Dashboard displays:*
- **Heat Index Gauge**: Real-time temperature with risk color coding
- **Neighborhood Heat Map**: Horizontal bars showing temperature variations
- **Vulnerable Population Chart**: Impact breakdown by demographics  
- **Heat vs Green Space**: Scatter plot correlation analysis
- **Current Conditions**: Detailed weather summary card
- **Risk Assessment**: Clear action recommendations

## 🤝 **Contributing**

We welcome contributions! Here's how to help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`  
5. **Open a Pull Request**

### **Areas for Contribution**
- Additional weather stations
- Improved neighborhood modeling
- Mobile responsiveness enhancements
- Data visualization improvements
- Performance optimizations
- Documentation improvements

## 📊 **Performance**

- **Data Collection**: ~2-3 seconds
- **Dashboard Generation**: ~5-10 seconds
- **Page Load Time**: ~1-2 seconds
- **Update Frequency**: Every 30 minutes (configurable)
- **Browser Compatibility**: All modern browsers

## 🛡️ **Privacy & Security**

- **No Personal Data Collection**: Only uses public weather data
- **No API Keys Required**: Uses free public APIs
- **No User Tracking**: Statically generated dashboard
- **Open Source**: Fully transparent codebase

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 **Author**

**Rosalina Torres**
- GitHub: [@rosalinatorres888](https://github.com/rosalinatorres888)
- Project: [Boston Heatwave Monitor](https://github.com/rosalinatorres888/boston-heatwave-monitor)

## 🙏 **Acknowledgments**

- **NOAA Weather Service** for providing free, real-time weather data
- **Plotly** for excellent interactive visualization capabilities  
- **Boston Public Health Commission** for heat vulnerability research
- **Urban heat island research community** for neighborhood modeling insights
- **Open source community** for tools and libraries

## 📞 **Support**

- **Issues**: [GitHub Issues](https://github.com/rosalinatorres888/boston-heatwave-monitor/issues)
- **Documentation**: See project wiki
- **Updates**: Watch this repository for latest features

---

**🌡️ Stay Cool, Stay Safe, Stay Informed**

*Real-time heat monitoring for a healthier Boston community*
