# GenETL User Guide

Welcome to GenETL - the AI-Enhanced ETL Data Platform! This comprehensive guide will help you get the most out of GenETL's powerful features, from basic setup to advanced AI analytics.

## 📚 Table of Contents

1. [Getting Started](#getting-started)
2. [Understanding GenETL](#understanding-genetl)
3. [Installation and Setup](#installation-and-setup)
4. [Basic Usage](#basic-usage)
5. [AI Features Guide](#ai-features-guide)
6. [ETL Pipeline Management](#etl-pipeline-management)
7. [Data Management](#data-management)
8. [Monitoring and Troubleshooting](#monitoring-and-troubleshooting)
9. [Best Practices](#best-practices)
10. [FAQ](#frequently-asked-questions)

---

## Getting Started

### What is GenETL?

GenETL is an AI-powered ETL (Extract, Transform, Load) platform that combines traditional data processing with advanced artificial intelligence capabilities. It provides:

- **Intelligent Data Processing**: AI-driven data quality checks and transformations
- **Business Intelligence**: Automated insights and analytics generation
- **Predictive Analytics**: Machine learning-powered forecasting
- **Natural Language Interface**: Query your data using plain English
- **Automated Reporting**: Professional business intelligence reports

### Who Should Use GenETL?

- **Data Engineers**: Building and managing ETL pipelines
- **Data Analysts**: Analyzing data and generating insights
- **Business Users**: Accessing data through natural language queries
- **Data Scientists**: Leveraging AI for predictive analytics
- **Business Leaders**: Getting automated business intelligence reports

### Prerequisites

Before using GenETL, ensure you have:
- Basic understanding of databases and data concepts
- Familiarity with SQL (helpful but not required for AI features)
- Access to your data sources
- Understanding of your business requirements

---

## Understanding GenETL

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     GenETL Platform                         │
├─────────────────────────────────────────────────────────────┤
│  Data Sources → Extract → AI Quality → Transform → Load     │
│                              ↓                             │
│                      AI Components                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │
│  │ AI Insights │ │ Data Quality│ │ Query Interface     │   │
│  │ Generator   │ │ AI          │ │                     │   │
│  └─────────────┘ └─────────────┘ └─────────────────────┘   │
│  ┌─────────────┐ ┌─────────────┐                           │
│  │ Predictive  │ │ Report      │                           │
│  │ Analytics   │ │ Generator   │                           │
│  └─────────────┘ └─────────────┘                           │
│                              ↓                             │
│              Business Intelligence Dashboard                │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

1. **Apache Airflow**: Orchestrates and schedules your data workflows
2. **PostgreSQL Database**: Stores your processed data and insights
3. **Redis Cache**: Provides high-performance data caching
4. **AI Engine**: Powers all intelligent features and analytics

### AI Components

1. **AI Insights Generator**: Automatically generates business insights
2. **Smart Data Quality AI**: Validates and improves data quality
3. **AI Query Interface**: Converts natural language to SQL queries
4. **Predictive Analytics Engine**: Forecasts trends and patterns
5. **AI Report Generator**: Creates professional business reports

---

## Installation and Setup

### Quick Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/reddygautam98/GenETL.git
   cd GenETL
   ```

2. **Set Up Environment**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit configuration (see Configuration section below)
   notepad .env  # Windows
   nano .env     # Linux/Mac
   ```

3. **Start GenETL**
   ```bash
   # Start all services
   docker-compose up -d
   
   # Check service status
   docker-compose ps
   ```

4. **Access the Platform**
   - **Airflow UI**: http://localhost:8095 (admin/admin)
   - **Database**: localhost:5450
   - **Redis**: localhost:6390

### Configuration Guide

Edit your `.env` file to configure GenETL for your environment:

#### Essential Settings
```env
# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5450
POSTGRES_DB=genetl_warehouse
POSTGRES_USER=genetl
POSTGRES_PASSWORD=your_secure_password

# AI Configuration  
AI_MODEL_CONFIDENCE_THRESHOLD=0.7
AI_MAX_RECORDS_PER_BATCH=10000
AI_ENABLE_CACHING=True
```

#### Security Settings
```env
# Change these for production!
SECRET_KEY=your-super-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key
AIRFLOW__CORE__FERNET_KEY=your-fernet-key-here
```

### Initial Setup

1. **Create Airflow User**
   ```bash
   docker exec -it genetl-airflow-webserver airflow users create \
     --username admin --firstname Admin --lastname User \
     --role Admin --email admin@example.com --password admin
   ```

2. **Verify Installation**
   ```bash
   # Test AI features
   python test_ai_basic.py
   
   # Run demo
   python demo_ai_features.py
   ```

---

## Basic Usage

### Accessing GenETL

1. **Open Airflow UI**: Navigate to http://localhost:8095
2. **Login**: Use admin/admin (or your custom credentials)
3. **View DAGs**: See your available data pipelines

### Understanding the Interface

#### Airflow Dashboard
- **DAGs**: Your data pipelines and workflows
- **Tasks**: Individual steps in your pipelines  
- **Logs**: Execution logs and debugging information
- **Admin**: User management and system configuration

#### Key Concepts
- **DAG (Directed Acyclic Graph)**: A complete data workflow
- **Task**: A single operation (extract, transform, load, analyze)
- **Run**: An execution instance of a DAG
- **Schedule**: When and how often DAGs run

### Your First Pipeline Run

1. **Find the AI Enhanced ETL DAG**
   - Look for "ai_enhanced_etl_dag" in the DAGs list
   - This is the main pipeline with all AI features

2. **Trigger a Run**
   - Click the "Play" button next to the DAG
   - Or set it to run on a schedule

3. **Monitor Progress**
   - Click on the DAG to see task details
   - Green = Success, Red = Failed, Yellow = Running

4. **View Results**
   - Check task logs for detailed output
   - Generated reports will be in your configured output directory

---

## AI Features Guide

### 🧠 AI Insights Generator

**Purpose**: Automatically generates business intelligence insights from your data.

#### What It Does
- Analyzes pricing patterns and anomalies
- Identifies inventory optimization opportunities
- Assesses data quality and completeness
- Provides category performance analysis

#### How to Use

**Python API**:
```python
from ai_insights_generator import GenETLAIAnalyzer

# Initialize analyzer
analyzer = GenETLAIAnalyzer()

# Load your data
data = analyzer.load_warehouse_data()

# Generate pricing insights
pricing_insights = analyzer.analyze_pricing_intelligence(data)
for insight in pricing_insights:
    print(f"{insight.insight_type}: {insight.description}")
    print(f"Confidence: {insight.confidence_score}")

# Generate inventory insights  
inventory_insights = analyzer.analyze_inventory_intelligence(data)

# Generate quality insights
quality_insights = analyzer.analyze_quality_intelligence(data)
```

**Understanding Results**:
- **Insight Type**: Category of insight (pricing, inventory, quality)
- **Description**: Human-readable explanation
- **Confidence Score**: How certain the AI is (0-1 scale)
- **Recommendations**: Suggested actions

#### Example Insights
- "High-priced Electronics category shows 15% price increase trend"
- "Books category has 23 products with low stock levels"
- "Product rating data has 98.2% completeness with good quality"

### 🔍 Smart Data Quality AI

**Purpose**: Automatically validates data quality and identifies issues.

#### What It Does
- Detects statistical outliers using Z-scores and IQR methods
- Validates data completeness and consistency
- Analyzes patterns and identifies anomalies
- Provides data improvement recommendations

#### How to Use

**Python API**:
```python
from smart_data_quality_ai import SmartDataQualityAI

# Initialize quality checker
quality_ai = SmartDataQualityAI()

# Run comprehensive quality check
issues = quality_ai.comprehensive_quality_check(your_dataframe)

# Check for outliers
outliers = quality_ai.ai_detect_outliers(your_dataframe, 'price')
print(f"Found {len(outliers)} price outliers")

# Analyze data completeness
completeness = quality_ai.ai_completeness_check(your_dataframe)
print(f"Data completeness: {completeness['overall_completeness']:.1%}")
```

**Quality Metrics**:
- **Completeness**: Percentage of non-null values
- **Outliers**: Statistical anomalies that need review
- **Patterns**: Data distribution and consistency analysis
- **Recommendations**: Specific improvement suggestions

#### Interpreting Results
- **Green**: Good data quality (>90% completeness, few outliers)
- **Yellow**: Moderate issues (70-90% completeness, some outliers)
- **Red**: Significant problems (<70% completeness, many outliers)

### 💬 AI Query Interface

**Purpose**: Convert natural language questions into SQL queries and get answers.

#### What It Does
- Understands questions in plain English
- Converts to optimized SQL queries
- Executes queries and formats results
- Provides interactive chat-like experience

#### How to Use

**Python API**:
```python
from ai_query_interface import AIQueryInterface

# Initialize query interface
query_ai = AIQueryInterface()

# Ask questions in natural language
response = query_ai.process_natural_query("What is the average price by category?")
print("Answer:", response.result)
print("SQL Used:", response.sql_query)

# More example queries
queries = [
    "Show me all products with high ratings",
    "Which categories have the most expensive items?",
    "What's the total inventory value?",
    "Find products that are almost out of stock"
]

for question in queries:
    response = query_ai.process_natural_query(question)
    print(f"Q: {question}")
    print(f"A: {response.result}\n")
```

**Interactive Session**:
```python
# Start an interactive session
session = query_ai.start_interactive_session()
while True:
    question = input("Ask me about your data: ")
    if question.lower() in ['exit', 'quit']:
        break
    response = query_ai.process_natural_query(question)
    print(f"Answer: {response.result}\n")
```

#### Supported Question Types
- **Aggregations**: "What's the average price?", "How many products do we have?"
- **Filtering**: "Show me expensive products", "Find items with low stock"  
- **Comparisons**: "Which category has higher ratings?", "Compare sales by region"
- **Trends**: "Show me price trends", "What's selling best?"

### 🔮 Predictive Analytics Engine

**Purpose**: Forecast future trends and business performance using machine learning.

#### What It Does
- Predicts sales performance and trends
- Forecasts demand and inventory needs
- Analyzes market patterns
- Models business performance scenarios

#### How to Use

**Python API**:
```python
from predictive_analytics_engine import PredictiveAnalyticsEngine

# Initialize predictor
predictor = PredictiveAnalyticsEngine()

# Generate business forecast
forecast = predictor.generate_business_forecast(days=30)
print(f"30-day sales forecast: ${forecast.predicted_sales:,.2f}")
print(f"Confidence: {forecast.confidence_score:.1%}")

# Predict sales performance
sales_prediction = predictor.predict_sales_performance(
    category='Electronics',
    time_horizon=7
)
print(f"Electronics 7-day sales: {sales_prediction.prediction}")

# Get trend analysis
trends = predictor.analyze_trends(metric='revenue', period='monthly')
for trend in trends:
    print(f"{trend.period}: {trend.direction} ({trend.strength})")
```

**Understanding Predictions**:
- **Prediction Value**: Forecasted number or trend
- **Confidence Score**: How reliable the prediction is
- **Trend Direction**: Increasing, decreasing, or stable
- **Seasonal Factors**: Regular patterns in your data

#### Use Cases
- **Inventory Planning**: "How much stock will I need next month?"
- **Revenue Forecasting**: "What will my sales be this quarter?"
- **Demand Planning**: "Which products will be popular?"
- **Risk Assessment**: "What are my business risks?"

### 📊 AI Report Generator

**Purpose**: Automatically create professional business intelligence reports.

#### What It Does
- Generates executive summaries with key metrics
- Creates interactive data visualizations
- Writes AI-generated insights and recommendations
- Produces professional HTML reports

#### How to Use

**Python API**:
```python
from ai_report_generator import AIReportGenerator

# Initialize report generator
report_gen = AIReportGenerator()

# Generate comprehensive report
html_report = report_gen.compile_comprehensive_report()

# Save report
with open('business_report.html', 'w') as f:
    f.write(html_report)

# Generate specific sections
executive_summary = report_gen.generate_executive_summary()
data_insights = report_gen.generate_data_insights()
visualizations = report_gen.create_visualizations()
```

**Report Sections**:
1. **Executive Summary**: High-level business overview
2. **Key Metrics**: Important performance indicators  
3. **Data Analysis**: Detailed findings and trends
4. **Visualizations**: Charts, graphs, and dashboards
5. **Recommendations**: AI-generated action items
6. **Appendix**: Technical details and methodology

#### Customizing Reports
```python
# Custom report configuration
config = {
    'include_predictions': True,
    'time_period': '30_days',
    'categories': ['Electronics', 'Books'],
    'visualization_style': 'professional',
    'detail_level': 'comprehensive'
}

report = report_gen.compile_comprehensive_report(config=config)
```

---

## ETL Pipeline Management

### Understanding Your Pipelines

GenETL comes with a pre-built AI-enhanced ETL pipeline that includes:

1. **Data Extraction**: Load data from your sources
2. **AI Quality Check**: Validate data quality automatically
3. **Smart Transformation**: AI-powered data cleaning and enhancement
4. **Intelligent Loading**: Load data with real-time insights
5. **AI Analytics**: Generate insights and predictions
6. **Report Generation**: Create automated business reports

### Managing DAGs

#### Viewing DAG Details
1. Click on a DAG name in the Airflow UI
2. View the **Graph View** to see task dependencies
3. Check the **Tree View** for historical runs
4. Review **Logs** for detailed execution information

#### Scheduling Pipelines
```python
# In your DAG file
from airflow import DAG
from datetime import datetime, timedelta

default_args = {
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'my_custom_pipeline',
    default_args=default_args,
    schedule_interval='@daily',  # Run daily
    catchup=False
)
```

#### Common Schedule Intervals
- `@hourly`: Every hour
- `@daily`: Every day at midnight
- `@weekly`: Every Sunday
- `@monthly`: First day of each month
- `0 */6 * * *`: Every 6 hours (cron format)

### Monitoring Pipeline Health

#### Key Metrics to Watch
- **Success Rate**: Percentage of successful runs
- **Execution Time**: How long pipelines take
- **Data Quality Scores**: AI-generated quality metrics
- **Error Patterns**: Common failure points

#### Setting Up Alerts
```python
# In your DAG configuration
default_args = {
    'email_on_failure': True,
    'email_on_retry': False,
    'email': ['your-email@example.com']
}
```

### Troubleshooting Pipelines

#### Common Issues and Solutions

**Pipeline Not Starting**:
- Check DAG syntax: `python your_dag.py`
- Verify schedule and start date
- Ensure DAG is not paused

**Task Failures**:
- Review task logs in Airflow UI
- Check database connectivity
- Verify data source availability
- Look for AI model errors

**Performance Issues**:
- Monitor resource usage
- Check for large dataset processing
- Review AI batch sizes
- Consider parallel processing

---

## Data Management

### Data Sources

GenETL can work with various data sources:

#### Supported Formats
- **Databases**: PostgreSQL, MySQL, SQLite, Oracle
- **Files**: CSV, JSON, Excel, Parquet
- **APIs**: REST APIs, GraphQL
- **Cloud Storage**: AWS S3, Google Cloud, Azure
- **Streaming**: Kafka, Redis Streams

#### Connecting Data Sources

**Database Connection**:
```python
from sqlalchemy import create_engine

# Configure in your .env file
DATABASE_URL = "postgresql://user:password@localhost:5432/database"

# Connect in your code
engine = create_engine(DATABASE_URL)
data = pd.read_sql("SELECT * FROM your_table", engine)
```

**File Sources**:
```python
import pandas as pd

# CSV files
data = pd.read_csv('your_data.csv')

# JSON files  
data = pd.read_json('your_data.json')

# Excel files
data = pd.read_excel('your_data.xlsx')
```

### Data Quality Standards

GenETL's AI automatically checks for:

#### Completeness
- **Missing Values**: Null or empty fields
- **Required Fields**: Critical data points
- **Data Coverage**: Temporal and categorical coverage

#### Accuracy
- **Format Validation**: Email, phone, date formats
- **Range Checks**: Numeric bounds and constraints
- **Consistency**: Cross-field validation

#### Timeliness
- **Data Freshness**: How recent is your data
- **Update Frequency**: Regular data refresh patterns
- **Historical Gaps**: Missing time periods

### Data Transformation Best Practices

#### Clean Data Early
```python
# Use AI quality checks first
quality_issues = quality_ai.comprehensive_quality_check(raw_data)
if quality_issues['overall_score'] < 0.8:
    print("⚠️ Data quality issues detected - review before processing")
```

#### Standardize Formats
```python
# Standardize date formats
data['date'] = pd.to_datetime(data['date'])

# Normalize text data
data['category'] = data['category'].str.lower().str.strip()

# Handle missing values
data['price'].fillna(data['price'].median(), inplace=True)
```

#### Validate Business Rules
```python
# Check for logical consistency
invalid_data = data[data['price'] <= 0]
if len(invalid_data) > 0:
    print(f"⚠️ Found {len(invalid_data)} records with invalid prices")
```

---

## Monitoring and Troubleshooting

### System Health Monitoring

#### Key Metrics Dashboard

Check these metrics regularly:

**System Performance**:
- CPU and memory usage
- Database connection pool status
- Redis cache hit rates
- Disk space availability

**AI Performance**:
- Model inference times
- Prediction accuracy scores
- Data processing throughput
- Cache utilization rates

#### Health Check Commands

```bash
# Check container status
docker-compose ps

# View container logs
docker-compose logs genetl-airflow-webserver
docker-compose logs genetl-postgres
docker-compose logs genetl-redis

# Check database connectivity
docker-compose exec genetl-postgres pg_isready -U genetl

# Test Redis connection
docker-compose exec genetl-redis redis-cli ping
```

### AI Component Monitoring

#### Running System Tests
```bash
# Test all AI components
python test_ai_basic.py

# Run comprehensive demo
python demo_ai_features.py

# Check individual components
python -c "
from ai_insights_generator import GenETLAIAnalyzer
analyzer = GenETLAIAnalyzer()
print('✅ AI Insights Generator working')
"
```

#### Performance Monitoring
```python
import time
from ai_insights_generator import GenETLAIAnalyzer

# Monitor AI performance
start_time = time.time()
analyzer = GenETLAIAnalyzer()
data = analyzer.load_warehouse_data()
insights = analyzer.analyze_pricing_intelligence(data)
processing_time = time.time() - start_time

print(f"Processed {len(data)} records in {processing_time:.2f} seconds")
print(f"Generated {len(insights)} insights")
```

### Common Issues and Solutions

#### Database Connection Issues

**Problem**: "Connection refused" or timeout errors
**Solutions**:
```bash
# Check if PostgreSQL is running
docker-compose ps genetl-postgres

# Restart database container
docker-compose restart genetl-postgres

# Check database logs
docker-compose logs genetl-postgres

# Test connection manually
docker-compose exec genetl-postgres psql -U genetl -d genetl_warehouse
```

#### AI Component Errors

**Problem**: AI components not generating results
**Solutions**:
1. **Check Data Availability**:
   ```python
   # Verify data exists
   from ai_insights_generator import GenETLAIAnalyzer
   analyzer = GenETLAIAnalyzer()
   data = analyzer.load_warehouse_data()
   print(f"Loaded {len(data)} records")
   ```

2. **Verify Model Performance**:
   ```python
   # Test with minimal data
   test_data = data.head(100)  # Use small sample
   insights = analyzer.analyze_pricing_intelligence(test_data)
   ```

3. **Check Configuration**:
   ```bash
   # Verify environment variables
   echo $AI_MODEL_CONFIDENCE_THRESHOLD
   echo $AI_MAX_RECORDS_PER_BATCH
   ```

#### Performance Issues

**Problem**: Slow AI processing or timeouts
**Solutions**:

1. **Reduce Batch Size**:
   ```env
   # In .env file
   AI_MAX_RECORDS_PER_BATCH=1000  # Reduce from default 10000
   ```

2. **Enable Caching**:
   ```env
   AI_ENABLE_CACHING=True
   AI_CACHE_TTL=3600
   ```

3. **Monitor Resource Usage**:
   ```bash
   # Check system resources
   docker stats
   
   # Check memory usage
   docker-compose exec genetl-postgres free -h
   ```

#### Airflow Issues

**Problem**: DAGs not appearing or failing to run
**Solutions**:

1. **Check DAG Syntax**:
   ```bash
   # Test DAG file
   python dags/ai_enhanced_etl_dag.py
   ```

2. **Restart Airflow**:
   ```bash
   docker-compose restart genetl-airflow-webserver
   docker-compose restart genetl-airflow-scheduler
   ```

3. **Clear DAG Cache**:
   ```bash
   # In Airflow UI: Browse > DAG Runs > Delete
   # Or via command line:
   docker-compose exec genetl-airflow-webserver airflow dags delete ai_enhanced_etl_dag
   ```

### Log Analysis

#### Important Log Locations

**Airflow Logs**:
- Webserver: `logs/webserver/`
- Scheduler: `logs/scheduler/`
- Task Logs: Available in Airflow UI

**Application Logs**:
```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# In your AI components
logger = logging.getLogger(__name__)
logger.info("Processing started")
logger.debug(f"Processing {len(data)} records")
```

#### Log Analysis Tips

**Error Patterns to Look For**:
- Connection timeouts: Network or database issues
- Memory errors: Need more resources or smaller batches  
- Permission errors: File or database access issues
- Import errors: Missing dependencies

**Performance Indicators**:
- Processing times: Look for sudden increases
- Cache hit rates: Should be >80% for good performance
- Queue sizes: Should not grow continuously

---

## Best Practices

### Development Best Practices

#### Code Organization
```
your_project/
├── dags/                    # Airflow DAGs
├── plugins/                 # Custom operators
├── data/                    # Data files
├── config/                  # Configuration files
├── tests/                   # Test files
└── logs/                    # Log files
```

#### Version Control
```bash
# Initialize git repository
git init
git add .
git commit -m "Initial GenETL setup"

# Create development branch
git checkout -b development
```

#### Testing Strategy
```python
# Test AI components regularly
def test_ai_pipeline():
    """Test complete AI pipeline with sample data."""
    # Load test data
    test_data = create_sample_data()
    
    # Test each component
    analyzer = GenETLAIAnalyzer()
    insights = analyzer.analyze_pricing_intelligence(test_data)
    assert len(insights) > 0, "Should generate insights"
    
    quality_ai = SmartDataQualityAI()
    quality_report = quality_ai.comprehensive_quality_check(test_data)
    assert quality_report['overall_score'] > 0.5, "Quality should be reasonable"
```

### Data Management Best Practices

#### Data Validation
```python
# Always validate data before processing
def validate_input_data(data):
    """Validate data meets requirements."""
    required_columns = ['product_id', 'name', 'category', 'price']
    
    # Check required columns
    missing_cols = [col for col in required_columns if col not in data.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Check data types
    if not pd.api.types.is_numeric_dtype(data['price']):
        raise ValueError("Price column must be numeric")
    
    # Check for reasonable data ranges
    if data['price'].min() < 0:
        raise ValueError("Price cannot be negative")
    
    return True
```

#### Data Quality Monitoring
```python
# Set up automatic quality monitoring
def monitor_data_quality(data, threshold=0.8):
    """Monitor data quality and alert if below threshold."""
    quality_ai = SmartDataQualityAI()
    quality_report = quality_ai.comprehensive_quality_check(data)
    
    if quality_report['overall_score'] < threshold:
        # Send alert
        send_quality_alert(quality_report)
        return False
    
    return True
```

### Performance Optimization

#### Batch Processing
```python
# Process large datasets in batches
def process_large_dataset(data, batch_size=10000):
    """Process data in batches for better performance."""
    results = []
    
    for i in range(0, len(data), batch_size):
        batch = data.iloc[i:i+batch_size]
        batch_result = process_batch(batch)
        results.append(batch_result)
        
        # Log progress
        print(f"Processed batch {i//batch_size + 1}/{len(data)//batch_size + 1}")
    
    return pd.concat(results, ignore_index=True)
```

#### Caching Strategy
```python
# Implement intelligent caching
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def cached_ai_analysis(data_hash, analysis_type):
    """Cache AI analysis results."""
    if analysis_type == 'pricing':
        return analyzer.analyze_pricing_intelligence(data)
    elif analysis_type == 'quality':
        return quality_ai.comprehensive_quality_check(data)
    # ... other analysis types

# Use caching
data_hash = hashlib.md5(str(data).encode()).hexdigest()
insights = cached_ai_analysis(data_hash, 'pricing')
```

### Production Deployment

#### Environment Configuration
```env
# Production settings in .env
DEBUG=False
LOG_LEVEL=INFO
AI_MODEL_CONFIDENCE_THRESHOLD=0.8
DB_POOL_SIZE=20
ENABLE_MONITORING=True
```

#### Security Checklist
- [ ] Change all default passwords
- [ ] Enable SSL/TLS for database connections
- [ ] Set up firewall rules
- [ ] Configure backup procedures
- [ ] Enable audit logging
- [ ] Implement access controls
- [ ] Set up monitoring and alerting

#### Monitoring Setup
```python
# Production monitoring
import psutil
import time

def monitor_system_health():
    """Monitor system resources and performance."""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    metrics = {
        'cpu_percent': cpu_percent,
        'memory_percent': memory.percent,
        'disk_percent': disk.percent,
        'timestamp': time.time()
    }
    
    # Log or send to monitoring system
    log_metrics(metrics)
    
    # Alert if resources are high
    if cpu_percent > 80 or memory.percent > 80:
        send_alert(f"High resource usage: CPU {cpu_percent}%, Memory {memory.percent}%")
```

### Backup and Recovery

#### Database Backups
```bash
# Automated database backup
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="genetl_backup_$DATE.sql"

# Create backup
docker-compose exec -T genetl-postgres pg_dump -U genetl genetl_warehouse > "$BACKUP_DIR/$BACKUP_FILE"

# Compress backup
gzip "$BACKUP_DIR/$BACKUP_FILE"

# Keep only last 30 days of backups
find "$BACKUP_DIR" -name "genetl_backup_*.sql.gz" -mtime +30 -delete
```

#### Configuration Backups
```bash
# Backup configuration files
tar -czf config_backup_$(date +%Y%m%d).tar.gz \
    .env \
    docker-compose.yml \
    dags/ \
    config/
```

---

## Frequently Asked Questions

### General Questions

**Q: What makes GenETL different from other ETL tools?**
A: GenETL combines traditional ETL with AI capabilities, providing automated insights, data quality validation, natural language querying, and predictive analytics all in one platform.

**Q: Do I need to know programming to use GenETL?**
A: Basic use through the Airflow UI doesn't require programming. However, customizing AI features and creating complex pipelines benefits from Python knowledge.

**Q: Can GenETL handle big data?**
A: Yes, GenETL is designed for scalability. It uses batch processing, caching, and can be configured for large datasets. Performance depends on your infrastructure.

### Installation and Setup

**Q: What are the minimum system requirements?**
A: 
- **CPU**: 2+ cores recommended
- **RAM**: 8GB minimum, 16GB recommended  
- **Storage**: 20GB free space minimum
- **OS**: Windows 10+, macOS 10.14+, or Linux

**Q: Can I run GenETL on cloud platforms?**
A: Yes, GenETL works on AWS, Google Cloud, Azure, and other cloud platforms. Docker containers make deployment straightforward.

**Q: How do I migrate from my existing ETL system?**
A: Start by running GenETL alongside your current system. Gradually migrate pipelines and use GenETL's AI features to enhance your existing processes.

### AI Features

**Q: How accurate are the AI predictions?**
A: Accuracy depends on your data quality and quantity. GenETL provides confidence scores with all predictions. Typical accuracy ranges from 70-95% depending on the use case.

**Q: Can I train my own AI models?**
A: Currently, GenETL uses pre-built AI models optimized for business data. Custom model training is planned for future releases.

**Q: What happens if the AI makes incorrect predictions?**
A: All AI outputs include confidence scores. You can set thresholds to filter low-confidence predictions. The system learns from feedback to improve over time.

### Data Management

**Q: What data sources does GenETL support?**
A: GenETL supports databases (PostgreSQL, MySQL, etc.), files (CSV, JSON, Excel), APIs, cloud storage, and streaming sources.

**Q: How does GenETL handle sensitive data?**
A: GenETL follows security best practices including encryption, access controls, and audit logging. See the Security Guide for details.

**Q: Can I use GenETL with my existing database?**
A: Yes, GenETL can connect to existing databases. It also provides its own PostgreSQL instance for processed data and insights.

### Performance and Scaling

**Q: My AI processing is slow. How can I improve performance?**
A: Try reducing batch sizes, enabling caching, adding more CPU/memory resources, or processing smaller datasets initially.

**Q: How often should I run my pipelines?**
A: This depends on your data update frequency and business needs. Common patterns are hourly for real-time needs, daily for business reporting, or weekly for trend analysis.

**Q: Can GenETL handle real-time data processing?**
A: GenETL is primarily designed for batch processing. For real-time needs, you can run pipelines more frequently (every few minutes) or integrate with streaming platforms.

### Troubleshooting

**Q: My containers won't start. What should I check?**
A: 
1. Check if ports 5450, 6390, and 8095 are available
2. Ensure Docker has enough memory allocated (4GB+)
3. Check Docker logs: `docker-compose logs`
4. Verify your `.env` file configuration

**Q: I'm getting "Permission Denied" errors. How do I fix this?**
A: This usually indicates file or database permission issues:
1. Check file ownership: `sudo chown -R $USER:$USER .`
2. Verify database credentials in `.env` file
3. Ensure Docker has permission to access your directories

**Q: The AI features aren't generating results. What's wrong?**
A: Common causes:
1. No data in the database - run the data loading pipeline first
2. AI confidence threshold set too high - lower it in `.env`
3. Insufficient data for analysis - AI needs minimum data to generate insights

### Best Practices

**Q: How should I structure my data for best AI results?**
A: 
- Ensure consistent data formats and naming
- Maintain good data quality (>80% completeness)
- Include temporal data for trend analysis
- Provide sufficient historical data for predictions

**Q: What's the recommended backup strategy?**
A: 
- Daily automated database backups
- Weekly configuration backups
- Monthly full system backups
- Test restore procedures regularly

**Q: How do I monitor GenETL in production?**
A: 
- Use the built-in Airflow monitoring
- Set up alerts for pipeline failures
- Monitor system resources (CPU, memory, disk)
- Track AI performance metrics and confidence scores

### Integration

**Q: Can I integrate GenETL with my BI tools?**
A: Yes, GenETL's PostgreSQL database can connect to most BI tools (Tableau, Power BI, etc.). The AI Report Generator also creates standalone HTML reports.

**Q: Does GenETL have an API?**
A: GenETL components have Python APIs. REST API support is planned for future releases.

**Q: Can I customize the AI insights for my business?**
A: Yes, you can modify confidence thresholds, analysis parameters, and business rules in the configuration files and code.

---

## Getting Help and Support

### Community Resources

- **GitHub Repository**: [https://github.com/reddygautam98/GenETL](https://github.com/reddygautam98/GenETL)
- **Issues and Bug Reports**: [GitHub Issues](https://github.com/reddygautam98/GenETL/issues)
- **Discussions and Q&A**: [GitHub Discussions](https://github.com/reddygautam98/GenETL/discussions)
- **Documentation**: [GenETL Docs](https://github.com/reddygautam98/GenETL/tree/main/docs)

### Contact Support

- **Email**: [reddygautam98@gmail.com](mailto:reddygautam98@gmail.com)
- **Response Time**: Within 48 hours for bug reports
- **Security Issues**: Use same email with "SECURITY" in subject line

### Contributing

We welcome contributions! See our [Contributing Guide](../CONTRIBUTING.md) for details on:
- Reporting bugs
- Suggesting features  
- Contributing code
- Improving documentation

### Training and Consultation

For enterprise training or consultation services, contact [reddygautam98@gmail.com](mailto:reddygautam98@gmail.com).

---

*This user guide is continuously updated. Check back regularly for new features and improvements!*

**Last Updated**: October 2025 | **Version**: 2.0.0