# Budget Manager

A Django + Celery backend system for managing ad campaign budgets across brands. It tracks spend, enforces budget limits, and supports dayparting schedules.

---

## Features

- Track daily and monthly ad spend per brand and campaign
- Automatically pause campaigns that go over budget
- Dayparting: campaigns only run during scheduled hours
- Daily and monthly resets that reactivate eligible campaigns
- Admin panel to manage brands, campaigns, schedules, and logs

---

## Setup Instructions

### 1. Clone the Repo

`bash
git clone https://github.com/your-username/budget-manager.git
cd budget-manager

-------------------------------------------------------------
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
-------------------------------------------------------------
pip install -r requirements.txt
-------------------------------------------------------------
DB SETUP:
CREATE DATABASE budget_db;
CREATE USER budget_user WITH PASSWORD 'budget_pass';
GRANT ALL PRIVILEGES ON DATABASE budget_db TO budget_user;
-------------------------------------------------------------
python manage.py makemigrations
python manage.py migrate
-------------------------------------------------------------
python manage.py createsuperuser
-------------------------------------------------------------
python manage.py runserver
-------------------------------------------------------------
celery -A budget_manager worker --loglevel=info
-------------------------------------------------------------
celery -A budget_manager beat --loglevel=info