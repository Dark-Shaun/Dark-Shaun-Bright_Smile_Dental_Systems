from .home_view import HomeView
from .clinic_views import (
    ClinicListView, ClinicDetailView, ClinicCreateView, 
    ClinicUpdateView, ClinicDeleteView
)
from .doctor_views import (
    DoctorListView, DoctorDetailView, DoctorCreateView, 
    DoctorUpdateView, DoctorDeleteView, AddDoctorAffiliationView, 
    DoctorAffiliationDeleteView
)
from .patient_views import (
    PatientListView, PatientDetailView, PatientCreateView, 
    PatientUpdateView, PatientDeleteView
)
from .visit_views import (
    VisitListView, VisitDetailView, VisitCreateView, VisitDeleteView
)
from .appointment_views import (
    AppointmentScheduleView, AppointmentDetailView, AppointmentDeleteView
)
from .api_views import (
    PatientCreateAPIView, DoctorCreateAPIView, 
    ClinicCreateAPIView, ClinicRetrieveAPIView
)
from .auth_views import CustomLoginView,CustomLogoutView