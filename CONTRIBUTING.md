# Contributing to GenETL

First off, thank you for considering contributing to GenETL! It's people like you that make GenETL such a great tool for the data engineering community.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [reddygautam98@gmail.com](mailto:reddygautam98@gmail.com).

## How Can I Contribute?

### 🐛 Reporting Bugs

This section guides you through submitting a bug report for GenETL. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

**Before Submitting A Bug Report:**
- Check the debugging guide
- Check the FAQ for common issues
- Perform a cursory search to see if the problem has already been reported

**How Do I Submit A Good Bug Report?**

Bugs are tracked as GitHub issues. Create an issue and provide the following information:

- **Use a clear and descriptive title** for the issue to identify the problem
- **Describe the exact steps which reproduce the problem** in as many details as possible
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior
- **Explain which behavior you expected to see instead and why**
- **Include screenshots and animated GIFs** if possible
- **Include your environment details:**
  - OS and version
  - Python version
  - Docker version
  - GenETL version
  - Database details

### 🚀 Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for GenETL, including completely new features and minor improvements to existing functionality.

**Before Submitting An Enhancement Suggestion:**
- Check if the enhancement has already been suggested
- Check if the enhancement fits with the project's goals
- Determine which repository the enhancement should be suggested in

**How Do I Submit A Good Enhancement Suggestion?**

Enhancement suggestions are tracked as GitHub issues. Create an issue and provide the following information:

- **Use a clear and descriptive title** for the issue to identify the suggestion
- **Provide a step-by-step description of the suggested enhancement** in as many details as possible
- **Provide specific examples to demonstrate the steps or point out the part which the suggestion is related to**
- **Describe the current behavior** and **explain which behavior you expected to see instead** and why
- **Explain why this enhancement would be useful** to most GenETL users

### 💻 Pull Requests

The process described here has several goals:
- Maintain GenETL's quality
- Fix problems that are important to users
- Engage the community in working toward the best possible GenETL
- Enable a sustainable system for GenETL's maintainers to review contributions

**Pull Request Process:**

1. **Fork the repository** and create your branch from `main`
2. **Install dependencies** and set up development environment
3. **Make your changes** following our coding standards
4. **Add tests** for your changes
5. **Update documentation** if needed
6. **Run the test suite** to ensure everything works
7. **Commit your changes** with a clear commit message
8. **Push to your fork** and submit a pull request

## Development Environment Setup

### Prerequisites

- Python 3.13+
- Docker and Docker Compose
- Git
- PostgreSQL client (optional, for direct database access)

### Setting Up Your Development Environment

1. **Clone your fork:**
   ```bash
   git clone https://github.com/your-username/GenETL.git
   cd GenETL
   ```

2. **Set up Python environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your local configuration
   ```

4. **Start the development environment:**
   ```bash
   docker-compose up -d
   ```

5. **Run tests to ensure everything works:**
   ```bash
   python test_ai_basic.py
   ```

### 🧪 Running Tests

We use pytest for our test suite. Here are the commands you need to know:

```bash
# Run all tests
pytest

# Run specific test file
python test_ai_basic.py

# Run comprehensive demo
python demo_ai_features.py

# Run with coverage
pytest --cov=. --cov-report=html
```

### 🎨 Code Style

We follow PEP 8 with some modifications. Here are the key points:

- **Line length:** Maximum 100 characters
- **Indentation:** 4 spaces (no tabs)
- **Imports:** One import per line, grouped by standard library, third-party, and local
- **Docstrings:** Use Google-style docstrings
- **Type hints:** Use type hints for all function parameters and return values

**Formatting Tools:**
```bash
# Install formatting tools
pip install black flake8 isort mypy

# Format code
black .
isort .

# Check code style
flake8 .

# Type checking
mypy .
```

### 📝 Commit Guidelines

We follow conventional commits for clear history:

**Format:** `<type>(<scope>): <description>`

**Types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

**Examples:**
```bash
git commit -m "feat(ai): add new predictive analytics model"
git commit -m "fix(db): resolve connection timeout issue"
git commit -m "docs(readme): update installation instructions"
```

## 🏗️ Project Structure

Understanding the project structure will help you contribute effectively:

```
GenETL/
├── ai_insights_generator.py        # AI business intelligence
├── smart_data_quality_ai.py        # Data quality validation
├── ai_query_interface.py           # Natural language queries
├── ai_report_generator.py          # Report generation
├── predictive_analytics_engine.py  # ML forecasting
├── dags/                           # Airflow DAGs
│   └── ai_enhanced_etl_dag.py
├── tests/                          # Test files
│   ├── test_ai_basic.py
│   └── demo_ai_features.py
├── docs/                           # Documentation
├── docker-compose.yml              # Container setup
├── requirements.txt                # Python dependencies
└── .env.example                    # Environment template
```

## 🧠 AI Components Development

When contributing to AI components, consider:

### Data Quality Standards
- All AI functions should handle missing data gracefully
- Include confidence scores in AI-generated insights
- Validate data types and ranges before processing
- Provide meaningful error messages

### Performance Guidelines
- Optimize database queries for large datasets
- Use connection pooling for database access
- Cache frequently accessed data
- Profile code for performance bottlenecks

### Testing AI Features
- Test with various data scenarios (empty, small, large datasets)
- Validate AI model outputs for reasonableness
- Test error handling with invalid inputs
- Include integration tests with the database

## 📋 AI Component Checklist

When adding new AI features, ensure:

- [ ] **Database Integration:** Connects to PostgreSQL properly
- [ ] **Error Handling:** Graceful error handling and logging
- [ ] **Configuration:** Uses environment variables for settings
- [ ] **Documentation:** Comprehensive docstrings and examples
- [ ] **Testing:** Unit tests and integration tests
- [ ] **Performance:** Optimized for production use
- [ ] **Airflow Integration:** Compatible with existing DAG structure
- [ ] **Type Safety:** Type hints for all functions
- [ ] **Logging:** Appropriate logging levels and messages

## 🔄 ETL Pipeline Contributions

When modifying the ETL pipeline:

1. **Understand the Flow:** Extract → Validate → Transform → Load → Analyze
2. **Maintain Compatibility:** Ensure changes work with existing components
3. **Add Monitoring:** Include appropriate logging and metrics
4. **Test Thoroughly:** Test with real data scenarios
5. **Update DAG:** Modify Airflow DAG if needed

## 🐳 Docker Development

For Docker-related contributions:

- Test changes in clean environment
- Update documentation for new containers
- Ensure compatibility across platforms
- Optimize image sizes
- Follow security best practices

## 📖 Documentation

We use Markdown for documentation. When contributing docs:

- Keep language clear and concise
- Include code examples
- Add screenshots for UI changes
- Update relevant sections
- Check links are working

## 🚀 Release Process

For maintainers releasing new versions:

1. Update version numbers
2. Update CHANGELOG.md
3. Create release notes
4. Tag the release
5. Update Docker images
6. Announce the release

## 💬 Communication

- **GitHub Issues:** For bug reports and feature requests
- **GitHub Discussions:** For questions and general discussion
- **Email:** [reddygautam98@gmail.com](mailto:reddygautam98@gmail.com) for security issues

## 🎯 Roadmap

Current development priorities:

1. **Enhanced AI Models:** More sophisticated ML algorithms
2. **Real-time Processing:** Streaming data support
3. **API Endpoints:** REST API for external integration
4. **Enhanced Security:** Better authentication and authorization
5. **Performance Optimization:** Faster processing for large datasets

## 🙏 Recognition

Contributors will be:
- Listed in the AUTHORS file
- Mentioned in release notes
- Credited in relevant documentation

Thank you for contributing to GenETL! Your contributions make the project better for everyone.