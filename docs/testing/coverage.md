# Test Coverage Reports

This page provides access to the comprehensive test coverage reports for the Bewerbung Generator project.

## Coverage Overview

The project uses `pytest-cov` and `coverage` to track test coverage across all source code modules. Our current coverage targets:

- **Minimum Coverage**: 40% (current threshold)
- **Target Coverage**: 75% (future goal)
- **Critical Modules**: Template Manager, AI Client Factory, PDF Generator

## Current Coverage Status

📊 **Latest Coverage Report**: [📈 View Interactive HTML Coverage Report](../_static/coverage/index.html)

## Running Coverage Tests

To generate fresh coverage reports, use the following Makefile targets:

### Full Test Suite with Coverage

```bash
make test-coverage
```

This runs all tests and generates both HTML and XML coverage reports.

### Generate HTML Report Only

```bash
make coverage-report
```

### Generate XML Report (for CI/CD)

```bash
make coverage-xml
```

### Clean Coverage Data

```bash
make coverage-clean
```

## Coverage Configuration

Coverage settings are configured in `pyproject.toml`:

```toml
[tool.coverage.run]
source = ["src"]
omit = [
    "tests/*",
    "*/conftest.py",
    "*/__pycache__/*",
    "setup.py",
    "docs/*"
]

[tool.coverage.report]
show_missing = true
skip_covered = false
precision = 2
fail_under = 40

[tool.coverage.html]
directory = "docs/_static/coverage"
title = "Bewerbung Generator Test Coverage Report"
```

## Understanding Coverage Reports

The HTML coverage report provides detailed information about:

- **Module Coverage**: Overall percentage of code lines executed during tests
- **Missing Lines**: Specific line numbers not covered by tests
- **Branch Coverage**: Coverage of conditional statements and code branches
- **Function Coverage**: Which functions have been called during testing

## Coverage Targets by Module

| Module | Current Coverage | Target Coverage |
|--------|------------------|-----------------|
| template_manager.py | 78% | 85% |
| pdf_generator.py | 75% | 85% |
| ai_client_factory.py | 61% | 80% |
| base_ai_client.py | 67% | 80% |

## Improving Coverage

To improve test coverage:

1. **Identify Uncovered Code**: Use the HTML report to find untested lines
2. **Add Unit Tests**: Write tests for uncovered functions and methods
3. **Integration Tests**: Test end-to-end workflows
4. **Edge Cases**: Test error conditions and boundary cases

### Key Areas for Improvement

- AI provider error handling
- PDF generation edge cases
- Template rendering with various data combinations
- File system operations and error conditions

## CI/CD Integration

The coverage reports are generated in formats suitable for continuous integration:

- **HTML Reports**: For developer review and documentation
- **XML Reports**: For integration with CI/CD systems and coverage badges
- **Terminal Output**: For quick feedback during development

## Coverage Best Practices

### Writing Testable Code
- Keep functions small and focused
- Minimize dependencies and side effects
- Use dependency injection for external services

### Effective Testing
- Test both success and failure paths
- Use fixtures for consistent test data
- Mock external dependencies appropriately

### Coverage Interpretation
- 100% coverage doesn't guarantee bug-free code
- Focus on testing critical business logic
- Use coverage to identify untested code paths

## Related Resources

- [General Testing Documentation](../development/testing.md)
- [Contribution Guidelines](../development/contributing.md)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)