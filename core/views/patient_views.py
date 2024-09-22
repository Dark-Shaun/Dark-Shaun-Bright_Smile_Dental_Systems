from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from ..models import Patient, Visit
from django.contrib.auth.mixins import LoginRequiredMixin

class PatientListView(LoginRequiredMixin,ListView):
    model = Patient
    template_name = 'core/patient/patient_list.html'
    context_object_name = 'patients'

class PatientDetailView(LoginRequiredMixin,DetailView):
    model = Patient
    template_name = 'core/patient/patient_detail.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['visits'] = Visit.objects.filter(patient=self.object).order_by('-date', '-time')
        return context

class PatientCreateView(LoginRequiredMixin,CreateView):
    model = Patient
    template_name = 'core/patient/patient_form.html'
    fields = ['name', 'date_of_birth', 'gender', 'address', 'phone_number', 'ssn_last_4']
    success_url = reverse_lazy('patient_list')

class PatientUpdateView(LoginRequiredMixin,UpdateView):
    model = Patient
    template_name = 'core/patient/patient_form.html'
    fields = ['name', 'date_of_birth', 'gender', 'address', 'phone_number', 'ssn_last_4']
    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.object.pk})

class PatientDeleteView(LoginRequiredMixin,DeleteView):
    model = Patient
    template_name = 'core/patient/patient_confirm_delete.html'
    success_url = reverse_lazy('patient_list')
    success_message = "Patient was deleted successfully."