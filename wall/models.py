from django.db import models


class WallProfile(models.Model):
    sections = models.CharField(max_length=500)  # Space-separated string of section heights

    def get_sections(self):
        return list(map(int, self.sections.split()))

    def calculate_total_cost(self):
        daily_usages = self.daily_usages.all()
        daily_costs = [daily.cost for daily in daily_usages]
        return sum(daily_costs)

    def __str__(self):
        return f'WallProfile {self.id}'


class DailyIceUsage(models.Model):
    profile = models.ForeignKey(WallProfile, related_name='daily_usages', on_delete=models.CASCADE)
    day = models.IntegerField()
    ice_used = models.IntegerField()
    cost = models.IntegerField()

    def __str__(self):
        return f'DailyIceUsage day={self.day} profile_id={self.profile.id}'
