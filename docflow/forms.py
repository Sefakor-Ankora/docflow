from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Memo
from .models import User, Project, BudgetLine


class RegistrationForm(UserCreationForm):
    prefix = forms.CharField(max_length=10)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'prefix','password1', 'password2']

class LoginForm(AuthenticationForm):

    pass





class CreateMemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = ['recipient', 'cc', 'project', 'budget_line', 'purpose', 'attachment']
        widgets = {
            'sender': forms.HiddenInput()  # Hide the sender field in the form
        }








class LeaveRequestForm(forms.Form):
    recipient = forms.CharField(max_length=100)
    name = forms.CharField(max_length=100)
    staff_id = forms.CharField(max_length=100)
    position = forms.CharField(max_length=100)
    department = forms.CharField(max_length=100)
    leave_type = forms.CharField(max_length=100)
    annual_leave_entitled = forms.CharField(max_length=100)
    leave_days_taken = forms.CharField(max_length=100)
    leave_days_requested = forms.CharField(max_length=100)
    remaining_leave_days = forms.CharField(max_length=100)
    proposed_leave_start_date = forms.DateField()
    proposed_leave_end_date = forms.DateField()
    handing_over_notes_done = forms.CharField(max_length=100)
    resumption_date = forms.DateField()
    contact_details = forms.CharField(max_length=100)
    is_approved = forms.BooleanField(required=False)
    is_declined = forms.BooleanField(required=False)
    remarks = forms.CharField(max_length=100)
    handing_over_to = forms.CharField(max_length=100)
    
    def clean_proposed_leave_end_date(self):
        start_date = self.cleaned_data.get('proposed_leave_start_date')
        end_date = self.cleaned_data.get('proposed_leave_end_date')

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date cannot be before start date.")
        
        return end_date