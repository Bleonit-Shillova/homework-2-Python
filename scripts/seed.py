"""
Seed script to populate sample data.
Run with: python scripts/seed.py
"""

import os
import sys

# Make sure we can import gradebook when running from project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gradebook import service  # noqa: E402
from gradebook import storage  # noqa: E402


def main():
    # reset data to empty first
    data = {"students": [], "courses": [], "enrollments": []}
    storage.save_data(data)

    # create students
    bleonit_id = service.add_student("Bleonit Shillova")
    diar_id = service.add_student("Diar Sadiku")
    alba_id = service.add_student("Alba Krasniqi")

    # create courses
    service.add_course("CS101", "Intro to CS")
    service.add_course("MATH201", "Discrete Math")

    # enrollments
    service.enroll(bleonit_id, "CS101")
    service.enroll(bleonit_id, "MATH201")
    service.enroll(alba_id, "CS101")

    # grades
    service.add_grade(bleonit_id, "CS101", 95)
    service.add_grade(bleonit_id, "CS101", 88)
    service.add_grade(bleonit_id, "MATH201", 92)

    service.add_grade(alba_id, "CS101", 75)
    service.add_grade(alba_id, "CS101", 82)

    print(" Seed data created in data/gradebook.json")


if __name__ == "__main__":
    main()