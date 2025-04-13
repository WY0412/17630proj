"""
A sample module with various Python features for testing test generation.
This module includes functions, classes, and different code paths to exercise test generation.
"""

def add(a, b):
    """Add two numbers and return the result."""
    return a + b

def subtract(a, b):
    """Subtract b from a and return the result."""
    return a - b

def multiply(a, b):
    """Multiply two numbers and return the result."""
    return a * b

def divide(a, b):
    """
    Divide a by b and return the result.
    
    Args:
        a: Numerator
        b: Denominator
    
    Returns:
        The result of a/b
        
    Raises:
        ZeroDivisionError: If b is zero
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def factorial(n):
    """
    Calculate the factorial of n.
    
    Args:
        n: A non-negative integer
        
    Returns:
        The factorial of n
        
    Raises:
        ValueError: If n is negative
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    if n < 0:
        raise ValueError("Input must be non-negative")
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

def is_prime(n):
    """
    Check if a number is prime.
    
    Args:
        n: A positive integer
        
    Returns:
        True if n is prime, False otherwise
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def fibonacci(n):
    """
    Generate the nth Fibonacci number.
    
    Args:
        n: A non-negative integer
        
    Returns:
        The nth Fibonacci number
    """
    if n < 0:
        raise ValueError("Input must be non-negative")
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def count_words(text):
    """
    Count the number of words in a text.
    
    Args:
        text: A string
        
    Returns:
        The number of words in the text
    """
    if not text:
        return 0
    
    words = text.split()
    return len(words)

class Person:
    """A simple class representing a person."""
    
    def __init__(self, name, age):
        """
        Initialize a Person object.
        
        Args:
            name: The person's name
            age: The person's age
        """
        self.name = name
        self._age = age
        
    @property
    def age(self):
        """Get the person's age."""
        return self._age
    
    @age.setter
    def age(self, value):
        """
        Set the person's age.
        
        Args:
            value: The new age
            
        Raises:
            ValueError: If age is negative
        """
        if value < 0:
            raise ValueError("Age cannot be negative")
        self._age = value
        
    def greet(self, other_name=None):
        """
        Generate a greeting.
        
        Args:
            other_name: The name of the person to greet
            
        Returns:
            A greeting string
        """
        if other_name:
            return f"Hello {other_name}, my name is {self.name}!"
        return f"Hello, my name is {self.name}!"
    
    def is_adult(self):
        """
        Check if the person is an adult.
        
        Returns:
            True if the person is 18 or older, False otherwise
        """
        return self._age >= 18

def find_max(numbers):
    """
    Find the maximum value in a list of numbers.
    
    Args:
        numbers: A list of numbers
        
    Returns:
        The maximum value
        
    Raises:
        ValueError: If the list is empty
    """
    if not numbers:
        raise ValueError("Cannot find max of empty list")
    
    max_value = numbers[0]
    for num in numbers:
        if num > max_value:
            max_value = num
    
    return max_value

def process_data(data, filter_func=None, transform_func=None):
    """
    Process data with optional filtering and transformation.
    
    Args:
        data: A list of items to process
        filter_func: Optional function to filter items
        transform_func: Optional function to transform items
        
    Returns:
        A list of processed items
    """
    if not data:
        return []
    
    result = data
    
    # Apply filter if provided
    if filter_func:
        result = [item for item in result if filter_func(item)]
    
    # Apply transformation if provided
    if transform_func:
        result = [transform_func(item) for item in result]
    
    return result