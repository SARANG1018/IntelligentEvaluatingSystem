# IntelligentEvaluatingSystem
The Intelligent Evaluating System is a web-based application designed to assess students' abilities in mathematics, particularly in the field of mensuration. It presents students with multiple-choice questions and evaluates their problem-solving skills. Once a student successfully completes a level, they will no longer be presented with that particular level.

# Features
Multiple-choice questions on mensuration
Dynamic problem generation
Intelligent evaluation of students' problem-solving abilities
Level-based progression system
Django backend
HTML, CSS, and JavaScript frontend

# Installation
Clone the repository: 
```
git clone https://github.com/SARANG1018/IntelligentEvaluatingSystem.git
```
Navigate to the project directory: 
```
cd intelligent-evaluating-system
```
Create and activate a virtual environment (optional, but recommended):
Create: 
```
python3 -m venv env
```

Activate:
Windows:
```
env\Scripts\activate
```

Unix/macOS: 
```
source env/bin/activate
```
Install the dependencies: 
```
pip install -r requirements.txt
```
Run database migrations:
```
python manage.py migrate
```

Start the development server: 
```
python manage.py runserver
```

# Usage
Access the application by opening a web browser and visiting http://localhost:8000.
Create an account or log in if you already have one.
Start solving multiple-choice questions on mensuration.
Each level will present you with a new set of questions.
Your problem-solving abilities will be evaluated and your progress will be tracked.
Once you successfully complete a level, you will no longer encounter those questions.

# Acknowledgments
Django - The web framework used
Bootstrap - Frontend framework
Font Awesome - Icons
