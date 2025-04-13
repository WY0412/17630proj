import argparse
import os
import sys
from colorama import Fore, Style, init

from enhanced_test_gen.test_generator import TestGenerator

# Initialize colorama
init()

def parse_args():
    parser = argparse.ArgumentParser(description="Generate and test Python code with coverage analysis")
    parser.add_argument("source_file", help="Path to the source code file")
    parser.add_argument("--test-file", help="Path to the test file (default: test_<source>.py)")
    parser.add_argument("--model", default="gpt-4o", help="AI model to use (default: gpt-4o)")
    parser.add_argument("--target-coverage", type=int, default=80, help="Target coverage percentage (default: 80)")
    
    return parser.parse_args()

def main():
    print(f"{Fore.CYAN}===== Enhanced Test Generator with Coverage Analysis ====={Style.RESET_ALL}")
    
    args = parse_args()
    
    # Check if source file exists
    if not os.path.exists(args.source_file):
        print(f"{Fore.RED}Error: Source file '{args.source_file}' not found{Style.RESET_ALL}")
        sys.exit(1)
    
    # Check if API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        print(f"{Fore.RED}Error: OPENAI_API_KEY environment variable not set{Style.RESET_ALL}")
        sys.exit(1)
    
    # Create test generator
    generator = TestGenerator(
        source_file=args.source_file,
        test_file=args.test_file,
        model=args.model,
        target_coverage=args.target_coverage
    )
    
    # Generate tests (only if test file doesn't exist)
    print(f"{Fore.YELLOW}Target coverage: {args.target_coverage}%{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Source file: {args.source_file}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Test file: {generator.test_file}{Style.RESET_ALL}")
    
    # Generate tests
    print(f"\n{Fore.GREEN}Starting test generation...{Style.RESET_ALL}")
    generator.generate_tests()
    
    # Final message
    print(f"\n{Fore.CYAN}Tests saved to: {generator.test_file}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()