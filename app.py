import os
import json
from flask import Flask, render_template, abort
from jinja2 import TemplateNotFound

app = Flask(__name__)

def load_mock_data():
    """
    Scans the mock_data directory and loads all JSON files 
    into a dictionary keyed by filename.
    """
    data = {}
    mock_dir = os.path.join(app.root_path, 'mock_data')
    
    if os.path.exists(mock_dir):
        for filename in os.listdir(mock_dir):
            if filename.endswith('.json'):
                key = filename.replace('.json', '')
                filepath = os.path.join(mock_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        data[key] = json.load(f)
                except json.JSONDecodeError:
                    print(f"Error decoding {filename}")
                    data[key] = {}
    return data

@app.context_processor
def inject_global_data():
    """
    Injects the mock data into every template automatically.
    Usage in Jinja: {{ mock.filename.key }}
    """
    return dict(mock=load_mock_data())

@app.route('/')
def index():
    """Listing of all available widget tests."""
    return render_template('workbench/index.html')

@app.route('/<widget_name>')
def test_widget(widget_name):
    """
    Dynamic route to load test templates.
    Accessing /panel tries to load templates/workbench/test_panel.html
    """
    try:
        return render_template(f'workbench/test_{widget_name}.html')
    except TemplateNotFound:
        abort(404)

@app.route('/nav_panel')
@app.route('/nav_panel/<slug>')
def test_nav_panel(slug=None):
    """
    Specific route for the Navigation Panel widget to handle state.
    """
    data = load_mock_data()
    nav_items = data.get('family', {}).get('navigation', [])
    
    # Default to the first item if no slug provided
    if not slug and nav_items:
        slug = nav_items[0]['slug']
        
    return render_template('workbench/test_nav_panel.html', active_slug=slug)

if __name__ == '__main__':
    # Docker handles the port mapping, so we listen on 5000 internally
    app.run(host='0.0.0.0', port=5000, debug=True)