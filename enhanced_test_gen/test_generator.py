import os
import re
from pathlib import Path
import subprocess
import json
from enhanced_test_gen.ai_caller import AICaller
from enhanced_test_gen.test_runner import TestRunner
from enhanced_test_gen.prompts.test_generation import build_prompt

class TestGenerator:
    def __init__(self, source_file, test_file=None, model="gpt-4", target_coverage=80):
        """
        Initialize the enhanced test generator.
        
        Args:
            source_file: Path to the source file
            test_file: Path to the test file (default: test_<source>.py)
            model: AI model to use
            target_coverage: Target coverage percentage
        """
        self.source_file = source_file
        
        # If test file not specified, create one based on source filename
        if test_file is None:
            source_basename = os.path.basename(source_file)
            source_name = os.path.splitext(source_basename)[0]
            self.test_file = os.path.join(os.path.dirname(source_file), f"test_{source_name}.py")
        else:
            self.test_file = test_file
            
        self.ai_caller = AICaller(model=model)
        self.test_runner = TestRunner(self.test_file)
        self.target_coverage = target_coverage
    
    def read_source_code(self):
        """Read the source code file."""
        with open(self.source_file, "r") as f:
            return f.read()
    
    def read_source_json(self):
        """Read the source code file."""
        with open(self.source_file, "r") as f:
            return json.load(f)
    
    def read_existing_tests(self):
        """Read existing test file if it exists."""
        if os.path.exists(self.test_file):
            with open(self.test_file, "r") as f:
                return f.read()
        return None
    
    def save_tests(self, tests):
        """
        Save generated tests to the test file.
        
        Args:
            tests: Generated test code
            append: Whether to append to existing file
        """
        
        # Write or append to file
        with open(self.test_file, "w") as f:
            f.write(tests)
        
        print(f"Tests saved to {self.test_file}")
        
    def _ensure_required_imports(self, tests):
        """Ensure tests have the correct import statements, excluding class methods"""
        
        # Get module and package names
        module_name = os.path.splitext(os.path.basename(self.source_file))[0]
        dir_name = os.path.basename(os.path.dirname(self.source_file))
        
        # Analyze source file to extract functions and classes
        try:
            with open(self.source_file, 'r') as f:
                source_code = f.read()
                
            # Use regex to identify top-level functions and classes (not inside class definitions)
            import re
            
            # Match class definitions
            class_pattern = re.compile(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[:\(]')
            classes = class_pattern.findall(source_code)
            
            # Match non-class methods (top-level functions) - simplified version
            # We look for function definitions not inside class indentation
            lines = source_code.split('\n')
            top_level_funcs = []
            in_class = False
            class_indent = 0
            
            for line in lines:
                if re.match(r'^\s*class\s+', line):
                    in_class = True
                    class_indent = len(line) - len(line.lstrip())
                    continue
                    
                # Check if we've left the class definition
                if in_class and line.strip() and not line.startswith(' ' * (class_indent + 4)):
                    in_class = False
                    
                # If not in a class and found a function definition
                if not in_class:
                    func_match = re.match(r'^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', line)
                    if func_match:
                        top_level_funcs.append(func_match.group(1))
            
            # Combine all names that need to be imported
            names_to_import = ", ".join(top_level_funcs + classes)
            
            # Build import statements
            required_imports = [
                "import pytest",
                f"from {dir_name}.{module_name} import {names_to_import}"
            ]
        except Exception as e:
            print(f"Error analyzing source file: {e}")
            # Fallback to basic import
            required_imports = [
                "import pytest",
                f"from {dir_name}.{module_name} import *"
            ]
        
        # Check if pytest is already imported
        has_pytest = bool(re.search(r'import\s+pytest', tests))
        
        # Check if correct module import already exists
        correct_import_pattern = f"from\\s+{dir_name}\\.{module_name}\\s+import"
        has_correct_module_import = bool(re.search(correct_import_pattern, tests))
        
        # Remove any incorrect imports
        if not has_correct_module_import:
            # Replace incorrect import patterns
            tests = re.sub(r'(import\s+{0}|from\s+{0}\s+import)'.format(module_name), 
                        f"from {dir_name}.{module_name} import", tests)
            
            # If no import statement exists, add the correct one
            if not re.search(correct_import_pattern, tests):
                tests = f"{required_imports[1]}\n{tests}"
        
        # Add pytest import if missing
        if not has_pytest:
            tests = f"{required_imports[0]}\n{tests}"
        
        return tests
        
    def _report_coverage(self, coverage_data):
        """Report coverage and test results"""
        coverage_pct = coverage_data.get('coverage_pct', 0)
        print(f"Current coverage: {coverage_pct}% (Target: {self.target_coverage}%)")
        
        if coverage_data.get('target_reached', False):
            print(f"🎉 Target coverage of {self.target_coverage}% reached!")
        else:
            print(f"⚠️ Target coverage of {self.target_coverage}% not reached.")
            
        # Print failed tests
        failed_tests = coverage_data.get('failed_tests', [])
        if failed_tests:
            print(f"\n❌ Failed tests ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"  - {test}")

    def generate_tests(self):
        """
        Generate tests only if test file doesn't exist
        """
        # Read source code
        source_code = self.read_source_code()
        
        # Check if test file exists
        existing_tests = self.read_existing_tests()
        if existing_tests:
            print(f"Found existing test file: {self.test_file}")
            # Run tests and analyze coverage
            coverage_data = self.test_runner.analyze_coverage(self.target_coverage)
            self._report_coverage(coverage_data)
            return True
        
        # If test file doesn't exist, create it
        print(f"Creating new test file: {self.test_file}")
        
        # Build prompt with source code
        prompt = build_prompt(
            source_code=source_code,
            existing_tests=None,
            coverage_report=None,
        )
        
        # Call AI model to generate new tests
        generated_tests = self.ai_caller.call_model(prompt)
        
        # Clean up generated test code
        cleaned_tests = self._clean_up_tests(generated_tests)
        
        # Ensure tests have correct imports
        cleaned_tests = self._ensure_required_imports(cleaned_tests)
        
        # Add new tests to test file
        self.save_tests(cleaned_tests)
        
        # Run tests and analyze coverage
        coverage_data = self.test_runner.analyze_coverage(self.target_coverage)
        print(f"Coverage after test generation: {coverage_data.get('coverage_pct', 0)}% (Target: {self.target_coverage}%)")
        self._report_coverage(coverage_data)
        
    
    def _clean_up_tests(self, tests):
        """Clean up the generated tests."""
        # Remove markdown code blocks if present
        if tests.startswith("```python"):
            tests = tests.replace("```python", "", 1)
            
        if tests.endswith("```"):
            tests = tests.replace("```", "", 1)
            
        return tests.strip()
