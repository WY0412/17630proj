# Code under test:
def square_nums(nums):
 square_nums = list(map(lambda x: x ** 2, nums))
 return square_nums

import os
import sys
import math
def test_case():
    # Create file to store test results
    output_dir = os.path.dirname(__file__)
    test_results_file = os.path.join(output_dir, "test_start_results.txt")
    
    failed_tests = []
    total_tests = 0
    
    def run_assert(assertion_func, description=None):
        nonlocal total_tests
        total_tests += 1
        try:
            # Execute the assertion function instead of directly calculating the assertion expression
            assertion_result = assertion_func()
            assert assertion_result
        except AssertionError:
            failed_message = f"Assertion failed: {description}" if description else f"Assertion failed: {assertion_func}"
            failed_tests.append(failed_message)
            # Write failure information to file in real-time
            with open(test_results_file, "a") as f:
                f.write(f"{failed_message}\n")
        except NameError as e:
            # Handle undefined variable errors
            failed_message = f"Variable error in: {description} - {str(e)}"
            failed_tests.append(failed_message)
            with open(test_results_file, "a") as f:
                f.write(f"{failed_message}\n")
        except ImportError as e:
            # Handle missing module errors
            failed_message = f"Import error in: {description} - {str(e)}"
            failed_tests.append(failed_message)
            with open(test_results_file, "a") as f:
                f.write(f"{failed_message}\n")
        except AttributeError as e:
            # Handle undefined attribute/method errors
            failed_message = f"Attribute error in: {description} - {str(e)}"
            failed_tests.append(failed_message)
            with open(test_results_file, "a") as f:
                f.write(f"{failed_message}\n")
        except Exception as e:
            # Catch all other exceptions
            failed_message = f"Error in: {description} - {str(e)}"
            failed_tests.append(failed_message)
            with open(test_results_file, "a") as f:
                f.write(f"{failed_message}\n")
    
    # Clear or create results file
    with open(test_results_file, "w") as f:
        f.write("Test Results Log\n")
        f.write("=" * 50 + "\n\n")
    
    # Test with a list of positive integers: Provide a list such as `[1, 2, 3, 4, 5]` to verify that the function performs as expected with standard positive integer inputs, ensuring basic computations and logic paths are executed correctly.
    run_assert(lambda: square_nums([1, 2, 3, 4, 5]) == [1, 4, 9, 16, 25], "assert square_nums([1, 2, 3, 4, 5]) == [1, 4, 9, 16, 25]")
    run_assert(lambda: square_nums([0, 1, 2, 3]) == [0, 1, 4, 9], "assert square_nums([0, 1, 2, 3]) == [0, 1, 4, 9]")
    run_assert(lambda: square_nums([10, 20, 30]) == [100, 400, 900], "assert square_nums([10, 20, 30]) == [100, 400, 900]")
    run_assert(lambda: square_nums([6, 7, 8]) == [36, 49, 64], "assert square_nums([6, 7, 8]) == [36, 49, 64]")
    run_assert(lambda: square_nums([9]) == [81], "assert square_nums([9]) == [81]")

    # Test with a list of negative integers: Use a list like `[-1, -2, -3, -4, -5]` to ensure the function accurately processes negative values, correctly handling operations that depend on the sign of the numbers.
    run_assert(lambda: square_nums([-1, -2, -3, -4, -5]) == [1, 4, 9, 16, 25], "assert square_nums([-1, -2, -3, -4, -5]) == [1, 4, 9, 16, 25]")
    run_assert(lambda: square_nums([-10, -20, -30]) == [100, 400, 900], "assert square_nums([-10, -20, -30]) == [100, 400, 900]")
    run_assert(lambda: square_nums([-7, -8, -9]) == [49, 64, 81], "assert square_nums([-7, -8, -9]) == [49, 64, 81]")
    run_assert(lambda: square_nums([-100, -200]) == [10000, 40000], "assert square_nums([-100, -200]) == [10000, 40000]")
    run_assert(lambda: square_nums([-0]) == [0], "assert square_nums([-0]) == [0]")

    # Test with a list of zero: Submit a list `[0, 0, 0]` to confirm that zeros are handled as neutral elements in arithmetic operations where applicable, ensuring they neither disrupt nor alter calculations improperly.
    run_assert(lambda: square_nums([0, 0, 0]) == [0, 0, 0], "assert square_nums([0, 0, 0]) == [0, 0, 0]")

    # Test with an empty list: Pass an empty list `[]` to confirm the function gracefully handles the absence of input without causing errors, and returns an appropriate result reflecting no data processed.
    run_assert(lambda: square_nums([]) == [], "assert square_nums([]) == []")

    # Test with a list of mixed positive and negative integers: Provide a list such as `[10, -10, 20, -20, 0]` to ensure that the function deals with both positive and negative numbers together, maintaining the correct logic for operations that factor in number signs.
    run_assert(lambda: square_nums([10, -10, 20, -20, 0]) == [100, 100, 400, 400, 0], "assert square_nums([10, -10, 20, -20, 0]) == [100, 100, 400, 400, 0]")
    run_assert(lambda: square_nums([-1, -2, -3, -4, -5]) == [1, 4, 9, 16, 25], "assert square_nums([-1, -2, -3, -4, -5]) == [1, 4, 9, 16, 25]")
    run_assert(lambda: square_nums([1, 2, 3, 4, 5]) == [1, 4, 9, 16, 25], "assert square_nums([1, 2, 3, 4, 5]) == [1, 4, 9, 16, 25]")
    run_assert(lambda: square_nums([0]) == [0], "assert square_nums([0]) == [0]")
    run_assert(lambda: square_nums([]) == [], "assert square_nums([]) == []")

    # Test with a list containing non-integer numbers (floats): Use a list like `[1.5, -2.5, 3.0, 0.0]` to verify that floats are processed correctly or appropriately flagged if not supported, ensuring that decimal values do not cause disruption in integer-centric logic.
    run_assert(lambda: square_nums([1.5, -2.5, 3.0, 0.0]) == [2.25, 6.25, 9.0, 0.0], "assert square_nums([1.5, -2.5, 3.0, 0.0]) == [2.25, 6.25, 9.0, 0.0]")
    run_assert(lambda: square_nums([-1.5, 2.5, -3.0, 0.0]) == [2.25, 6.25, 9.0, 0.0], "assert square_nums([-1.5, 2.5, -3.0, 0.0]) == [2.25, 6.25, 9.0, 0.0]")
    run_assert(lambda: square_nums([0.5, 1.5, 2.5]) == [0.25, 2.25, 6.25], "assert square_nums([0.5, 1.5, 2.5]) == [0.25, 2.25, 6.25]")
    run_assert(lambda: square_nums([0.0]) == [0.0], "assert square_nums([0.0]) == [0.0]")
    run_assert(lambda: square_nums([]) == [], "assert square_nums([]) == []")

    # Test with a list containing non-numeric types: Submit a list such as `[5, 'a', None, '123']` to check the function's robustness in handling unexpected data types, triggering type checks, or handling exceptions for unsupported data effectively.
    run_assert(lambda: square_nums([]) == [], "assert square_nums([]) == []")
    run_assert(lambda: square_nums([1, 2, 3]) == [1, 4, 9], "assert square_nums([1, 2, 3]) == [1, 4, 9]")
    run_assert(lambda: square_nums([0, -1, 2.5]) == [0, 1, 6.25], "assert square_nums([0, -1, 2.5]) == [0, 1, 6.25]")

    # Test with large numbers for performance: Provide a list with very large integers to evaluate how the function handles computational stress and the potential for overflow, verifying that logical operations complete efficiently without performance degradation.
    run_assert(lambda: square_nums([10**6, 10**7, 10**8]) == [10**12, 10**14, 10**16], "assert square_nums([10**6, 10**7, 10**8]) == [10**12, 10**14, 10**16]")
    run_assert(lambda: square_nums([10**9, 10**10, 10**11]) == [10**18, 10**20, 10**22], "assert square_nums([10**9, 10**10, 10**11]) == [10**18, 10**20, 10**22]")
    run_assert(lambda: square_nums([10**12, 10**13, 10**14]) == [10**24, 10**26, 10**28], "assert square_nums([10**12, 10**13, 10**14]) == [10**24, 10**26, 10**28]")
    run_assert(lambda: square_nums([10**15, 10**16, 10**17]) == [10**30, 10**32, 10**34], "assert square_nums([10**15, 10**16, 10**17]) == [10**30, 10**32, 10**34]")
    run_assert(lambda: square_nums([10**18, 10**19, 10**20]) == [10**36, 10**38, 10**40], "assert square_nums([10**18, 10**19, 10**20]) == [10**36, 10**38, 10**40]")

    # Edge case with single-element list: Use a list `[42]` to explore behavior with the minimal non-empty list, checking if the function correctly processes list-based logic with only one element to operate on.
    run_assert(lambda: square_nums([42]) == [1764], "assert square_nums([42]) == [1764]")
    run_assert(lambda: square_nums([0]) == [0], "assert square_nums([0]) == [0]")
    run_assert(lambda: square_nums([-42]) == [1764], "assert square_nums([-42]) == [1764]")

    # Edge case with very large positive integers: Test with values reaching system limits (e.g., `[2**31 - 1]`) to ensure that the function correctly handles such large values without encountering overflow issues in computation or logic errors due to size constraints.
    run_assert(lambda: square_nums([2**31 - 1]) == [(2**31 - 1) ** 2], "assert square_nums([2**31 - 1]) == [(2**31 - 1) ** 2]")
    run_assert(lambda: square_nums([0]) == [0], "assert square_nums([0]) == [0]")
    run_assert(lambda: square_nums([1, 2, 3, 4, 5]) == [1, 4, 9, 16, 25], "assert square_nums([1, 2, 3, 4, 5]) == [1, 4, 9, 16, 25]")
    run_assert(lambda: square_nums([-1, -2, -3, -4, -5]) == [1, 4, 9, 16, 25], "assert square_nums([-1, -2, -3, -4, -5]) == [1, 4, 9, 16, 25]")

    # Edge case with single zero-value: Provide a list `[0]` to verify that single zero-value scenarios are handled sensibly, maintaining any invariants related to zero being a neutral element in operations.
    run_assert(lambda: square_nums([0]) == [0], "assert square_nums([0]) == [0]")

    # Edge case with a list of zeros: Use `[0, 0, 0]` to confirm that the function's logic processes multiple zeroes without introducing unintended arithmetic or logical errors.
    run_assert(lambda: square_nums([0, 0, 0]) == [0, 0, 0], "assert square_nums([0, 0, 0]) == [0, 0, 0]")
    run_assert(lambda: square_nums([0]) == [0], "assert square_nums([0]) == [0]")
    run_assert(lambda: square_nums([0, 1, 2]) == [0, 1, 4], "assert square_nums([0, 1, 2]) == [0, 1, 4]")
    run_assert(lambda: square_nums([0, -1, -2]) == [0, 1, 4], "assert square_nums([0, -1, -2]) == [0, 1, 4]")
    run_assert(lambda: square_nums([]) == [], "assert square_nums([]) == []")

    # Edge case with balanced mix: Pass a list like `[-1, 1, -2, 2, 0]` ensuring operations calculate accurately across transitions in sign, effectively balancing positive and negative contributions as per intended arithmetic logic.
    run_assert(lambda: square_nums([-1, 1, -2, 2, 0]) == [1, 1, 4, 4, 0], "assert square_nums([-1, 1, -2, 2, 0]) == [1, 1, 4, 4, 0]")
    run_assert(lambda: square_nums([0]) == [0], "assert square_nums([0]) == [0]")
    run_assert(lambda: square_nums([-3, 3]) == [9, 9], "assert square_nums([-3, 3]) == [9, 9]")
    run_assert(lambda: square_nums([2, -2, 2, -2]) == [4, 4, 4, 4], "assert square_nums([2, -2, 2, -2]) == [4, 4, 4, 4]")
    run_assert(lambda: square_nums([-1, 0, 1]) == [1, 0, 1], "assert square_nums([-1, 0, 1]) == [1, 0, 1]")

    # Edge case with float and integers: Use `[1, -1.5, 0.5, 2]` to confirm mixed-type handling, ensuring each element is processed according to its type, particularly checking for potential miscalculations due to floating-point arithmetic decisions.
    run_assert(lambda: square_nums([1, -1.5, 0.5, 2]) == [1, 2.25, 0.25, 4], "assert square_nums([1, -1.5, 0.5, 2]) == [1, 2.25, 0.25, 4]")
    run_assert(lambda: square_nums([0, 0.0, -0.0]) == [0, 0.0, 0.0], "assert square_nums([0, 0.0, -0.0]) == [0, 0.0, 0.0]")
    run_assert(lambda: square_nums([-2, -3.5, 4.5]) == [4, 12.25, 20.25], "assert square_nums([-2, -3.5, 4.5]) == [4, 12.25, 20.25]")
    run_assert(lambda: square_nums([1.1, 2.2, 3.3]) == [1.21, 4.84, 10.89], "assert square_nums([1.1, 2.2, 3.3]) == [1.21, 4.84, 10.89]")
    run_assert(lambda: square_nums([]) == [], "assert square_nums([]) == []")

    # Edge case with NaN: Include lists containing `float('nan')`, such as `[1, float('nan'), 2]`, to test its impact on computations, verifying if NaN values propagate, causing skips or undesired output.
    run_assert(lambda: square_nums([1, float('nan'), 2]) == [1, float('nan'), 4], "assert square_nums([1, float('nan'), 2]) == [1, float('nan'), 4]")
    run_assert(lambda: square_nums([float('nan')]) == [float('nan')], "assert square_nums([float('nan')]) == [float('nan')]")
    run_assert(lambda: square_nums([0, float('nan'), -1]) == [0, float('nan'), 1], "assert square_nums([0, float('nan'), -1]) == [0, float('nan'), 1]")
    run_assert(lambda: square_nums([float('nan'), float('nan')]) == [float('nan'), float('nan')], "assert square_nums([float('nan'), float('nan')]) == [float('nan'), float('nan')]")
    run_assert(lambda: square_nums([3, 4, float('nan')]) == [9, 16, float('nan')], "assert square_nums([3, 4, float('nan')]) == [9, 16, float('nan')]")

    # Edge case with string-convertible numbers: Input a list like `['5', '10', 'twenty']` to see if the function converts string numbers unintentionally, maintaining clarity between numeric and non-numeric entries.
    run_assert(lambda: square_nums([5, 10, 20]) == [25, 100, 400], "assert square_nums([5, 10, 20]) == [25, 100, 400]")
    run_assert(lambda: square_nums([]) == [], "assert square_nums([]) == []")
    run_assert(lambda: square_nums([0, -1, -2]) == [0, 1, 4], "assert square_nums([0, -1, -2]) == [0, 1, 4]")

    # Edge case with concurrent access: Simulate multiple threads accessing a list like `[1, 2, 3, 4]` concurrently to test that shared data access points do not cause race conditions, particularly in environments requiring thread safety.
    run_assert(lambda: result == expected_output, "assert result == expected_output")

    # Edge case with duplicated maximum values: Provide lists `[maxsize, maxsize, maxsize]` to evaluate how the function handles repeated extreme values, verifying computation limits and behavioral consistency in repetitive contexts.
    run_assert(lambda: square_nums([]) == [], "assert square_nums([]) == []")
    run_assert(lambda: square_nums([5]) == [25], "assert square_nums([5]) == [25]")
    run_assert(lambda: square_nums([-1, -2, -3]) == [1, 4, 9], "assert square_nums([-1, -2, -3]) == [1, 4, 9]")
    run_assert(lambda: square_nums([1, -1, 0, 2, -2]) == [1, 1, 0, 4, 4], "assert square_nums([1, -1, 0, 2, -2]) == [1, 1, 0, 4, 4]")

    # Output test result statistics to file
    with open(test_results_file, "a") as f:
        f.write("\n" + "=" * 50 + "\n")
        f.write(f"Test Result Summary:\n")
        f.write(f"Total tests: {total_tests}\n")
        f.write(f"Failed tests: {len(failed_tests)}\n")
        f.write(f"Success rate: {(total_tests - len(failed_tests)) / total_tests * 100:.2f}%\n")
        
        if failed_tests:
            f.write("\nList of Failed Tests:\n")
            for i, test in enumerate(failed_tests, 1):
                f.write(f"{i}. {test}\n")
    
    print(f"Test results saved to {test_results_file}")
    # Return failed tests list for further processing
    return failed_tests
