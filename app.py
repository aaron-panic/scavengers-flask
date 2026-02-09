#    app.py - for mock server workbench routes
#    Copyright (C) 2026  Aaron Reichenbach
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import json
import math
from flask import Flask, render_template, abort, request, url_for
from jinja2 import TemplateNotFound

app = Flask(__name__)

def load_mock_data():
    data = {}
    mock_dir = os.path.join(app.root_path, 'mock_data')
    if os.path.exists(mock_dir):
        for filename in os.listdir(mock_dir):
            if filename.endswith('.json'):
                key = filename.replace('.json', '')
                try:
                    with open(os.path.join(mock_dir, filename), 'r') as f:
                        data[key] = json.load(f)
                except json.JSONDecodeError:
                    data[key] = {}
    return data

@app.context_processor
def inject_global_data():
    return dict(mock=load_mock_data())

@app.route('/')
def index():
    return render_template('workbench/index.html')

@app.route('/panel')
def test_panel():
    return render_template('workbench/test_panel.html')

@app.route('/form')
def test_form():
    return render_template('workbench/test_form.html')

@app.route('/modal')
def test_modal():
    return render_template('workbench/test_modal.html')

@app.route('/table')
def test_table():
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
        'prev_href': f"?page={page-1}",
        'next_href': f"?page={page+1}"
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

@app.route('/nav_panel')
def test_nav_panel():
    slug = request.args.get('slug')
    data = load_mock_data()
    nav_items = data.get('family', {}).get('navigation', [])
    
    # Default to first item if no slug provided
    if not slug and nav_items:
        slug = nav_items[0]['slug']
    
    # Construct Tabs Logic in Python
    tabs = []
    active_item = None
    for item in nav_items:
        is_active = (item['slug'] == slug)
        if is_active:
            active_item = item
        tabs.append({
            'label': item['label'],
            'href': f"?slug={item['slug']}",
            'active': is_active
        })

    # Fallback if slug is invalid
    if not active_item and nav_items:
        active_item = nav_items[0]
        
    return render_template('workbench/test_nav_panel.html', 
                           tabs=tabs, 
                           active_item=active_item)

@app.route('/admin')
def admin_panel():
    data = load_mock_data()
    active_tab = request.args.get('tab', 'users')
    
    # Define Tabs
    tabs = [
        {'label': 'Users', 'href': '?tab=users', 'active': (active_tab == 'users')},
        {'label': 'Announcements', 'href': '?tab=announcements', 'active': (active_tab == 'announcements')}
    ]
    
    rows = []
    columns = []
    actions = []
    
    if active_tab == 'users':
        rows = data.get('users', [])
        columns = [
            {'key': 'id', 'label': 'ID', 'class': 'col-narrow'},
            {'key': 'name', 'label': 'Name'},
            {'key': 'email', 'label': 'Email'},
            {'key': 'role', 'label': 'Role', 'class': 'col-narrow'}
        ]
        actions = [
            {'label': 'Approve', 'icon': '&#10003;', 'class': ''},
            {'label': 'Details', 'icon': '&#8505;', 'class': ''},
            {'label': 'Delete', 'icon': '&#10005;', 'class': 'destructive'}
        ]
        
    elif active_tab == 'announcements':
        rows = data.get('announcements', [])
        columns = [
            {'key': 'id', 'label': 'ID', 'class': 'col-narrow'},
            {'key': 'title', 'label': 'Title'},
            {'key': 'username', 'label': 'Posted By'}
        ]
        actions = [
            {'label': 'Modify', 'icon': '&#9998;', 'class': ''},
            {'label': 'Delete', 'icon': '&#10005;', 'class': 'destructive'}
        ]

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 25
    total_pages = math.ceil(len(rows) / per_page)
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
        'prev_href': f"?tab={active_tab}&page={page-1}",
        'next_href': f"?tab={active_tab}&page={page+1}"
    }

    return render_template('workbench/test_nav_tables.html',
                           tabs=tabs,
                           columns=columns,
                           rows=rows_slice,
                           actions=actions,
                           pagination=pagination)

@app.route('/events')
def test_events():
    data = load_mock_data()
    all_events = data.get('events', [])
    active_tab = request.args.get('tab', 'browse')
    active_tag = request.args.get('tag')
    
    # Construct Tabs Logic in Python
    tabs = [
        {'label': 'Browse Events', 'href': '?tab=browse', 'active': (active_tab == 'browse')},
        {'label': 'Add Event', 'href': '?tab=new', 'active': (active_tab == 'new')}
    ]

    grid_items = []
    pagination = None
    all_tags = sorted(list(set(tag for event in all_events for tag in event['tags'])))
    
    if active_tab == 'browse':
        filtered = [e for e in all_events if active_tag in e['tags']] if active_tag else all_events
        
        page = request.args.get('page', 1, type=int)
        per_page = 4
        total_pages = math.ceil(len(filtered) / per_page)
        start = (page - 1) * per_page
        grid_items = filtered[start:start+per_page]
        
        pagination = {
            'page': page,
            'pages': total_pages,
            'has_prev': page > 1,
            'has_next': page < total_pages,
            'prev_href': f"?tab=browse&page={page-1}&tag={active_tag or ''}",
            'next_href': f"?tab=browse&page={page+1}&tag={active_tag or ''}"
        }

    form_data = data.get('forms', {}).get('request_form', {})
    
    return render_template('workbench/test_events.html',
                           active_tab=active_tab,
                           tabs=tabs,
                           active_tag=active_tag,
                           all_tags=all_tags,
                           grid_items=grid_items,
                           pagination=pagination,
                           form_data=form_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)