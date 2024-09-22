from rest_framework import serializers
from .models import Patient, Doctor, Clinic

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name', 'address', 'phone_number', 'date_of_birth', 'ssn_last_4', 'gender']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'npi', 'name', 'email', 'phone_number']

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ['id', 'name', 'address', 'city', 'state', 'phone_number', 'email']