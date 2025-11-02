"""
GenETL AI Query Interface
Natural language to SQL converter with intelligent data exploration
"""

import logging
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class QueryResponse:
    """AI query response structure"""

    natural_query: str
    sql_query: str
    results: pd.DataFrame
    interpretation: str
    confidence: float
    suggestions: List[str]


class AIQueryInterface:
    """Natural Language Query Interface for GenETL Data"""

    def __init__(self):
        self.db_config = {
            "host": "localhost",
            "port": 5450,
            "database": "genetl_warehouse",
            "user": "genetl",
            "password": "genetl_pass",
        }
        self.engine = None
        self.schema_info = None
        self.query_patterns = self._initialize_query_patterns()

    def get_db_connection(self):
        """Establish database connection"""
        if not self.engine:
            connection_string = f"postgresql://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"
            self.engine = create_engine(connection_string)
        return self.engine

    def _initialize_query_patterns(self) -> Dict[str, Dict]:
        """Initialize AI query pattern recognition"""
        return {
            "aggregation": {
                "patterns": [
                    r"(how many|count|total number of)",
                    r"(average|avg|mean) (price|rating|cost)",
                    r"(sum|total) (price|revenue|sales)",
                    r"(maximum|max|highest) (price|rating)",
                    r"(minimum|min|lowest) (price|rating)",
                ],
                "sql_templates": {
                    "count": "SELECT COUNT(*) as count FROM warehouse.products",
                    "avg_price": "SELECT AVG(price) as average_price FROM warehouse.products",
                    "total_price": "SELECT SUM(price) as total_value FROM warehouse.products",
                    "max_price": "SELECT MAX(price) as max_price FROM warehouse.products",
                    "min_price": "SELECT MIN(price) as min_price FROM warehouse.products",
                },
            },
            "filtering": {
                "patterns": [
                    r"(products|items) (in|from) category (\w+)",
                    r"(products|items) (with|having) (price|rating) (greater|less|higher|lower|above|below) than (\d+)",
                    r"(products|items) (by|from) brand (\w+)",
                    r"(out of stock|low stock|in stock) (products|items)",
                    r"(expensive|cheap) (products|items)",
                ],
                "sql_templates": {
                    "category_filter": "SELECT * FROM warehouse.products WHERE category ILIKE '%{category}%'",
                    "price_filter": "SELECT * FROM warehouse.products WHERE price {operator} {value}",
                    "brand_filter": "SELECT * FROM warehouse.products WHERE brand ILIKE '%{brand}%'",
                    "stock_filter": "SELECT * FROM warehouse.products WHERE stock_status = '{status}'",
                    "price_range": "SELECT * FROM warehouse.products WHERE price {condition}",
                },
            },
            "comparison": {
                "patterns": [
                    r"compare (categories|brands)",
                    r"(best|worst) (selling|rated) (category|brand)",
                    r"(category|brand) (comparison|performance)",
                ],
                "sql_templates": {
                    "category_comparison": "SELECT category, COUNT(*) as product_count, AVG(price) as avg_price, AVG(rating) as avg_rating FROM warehouse.products GROUP BY category ORDER BY avg_rating DESC",
                    "brand_comparison": "SELECT brand, COUNT(*) as product_count, AVG(price) as avg_price, AVG(rating) as avg_rating FROM warehouse.products GROUP BY brand ORDER BY avg_rating DESC",
                },
            },
            "trending": {
                "patterns": [
                    r"(trending|popular|top) (products|items)",
                    r"(best|highest|top) (rated|selling) (products|items)",
                    r"(recent|new|latest) (products|items)",
                ],
                "sql_templates": {
                    "top_rated": "SELECT product_name, category, brand, rating, price FROM warehouse.products ORDER BY rating DESC LIMIT 10",
                    "recent_products": "SELECT product_name, category, brand, rating, price, created_date FROM warehouse.products ORDER BY created_date DESC LIMIT 10",
                },
            },
        }

    def load_schema_info(self) -> Dict[str, Any]:
        """Load database schema information for AI context"""
        try:
            engine = self.get_db_connection()

            # Get table structure
            schema_query = """
            SELECT 
                column_name,
                data_type,
                is_nullable
            FROM information_schema.columns 
            WHERE table_schema = 'warehouse' 
            AND table_name = 'products'
            ORDER BY ordinal_position
            """

            columns_df = pd.read_sql(schema_query, engine)

            # Get sample data for context
            sample_query = "SELECT * FROM warehouse.products LIMIT 5"
            sample_df = pd.read_sql(sample_query, engine)

            # Get unique values for categorical columns
            categorical_info = {}
            for col in ["category", "brand", "stock_status"]:
                try:
                    unique_query = f"SELECT DISTINCT {col} FROM warehouse.products WHERE {col} IS NOT NULL LIMIT 20"
                    unique_df = pd.read_sql(unique_query, engine)
                    categorical_info[col] = unique_df[col].tolist()
                except:
                    categorical_info[col] = []

            self.schema_info = {
                "columns": columns_df.to_dict("records"),
                "sample_data": sample_df.to_dict("records"),
                "categorical_values": categorical_info,
                "table_name": "warehouse.products",
            }

            logger.info("Schema information loaded successfully")
            return self.schema_info

        except Exception as e:
            logger.error(f"Error loading schema info: {e}")
            return {}

    def parse_natural_query(self, natural_query: str) -> Dict[str, Any]:
        """Parse natural language query using AI pattern recognition"""
        query_lower = natural_query.lower().strip()

        parsed = {
            "intent": "unknown",
            "entities": {},
            "sql_template": None,
            "confidence": 0.0,
            "parameters": {},
        }

        # Check each pattern category
        for category, info in self.query_patterns.items():
            for pattern in info["patterns"]:
                match = re.search(pattern, query_lower)
                if match:
                    parsed["intent"] = category
                    parsed["confidence"] = 0.8

                    # Extract entities based on pattern
                    if category == "aggregation":
                        if "count" in query_lower or "how many" in query_lower:
                            parsed["sql_template"] = "count"
                        elif "average" in query_lower or "avg" in query_lower:
                            parsed["sql_template"] = "avg_price"
                        elif "sum" in query_lower or "total" in query_lower:
                            parsed["sql_template"] = "total_price"
                        elif "max" in query_lower or "highest" in query_lower:
                            parsed["sql_template"] = "max_price"
                        elif "min" in query_lower or "lowest" in query_lower:
                            parsed["sql_template"] = "min_price"

                    elif category == "filtering":
                        # Extract category
                        category_match = re.search(r"category (\w+)", query_lower)
                        if category_match:
                            parsed["entities"]["category"] = category_match.group(1)
                            parsed["sql_template"] = "category_filter"

                        # Extract brand
                        brand_match = re.search(r"brand (\w+)", query_lower)
                        if brand_match:
                            parsed["entities"]["brand"] = brand_match.group(1)
                            parsed["sql_template"] = "brand_filter"

                        # Extract price conditions
                        price_match = re.search(
                            r"price (greater|less|higher|lower|above|below) than (\d+)",
                            query_lower,
                        )
                        if price_match:
                            operator = (
                                ">"
                                if price_match.group(1)
                                in ["greater", "higher", "above"]
                                else "<"
                            )
                            parsed["entities"]["operator"] = operator
                            parsed["entities"]["value"] = price_match.group(2)
                            parsed["sql_template"] = "price_filter"

                        # Extract stock status
                        if "out of stock" in query_lower:
                            parsed["entities"]["status"] = "Out of Stock"
                            parsed["sql_template"] = "stock_filter"
                        elif "low stock" in query_lower:
                            parsed["entities"]["status"] = "Low Stock"
                            parsed["sql_template"] = "stock_filter"
                        elif "in stock" in query_lower:
                            parsed["entities"]["status"] = "In Stock"
                            parsed["sql_template"] = "stock_filter"

                    elif category == "comparison":
                        if "categor" in query_lower:
                            parsed["sql_template"] = "category_comparison"
                        elif "brand" in query_lower:
                            parsed["sql_template"] = "brand_comparison"

                    elif category == "trending":
                        if (
                            "recent" in query_lower
                            or "new" in query_lower
                            or "latest" in query_lower
                        ):
                            parsed["sql_template"] = "recent_products"
                        else:
                            parsed["sql_template"] = "top_rated"

                    break

            if parsed["intent"] != "unknown":
                break

        return parsed

    def build_sql_query(self, parsed_query: Dict[str, Any]) -> str:
        """Build SQL query from parsed natural language"""
        try:
            intent = parsed_query["intent"]
            sql_template = parsed_query.get("sql_template")
            entities = parsed_query.get("entities", {})

            if intent == "unknown" or not sql_template:
                return "SELECT * FROM warehouse.products LIMIT 10"  # Default fallback

            # Get base SQL template
            base_sql = self.query_patterns[intent]["sql_templates"].get(
                sql_template, ""
            )

            # Replace placeholders with entities
            if entities:
                for key, value in entities.items():
                    placeholder = "{" + key + "}"
                    if placeholder in base_sql:
                        base_sql = base_sql.replace(placeholder, str(value))

            return base_sql

        except Exception as e:
            logger.error(f"Error building SQL query: {e}")
            return "SELECT * FROM warehouse.products LIMIT 10"

    def execute_query(self, sql_query: str) -> pd.DataFrame:
        """Execute SQL query and return results"""
        try:
            engine = self.get_db_connection()
            df = pd.read_sql(sql_query, engine)
            logger.info(f"Query executed successfully, returned {len(df)} rows")
            return df

        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return pd.DataFrame()

    def generate_interpretation(
        self, natural_query: str, sql_query: str, results: pd.DataFrame
    ) -> str:
        """Generate AI interpretation of query results"""
        try:
            if results.empty:
                return "No results found for your query. Try refining your search criteria."

            row_count = len(results)

            # Generate contextual interpretation based on query type
            if "count" in sql_query.lower():
                if "COUNT(*)" in sql_query:
                    count_value = results.iloc[0, 0] if not results.empty else 0
                    return f"Found {count_value:,} total products in the database."

            elif "avg" in sql_query.lower():
                if not results.empty:
                    avg_value = results.iloc[0, 0]
                    if "price" in sql_query.lower():
                        return f"The average price across all products is ${avg_value:.2f}."
                    elif "rating" in sql_query.lower():
                        return f"The average rating across all products is {avg_value:.2f}/5.0."

            elif "max" in sql_query.lower():
                if not results.empty:
                    max_value = results.iloc[0, 0]
                    if "price" in sql_query.lower():
                        return f"The highest priced product costs ${max_value:.2f}."
                    elif "rating" in sql_query.lower():
                        return f"The highest rated product has a {max_value:.2f}/5.0 rating."

            elif "group by category" in sql_query.lower():
                categories = len(results)
                return f"Analysis across {categories} product categories. Results sorted by performance metrics."

            elif "group by brand" in sql_query.lower():
                brands = len(results)
                return f"Comparison of {brands} different brands based on key performance indicators."

            elif "order by rating desc" in sql_query.lower():
                return f"Top {row_count} highest-rated products, sorted by customer satisfaction."

            elif "order by created_date desc" in sql_query.lower():
                return f"Most recent {row_count} products added to the catalog."

            elif "where" in sql_query.lower():
                return f"Found {row_count} products matching your filter criteria."

            # Default interpretation
            return f"Query returned {row_count} results. Data shows product information from the warehouse."

        except Exception as e:
            logger.error(f"Error generating interpretation: {e}")
            return "Results retrieved successfully. Review the data for insights."

    def generate_suggestions(
        self, natural_query: str, results: pd.DataFrame
    ) -> List[str]:
        """Generate AI-powered follow-up suggestions"""
        suggestions = []

        try:
            query_lower = natural_query.lower()

            # Context-based suggestions
            if "category" in query_lower and not results.empty:
                suggestions.append("Try: 'Compare all categories by average rating'")
                suggestions.append(
                    "Ask: 'Which category has the most expensive products?'"
                )

            elif "brand" in query_lower and not results.empty:
                suggestions.append(
                    "Try: 'Show me the top rated products from each brand'"
                )
                suggestions.append("Ask: 'Which brand has the highest average price?'")

            elif "price" in query_lower:
                suggestions.append("Try: 'Show products with rating above 4.0'")
                suggestions.append("Ask: 'What's the price range for each category?'")

            elif "count" in query_lower or "how many" in query_lower:
                suggestions.append("Try: 'Show me the average price by category'")
                suggestions.append("Ask: 'Which category has the most products?'")

            elif "rating" in query_lower:
                suggestions.append("Try: 'Show products with price above $500'")
                suggestions.append("Ask: 'Which products have the lowest ratings?'")

            # Always include some general suggestions
            if len(suggestions) < 3:
                general_suggestions = [
                    "Try: 'Show me trending products'",
                    "Ask: 'Compare categories by performance'",
                    "Try: 'Show out of stock products'",
                    "Ask: 'What are the most expensive products?'",
                    "Try: 'Show recent products'",
                ]

                for suggestion in general_suggestions:
                    if suggestion not in suggestions:
                        suggestions.append(suggestion)
                        if len(suggestions) >= 3:
                            break

            return suggestions[:3]  # Return top 3 suggestions

        except Exception as e:
            logger.error(f"Error generating suggestions: {e}")
            return [
                "Try: 'Show me all categories'",
                "Ask: 'What's the average price?'",
                "Try: 'Show top rated products'",
            ]

    def process_natural_query(self, natural_query: str) -> QueryResponse:
        """Process complete natural language query pipeline"""
        try:
            logger.info(f"Processing query: {natural_query}")

            # Ensure schema info is loaded
            if not self.schema_info:
                self.load_schema_info()

            # Parse natural language
            parsed = self.parse_natural_query(natural_query)

            # Build SQL query
            sql_query = self.build_sql_query(parsed)

            # Execute query
            results = self.execute_query(sql_query)

            # Generate interpretation and suggestions
            interpretation = self.generate_interpretation(
                natural_query, sql_query, results
            )
            suggestions = self.generate_suggestions(natural_query, results)

            response = QueryResponse(
                natural_query=natural_query,
                sql_query=sql_query,
                results=results,
                interpretation=interpretation,
                confidence=parsed.get("confidence", 0.5),
                suggestions=suggestions,
            )

            logger.info(
                f"Query processed successfully with {parsed.get('confidence', 0.5):.0%} confidence"
            )
            return response

        except Exception as e:
            logger.error(f"Error processing natural query: {e}")
            return QueryResponse(
                natural_query=natural_query,
                sql_query="SELECT 'Error' as message",
                results=pd.DataFrame(),
                interpretation="Sorry, I couldn't process your query. Please try rephrasing it.",
                confidence=0.0,
                suggestions=[
                    "Try: 'Show me all products'",
                    "Ask: 'What categories do you have?'",
                ],
            )

    def interactive_query_session(self):
        """Start interactive AI query session"""
        print("🤖 GenETL AI Query Interface")
        print("=" * 50)
        print("Ask me anything about your product data in natural language!")
        print("Examples:")
        print("  • 'How many products do we have?'")
        print("  • 'Show me electronics products'")
        print("  • 'Compare categories by average rating'")
        print("  • 'What are the most expensive products?'")
        print("\nType 'exit' to quit, 'help' for more examples\n")

        while True:
            try:
                user_input = input("🗣️  Ask me: ").strip()

                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("👋 Thanks for using GenETL AI Query Interface!")
                    break

                elif user_input.lower() == "help":
                    self._show_help_examples()
                    continue

                elif not user_input:
                    print("Please enter a question about your data.")
                    continue

                # Process the query
                print(f"\n🤖 Processing: '{user_input}'...")
                response = self.process_natural_query(user_input)

                # Display results
                print(f"\n📊 Results (Confidence: {response.confidence:.0%}):")
                print(f"💡 {response.interpretation}")

                if not response.results.empty:
                    print(f"\n📋 Data ({len(response.results)} rows):")
                    if len(response.results) <= 10:
                        print(response.results.to_string(index=False))
                    else:
                        print(response.results.head(10).to_string(index=False))
                        print(f"\n... and {len(response.results) - 10} more rows")

                print(f"\n🔧 SQL Query: {response.sql_query}")

                print(f"\n💭 Suggestions:")
                for suggestion in response.suggestions:
                    print(f"   {suggestion}")

                print("\n" + "─" * 60)

            except KeyboardInterrupt:
                print("\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again with a different question.")

    def _show_help_examples(self):
        """Show help examples for users"""
        examples = [
            "Basic Counts:",
            "  • 'How many products do we have?'",
            "  • 'Count products in electronics category'",
            "",
            "Filtering & Search:",
            "  • 'Show me products from Apple brand'",
            "  • 'Products with price above 100'",
            "  • 'Out of stock products'",
            "",
            "Analytics & Comparisons:",
            "  • 'Average price by category'",
            "  • 'Compare brands by rating'",
            "  • 'Most expensive products'",
            "",
            "Trending & Performance:",
            "  • 'Top rated products'",
            "  • 'Recent products'",
            "  • 'Best selling category'",
        ]

        print("\n📚 Query Examples:")
        print("=" * 30)
        for example in examples:
            print(example)
        print()


def main():
    """Main execution function"""
    # Initialize AI Query Interface
    ai_query = AIQueryInterface()

    # Load schema information
    ai_query.load_schema_info()

    # Start interactive session
    ai_query.interactive_query_session()


if __name__ == "__main__":
    main()
