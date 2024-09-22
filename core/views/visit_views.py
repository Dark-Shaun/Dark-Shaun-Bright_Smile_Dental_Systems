from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy, reverse
from ..models import Visit, Patient
from django.contrib.auth.mixins import LoginRequiredMixin

class VisitListView(LoginRequiredMixin,ListView):
    model = Visit
    template_name = 'core/visit/visit_list.html'
    context_object_name = 'visits'

class VisitDetailView(LoginRequiredMixin,DetailView):
    model = Visit
    template_name = 'core/visit/visit_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        visit = self.object
        context['procedures'] = visit.procedures.all()
        return context

class VisitDeleteView(LoginRequiredMixin, DeleteView):
    model = Visit
    template_name = 'core/visit/visit_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.object.patient.pk})

class VisitCreateView(LoginRequiredMixin,CreateView):
    model = Visit
    template_name = 'core/visit/visit_form.html'
    fields = ['doctor', 'clinic', 'date', 'time', 'procedures', 'doctor_notes']

    def form_valid(self, form):
        form.instance.patient = Patient.objects.get(pk=self.request.GET.get('patient_id'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.object.patient.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(pk=self.request.GET.get('patient_id'))
        return context