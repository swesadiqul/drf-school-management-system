import unittest
from .tasks import apply_fines
from .models.fees import FeesMaster 
import os
from datetime import datetime, timedelta

# python -m unittest student.tests

# os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings' 
# django.setup()

class TestApplyFines(unittest.TestCase):
    def test_apply_fines(self):
        # Simulate a due date that has passed
        due_date = datetime.now() - timedelta(days=1)

        # Trigger the task
        apply_fines.apply_async(kwargs={'due_date': due_date})

        # Perform assertions to check if fines have been applied correctly
        # Replace the following with actual database queries and assertions

        # Example: Retrieve the FeesMaster object and check if fines have been applied
        # fees_master = FeesMaster.objects.get(due_date=due_date)
        # self.assertTrue(fees_master.fine_applied, "Fines have not been applied")

if __name__ == '__main':
    unittest.main()

