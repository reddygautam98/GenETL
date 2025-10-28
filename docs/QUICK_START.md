# GenETL Quick Start Guide

Get up and running with GenETL in under 15 minutes! This guide covers the essentials to start using the AI-Enhanced ETL Data Platform.

## 🚀 5-Minute Setup

### Prerequisites
- Docker and Docker Compose installed
- 8GB+ RAM available
- Ports 5450, 6390, 8095 available

### Quick Installation

1. **Clone and Start**
   ```bash
   git clone https://github.com/reddygautam98/GenETL.git
   cd GenETL
   docker-compose up -d
   ```

2. **Create Airflow User** (in new terminal)
   ```bash
   docker exec -it genetl-airflow-webserver airflow users create \
     --username admin --firstname Admin --lastname User \
     --role Admin --email admin@example.com --password admin
   ```

3. **Access GenETL**
   - Open http://localhost:8095
   - Login: admin / admin

## 🧠 Try the AI Features (5 minutes)

### Test All AI Components
```bash
# Verify everything works
python test_ai_basic.py
```

Expected output:
```
✅ AI Insights Generator: Working
✅ Smart Data Quality AI: Working  
✅ AI Query Interface: Working
✅ Predictive Analytics Engine: Working
✅ AI Report Generator: Working
All AI components are functioning correctly!
```

### Run AI Demo
```bash
# See AI features in action
python demo_ai_features.py
```

This will:
- Load sample data (5000 products)
- Generate business insights
- Create quality reports
- Process natural language queries
- Generate predictions
- Create an HTML business report

## 🔄 Run Your First Pipeline (5 minutes)

### In Airflow UI (localhost:8095):

1. **Find the AI Pipeline**
   - Look for `ai_enhanced_etl_dag`
   - Toggle it ON if it's paused

2. **Trigger a Run**
   - Click the ▷ (play) button
   - Watch tasks turn green as they complete

3. **View Results**
   - Click on the DAG name
   - Check task logs for detailed output
   - Look for generated insights and reports

## 💬 Ask Questions in Natural Language

### Interactive AI Query
```python
from ai_query_interface import AIQueryInterface

query_ai = AIQueryInterface()

# Ask questions about your data
questions = [
    "What is the average price by category?",
    "Show me all high-rated products",
    "Which categories have the most expensive items?",
    "Find products that are almost out of stock"
]

for question in questions:
    response = query_ai.process_natural_query(question)
    print(f"Q: {question}")
    print(f"A: {response.result}\n")
```

## 📊 Generate Business Reports

### Create Instant Business Intelligence
```python
from ai_report_generator import AIReportGenerator

# Generate comprehensive report
report_gen = AIReportGenerator()
html_report = report_gen.compile_comprehensive_report()

# Save and view report
with open('my_business_report.html', 'w') as f:
    f.write(html_report)

print("📊 Business report generated: my_business_report.html")
```

## 🔮 Get Predictions

### Sales Forecasting
```python
from predictive_analytics_engine import PredictiveAnalyticsEngine

predictor = PredictiveAnalyticsEngine()

# Get 30-day business forecast
forecast = predictor.generate_business_forecast(days=30)
print(f"📈 30-day sales prediction: ${forecast.predicted_sales:,.2f}")
print(f"📊 Confidence: {forecast.confidence_score:.1%}")
```

## 🔍 Check Data Quality

### Automatic Quality Analysis
```python
from smart_data_quality_ai import SmartDataQualityAI
from ai_insights_generator import GenETLAIAnalyzer

# Load data and check quality
analyzer = GenETLAIAnalyzer()
data = analyzer.load_warehouse_data()

quality_ai = SmartDataQualityAI()
quality_report = quality_ai.comprehensive_quality_check(data)

print(f"📋 Data Quality Score: {quality_report['overall_score']:.1%}")
print(f"📊 Completeness: {quality_report['completeness']['overall_completeness']:.1%}")
print(f"🎯 Outliers detected: {quality_report['outliers']['total_outliers']}")
```

## 🎯 Common Use Cases

### Business Intelligence Automation
```python
# Daily business insights
from ai_insights_generator import GenETLAIAnalyzer

analyzer = GenETLAIAnalyzer()
data = analyzer.load_warehouse_data()

# Get pricing insights
pricing_insights = analyzer.analyze_pricing_intelligence(data)
for insight in pricing_insights:
    print(f"💡 {insight.insight_type}: {insight.description}")
    print(f"   Confidence: {insight.confidence_score:.1%}\n")
```

### Inventory Management
```python
# Inventory optimization insights
inventory_insights = analyzer.analyze_inventory_intelligence(data)
for insight in inventory_insights:
    if 'low stock' in insight.description.lower():
        print(f"⚠️  ALERT: {insight.description}")
```

### Customer Analytics
```python
# Product performance analysis  
quality_insights = analyzer.analyze_quality_intelligence(data)
for insight in quality_insights:
    if insight.insight_type == 'rating_analysis':
        print(f"⭐ {insight.description}")
```

## ⚙️ Quick Configuration

### Essential Settings
Create `.env` file with:
```env
# Database (use defaults for quick start)
POSTGRES_HOST=localhost
POSTGRES_PORT=5450
POSTGRES_DB=genetl_warehouse
POSTGRES_USER=genetl
POSTGRES_PASSWORD=genetl_pass

# AI Settings (adjust as needed)
AI_MODEL_CONFIDENCE_THRESHOLD=0.7
AI_MAX_RECORDS_PER_BATCH=10000
AI_ENABLE_CACHING=True

# Performance
LOG_LEVEL=INFO
DEBUG=False
```

## 🔧 Quick Troubleshooting

### Container Issues
```bash
# Check if all containers are running
docker-compose ps

# Restart if needed
docker-compose restart

# View logs if problems
docker-compose logs genetl-airflow-webserver
```

### Database Connection Issues
```bash
# Test database connection
docker-compose exec genetl-postgres pg_isready -U genetl
```

### AI Component Issues
```bash
# Re-run AI test
python test_ai_basic.py

# Check Python environment
python -c "import pandas, sqlalchemy, scipy, plotly; print('✅ All packages available')"
```

## 📈 Next Steps

### Explore More Features
1. **Custom Pipelines**: Create your own ETL workflows
2. **Advanced AI**: Tune AI models for your specific data
3. **Integrations**: Connect to your existing tools
4. **Scheduling**: Set up automated pipeline runs
5. **Monitoring**: Add alerts and performance tracking

### Learn More
- **Full User Guide**: [USER_GUIDE.md](USER_GUIDE.md)
- **API Reference**: [API_REFERENCE.md](API_REFERENCE.md)
- **Configuration Guide**: [CONFIGURATION.md](CONFIGURATION.md)
- **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Get Help
- **Issues**: [GitHub Issues](https://github.com/reddygautam98/GenETL/issues)
- **Discussions**: [GitHub Discussions](https://github.com/reddygautam98/GenETL/discussions)
- **Email**: [reddygautam98@gmail.com](mailto:reddygautam98@gmail.com)

## 📋 Quick Reference Card

### Essential Commands
```bash
# Start GenETL
docker-compose up -d

# Stop GenETL
docker-compose down

# View logs
docker-compose logs

# Test AI features
python test_ai_basic.py

# Run AI demo
python demo_ai_features.py

# Check service status
docker-compose ps
```

### Key URLs
- **Airflow UI**: http://localhost:8095
- **Database**: localhost:5450
- **Redis**: localhost:6390

### Default Credentials
- **Airflow**: admin / admin
- **Database**: genetl / genetl_pass

### Quick AI Examples
```python
# Business insights
from ai_insights_generator import GenETLAIAnalyzer
analyzer = GenETLAIAnalyzer()
insights = analyzer.analyze_pricing_intelligence(analyzer.load_warehouse_data())

# Natural language queries
from ai_query_interface import AIQueryInterface
query_ai = AIQueryInterface()
result = query_ai.process_natural_query("What is the average price?")

# Business reports
from ai_report_generator import AIReportGenerator
report_gen = AIReportGenerator()
report = report_gen.compile_comprehensive_report()

# Predictions
from predictive_analytics_engine import PredictiveAnalyticsEngine
predictor = PredictiveAnalyticsEngine()
forecast = predictor.generate_business_forecast(days=7)
```

---

**🎉 Congratulations!** You're now ready to explore GenETL's powerful AI-enhanced ETL capabilities. 

*Need help? Check out the [Full User Guide](USER_GUIDE.md) or [contact support](mailto:reddygautam98@gmail.com).*