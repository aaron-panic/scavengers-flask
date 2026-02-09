# Scavengers Flask Framework

**Code Name:** Scavengers
**Version:** 0.2.0 (Refactor)

## Overview

Scavengers Flask is a robust, server-driven web architecture designed to reject modern client-side bloat in favor of semantic HTML, rigorous CSS compartmentalization, and server-side rendering (SSR). 

It is built on **Flask** and **Jinja2**, employing a "Configuration over Code" philosophy where UI components are driven by data structures rather than hard-coded HTML.

## Core Philosophy

1.  **The Server is the Source of Truth:** The client is a display terminal. State, logic, and routing are handled exclusively by the server.
2.  **No-Bloat:** Zero reliance on heavy frontend frameworks (React, Vue, Bootstrap). The UI is built with native HTML5 <dialog>, CSS Grid, and semantic tags.
3.  **The CSS Trinity:** Styling is strictly separated into three layers:
    * `base.css`: Atomic tokens (variables only).
    * `layout.css`: Geometry and positioning (no aesthetics).
    * `widget.css`: Aesthetics and theming (no layout).
4.  **CSP Compliance:** The architecture is designed to be Content Security Policy (CSP) compliant, banning inline styles and scripts in production.

## Features

* **Unified Panel Architecture:** A single master component that morphs into Article, Tabbed, Grid, or Empty states based on configuration.
* **Data-Driven Forms:** Render complex input arrays from JSON schemas with standardized validation styling.
* **Native Modals:** Accessible, script-light modal dialogs using the HTML5 <dialog> element.
* **Component Workbench:** A built-in isolated development environment (`/workbench`) for testing widgets without database dependencies.
* **Themeable:** Complete visual overhaul possible by modifying only `base.css` and `widget.css`.

## Installation & Setup

### Docker (Recommended)
```bash
docker-compose up --build
```

### Manual Setup
1.  Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the application:
    ```bash
    python app.py
    ```

## Development

The project includes a **Workbench** route at `/`. This serves as a living style guide and test harness for all components.

* **Workbench:** `http://localhost:5000/`
* **Admin Test:** `http://localhost:5000/admin`
* **Events Dashboard:** `http://localhost:5000/events`

## License: GNU AGPL-3.0

**scavengers-flask:** Flask/Jinja2 based component library.
Copyright (C) 2026 Aaron Reichenbach

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Also add information on how to contact you by electronic and paper mail.