# Component Implementation Guide

This document details how to implement the Scavengers UI components using Jinja2 macros.

## 1. The Master Panel (`panel.html`)

The Panel is the fundamental container for all content. It supports four archetypes defined by the `type` parameter.

### Import
```jinja
{% import "components/panel.html" as Panel %}
```

### Usage

**Type: `empty`**
*A basic container with no decorations.*
```jinja
{% call Panel.render(type='empty') %}
    <p>Your content here.</p>
{% endcall %}
```

**Type: `article`**
*Standard page content with metadata.*
```jinja
{% call Panel.render(
    type='article',
    header={
        'title': 'Page Title', 
        'subtitle': 'Optional Subtitle',
        'author': 'User Name',  # Optional
        'date': '2026-02-10'    # Optional
    }
) %}
    <p>Content...</p>
{% endcall %}
```

**Type: `tabbed`**
*Navigation tabs for switching views.*
```jinja
{% set tabs = [
    {'label': 'Overview', 'href': '?tab=overview', 'active': True},
    {'label': 'Settings', 'href': '?tab=settings', 'active': False}
] %}

{% call Panel.render(
    type='tabbed',
    header={'title': 'Settings'},
    tabs=tabs
) %}
    <p>Tab content...</p>
{% endcall %}
```

**Type: `grid`**
*A grid layout for Cards. Supports a toolbar for filters.*
```jinja
{% set filters = [{'label': 'All', 'href': '#', 'active': True}] %}

{% call Panel.render(
    type='grid',
    header={'title': 'Dashboard'},
    filters=filters
) %}
    {{ Card.render(data) }}
    {{ Card.render(data) }}
{% endcall %}
```

---

## 2. Card (`card.html`)

Used inside `grid` panels to display summary content.

### Import
```jinja
{% import "components/card.html" as Card %}
```

### Data Structure
```python
card_data = {
    'title': 'Server Maintenance',
    'description': 'Routine patching of linux kernels.',
    'meta': '2026-02-10',       # Optional: Date or secondary info
    'tags': ['ops', 'urgent']   # Optional: List of strings
}
```

### Usage
```jinja
{{ Card.render(card_data) }}
```

---

## 3. Table (`table.html`)

Displays tabular data with automated actions and pagination hooks.

### Import
```jinja
{% import "components/table.html" as Table %}
```

### Configuration
```python
columns = [
    {'key': 'id', 'label': 'ID', 'class': 'col-narrow'},
    {'key': 'name', 'label': 'Full Name'},
    {'key': 'role', 'label': 'Role'}
]

actions = [
    {'label': 'Edit', 'icon': '&#9998;', 'class': ''},
    {'label': 'Delete', 'icon': '&#10005;', 'class': 'destructive'}
]
```

### Usage
```jinja
{{ Table.render(
    columns=columns, 
    rows=rows_list, 
    actions=actions
) }}
```

---

## 4. Form (`form.html`)

Renders a standard input array.

### Import
```jinja
{% import "components/form.html" as Form %}
```

### Data Structure
```python
form_data = {
    'action': '/submit',
    'method': 'POST',
    'fields': [
        {
            'name': 'username', 
            'label': 'Username', 
            'type': 'text', 
            'width': 'half-width' # Options: full-width, half-width, one-third-width
        },
        {
            'name': 'bio', 
            'label': 'Biography', 
            'type': 'textarea', 
            'height': 'height-m'  # Options: height-s, height-m, height-l
        }
    ],
    'buttons': [
        {'label': 'Save', 'type': 'submit', 'class': 'inverted'}
    ]
}
```

### Usage
```jinja
{{ Form.render(form_data) }}
```

---

## 5. Modal (`modal.html`)

Renders a native `<dialog>` element. Can display a confirmation message OR a key-value detail grid.

### Import
```jinja
{% import "components/modal.html" as Modal %}
```

### Usage
1. **Render the modal** (hidden by default):
    ```jinja
    {{ Modal.render(id='my-modal', data=modal_data) }}
    ```
2. **Trigger it** using a button with the data attribute:
    ```html
    <button class="btn" data-modal-target="my-modal">Open Modal</button>
    ```

### Data Structure (Confirmation)
```python
{
    'title': 'Delete User?',
    'content': 'Are you sure you want to delete this?',
    'actions': [
        {'label': 'Cancel', 'role': 'cancel', 'class': ''},
        {'label': 'Confirm', 'role': 'confirm', 'class': 'destructive'}
    ]
}
```

### Data Structure (Details View)
```python
{
    'title': 'User Details',
    'details': [
        {'key': 'ID', 'value': '104'},
        {'key': 'Email', 'value': 'admin@example.com'}
    ],
    'actions': [{'label': 'Close', 'role': 'cancel'}]
}
```