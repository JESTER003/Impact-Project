from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
import hashlib
import validators

# Define a blueprint
main = Blueprint('main', __name__)

# Dictionary to store the mapping between long URLs and short URLs
url_mapping = {}

# Stack to manage tasks
task_stack = []
task_editable = []

@main.route('/')
def main_page():
    return render_template('index.html')

@main.route('/url-shortener', methods=['GET', 'POST'])
def url_shortener():
    short_url = None
    error_message = None
    if request.method == 'POST':
        long_url = request.form['long_url']
        if validators.url(long_url):
            short_url = shorten_url(long_url)
        else:
            error_message = "Invalid URL. Please enter a valid URL."
    return render_template('url_shortener.html', short_url=short_url, error_message=error_message)

def shorten_url(long_url):
    """Generate a short URL by hashing the long URL."""
    short_url_hash = hashlib.sha256(long_url.encode()).hexdigest()[:6]
    short_url = f"/s/{short_url_hash}"
    url_mapping[short_url_hash] = long_url
    return request.host_url.strip('/') + short_url

@main.route('/s/<short_url_hash>')
def redirect_to_long_url(short_url_hash):
    long_url = url_mapping.get(short_url_hash)
    if long_url:
        return redirect(long_url)
    else:
        return abort(404, description="Short URL not found")

@main.route('/todo', methods=['GET', 'POST'])
def todo():
    if request.method == 'POST':
        task = request.form['task']
        task_stack.append(task)  # Push task onto the stack
        task_editable.append(False)  # Initially, tasks are not editable
    return render_template('todo.html', tasks=task_stack, task_editable=task_editable)

@main.route('/todo/complete', methods=['POST'])
def complete_task():
    task_index = int(request.form['task_index'])
    if 0 <= task_index < len(task_stack):
        task_stack.pop(task_index)  # Remove the task at the given index
        task_editable.pop(task_index)
    return redirect(url_for('main.todo'))

@main.route('/todo/edit', methods=['POST'])
def edit_task():
    task_index = int(request.form['task_index'])
    if 0 <= task_index < len(task_stack):
        task_editable[task_index] = True  # Make the task editable
    return redirect(url_for('main.todo'))

@main.route('/todo/update', methods=['POST'])
def update_task():
    task_index = int(request.form['task_index'])
    updated_task = request.form['updated_task']
    if 0 <= task_index < len(task_stack):
        task_stack[task_index] = updated_task  # Update the task
        task_editable[task_index] = False  # Make the task non-editable again
    return redirect(url_for('main.todo'))

@main.route('/chat')
def chat():
    return render_template('chat.html')