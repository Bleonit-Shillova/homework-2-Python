import os
import sys
import unittest

# Ensure project root is on sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gradebook import service, storage  # noqa: E402


class ServiceTests(unittest.TestCase):
    def setUp(self):
        # before each test: start with clean data file
        empty = {"students": [], "courses": [], "enrollments": []}
        storage.save_data(empty)

    def test_add_student(self):
        new_id = service.add_student("Test Student")
        data = storage.load_data()
        self.assertEqual(len(data["students"]), 1)
        self.assertEqual(data["students"][0]["id"], new_id)
        self.assertEqual(data["students"][0]["name"], "Test Student")

    def test_add_grade_and_average(self):
        # setup student, course, enrollment
        sid = service.add_student("Bleonit")
        service.add_course("CS101", "Intro")
        service.enroll(sid, "CS101")

        # add grades
        service.add_grade(sid, "CS101", 100)
        service.add_grade(sid, "CS101", 80)

        avg = service.compute_average(sid, "CS101")
        # average of 100 and 80 is 90
        self.assertAlmostEqual(avg, 90.0)

    def test_add_grade_invalid_value(self):
        # adding an invalid grade should raise ValueError
        sid = service.add_student("Alba")
        service.add_course("CS102", "Data Structures")
        service.enroll(sid, "CS102")

        with self.assertRaises(ValueError):
            service.add_grade(sid, "CS102", 150)  # invalid (>100)


if __name__ == "__main__":
    unittest.main()
