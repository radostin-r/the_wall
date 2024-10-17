from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from wall.models import WallProfile, DailyIceUsage


class APITest(TestCase):
    def setUp(self):
        self.day = '1'
        self.ice_used = 585
        self.cost = str(self.ice_used * 1900)
        self.profile1 = WallProfile.objects.create(sections='21 25 28')
        self.profile2 = WallProfile.objects.create(sections='17 22 17 19 17')
        DailyIceUsage.objects.create(profile=self.profile1, day=1, ice_used=585, cost=self.cost)

    def test_get_profile_overview(self):
        response = self.client.get(reverse('profiles-profile-overview', kwargs={'profile_id': self.profile1.id, 'day': self.day}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['day'], self.day)
        self.assertEqual(response.data['cost'], self.cost)

    def test_get_daily_usage(self):
        response = self.client.get(reverse('profiles-daily-usage', kwargs={'pk': self.profile1.id, 'day': self.day}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ice_amount'], str(self.ice_used))
        self.assertEqual(response.data['day'], self.day)

    def test_get_daily_overview(self):
        response = self.client.get(reverse('profiles-daily-overview', kwargs={'day': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['day'], self.day)
        self.assertEqual(response.data['cost'], self.cost)

    def test_get_profile_overview(self):
        response = self.client.get(reverse('profiles-total-overview'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['day'], None)
        self.assertEqual(response.data['cost'], self.cost)
