from django.contrib import admin
from .models import Clinic, Doctor, Patient, Procedure, Appointment, Visit, DoctorClinicAffiliation, TimeSlot

admin.site.register(Clinic)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Procedure)
admin.site.register(Appointment)
admin.site.register(Visit)
admin.site.register(DoctorClinicAffiliation)
admin.site.register(TimeSlot)