from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from ..models import Clinic, DoctorClinicAffiliation, TimeSlot
from ..forms import ClinicForm
from django.contrib.auth.mixins import LoginRequiredMixin

class ClinicListView(LoginRequiredMixin,ListView):
    model = Clinic
    template_name = 'core/clinic/clinic_list.html'
    context_object_name = 'clinics'

class ClinicDetailView(LoginRequiredMixin,DetailView):
    model = Clinic
    template_name = 'core/clinic/clinic_detail.html'
    context_object_name = 'clinic'

class ClinicCreateView(LoginRequiredMixin,CreateView):
    model = Clinic
    form_class = ClinicForm
    template_name = 'core/clinic/clinic_form.html'
    success_url = reverse_lazy('clinic_list')


class ClinicUpdateView(LoginRequiredMixin,UpdateView):
    model = Clinic
    template_name = 'core/clinic/clinic_form.html'
    fields = ['name', 'address', 'city', 'state', 'phone_number', 'email']
    
    def get_success_url(self):
        return reverse('clinic_detail', kwargs={'pk': self.object.pk})

class ClinicDeleteView(LoginRequiredMixin,DeleteView):
    model = Clinic
    template_name = 'core/clinic/clinic_confirm_delete.html'
    success_url = reverse_lazy('clinic_list')

class ClinicDetailView(LoginRequiredMixin,DetailView):
    model = Clinic
    template_name = 'core/clinic/clinic_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        affiliations = DoctorClinicAffiliation.objects.filter(clinic=self.object).prefetch_related('time_slots', 'doctor')
        doctors_data = []
        for affiliation in affiliations:
            schedule = {day: [] for day, _ in TimeSlot.DAYS_OF_WEEK}
            time_slots = affiliation.time_slots.all()
            print(f"Time slots for {affiliation.doctor.name}: {list(time_slots.values('day_of_week', 'start_time'))}")  # Debug print
            for time_slot in time_slots:
                day_number = time_slot.day_of_week
                time_str = dict(TimeSlot.TIME_CHOICES)[time_slot.start_time]
                schedule[day_number].append(time_str)
            
            # Convert day numbers to day names for display
            formatted_schedule = {}
            for day_number, times in schedule.items():
                day_name = dict(TimeSlot.DAYS_OF_WEEK)[day_number]
                if times:
                    formatted_schedule[day_name] = sorted(times)
            
            doctors_data.append({
                'doctor': affiliation.doctor,
                'office_address': affiliation.office_address,
                'schedule': formatted_schedule,
                'affiliation_id': affiliation.id
            })
        context['doctors_data'] = doctors_data
        print("Doctors data:", doctors_data)
        return context