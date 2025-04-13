import os
import subprocess
import tempfile
from pathlib import Path
import json
import re

class TestRunner:
    def __init__(self, test_file):
        """
        Initialize the test runner.
        
        Args:
            source_file: Path to the source file
            test_file: Path to the test file
        """
        self.test_file = test_file
        
    def run_tests(self):
        """
        Run tests and return success status.
        
        Returns:
            bool: Whether tests passed
        """
        cmd = ["python", "-m", "pytest", self.test_file, "-v"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    
    def analyze_coverage(self, target_coverage=80):
        print("Analyzing coverage...")
        print(self.test_file)
        """Run tests with coverage analysis and return report from 'coverage report -m'"""
        try:
            # Run the coverage command
            run_cmd = ["coverage", "run", "-m", "pytest", self.test_file]
            result = subprocess.run(run_cmd, capture_output=True, text=True)
            success = result.returncode == 0
            
            # Parse failed tests
            failed_tests = []
            if not success:
                # Use regex to parse failed tests from pytest output
                for line in result.stdout.split('\n'):
                    # Find lines with FAILED format
                    failed_match = re.search(r'(FAILED|ERROR)\s+(.*?::.*?)(\s|$)', line)
                    if failed_match:
                        failed_tests.append(failed_match.group(2))
            
            # Generate and capture the coverage report output directly
            report_cmd = ["coverage", "report", "-m"]
            report_result = subprocess.run(report_cmd, capture_output=True, text=True)
            report_output = report_result.stdout
            
            # Print the coverage report for user visibility
            print("\nCoverage Report:")
            print(report_output)
            
            # Extract coverage percentage using regex
            coverage_pct = 0
            line_coverage_match = re.search(r'Line Coverage:\s+(\d+\.\d+)%', report_output)
            if line_coverage_match:
                coverage_pct = float(line_coverage_match.group(1))
            else:
                # Alternative pattern for different report formats
                total_match = re.search(r'TOTAL\s+\d+\s+\d+\s+(\d+)%', report_output)
                if total_match:
                    coverage_pct = float(total_match.group(1))
            
            # Extract covered/total lines
            covered_lines_match = re.search(r'Lines Covered:\s+(\d+)/(\d+)', report_output)
            if covered_lines_match:
                covered_count = int(covered_lines_match.group(1))
                total_count = int(covered_lines_match.group(2))
            else:
                covered_count = 0
                total_count = 0
            
            # Check if target coverage is reached
            target_reached = coverage_pct >= target_coverage
            
            # Return simplified coverage information
            return {
                'success': success,
                'coverage_pct': coverage_pct,
                'covered_lines': [],  
                'total_lines': total_count,
                'target_reached': target_reached,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'report': report_output,  # Include the full report for use in prompts
                'failed_tests': failed_tests  # Include failed tests in return data
            }
        
        except Exception as e:
            print(f"Error running coverage: {e}")
            return {
                'success': False,
                'coverage_pct': 0,
                'covered_lines': [], 
                'total_lines': 0,
                'target_reached': False,
                'stdout': "",
                'stderr': str(e),
                'report': "",
                'failed_tests': []
            }