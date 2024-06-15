import unittest
from employee import Employee
from unittest.mock import patch

class TestEmployee(unittest.TestCase):
    def setUp(self):
        self.emp1 = Employee('Prem', 'Kumar', 100)
        self.emp2 = Employee('Vicky', 'Verna', 1000)

    def tearDown(self):
        return None
    
    def test_fullname(self):
        self.assertEqual(self.emp1.fullname(), 'Prem Kumar')
        self.assertEqual(self.emp2.fullname(), 'Vicky Verna')

    def test_email(self):
        self.assertEqual(self.emp1.email(), 'Prem.Kumar@email.com')
        self.assertEqual(self.emp2.email(), 'Vicky.Verna@email.com')

    def test_apply_raise(self):
        self.assertEqual(self.emp1.apply_raise(),105)
        self.assertEqual(self.emp2.apply_raise(), 1050)


    def test_schedule(self):
        with patch('employee.requests.get') as mocked_get:
            mocked_get.return_value.ok=True
            mocked_get.return_value.text = 'Success'

            schedule = self.emp1.monthly_schedule('June')
            mocked_get.assert_called_with('http://company.com/Kumar/June')
            self.assertEqual(schedule, 'Success')

            mocked_get.return_value.ok=False
            schedule = self.emp2.monthly_schedule('July')
            mocked_get.assert_called_with('http://company.com/Verna/July')
            self.assertEqual(schedule, 'Bad Response!')
if __name__ == '__main__':
    unittest.main()