import os
import json
import math
from flask import Flask, render_template, abort, request
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
    """
    try:
        return render_template(f'workbench/test_{widget_name}.html')
    except TemplateNotFound:
        abort(404)

@app.route('/table')
def test_table():
    """
    Route to test the Table widget with pagination logic.
    """
    data = load_mock_data()
    all_users = data.get('users', [])
    
    page = request.args.get('page', 1, type=int)
    per_page = 25
    total_items = len(all_users)
    total_pages = math.ceil(total_items / per_page)
    
    if page < 1: page = 1
    if page > total_pages and total_pages > 0: page = total_pages
    
    start = (page - 1) * per_page
    end = start + per_page
    users_slice = all_users[start:end]
    
    pagination = {
        'page': page,
        'pages': total_pages,
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev_num': page - 1,
        'next_num': page + 1
    }
    
    columns = [
        {'key': 'id', 'label': 'ID', 'class': 'col-narrow'},
        {'key': 'name', 'label': 'Name'},
        {'key': 'email', 'label': 'Email'},
        {'key': 'role', 'label': 'Role', 'class': 'col-narrow'},
        {'key': 'status', 'label': 'Status', 'class': 'col-narrow'}
    ]

    return render_template('workbench/test_table.html', 
                           rows=users_slice, 
                           columns=columns, 
                           pagination=pagination)

@app.route('/admin')
def admin_panel():
    """
    Combines NavPanel and Table widgets.
    """
    data = load_mock_data()
    
    requested_tab = request.args.get('tab', 'users')
    
    nav_structure = [
        {'slug': 'users', 'label': 'Users', 'title': 'User Administration'},
        {'slug': 'announcements', 'label': 'Announcements', 'title': 'System Announcements'}
    ]
    
    # VALIDATION FIX: Ensure requested tab exists, otherwise default to 'users'
    valid_slugs = [item['slug'] for item in nav_structure]
    active_tab = requested_tab if requested_tab in valid_slugs else 'users'
    
    rows = []
    columns = []
    actions = []
    
    if active_tab == 'users':
        rows = data.get('users', [])
        columns = [
            {'key': 'id', 'label': 'ID', 'class': 'col-narrow'},
            {'key': 'name', 'label': 'Name'},
            {'key': 'email', 'label': 'Email'},
            {'key': 'role', 'label': 'Role', 'class': 'col-narrow'},
            {'key': 'status', 'label': 'Status', 'class': 'col-narrow'}
        ]
        actions = [
            {'label': 'Approve', 'icon': '&#10003;', 'class': ''},
            {'label': 'Details', 'icon': '&#8505;', 'class': ''},
            {'label': 'Delete', 'icon': '&#10005;', 'class': 'destructive'}
        ]
        
    elif active_tab == 'announcements':
        raw_rows = data.get('announcements', [])
        rows = []
        for r in raw_rows:
            item = r.copy()
            if len(item['title']) > 25:
                item['title'] = item['title'][:25] + '...'
            rows.append(item)
            
        columns = [
            {'key': 'id', 'label': 'ID', 'class': 'col-narrow'},
            {'key': 'title', 'label': 'Title'},
            {'key': 'username', 'label': 'Posted By'},
            {'key': 'timestamp', 'label': 'Date', 'class': 'col-narrow'}
        ]
        actions = [
            {'label': 'Modify', 'icon': '&#9998;', 'class': ''},
            {'label': 'Hide', 'icon': '&#128065;', 'class': ''},
            {'label': 'Delete', 'icon': '&#10005;', 'class': 'destructive'}
        ]

    page = request.args.get('page', 1, type=int)
    per_page = 25
    total_items = len(rows)
    total_pages = math.ceil(total_items / per_page)
    
    if page < 1: page = 1
    if page > total_pages and total_pages > 0: page = total_pages
    
    start = (page - 1) * per_page
    end = start + per_page
    rows_slice = rows[start:end]
    
    pagination = {
        'page': page,
        'pages': total_pages,
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev_num': page - 1,
        'next_num': page + 1
    }

    return render_template('workbench/test_nav_tables.html',
                           nav_data=nav_structure,
                           active_tab=active_tab,
                           columns=columns,
                           rows=rows_slice,
                           actions=actions,
                           pagination=pagination)

@app.route('/nav_panel')
@app.route('/nav_panel/<slug>')
def test_nav_panel(slug=None):
    """
    Specific route for the Navigation Panel widget to handle state.
    """
    data = load_mock_data()
    nav_items = data.get('family', {}).get('navigation', [])
    
    valid_slugs = [item['slug'] for item in nav_items]
    
    if not slug or slug not in valid_slugs:
        if nav_items:
            slug = nav_items[0]['slug']
        else:
            return "No navigation data found", 404
        
    return render_template('workbench/test_nav_panel.html', active_slug=slug)

if __name__ == '__main__':
    # Docker handles the port mapping, so we listen on 5000 internally
    app.run(host='0.0.0.0', port=5000, debug=True)