"""
GenETL Smart Data Quality AI
Intelligent anomaly detection and automated data quality suggestions
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import re
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class QualityIssue:
    """Data class for quality issues detected by AI"""
    issue_type: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    column: str
    affected_count: int
    description: str
    ai_suggestion: str
    fix_query: str
    confidence: float

@dataclass
class DataProfile:
    """AI-generated data profiling results"""
    column_name: str
    data_type: str
    null_count: int
    unique_count: int
    duplicate_count: int
    outlier_count: int
    pattern_violations: int
    quality_score: float
    ai_recommendations: List[str]

class SmartDataQualityAI:
    """AI-Powered Data Quality Assessment and Remediation Engine"""
    
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'port': 5450,
            'database': 'genetl_warehouse',
            'user': 'genetl',
            'password': 'genetl_pass'
        }
        self.engine = None
        self.quality_rules = self._initialize_ai_rules()
    
    def get_db_connection(self):
        """Establish database connection"""
        if not self.engine:
            connection_string = f"postgresql://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"
            self.engine = create_engine(connection_string)
        return self.engine
    
    def _initialize_ai_rules(self) -> Dict[str, Any]:
        """Initialize AI-powered data quality rules"""
        return {
            'price_rules': {
                'min_value': 0.01,
                'max_value': 50000.00,
                'outlier_threshold': 3,  # Standard deviations
                'decimal_places': 2
            },
            'rating_rules': {
                'min_value': 1.0,
                'max_value': 5.0,
                'decimal_places': 1
            },
            'text_rules': {
                'min_length': 2,
                'max_length': 255,
                'special_chars_threshold': 0.3
            },
            'id_rules': {
                'format_pattern': r'^[A-Z0-9]{6,12}$',
                'uniqueness_required': True
            },
            'stock_rules': {
                'min_value': 0,
                'max_value': 10000,
                'negative_alert': True
            }
        }
    
    def load_data_for_analysis(self, table_name: str = 'warehouse.products') -> pd.DataFrame:
        """Load data for quality analysis"""
        try:
            engine = self.get_db_connection()
            query = f"SELECT * FROM {table_name} LIMIT 10000"  # Limit for performance
            df = pd.read_sql(query, engine)
            logger.info(f"Loaded {len(df)} records from {table_name} for quality analysis")
            return df
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return pd.DataFrame()
    
    def ai_detect_outliers(self, df: pd.DataFrame, column: str, method: str = 'iqr') -> Tuple[List[int], float]:
        """AI-powered outlier detection using multiple algorithms"""
        try:
            if column not in df.columns or df[column].dtype not in ['int64', 'float64']:
                return [], 0.0
            
            data = df[column].dropna()
            if len(data) == 0:
                return [], 0.0
            
            outliers = []
            confidence = 0.0
            
            if method == 'iqr':
                Q1 = data.quantile(0.25)
                Q3 = data.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)].index.tolist()
                confidence = 0.85
                
            elif method == 'zscore':
                z_scores = np.abs(stats.zscore(data))
                threshold = self.quality_rules.get('price_rules', {}).get('outlier_threshold', 3)
                outliers = df[z_scores > threshold].index.tolist()
                confidence = 0.90
                
            elif method == 'modified_zscore':
                median = np.median(data)
                mad = np.median(np.abs(data - median))
                modified_z_scores = 0.6745 * (data - median) / mad
                outliers = df[np.abs(modified_z_scores) > 3.5].index.tolist()
                confidence = 0.92
            
            return outliers, confidence
            
        except Exception as e:
            logger.error(f"Error in outlier detection: {e}")
            return [], 0.0
    
    def ai_pattern_analysis(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """AI-powered pattern recognition and validation"""
        try:
            if column not in df.columns:
                return {}
            
            data = df[column].dropna().astype(str)
            if len(data) == 0:
                return {}
            
            patterns = {}
            
            # Analyze common patterns
            pattern_counts = {}
            for value in data:
                # Extract pattern (letters, numbers, special chars)
                pattern = re.sub(r'[A-Za-z]', 'A', value)
                pattern = re.sub(r'[0-9]', '9', pattern)
                pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
            
            # Find dominant pattern
            if pattern_counts:
                dominant_pattern = max(pattern_counts, key=pattern_counts.get)
                pattern_compliance = pattern_counts[dominant_pattern] / len(data)
                
                patterns = {
                    'dominant_pattern': dominant_pattern,
                    'compliance_rate': pattern_compliance,
                    'total_patterns': len(pattern_counts),
                    'violations': len(data) - pattern_counts[dominant_pattern],
                    'pattern_distribution': dict(sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)[:5])
                }
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error in pattern analysis: {e}")
            return {}
    
    def ai_completeness_check(self, df: pd.DataFrame) -> List[QualityIssue]:
        """AI-powered completeness analysis"""
        issues = []
        
        try:
            for column in df.columns:
                null_count = df[column].isnull().sum()
                null_percentage = (null_count / len(df)) * 100
                
                if null_percentage > 0:
                    severity = 'CRITICAL' if null_percentage > 10 else 'HIGH' if null_percentage > 5 else 'MEDIUM'
                    
                    # AI suggestion based on column type and context
                    if 'id' in column.lower():
                        suggestion = "IDs should never be null. Implement auto-generation or data source validation."
                    elif 'price' in column.lower():
                        suggestion = "Missing prices impact revenue calculations. Set default values or flag for manual review."
                    elif 'rating' in column.lower():
                        suggestion = "Missing ratings affect quality metrics. Consider default rating or exclude from averages."
                    else:
                        suggestion = f"Investigate data source for {column}. Consider default values or data imputation."
                    
                    issues.append(QualityIssue(
                        issue_type='COMPLETENESS',
                        severity=severity,
                        column=column,
                        affected_count=null_count,
                        description=f"{null_percentage:.1f}% of {column} values are missing ({null_count} records)",
                        ai_suggestion=suggestion,
                        fix_query=f"-- Update NULL values in {column}\nUPDATE warehouse.products SET {column} = 'DEFAULT_VALUE' WHERE {column} IS NULL;",
                        confidence=0.95
                    ))
            
            return issues
            
        except Exception as e:
            logger.error(f"Error in completeness check: {e}")
            return []
    
    def ai_consistency_check(self, df: pd.DataFrame) -> List[QualityIssue]:
        """AI-powered consistency analysis"""
        issues = []
        
        try:
            # Price consistency check
            if 'price' in df.columns:
                price_outliers, confidence = self.ai_detect_outliers(df, 'price', 'modified_zscore')
                if len(price_outliers) > 0:
                    outlier_percentage = (len(price_outliers) / len(df)) * 100
                    severity = 'HIGH' if outlier_percentage > 5 else 'MEDIUM'
                    
                    issues.append(QualityIssue(
                        issue_type='CONSISTENCY',
                        severity=severity,
                        column='price',
                        affected_count=len(price_outliers),
                        description=f"Detected {len(price_outliers)} price outliers ({outlier_percentage:.1f}% of data)",
                        ai_suggestion="Review pricing strategy. Outliers may indicate data entry errors or premium products requiring validation.",
                        fix_query="-- Review price outliers\nSELECT product_id, product_name, price FROM warehouse.products WHERE price > (SELECT AVG(price) + 3*STDDEV(price) FROM warehouse.products);",
                        confidence=confidence
                    ))
            
            # Rating consistency check  
            if 'rating' in df.columns:
                invalid_ratings = df[(df['rating'] < 1.0) | (df['rating'] > 5.0)].shape[0]
                if invalid_ratings > 0:
                    issues.append(QualityIssue(
                        issue_type='CONSISTENCY',
                        severity='HIGH',
                        column='rating',
                        affected_count=invalid_ratings,
                        description=f"Found {invalid_ratings} ratings outside valid range (1.0-5.0)",
                        ai_suggestion="Ratings must be between 1.0-5.0. Implement data validation at source or correct invalid values.",
                        fix_query="-- Fix invalid ratings\nUPDATE warehouse.products SET rating = CASE WHEN rating < 1.0 THEN 1.0 WHEN rating > 5.0 THEN 5.0 ELSE rating END;",
                        confidence=0.98
                    ))
            
            return issues
            
        except Exception as e:
            logger.error(f"Error in consistency check: {e}")
            return []
    
    def ai_uniqueness_check(self, df: pd.DataFrame) -> List[QualityIssue]:
        """AI-powered uniqueness validation"""
        issues = []
        
        try:
            # Check ID columns for duplicates
            id_columns = [col for col in df.columns if 'id' in col.lower()]
            
            for column in id_columns:
                duplicates = df[df.duplicated(subset=[column], keep=False)]
                if len(duplicates) > 0:
                    unique_dupes = len(duplicates[column].unique())
                    
                    issues.append(QualityIssue(
                        issue_type='UNIQUENESS',
                        severity='CRITICAL',
                        column=column,
                        affected_count=len(duplicates),
                        description=f"Found {unique_dupes} duplicate values in {column} affecting {len(duplicates)} records",
                        ai_suggestion=f"IDs must be unique. Implement auto-increment or UUID generation. Current duplicates need resolution.",
                        fix_query=f"-- Find duplicate IDs\nSELECT {column}, COUNT(*) as duplicate_count FROM warehouse.products GROUP BY {column} HAVING COUNT(*) > 1;",
                        confidence=0.99
                    ))
            
            return issues
            
        except Exception as e:
            logger.error(f"Error in uniqueness check: {e}")
            return []
    
    def ai_format_validation(self, df: pd.DataFrame) -> List[QualityIssue]:
        """AI-powered format and pattern validation"""
        issues = []
        
        try:
            # Product ID format validation
            if 'product_id' in df.columns:
                pattern_analysis = self.ai_pattern_analysis(df, 'product_id')
                if pattern_analysis and pattern_analysis.get('compliance_rate', 1.0) < 0.9:
                    violations = pattern_analysis.get('violations', 0)
                    
                    issues.append(QualityIssue(
                        issue_type='FORMAT',
                        severity='HIGH',
                        column='product_id',
                        affected_count=violations,
                        description=f"Inconsistent product_id format. {violations} records don't match dominant pattern",
                        ai_suggestion="Standardize product ID format. Implement consistent naming convention and validation rules.",
                        fix_query="-- Review product ID patterns\nSELECT product_id, LENGTH(product_id), product_name FROM warehouse.products WHERE LENGTH(product_id) NOT BETWEEN 6 AND 12;",
                        confidence=0.87
                    ))
            
            # Email format validation (if email column exists)
            email_columns = [col for col in df.columns if 'email' in col.lower()]
            for column in email_columns:
                if column in df.columns:
                    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                    invalid_emails = df[~df[column].astype(str).str.match(email_pattern, na=False)].shape[0]
                    
                    if invalid_emails > 0:
                        issues.append(QualityIssue(
                            issue_type='FORMAT',
                            severity='MEDIUM',
                            column=column,
                            affected_count=invalid_emails,
                            description=f"Found {invalid_emails} invalid email formats in {column}",
                            ai_suggestion="Validate email formats at data entry. Implement regex validation and user feedback.",
                            fix_query=f"-- Find invalid emails\nSELECT {column} FROM warehouse.products WHERE {column} !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{{2,}}$';",
                            confidence=0.95
                        ))
            
            return issues
            
        except Exception as e:
            logger.error(f"Error in format validation: {e}")
            return []
    
    def generate_data_profile(self, df: pd.DataFrame) -> List[DataProfile]:
        """Generate AI-powered data profiling"""
        profiles = []
        
        try:
            for column in df.columns:
                # Basic statistics
                null_count = df[column].isnull().sum()
                unique_count = df[column].nunique()
                duplicate_count = len(df) - unique_count
                
                # Detect outliers for numeric columns
                outlier_count = 0
                if df[column].dtype in ['int64', 'float64']:
                    outliers, _ = self.ai_detect_outliers(df, column)
                    outlier_count = len(outliers)
                
                # Pattern violations
                pattern_violations = 0
                if df[column].dtype == 'object':
                    pattern_analysis = self.ai_pattern_analysis(df, column)
                    pattern_violations = pattern_analysis.get('violations', 0)
                
                # Calculate quality score (0-100)
                completeness_score = ((len(df) - null_count) / len(df)) * 100
                uniqueness_score = (unique_count / len(df)) * 100 if 'id' in column.lower() else 100
                consistency_score = ((len(df) - outlier_count) / len(df)) * 100
                format_score = ((len(df) - pattern_violations) / len(df)) * 100
                
                quality_score = (completeness_score + uniqueness_score + consistency_score + format_score) / 4
                
                # AI recommendations
                recommendations = []
                if completeness_score < 95:
                    recommendations.append(f"Improve data completeness (currently {completeness_score:.1f}%)")
                if consistency_score < 90:
                    recommendations.append(f"Address data consistency issues ({outlier_count} outliers detected)")
                if format_score < 85:
                    recommendations.append(f"Standardize data formats ({pattern_violations} format violations)")
                
                profiles.append(DataProfile(
                    column_name=column,
                    data_type=str(df[column].dtype),
                    null_count=null_count,
                    unique_count=unique_count,
                    duplicate_count=duplicate_count,
                    outlier_count=outlier_count,
                    pattern_violations=pattern_violations,
                    quality_score=round(quality_score, 2),
                    ai_recommendations=recommendations
                ))
            
            return profiles
            
        except Exception as e:
            logger.error(f"Error generating data profile: {e}")
            return []
    
    def run_comprehensive_quality_assessment(self) -> Dict[str, Any]:
        """Execute complete AI-powered data quality assessment"""
        logger.info("🤖 Starting AI-powered data quality assessment...")
        
        # Load data
        df = self.load_data_for_analysis()
        if df.empty:
            return {"error": "No data available for quality assessment"}
        
        # Run all quality checks
        all_issues = []
        all_issues.extend(self.ai_completeness_check(df))
        all_issues.extend(self.ai_consistency_check(df))
        all_issues.extend(self.ai_uniqueness_check(df))
        all_issues.extend(self.ai_format_validation(df))
        
        # Generate data profiles
        data_profiles = self.generate_data_profile(df)
        
        # Calculate overall quality score
        if data_profiles:
            overall_quality_score = np.mean([profile.quality_score for profile in data_profiles])
        else:
            overall_quality_score = 0
        
        # Categorize issues by severity
        critical_issues = [issue for issue in all_issues if issue.severity == 'CRITICAL']
        high_issues = [issue for issue in all_issues if issue.severity == 'HIGH']
        medium_issues = [issue for issue in all_issues if issue.severity == 'MEDIUM']
        
        # Generate AI recommendations
        priority_actions = []
        if critical_issues:
            priority_actions.append("🚨 Address CRITICAL data integrity issues immediately")
        if high_issues:
            priority_actions.append("⚠️ Resolve HIGH priority data quality problems")
        if medium_issues:
            priority_actions.append("📊 Improve MEDIUM priority data consistency")
        if overall_quality_score > 90:
            priority_actions.append("✅ Maintain excellent data quality standards")
        
        results = {
            "assessment_timestamp": datetime.now().isoformat(),
            "records_analyzed": len(df),
            "overall_quality_score": round(overall_quality_score, 2),
            "total_issues_found": len(all_issues),
            "issue_breakdown": {
                "critical": len(critical_issues),
                "high": len(high_issues),  
                "medium": len(medium_issues),
                "low": len([issue for issue in all_issues if issue.severity == 'LOW'])
            },
            "quality_grade": self._calculate_quality_grade(overall_quality_score),
            "priority_actions": priority_actions,
            "data_profiles": [
                {
                    "column": profile.column_name,
                    "data_type": profile.data_type,
                    "quality_score": profile.quality_score,
                    "null_count": profile.null_count,
                    "unique_count": profile.unique_count,
                    "outlier_count": profile.outlier_count,
                    "recommendations": profile.ai_recommendations
                }
                for profile in data_profiles
            ],
            "quality_issues": [
                {
                    "type": issue.issue_type,
                    "severity": issue.severity,
                    "column": issue.column,
                    "affected_count": issue.affected_count,
                    "description": issue.description,
                    "ai_suggestion": issue.ai_suggestion,
                    "fix_query": issue.fix_query,
                    "confidence": issue.confidence
                }
                for issue in all_issues
            ]
        }
        
        logger.info(f"✅ Quality assessment complete! Overall score: {overall_quality_score:.1f}%")
        return results
    
    def _calculate_quality_grade(self, score: float) -> str:
        """Calculate letter grade based on quality score"""
        if score >= 95:
            return "A+ (Excellent)"
        elif score >= 90:
            return "A (Very Good)"
        elif score >= 85:
            return "B+ (Good)"
        elif score >= 80:
            return "B (Fair)"
        elif score >= 75:
            return "C+ (Needs Improvement)"
        elif score >= 70:
            return "C (Poor)"
        else:
            return "D (Critical Issues)"

def main():
    """Main execution function"""
    print("🤖 GenETL Smart Data Quality AI")
    print("=" * 50)
    
    # Initialize AI quality checker
    quality_ai = SmartDataQualityAI()
    
    # Run comprehensive assessment
    results = quality_ai.run_comprehensive_quality_assessment()
    
    if "error" in results:
        print(f"❌ Assessment failed: {results['error']}")
        return
    
    # Display results
    print(f"\n📊 DATA QUALITY REPORT")
    print(f"Assessment Date: {results['assessment_timestamp']}")
    print(f"Records Analyzed: {results['records_analyzed']:,}")
    print(f"Overall Quality Score: {results['overall_quality_score']}% ({results['quality_grade']})")
    
    print(f"\n🚨 ISSUE SUMMARY:")
    print(f"   Critical: {results['issue_breakdown']['critical']}")
    print(f"   High:     {results['issue_breakdown']['high']}")
    print(f"   Medium:   {results['issue_breakdown']['medium']}")
    print(f"   Low:      {results['issue_breakdown']['low']}")
    
    print(f"\n🎯 PRIORITY ACTIONS:")
    for action in results['priority_actions']:
        print(f"   • {action}")
    
    print(f"\n📋 DETAILED ISSUES:")
    print("-" * 80)
    for i, issue in enumerate(results['quality_issues'], 1):
        print(f"{i}. [{issue['severity']}] {issue['description']}")
        print(f"   Column: {issue['column']} | Affected: {issue['affected_count']} records")
        print(f"   💡 AI Suggestion: {issue['ai_suggestion']}")
        print(f"   🔧 Confidence: {issue['confidence']:.0%}")
        print()
    
    print("🎉 AI Quality Assessment Complete!")

if __name__ == "__main__":
    main()