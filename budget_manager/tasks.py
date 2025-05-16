from celery import shared_task
from django.utils import timezone
from .models import Campaign, SpendLog, DaypartingSchedule

@shared_task
def reset_daily_spends():
    today = timezone.now().date()
    # Reset daily spend logs or create them if missing
    campaigns = Campaign.objects.all()
    for campaign in campaigns:
        spend_log, created = SpendLog.objects.get_or_create(campaign=campaign, date=today)
        spend_log.daily_spend = 0
        spend_log.save()
        # Reactivate campaign if paused due to spend
        if campaign.paused:
            campaign.paused = False
            campaign.save()


@shared_task
def reset_monthly_spends():
    today = timezone.now().date()
    first_of_month = today.replace(day=1)
    campaigns = Campaign.objects.all()
    for campaign in campaigns:
        # Reset monthly spend on all spend logs for current month
        # We will reset monthly spend in SpendLogs for today (new record)
        spend_log, created = SpendLog.objects.get_or_create(campaign=campaign, date=today)
        spend_log.monthly_spend = 0
        spend_log.save()
        # Reactivate campaign if paused due to monthly budget
        if campaign.paused:
            campaign.paused = False
            campaign.save()


@shared_task
def enforce_dayparting():
    now = timezone.now()
    campaigns = Campaign.objects.all()
    for campaign in campaigns:
        try:
            schedule = campaign.dayparting_schedule
        except DaypartingSchedule.DoesNotExist:
            continue  # No schedule means no restriction

        if schedule.is_active_now():
            # Enable campaign if it was paused only due to dayparting
            if campaign.paused:
                campaign.paused = False
                campaign.save()
        else:
            # Pause campaign due to dayparting window
            if not campaign.paused:
                campaign.paused = True
                campaign.save()


@shared_task
def enforce_budgets():
    today = timezone.now().date()
    campaigns = Campaign.objects.all()

    for campaign in campaigns:
        spend_log, created = SpendLog.objects.get_or_create(campaign=campaign, date=today)

        brand = campaign.brand

        # Pause if daily or monthly spend exceeds budget
        if spend_log.daily_spend > brand.daily_budget or spend_log.monthly_spend > brand.monthly_budget:
            if not campaign.paused:
                campaign.paused = True
                campaign.save()
        else:
            # If spend is under budget, unpause if paused for budget reasons
            if campaign.paused:
                campaign.paused = False
                campaign.save()