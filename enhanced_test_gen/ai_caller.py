import os
from openai import OpenAI
import json
from collections import defaultdict
from tqdm import tqdm

class AICaller:
    def __init__(self, model="gpt-4o"):
        self.model = model
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
    def call_model(self, prompt):
        """Call the OpenAI API with the given prompt."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]}
                ],
                temperature=0.2,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling AI model: {e}")
            raise
    
    def agent1_decompose(self, code):
        print("Decomposing code...")
        prompt = {}
        prompt['system'] = 'You are a specialized problem decomposition agent.'
        prompt['user'] = f'''I will provide you with a code snippet. Your task is to identify and list every distinct functionality or behavior in the code that should be tested. Think step by step, but do not reveal your reasoning. Present only the final result as a list of bullet points—one bullet per functionality or behavior. Do not include any explanation or additional text.

        This is the code snippet: {code}'''
        return self.call_model(prompt)
    
    def run_agent_2(self, behavior):
        print("Running agent 2...")
        prompts = [
            # "For each functionality identified, describe the typical/expected use-cases along with the primary inputs, outputs, and any assumptions the code makes.",
            "For each functionality identified, describe the typical/expected use-cases along with any assumptions the code makes.",
            "For each functionality, think of possible edge cases or boundary conditions (extreme values, invalid data types, missing data, concurrency/timeout issues, or anything that might cause unusual behavior).",
            # "For each normal scenario and edge-case scenario, propose at least one set of input parameters that would effectively test it.",
            "Considering the previous scenarios, are there any overlaps or missed scenarios?",
            # "What invalid inputs or erroneous situations could occur that the code should handle gracefully? Suggest parameter values for each negative test and explain how they might trigger exceptions or error states.",
            # "Review and consolidate your lists of parameters. Are there any overlaps or missed scenarios? Refine the overall test parameter set to cover all essential paths without unnecessary duplication.",
            "Put all normal scenarios, edge cases, and negative tests in a bulleted list with a detailed description for each test in paragraph format. Do not include any introductory text, headings, comments, or additional explanations outside of these list items. Provide no additional formatting beyond the list. Do not provide unnecessary explanations, comments, or input parameters.",

        ]
        lines = behavior.strip().split('\n')
        code_chunk = "\n".join([line for line in lines if not line.startswith("-")])
        behaviors = [line[2:] for line in lines if line.startswith("-")]

        messages = [
            {
                "role": "system",
                "content": "You are a test case reasoning assistant helping to plan unit tests for software functionality."
            },
            {
                "role": "user",
                "content": (
                "Here is the code chunk:\n"
                f"{code_chunk}\n\n"
                "These are the functionalities to test:\n" +
                "\n".join(f"- {b}" for b in behaviors)
                )
            }
        ]

        for prompt in prompts:
            messages.append({"role": "user", "content": prompt})
            response = self.client.chat.completions.create(
                model="gpt-4o",
                store=True,
                messages=messages
            )
            reply = response.choices[0].message.content
            messages.append({"role": "assistant", "content": reply})

        return messages[-1]["content"]
    
    def parse_bullet_points(self, text: str):   
        print("Parsing bullet points...")
        """
        Splits a text containing bullet points (each starting with '- ')
        into a list of bullet contents.

        :param text: The full text with bullet points.
        :return: A list of strings, each corresponding to one bullet point.
        """
        lines = text.strip().split('\n')
        bullets = []
        current_bullet = []

        for line in lines:
            # Trim whitespace
            line = line.strip()

            # If this line starts a new bullet:
            if line.startswith('- '):
                # If there's a current bullet being built, append it before starting a new one
                if current_bullet:
                    bullets.append(' '.join(current_bullet))
                    current_bullet = []
                # Add the line content (minus the '- ') as the first piece of this bullet
                current_bullet.append(line[2:].strip())
            else:
                # Otherwise, continue adding to the current bullet
                current_bullet.append(line)

        # After the loop, append the last bullet if it exists
        if current_bullet:
            bullets.append(' '.join(current_bullet))

        return bullets
    
    def generate_test_case(self, description, code_chunk):
        print("Generating test case...")
        prompt = {}
        prompt['system'] = 'You are a unit test generation agent.'
        prompt['user'] = f"""
        You will be given a description of a functionality (behavior) in the code and a code chunk.
        You must generate Python unit tests that test this functionality thoroughly, including all edge cases and lines of code.
        Output ONLY the test in valid Python.
        Do NOT provide unnecessary explanations, comments, or code.

        Here is an example of a description and code chunk, along with the expected output format for unit tests:

        The code is:
        def similar_elements(test_tup1, test_tup2):\n  res = tuple(set(test_tup1) & set(test_tup2))\n  return (res)

        The description of the functionality is:
        Finds common elements between two tuples.

        Unit tests:
        - assert set(similar_elements((3, 4, 5, 6),(5, 7, 4, 10))) == set((4, 5))
        - assert set(similar_elements((1, 2, 3, 4),(5, 4, 3, 7))) == set((3, 4))
        - assert set(similar_elements((11, 12, 14, 13),(17, 15, 14, 13))) == set((13, 14))

        Now generate unit tests for the following code and description.
        YOU NEED TO FOLLOW THE REQUIREMENTS BELOW:
        - DO NOT USE ANY OTHER FUNCTIONS OR LIBRARIES UNLESS THEY ARE DEFINED IN THE CODE CHUNK
        - DO NOT USE ANY VARIABLES THAT ARE NOT DEFINED IN THE CODE CHUNK
        
        Here are 2 examples you should not follow:
        assert result == expected_output
        assert first_output == second_output == third_output 
        This is wrong because result, expected_output, first_output, second_output and third_output are not defined in the code chunk.
        

        The code is:
        {code_chunk}

        The description of the functionality is:
        {description}

        Unit tests:
        -
        """
        response = self.call_model(prompt)
        predicted_label = response.strip()
        return predicted_label
    
    def clean_testcase_output(self, agent3_output, code_chunk, gpt_model='gpt-4o'): 
        print("Cleaning test case output...")
        prompt = {}
        prompt['system'] = 'You are a test case validation and sanitization assistant.'
        prompt['user'] = f"""
        Your task:
        - Extract all assert statement code lines.
        - Remove any duplicate assert statements.
        - Remove any irrelevant text, spaces, or characters that are not part of the executable assert statements.
        - Remove any asserts with variables or functions that are not defined by the given code chunk.
        - Ensure the formatting of each assert statement is executable in Python.
        - Output only a list of assert statements (one per line), with no additional text, headings, or explanations.

        For example, if the input contains the following assert statements:
            - assert heap_queue_largest([1.5e+308, 1.4e+308, float('-inf'), float('inf')], 1) == [float('inf')]Unit tests:
        - assert heap_queue_largest([(1, 2), (3, 4), (5, 6)], 2) == [(5, 6), (3, 4)]
        - assert heap_queue_largest([(9, 2), (7, 8), (5, 6), (3, 4)], 3) == [(9, 2), (7, 8), (5, 6)]

        Your output should be:
            assert heap_queue_largest([1.5e+308, 1.4e+308, float('-inf'), float('inf')], 1) == [float('inf')]
            assert heap_queue_largest([(1, 2), (3, 4), (5, 6)], 2) == [(5, 6), (3, 4)]
            assert heap_queue_largest([(9, 2), (7, 8), (5, 6), (3, 4)], 3) == [(9, 2), (7, 8), (5, 6)]

        Do not include any extra content beyond the list of assert statement code lines.

        Code chunk:
        {code_chunk}

        Below is the output from Agent 3:
        {agent3_output}
        """

        response = self.call_model(prompt)
        predicted_label = response.strip()
        return predicted_label
    
    def generate_py(self, dataset, output_dir, filename):
        print("Generating py...")
        code_to_tests = {}
        code = dataset[0]['code']
        try:
            agent1_output = self.agent1_decompose(code)
            agent2_output = self.run_agent_2(agent1_output)
            agent2_bullets = self.parse_bullet_points(agent2_output)

            bullet_map = {}
            for bullet in agent2_bullets:
                try:
                    agent3_output = self.generate_test_case(bullet, code)
                    cleaned = self.clean_testcase_output(agent3_output, code)
                    cleaned_lines = [line.strip() for line in cleaned.strip().split('\n') if line.strip().startswith("assert")]
                    if cleaned_lines:
                        bullet_map[bullet] = cleaned_lines

                except Exception as e:
                    print(f" Test generation failed on sample for bullet:\n{bullet}\n {e}")
                    continue

            if bullet_map:
                code_to_tests[code] = bullet_map

        except Exception as e:
            print(f" Agent pipeline failed on dataset: {e}")
        

        os.makedirs(output_dir, exist_ok=True)
        
        if not code_to_tests:
            print("Error: No tests were generated.")
            return
            
        code_snippet, tests = list(code_to_tests.items())[0]

        file_path = os.path.join(output_dir, filename)
        
        # Extract base filename without extension for results file
        test_base_name = os.path.splitext(filename)[0]
        results_filename = f"{test_base_name}_results.txt"

        with open(file_path, "w") as f:
            # Write the code under test
            f.write("# Code under test:\n")
            f.write(code_snippet.strip() + "\n\n")
            
            # Import required modules
            f.write("import os\n")
            f.write("import sys\n")
            f.write("import math\n")
            
            # Write the enhanced test function
            f.write("def test_case():\n")
            f.write("    # Create file to store test results\n")
            f.write("    output_dir = os.path.dirname(__file__)\n")
            f.write(f"    test_results_file = os.path.join(output_dir, \"{results_filename}\")\n")
            f.write("    \n")
            f.write("    failed_tests = []\n")
            f.write("    total_tests = 0\n")
            f.write("    \n")
            
            # Add custom assert handling function with enhanced error handling
            f.write("    def run_assert(assertion_func, description=None):\n")
            f.write("        nonlocal total_tests\n")
            f.write("        total_tests += 1\n")
            f.write("        try:\n")
            f.write("            # Execute the assertion function instead of directly calculating the assertion expression\n")
            f.write("            assertion_result = assertion_func()\n")
            f.write("            assert assertion_result\n")
            f.write("        except AssertionError:\n")
            f.write("            failed_message = f\"Assertion failed: {description}\" if description else f\"Assertion failed: {assertion_func}\"\n")
            f.write("            failed_tests.append(failed_message)\n")
            f.write("            # Write failure information to file in real-time\n")
            f.write("            with open(test_results_file, \"a\") as f:\n")
            f.write("                f.write(f\"{failed_message}\\n\")\n")
            f.write("        except NameError as e:\n")
            f.write("            # Handle undefined variable errors\n")
            f.write("            failed_message = f\"Variable error in: {description} - {str(e)}\"\n")
            f.write("            failed_tests.append(failed_message)\n")
            f.write("            with open(test_results_file, \"a\") as f:\n")
            f.write("                f.write(f\"{failed_message}\\n\")\n")
            f.write("        except ImportError as e:\n")
            f.write("            # Handle missing module errors\n")
            f.write("            failed_message = f\"Import error in: {description} - {str(e)}\"\n")
            f.write("            failed_tests.append(failed_message)\n")
            f.write("            with open(test_results_file, \"a\") as f:\n")
            f.write("                f.write(f\"{failed_message}\\n\")\n")
            f.write("        except AttributeError as e:\n")
            f.write("            # Handle undefined attribute/method errors\n")
            f.write("            failed_message = f\"Attribute error in: {description} - {str(e)}\"\n")
            f.write("            failed_tests.append(failed_message)\n")
            f.write("            with open(test_results_file, \"a\") as f:\n")
            f.write("                f.write(f\"{failed_message}\\n\")\n")
            f.write("        except Exception as e:\n")
            f.write("            # Catch all other exceptions\n")
            f.write("            failed_message = f\"Error in: {description} - {str(e)}\"\n")
            f.write("            failed_tests.append(failed_message)\n")
            f.write("            with open(test_results_file, \"a\") as f:\n")
            f.write("                f.write(f\"{failed_message}\\n\")\n")
            f.write("    \n")
            
            # Initialize results file
            f.write("    # Clear or create results file\n")
            f.write("    with open(test_results_file, \"w\") as f:\n")
            f.write("        f.write(\"Test Results Log\\n\")\n")
            f.write("        f.write(\"=\" * 50 + \"\\n\\n\")\n")
            f.write("    \n")
            
            # Write the test assertions
            for description, assert_lines in tests.items():
                f.write(f"    # {description.strip()}\n")
                for line in assert_lines:
                    # Convert regular assert to run_assert with description
                    assert_statement = line.strip()
                    if assert_statement.startswith("assert "):
                        condition = assert_statement[7:]  # Remove "assert " prefix
                        f.write(f"    run_assert(lambda: {condition}, \"{assert_statement}\")\n")
                    else:
                        f.write(f"    {assert_statement}\n")
                f.write("\n")
            
            # Add summary output
            f.write("    # Output test result statistics to file\n")
            f.write("    with open(test_results_file, \"a\") as f:\n")
            f.write("        f.write(\"\\n\" + \"=\" * 50 + \"\\n\")\n")
            f.write("        f.write(f\"Test Result Summary:\\n\")\n")
            f.write("        f.write(f\"Total tests: {total_tests}\\n\")\n")
            f.write("        f.write(f\"Failed tests: {len(failed_tests)}\\n\")\n")
            f.write("        f.write(f\"Success rate: {(total_tests - len(failed_tests)) / total_tests * 100:.2f}%\\n\")\n")
            f.write("        \n")
            f.write("        if failed_tests:\n")
            f.write("            f.write(\"\\nList of Failed Tests:\\n\")\n")
            f.write("            for i, test in enumerate(failed_tests, 1):\n")
            f.write("                f.write(f\"{i}. {test}\\n\")\n")
            f.write("    \n")
            f.write("    print(f\"Test results saved to {test_results_file}\")\n")
            f.write("    # Return failed tests list for further processing\n")
            f.write("    return failed_tests\n")

        print(f"Wrote enhanced test file: {filename}")
            
        
    

