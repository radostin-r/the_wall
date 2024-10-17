from unittest import skip

from django.core.management import call_command
from django.test import TestCase
from wall.models import WallProfile, DailyIceUsage

from unittest.mock import patch
from the_wall.settings import BASE_DIR


class ManagementCommandTest(TestCase):
    def setUp(self):
        # Create sample wall profiles to be used in the command
        self.profile = WallProfile.objects.create(sections='21 25 28')

    def test_command_calculate_daily_ice_usage(self):
        call_command('start_work')

        daily_usages = DailyIceUsage.objects.filter(profile=self.profile).count()
        self.assertEqual(daily_usages, 9)

    @patch('multiprocessing.pool.ApplyResult.get', return_value=[])
    @patch('wall.workers.build_wall.worker')
    @skip("Not working as expected")
    def test_command_multiprocessing(self, mock_worker, mock_result):
        # Mock the behavior of the worker function
        mock_worker.return_value = None
        mock_result.return_value = []

        # Execute the command
        call_command('start_work', num_teams=4)

        self.assertEqual(mock_worker.call_count, 4)

    def test_command_insert_profiles(self):
        call_command('insert_profiles', f'{BASE_DIR}/profiles.txt')
        profiles = WallProfile.objects.all()

        self.assertEqual(profiles.count(), 4)
