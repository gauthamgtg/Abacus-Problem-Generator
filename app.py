import streamlit as st
import random

# Function to generate random numbers based on given min and max lengths
def generate_number(min_len, max_len):
    min_value = 10**(min_len - 1)
    max_value = 10**max_len - 1
    return random.randint(min_value, max_value)

# Function to generate a problem with either single or mixed operators
def generate_problem(num_lines, min_len, max_len, operations, mixed):
    numbers = [generate_number(min_len, max_len) for _ in range(num_lines)]
    problem_str = str(numbers[0])
    
    result = numbers[0]
    for i in range(1, num_lines):
        operation = random.choice(operations) if mixed else operations[0]
        
        if operation == "+":
            result += numbers[i]
            problem_str += f"\n+{numbers[i]}"
        elif operation == "-":
            result -= numbers[i]
            problem_str += f"\n-{numbers[i]}"
        elif operation == "*":
            result *= numbers[i]
            problem_str += f"\n*{numbers[i]}"
        elif operation == "/":
            result /= numbers[i]
            problem_str += f"\n/{numbers[i]}"
    
    return problem_str, result

# Initializing session state for problems and answers
if 'problems' not in st.session_state:
    st.session_state['problems'] = []
    st.session_state['correct_answers'] = []
    st.session_state['user_answers'] = {}

# Streamlit app interface
st.title("Abacus Problem Generator for Kids")

# Inputs
num_lines = st.number_input("Number of numbers in each problem (lines)", min_value=2, max_value=10, value=4)
min_len = st.number_input("Minimum number length", min_value=1, max_value=10, value=1)
max_len = st.number_input("Maximum number length", min_value=1, max_value=10, value=2)
operations_selected = st.multiselect("Operations to be performed", ["+", "-", "*", "/"], default=["+"])
mixed_operators = st.radio("Do you want mixed operators in a single problem?", ("Single Operator", "Mixed Operators"))
num_problems = st.number_input("Number of problems", min_value=1, max_value=100, value=5)

# Generate problems
if st.button("Generate Problems"):
    st.session_state['problems'] = []
    st.session_state['correct_answers'] = []
    
    mixed = mixed_operators == "Mixed Operators"
    
    for _ in range(num_problems):
        problem_str, correct_answer = generate_problem(num_lines, min_len, max_len, operations_selected, mixed)
        st.session_state['problems'].append(problem_str)
        st.session_state['correct_answers'].append(correct_answer)

# Displaying problems and accepting answers
if st.session_state['problems']:
    for idx, problem in enumerate(st.session_state['problems']):
        cols = st.columns(2)
        
        with cols[0]:
            st.text(f"Problem {idx+1}:")
            st.text(problem)  # Display the problem vertically
        
        with cols[1]:
            # Retrieve previous answer or set to empty
            if f"user_answer_{idx}" not in st.session_state:
                st.session_state[f"user_answer_{idx}"] = 0
            
            user_answer = st.number_input(f"Your answer for problem {idx+1}", value=st.session_state[f"user_answer_{idx}"], key=f"answer_{idx}")
            
            # Store user answer in session state
            st.session_state[f"user_answer_{idx}"] = user_answer
            
            # Check answer
            if st.button(f"Check answer for problem {idx+1}", key=f"check_{idx}"):
                if user_answer == st.session_state['correct_answers'][idx]:
                    st.write("Correct!")
                else:
                    st.write(f"Incorrect! The correct answer is {st.session_state['correct_answers'][idx]}")
