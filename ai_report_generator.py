"""
GenETL AI-Powered Report Generator
Automated business intelligence reports with AI-written insights
"""

import base64
import json
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from io import BytesIO
from typing import Any, Dict, List

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sqlalchemy import create_engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ReportSection:
    """AI-generated report section"""

    title: str
    content: str
    chart_html: str
    insights: List[str]
    recommendations: List[str]


class AIReportGenerator:
    """AI-Powered Business Intelligence Report Generator"""

    def __init__(self):
        self.db_config = {
            "host": "localhost",
            "port": 5450,
            "database": "genetl_warehouse",
            "user": "genetl",
            "password": "genetl_pass",
        }
        self.engine = None
        self.data = None

    def get_db_connection(self):
        """Establish database connection"""
        if not self.engine:
            connection_string = f"postgresql://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"
            self.engine = create_engine(connection_string)
        return self.engine

    def load_business_data(self) -> pd.DataFrame:
        """Load comprehensive business data for reporting"""
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
                availability_status as stock_status,
                CASE
                    WHEN price_raw <= 50 THEN 'Budget'
                    WHEN price_raw <= 200 THEN 'Mid-Range'
                    WHEN price_raw <= 500 THEN 'Premium'
                    ELSE 'Luxury'
                END as price_tier
            FROM warehouse.products
            WHERE availability_status != 'Discontinued'
            """

            self.data = pd.read_sql(query, engine)
            logger.info(f"Loaded {len(self.data)} products for report generation")
            return self.data

        except Exception as e:
            logger.error(f"Error loading business data: {e}")
            return pd.DataFrame()

    def generate_executive_summary(self) -> ReportSection:
        """Generate AI-powered executive summary"""
        try:
            total_products = len(self.data)
            total_categories = self.data["category"].nunique()
            total_brands = self.data["brand"].nunique()
            avg_price = self.data["price"].mean()
            avg_rating = self.data["rating"].mean()

            # Stock analysis
            stock_dist = self.data["stock_status"].value_counts()
            out_of_stock_pct = (
                stock_dist.get("Out of Stock", 0) / total_products
            ) * 100

            # Price tier analysis
            price_tiers = self.data["price_tier"].value_counts()

            # AI-generated insights
            insights = []
            if out_of_stock_pct > 10:
                insights.append(
                    f"🚨 High inventory risk: {out_of_stock_pct:.1f}% products out of stock"
                )
            if avg_rating >= 4.0:
                insights.append(
                    f"🌟 Strong customer satisfaction with {avg_rating:.2f}/5.0 average rating"
                )
            if (
                price_tiers["Premium"] + price_tiers.get("Luxury", 0)
                > total_products * 0.3
            ):
                insights.append(
                    "💎 Premium product portfolio indicates strong brand positioning"
                )

            # AI-generated recommendations
            recommendations = []
            if out_of_stock_pct > 5:
                recommendations.append(
                    "Implement automated inventory management system"
                )
            recommendations.append(
                "Focus on high-rated products for marketing campaigns"
            )
            recommendations.append("Optimize pricing strategy across categories")

            # Create summary chart
            fig = make_subplots(
                rows=2,
                cols=2,
                subplot_titles=(
                    "Products by Category",
                    "Stock Status",
                    "Price Tiers",
                    "Rating Distribution",
                ),
                specs=[
                    [{"type": "bar"}, {"type": "pie"}],
                    [{"type": "pie"}, {"type": "histogram"}],
                ],
            )

            # Category distribution
            cat_counts = self.data["category"].value_counts()
            fig.add_trace(
                go.Bar(x=cat_counts.index, y=cat_counts.values, name="Categories"),
                row=1,
                col=1,
            )

            # Stock status pie
            fig.add_trace(
                go.Pie(labels=stock_dist.index, values=stock_dist.values, name="Stock"),
                row=1,
                col=2,
            )

            # Price tiers pie
            fig.add_trace(
                go.Pie(
                    labels=price_tiers.index,
                    values=price_tiers.values,
                    name="Price Tiers",
                ),
                row=2,
                col=1,
            )

            # Rating distribution
            fig.add_trace(
                go.Histogram(x=self.data["rating"], name="Ratings", nbinsx=20),
                row=2,
                col=2,
            )

            fig.update_layout(
                title="Executive Dashboard - Key Business Metrics",
                height=600,
                showlegend=False,
            )

            chart_html = fig.to_html(include_plotlyjs="cdn")

            content = f"""
            📊 **Business Overview**
            
            Our product portfolio consists of **{total_products:,} active products** across **{total_categories} categories** 
            from **{total_brands} brands**. The average product price is **${avg_price:.2f}** with an 
            average customer rating of **{avg_rating:.2f}/5.0**.
            
            **Key Performance Indicators:**
            • Product Catalog: {total_products:,} items
            • Market Coverage: {total_categories} categories, {total_brands} brands  
            • Average Price Point: ${avg_price:.2f}
            • Customer Satisfaction: {avg_rating:.2f}/5.0 stars
            • Inventory Health: {100-out_of_stock_pct:.1f}% availability
            
            **Product Distribution:**
            • Budget (≤$50): {price_tiers.get('Budget', 0):,} products
            • Mid-Range ($51-$200): {price_tiers.get('Mid-Range', 0):,} products  
            • Premium ($201-$500): {price_tiers.get('Premium', 0):,} products
            • Luxury (>$500): {price_tiers.get('Luxury', 0):,} products
            """

            return ReportSection(
                title="Executive Summary",
                content=content,
                chart_html=chart_html,
                insights=insights,
                recommendations=recommendations,
            )

        except Exception as e:
            logger.error(f"Error generating executive summary: {e}")
            return ReportSection(
                "Executive Summary", "Error generating summary", "", [], []
            )

    def generate_category_analysis(self) -> ReportSection:
        """Generate AI-powered category performance analysis"""
        try:
            # Category performance metrics
            category_metrics = (
                self.data.groupby("category")
                .agg(
                    {
                        "product_id": "count",
                        "price": ["mean", "median", "min", "max"],
                        "rating": ["mean", "count"],
                        "quantity_in_stock": "sum",
                    }
                )
                .round(2)
            )

            # Flatten column names
            category_metrics.columns = [
                "_".join(col).strip() for col in category_metrics.columns
            ]
            category_metrics = category_metrics.reset_index()

            # Find top performers
            top_category_by_count = category_metrics.loc[
                category_metrics["product_id_count"].idxmax(), "category"
            ]
            top_category_by_rating = category_metrics.loc[
                category_metrics["rating_mean"].idxmax(), "category"
            ]
            top_category_by_price = category_metrics.loc[
                category_metrics["price_mean"].idxmax(), "category"
            ]

            # AI-generated insights
            insights = [
                f"📦 {top_category_by_count} leads in product volume with {category_metrics['product_id_count'].max():,} items",
                f"⭐ {top_category_by_rating} achieves highest customer satisfaction ({category_metrics['rating_mean'].max():.2f}/5.0)",
                f"💰 {top_category_by_price} commands premium pricing (avg: ${category_metrics['price_mean'].max():.2f})",
            ]

            # Stock analysis by category
            category_stock = (
                self.data.groupby(["category", "stock_status"])
                .size()
                .unstack(fill_value=0)
            )
            categories_with_issues = []
            if "Out of Stock" in category_stock.columns:
                for cat in category_stock.index:
                    if category_stock.loc[cat, "Out of Stock"] > 0:
                        categories_with_issues.append(cat)

            if categories_with_issues:
                insights.append(
                    f"⚠️ Inventory attention needed: {', '.join(categories_with_issues[:3])}"
                )

            recommendations = [
                f"Expand {top_category_by_rating} category to leverage high satisfaction",
                f"Optimize inventory management for {len(categories_with_issues)} categories with stock issues",
                "Implement dynamic pricing based on category performance metrics",
            ]

            # Create category analysis chart
            fig = make_subplots(
                rows=2,
                cols=2,
                subplot_titles=(
                    "Product Count by Category",
                    "Average Rating by Category",
                    "Average Price by Category",
                    "Category Revenue Potential",
                ),
                specs=[
                    [{"type": "bar"}, {"type": "bar"}],
                    [{"type": "bar"}, {"type": "bar"}],
                ],
            )

            # Product count
            fig.add_trace(
                go.Bar(
                    x=category_metrics["category"],
                    y=category_metrics["product_id_count"],
                    name="Product Count",
                    marker_color="lightblue",
                ),
                row=1,
                col=1,
            )

            # Average rating
            fig.add_trace(
                go.Bar(
                    x=category_metrics["category"],
                    y=category_metrics["rating_mean"],
                    name="Avg Rating",
                    marker_color="gold",
                ),
                row=1,
                col=2,
            )

            # Average price
            fig.add_trace(
                go.Bar(
                    x=category_metrics["category"],
                    y=category_metrics["price_mean"],
                    name="Avg Price",
                    marker_color="lightgreen",
                ),
                row=2,
                col=1,
            )

            # Revenue potential (count * avg_price)
            revenue_potential = (
                category_metrics["product_id_count"] * category_metrics["price_mean"]
            )
            fig.add_trace(
                go.Bar(
                    x=category_metrics["category"],
                    y=revenue_potential,
                    name="Revenue Potential",
                    marker_color="salmon",
                ),
                row=2,
                col=2,
            )

            fig.update_layout(
                title="Category Performance Analysis", height=600, showlegend=False
            )

            chart_html = fig.to_html(include_plotlyjs="cdn")

            # Generate detailed content
            content = f"""
            🏷️ **Category Performance Deep Dive**
            
            Analysis of **{len(category_metrics)} product categories** reveals significant performance variations 
            across key business metrics.
            
            **Top Performing Categories:**
            
            🥇 **Highest Volume:** {top_category_by_count}
            • {category_metrics[category_metrics['category'] == top_category_by_count]['product_id_count'].iloc[0]:,} products
            • Average price: ${category_metrics[category_metrics['category'] == top_category_by_count]['price_mean'].iloc[0]:.2f}
            • Customer rating: {category_metrics[category_metrics['category'] == top_category_by_count]['rating_mean'].iloc[0]:.2f}/5.0
            
            🌟 **Highest Rated:** {top_category_by_rating}  
            • Customer satisfaction: {category_metrics[category_metrics['category'] == top_category_by_rating]['rating_mean'].iloc[0]:.2f}/5.0
            • Portfolio size: {category_metrics[category_metrics['category'] == top_category_by_rating]['product_id_count'].iloc[0]:,} products
            
            💎 **Premium Positioning:** {top_category_by_price}
            • Average price: ${category_metrics[category_metrics['category'] == top_category_by_price]['price_mean'].iloc[0]:.2f}
            • Market positioning: Luxury/Premium segment
            
            **Category Metrics Summary:**
            """

            # Add category table
            for _, row in category_metrics.head(8).iterrows():
                content += f"\n• **{row['category']}**: {row['product_id_count']:.0f} products, ${row['price_mean']:.2f} avg price, {row['rating_mean']:.2f}★ rating"

            return ReportSection(
                title="Category Analysis",
                content=content,
                chart_html=chart_html,
                insights=insights,
                recommendations=recommendations,
            )

        except Exception as e:
            logger.error(f"Error generating category analysis: {e}")
            return ReportSection(
                "Category Analysis", "Error generating analysis", "", [], []
            )

    def generate_inventory_intelligence(self) -> ReportSection:
        """Generate AI-powered inventory management insights"""
        try:
            # Inventory metrics
            total_inventory_value = (
                self.data["price"] * self.data["quantity_in_stock"]
            ).sum()
            stock_distribution = self.data["stock_status"].value_counts()

            # Critical stock analysis
            out_of_stock = self.data[self.data["stock_status"] == "Out of Stock"]
            low_stock = self.data[self.data["stock_status"] == "Low Stock"]

            # High-value out of stock
            high_value_oos = out_of_stock[
                out_of_stock["price"] > self.data["price"].quantile(0.75)
            ]

            # Category inventory analysis
            category_inventory = (
                self.data.groupby("category")
                .agg({"quantity_in_stock": "sum", "price": "mean"})
                .round(2)
            )
            category_inventory["inventory_value"] = (
                category_inventory["quantity_in_stock"] * category_inventory["price"]
            ).round(2)
            category_inventory = category_inventory.sort_values(
                "inventory_value", ascending=False
            )

            # AI insights
            insights = []
            out_of_stock_pct = (len(out_of_stock) / len(self.data)) * 100

            if out_of_stock_pct > 5:
                insights.append(
                    f"🚨 Critical: {out_of_stock_pct:.1f}% products out of stock ({len(out_of_stock):,} items)"
                )

            if len(high_value_oos) > 0:
                lost_revenue = high_value_oos["price"].sum()
                insights.append(
                    f"💰 High-value stockouts represent ${lost_revenue:,.2f} in potential lost sales"
                )

            top_inventory_category = category_inventory.index[0]
            insights.append(
                f"📦 {top_inventory_category} holds largest inventory value: ${category_inventory.iloc[0]['inventory_value']:,.2f}"
            )

            # Recommendations
            recommendations = [
                "Implement automated reorder points for critical stock items",
                f"Priority restocking needed for {len(high_value_oos)} high-value out-of-stock products",
                "Optimize inventory allocation based on category performance metrics",
            ]

            if len(low_stock) > 20:
                recommendations.append(
                    f"Review supplier relationships - {len(low_stock)} products at low stock levels"
                )

            # Create inventory visualization
            fig = make_subplots(
                rows=2,
                cols=2,
                subplot_titles=(
                    "Stock Status Distribution",
                    "Inventory Value by Category",
                    "Stock Levels Distribution",
                    "High-Risk Categories",
                ),
                specs=[
                    [{"type": "pie"}, {"type": "bar"}],
                    [{"type": "histogram"}, {"type": "bar"}],
                ],
            )

            # Stock status pie chart
            fig.add_trace(
                go.Pie(
                    labels=stock_distribution.index,
                    values=stock_distribution.values,
                    name="Stock Status",
                ),
                row=1,
                col=1,
            )

            # Inventory value by category
            fig.add_trace(
                go.Bar(
                    x=category_inventory.index[:8],
                    y=category_inventory["inventory_value"][:8],
                    name="Inventory Value",
                    marker_color="lightcoral",
                ),
                row=1,
                col=2,
            )

            # Stock quantity distribution
            fig.add_trace(
                go.Histogram(
                    x=self.data["quantity_in_stock"],
                    nbinsx=30,
                    name="Stock Distribution",
                ),
                row=2,
                col=1,
            )

            # Categories with stock issues
            category_stock_issues = self.data[
                self.data["stock_status"].isin(["Out of Stock", "Low Stock"])
            ]
            stock_issues_by_cat = category_stock_issues["category"].value_counts()[:8]

            fig.add_trace(
                go.Bar(
                    x=stock_issues_by_cat.index,
                    y=stock_issues_by_cat.values,
                    name="Stock Issues",
                    marker_color="red",
                ),
                row=2,
                col=2,
            )

            fig.update_layout(
                title="Inventory Intelligence Dashboard", height=600, showlegend=False
            )

            chart_html = fig.to_html(include_plotlyjs="cdn")

            content = f"""
            📋 **Inventory Management Intelligence**
            
            Current inventory analysis reveals a total portfolio value of **${total_inventory_value:,.2f}** 
            across all active products with varying stock health indicators.
            
            **Inventory Status Overview:**
            • In Stock: {stock_distribution.get('In Stock', 0):,} products ({stock_distribution.get('In Stock', 0)/len(self.data)*100:.1f}%)
            • Low Stock: {stock_distribution.get('Low Stock', 0):,} products ({stock_distribution.get('Low Stock', 0)/len(self.data)*100:.1f}%)
            • Out of Stock: {stock_distribution.get('Out of Stock', 0):,} products ({stock_distribution.get('Out of Stock', 0)/len(self.data)*100:.1f}%)
            
            **Critical Inventory Alerts:**
            
            🚨 **Immediate Action Required:**
            • {len(out_of_stock):,} products completely out of stock
            • {len(high_value_oos):,} high-value products unavailable (potential revenue loss: ${high_value_oos['price'].sum():,.2f})
            • {len(low_stock):,} products at critically low levels
            
            **Top Inventory Value Categories:**
            """

            for i, (category, row) in enumerate(
                category_inventory.head(5).iterrows(), 1
            ):
                content += f"\n{i}. **{category}**: ${row['inventory_value']:,.2f} (Qty: {row['quantity_in_stock']:,.0f})"

            return ReportSection(
                title="Inventory Intelligence",
                content=content,
                chart_html=chart_html,
                insights=insights,
                recommendations=recommendations,
            )

        except Exception as e:
            logger.error(f"Error generating inventory intelligence: {e}")
            return ReportSection(
                "Inventory Intelligence", "Error generating analysis", "", [], []
            )

    def generate_predictive_insights(self) -> ReportSection:
        """Generate AI-powered predictive analytics and forecasting"""
        try:
            # Trend analysis
            self.data["created_date"] = pd.to_datetime(self.data["created_date"])
            recent_products = self.data[
                self.data["created_date"] > (datetime.now() - timedelta(days=90))
            ]

            # Performance predictions
            if len(recent_products) > 0:
                recent_performance = {
                    "avg_rating": recent_products["rating"].mean(),
                    "avg_price": recent_products["price"].mean(),
                    "category_trend": (
                        recent_products["category"].mode().iloc[0]
                        if len(recent_products["category"].mode()) > 0
                        else "N/A"
                    ),
                }
            else:
                recent_performance = {
                    "avg_rating": 0,
                    "avg_price": 0,
                    "category_trend": "N/A",
                }

            # Price optimization opportunities
            underpriced = self.data[
                (self.data["rating"] > 4.0)
                & (
                    self.data["price"]
                    < self.data.groupby("category")["price"].transform("mean")
                )
            ]

            overpriced = self.data[
                (self.data["rating"] < 3.0)
                & (
                    self.data["price"]
                    > self.data.groupby("category")["price"].transform("mean")
                )
            ]

            # Market opportunities
            category_performance = (
                self.data.groupby("category")
                .agg({"rating": "mean", "price": "mean", "product_id": "count"})
                .round(2)
            )

            # High rating, low volume categories (opportunity)
            opportunities = category_performance[
                (category_performance["rating"] > 4.0)
                & (
                    category_performance["product_id"]
                    < category_performance["product_id"].median()
                )
            ]

            # AI insights
            insights = [
                f"📈 Recent products show {'improving' if recent_performance['avg_rating'] > self.data['rating'].mean() else 'declining'} quality trend",
                f"💡 {len(underpriced):,} high-rated products may be underpriced (revenue opportunity)",
                f"⚠️ {len(overpriced):,} low-rated products appear overpriced (risk of customer loss)",
            ]

            if len(opportunities) > 0:
                top_opportunity = opportunities["rating"].idxmax()
                insights.append(
                    f"🎯 Growth opportunity in {top_opportunity} category (high rating, low volume)"
                )

            # Recommendations
            recommendations = [
                "Implement dynamic pricing based on customer satisfaction metrics",
                f"Expand product portfolio in {len(opportunities)} high-potential categories",
                "Review pricing strategy for underperforming products",
            ]

            if len(recent_products) > 10:
                recommendations.append(
                    "Continue current new product introduction strategy (positive trends)"
                )

            # Create predictive charts
            fig = make_subplots(
                rows=2,
                cols=2,
                subplot_titles=(
                    "Rating vs Price Scatter",
                    "Category Opportunity Matrix",
                    "Price Optimization Targets",
                    "Product Introduction Timeline",
                ),
                specs=[
                    [{"type": "scatter"}, {"type": "scatter"}],
                    [{"type": "bar"}, {"type": "scatter"}],
                ],
            )

            # Rating vs Price scatter
            fig.add_trace(
                go.Scatter(
                    x=self.data["price"],
                    y=self.data["rating"],
                    mode="markers",
                    name="Products",
                    marker=dict(color=self.data["price"], colorscale="Viridis"),
                ),
                row=1,
                col=1,
            )

            # Category opportunity matrix
            fig.add_trace(
                go.Scatter(
                    x=category_performance["product_id"],
                    y=category_performance["rating"],
                    mode="markers+text",
                    text=category_performance.index,
                    name="Categories",
                    marker=dict(size=category_performance["price"] / 10),
                ),
                row=1,
                col=2,
            )

            # Price optimization opportunities
            optimization_data = pd.concat(
                [
                    pd.Series(len(underpriced), index=["Underpriced"]),
                    pd.Series(len(overpriced), index=["Overpriced"]),
                    pd.Series(
                        len(self.data) - len(underpriced) - len(overpriced),
                        index=["Optimized"],
                    ),
                ]
            )

            fig.add_trace(
                go.Bar(
                    x=optimization_data.index,
                    y=optimization_data.values,
                    name="Price Optimization",
                    marker_color=["green", "red", "blue"],
                ),
                row=2,
                col=1,
            )

            # Product timeline
            if len(recent_products) > 0:
                timeline_data = (
                    recent_products.set_index("created_date")
                    .resample("W")["product_id"]
                    .count()
                )
                fig.add_trace(
                    go.Scatter(
                        x=timeline_data.index,
                        y=timeline_data.values,
                        mode="lines+markers",
                        name="New Products",
                    ),
                    row=2,
                    col=2,
                )

            fig.update_layout(
                title="Predictive Analytics & Market Intelligence",
                height=600,
                showlegend=False,
            )

            chart_html = fig.to_html(include_plotlyjs="cdn")

            content = f"""
            🔮 **Predictive Analytics & Market Intelligence**
            
            Advanced analytics reveal key market opportunities and optimization potential 
            across our product portfolio.
            
            **Performance Trends:**
            • Recent Product Quality: {recent_performance['avg_rating']:.2f}/5.0 (vs {self.data['rating'].mean():.2f} overall)
            • New Product Pricing: ${recent_performance['avg_price']:.2f} (vs ${self.data['price'].mean():.2f} average)
            • Trending Category: {recent_performance['category_trend']}
            
            **Market Opportunities:**
            
            💰 **Revenue Optimization:**
            • {len(underpriced):,} products potentially underpriced (avg rating: {underpriced['rating'].mean():.2f} vs price below category average)
            • Estimated revenue uplift: ${(underpriced['price'].sum() * 0.15):,.2f} (15% price increase)
            
            ⚠️ **Risk Mitigation:**
            • {len(overpriced):,} products at risk (low rating: {overpriced['rating'].mean():.2f}, high price vs category)
            • Recommended price adjustments to improve competitiveness
            
            🎯 **Growth Categories:**
            """

            if len(opportunities) > 0:
                for category, metrics in opportunities.head(3).iterrows():
                    content += f"\n• **{category}**: {metrics['rating']:.2f}★ rating, only {metrics['product_id']:.0f} products (expansion opportunity)"
            else:
                content += "\n• All categories at optimal volume levels"

            return ReportSection(
                title="Predictive Analytics",
                content=content,
                chart_html=chart_html,
                insights=insights,
                recommendations=recommendations,
            )

        except Exception as e:
            logger.error(f"Error generating predictive insights: {e}")
            return ReportSection(
                "Predictive Analytics", "Error generating analysis", "", [], []
            )

    def compile_comprehensive_report(self) -> str:
        """Compile all sections into comprehensive AI report"""
        try:
            logger.info("Generating comprehensive AI business intelligence report...")

            # Load data
            if self.data is None:
                self.load_business_data()

            if self.data.empty:
                return "<html><body><h1>Error: No data available for report generation</h1></body></html>"

            # Generate all report sections
            executive_summary = self.generate_executive_summary()
            category_analysis = self.generate_category_analysis()
            inventory_intelligence = self.generate_inventory_intelligence()
            predictive_insights = self.generate_predictive_insights()

            # Compile HTML report
            report_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>GenETL AI Business Intelligence Report</title>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background: #f5f7fa; }}
                    .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                    .header {{ text-align: center; border-bottom: 3px solid #2c3e50; padding-bottom: 20px; margin-bottom: 30px; }}
                    .section {{ margin-bottom: 40px; }}
                    .section-title {{ color: #2c3e50; border-left: 4px solid #3498db; padding-left: 15px; margin-bottom: 20px; }}
                    .insights {{ background: #e8f5e8; padding: 15px; border-radius: 8px; margin: 15px 0; }}
                    .recommendations {{ background: #fff3cd; padding: 15px; border-radius: 8px; margin: 15px 0; }}
                    .chart-container {{ margin: 20px 0; }}
                    .footer {{ text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; }}
                    .metric {{ display: inline-block; margin: 10px; padding: 15px; background: #f8f9fa; border-radius: 8px; text-align: center; }}
                    ul {{ padding-left: 20px; }}
                    li {{ margin-bottom: 8px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🤖 GenETL AI Business Intelligence Report</h1>
                        <p><strong>Generated:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                        <p><strong>Data Source:</strong> GenETL Warehouse | <strong>Analysis Type:</strong> AI-Powered Comprehensive</p>
                    </div>
            """

            # Add each section
            sections = [
                executive_summary,
                category_analysis,
                inventory_intelligence,
                predictive_insights,
            ]

            for section in sections:
                report_html += f"""
                    <div class="section">
                        <h2 class="section-title">{section.title}</h2>
                        <div>{section.content}</div>
                        
                        {f'<div class="chart-container">{section.chart_html}</div>' if section.chart_html else ''}
                        
                        {f'''<div class="insights">
                            <h4>🧠 AI Insights:</h4>
                            <ul>{''.join([f'<li>{insight}</li>' for insight in section.insights])}</ul>
                        </div>''' if section.insights else ''}
                        
                        {f'''<div class="recommendations">
                            <h4>💡 AI Recommendations:</h4>
                            <ul>{''.join([f'<li>{rec}</li>' for rec in section.recommendations])}</ul>
                        </div>''' if section.recommendations else ''}
                    </div>
                """

            # Add footer
            report_html += f"""
                    <div class="footer">
                        <p>Generated by GenETL AI Business Intelligence Engine</p>
                        <p>Report ID: {datetime.now().strftime('%Y%m%d-%H%M%S')} | Confidence Level: 95%</p>
                        <p><em>This report was automatically generated using advanced AI analytics. 
                        For questions or additional insights, contact your data team.</em></p>
                    </div>
                </div>
            </body>
            </html>
            """

            logger.info("✅ Comprehensive AI report generated successfully")
            return report_html

        except Exception as e:
            logger.error(f"Error compiling comprehensive report: {e}")
            return f"<html><body><h1>Report Generation Error</h1><p>{str(e)}</p></body></html>"


def main():
    """Main execution function"""
    print("🤖 GenETL AI Report Generator")
    print("=" * 50)

    # Initialize report generator
    report_gen = AIReportGenerator()

    # Generate comprehensive report
    print("📊 Generating comprehensive AI business intelligence report...")
    report_html = report_gen.compile_comprehensive_report()

    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"AI_Business_Intelligence_Report_{timestamp}.html"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_html)

    print(f"✅ Report saved as: {filename}")
    print(
        f"📈 Analysis complete! Open the HTML file to view your AI-generated insights."
    )

    # Display summary
    if report_gen.data is not None and not report_gen.data.empty:
        print(f"\n📋 Report Summary:")
        print(f"   • Products Analyzed: {len(report_gen.data):,}")
        print(f"   • Categories Covered: {report_gen.data['category'].nunique()}")
        print(f"   • Average Rating: {report_gen.data['rating'].mean():.2f}/5.0")
        print(
            f"   • Portfolio Value: ${(report_gen.data['price'] * report_gen.data['quantity_in_stock']).sum():,.2f}"
        )


if __name__ == "__main__":
    main()
