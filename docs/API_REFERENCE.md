# API Reference

## GenETL API Documentation

### Core Components

#### Data Loading
- `load_data.py` - Data ingestion and loading utilities
- `analyze_data.py` - Data analysis and transformation functions
- `create_dashboard.py` - Dashboard generation and visualization

#### AI Components
- `ai_insights_generator.py` - AI-powered insights and recommendations
- `smart_data_quality_ai.py` - AI-driven data quality assessment
- `predictive_analytics_engine.py` - Predictive modeling and analytics

### Database Schema

#### Products Table
```sql
CREATE TABLE warehouse.products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    category VARCHAR(100),
    price DECIMAL(10,2),
    rating DECIMAL(3,2),
    stock_quantity INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_HOST` | Database host | localhost |
| `POSTGRES_PORT` | Database port | 5432 |
| `POSTGRES_DB` | Database name | postgres |
| `POSTGRES_USER` | Database user | postgres |
| `POSTGRES_PASSWORD` | Database password | - |
| `REDIS_HOST` | Redis host | localhost |
| `REDIS_PORT` | Redis port | 6379 |

### Usage Examples

#### Basic Data Loading
```python
from load_data import load_sample_data
from analyze_data import analyze_products

# Load data
data = load_sample_data()

# Analyze
insights = analyze_products(data)
```

#### AI Insights Generation
```python
from ai_insights_generator import generate_insights

# Generate AI insights
insights = generate_insights(data_source="products")
```