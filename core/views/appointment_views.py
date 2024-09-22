from django.views.generic import View, DetailView, DeleteView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.db import transaction
from ..models import Appointment, Patient, Procedure, Clinic, Doctor
from ..appointment_utils import get_clinics_for_procedure, get_doctors_for_clinic_and_procedure, get_available_slots
from datetime import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

class AppointmentScheduleView(LoginRequiredMixin,View):
    template_name = 'core/appointment/schedule.html'

    def get(self, request):
        procedures = Procedure.objects.all()
        patient_id = request.GET.get('patient_id')
        patient = None
        if patient_id:
            patient = get_object_or_404(Patient, id=patient_id)
        return render(request, self.template_name, {'procedures': procedures, 'patient': patient})

    @method_decorator(require_POST)
    def post(self, request):
        action = request.POST.get('action')
        
        if action == 'get_clinics':
            procedure_id = request.POST.get('procedure_id')
            procedure = get_object_or_404(Procedure, id=procedure_id)
            clinics = get_clinics_for_procedure(procedure)
            return JsonResponse({'clinics': list(clinics.values('id', 'name'))})
        
        elif action == 'get_doctors':
            procedure_id = request.POST.get('procedure_id')
            clinic_id = request.POST.get('clinic_id')
            procedure = get_object_or_404(Procedure, id=procedure_id)
            clinic = get_object_or_404(Clinic, id=clinic_id)
            doctors = get_doctors_for_clinic_and_procedure(clinic, procedure)
            return JsonResponse({'doctors': list(doctors.values('id', 'name'))})
        
        elif action == 'get_slots':
            clinic_id = request.POST.get('clinic_id')
            doctor_id = request.POST.get('doctor_id')
            date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date()
            
            clinic = get_object_or_404(Clinic, id=clinic_id)
            doctor = get_object_or_404(Doctor, id=doctor_id)
            
            slots = get_available_slots(doctor, clinic, date)
            # print(f"Slots for {date}: {list(slots.values('id', 'start_time'))}")
            return JsonResponse({'slots': list(slots.values('id', 'start_time'))})
        
        elif action == 'book_appointment':
            with transaction.atomic():
                patient_id = request.POST.get('patient_id')
                procedure_id = request.POST.get('procedure_id')
                clinic_id = request.POST.get('clinic_id')
                doctor_id = request.POST.get('doctor_id')
                date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date()
                time_slot_id = request.POST.get('time_slot_id')
                
                appointment = Appointment(
                    patient_id=patient_id,
                    procedure_id=procedure_id,
                    clinic_id=clinic_id,
                    doctor_id=doctor_id,
                    date=date,
                    time_slot_id=time_slot_id,
                    status='scheduled'
                )
                
                try:
                    appointment.clean()
                    appointment.save()
                    return JsonResponse({'success': True, 'message': 'Appointment booked successfully!'})
                except ValidationError as e:
                    return JsonResponse({'success': False, 'message': str(e)})
        
        return JsonResponse({'error': 'Invalid action'}, status=400)

class AppointmentDetailView(LoginRequiredMixin,DetailView):
    model = Appointment
    template_name = 'core/appointment/appointment_detail.html'

class AppointmentDeleteView(LoginRequiredMixin,DeleteView):
    model = Appointment
    template_name = 'core/appointment/appointment_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, "Appointment was successfully cancelled.")
        return reverse('patient_detail', kwargs={'pk': self.object.patient.pk})

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)