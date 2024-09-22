from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Count
from ..models import Doctor, Patient, DoctorClinicAffiliation, TimeSlot
from ..forms import DoctorAffiliationForm, TimeSlotFormSet
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Exists, OuterRef
from ..models import Clinic
from django.contrib.auth.mixins import LoginRequiredMixin

class DoctorListView(LoginRequiredMixin,ListView):
    model = Doctor
    template_name = 'core/doctor/doctor_list.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        return Doctor.objects.annotate(
            clinic_count=Count('clinics', distinct=True),
            patient_count=Count('appointment__patient', distinct=True)
        ).prefetch_related('specialties')

class DoctorDetailView(LoginRequiredMixin,DetailView):
    model = Doctor
    template_name = 'core/doctor/doctor_detail.html'
    context_object_name = 'doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.object

        # Fetch affiliated clinics
        context['affiliated_clinics'] = doctor.clinics.all()

        # Fetch affiliated patients
        affiliated_patients = Patient.objects.filter(
            appointment__doctor=doctor
        ).distinct().order_by('name')

        context['affiliated_patients'] = affiliated_patients

        return context

class DoctorCreateView(LoginRequiredMixin,CreateView):
    model = Doctor
    template_name = 'core/doctor/doctor_form.html'
    fields = ['npi', 'name', 'email', 'phone_number', 'specialties']
    success_url = reverse_lazy('doctor_list')

class DoctorDeleteView( LoginRequiredMixin,DeleteView):
    model = Doctor
    template_name = 'core/doctor/doctor_confirm_delete.html'
    success_url = reverse_lazy('doctor_list')
    success_message = "Doctor was deleted successfully."

class DoctorUpdateView(LoginRequiredMixin,UpdateView):
    model = Doctor
    template_name = 'core/doctor/doctor_form.html'
    fields = ['npi', 'name', 'email', 'phone_number', 'specialties']
    success_url = reverse_lazy('doctor_list')

class DoctorDeleteView(LoginRequiredMixin,DeleteView):
    model = Doctor
    template_name = 'core/doctor/doctor_confirm_delete.html'
    success_url = reverse_lazy('doctor_list')

class AddDoctorAffiliationView(LoginRequiredMixin,CreateView):
    model = DoctorClinicAffiliation
    form_class = DoctorAffiliationForm
    template_name = 'core/clinic/doctor_affiliation_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        clinic_id = self.kwargs.get('clinic_pk')
        clinic = get_object_or_404(Clinic, pk=clinic_id)
        
        # Subquery to check if a doctor is already affiliated with this clinic
        is_affiliated = DoctorClinicAffiliation.objects.filter(
            doctor=OuterRef('pk'),
            clinic=clinic
        )

        # Filter out doctors who are already affiliated with this clinic
        available_doctors = Doctor.objects.annotate(
            is_affiliated=Exists(is_affiliated)
        ).filter(is_affiliated=False)

        form.fields['doctor'].queryset = available_doctors
        return form

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['time_slot_formset'] = TimeSlotFormSet(self.request.POST)
        else:
            data['time_slot_formset'] = TimeSlotFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        time_slot_formset = context['time_slot_formset']
        if form.is_valid() and time_slot_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.clinic = get_object_or_404(Clinic, pk=self.kwargs['clinic_pk'])
            self.object.save()
            
            # Save time slots
            time_slots = []
            for day in range(7):  # 0 to 6 for Monday to Sunday
                start_times = self.request.POST.getlist(f'form-{day}-start_time')
                print(f"Day {day} start times: {start_times}")  # Debug print
                for start_time in start_times:
                    time_slot = TimeSlot(
                        affiliation=self.object,
                        day_of_week=day,
                        start_time=int(start_time)
                    )
                    time_slots.append(time_slot)
            
            print("Time slots to be created:", [(ts.day_of_week, ts.start_time) for ts in time_slots])  # Debug print
            TimeSlot.objects.bulk_create(time_slots)
            
            return redirect('clinic_detail', pk=self.object.clinic.pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class DoctorAffiliationDeleteView(LoginRequiredMixin,DeleteView):
    model = DoctorClinicAffiliation
    template_name = 'core/clinic/doctor_affiliation_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, "Doctor affiliation has been removed successfully.")
        return reverse_lazy('clinic_detail', kwargs={'pk': self.object.clinic.pk})