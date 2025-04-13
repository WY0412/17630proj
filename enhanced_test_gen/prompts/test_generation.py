SYSTEM_PROMPT = """
You are an expert Python developer specializing in test generation. Your task is to write effective pytest test cases that achieve high code coverage.

Follow these guidelines:
1. Focus on writing tests that increase line coverage
2. Pay special attention to conditional branches, exception handling, and edge cases
3. Each test should test a single aspect of the code
4. Write clear test functions with descriptive names
5. Generate tests that will run successfully when added to the existing test file
"""

USER_PROMPT_TEMPLATE = """
## Source Code
Here is the Python source code for which you need to generate tests:
```python
{{ source_code }}
```

{% if coverage_report %}
## Current Coverage Status
{{ coverage_report }}
{% else %}
## Coverage Status
No existing coverage data available. This is the first iteration.
{% endif %}

{% if existing_tests %}
## Existing Tests
Here are the existing tests:
```python
{{ existing_tests }}
```
{% endif %}

## Task
This is iteration {{ iteration }} of test generation. Your goal is to write additional pytest test cases that increase line coverage to at least {{ target_coverage }}% by covering untested lines.

{% if coverage_report %}
Focus on testing the uncovered lines mentioned in the report above. Write tests specifically designed to execute those code paths.
{% else %}
Since this is the first iteration, focus on comprehensive testing of the main functionality.
{% endif %}

For each function in the source code:
1. Create tests for normal inputs
2. Create tests for edge cases
3. Create tests for error conditions where applicable

## Important Requirements
- Your tests must use pytest and should follow pytest conventions
- Tests must be runnable immediately without modifications
- Use descriptive test names that explain what they're testing
- Do not duplicate existing tests
- Focus on increasing line coverage
- DO NOT include any import statements in your code. The testing framework will automatically add all necessary imports.

Return ONLY runnable pytest test code without explanations or markdown formatting.
"""

def build_prompt(source_code, existing_tests=None, coverage_report=None, iteration=1, target_coverage=80):
    """Build the prompt for test generation."""
    from jinja2 import Template
    
    system = SYSTEM_PROMPT
    user = Template(USER_PROMPT_TEMPLATE).render(
        source_code=source_code,
        existing_tests=existing_tests,
        coverage_report=coverage_report,
        iteration=iteration,
        target_coverage=target_coverage
    )
    
    return {
        "system": system,
        "user": user
    }