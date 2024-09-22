from django.db.models import Q
from datetime import datetime, timedelta
from .models import Clinic, Doctor, TimeSlot, Appointment, Procedure

def get_clinics_for_procedure(procedure):
    return Clinic.objects.filter(doctors__specialties=procedure).distinct()

def get_doctors_for_clinic_and_procedure(clinic, procedure):
    return Doctor.objects.filter(clinics=clinic, specialties=procedure)

def get_available_slots(doctor, clinic, date):
    # Get all time slots for the doctor at the clinic
    all_slots = TimeSlot.objects.filter(
        affiliation__doctor=doctor,
        affiliation__clinic=clinic,
        day_of_week=date.weekday()
    )
    # Get all booked appointments for the doctor on the given date
    booked_appointments = Appointment.objects.filter(
        doctor=doctor,
        clinic=clinic,
        date=date,
        status='scheduled'
    ).values_list('time_slot', flat=True)
    
    available_slots = all_slots.exclude(id__in=booked_appointments)

    return all_slots.exclude(id__in=booked_appointments)