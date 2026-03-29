# IT Inventory Manager

Offline IT inventory management software built as a portfolio project for small teams that need asset tracking, assignment history, account control, and reporting without relying on a separate database server.

## Why This Project

This project was designed to show a practical IT-focused workflow rather than a generic CRUD demo. It focuses on the kinds of tasks an IT specialist or support administrator actually handles:

- tracking devices and asset tags
- assigning equipment to people
- managing account roles and password updates
- keeping assignment history
- exporting operational records for reporting
- running fully offline in a portable local setup

## Highlights

- Fully offline inventory system
- Python backend with local SQLite storage
- Desktop mode with `pywebview`
- Browser mode with a built-in local web server
- Asset, team member, assignment, and account management
- Search, filtering, and sorting across major sections
- CSV import/export and styled PDF export
- Reusable saved suggestions with in-place CRUD for repeated fields
- Local, portable data file for easy transfer between machines

## Tech Stack

- Python
- SQLite
- HTML
- CSS
- Vanilla JavaScript
- `pywebview`
- `reportlab`

## Main Features

- Dashboard
  View high-level asset counts, recent assignment history, and recent asset activity.
- Asset Management
  Create, edit, assign, return, and remove inventory records.
- Team Member Profiles
  Track the people who receive and use devices.
- Accounts and Roles
  Manage login accounts with `Super Admin`, `Admin`, and `User` roles.
- Search and Filters
  Quickly narrow down data in the major tables.
- Saved Suggestions
  Reuse values such as device name, category, role, status, condition, location, and department.
- Import and Export
  Import CSV data and export clean CSV or PDF reports.
- Password Controls
  Allow admins to reset account passwords and let each user change their own password.

## Run Options

### Option 1: Browser Mode

1. Install Python 3.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
python app.py
```

4. Open [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Option 2: Desktop Mode

1. Install Python 3.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the desktop app:

```bash
python desktop.py
```

### Windows Launchers

- `run.bat`: browser mode
- `run_desktop.bat`: desktop mode
- `app.pyw`: browser mode without a visible terminal window
- `desktop.pyw`: desktop mode without a visible terminal window

## Default Login

- Username: `admin`
- Password: `admin`

## First-Time Walkthrough

This is a simple way for a new user to explore the app:

1. Sign in with the default admin account.
2. Open the Dashboard to review totals and recent activity.
3. Go to `Team Members` and create or edit employee/device-holder profiles.
4. Open `Assets` and add inventory items such as laptops, monitors, phones, or printers.
5. Use the `Assignments` screen to check out a device to a team member and later check it back in.
6. Open `Accounts` to manage login access, roles, and password resets.
7. Use the search bar, filters, and sorting controls on each main data screen.
8. Click the small pencil icons beside lookup-backed fields to manage saved suggestion values.
9. Use import/export controls to move data in or generate CSV and PDF reports.

## How Key Actions Work

### Adding an Asset

- Go to `Assets`
- Click `New Asset`
- Fill in asset details such as asset tag, category, device name, brand, model, serial number, status, and location
- Save the record

### Assigning a Device

- Go to `Assignments`
- Click `Assign Asset`
- Pick an asset and a team member
- Add optional checkout notes
- Save the assignment

### Returning a Device

- Go to `Assignments`
- Find the active assignment
- Use the return/check-in action
- Add optional return notes

### Managing Roles and Saved Suggestions

- Click the small pencil icon beside supported fields
- Use the popup to add, edit, delete, or select saved values
- This works for repeated values such as category, device name, department, role, status, condition, and location

### Importing and Exporting

- CSV import is available on the main record sections
- CSV export creates spreadsheet-friendly records
- PDF export generates a styled table report for presentation or printing

## Project Structure

- `app.py`: backend server, API routes, SQLite integration
- `desktop.py`: desktop launcher with `pywebview`
- `static/index.html`: base UI layout
- `static/styles.css`: UI styling and responsive layout
- `static/app.js`: frontend behavior and view rendering
- `data/`: local runtime database files
- `seed_dummy_data.py`: helper for generating test/demo records
- `recover_admin.py`: helper to restore admin access if needed

## Portability

The working app stores data locally in `data/inventory.db`, so it can be moved by copying the whole project folder.

For my own local use, I also maintain a separate portable runtime version that bundles Python directly inside the project folder. That larger runtime is intentionally not included in the GitHub portfolio copy.
