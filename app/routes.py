from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
import hashlib
import validators
import re

# Define a blueprint
main = Blueprint("main", __name__)

# Dictionary to store the mapping between long URLs and short URLs
url_mapping = {}

# Stack to manage tasks
task_stack = []
task_editable = []


@main.route("/")
def main_page():
    return render_template("index.html")


@main.route("/url-shortener", methods=["GET", "POST"])
def url_shortener():
    short_url = None
    error_message = None
    if request.method == "POST":
        long_url = request.form["long_url"]
        if validators.url(long_url):
            short_url = shorten_url(long_url)
        else:
            error_message = "Invalid URL. Please enter a valid URL."
    return render_template(
        "url_shortener.html", short_url=short_url, error_message=error_message
    )


def shorten_url(long_url):
    """Generate a short URL by hashing the long URL."""
    short_url_hash = hashlib.sha256(long_url.encode()).hexdigest()[:6]
    short_url = f"/s/{short_url_hash}"
    url_mapping[short_url_hash] = long_url
    return request.host_url.strip("/") + short_url


@main.route("/s/<short_url_hash>")
def redirect_to_long_url(short_url_hash):
    long_url = url_mapping.get(short_url_hash)
    if long_url:
        return redirect(long_url)
    else:
        return abort(404, description="Short URL not found")


@main.route("/todo", methods=["GET", "POST"])
def todo():
    if request.method == "POST":
        task = request.form["task"]
        task_stack.append(task)  # Push task onto the stack
        task_editable.append(False)  # Initially, tasks are not editable
    return render_template("todo.html", tasks=task_stack, task_editable=task_editable)


@main.route("/todo/complete", methods=["POST"])
def complete_task():
    task_index = int(request.form["task_index"])
    if 0 <= task_index < len(task_stack):
        task_stack.pop(task_index)  # Remove the task at the given index
        task_editable.pop(task_index)
    return redirect(url_for("main.todo"))


@main.route("/todo/edit", methods=["POST"])
def edit_task():
    task_index = int(request.form["task_index"])
    if 0 <= task_index < len(task_stack):
        task_editable[task_index] = True  # Make the task editable
    return redirect(url_for("main.todo"))


@main.route("/todo/update", methods=["POST"])
def update_task():
    task_index = int(request.form["task_index"])
    updated_task = request.form["updated_task"]
    if 0 <= task_index < len(task_stack):
        task_stack[task_index] = updated_task  # Update the task
        task_editable[task_index] = False  # Make the task non-editable again
    return redirect(url_for("main.todo"))


@main.route('/expression-converter', methods=['GET', 'POST'])
def expression_converter():
    """Handles input from the form and evaluates the expression."""
    result = None
    if request.method == 'POST':
        expression = request.form['expression']
        print(f"Received expression: {expression}")  # Debugging line
        try:
            postfix_expr = infix_to_postfix(expression)
            print(f"Postfix expression: {postfix_expr}")  # Debugging line
            
            # Check if the expression contains variables (A-Z or a-z)
            if re.search(r'[a-zA-Z]', expression):
                result = f"Postfix: {postfix_expr} | Evaluated Result: Cannot evaluate expression with variables."
            else:
                evaluated_result = evaluate_postfix(postfix_expr)
                print(f"Evaluated result: {evaluated_result}")  # Debugging line
                result = f"Postfix: {postfix_expr} | Evaluated Result: {evaluated_result}"
        except Exception as e:
            result = f"Error: {str(e)}"
            print(f"Error: {str(e)}")  # Debugging line
    
    return render_template('expression_converter.html', result=result)

def infix_to_postfix(expression):
    """Convert infix expression to postfix using the Shunting Yard Algorithm."""
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}  # Operator precedence
    associativity = {'+': 'L', '-': 'L', '*': 'L', '/': 'L', '^': 'R'}  # Left/Right associative
    output = []  # Stores final postfix expression
    stack = []  # Operator stack

    # Tokenizing the input expression (Supports numbers and variables A-Z)
    tokens = re.findall(r'\d+(\.\d+)?|[a-zA-Z]+|[+\-*/^()]', expression.replace(" ", ""))

    for token in tokens:
        if re.match(r'\d+(\.\d+)?', token) or re.match(r'[a-zA-Z]+', token):  # If it's a number or variable
            output.append(token)
        elif token in precedence:  # If it's an operator
            while (stack and stack[-1] != '(' and
                   (precedence.get(stack[-1], 0) > precedence[token] or
                    (precedence.get(stack[-1], 0) == precedence[token] and associativity[token] == 'L'))):
                output.append(stack.pop())
            stack.append(token)
        elif token == '(':  # Left parenthesis
            stack.append(token)
        elif token == ')':  # Right parenthesis
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack:
                raise ValueError("Mismatched parentheses")
            stack.pop()  # Remove '('

    while stack:  # Pop remaining operators
        if stack[-1] in '()':
            raise ValueError("Mismatched parentheses")
        output.append(stack.pop())

    return " ".join(output)

def evaluate_postfix(expression):
    """Evaluate a postfix expression using a stack."""
    stack = []
    tokens = expression.split()

    for token in tokens:
        if re.match(r'\d+(\.\d+)?', token):  # If it's a number
            stack.append(float(token))
        else:  # It's an operator
            if len(stack) < 2:
                raise ValueError("Invalid Expression")
            b, a = stack.pop(), stack.pop()  # Pop two operands
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                if b == 0:
                    raise ValueError("Division by zero")
                stack.append(a / b)
            elif token == '^':
                stack.append(a ** b)
    
    if len(stack) != 1:
        raise ValueError("Invalid Expression")
    
    return stack.pop()

