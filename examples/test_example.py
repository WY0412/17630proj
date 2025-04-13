import pytest
from examples.example import add, subtract, multiply, divide, factorial, is_prime, fibonacci, count_words, find_max, process_data, Person
def test_add_positive_numbers():
    assert add(3, 5) == 8

def test_add_negative_numbers():
    assert add(-3, -5) == -8

def test_subtract_positive_numbers():
    assert subtract(10, 5) == 1

def test_subtract_negative_numbers():
    assert subtract(-10, -5) == -5

def test_multiply_positive_numbers():
    assert multiply(4, 5) == 20

def test_multiply_negative_numbers():
    assert multiply(-4, 5) == -20

def test_divide_positive_numbers():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_factorial_positive_integer():
    assert factorial(5) == 120

def test_factorial_zero():
    assert factorial(0) == 1

def test_factorial_negative_integer():
    with pytest.raises(ValueError):
        factorial(-5)

def test_factorial_non_integer():
    with pytest.raises(TypeError):
        factorial(5.5)

def test_is_prime_prime_number():
    assert is_prime(7) is True

def test_is_prime_non_prime_number():
    assert is_prime(4) is False

def test_is_prime_edge_case():
    assert is_prime(1) is False

def test_fibonacci_positive_integer():
    assert fibonacci(5) == 5

def test_fibonacci_zero():
    assert fibonacci(0) == 0

def test_fibonacci_negative_integer():
    with pytest.raises(ValueError):
        fibonacci(-1)

def test_count_words_empty_string():
    assert count_words("") == 0

def test_count_words_multiple_words():
    assert count_words("Hello world") == 2

def test_person_initialization():
    person = Person("Alice", 30)
    assert person.name == "Alice"
    assert person.age == 30

def test_person_age_setter():
    person = Person("Bob", 25)
    person.age = 26
    assert person.age == 26

def test_person_age_setter_negative():
    person = Person("Charlie", 40)
    with pytest.raises(ValueError):
        person.age = -1

def test_person_greet_with_name():
    person = Person("David", 22)
    assert person.greet("Eve") == "Hello Eve, my name is David!"

def test_person_greet_without_name():
    person = Person("Frank", 35)
    assert person.greet() == "Hello, my name is Frank!"

def test_person_is_adult_true():
    person = Person("George", 20)
    assert person.is_adult() is True

def test_person_is_adult_false():
    person = Person("Hannah", 17)
    assert person.is_adult() is False

def test_find_max_normal_case():
    assert find_max([1, 2, 3, 4, 5]) == 5

def test_find_max_single_element():
    assert find_max([42]) == 42

def test_find_max_empty_list():
    with pytest.raises(ValueError):
        find_max([])

def test_process_data_no_filter_no_transform():
    data = [1, 2, 3]
    assert process_data(data) == [1, 2, 3]

def test_process_data_with_filter():
    data = [1, 2, 3, 4]
    assert process_data(data, filter_func=lambda x: x > 2) == [3, 4]

def test_process_data_with_transform():
    data = [1, 2, 3]
    assert process_data(data, transform_func=lambda x: x * 2) == [2, 4, 6]

def test_process_data_with_filter_and_transform():
    data = [1, 2, 3, 4]
    assert process_data(data, filter_func=lambda x: x > 2, transform_func=lambda x: x * 2) == [6, 8]

def test_process_data_empty_list():
    assert process_data([]) == []