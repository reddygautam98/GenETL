"""
GenETL Predictive Analytics Engine
Advanced ML-powered forecasting and business intelligence
"""

import logging
import math
import warnings
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

import pandas as pd
from scipy import stats
from sqlalchemy import create_engine

# Suppress warnings
warnings.filterwarnings("ignore")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PredictionResult:
    """Prediction result with confidence metrics"""

    metric: str
    current_value: float
    predicted_value: float
    confidence_score: float
    trend_direction: str
    prediction_date: datetime
    methodology: str
    supporting_data: List[str]


@dataclass
class ForecastModel:
    """Forecast model configuration"""

    name: str
    description: str
    accuracy_score: float
    last_trained: datetime
    parameters: dict


class PredictiveAnalyticsEngine:
    """AI-Powered Predictive Analytics and Forecasting System"""

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
        self.models = {}

    def get_db_connection(self):
        """Establish database connection"""
        if not self.engine:
            connection_string = f"postgresql://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"
            self.engine = create_engine(connection_string)
        return self.engine

    def load_historical_data(self) -> pd.DataFrame:
        """Load comprehensive historical data for analysis"""
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
                extracted_at as created_date,
                extracted_at as last_updated,
                CASE 
                    WHEN availability_status != 'Discontinued' THEN true
                    ELSE false
                END as is_active
            FROM warehouse.products
            ORDER BY extracted_at DESC
            """

            self.data = pd.read_sql(query, engine)
            self.data["created_date"] = pd.to_datetime(self.data["created_date"])
            self.data["last_updated"] = pd.to_datetime(self.data["last_updated"])

            logger.info(f"Loaded {len(self.data)} records for predictive analysis")
            return self.data

        except Exception as e:
            logger.error(f"Error loading historical data: {e}")
            return pd.DataFrame()

    def calculate_moving_average(
        self, series: pd.Series, window: int = 30
    ) -> pd.Series:
        """Calculate moving average for trend analysis"""
        return series.rolling(window=window, min_periods=1).mean()

    def detect_seasonality(self, series: pd.Series) -> dict:
        """Detect seasonal patterns in data"""
        try:
            # Basic seasonality detection using autocorrelation
            if len(series) < 10:
                return {"seasonal": False, "period": None, "strength": 0}

            # Calculate autocorrelation for different lags
            autocorrs = []
            max_lag = min(len(series) // 2, 365)  # Maximum 1 year or half series length

            for lag in range(1, max_lag):
                if len(series) > lag:
                    corr = series.autocorr(lag=lag)
                    if not pd.isna(corr):
                        autocorrs.append((lag, abs(corr)))

            if not autocorrs:
                return {"seasonal": False, "period": None, "strength": 0}

            # Find strongest correlation
            best_lag, best_corr = max(autocorrs, key=lambda x: x[1])

            return {
                "seasonal": best_corr > 0.3,  # Threshold for seasonality
                "period": best_lag,
                "strength": best_corr,
            }

        except Exception as e:
            logger.warning(f"Seasonality detection failed: {e}")
            return {"seasonal": False, "period": None, "strength": 0}

    def linear_trend_forecast(
        self, series: pd.Series, periods: int = 30
    ) -> Tuple[List[float], float]:
        """Simple linear trend forecasting"""
        try:
            if len(series) < 2:
                return [series.iloc[-1]] * periods, 0.5

            # Prepare data for linear regression
            x = list(range(len(series)))
            y = series.tolist()

            # Calculate linear regression coefficients
            n = len(x)
            sum_x = sum(x)
            sum_y = sum(y)
            sum_xy = sum(xi * yi for xi, yi in zip(x, y))
            sum_x2 = sum(xi * xi for xi in x)

            # Avoid division by zero
            denominator = n * sum_x2 - sum_x * sum_x
            if denominator == 0:
                return [series.mean()] * periods, 0.5

            slope = (n * sum_xy - sum_x * sum_y) / denominator
            intercept = (sum_y - slope * sum_x) / n

            # Generate predictions
            last_x = len(series) - 1
            predictions = []
            for i in range(1, periods + 1):
                pred_x = last_x + i
                pred_y = slope * pred_x + intercept
                predictions.append(max(0, pred_y))  # Ensure non-negative

            # Calculate R-squared for confidence
            y_pred = [slope * xi + intercept for xi in x]
            ss_res = sum((y[i] - y_pred[i]) ** 2 for i in range(n))
            ss_tot = sum((y[i] - sum_y / n) ** 2 for i in range(n))

            r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
            confidence = max(0.1, min(0.95, r_squared))  # Bounded confidence

            return predictions, confidence

        except Exception as e:
            logger.warning(f"Linear trend forecast failed: {e}")
            return [series.mean()] * periods, 0.5

    def exponential_smoothing_forecast(
        self, series: pd.Series, periods: int = 30, alpha: float = 0.3
    ) -> Tuple[List[float], float]:
        """Exponential smoothing forecasting"""
        try:
            if len(series) == 0:
                return [0] * periods, 0.1
            elif len(series) == 1:
                return [series.iloc[0]] * periods, 0.5

            # Initialize
            smoothed = [series.iloc[0]]

            # Calculate exponentially smoothed values
            for i in range(1, len(series)):
                smoothed_val = alpha * series.iloc[i] + (1 - alpha) * smoothed[-1]
                smoothed.append(smoothed_val)

            # Forecast future values
            last_smoothed = smoothed[-1]
            predictions = [last_smoothed] * periods

            # Calculate mean absolute error for confidence
            errors = []
            for i in range(1, len(series)):
                error = abs(series.iloc[i] - smoothed[i - 1])
                errors.append(error)

            mean_error = sum(errors) / len(errors) if errors else series.std()
            confidence = (
                max(0.1, min(0.9, 1 - (mean_error / series.mean())))
                if series.mean() != 0
                else 0.5
            )

            return predictions, confidence

        except Exception as e:
            logger.warning(f"Exponential smoothing failed: {e}")
            return [series.mean()] * periods, 0.5

    def predict_sales_performance(self) -> List[PredictionResult]:
        """Predict sales performance metrics"""
        try:
            if self.data is None or self.data.empty:
                self.load_historical_data()

            predictions = []

            # 1. Average Price Trend Prediction
            price_series = (
                self.data.set_index("created_date")["price"]
                .resample("D")
                .mean()
                .fillna(method="ffill")
            )
            if len(price_series) > 0:
                price_forecast, price_confidence = self.linear_trend_forecast(
                    price_series, 30
                )

                predictions.append(
                    PredictionResult(
                        metric="Average Product Price",
                        current_value=(
                            price_series.iloc[-1] if len(price_series) > 0 else 0
                        ),
                        predicted_value=(
                            price_forecast[29] if price_forecast else 0
                        ),  # 30 days ahead
                        confidence_score=price_confidence,
                        trend_direction=(
                            "upward"
                            if (price_forecast[29] if price_forecast else 0)
                            > (price_series.iloc[-1] if len(price_series) > 0 else 0)
                            else "downward"
                        ),
                        prediction_date=datetime.now() + timedelta(days=30),
                        methodology="Linear Trend Analysis",
                        supporting_data=[
                            f"Historical data points: {len(price_series)}",
                            f"Price volatility: {price_series.std():.2f}",
                        ],
                    )
                )

            # 2. Product Rating Trend
            rating_series = (
                self.data.set_index("created_date")["rating"]
                .resample("W")
                .mean()
                .fillna(method="ffill")
            )
            if len(rating_series) > 0:
                rating_forecast, rating_confidence = (
                    self.exponential_smoothing_forecast(rating_series, 4)
                )  # 4 weeks

                predictions.append(
                    PredictionResult(
                        metric="Customer Satisfaction Rating",
                        current_value=(
                            rating_series.iloc[-1] if len(rating_series) > 0 else 0
                        ),
                        predicted_value=(
                            rating_forecast[3] if rating_forecast else 0
                        ),  # 4 weeks ahead
                        confidence_score=rating_confidence,
                        trend_direction=(
                            "improving"
                            if (rating_forecast[3] if rating_forecast else 0)
                            > (rating_series.iloc[-1] if len(rating_series) > 0 else 0)
                            else "declining"
                        ),
                        prediction_date=datetime.now() + timedelta(weeks=4),
                        methodology="Exponential Smoothing",
                        supporting_data=[
                            f"Rating stability: {rating_series.std():.3f}",
                            f"Trend strength: {rating_confidence:.2f}",
                        ],
                    )
                )

            # 3. Inventory Turnover Prediction
            stock_series = (
                self.data.set_index("created_date")["quantity_in_stock"]
                .resample("D")
                .sum()
            )
            if len(stock_series) > 0:
                stock_forecast, stock_confidence = self.linear_trend_forecast(
                    stock_series, 14
                )  # 2 weeks

                predictions.append(
                    PredictionResult(
                        metric="Total Inventory Level",
                        current_value=(
                            stock_series.iloc[-1] if len(stock_series) > 0 else 0
                        ),
                        predicted_value=(
                            stock_forecast[13] if stock_forecast else 0
                        ),  # 2 weeks ahead
                        confidence_score=stock_confidence,
                        trend_direction=(
                            "increasing"
                            if (stock_forecast[13] if stock_forecast else 0)
                            > (stock_series.iloc[-1] if len(stock_series) > 0 else 0)
                            else "decreasing"
                        ),
                        prediction_date=datetime.now() + timedelta(days=14),
                        methodology="Linear Regression",
                        supporting_data=[
                            f"Inventory volatility: {stock_series.std():.0f}",
                            f"Seasonal pattern detected: {self.detect_seasonality(stock_series)['seasonal']}",
                        ],
                    )
                )

            logger.info(f"Generated {len(predictions)} sales performance predictions")
            return predictions

        except Exception as e:
            logger.error(f"Error predicting sales performance: {e}")
            return []

    def predict_category_trends(self) -> List[PredictionResult]:
        """Predict category-specific trends"""
        try:
            if self.data is None or self.data.empty:
                self.load_historical_data()

            predictions = []
            categories = self.data["category"].unique()

            for category in categories[:5]:  # Analyze top 5 categories
                cat_data = self.data[self.data["category"] == category]

                if len(cat_data) < 5:  # Skip if insufficient data
                    continue

                # Category growth prediction
                cat_timeline = (
                    cat_data.set_index("created_date")
                    .resample("W")["product_id"]
                    .count()
                )

                if len(cat_timeline) > 2:
                    growth_forecast, growth_confidence = self.linear_trend_forecast(
                        cat_timeline, 8
                    )  # 8 weeks

                    current_weekly_products = (
                        cat_timeline.iloc[-1] if len(cat_timeline) > 0 else 0
                    )
                    predicted_weekly_products = (
                        growth_forecast[7] if growth_forecast else 0
                    )

                    predictions.append(
                        PredictionResult(
                            metric=f"{category} Category Growth",
                            current_value=current_weekly_products,
                            predicted_value=predicted_weekly_products,
                            confidence_score=growth_confidence,
                            trend_direction=(
                                "expanding"
                                if predicted_weekly_products > current_weekly_products
                                else "contracting"
                            ),
                            prediction_date=datetime.now() + timedelta(weeks=8),
                            methodology="Category Growth Analysis",
                            supporting_data=[
                                f"Total products: {len(cat_data)}",
                                f"Average price: ${cat_data['price'].mean():.2f}",
                                f"Average rating: {cat_data['rating'].mean():.2f}",
                            ],
                        )
                    )

                # Category price trend
                cat_price_series = (
                    cat_data.set_index("created_date")["price"]
                    .resample("W")
                    .mean()
                    .fillna(method="ffill")
                )

                if len(cat_price_series) > 2:
                    price_forecast, price_confidence = (
                        self.exponential_smoothing_forecast(cat_price_series, 4)
                    )

                    predictions.append(
                        PredictionResult(
                            metric=f"{category} Average Price",
                            current_value=(
                                cat_price_series.iloc[-1]
                                if len(cat_price_series) > 0
                                else 0
                            ),
                            predicted_value=price_forecast[3] if price_forecast else 0,
                            confidence_score=price_confidence,
                            trend_direction=(
                                "increasing"
                                if (price_forecast[3] if price_forecast else 0)
                                > (
                                    cat_price_series.iloc[-1]
                                    if len(cat_price_series) > 0
                                    else 0
                                )
                                else "decreasing"
                            ),
                            prediction_date=datetime.now() + timedelta(weeks=4),
                            methodology="Price Trend Forecasting",
                            supporting_data=[
                                f"Price range: ${cat_data['price'].min():.2f} - ${cat_data['price'].max():.2f}",
                                f"Price volatility: {cat_price_series.std():.2f}",
                            ],
                        )
                    )

            logger.info(f"Generated {len(predictions)} category trend predictions")
            return predictions

        except Exception as e:
            logger.error(f"Error predicting category trends: {e}")
            return []

    def predict_demand_patterns(self) -> List[PredictionResult]:
        """Predict demand patterns and market opportunities"""
        try:
            if self.data is None or self.data.empty:
                self.load_historical_data()

            predictions = []

            # 1. High-demand price points
            price_demand = self.data.groupby(pd.cut(self.data["price"], bins=10))[
                "product_id"
            ].count()
            if len(price_demand) > 0:
                # Find most popular price range
                popular_range = price_demand.idxmax()
                demand_growth = price_demand.max()

                predictions.append(
                    PredictionResult(
                        metric="Optimal Price Range Demand",
                        current_value=demand_growth,
                        predicted_value=demand_growth * 1.15,  # 15% growth assumption
                        confidence_score=0.75,
                        trend_direction="increasing",
                        prediction_date=datetime.now() + timedelta(days=90),
                        methodology="Price-Demand Analysis",
                        supporting_data=[
                            f"Optimal range: ${popular_range.left:.2f} - ${popular_range.right:.2f}",
                            f"Current demand: {demand_growth} products",
                        ],
                    )
                )

            # 2. Brand performance prediction
            brand_performance = (
                self.data.groupby("brand")
                .agg({"product_id": "count", "rating": "mean", "price": "mean"})
                .sort_values("product_id", ascending=False)
            )

            if len(brand_performance) > 0:
                top_brand = brand_performance.index[0]
                brand_products = brand_performance.iloc[0]["product_id"]

                predictions.append(
                    PredictionResult(
                        metric=f"{top_brand} Brand Market Share",
                        current_value=(brand_products / len(self.data)) * 100,
                        predicted_value=((brand_products * 1.2) / len(self.data))
                        * 100,  # 20% growth
                        confidence_score=0.70,
                        trend_direction="expanding",
                        prediction_date=datetime.now() + timedelta(days=180),
                        methodology="Market Share Analysis",
                        supporting_data=[
                            f"Current products: {brand_products}",
                            f"Average rating: {brand_performance.iloc[0]['rating']:.2f}",
                            f"Average price: ${brand_performance.iloc[0]['price']:.2f}",
                        ],
                    )
                )

            # 3. Seasonal demand prediction
            if "created_date" in self.data.columns:
                monthly_creation = (
                    self.data.set_index("created_date")
                    .resample("M")["product_id"]
                    .count()
                )
                seasonality = self.detect_seasonality(monthly_creation)

                if seasonality["seasonal"]:
                    predictions.append(
                        PredictionResult(
                            metric="Seasonal Product Introduction",
                            current_value=(
                                monthly_creation.iloc[-1]
                                if len(monthly_creation) > 0
                                else 0
                            ),
                            predicted_value=(
                                monthly_creation.iloc[-1]
                                if len(monthly_creation) > 0
                                else 0
                            )
                            * 1.3,  # Seasonal boost
                            confidence_score=seasonality["strength"],
                            trend_direction="seasonal_peak",
                            prediction_date=datetime.now()
                            + timedelta(days=seasonality["period"]),
                            methodology="Seasonal Pattern Analysis",
                            supporting_data=[
                                f"Seasonal strength: {seasonality['strength']:.2f}",
                                f"Cycle period: {seasonality['period']} days",
                                f"Pattern detected: {'Yes' if seasonality['seasonal'] else 'No'}",
                            ],
                        )
                    )

            logger.info(f"Generated {len(predictions)} demand pattern predictions")
            return predictions

        except Exception as e:
            logger.error(f"Error predicting demand patterns: {e}")
            return []

    def generate_business_forecast(self, horizon_days: int = 90) -> dict:
        """Generate comprehensive business forecast"""
        try:
            logger.info(f"Generating {horizon_days}-day business forecast...")

            # Collect all predictions
            sales_predictions = self.predict_sales_performance()
            category_predictions = self.predict_category_trends()
            demand_predictions = self.predict_demand_patterns()

            all_predictions = (
                sales_predictions + category_predictions + demand_predictions
            )

            # Calculate overall confidence
            if all_predictions:
                avg_confidence = sum(p.confidence_score for p in all_predictions) / len(
                    all_predictions
                )
            else:
                avg_confidence = 0.5

            # Generate summary insights
            upward_trends = sum(
                1
                for p in all_predictions
                if p.trend_direction
                in ["upward", "increasing", "expanding", "improving"]
            )
            total_predictions = len(all_predictions)

            forecast_summary = {
                "forecast_date": datetime.now(),
                "horizon_days": horizon_days,
                "total_predictions": total_predictions,
                "average_confidence": avg_confidence,
                "positive_trends": upward_trends,
                "trend_ratio": (
                    (upward_trends / total_predictions) if total_predictions > 0 else 0
                ),
                "predictions": all_predictions,
                "key_insights": self._generate_key_insights(all_predictions),
                "recommendations": self._generate_recommendations(all_predictions),
            }

            logger.info(
                f"✅ Generated comprehensive forecast with {total_predictions} predictions"
            )
            return forecast_summary

        except Exception as e:
            logger.error(f"Error generating business forecast: {e}")
            return {"error": str(e)}

    def _generate_key_insights(self, predictions: List[PredictionResult]) -> List[str]:
        """Generate key business insights from predictions"""
        insights = []

        if not predictions:
            return ["Insufficient data for meaningful insights"]

        # Analyze trend directions
        trend_counts = {}
        for pred in predictions:
            trend_counts[pred.trend_direction] = (
                trend_counts.get(pred.trend_direction, 0) + 1
            )

        most_common_trend = (
            max(trend_counts.items(), key=lambda x: x[1])
            if trend_counts
            else ("neutral", 0)
        )

        insights.append(
            f"📈 Primary trend: {most_common_trend[1]} metrics showing {most_common_trend[0]} direction"
        )

        # High confidence predictions
        high_confidence = [p for p in predictions if p.confidence_score > 0.8]
        if high_confidence:
            insights.append(
                f"🎯 {len(high_confidence)} high-confidence predictions (>80% certainty)"
            )

        # Significant changes
        significant_changes = [
            p
            for p in predictions
            if abs(p.predicted_value - p.current_value) / max(p.current_value, 1) > 0.1
        ]
        if significant_changes:
            insights.append(
                f"⚡ {len(significant_changes)} metrics expected to change significantly (>10%)"
            )

        # Average confidence assessment
        avg_confidence = sum(p.confidence_score for p in predictions) / len(predictions)
        confidence_level = (
            "High"
            if avg_confidence > 0.75
            else "Medium" if avg_confidence > 0.5 else "Low"
        )
        insights.append(
            f"🔍 Overall forecast confidence: {confidence_level} ({avg_confidence:.1%})"
        )

        return insights

    def _generate_recommendations(
        self, predictions: List[PredictionResult]
    ) -> List[str]:
        """Generate actionable business recommendations"""
        recommendations = []

        if not predictions:
            return ["Collect more data for improved predictions"]

        # Price-related recommendations
        price_predictions = [p for p in predictions if "price" in p.metric.lower()]
        if price_predictions:
            increasing_prices = sum(
                1
                for p in price_predictions
                if p.trend_direction in ["upward", "increasing"]
            )
            if increasing_prices > len(price_predictions) / 2:
                recommendations.append(
                    "💰 Consider price optimization strategies as market trends suggest upward pricing pressure"
                )

        # Growth opportunities
        growth_predictions = [
            p
            for p in predictions
            if "growth" in p.metric.lower() or "expanding" in p.trend_direction
        ]
        if growth_predictions:
            recommendations.append(
                f"🚀 Focus investment on {len(growth_predictions)} expanding categories for maximum ROI"
            )

        # Risk mitigation
        declining_predictions = [
            p
            for p in predictions
            if p.trend_direction
            in ["downward", "decreasing", "declining", "contracting"]
        ]
        if declining_predictions:
            recommendations.append(
                f"⚠️ Monitor {len(declining_predictions)} declining metrics and implement corrective measures"
            )

        # Seasonal opportunities
        seasonal_predictions = [
            p for p in predictions if "seasonal" in p.trend_direction
        ]
        if seasonal_predictions:
            recommendations.append(
                "📅 Prepare seasonal inventory and marketing strategies based on detected patterns"
            )

        # High-confidence actions
        high_confidence = [p for p in predictions if p.confidence_score > 0.8]
        if high_confidence:
            recommendations.append(
                f"🎯 Prioritize actions on {len(high_confidence)} high-confidence predictions for immediate impact"
            )

        return recommendations


def main():
    """Main execution function"""
    print("🔮 GenETL Predictive Analytics Engine")
    print("=" * 50)

    # Initialize engine
    engine = PredictiveAnalyticsEngine()

    # Load data
    print("📊 Loading historical data...")
    engine.load_historical_data()

    if engine.data is None or engine.data.empty:
        print("❌ No data available for analysis")
        return

    # Generate comprehensive forecast
    print("🔄 Generating business forecasts...")
    forecast = engine.generate_business_forecast(90)  # 90-day forecast

    if "error" in forecast:
        print(f"❌ Error generating forecast: {forecast['error']}")
        return

    # Display results
    print(f"\n✅ Forecast Complete!")
    print(f"📅 Forecast Date: {forecast['forecast_date'].strftime('%Y-%m-%d %H:%M')}")
    print(f"🎯 Horizon: {forecast['horizon_days']} days")
    print(f"📊 Total Predictions: {forecast['total_predictions']}")
    print(f"🔍 Average Confidence: {forecast['average_confidence']:.1%}")
    print(
        f"📈 Positive Trends: {forecast['positive_trends']}/{forecast['total_predictions']} ({forecast['trend_ratio']:.1%})"
    )

    print(f"\n🧠 Key Insights:")
    for insight in forecast["key_insights"]:
        print(f"   • {insight}")

    print(f"\n💡 Recommendations:")
    for rec in forecast["recommendations"]:
        print(f"   • {rec}")

    print(f"\n📋 Detailed Predictions:")
    for i, pred in enumerate(forecast["predictions"][:8], 1):  # Show top 8
        direction_icon = (
            "📈"
            if pred.trend_direction
            in ["upward", "increasing", "expanding", "improving"]
            else "📉"
        )
        print(f"   {i}. {direction_icon} {pred.metric}")
        print(
            f"      Current: {pred.current_value:.2f} → Predicted: {pred.predicted_value:.2f}"
        )
        print(
            f"      Confidence: {pred.confidence_score:.1%} | Method: {pred.methodology}"
        )
        print(f"      Target Date: {pred.prediction_date.strftime('%Y-%m-%d')}")
        print()


if __name__ == "__main__":
    main()
