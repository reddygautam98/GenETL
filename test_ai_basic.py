"""
Basic tests for AI modules in GenETL project.
Tests the AI module classes and their basic functionality.
"""

import os
import sys

import pytest

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import AI modules (must be after sys.path modification)
from ai_insights_generator import GenETLAIAnalyzer  # noqa: E402
from ai_query_interface import AIQueryInterface  # noqa: E402
from ai_report_generator import AIReportGenerator  # noqa: E402
from predictive_analytics_engine import PredictiveAnalyticsEngine  # noqa: E402
from smart_data_quality_ai import SmartDataQualityAI  # noqa: E402


class TestGenETLAIAnalyzer:
    """Test cases for GenETLAIAnalyzer class."""

    def test_analyzer_initialization(self):
        """Test that GenETLAIAnalyzer can be initialized."""
        analyzer = GenETLAIAnalyzer()
        assert analyzer is not None

    def test_analyze_data(self):
        """Test analyze_data method returns expected structure."""
        analyzer = GenETLAIAnalyzer()
        result = analyzer.analyze_data({"test": "data"})
        assert isinstance(result, dict)
        assert "status" in result
        assert "insights" in result

    def test_generate_insights(self):
        """Test generate_insights method returns a list."""
        analyzer = GenETLAIAnalyzer()
        insights = analyzer.generate_insights({"test": "data"})
        assert isinstance(insights, list)
        assert len(insights) > 0

    def test_create_report(self):
        """Test create_report method returns a string."""
        analyzer = GenETLAIAnalyzer()
        report = analyzer.create_report([{"type": "test", "message": "test"}])
        assert isinstance(report, str)
        assert len(report) > 0


class TestAIQueryInterface:
    """Test cases for AIQueryInterface class."""

    def test_query_interface_initialization(self):
        """Test that AIQueryInterface can be initialized."""
        interface = AIQueryInterface()
        assert interface is not None

    def test_execute_query(self):
        """Test execute_query method returns expected structure."""
        interface = AIQueryInterface()
        result = interface.execute_query("SELECT * FROM test")
        assert isinstance(result, dict)
        assert "status" in result
        assert "query" in result

    def test_process_natural_language_query(self):
        """Test natural language query processing."""
        interface = AIQueryInterface()
        result = interface.process_natural_language_query("Show me all users")
        assert isinstance(result, dict)
        assert "status" in result
        assert "query" in result

    def test_get_query_results(self):
        """Test get_query_results method returns a list."""
        interface = AIQueryInterface()
        results = interface.get_query_results("test_query_id")
        assert isinstance(results, list)


class TestAIReportGenerator:
    """Test cases for AIReportGenerator class."""

    def test_report_generator_initialization(self):
        """Test that AIReportGenerator can be initialized."""
        generator = AIReportGenerator()
        assert generator is not None

    def test_generate_report(self):
        """Test generate_report method returns a string."""
        generator = AIReportGenerator()
        report = generator.generate_report({"test": "data"})
        assert isinstance(report, str)
        assert len(report) > 0

    def test_create_dashboard(self):
        """Test create_dashboard method returns a dictionary."""
        generator = AIReportGenerator()
        dashboard = generator.create_dashboard({"test": "data"})
        assert isinstance(dashboard, dict)
        assert "status" in dashboard

    def test_export_report(self):
        """Test export_report method returns a string."""
        generator = AIReportGenerator()
        export_result = generator.export_report("Test report", "pdf")
        assert isinstance(export_result, str)
        assert "pdf" in export_result.lower()


class TestPredictiveAnalyticsEngine:
    """Test cases for PredictiveAnalyticsEngine class."""

    def test_engine_initialization(self):
        """Test that PredictiveAnalyticsEngine can be initialized."""
        engine = PredictiveAnalyticsEngine()
        assert engine is not None

    def test_train_model(self):
        """Test train_model method executes without error."""
        engine = PredictiveAnalyticsEngine()
        # Should not raise an exception
        engine.train_model({"test": "data"})

    def test_predict(self):
        """Test predict method returns a list of floats."""
        engine = PredictiveAnalyticsEngine()
        predictions = engine.predict({"test": "data"})
        assert isinstance(predictions, list)
        assert len(predictions) > 0
        assert all(isinstance(p, float) for p in predictions)

    def test_evaluate_model(self):
        """Test evaluate_model method returns expected metrics."""
        engine = PredictiveAnalyticsEngine()
        metrics = engine.evaluate_model({"test": "data"})
        assert isinstance(metrics, dict)
        assert "accuracy" in metrics
        assert "precision" in metrics
        assert "recall" in metrics


class TestSmartDataQualityAI:
    """Test cases for SmartDataQualityAI class."""

    def test_quality_ai_initialization(self):
        """Test that SmartDataQualityAI can be initialized."""
        quality_ai = SmartDataQualityAI()
        assert quality_ai is not None

    def test_check_data_quality(self):
        """Test check_data_quality method returns expected structure."""
        quality_ai = SmartDataQualityAI()
        result = quality_ai.check_data_quality({"test": "data"})
        assert isinstance(result, dict)
        assert "status" in result
        assert "quality_score" in result
        assert "issues" in result

    def test_detect_anomalies(self):
        """Test detect_anomalies method returns a list."""
        quality_ai = SmartDataQualityAI()
        anomalies = quality_ai.detect_anomalies({"test": "data"})
        assert isinstance(anomalies, list)
        assert len(anomalies) > 0

    def test_suggest_improvements(self):
        """Test suggest_improvements method returns a list of strings."""
        quality_ai = SmartDataQualityAI()
        suggestions = quality_ai.suggest_improvements({"quality_score": 0.5})
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
        assert all(isinstance(s, str) for s in suggestions)


def test_all_ai_modules_importable():
    """Test that all AI modules can be imported without errors."""
    # This test ensures all modules are properly structured
    modules = [
        "ai_insights_generator",
        "ai_query_interface",
        "ai_report_generator",
        "predictive_analytics_engine",
        "smart_data_quality_ai",
    ]

    for module_name in modules:
        try:
            __import__(module_name)
        except ImportError as e:
            pytest.fail(f"Failed to import {module_name}: {e}")


if __name__ == "__main__":
    # Allow running this test file directly
    pytest.main([__file__])
