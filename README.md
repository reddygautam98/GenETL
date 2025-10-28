# GenETL - AI-Enhanced ETL Data Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=flat&logo=Apache%20Airflow&logoColor=white)](https://airflow.apache.org/)
[![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

> **A comprehensive AI-powered ETL platform combining traditional data processing with advanced artificial intelligence capabilities for intelligent analytics, automated insights, and predictive forecasting.**

## 🚀 Features

### 🧠 AI-Powered Intelligence
- **AI Insights Generator** - Automated business intelligence with pricing, inventory, and quality analysis
- **Smart Data Quality AI** - Intelligent anomaly detection and data validation
- **AI Query Interface** - Natural language to SQL conversion for easy data access
- **Predictive Analytics Engine** - ML-powered forecasting and trend analysis
- **AI Report Generator** - Automated business intelligence reports with visualizations

### ⚙️ Core ETL Infrastructure
- **Apache Airflow 2.7.3** - Workflow orchestration and scheduling
- **PostgreSQL Database** - Scalable data warehouse
- **Redis Cache** - High-performance caching layer
- **Docker Containerization** - Easy deployment and scaling

### 📊 Advanced Analytics
- Real-time data processing and validation
- Interactive dashboards and visualizations
- Automated report generation
- Business intelligence insights
- Predictive modeling and forecasting

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   GenETL AI Platform                        │
├─────────────────────────────────────────────────────────────┤
│  Data Sources → AI Quality Check → AI Transform → AI Load   │
│                          ↓                                  │
│              AI Insights & Predictions                      │
│                          ↓                                  │
│               AI Report Generation                          │
│                          ↓                                  │
│            Business Intelligence Dashboard                  │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

- **Language:** Python 3.13+
- **Orchestration:** Apache Airflow 2.7.3
- **Database:** PostgreSQL 15+
- **Cache:** Redis 7+
- **Containerization:** Docker & Docker Compose
- **AI/ML:** SciPy, Pandas, NumPy, Plotly
- **Web Framework:** Flask (for Airflow UI)

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.13+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/reddygautam98/GenETL.git
   cd GenETL
   ```

2. **Set up Python environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Start the platform**
   ```bash
   docker-compose up -d
   ```

4. **Initialize Airflow**
   ```bash
   docker exec -it genetl-airflow-webserver airflow db init
   docker exec -it genetl-airflow-webserver airflow users create \
     --username admin --firstname Admin --lastname User \
     --role Admin --email admin@example.com --password admin
   ```

5. **Access the services**
   - **Airflow UI:** http://localhost:8095 (admin/admin)
   - **Database:** localhost:5450 (genetl/genetl_pass)
   - **Redis:** localhost:6390

## 📊 AI Components

### 🧠 AI Insights Generator
Provides comprehensive business intelligence analysis:
- Pricing anomaly detection
- Inventory optimization recommendations
- Quality assessment and insights
- Category performance analysis

```python
from ai_insights_generator import GenETLAIAnalyzer

analyzer = GenETLAIAnalyzer()
insights = analyzer.analyze_pricing_intelligence(data)
```

### 🔍 Smart Data Quality AI
Automated data validation and quality assurance:
- Statistical outlier detection
- Data completeness validation
- Pattern analysis and consistency checks
- Automated improvement recommendations

```python
from smart_data_quality_ai import SmartDataQualityAI

quality_ai = SmartDataQualityAI()
issues = quality_ai.comprehensive_quality_check(dataframe)
```

### 💬 AI Query Interface
Natural language data access:
- Convert questions to SQL queries
- Interactive chat interface
- Intent recognition and processing
- Automated query optimization

```python
from ai_query_interface import AIQueryInterface

query_ai = AIQueryInterface()
result = query_ai.process_natural_query("Show me all high-rated products")
```

### 🔮 Predictive Analytics Engine
ML-powered forecasting and predictions:
- Sales performance forecasting
- Market trend analysis
- Demand prediction
- Business performance modeling

```python
from predictive_analytics_engine import PredictiveAnalyticsEngine

predictor = PredictiveAnalyticsEngine()
forecast = predictor.generate_business_forecast(days=30)
```

### 📊 AI Report Generator
Automated business intelligence reporting:
- Executive dashboards
- Interactive visualizations
- AI-written insights
- Professional HTML reports

```python
from ai_report_generator import AIReportGenerator

report_gen = AIReportGenerator()
html_report = report_gen.compile_comprehensive_report()
```

## 🔄 ETL Pipeline

The AI-Enhanced ETL pipeline includes:

1. **Data Extraction** with intelligent preprocessing
2. **AI Quality Validation** with automated checks
3. **Smart Data Transformation** with AI optimization
4. **Intelligent Data Loading** with real-time insights
5. **Predictive Analytics** generation
6. **Automated Reporting** with AI insights

## 📁 Project Structure

```
GenETL/
├── ai_insights_generator.py        # Business intelligence engine
├── smart_data_quality_ai.py        # Quality validation system
├── ai_query_interface.py           # Natural language interface
├── ai_report_generator.py          # Automated reporting
├── predictive_analytics_engine.py  # ML forecasting engine
├── dags/
│   └── ai_enhanced_etl_dag.py     # Integrated AI pipeline
├── docker-compose.yml             # Container orchestration
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
└── docs/                          # Documentation
```

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5450
POSTGRES_DB=genetl_warehouse
POSTGRES_USER=genetl
POSTGRES_PASSWORD=genetl_pass

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6390

# Airflow Configuration
AIRFLOW_HOME=/opt/airflow
AIRFLOW__CORE__EXECUTOR=LocalExecutor
```

### Database Setup

The platform uses PostgreSQL with the following schema:
- **Database:** `genetl_warehouse`
- **Main Table:** `warehouse.products`
- **Connection:** Configured for AI components

## 📈 Usage Examples

### Running AI Analysis

```python
# Load and analyze business data
from ai_insights_generator import GenETLAIAnalyzer

analyzer = GenETLAIAnalyzer()
data = analyzer.load_warehouse_data()
insights = analyzer.analyze_pricing_intelligence(data)

for insight in insights:
    print(f"{insight.insight_type}: {insight.description}")
```

### Natural Language Queries

```python
# Ask questions in natural language
from ai_query_interface import AIQueryInterface

query_ai = AIQueryInterface()
response = query_ai.process_natural_query("What is the average price by category?")
print(response.result)
```

### Generate Business Reports

```python
# Create comprehensive business reports
from ai_report_generator import AIReportGenerator

report_gen = AIReportGenerator()
html_report = report_gen.compile_comprehensive_report()

# Save report
with open('business_report.html', 'w') as f:
    f.write(html_report)
```

## 🧪 Testing

Run the comprehensive AI features test:

```bash
# Basic functionality test
python test_ai_basic.py

# Comprehensive demo
python demo_ai_features.py
```

## 📚 Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [API Reference](docs/API_REFERENCE.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [AI Features Documentation](docs/AI_FEATURES.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Documentation:** [GenETL Docs](docs/)
- **Issues:** [GitHub Issues](https://github.com/reddygautam98/GenETL/issues)
- **Discussions:** [GitHub Discussions](https://github.com/reddygautam98/GenETL/discussions)

## 🎯 Roadmap

- [ ] Advanced ML model integration
- [ ] Real-time streaming analytics
- [ ] Enhanced visualizations
- [ ] API endpoints for external integration
- [ ] Mobile-friendly dashboards
- [ ] Advanced security features

## 👨‍💻 Author

**Gautam Reddy** - *Initial work* - [reddygautam98](https://github.com/reddygautam98)

## 🙏 Acknowledgments

- Apache Airflow community
- PostgreSQL development team
- Python data science ecosystem
- Open source AI/ML libraries

---

**⭐ If you find this project helpful, please give it a star!**

*GenETL - Transforming data processing with artificial intelligence*