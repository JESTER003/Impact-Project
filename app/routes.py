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
    result = None
    
    if request.method == 'POST':
        expression = request.form.get('expression', '').strip()
        conversion_type = request.form.get('conversion_type')
        
        try:
            if conversion_type == 'infix_to_postfix':
                converted = infix_to_postfix(expression)
            else:  # postfix_to_infix
                converted = postfix_to_infix(expression)
                
            result = {
                'input': expression,
                'output': converted
            }
        except Exception as e:
            result = {
                'input': expression,
                'output': f"Error: {str(e)}"
            }
    
    return render_template('expression_converter.html', result=result)

def infix_to_postfix(expression):
    """Convert infix expression to postfix."""
    # Define operator precedence
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    
    # Initialize empty lists for output and operator stack
    output = []
    operators = []
    
    # Split the expression into tokens
    tokens = expression.replace(' ', '')
    
    # Process each character in the expression
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        # If token is a number, add it to output
        if token.isdigit():
            num = ''
            while i < len(tokens) and (tokens[i].isdigit() or tokens[i] == '.'):
                num += tokens[i]
                i += 1
            output.append(num)
            i -= 1
            
        # If token is an opening parenthesis, push to operators
        elif token == '(':
            operators.append(token)
            
        # If token is a closing parenthesis, process until matching opening parenthesis
        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            if operators:
                operators.pop()  # Remove '('
                
        # If token is an operator
        elif token in precedence:
            while (operators and operators[-1] != '(' and 
                   precedence.get(operators[-1], 0) >= precedence[token]):
                output.append(operators.pop())
            operators.append(token)
            
        i += 1
    
    # Pop remaining operators to output
    while operators:
        if operators[-1] == '(':
            raise ValueError("Mismatched parentheses")
        output.append(operators.pop())
    
    return ' '.join(output)

def postfix_to_infix(expression):
    """Convert postfix expression to infix."""
    stack = []
    tokens = expression.split()
    
    for token in tokens:
        if token.replace('.', '').isdigit():  # If token is a number
            stack.append(token)
        elif token in {'+', '-', '*', '/', '^'}:  # If token is an operator
            if len(stack) < 2:
                raise ValueError("Invalid postfix expression")
            b = stack.pop()
            a = stack.pop()
            stack.append(f"({a} {token} {b})")
    
    if len(stack) != 1:
        raise ValueError("Invalid postfix expression")
    
    return stack[0]

