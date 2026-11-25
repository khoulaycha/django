from django.contrib import admin
from .models import Appointment

# Register your models here.
#admin.site.register(Appointment)

@admin.action(description="make them confirmed")
def confirm_appointment(model, request, queryset):
    queryset.update(status='CONFIRMED')

@admin.register(Appointment)
class AppointmentAdminPers(admin.ModelAdmin):
    actions = [confirm_appointment]
    list_display = ('reason', 'status', 'duration_minutes', 'appointment_date')
    list_filter = ('status', 'appointment_date')
    list_editable=('status',)
    search_fields=("reason", "status")
    ordering=("-appointment_date",)
    fieldsets = (
        ('Description', {
            'fields': ('reason', 'status', 'prescription')
        }),
        ('Date + Duration', {
            'fields': ('appointment_date', 'duration_minutes')
        }),
        ('Patient/doctor', {
            'fields': ('patient', 'doctor')
        }),
        ('Planification', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

