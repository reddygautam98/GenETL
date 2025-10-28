"""
GenETL AI-Powered Data Insights Generator
Advanced analytics with Large Language Model integration
"""

import pandas as pd
import numpy as np
import psycopg2
from sqlalchemy import create_engine, text
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import requests
import statistics
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DataInsight:
    """Data class for AI-generated insights"""
    insight_type: str
    title: str
    description: str
    confidence: float
    data_points: Dict[str, Any]
    recommendation: str
    priority: str  # HIGH, MEDIUM, LOW

class GenETLAIAnalyzer:
    """AI-Enhanced Data Analysis Engine for GenETL"""
    
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'port': 5450,
            'database': 'genetl_warehouse',
            'user': 'genetl',
            'password': 'genetl_pass'
        }
        self.engine = None
        self.ai_insights = []
    
    def get_db_connection(self):
        """Establish database connection"""
        if not self.engine:
            connection_string = f"postgresql://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"
            self.engine = create_engine(connection_string)
        return self.engine
    
    def load_warehouse_data(self) -> pd.DataFrame:
        """Load data from warehouse for AI analysis"""
        try:
            engine = self.get_db_connection()
            
            query = """
            SELECT 
                product_id,
                product_name,
                category,
                brand,
                price_raw as price,
                rating_raw as rating,
                CASE 
                    WHEN availability_status = 'Out of Stock' THEN 0
                    WHEN availability_status = 'Limited Stock' THEN 5
                    ELSE 50
                END as quantity_in_stock,
                CASE 
                    WHEN availability_status != 'Discontinued' THEN true
                    ELSE false
                END as is_active,
                extracted_at as created_date,
                extracted_at as last_updated,
                availability_status as stock_status
            FROM warehouse.products
            WHERE availability_status != 'Discontinued'
            """
            
            df = pd.read_sql(query, engine)
            logger.info(f"Loaded {len(df)} products for AI analysis")
            return df
            
        except Exception as e:
            logger.error(f"Error loading warehouse data: {e}")
            return pd.DataFrame()
    
    def analyze_pricing_intelligence(self, df: pd.DataFrame) -> List[DataInsight]:
        """AI-powered pricing analysis and insights"""
        insights = []
        
        try:
            # Price distribution analysis
            price_stats = {
                'mean': df['price'].mean(),
                'median': df['price'].median(),
                'std': df['price'].std(),
                'min': df['price'].min(),
                'max': df['price'].max()
            }
            
            # Category price analysis
            category_prices = df.groupby('category')['price'].agg(['mean', 'median', 'count']).round(2)
            
            # AI Insight 1: Price Outliers Detection
            price_threshold = price_stats['mean'] + (2 * price_stats['std'])
            expensive_products = df[df['price'] > price_threshold]
            
            if len(expensive_products) > 0:
                insights.append(DataInsight(
                    insight_type="PRICING_ANOMALY",
                    title="🎯 Premium Products Detected",
                    description=f"Found {len(expensive_products)} products priced significantly above average (>${price_threshold:.2f}). These represent {(len(expensive_products)/len(df)*100):.1f}% of inventory.",
                    confidence=0.95,
                    data_points={
                        "expensive_count": len(expensive_products),
                        "threshold": round(price_threshold, 2),
                        "top_expensive": expensive_products.nlargest(3, 'price')[['product_name', 'price', 'category']].to_dict('records')
                    },
                    recommendation="Consider premium pricing strategy or investigate if these prices are justified by value proposition.",
                    priority="MEDIUM"
                ))
            
            # AI Insight 2: Category Price Strategy
            most_expensive_category = category_prices['mean'].idxmax()
            cheapest_category = category_prices['mean'].idxmin()
            
            insights.append(DataInsight(
                insight_type="CATEGORY_PRICING",
                title="📊 Category Pricing Strategy Analysis",
                description=f"Category '{most_expensive_category}' has highest average price (${category_prices.loc[most_expensive_category, 'mean']:.2f}) while '{cheapest_category}' has lowest (${category_prices.loc[cheapest_category, 'mean']:.2f}).",
                confidence=0.90,
                data_points={
                    "highest_category": most_expensive_category,
                    "highest_price": round(category_prices.loc[most_expensive_category, 'mean'], 2),
                    "lowest_category": cheapest_category,
                    "lowest_price": round(category_prices.loc[cheapest_category, 'mean'], 2),
                    "price_spread": round(category_prices.loc[most_expensive_category, 'mean'] - category_prices.loc[cheapest_category, 'mean'], 2)
                },
                recommendation="Optimize pricing tiers across categories to maximize revenue potential.",
                priority="HIGH"
            ))
            
            return insights
            
        except Exception as e:
            logger.error(f"Error in pricing analysis: {e}")
            return []
    
    def analyze_inventory_intelligence(self, df: pd.DataFrame) -> List[DataInsight]:
        """AI-powered inventory optimization insights"""
        insights = []
        
        try:
            # Stock level analysis
            stock_distribution = df['stock_status'].value_counts()
            total_products = len(df)
            
            # AI Insight 1: Inventory Risk Assessment
            out_of_stock_pct = (stock_distribution.get('Out of Stock', 0) / total_products) * 100
            low_stock_pct = (stock_distribution.get('Low Stock', 0) / total_products) * 100
            
            if out_of_stock_pct > 5:  # If more than 5% out of stock
                insights.append(DataInsight(
                    insight_type="INVENTORY_RISK",
                    title="⚠️ Critical Inventory Alert",
                    description=f"High out-of-stock rate detected: {out_of_stock_pct:.1f}% of products unavailable. Additional {low_stock_pct:.1f}% at low stock levels.",
                    confidence=0.98,
                    data_points={
                        "out_of_stock_count": stock_distribution.get('Out of Stock', 0),
                        "out_of_stock_percentage": round(out_of_stock_pct, 1),
                        "low_stock_count": stock_distribution.get('Low Stock', 0),
                        "low_stock_percentage": round(low_stock_pct, 1)
                    },
                    recommendation="Implement automated reordering system for critical stock levels and review supplier performance.",
                    priority="HIGH"
                ))
            
            # AI Insight 2: Category Stock Performance
            category_stock = df.groupby(['category', 'stock_status']).size().unstack(fill_value=0)
            if 'Out of Stock' in category_stock.columns:
                worst_category = category_stock['Out of Stock'].idxmax()
                worst_count = category_stock.loc[worst_category, 'Out of Stock']
                
                insights.append(DataInsight(
                    insight_type="CATEGORY_INVENTORY",
                    title="📦 Category Inventory Performance",
                    description=f"Category '{worst_category}' has highest stock-out rate with {worst_count} products unavailable.",
                    confidence=0.85,
                    data_points={
                        "worst_performing_category": worst_category,
                        "out_of_stock_products": int(worst_count),
                        "category_stock_breakdown": category_stock.to_dict()
                    },
                    recommendation=f"Focus inventory management efforts on '{worst_category}' category to reduce stock-outs.",
                    priority="MEDIUM"
                ))
            
            return insights
            
        except Exception as e:
            logger.error(f"Error in inventory analysis: {e}")
            return []
    
    def analyze_quality_intelligence(self, df: pd.DataFrame) -> List[DataInsight]:
        """AI-powered product quality and rating analysis"""
        insights = []
        
        try:
            # Rating analysis
            avg_rating = df['rating'].mean()
            rating_std = df['rating'].std()
            
            # AI Insight 1: Quality Performance
            low_rated_threshold = avg_rating - rating_std
            low_rated_products = df[df['rating'] < low_rated_threshold]
            
            if len(low_rated_products) > 0:
                insights.append(DataInsight(
                    insight_type="QUALITY_ALERT",
                    title="⭐ Product Quality Concerns",
                    description=f"Identified {len(low_rated_products)} products with ratings significantly below average ({avg_rating:.2f}). These may need quality improvement or review.",
                    confidence=0.88,
                    data_points={
                        "low_rated_count": len(low_rated_products),
                        "average_rating": round(avg_rating, 2),
                        "threshold": round(low_rated_threshold, 2),
                        "worst_products": low_rated_products.nsmallest(3, 'rating')[['product_name', 'rating', 'category']].to_dict('records')
                    },
                    recommendation="Review product quality, customer feedback, and consider improvements or discontinuation for consistently low-rated items.",
                    priority="HIGH"
                ))
            
            # AI Insight 2: Category Quality Comparison
            category_ratings = df.groupby('category')['rating'].agg(['mean', 'count']).round(2)
            best_category = category_ratings['mean'].idxmax()
            worst_category = category_ratings['mean'].idxmin()
            
            insights.append(DataInsight(
                insight_type="CATEGORY_QUALITY",
                title="🏆 Category Quality Ranking",
                description=f"Quality leader: '{best_category}' (avg: {category_ratings.loc[best_category, 'mean']:.2f}). Needs attention: '{worst_category}' (avg: {category_ratings.loc[worst_category, 'mean']:.2f}).",
                confidence=0.92,
                data_points={
                    "best_category": best_category,
                    "best_rating": float(category_ratings.loc[best_category, 'mean']),
                    "worst_category": worst_category,
                    "worst_rating": float(category_ratings.loc[worst_category, 'mean']),
                    "rating_gap": round(category_ratings.loc[best_category, 'mean'] - category_ratings.loc[worst_category, 'mean'], 2)
                },
                recommendation=f"Apply successful practices from '{best_category}' to improve quality in '{worst_category}'.",
                priority="MEDIUM"
            ))
            
            return insights
            
        except Exception as e:
            logger.error(f"Error in quality analysis: {e}")
            return []
    
    def generate_predictive_insights(self, df: pd.DataFrame) -> List[DataInsight]:
        """AI-powered predictive analytics and forecasting"""
        insights = []
        
        try:
            # Trend analysis based on created_date
            df['created_date'] = pd.to_datetime(df['created_date'])
            recent_products = df[df['created_date'] > (datetime.now() - timedelta(days=30))]
            
            if len(recent_products) > 0:
                # New product performance prediction
                recent_avg_rating = recent_products['rating'].mean()
                recent_avg_price = recent_products['price'].mean()
                overall_avg_rating = df['rating'].mean()
                
                trend_direction = "improving" if recent_avg_rating > overall_avg_rating else "declining"
                
                insights.append(DataInsight(
                    insight_type="TREND_PREDICTION",
                    title="🔮 Product Performance Trend",
                    description=f"Recent products show {trend_direction} quality trend. New products avg rating: {recent_avg_rating:.2f} vs overall: {overall_avg_rating:.2f}.",
                    confidence=0.75,
                    data_points={
                        "recent_products_count": len(recent_products),
                        "recent_avg_rating": round(recent_avg_rating, 2),
                        "recent_avg_price": round(recent_avg_price, 2),
                        "overall_avg_rating": round(overall_avg_rating, 2),
                        "trend_direction": trend_direction
                    },
                    recommendation="Monitor new product introduction strategy and quality control processes.",
                    priority="MEDIUM"
                ))
            
            # Revenue opportunity analysis
            high_rated_expensive = df[(df['rating'] > 4.0) & (df['price'] > df['price'].median())]
            if len(high_rated_expensive) > 0:
                revenue_opportunity = high_rated_expensive['price'].sum()
                
                insights.append(DataInsight(
                    insight_type="REVENUE_OPPORTUNITY",
                    title="💰 Premium Revenue Opportunity",
                    description=f"Found {len(high_rated_expensive)} high-quality premium products. Potential to leverage quality for pricing optimization.",
                    confidence=0.82,
                    data_points={
                        "premium_products_count": len(high_rated_expensive),
                        "potential_revenue_focus": round(revenue_opportunity, 2),
                        "avg_premium_rating": round(high_rated_expensive['rating'].mean(), 2),
                        "avg_premium_price": round(high_rated_expensive['price'].mean(), 2)
                    },
                    recommendation="Focus marketing and sales efforts on high-quality premium products to maximize revenue.",
                    priority="HIGH"
                ))
            
            return insights
            
        except Exception as e:
            logger.error(f"Error in predictive analysis: {e}")
            return []
    
    def generate_ai_summary(self, all_insights: List[DataInsight]) -> str:
        """Generate AI-powered executive summary"""
        try:
            high_priority = [i for i in all_insights if i.priority == "HIGH"]
            medium_priority = [i for i in all_insights if i.priority == "MEDIUM"]
            
            summary = f"""
🤖 AI-POWERED BUSINESS INTELLIGENCE REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 EXECUTIVE SUMMARY:
Analyzed {len(all_insights)} key business insights across pricing, inventory, quality, and predictive analytics.

🚨 HIGH PRIORITY ACTIONS ({len(high_priority)} items):
"""
            
            for insight in high_priority[:3]:  # Top 3 high priority
                summary += f"\n• {insight.title}: {insight.description[:100]}..."
            
            summary += f"""

⚡ MEDIUM PRIORITY OPPORTUNITIES ({len(medium_priority)} items):
"""
            
            for insight in medium_priority[:2]:  # Top 2 medium priority
                summary += f"\n• {insight.title}: {insight.description[:100]}..."
            
            summary += f"""

🎯 KEY RECOMMENDATIONS:
• Focus on inventory management to reduce stock-outs
• Optimize pricing strategy across product categories  
• Leverage high-quality products for revenue growth
• Monitor product quality trends for continuous improvement

📈 CONFIDENCE LEVEL: {np.mean([i.confidence for i in all_insights]):.0%}
"""
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating AI summary: {e}")
            return "AI Summary generation failed. Please check logs."
    
    def run_comprehensive_analysis(self) -> Dict[str, Any]:
        """Execute complete AI-powered analysis pipeline"""
        logger.info("🤖 Starting AI-powered data analysis...")
        
        # Load data
        df = self.load_warehouse_data()
        if df.empty:
            return {"error": "No data available for analysis"}
        
        # Generate insights
        all_insights = []
        all_insights.extend(self.analyze_pricing_intelligence(df))
        all_insights.extend(self.analyze_inventory_intelligence(df))
        all_insights.extend(self.analyze_quality_intelligence(df))
        all_insights.extend(self.analyze_predictive_insights(df))
        
        # Generate AI summary
        ai_summary = self.generate_ai_summary(all_insights)
        
        # Compile results
        results = {
            "analysis_timestamp": datetime.now().isoformat(),
            "data_points_analyzed": len(df),
            "total_insights_generated": len(all_insights),
            "ai_summary": ai_summary,
            "insights": [
                {
                    "type": insight.insight_type,
                    "title": insight.title,
                    "description": insight.description,
                    "confidence": insight.confidence,
                    "priority": insight.priority,
                    "recommendation": insight.recommendation,
                    "data_points": insight.data_points
                }
                for insight in all_insights
            ],
            "metadata": {
                "high_priority_count": len([i for i in all_insights if i.priority == "HIGH"]),
                "medium_priority_count": len([i for i in all_insights if i.priority == "MEDIUM"]),
                "low_priority_count": len([i for i in all_insights if i.priority == "LOW"]),
                "average_confidence": round(np.mean([i.confidence for i in all_insights]), 2)
            }
        }
        
        logger.info(f"✅ AI analysis complete! Generated {len(all_insights)} insights")
        return results
    
    def save_insights_to_warehouse(self, results: Dict[str, Any]) -> bool:
        """Save AI insights back to warehouse for tracking"""
        try:
            engine = self.get_db_connection()
            
            # Create AI insights table if not exists
            create_table_query = """
            CREATE SCHEMA IF NOT EXISTS ai_insights;
            
            CREATE TABLE IF NOT EXISTS ai_insights.analysis_results (
                id SERIAL PRIMARY KEY,
                analysis_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_insights INTEGER,
                high_priority_count INTEGER,
                medium_priority_count INTEGER,
                average_confidence FLOAT,
                ai_summary TEXT,
                full_results JSONB
            );
            """
            
            with engine.connect() as conn:
                conn.execute(text(create_table_query))
                
                # Insert current results
                insert_query = """
                INSERT INTO ai_insights.analysis_results 
                (total_insights, high_priority_count, medium_priority_count, average_confidence, ai_summary, full_results)
                VALUES (:total, :high, :medium, :confidence, :summary, :results)
                """
                
                conn.execute(text(insert_query), {
                    'total': results['total_insights_generated'],
                    'high': results['metadata']['high_priority_count'],
                    'medium': results['metadata']['medium_priority_count'],
                    'confidence': results['metadata']['average_confidence'],
                    'summary': results['ai_summary'],
                    'results': json.dumps(results)
                })
                
                conn.commit()
                
            logger.info("✅ AI insights saved to warehouse")
            return True
            
        except Exception as e:
            logger.error(f"Error saving insights: {e}")
            return False

def main():
    """Main execution function"""
    print("🚀 GenETL AI-Powered Analytics Engine")
    print("=" * 50)
    
    # Initialize AI analyzer
    ai_analyzer = GenETLAIAnalyzer()
    
    # Run comprehensive analysis
    results = ai_analyzer.run_comprehensive_analysis()
    
    if "error" in results:
        print(f"❌ Analysis failed: {results['error']}")
        return
    
    # Display results
    print(results['ai_summary'])
    
    print(f"\n📊 DETAILED INSIGHTS ({results['total_insights_generated']} total):")
    print("=" * 60)
    
    for i, insight in enumerate(results['insights'], 1):
        print(f"\n{i}. {insight['title']} [{insight['priority']}]")
        print(f"   {insight['description']}")
        print(f"   💡 Recommendation: {insight['recommendation']}")
        print(f"   🎯 Confidence: {insight['confidence']:.0%}")
    
    # Save to warehouse
    if ai_analyzer.save_insights_to_warehouse(results):
        print(f"\n✅ Analysis results saved to warehouse!")
    
    print(f"\n🎉 AI Analysis Complete!")
    print(f"Generated {results['total_insights_generated']} insights with {results['metadata']['average_confidence']:.0%} average confidence")

if __name__ == "__main__":
    main()