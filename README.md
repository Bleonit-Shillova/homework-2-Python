Homework #2: Python Gradebook CLI

Goal

A simple command-line gradebook application built in Python to practice core concepts:
variables, control flow, functions, file I/O, exceptions, and basic OOP.

⸻

Setup
1.	Clone the repository:
  git clone https://github.com/Bleonit-Shillova/homework-2-Python.git
  cd homework-2-Python

2.	Create and activate a virtual environment:
  python3 -m venv venv
  source venv/bin/activate

3.	Run seed data (optional):
     python3 scripts/seed.py

Usage

Examples:
python3 main.py add-student --name "Filan Fisteku"
python3 main.py add-course --code CS101 --title "Intro to CS"
python3 main.py enroll --student-id 1 --course CS101
python3 main.py add-grade --student-id 1 --course CS101 --grade 95
python3 main.py list students --sort name
python3 main.py avg --student-id 1 --course CS101
python3 main.py gpa --student-id 1


Tests

Run all tests:
python3 -m unittest discover tests



Project Structure
gradebook-project/
├── data/
├── gradebook/
├── logs/
├── scripts/
├── tests/
├── main.py
└── README.md


Author

Bleonit Shillova
