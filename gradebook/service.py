"""
Business logic for gradebook.
These functions are used by the CLI.
"""

from typing import List, Dict, Any, Optional
from . import storage  # relative import inside the package
from .models import Student, Course, Enrollment


def _get_next_student_id(data: Dict[str, Any]) -> int:
    if not data["students"]:
        return 1
    return max(s["id"] for s in data["students"]) + 1


def add_student(name: str) -> int:
    """
    Create a new student and return their new ID.
    """
    data = storage.load_data()

    new_id = _get_next_student_id(data)
    student = Student(student_id=new_id, name=name)

    data["students"].append({"id": student.id, "name": student.name})
    storage.save_data(data)

    return new_id


def add_course(code: str, title: str) -> None:
    """
    Add a new course. Course code must be unique.
    """
    data = storage.load_data()

    # check duplicate
    for c in data["courses"]:
        if c["code"] == code:
            raise ValueError(f"Course {code} already exists.")

    course = Course(code=code, title=title)
    data["courses"].append({"code": course.code, "title": course.title})

    storage.save_data(data)


def enroll(student_id: int, course_code: str) -> None:
    """
    Enroll a student in a course.
    """
    data = storage.load_data()

    # verify student exists
    if not any(s["id"] == student_id for s in data["students"]):
        raise ValueError(f"Student {student_id} not found.")

    # verify course exists
    if not any(c["code"] == course_code for c in data["courses"]):
        raise ValueError(f"Course {course_code} not found.")

    # check if already enrolled
    for e in data["enrollments"]:
        if e["student_id"] == student_id and e["course_code"] == course_code:
            return  # silently ignore, or raise? We'll just ignore.

    enrollment = Enrollment(student_id=student_id, course_code=course_code, grades=[])
    data["enrollments"].append(
        {
            "student_id": enrollment.student_id,
            "course_code": enrollment.course_code,
            "grades": enrollment.grades,
        }
    )

    storage.save_data(data)


def add_grade(student_id: int, course_code: str, grade: float) -> None:
    """
    Add a grade (0-100) for a student's enrollment.
    """
    data = storage.load_data()

    # validate grade
    if not (0 <= grade <= 100):
        raise ValueError("grade must be between 0 and 100")

    # find enrollment
    for e in data["enrollments"]:
        if e["student_id"] == student_id and e["course_code"] == course_code:
            e["grades"].append(grade)
            storage.save_data(data)
            return

    raise ValueError(
        f"Student {student_id} is not enrolled in {course_code}, cannot add grade."
    )


def list_students() -> List[Dict[str, Any]]:
    """
    Return list of students sorted by name then id.
    """
    data = storage.load_data()
    return sorted(
        data["students"],
        key=lambda s: (s["name"].lower(), s["id"])
    )


def list_courses() -> List[Dict[str, Any]]:
    """
    Return list of courses sorted by code.
    """
    data = storage.load_data()
    return sorted(
        data["courses"],
        key=lambda c: c["code"].lower()
    )


def list_enrollments() -> List[Dict[str, Any]]:
    """
    Return list of enrollments sorted by student_id then course_code.
    """
    data = storage.load_data()
    return sorted(
        data["enrollments"],
        key=lambda e: (e["student_id"], e["course_code"].lower())
    )


def compute_average(student_id: int, course_code: str) -> Optional[float]:
    """
    Average grade for ONE course for ONE student.
    Returns None if no grades yet.
    """
    data = storage.load_data()

    for e in data["enrollments"]:
        if e["student_id"] == student_id and e["course_code"] == course_code:
            grades = e["grades"]
            if not grades:
                return None
            return sum(grades) / len(grades)

    raise ValueError(
        f"Student {student_id} is not enrolled in {course_code}."
    )


def compute_gpa(student_id: int) -> Optional[float]:
    """
    Simple GPA = mean of all course averages for this student.
    Returns None if the student has no graded courses.
    """
    data = storage.load_data()

    # get all enrollments for that student
    avgs = []
    for e in data["enrollments"]:
        if e["student_id"] == student_id:
            grades = e["grades"]
            if grades:
                avgs.append(sum(grades) / len(grades))

    if not avgs:
        return None

    return sum(avgs) / len(avgs)