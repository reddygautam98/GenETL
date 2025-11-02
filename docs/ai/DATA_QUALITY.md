# Data Quality AI

## Smart Data Quality Assessment

### Overview
AI-powered data quality assessment provides intelligent validation and quality scoring for your datasets.

### Quality Metrics

#### Completeness
- Missing value detection
- Data coverage analysis
- Field population rates

#### Accuracy
- Data type validation
- Range and constraint checking
- Pattern matching verification

#### Consistency
- Cross-field validation
- Referential integrity checks
- Format standardization

#### Timeliness
- Data freshness assessment
- Update frequency analysis
- Staleness detection

### Usage

```python
from smart_data_quality_ai import SmartDataQualityAI

# Initialize the quality AI
quality_ai = SmartDataQualityAI()

# Assess data quality
quality_report = quality_ai.assess_quality(
    dataframe=df,
    rules="auto",  # or custom rules
    threshold=0.85
)

# Get quality score
score = quality_report.overall_score
```

### Quality Report Structure

```json
{
    "overall_score": 85.2,
    "dimensions": {
        "completeness": 90.5,
        "accuracy": 88.0,
        "consistency": 82.1,
        "timeliness": 80.0
    },
    "issues": [
        {
            "type": "missing_values",
            "field": "email",
            "severity": "medium",
            "count": 15
        }
    ],
    "recommendations": [
        "Consider data imputation for missing email values",
        "Standardize phone number formats"
    ]
}
```

### Configuration

```yaml
quality_config:
  rules:
    completeness_threshold: 0.95
    accuracy_threshold: 0.90
    consistency_threshold: 0.85
  
  validation_rules:
    email: "regex:^[\\w\\.-]+@[\\w\\.-]+\\.[a-zA-Z]{2,}$"
    phone: "format:phone"
    date: "range:1900-01-01,today"
```