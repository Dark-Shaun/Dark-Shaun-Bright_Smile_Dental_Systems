from django.contrib import admin
from django.urls import path, include
from core.views import HomeView
from core.views.clinic_views import (
    ClinicListView, ClinicDetailView, ClinicCreateView, 
    ClinicUpdateView, ClinicDeleteView 
)
from core.views.doctor_views import (
    DoctorListView, DoctorDetailView, DoctorCreateView, 
    DoctorUpdateView, DoctorDeleteView, DoctorAffiliationDeleteView, AddDoctorAffiliationView
)
from core.views.patient_views import (
    PatientListView, PatientDetailView, PatientCreateView, 
    PatientUpdateView, PatientDeleteView
)
from core.views.visit_views import (
    VisitListView, VisitDetailView, VisitCreateView, VisitDeleteView
)
from core.views.appointment_views import (
    AppointmentDeleteView, AppointmentScheduleView, AppointmentDetailView
)
from core.views.api_views import (
    PatientCreateAPIView, DoctorCreateAPIView, 
    ClinicCreateAPIView, ClinicRetrieveAPIView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', HomeView.as_view(), name='home'),
    
    # Clinic URLs
    path('clinics/', ClinicListView.as_view(), name='clinic_list'),
    path('clinics/<int:pk>/', ClinicDetailView.as_view(), name='clinic_detail'),
    path('clinics/create/', ClinicCreateView.as_view(), name='clinic_create'),
    path('clinics/<int:pk>/edit/', ClinicUpdateView.as_view(), name='clinic_edit'),
    path('clinics/<int:pk>/delete/', ClinicDeleteView.as_view(), name='clinic_delete'),
    path('clinics/<int:clinic_pk>/add_doctor/', AddDoctorAffiliationView.as_view(), name='add_doctor_affiliation'),
    
    # Doctor URLs
    path('doctors/', DoctorListView.as_view(), name='doctor_list'),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor_detail'),
    path('doctors/create/', DoctorCreateView.as_view(), name='doctor_create'),
    path('doctors/<int:pk>/edit/', DoctorUpdateView.as_view(), name='doctor_edit'),
    path('doctors/<int:pk>/delete/', DoctorDeleteView.as_view(), name='doctor_delete'),
    path('doctor-affiliation/<int:pk>/delete/', DoctorAffiliationDeleteView.as_view(), name='delete_doctor_affiliation'),
    
    # Patient URLs
    path('patients/', PatientListView.as_view(), name='patient_list'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
    path('patients/create/', PatientCreateView.as_view(), name='patient_create'),
    path('patients/<int:pk>/edit/', PatientUpdateView.as_view(), name='patient_edit'),
    path('patients/<int:pk>/delete/', PatientDeleteView.as_view(), name='patient_delete'),
    
    # Visit URLs
    path('visits/', VisitListView.as_view(), name='visit_list'),
    path('visits/<int:pk>/', VisitDetailView.as_view(), name='visit_detail'),
    path('visits/create/', VisitCreateView.as_view(), name='visit_create'),
    path('visits/<int:pk>/delete/', VisitDeleteView.as_view(), name='visit_delete'),
    
    # Appointment URLs
    path('appointments/<int:pk>/delete/', AppointmentDeleteView.as_view(), name='appointment_delete'),
    path('appointments/schedule/', AppointmentScheduleView.as_view(), name='appointment_schedule'),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='appointment_detail'),

    # API URLs
    path('api/patients/create/', PatientCreateAPIView.as_view(), name='api_patient_create'),
    path('api/doctors/create/', DoctorCreateAPIView.as_view(), name='api_doctor_create'),
    path('api/clinics/create/', ClinicCreateAPIView.as_view(), name='api_clinic_create'),
    path('api/clinics/<int:pk>/', ClinicRetrieveAPIView.as_view(), name='api_clinic_retrieve'),
]