from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import F 
import datetime
from django.core.validators import RegexValidator

# Clinic Model
class Clinic(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)

    def get_affiliated_doctors_count(self):
        return self.doctors.count()

    def get_affiliated_patients_count(self):
        return Patient.objects.filter(appointment__clinic=self).distinct().count()

    def get_available_doctors(self, procedure, date):
        return self.doctors.filter(
            specialties__id=procedure.id,
            doctorclinicaffiliation__workingschedule__day_of_week=date.weekday()
        ).distinct()

    def get_available_timeslots(self, doctor, date):
        booked_slots = Appointment.objects.filter(
            doctor=doctor,
            clinic=self,
            date=date,
            status='scheduled'
        ).values_list('time_slot__start_time', flat=True)

        available_slots = TimeSlot.objects.filter(
            affiliation__doctor=doctor,
            affiliation__clinic=self,
            day_of_week=date.weekday()
        ).exclude(start_time__in=booked_slots)

        return available_slots
    
    def clean(self):
        super().clean()
        errors = {}
        # Check for duplicate phone number
        if Clinic.objects.filter(phone_number=self.phone_number).exclude(pk=self.pk).exists():
            errors['phone_number'] = "A clinic with this phone number already exists."
        # Check for duplicate email
        if Clinic.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            errors['email'] = "A clinic with this email address already exists."

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.name

# Procedure Model
class Procedure(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Doctor Model
class Doctor(models.Model):
    NPI_REGEX = RegexValidator(regex=r'^\d{10}$', message="NPI must be 10 digits")
    
    npi = models.CharField(max_length=10, unique=True, validators=[NPI_REGEX])
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    clinics = models.ManyToManyField('Clinic', through='DoctorClinicAffiliation', related_name='doctors')
    specialties = models.ManyToManyField(Procedure)

    def clean(self):
        super().clean()
        if Doctor.objects.filter(npi=self.npi).exclude(pk=self.pk).exists():
            existing_doctor = Doctor.objects.get(npi=self.npi)
            raise ValidationError({
                'npi': f"A doctor with this NPI already exists: {existing_doctor.name} (NPI: {existing_doctor.npi})"
            })
    
    def get_affiliated_clinics_count(self):
        return self.clinics.count()

    def get_affiliated_patients_count(self):
        return Patient.objects.filter(appointment__doctor=self).distinct().count()

    def get_schedule(self, clinic, date):
        return TimeSlot.objects.filter(
            affiliation__doctor=self,
            affiliation__clinic=clinic,
            day_of_week=date.weekday()
        )

    def is_available(self, clinic, date, time_slot):
        return not Appointment.objects.filter(
            doctor=self,
            clinic=clinic,
            date=date,
            time_slot=time_slot,
            status='scheduled'
        ).exists()

    def __str__(self):
        return f"{self.name} (NPI: {self.npi})"

# Patient Model
class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    ssn_last_4 = models.CharField(max_length=4)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    class Meta:
        unique_together = ['name', 'date_of_birth', 'ssn_last_4']

    def get_last_visit(self):
        return self.visits.order_by('-date', '-time').first()

    def get_next_appointment(self):
        return self.appointment_set.filter(
            status='scheduled',
            date__gte=timezone.now().date()
        ).order_by('date',F('time_slot__start_time')).first()

    def get_visit_history(self):
        return self.visits.all().order_by('-date', '-time')

    def get_upcoming_appointments(self):
        return self.appointment_set.filter(
            status='scheduled',
            date__gte=timezone.now().date()
        ).order_by('date', F('time_slot__start_time'))

    def clean(self):
        super().clean()
        if Patient.objects.filter(
            name=self.name,
            date_of_birth=self.date_of_birth,
            ssn_last_4=self.ssn_last_4
        ).exclude(pk=self.pk).exists():
            raise ValidationError("A patient with this name, date of birth, and SSN already exists.")

    def __str__(self):
        return self.name

# DoctorClinicAffiliation Model
class DoctorClinicAffiliation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    office_address = models.TextField()

    class Meta:
        unique_together = ('doctor', 'clinic')

    def __str__(self):
        return f"{self.doctor.name} at {self.clinic.name}"

# TimeSlot Model
class TimeSlot(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    TIME_CHOICES = [
        (9, '9:00 AM'),
        (10, '10:00 AM'),
        (11, '11:00 AM'),
        (12, '12:00 PM'),
        (13, '1:00 PM'),
        (14, '2:00 PM'),
        (15, '3:00 PM'),
        (16, '4:00 PM'),
        (17, '5:00 PM'),
    ]
    affiliation = models.ForeignKey(DoctorClinicAffiliation, on_delete=models.CASCADE, related_name='time_slots')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.IntegerField(choices=TIME_CHOICES)

    class Meta:
        unique_together = ['affiliation', 'day_of_week', 'start_time']

    def __str__(self):
        return f"{self.get_day_of_week_display()} {self.get_start_time_display()} ({self.affiliation})"

# Appointment Model
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE,default=None)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    date_booked = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['time_slot', 'date']
        
    def clean(self):
        super().clean()
        if not self.doctor.is_available(self.clinic, self.date, self.time_slot):
            raise ValidationError("The selected doctor is not available at this time.")

        if Appointment.objects.filter(
            clinic=self.clinic,
            date=self.date,
            time_slot=self.time_slot,
            status='scheduled'
        ).exclude(pk=self.pk).exists():
            raise ValidationError("This time slot is already booked.")
    
    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name} - {self.date} {self.time_slot.start_time}"

# Visit Model
class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    clinic = models.ForeignKey('Clinic', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    procedures = models.ManyToManyField('Procedure')
    doctor_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name} - {self.date} {self.time}"