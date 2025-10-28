"""
Data models for the gradebook.
"""

from typing import List


class Student:
    """
    Represents a single student.
    """

    def __init__(self, student_id: int, name: str):
        if not isinstance(student_id, int):
            raise ValueError("student_id must be an int")
        if not name or not isinstance(name, str):
            raise ValueError("name must be a non-empty string")

        self.id = student_id
        self.name = name

    def __str__(self) -> str:
        return f"Student(id={self.id}, name='{self.name}')"


class Course:
    """
    Represents a course offering.
    """

    def __init__(self, code: str, title: str):
        if not code or not isinstance(code, str):
            raise ValueError("code must be a non-empty string")
        if not title or not isinstance(title, str):
            raise ValueError("title must be a non-empty string")

        self.code = code
        self.title = title

    def __str__(self) -> str:
        return f"Course(code='{self.code}', title='{self.title}')"


class Enrollment:
    """
    Connects a student to a course and tracks their grades.
    """

    def __init__(self, student_id: int, course_code: str, grades: List[float] | None = None):
        if not isinstance(student_id, int):
            raise ValueError("student_id must be an int")
        if not course_code or not isinstance(course_code, str):
            raise ValueError("course_code must be a non-empty string")

        # Validate grades list
        if grades is None:
            grades = []
        for g in grades:
            if not (0 <= g <= 100):
                raise ValueError("grades must be between 0 and 100")

        self.student_id = student_id
        self.course_code = course_code
        self.grades = grades

    def __str__(self) -> str:
        return (
            f"Enrollment(student_id={self.student_id}, "
            f"course_code='{self.course_code}', grades={self.grades})"
        )