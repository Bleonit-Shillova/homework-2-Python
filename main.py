"""
Command-line interface for the gradebook project.
"""

import argparse
import logging
import os

from gradebook import service

# logging setup (same log file as storage)
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def parse_positive_int(value: str) -> int:
    try:
        ivalue = int(value)
    except ValueError:
        raise ValueError("must be an integer")

    if ivalue <= 0:
        raise ValueError("must be > 0")
    return ivalue


def parse_grade(value: str) -> float:
    try:
        g = float(value)
    except ValueError:
        raise ValueError("grade must be a number")
    if not (0 <= g <= 100):
        raise ValueError("grade must be between 0 and 100")
    return g


def cmd_add_student(args):
    try:
        new_id = service.add_student(args.name)
        print(f" Added student '{args.name}' with id={new_id}")
    except Exception as e:
        logging.error(f"add-student failed: {e}")
        print(f"ERROR: {e}")


def cmd_add_course(args):
    try:
        service.add_course(args.code, args.title)
        print(f" Added course {args.code} '{args.title}'")
    except Exception as e:
        logging.error(f"add-course failed: {e}")
        print(f"ERROR: {e}")


def cmd_enroll(args):
    try:
        sid = parse_positive_int(args.student_id)
        service.enroll(sid, args.course)
        print(f" Enrolled student {sid} in {args.course}")
    except Exception as e:
        logging.error(f"enroll failed: {e}")
        print(f"ERROR: {e}")


def cmd_add_grade(args):
    try:
        sid = parse_positive_int(args.student_id)
        grade = parse_grade(args.grade)
        service.add_grade(sid, args.course, grade)
        print(f" Added grade {grade} for student {sid} in {args.course}")
    except Exception as e:
        logging.error(f"add-grade failed: {e}")
        print(f"ERROR: {e}")


def cmd_list(args):
    sort_key = getattr(args, "sort", None)

    try:
        if args.what == "students":
            students = service.list_students()
            # optional sort override
            if sort_key == "name":
                students = sorted(students, key=lambda s: s["name"].lower())
            for s in students:
                print(f"[{s['id']}] {s['name']}")

        elif args.what == "courses":
            courses = service.list_courses()
            if sort_key == "code":
                courses = sorted(courses, key=lambda c: c["code"].lower())
            for c in courses:
                print(f"[{c['code']}] {c['title']}")

        elif args.what == "enrollments":
            enrollments = service.list_enrollments()
            for e in enrollments:
                print(
                    f"Student {e['student_id']} in {e['course_code']} -> grades {e['grades']}"
                )
        else:
            print("ERROR: unknown list target")

    except Exception as e:
        logging.error(f"list failed: {e}")
        print(f"ERROR: {e}")


def cmd_avg(args):
    try:
        sid = parse_positive_int(args.student_id)
        avg = service.compute_average(sid, args.course)
        if avg is None:
            print(f"ℹ No grades yet for student {sid} in {args.course}")
        else:
            print(f" Average for student {sid} in {args.course}: {avg:.2f}")
    except Exception as e:
        logging.error(f"avg failed: {e}")
        print(f"ERROR: {e}")


def cmd_gpa(args):
    try:
        sid = parse_positive_int(args.student_id)
        gpa = service.compute_gpa(sid)
        if gpa is None:
            print(f"ℹ No GPA yet for student {sid} (no graded courses).")
        else:
            print(f" GPA for student {sid}: {gpa:.2f}")
    except Exception as e:
        logging.error(f"gpa failed: {e}")
        print(f"ERROR: {e}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gradebook",
        description="Gradebook CLI"
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # add-student
    p_add_student = sub.add_parser("add-student", help="Add a new student")
    p_add_student.add_argument("--name", required=True)
    p_add_student.set_defaults(func=cmd_add_student)

    # add-course
    p_add_course = sub.add_parser("add-course", help="Add a new course")
    p_add_course.add_argument("--code", required=True)
    p_add_course.add_argument("--title", required=True)
    p_add_course.set_defaults(func=cmd_add_course)

    # enroll
    p_enroll = sub.add_parser("enroll", help="Enroll a student in a course")
    p_enroll.add_argument("--student-id", required=True)
    p_enroll.add_argument("--course", required=True)
    p_enroll.set_defaults(func=cmd_enroll)

    # add-grade
    p_add_grade = sub.add_parser("add-grade", help="Add a grade")
    p_add_grade.add_argument("--student-id", required=True)
    p_add_grade.add_argument("--course", required=True)
    p_add_grade.add_argument("--grade", required=True)
    p_add_grade.set_defaults(func=cmd_add_grade)

    # list
    p_list = sub.add_parser("list", help="List students/courses/enrollments")
    p_list.add_argument("what", choices=["students", "courses", "enrollments"])
    p_list.add_argument("--sort", choices=["name", "code"])
    p_list.set_defaults(func=cmd_list)

    # avg
    p_avg = sub.add_parser("avg", help="Compute average for a student in a course")
    p_avg.add_argument("--student-id", required=True)
    p_avg.add_argument("--course", required=True)
    p_avg.set_defaults(func=cmd_avg)

    # gpa
    p_gpa = sub.add_parser("gpa", help="Compute GPA for a student")
    p_gpa.add_argument("--student-id", required=True)
    p_gpa.set_defaults(func=cmd_gpa)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()