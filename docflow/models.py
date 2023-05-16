from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.utils.dateparse import parse_date as parse_date_str
from django.db.models.signals import pre_save
from django.core.mail import send_mail
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()

    def get_display_name(self):
        """Return the display name of the profile."""
        return f"{self.full_name} ({self.user.username})"

class Project(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BudgetLine(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Memo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    reference_number = models.CharField(max_length=20, unique=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_memos')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_memos')
    cc = models.ManyToManyField(User, blank=True, null=True, related_name='copied_memos')
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    budget_line = models.ForeignKey(BudgetLine, on_delete=models.SET_NULL, null=True)
    purpose = models.TextField(max_length=500, default="")
    attachment = models.FileField(upload_to='memo_attachments/', blank=True, null=True)

    def get_reference_number_prefix(self):
        return self.sender.profile.department.upper()

    def save(self, *args, **kwargs):
        if not self.reference_number:
            today = date.today().strftime('%Y%m%d')
            count = Memo.objects.filter(created_at__date=date.today()).count() + 1
            prefix = self.get_reference_number_prefix()
            self.reference_number = f'{prefix}-{today}-{count}'
        super().save(*args, **kwargs)


class LeaveRequest(models.Model):
    LEAVE_TYPES = [
        ('annual', 'Annual Leave'),
        ('sick', 'Sick Leave'),
        ('compassionate', 'Compassionate Leave'),
        ('maternity', 'Maternity Leave'),
        ('paternity', 'Paternity Leave'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    staff_id = models.CharField(max_length=20)
    position = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    annual_leave_entitled = models.IntegerField()
    leave_days_taken = models.IntegerField(default=0)
    leave_days_requested = models.IntegerField()
    remaining_leave_days = models.IntegerField(default=0)
    proposed_leave_start_date = models.DateField(null=True, blank=True)
    proposed_leave_end_date = models.DateField(null=True, blank=True)
    handing_over_notes_done = models.BooleanField(default=False)
    resumption_date = models.DateField(null=True, blank=True)
    contact_details = models.CharField(max_length=20)
    is_approved = models.BooleanField(null=True, blank=True)
    is_declined = models.BooleanField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_leave_requests', default=False)
    handing_over_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='handover_leave_requests')

    

    def save(self, *args, **kwargs):
        self.clean_fields()
        self.remaining_leave_days = self.annual_leave_entitled - self.leave_days_taken
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        self.proposed_leave_start_date = self.parse_date(self.proposed_leave_start_date)
        self.proposed_leave_end_date = self.parse_date(self.proposed_leave_end_date)
        self.resumption_date = self.parse_date(self.resumption_date)

    @staticmethod
    def parse_date(value):
        if isinstance(value, str):
            return parse_date_str(value)
        return value
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Create a notification after saving the leave request
        notification = Notification(memo=self)
        notification.send_notification()





    

class Notification(models.Model):
    memo = models.ForeignKey('Memo', on_delete=models.CASCADE, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')

    def send_notification(self):
        recipient = self.memo.recipient
        message = self.generate_message()  # Generate the appropriate message for the notification
        # Code to send the notification message to the recipient

    def generate_message(self):
        # Generate the message based on the memo or leave request
        # You can customize the message format according to your requirements
        # For example:
        message = f"You have a new memo: {self.memo.reference_number}"
        return message
    
    def send_email_notification(self):
        subject = 'Notification from Your App'
        message = self.message
        recipient_list = [self.recipient.email]  # Assuming recipient has an email field

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)







