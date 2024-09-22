from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Clinic, Doctor, Patient, Procedure, DoctorClinicAffiliation, TimeSlot, Appointment, Visit
from django.utils import timezone

User = get_user_model()

class DentalManagementSystemTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username='shaun',
            email='shaun@example.com',
            password='shaunak'
        )
        self.clinic = Clinic.objects.create(
            name='Test Clinic',
            address='123 Test St',
            city='Test City',
            state='TS',
            phone_number='1234567890',
            email='testclinic@example.com'
        )
        self.procedure = Procedure.objects.create(name='Cleaning')
        self.doctor = Doctor.objects.create(
            npi='1234567890',
            name='Dr. Test',
            email='drtest@example.com',
            phone_number='0987654321'
        )
        self.doctor.specialties.add(self.procedure)
        self.affiliation = DoctorClinicAffiliation.objects.create(
            doctor=self.doctor,
            clinic=self.clinic,
            office_address='123 Office St'
        )
        self.time_slot = TimeSlot.objects.create(
            affiliation=self.affiliation,
            day_of_week=0,
            start_time=9
        )
        self.patient = Patient.objects.create(
            name='Test Patient',
            address='789 Patient St',
            phone_number='1122334455',
            date_of_birth='1990-01-01',
            ssn_last_4='6789',
            gender='M'
        )

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'shaun',
            'password': 'shaunak'
        })
        self.assertRedirects(response, reverse('home'))

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {
            'username': 'shaun',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your username and password didn't match. Please try again.")

    def test_clinics_list(self):
        self.client.login(username='shaun', password='shaunak')
        response = self.client.get(reverse('clinic_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Clinic')

    def test_doctors_list(self):
        self.client.login(username='shaun', password='shaunak')
        response = self.client.get(reverse('doctor_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dr. Test')

    def test_patients_list(self):
        self.client.login(username='shaun', password='shaunak')
        response = self.client.get(reverse('patient_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Patient')

    def test_add_clinic(self):
        self.client.login(username='shaun', password='shaunak')
        response = self.client.post(reverse('clinic_create'), {
            'name': 'New Clinic',
            'address': '456 New St',
            'city': 'New City',
            'state': 'NS',
            'phone_number': '5556667777',
            'email': 'newclinic@example.com'
        })
        if response.status_code != 302:
            print("Add Clinic Form Errors:", response.context['form'].errors if 'form' in response.context else "No form in context")
            print("Response Content:", response.content)
        self.assertRedirects(response, reverse('clinic_list'))
        self.assertTrue(Clinic.objects.filter(name='New Clinic').exists())

    def test_add_doctor(self):
        self.client.login(username='shaun', password='shaunak')
        response = self.client.post(reverse('doctor_create'), {
            'npi': '9876543210',
            'name': 'Dr. New',
            'email': 'drnew@example.com',
            'phone_number': '7778889999',
            'specialties': [self.procedure.id],
            'clinics': [self.clinic.id]
        })
        if response.status_code != 302:
            print("Add Doctor Form Errors:", response.context['form'].errors if 'form' in response.context else "No form in context")
            print("Response Content:", response.content)
        self.assertRedirects(response, reverse('doctor_list'))
        self.assertTrue(Doctor.objects.filter(name='Dr. New').exists())

    def test_add_patient(self):
        self.client.login(username='shaun', password='shaunak')
        response = self.client.post(reverse('patient_create'), {
            'name': 'New Patient',
            'address': '456 New St',
            'phone_number': '3334445555',
            'date_of_birth': '1995-05-05',
            'ssn_last_4': '4321',
            'gender': 'F'
        })
        if response.status_code != 302:
            print("Add Patient Form Errors:", response.context['form'].errors if 'form' in response.context else "No form in context")
            print("Response Content:", response.content)
        self.assertRedirects(response, reverse('patient_list'))
        self.assertTrue(Patient.objects.filter(name='New Patient').exists())

    def test_clinic_detail(self):
        self.client.login(username='shaun', password='shaunak')
        response = self.client.get(reverse('clinic_detail', kwargs={'pk': self.clinic.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Clinic')

    def test_doctor_detail(self):
        self.client.login(username='shaun', password='shaunak')
        response = self.client.get(reverse('doctor_detail', kwargs={'pk': self.doctor.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dr. Test')

    def test_patient_detail(self):
        self.client.login(username='shaun', password='shaunak')
        response = self.client.get(reverse('patient_detail', kwargs={'pk': self.patient.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Patient')

    def test_unauthenticated_access(self):
        response = self.client.get(reverse('clinic_list'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('clinic_list')}")

    def test_logout(self):
        self.client.login(username='shaun', password='shaunak')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

def test_add_visit(self):
    self.client.login(username='shaun', password='shaunak')
    url = reverse('visit_create') + f'?patient_id={self.patient.id}'  # Add patient_id to GET parameters
    response = self.client.post(url, {
        'doctor': self.doctor.id,
        'clinic': self.clinic.id,
        'date': '2023-06-01',
        'time': '09:00:00',
        'procedures': [self.procedure.id],
        'doctor_notes': 'Test visit notes'
    })
    if response.status_code != 302:
        print("Add Visit Form Errors:", response.context['form'].errors if 'form' in response.context else "No form in context")
        print("Response Content:", response.content)
    self.assertRedirects(response, reverse('visit_list'))  # Make sure this name matches your URL pattern
    self.assertTrue(Visit.objects.filter(patient=self.patient, doctor=self.doctor).exists())