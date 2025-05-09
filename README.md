SmartBites
A Python-based meal-planning app backed by a SQL database.

FEATURES
- User signup/login with SQL password prompt
- Browse recipes and meal plans
- View full details by clicking on any recipe or meal-plan label
- My Items tab: add your own recipes or meal plans
- Save Items tab: save recipes or meal plans from friends or from the popular tabs
- My Grocery List: view, add, or remove ingredients; see price ranges
- My Pantry: track which ingredients you already have
- Popular Recipes & Popular Meal Plans: search and see the highest-rated items
- My Reviews: view and add reviews on any recipe or meal plan you didn’t create
- Add new ingredients or recipes via the UI (automatically saved to the database)

PREREQUISITES
- Python 3.8 or higher
- MySQL (or compatible SQL server)
- pip for installing Python packages

INSTALLATION
Clone the repo:
    git clone https://github.com/martaah7/SmartBite.git
    cd SmartBites

(Optional) Create and activate a virtual environment:
python -m venv venv
    - macOS/Linux: source venv/bin/activate
    - Windows: venv\Scripts\activate

Install dependencies:
    pip install -r requirements.txt

DATABASE SETUP
- Install MySQL if it’s not already on your machine.
- Create and populate the database using the provided SQL scripts at the top of the files in the sql directory starting with createDatabase.sql

RUNNING THE APP
- python main.py
- On first launch you’ll sign up and enter your SQL password.
- Once you've signed up, use your log in credentials, you will still be prompted for your SQL password
- Navigate via the tabs (Recipes, Meal Plans, My Items, Save Items, My Grocery List, My Pantry, Popular Recipes, Popular Meal Plans, My Reviews) and click labels to see full details.

NOTES
- No hard-coded credentials—DB passwords are entered at runtime.
- Keep the sql/ folder intact so the app can locate your schema and seed data.