from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Memo, LeaveRequest
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm
from .models import Memo, LeaveRequest, Notification, Project, BudgetLine
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import LoginForm
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from .forms import CreateMemoForm
from django.views import View
from .forms import CreateMemoForm




@login_required
def create_memo(request):
    if request.method == 'POST':
        form = CreateMemoForm(request.POST, request.FILES)
        if form.is_valid():
            memo = form.save(commit=False)
            memo.sender = request.user  # Set the sender field to the current user
            memo.save()
            form.save_m2m()
        sender = request.user.get_full_name()
        recipient = request.POST.get('recipient')
        cc = request.POST.get('cc')
        project = request.POST.get('project')
        budget_line = request.POST.get('budget_line')
        purpose = request.POST.get('purpose')
        attachment = request.FILES.get('attachment')

        memo = Memo.objects.create(
            recipient=recipient,
            cc=cc,
            project=project,
            budget_line=budget_line,
            purpose=purpose,
            attachment=attachment,
            sender=sender
        )

        # Perform any additional processing or validation as needed

        # Save the memo or perform any other actions

        return redirect('memo_list')
    else:
        form = CreateMemoForm()

    return render(request, 'create_memo.html', {'form': form})

    

@login_required
def memo_list(request):
    memos = Memo.objects.filter(recipient=request.user)
    return render(request, 'memo_list.html', {'memos': memos})


@login_required
def memo_detail(request, memo_id):
    memo = Memo.objects.get(id=memo_id)
    return render(request, 'memo_detail.html', {'memo': memo})





    




@login_required
def leave_request(request):
    if request.method == 'POST':
        # Retrieve form data
        recipient_id = request.POST.get('recipient')
        leave_type_id = request.POST.get('leave_types')
        # ... Retrieve other form fields
        name_id = request.POST.get('name')
        staff_id_id = request.POST.get('staff_id')
        position_id = request.POST.get('position')
        department_id = request.POST.get('department')
        annual_leave_entitled_id = request.POST.get('annual_leave_entitled')
        leave_days_taken_id = request.POST.get('leave_days_taken')
        leave_days_requested_id = request.POST.get('leave_days_requested')
        remaining_leave_days_id = request.POST.get('remaining_leave_days')
        proposed_leave_start_date_id = request.POST.get('proposed_leave_start_date')
        proposed_leave_end_date_id = request.POST.get('proposed_leave_end_date')
        handing_over_notes_done_id = request.POST.get('handing_over_notes_done')
        resumption_date_id = request.POST.get('resumption_date')
        contact_details_id = request.POST.get('contact_details')
        is_approved_id = request.POST.get('is_approved')
        is_declined_id = request.POST.get('is_declined')
        remarks_id = request.POST.get('remarks')
        handing_over_to_id = request.POST.get('handing_over_to')

    

        # Create a new leave request object
        leave_request = LeaveRequest(
            recipient_id=recipient_id,
            # ... Set other leave request fields
            name_id=name_id,
            staff_id_id=staff_id_id,
            position_id=position_id,
            department_id=department_id,
            leave_type_id=leave_type_id,
            annual_leave_entitled_id=annual_leave_entitled_id,
            leave_days_taken_id=leave_days_taken_id,
            leave_days_requested_id=leave_days_requested_id,
            remaining_leave_days_id=remaining_leave_days_id,
            proposed_leave_start_date_id=proposed_leave_start_date_id,
            proposed_leave_end_date_id=proposed_leave_end_date_id,
            handing_over_notes_done_id=handing_over_notes_done_id,
            resumption_date_id=resumption_date_id,
            contact_details_id=contact_details_id,
            is_approved_id=is_approved_id,
            is_declined_id=is_declined_id,
            remarks_id=remarks_id,
            handing_over_to_id=handing_over_to_id,

        )
        leave_request.save()

        # Send notification to the recipient
        notification = Notification(memo=leave_request, recipient=leave_request.recipient)
        notification.send_email_notification()

        # Redirect to a success page or render a success message
        return redirect('leave_request_created')  # Assuming you have a URL pattern named 'leave_request_created'

    else:
        # Render the form to create a new leave request
        leave_types = LeaveRequest.LEAVE_TYPES
        context = {
            # ... Add any context variables needed for the form
            'leave_types': leave_types,
    
        }
    
        return render(request, 'docflow/leave_request.html', context )




def home(request):
    company_logo = '/static/images/wacrenlogo.jpg'
    return render(request, 'home.html', {'company_logo': company_logo})






def base(request):
    company_logo = '/static/images/wacrenlogo.jpg'
    return render(request, 'docflow/base.html', {'company_logo': company_logo})





def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            return redirect('login')
    else:
        form = RegistrationForm()
    company_logo = '/static/images/wacrenlogo.jpg'
    return render(request, 'registration/register.html', {'form': form, 'company_logo': company_logo})




@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    company_logo = '/static/images/wacrenlogo.jpg'
    return render(request, 'registration/login.html', {'form': form, 'company_logo': company_logo})




@login_required
def user_logout(request):
    logout(request)
    return redirect('')




@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})



@login_required
def dashboard(request):
    # Retrieve user activities
    user_activities = get_user_activities(request.user)
    print('User Activities:', user_activities)  # Print the user activities

    # Retrieve reports on memos created
    memos_created = Memo.objects.filter(sender=request.user)
    print('Memos Created:', memos_created)  # Print the memos created


    # Retrieve reports on leave requests
    leave_requests = LeaveRequest.objects.filter(recipient=request.user)
    print('Leave Requests:', leave_requests)  # Print the leave requests

    context = {
        'user_activities': user_activities,
        'memos_created': memos_created,
        'leave_requests': leave_requests,
    }
    company_logo = '/static/images/wacrenlogo.jpg'
    context = {'company_logo': company_logo}
    return render(request, 'dashboard.html', context)






def get_user_activities(user):
    # Retrieve user activities based on your specific logic
    # For example, you can query the database for user-related activities

    # Sample activities list for demonstration purposes
    activities = [
        "Logged in to the system",
        "Created a new memo",
        "Submitted a leave request",
        "Updated user profile",
    ]

    return activities


def fetch_memos(request):
    # Retrieve memos from the "docflow" database
    memos = Memo.objects.using('docflow').all()

    # Pass the memos to the template for rendering
    context = {'memos': memos}
    return render(request, 'memos.html', context)