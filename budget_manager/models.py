from django.db import models
from django.utils import timezone

class Brand(models.Model):
    name = models.CharField(max_length=255)
    daily_budget = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_budget = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.name


class Campaign(models.Model):
    brand = models.ForeignKey(Brand, related_name='campaigns', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    paused = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.brand.name})"


class DaypartingSchedule(models.Model):
    campaign = models.OneToOneField(Campaign, related_name='dayparting_schedule', on_delete=models.CASCADE)
    start_hour = models.PositiveSmallIntegerField()  # 0-23
    end_hour = models.PositiveSmallIntegerField()    # 0-23

    def is_active_now(self):
        now_hour = timezone.now().hour
        if self.start_hour <= self.end_hour:
            return self.start_hour <= now_hour < self.end_hour
        else:
            return now_hour >= self.start_hour or now_hour < self.end_hour

    def __str__(self):
        return f"{self.campaign.name} schedule: {self.start_hour} - {self.end_hour}"


class SpendLog(models.Model):
    campaign = models.ForeignKey(Campaign, related_name='spend_logs', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    daily_spend = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monthly_spend = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        unique_together = ('campaign', 'date')

    def __str__(self):
        return f"{self.campaign.name} spend on {self.date}"