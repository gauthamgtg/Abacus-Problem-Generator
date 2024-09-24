import streamlit as st
import random

# Function to generate random numbers based on given min and max lengths
def generate_number(min_len, max_len):
    min_value = 10**(min_len - 1)
    max_value = 10**max_len - 1
    return random.randint(min_value, max_value)

# Function to generate a problem
def generate_problem(num_lines, min_len, max_len, operations):
    numbers = [generate_number(min_len, max_len) for _ in range(num_lines)]
    operation = random.choice(operations)
    
    if operation == "+":
        return f" + ".join(map(str, numbers)), sum(numbers)
    elif operation == "-":
        return f" - ".join(map(str, numbers)), numbers[0] - sum(numbers[1:])
    elif operation == "*":
        result = 1
        for num in numbers:
            result *= num
        return f" * ".join(map(str, numbers)), result
    elif operation == "/":
        result = numbers[0]
        for num in numbers[1:]:
            result /= num
        return f" / ".join(map(str, numbers)), result

# Streamlit app interface
st.title("Abacus Problem Generator for Kids")

# Inputs
num_lines = st.number_input("Number of numbers in each problem (lines)", min_value=2, max_value=10, value=4)
min_len = st.number_input("Minimum number length", min_value=1, max_value=10, value=1)
max_len = st.number_input("Maximum number length", min_value=1, max_value=10, value=2)
operations_selected = st.multiselect("Operations to be performed", ["+", "-", "*", "/"], default=["+"])
num_problems = st.number_input("Number of problems", min_value=1, max_value=100, value=5)

# Displaying problems and accepting answers
if st.button("Generate Problems"):
    problems = []
    correct_answers = []
    
    for _ in range(num_problems):
        problem_str, correct_answer = generate_problem(num_lines, min_len, max_len, operations_selected)
        problems.append(problem_str)
        correct_answers.append(correct_answer)
    
    # For each problem, show input for answer
    for idx, problem in enumerate(problems):
        st.write(f"Problem {idx+1}: {problem}")
        user_answer = st.number_input(f"Your answer for problem {idx+1}", key=idx)
        
        if st.button(f"Check answer for problem {idx+1}", key=f"check_{idx}"):
            if user_answer == correct_answers[idx]:
                st.write("Correct!")
            else:
                st.write(f"Incorrect! The correct answer is {correct_answers[idx]}")
