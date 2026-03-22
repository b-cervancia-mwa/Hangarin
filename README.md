# Hangarin

Hangarin is a Django task and to-do manager that lets users manage tasks, subtasks, notes, priorities, and categories from one workspace.

## Requirements

- Python 3.12
- pip

## Local Setup

```powershell
cd projectsite
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r ..\requirements.txt
py manage.py migrate
py manage.py runserver
```

Open `http://127.0.0.1:8000/login/`.

## Sample Data

The project automatically restores the default workspace demo data when the workspace is empty.

To generate additional fake data with Faker:

```powershell
cd projectsite
.\.venv\Scripts\Activate.ps1
py manage.py seed_data
```

The `seed_data` command ensures the required default priorities and categories exist before creating fake tasks, notes, and subtasks.

## Admin Features

- `TaskAdmin` displays `title`, `status`, `deadline`, `priority`, and `category`
- `TaskAdmin` filters by `status`, `priority`, and `category`
- `TaskAdmin` searches by `title` and `description`
- `SubTaskAdmin` displays `title`, `status`, and `parent_task_name`
- `SubTaskAdmin` filters by `status`
- `SubTaskAdmin` searches by `title`
- `CategoryAdmin` and `PriorityAdmin` display `name` and are searchable
- `NoteAdmin` displays `task`, `content`, and `created_at`
- `NoteAdmin` filters by `created_at`
- `NoteAdmin` searches by `content`

## PythonAnywhere Deployment

1. Clone the repository on PythonAnywhere:

```bash
cd ~
git clone https://github.com/b-cervancia-mwa/Hangarin.git
```

2. Create and activate a virtualenv:

```bash
mkvirtualenv hangarin --python=/usr/bin/python3.12
workon hangarin
```

3. Install dependencies and migrate:

```bash
cd ~/Hangarin/projectsite
pip install -r ~/Hangarin/requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

4. In the PythonAnywhere Web tab, set:

- Source code: `/home/bcervancia/Hangarin/projectsite`
- Working directory: `/home/bcervancia/Hangarin/projectsite`
- Virtualenv: `/home/bcervancia/.virtualenvs/hangarin`

5. In `/var/www/<your-domain>_wsgi.py`, make sure Django points to:

- project path: `/home/bcervancia/Hangarin/projectsite`
- settings module: `projectsite.settings`

6. Reload the web app.
