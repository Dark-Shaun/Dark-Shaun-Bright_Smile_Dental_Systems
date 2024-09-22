from django import forms
from .models import Clinic, DoctorClinicAffiliation
from .models import Doctor, Procedure
from .models import DoctorClinicAffiliation, TimeSlot


# Clinic forms Section
class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = ['name', 'address', 'phone_number', 'city', 'state','email']

class TimeSlotForm(forms.ModelForm):
    start_time = forms.MultipleChoiceField(
        choices=[(str(i), f"{i:02d}:00") for i in range(9, 18)],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = TimeSlot
        fields = ['day_of_week', 'start_time']

TimeSlotFormSet = forms.inlineformset_factory(
    DoctorClinicAffiliation, TimeSlot, form=TimeSlotForm,
    extra=6, max_num=6, can_delete=True
)

# Doctor forms Section
class DoctorForm(forms.ModelForm):
    specialties = forms.ModelMultipleChoiceField(
        queryset=Procedure.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Doctor
        fields = ['npi', 'name', 'email', 'phone_number', 'specialties']

class DoctorAffiliationForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.none(), empty_label="Select a doctor")

    class Meta:
        model = DoctorClinicAffiliation
        fields = ['doctor', 'office_address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'doctor' in self.fields:
            self.fields['doctor'].queryset = Doctor.objects.all()