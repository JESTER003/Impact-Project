# DevTools 

Welcome to the DevTools Suite, a collection of web tools designed to enhance productivity and streamline workflows. This project includes a URL Shortener, a To-Do App, and a Realtime Chat-App, all built using Flask and styled with Tailwind CSS.

## Features

- **URL Shortener**: Convert long URLs into short, manageable links using hashing techniques.
- **To-Do App**: Manage your tasks efficiently with a stack-based approach, allowing you to add, edit, and complete tasks.
- **Realtime Chat-App**: Engage in real-time communication using graph-based concepts (feature placeholder).

## Tech Stack

- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Backend**: Python, Flask
- **Templating**: Jinja2
- **Validation**: Validators library for URL validation
- **Hashing**: hashlib for generating unique short URLs

## Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/devtools-suite.git
   cd devtools-suite
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Flask server**:
   ```bash
   python run.py
   ```

2. **Open your browser and visit**:
   ```
   http://127.0.0.1:5000/
   ```

## Project Structure

- `app/templates/`: Contains HTML templates for the web pages.
- `app/static/css/`: Contains custom CSS styles.
- `run.py`: The entry point for running the Flask application.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please contact [Jester003](https://www.github.com/jester003).
