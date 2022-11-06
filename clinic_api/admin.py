from django.contrib import admin
from clinic_api import models


admin.site.register(models.UserProfile)
admin.site.register(models.Clinic)
admin.site.register(models.Staff)
admin.site.register(models.Patient)
admin.site.register(models.Appointment)
admin.site.register(models.Service)
admin.site.register(models.Report)
admin.site.register(models.Invoice)