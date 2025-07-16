import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import CodingProblem, UserSubmission
from .ai_feedback import get_ai_feedback, get_basic_feedback


def auth_view(request):
    context = {"login": True}

    if request.method == 'POST':
        action = request.POST.get('action')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if action == 'signup':
            otp = str(random.randint(100000, 999999))
            request.session['temp_user'] = {'username': username, 'password': password, 'otp': otp}

            # Send OTP
            send_mail(
                'Your InterviewPrep OTP Code',
                f'Your OTP is {otp}',
                settings.EMAIL_HOST_USER,
                [username],  # assuming username = email
                fail_silently=False,
            )
            return redirect('verify_otp')

        elif action == 'login':
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')  # replace with your route
            else:
                context['error'] = "Invalid credentials."
            context['login'] = True

    return render(request, 'auth.html', context)


def verify_otp_view(request):
    if request.method == 'POST':
        user_input_otp = request.POST.get('otp')
        temp_user = request.session.get('temp_user', {})

        if temp_user and user_input_otp == temp_user.get('otp'):
            username = temp_user.get('username')
            password = temp_user.get('password')
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            del request.session['temp_user']
            return redirect('dashboard')
        else:
            return render(request, 'verify_otp.html', {'error': "Invalid OTP. Please try again."})

    return render(request, 'verify_otp.html')


def dashboard(request):
    problems = CodingProblem.objects.all()
    return render(request, 'dashboard.html', {'problems': problems})


def problem_list_view(request):
    problems = CodingProblem.objects.all()
    return render(request, 'problem_list.html', {'problems': problems})


def code_editor_view(request, pk):
    problem = get_object_or_404(CodingProblem, pk=pk)

    # Get the next problem (if exists)
    previous_problem = CodingProblem.objects.filter(pk__lt=pk).order_by('-pk').first()
    next_problem = CodingProblem.objects.filter(pk__gt=pk).order_by('pk').first()

    if request.method == 'POST':
        code = request.POST.get('code', '')
        feedback = get_ai_feedback(problem.title, problem.description, code, mode="code")

        UserSubmission.objects.create(
            user=request.user,
            problem=problem,
            code=code,
            feedback=feedback,
        )

        return render(request, 'code_editor.html', {
            'problem': problem,
            'feedback': feedback,
            'submitted_code': code,
            'next_problem': next_problem,  
            'previous_problem': previous_problem,
        })

    return render(request, 'code_editor.html', {
        'problem': problem,
        'next_problem': next_problem,
        'previous_problem': previous_problem,
    })



def behavioral_dashboard(request):
    questions = [
        "Tell me about a time you handled a conflict at work.",
        "What's your greatest strength?",
        "Describe a situation where you showed leadership.",
        "How do you handle criticism?",
    ]

    feedback = None
    submitted_index = None
    submitted_answer = ""

    if request.method == 'POST':
        submitted_answer = request.POST.get('answer', '')
        submitted_index = int(request.POST.get('question_index', 0))

        if submitted_answer.strip():
            feedback = get_ai_feedback(
                title="Behavioral Question",
                description=questions[submitted_index],
                content=submitted_answer,  # Changed from 'code' to 'content'
                mode="behavior"
            )

    return render(request, 'behavioral_dashboard.html', {
        'questions': questions,
        'feedback': feedback,
        'submitted_index': submitted_index,
        'submitted_answer': submitted_answer,
    })