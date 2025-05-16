from django.contrib import admin
from .models import Brand, Campaign, DaypartingSchedule, SpendLog

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'daily_budget', 'monthly_budget')


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'is_active', 'paused')
    list_filter = ('brand', 'is_active', 'paused')


@admin.register(DaypartingSchedule)
class DaypartingScheduleAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'start_hour', 'end_hour')


@admin.register(SpendLog)
class SpendLogAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'date', 'daily_spend', 'monthly_spend')
    list_filter = ('date',)