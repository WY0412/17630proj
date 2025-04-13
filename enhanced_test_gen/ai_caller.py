import os
from openai import OpenAI

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
        prompt = {}
        prompt['system'] = 'You are a specialized problem decomposition agent.'
        prompt['user'] = f'''I will provide you with a code snippet. Your task is to identify and list every distinct functionality or behavior in the code that should be tested. Think step by step, but do not reveal your reasoning. Present only the final result as a list of bullet points—one bullet per functionality or behavior. Do not include any explanation or additional text.

        This is the code snippet: {code}'''
        return self.call_model(prompt)
    
    def run_agent_2(self, behavior):
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
        prompt = f"""
        You are a unit test generation agent.
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

        Now generate unit tests for the following code and description:

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
    

