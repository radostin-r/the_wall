from django.test import TestCase
from wall.models import WallProfile, DailyIceUsage


class WallProfileModelTest(TestCase):
    def setUp(self):
        # Set up a sample wall profile
        WallProfile.objects.create(sections='21 25 28')
        WallProfile.objects.create(sections='17 22 17 19 17')

    def test_wall_profile_creation(self):
        profile = WallProfile.objects.get(id=1)
        self.assertEqual(profile.get_sections(), [21, 25, 28])


class DailyUsageModelTest(TestCase):
    def setUp(self):
        # Create a wall profile and a corresponding daily usage entry
        self.profile = WallProfile.objects.create(sections='21 25 28')
        DailyIceUsage.objects.create(profile=self.profile, day=1, ice_used=585, cost=585 * 1900)

    def test_daily_usage_creation(self):
        usage = DailyIceUsage.objects.get(profile=self.profile, day=1)
        self.assertEqual(usage.ice_used, 585)
