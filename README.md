# 🌡️ Boston Heatwave Monitor

**Real-time heat monitoring and risk assessment for Greater Boston**

A comprehensive heat monitoring system that tracks dangerous temperature conditions across Boston neighborhoods, analyzes vulnerable population impacts, and provides actionable public health insights.

![Boston Heatwave Monitor](https://img.shields.io/badge/Status-Live-brightgreen) ![Python](https://img.shields.io/badge/Python-3.9+-blue) ![Plotly](https://img.shields.io/badge/Plotly-Interactive-orange) ![Streamlit](https://img.shields.io/badge/Streamlit-Live-red) ![NOAA](https://img.shields.io/badge/Data-NOAA%20Weather-lightblue)

## 🎯 **Live Demos**

### 🌟 **Interactive Streamlit Dashboard (Recommended)**
🌐 **[View Interactive Dashboard](https://boston-weather-live.streamlit.app/)** 
*Features real-time widgets, custom neon styling, and enhanced interactivity*

### 📊 **Static Plotly Dashboard**
🌐 **[View Static Dashboard](https://boston-weather-live.netlify.app/)**
*Clean, professional charts with responsive design*

## ✨ **Features**

### 🌡️ **Real-Time Weather Monitoring**
- Live weather data from NOAA Weather Service API (Logan Airport)
- Current temperature, humidity, heat index, and conditions
- Multiple Boston-area weather stations (Logan, Blue Hill, Bedford, Norwood)
- **No API key required** - completely free data source
- Updates automatically on page refresh

### 🏘️ **Neighborhood Heat Island Analysis**
- Heat impact analysis for **10 Boston neighborhoods**:
  - Chinatown, Roxbury, Dorchester, East Boston, Mattapan
  - South End, Back Bay, Jamaica Plain, Charlestown, Brighton
- Urban heat island effect modeling with realistic factors (1.05x - 1.5x multipliers)
- Green space correlation analysis
- Temperature variations across different areas

### 👥 **Vulnerable Population Assessment**
- Real-time risk calculation for **at-risk populations**:
  - **Elderly residents** (65+) - 35% of total risk
  - **Children under 5** - 15% of total risk
  - **People with chronic conditions** - 30% of total risk
  - **Outdoor workers** - 20% of total risk
- Neighborhood-specific impact analysis with population-weighted risk factors
- **Current monitoring**: Up to 12,000+ vulnerable residents across Boston

### 📊 **Interactive Visualizations**

#### **Streamlit Version Features:**
- **🎨 Custom neon theme** with dark mode styling
- **🎛️ Interactive widgets** and real-time controls
- **📱 Mobile-optimized** responsive design
- **⚡ Enhanced user experience** with Streamlit's powerful features

#### **Plotly Version Features:**
- **🌡️ Heat Index Gauge**: Color-coded risk levels with professional styling
- **🏘️ Neighborhood Temperature Map**: Horizontal bar chart of hottest areas
- **👥 Population Impact Charts**: Breakdown by vulnerable groups
- **📈 Heat vs Green Space Analysis**: Scatter plot showing correlation
- **🔥 Heat Island Effect Visualization**: Comparative factors across neighborhoods

### ⚠️ **5-Level Risk Assessment System**
- **🟢 LOW** (< 80°F): Normal activities safe
- **🟡 MODERATE** (80-89°F): Stay hydrated, monitor conditions
- **🟠 HIGH** (90-104°F): Limit outdoor exposure, check on vulnerable neighbors
- **🔴 EXTREME** (105-129°F): Stay indoors, cooling centers open
- **🟣 DANGEROUS** (130°F+): EMERGENCY - seek immediate cooling

### 🔄 **Real-Time Updates**
- **Streamlit**: Real-time data generation on each interaction
- **Netlify**: Automatic refresh every 30 minutes + fresh data on page visits
- Live weather conditions from Logan International Airport
- Responsive design for mobile and desktop

## 🚀 **Quick Start**

### **Option 1: View Live Dashboards**
- **Interactive Experience**: Visit [boston-weather-live.streamlit.app](https://boston-weather-live.streamlit.app/)
- **Static Dashboard**: Visit [boston-weather-live.netlify.app](https://boston-weather-live.netlify.app/)

### **Option 2: Run Locally**

```bash
# Clone the repository
git clone https://github.com/rosalinatorres888/boston-heatwave-monitor.git
cd boston-heatwave-monitor

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app (interactive)
streamlit run app_neon.py

# OR generate static dashboard
python boston_heatwave_netlify.py
open index.html
```

## 🛠️ **Installation**

### **Requirements**
- Python 3.9+ (Tested on Python 3.13)
- Internet connection (for NOAA API)

### **Dependencies**
```bash
# Main dependencies
pip install streamlit pandas numpy plotly requests seaborn matplotlib scikit-learn
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

## 📋 **Usage**

### **Interactive Streamlit App**
```bash
streamlit run app_neon.py
```
- Opens at `http://localhost:8501`
- Features custom neon styling, interactive widgets, and real-time updates

### **Static Dashboard Generator**
```bash
python boston_heatwave_netlify.py
```
- Creates `index.html` with current weather data and interactive Plotly charts
- Perfect for static hosting on Netlify, Vercel, or GitHub Pages

### **Original Analysis Tool**
```bash
python boston_heatwave.py
```
- Command-line interface with detailed analysis, ML predictions, and matplotlib visualizations

## 🌐 **Deployment**

### **Streamlit Cloud (Recommended for Interactive Apps)**
1. **Fork/Clone** this repository
2. **Push to GitHub**
3. **Deploy on Streamlit Cloud:**
   - Repository: `your-username/boston-heatwave-monitor`
   - Branch: `main`
   - Main file: `app_neon.py`
   - **Auto-deployment** on git push

### **Netlify (Perfect for Static Dashboards)**
1. **Connect GitHub repository**
2. **Build settings:**
   - Build command: `pip install -r requirements.txt && python boston_heatwave_netlify.py`
   - Publish directory: `.`
   - Branch: `main`

### **Other Platforms**
- **Railway**: Excellent for Streamlit apps
- **Heroku**: Classic deployment platform
- **Render**: Free tier with auto-deploy
- **Vercel**: Great for static sites

## 📊 **Data Sources**

### **Weather Data: NOAA Weather Service API**
- **Primary Endpoint**: `https://api.weather.gov/stations/KBOS/observations/latest`
- **Station**: KBOS (Logan International Airport, Boston)
- **Additional Stations**: 
  - KMQE (Blue Hill Observatory) - Highest point in Greater Boston
  - KBED (Hanscom Field, Bedford) - Northwest suburbs
  - KOWD (Norwood Memorial Airport) - Southwest suburbs
- **Data Points**: Temperature, humidity, heat index, wind speed, visibility, conditions
- **Update Frequency**: Every 1-3 hours (NOAA standard)
- **Cost**: **100% Free** - No API key, no rate limits

### **Neighborhood Heat Island Data**
Research-based data from:
- **Boston Public Health Commission** heat vulnerability studies
- **Urban heat island research** for Greater Boston metropolitan area
- **U.S. Census Bureau** demographic data
- **Boston Planning & Development Agency** green space analysis
- **Climate Ready Boston** resilience planning data

## 🏗️ **Technical Architecture**

### **Core Components**

#### **Data Collection Layer**
1. **`BostonWeatherCollector`**: Fetches real-time weather data from NOAA API
   - Automatic fallback to sample data if API unavailable
   - Multiple weather station support
   - Official NOAA heat index calculation

#### **Analysis Layer**
2. **`HeatRiskAnalyzer`**: Risk assessment and vulnerable population modeling
   - 5-level risk classification system
   - Neighborhood-specific heat island multipliers
   - Population-weighted vulnerability calculations

#### **Visualization Layer**
3. **`PlotlyDashboardGenerator`**: Interactive chart generation
4. **Streamlit Interface**: Real-time interactive dashboard
5. **Static HTML Generator**: Self-contained dashboard files

### **Key Technical Features**
- **🛡️ Robust error handling** with graceful API failure recovery
- **📱 Responsive design** optimized for mobile and desktop
- **⚡ Performance optimized** data processing and visualization
- **♿ Accessibility features** with clear color coding and readable fonts
- **🔄 Real-time updates** with configurable refresh intervals

## 📈 **Monitored Neighborhoods**

| Neighborhood | Heat Factor | Vulnerable Pop. | Green Space % | Risk Level |
|--------------|-------------|----------------|---------------|------------|
| **Chinatown** | **1.5x** | 3,500 | 2% | 🔴 Highest |
| **Roxbury** | **1.4x** | 8,500 | 8% | 🔴 Very High |
| **East Boston** | 1.35x | 6,500 | 5% | 🟠 High |
| **Dorchester** | 1.3x | 12,000 | 12% | 🟠 High |
| **South End** | 1.3x | 4,000 | 6% | 🟠 High |
| Mattapan | 1.25x | 5,500 | 15% | 🟡 Moderate |
| Charlestown | 1.2x | 3,000 | 10% | 🟡 Moderate |
| Back Bay | 1.15x | 2,500 | 20% | 🟡 Lower |
| Jamaica Plain | 1.1x | 5,000 | 35% | 🟢 Lowest |
| Brighton | 1.05x | 6,000 | 25% | 🟢 Lowest |

**Total Monitored Population**: **56,000+ vulnerable residents**

## 🔮 **Future Enhancements**

### **Planned Features**
- [ ] **📧 Alert System**: Email/SMS notifications for extreme heat warnings
- [ ] **📅 Historical Analysis**: 30-day temperature trends and patterns
- [ ] **🌤️ Weather Forecasting**: 5-day heat forecast integration
- [ ] **🗺️ Interactive Map**: Neighborhood heat map with cooling center locations
- [ ] **📊 Air Quality Integration**: AQI data during heat events
- [ ] **📱 PWA Mobile App**: Installable progressive web app
- [ ] **🔗 API Endpoint**: JSON API for third-party integrations

### **Expansion Ideas**
- [ ] **🌍 Multi-City Support**: Extend to other metropolitan areas
- [ ] **🏥 Healthcare Integration**: Hospital heat emergency preparedness
- [ ] **📢 Social Features**: Community heat reporting and neighborhood alerts
- [ ] **🧠 ML Predictions**: Advanced heat event forecasting with machine learning
- [ ] **📱 Native Mobile Apps**: iOS and Android applications

## 💻 **Development**

### **Project Structure**
```
boston-heatwave-monitor/
├── 📱 app_neon.py                    # Interactive Streamlit dashboard
├── 🌐 boston_heatwave_netlify.py     # Static dashboard generator  
├── 🐍 boston_heatwave.py             # Original analysis tool
├── 📄 index.html                     # Generated static dashboard
├── 📋 requirements.txt               # Python dependencies
├── 📖 README.md                      # This file
└── 📊 data/
    └── boston_weather_data.csv       # Historical weather data
```

### **Key Files**
- **`app_neon.py`**: Main Streamlit application with custom styling
- **`boston_heatwave_netlify.py`**: Plotly dashboard generator for static hosting
- **`boston_heatwave.py`**: Original comprehensive analysis tool with ML features

## 🤝 **Contributing**

We welcome contributions! Areas for improvement:

### **High Priority**
- **📱 Mobile optimization** improvements
- **♿ Accessibility enhancements**
- **🎨 UI/UX improvements**
- **📊 Additional data visualizations**

### **Medium Priority**
- **🏥 Healthcare provider features**
- **📧 Notification system**
- **🗺️ Interactive mapping**
- **📈 Historical trend analysis**

### **How to Contribute**
1. **Fork** the repository
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

## 📊 **Performance & Analytics**

### **System Performance**
- **⚡ Data Collection**: ~2-3 seconds from NOAA API
- **🎨 Dashboard Generation**: ~5-10 seconds (static), instant (Streamlit)
- **📱 Page Load Time**: ~1-2 seconds on 4G connection
- **🔄 Update Frequency**: 30 minutes (configurable)
- **🌍 Browser Support**: All modern browsers (Chrome, Firefox, Safari, Edge)

### **Usage Statistics** (Since Launch)
- **📈 Live Deployments**: 2 (Streamlit + Netlify)
- **🌡️ Weather Stations**: 4 monitored
- **🏘️ Neighborhoods**: 10 analyzed
- **👥 Population Coverage**: 56,000+ vulnerable residents

## 🛡️ **Privacy & Security**

### **Data Privacy**
- **🚫 No personal data collection**: Only uses public weather data
- **🔑 No API keys required**: Uses free public NOAA endpoints
- **📊 No user tracking**: Statically generated dashboards
- **🔓 Open source**: Fully transparent codebase

### **Security Features**
- **✅ HTTPS everywhere**: Secure connections on all deployments
- **🛡️ No sensitive data storage**: All data is public weather information
- **🔄 Regular updates**: Dependencies updated for security patches

## 📄 **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 **Author**

**Rosalina Torres**
- GitHub: [@rosalinatorres888](https://github.com/rosalinatorres888)
- Project: [Boston Heatwave Monitor](https://github.com/rosalinatorres888/boston-heatwave-monitor)
- Live Apps: [Streamlit](https://boston-weather-live.streamlit.app/) | [Netlify](https://boston-weather-live.netlify.app/)

## 🙏 **Acknowledgments**

### **Data & Research**
- **🏛️ NOAA Weather Service** for providing free, real-time weather data
- **🏥 Boston Public Health Commission** for heat vulnerability research
- **🌡️ Urban heat island research community** for neighborhood modeling insights
- **📊 Climate Ready Boston** for resilience planning data

### **Technology & Tools**
- **🎨 Streamlit** for amazing interactive web apps
- **📊 Plotly** for excellent interactive visualization capabilities
- **🌐 Netlify** for seamless static site deployment
- **☁️ Streamlit Cloud** for free interactive app hosting
- **🐙 GitHub** for code hosting and version control

### **Community**
- **🔓 Open source community** for tools, libraries, and inspiration
- **🌡️ Weather monitoring enthusiasts** for feedback and suggestions
- **🏙️ Boston community** for the motivation to create this public service

## 📞 **Support & Contact**

- **🐛 Issues**: [GitHub Issues](https://github.com/rosalinatorres888/boston-heatwave-monitor/issues)
- **📚 Documentation**: Project README and code comments
- **📈 Updates**: Watch this repository for latest features
- **💬 Discussions**: GitHub Discussions for questions and ideas

---

## 🏆 **Project Achievements**

✅ **Two Live Production Deployments**  
✅ **Real-Time Weather Monitoring**  
✅ **56,000+ Vulnerable Residents Monitored**  
✅ **Zero-Cost Public Service**  
✅ **Mobile-Responsive Design**  
✅ **Open Source & Transparent**  

---

**🌡️ Stay Cool, Stay Safe, Stay Informed**

*Real-time heat monitoring for a healthier Boston community*

### 📱 **Quick Access Links**
- 🌟 **[Interactive Dashboard](https://boston-weather-live.streamlit.app/)** ← *Start Here!*
- 📊 **[Static Dashboard](https://boston-weather-live.netlify.app/)**
- 🐙 **[Source Code](https://github.com/rosalinatorres888/boston-heatwave-monitor)**