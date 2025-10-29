import os
import sys
import unittest


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gradebook import service, storage  # noqa: E402


class ServiceTests(unittest.TestCase):
    def setUp(self):

        empty = {"students": [], "courses": [], "enrollments": []}
        storage.save_data(empty)

    def test_add_student(self):
        new_id = service.add_student("Test Student")
        data = storage.load_data()
        self.assertEqual(len(data["students"]), 1)
        self.assertEqual(data["students"][0]["id"], new_id)
        self.assertEqual(data["students"][0]["name"], "Test Student")

    def test_add_grade_and_average(self):

        sid = service.add_student("Bleonit")
        service.add_course("CS101", "Intro")
        service.enroll(sid, "CS101")


        service.add_grade(sid, "CS101", 100)
        service.add_grade(sid, "CS101", 80)

        avg = service.compute_average(sid, "CS101")

        self.assertAlmostEqual(avg, 90.0)

    def test_add_grade_invalid_value(self):

        sid = service.add_student("Alba")
        service.add_course("CS102", "Data Structures")
        service.enroll(sid, "CS102")

        with self.assertRaises(ValueError):
            service.add_grade(sid, "CS102", 150)  # invalid (>100)


if __name__ == "__main__":
    unittest.main()
