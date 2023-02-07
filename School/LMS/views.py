from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import RegisterForm, NotifcationForm
from .models import *

# Create your views here.
# security functions:
def role_check(user, role):
    for item in Profile.objects.filter(user=user):
        if item.role == role:
            return True
        else:
            return False
# These are code for admin of site
def register_user_admin(request):
    all_user = User.objects.all()
    all_profile = Profile.objects.all()
    form = RegisterForm(request.POST or None)
    context = {
        "title": "افزودن کاربر",
        "users": all_user,
        "profiles": all_profile,
        "form": form,
    }
    if form.is_valid():
        username = request.POST['username']
        password = request.POST['password1']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
        if request.POST['role'] == "Teacher":
            for user in all_user:
                if user.username == username:
                    user_obj = user
            Profile.objects.create(user=user_obj, role="Teacher")
            return redirect(f'/account/register/teacher-class?user={user_obj}')
        elif request.POST['role'] == "Student":
            for user in all_user:
                if user.username == username:
                    user_obj = user
            Profile.objects.create(user=user_obj, role="Student")
            return redirect(f'/account/register/student-class?user={user_obj}')
    return render(request, 'LMS/register_user.html', context)

def SelectClassTeacher(request):
    if request.method == "POST":
        for i in User.objects.all():
            if i.username == request.GET['user']:
                user = i
        Teacher.objects.create(user=user, class_subject=request.POST['class_subject'])
        redirect('/account/register')
    return render(request, 'LMS/teacher class.html', {"title": "انتخاب کلاس و درس"})
def SelectClassStudent(request):
    for i in User.objects.all():
        if i.username == request.GET['user']:
            user = i
    if request.method == "POST":
        grade = request.POST['grade']
        clas = request.POST['class']
        Student.objects.create(user=user, grade=grade, clas=clas)
        return redirect('/account/register/')
    return render(request, 'LMS/student class.html', {"title": "انتخاب کلاس و درس", "user": user})

def manage_ticket_notification(request):
    context = {
        'title': 'مدیریت تیکت ها',
        'notifications': Notification.objects.all(),
        'support_tickets': SupportTicket.objects.all(),
    }
    if request.method == 'POST':
        for_users = request.POST.get('for')
        message = request.POST.get('message')
        Notification.objects.create(to=for_users, from_user=request.user, message=message)
        return redirect('/account/manage-tickets-notifs/')
    return render(request, 'LMS/manage tickets notifs.html', context)
def answer_support_ticket(request, id):
    context = {
        'title': f'پاسخ تیکت: {id}',
        'ticket_id': id,
    }
    if SupportTicket.objects.filter(id=id)[0].status:
        context['last_answer'] = SupportTicket.objects.filter(id=id)[0].reply
    if request.method == "POST":
        answer = request.POST.get('answer')
        SupportTicket.objects.filter(id=id).update(status=True, reply=answer)
        return redirect('/account/manage-tickets-notifs/')
    return render(request, 'LMS/answer ticket.html', context)

def edit_notification(request, id):
    # a form for notification with persian label
    obj = get_object_or_404(Notification, id=id)
    form = NotifcationForm(request.POST or None, instance=obj)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('/account/manage-tickets-notifs')
    context = {
        'title': 'ویرایش اعلامیه',
        'id': id,
        'form': form
    }
    return render(request, 'LMS/edit notif.html', context)
# Teacher view are here
def manage_score(request):
    if not role_check(request.user, 'Teacher'):
        return redirect('/account/scores/')
    class_choices2 = []
    context = {
        'title': 'مدیریت نمرات',
        'users': User.objects.all(),
        'scores': Score.objects.all()
    }
    teacher_info = Teacher.objects.filter(user=request.user) or False
    if teacher_info:
        class_choices1 = teacher_info[0].class_subject.split(', ')
        for choice in class_choices1:
            class_choices2.append(choice.replace("_", ' '))
        context['class_choices'] = class_choices2
        if request.GET.get('class_subject_choice'):
            class_subject_choice = request.GET.get('class_subject_choice')
            clas = class_subject_choice[:2]
            subject = class_subject_choice[3:]
            students_list = Student.objects.filter(grade=clas[0], clas=clas.upper()[1])
            context['teacher_subject'] = subject
            context['teacher_class'] = subject
            context['students_list'] = students_list
    else:
        class_choices2 = False
    return render(request, "LMS/manage score.html", context)

def teacher_update_scores(request, student, subject):
    # functions
    def score_exist(title, subject, user):
        for score in Score.objects.all():
            if str(score.title) == str(title) and str(score.subject) == str(subject) and str(score.user) == str(user):
                return True
            else:
                continue

    # get student obj
    for user in Student.objects.all():
        username = user.user
        if str(username) == str(student):
            user_obj = user
            break
    if request.method == "POST":
        title = request.POST.get('title')
        score = request.POST.get('score')
        # add or update scores in Score model
        if score_exist(title, subject, user_obj):
            Score.objects.filter(user=user_obj, title=title, subject=subject).update(score=score)
            redirect('/account/manage-scores/')
        else:
            Score.objects.create(user=user_obj, title=title, subject=subject, score=score)
            redirect('/account/manage-scores/')

    context = {
        'title': 'ویرایش',
        'fullname': User.objects.filter(username=student)[0].get_full_name(),
    }
    return render(request, 'LMS/edit score.html', context)
# student scores
def student_score(request):
    context = {
        'title': 'نمرات',
        'fullname': User.objects.filter(username=request.user)[0].get_full_name(),
        'scores': Score.objects.filter(user=Student.objects.filter(user=request.user)[0]),
    }
    return render(request, 'LMS/score.html', context)

# manage homework from teacher:
def manage_homework(request):
    # functions
    def homework_exist(grade, subject):
        for homework in Homework.objects.all():
            # print(f"{grade} == {homework.class_grade} / {subject} == {homework.subject}")
            if grade == homework.class_grade and subject == homework.subject:
                return True
            else:
                return False
    # make subject and class looks better
    class_subjects = []
    for class_subject in Teacher.objects.filter(user=request.user):
        class_subjects.append(class_subject.class_subject.replace('_', ' '))
    context = {
        'title': 'مدیریت تکالیف',
        'homeworks': Homework.objects.filter(teacher=Teacher.objects.filter(user=request.user)[0]),
        'class_subject': class_subjects
    }
    # get teacher's object
    if request.method == "POST":
        grade = request.POST.get('class')[:2]
        subject = str(request.POST.get('class')[3:])
        homework = request.POST.get('homework')
        check_date = request.POST.get('check_date')
        if homework_exist(grade, subject.replace('-', ' ')):
            Homework.objects.filter(teacher=Teacher.objects.filter(user=request.user)[0], class_grade=grade, subject=subject.replace('-', ' ')).update(homework=homework, check_date=check_date)
            return redirect('/account/manage-homeworks/')
        else:
            Homework.objects.create(teacher=Teacher.objects.filter(user=request.user)[0], class_grade=grade, subject=subject.replace('-', ' '), homework=homework, check_date=check_date)
            return redirect('/account/manage-homeworks/')

    return render(request, 'LMS/manage homework.html', context)
# student's homework
def student_homework(request):
    # get all homeworks for student's class
    homeworks = Homework.objects.filter(class_grade=f"{Student.objects.filter(user=request.user)[0].grade}{Student.objects.filter(user=request.user)[0].clas.lower()}")
    context = {
        'title': 'تکالیف',
        'homeworks': homeworks,
    }
    return render(request, 'LMS/homeworks.html', context)

# teacher's manage exams
def manage_exam(request):
    teacher_classes = []
    for class_subject in Teacher.objects.filter(user=request.user):
        teacher_classes.append(class_subject.class_subject.replace('_', ' '))
    
    if request.method == "POST":
        teacher = request.user
        class_grade = request.POST.get('class_subject')[:2]
        subject = request.POST.get('class_subject')[3:]
        descriptions = request.POST.get('description')
        date = request.POST.get('date')
        Exam.objects.create(teacher=teacher, class_grade=class_grade, subject=subject, descriptions=descriptions, date=date, status=False)
        return redirect('/account/manage-exams/')
    context = {
        'title': 'مدیریت امتحانات',
        'all_exam': Exam.objects.all() or False,
        'teacher_classes': teacher_classes,
    }
    return render(request, 'LMS/manage exams.html', context)
def delete_exam(request, id):
    Exam.objects.filter(id=id).delete()
    return redirect('/account/manage-exams/')
def edit_exam(request, id):
    if request.method == "POST":
        description = request.POST.get('description')
        date = request.POST.get('date')
        status = request.POST.get('status')
        Exam.objects.filter(id=id).update(descriptions=description, date=date, status=status)
        return redirect('/account/manage-exams/')
    context = {
        'title': f'ویرایش امتحان{id}',
        'description_value': Exam.objects.filter(id=id)[0].descriptions,
        'date_value': Exam.objects.filter(id=id)[0].date,
        'id': id,
    }
    return render(request, 'LMS/edit exam.html', context)

# Manage student's exam score (in class)
def edit_examScore(request, id):
    grade = Exam.objects.filter(id=id)[0].class_grade[:1]
    clas = Exam.objects.filter(id=id)[0].class_grade[1:2].upper()
    student_list = Student.objects.filter(grade=grade, clas=clas)
    context = {
        'title': 'ثبت نمرات دانش آموزان',
        'student_list': student_list,
        'users': User.objects.all(),
    }
    return render(request, 'LMS/edit examscore.html', context)
def change_student_examscore(request, id, student_id):
    context = {
        'title': 'ویرایش نمره',
        'exam_id': id,
        'student_id': student_id
    }
    for exam_score in ExamScore.objects.all():
        if int(exam_score.exam_id.id) == int(id) and int(exam_score.student.user_id) == int(student_id):
            context['last_score'] = exam_score.exam_score
            
    if request.method == "POST":
        exist = False
        for instance in ExamScore.objects.all():
            if instance.exam_id.id == id and instance.student.user_id == student_id:
                exist = True
            else:
                continue
        if exist:
            ExamScore.objects.filter(exam_id=Exam.objects.filter(id=id)[0], student=Student.objects.    filter(user_id=student_id)[0]).update(exam_score=request.POST.get('score'))
            return redirect(f'/account/manage-exams/{id}/scores')
        else:
            ExamScore.objects.create(exam_id=Exam.objects.filter(id=id)[0], student=Student.objects.filter(user_id=student_id)[0], exam_score=request.POST.get('score'))
            return redirect(f'/account/manage-exams/{id}/scores')
    return render(request, 'LMS/change student examscore.html', context)

# student see his scores
def student_exam(request):
    class_grade = f"{Student.objects.filter(user=request.user)[0].grade}{Student.objects.filter(user=request.user)[0].clas.lower()}"
    exam_schecdule = Exam.objects.filter(class_grade=class_grade)
    context = {
        'title': 'امتحانات',
        'exam_schedule': exam_schecdule,
        'exam_scores': ExamScore.objects.all()
    }
    return render(request, 'LMS/exams.html', context)
# make a ticekt for students and teachers
def make_ticket(request):
    role = Profile.objects.filter(user=request.user)[0].role
    context = {
        'title': 'تیکت ها',
        'private_tickets': PrivateTicket.objects.filter(from_user=request.user),
        'support_tickets': SupportTicket.objects.filter(from_user=request.user),
        'role': role,
    }
    if role == "Student":
        teachers = []
        for teacher in Teacher.objects.all():
            if teacher.class_subject[:2] == f"{Student.objects.filter(user=request.user)[0].grade}{Student.objects.filter(user=request.user)[0].clas.lower()}":
                teachers.append(teacher)
        context['teachers'] = teachers
    if request.method == "POST":
        for_user = request.POST.get('for')
        message = request.POST.get('message')
        if for_user == "support":
            SupportTicket.objects.create(from_user=request.user, message=message, status=False)
            return redirect('/account/tickets/')
        else:
            PrivateTicket.objects.create(from_user=request.user, to_user=Teacher.objects.filter(user__last_name=for_user)[0], message=message, status=False)
            return redirect('/account/tickets/')
    # if the user is a teacher -> he/she can also answer Private tickets
    if role == "Teacher":
        teacher_tickets = PrivateTicket.objects.filter(to_user__user=request.user)
        context['teacher_tickets'] = teacher_tickets
    return render(request, 'LMS/tickets.html', context)

def answer_ticket(request, id):
    context = {
        'title': f'پاسخ تیکت: {id}',
        'ticket_id': id,
    }
    if PrivateTicket.objects.filter(id=id)[0].status:
        context['last_answer'] = PrivateTicket.objects.filter(id=id)[0].reply
    if request.method == "POST":
        answer = request.POST.get('answer')
        PrivateTicket.objects.filter(id=id).update(status=True, reply=answer)
        return redirect('/account/tickets/')
    return render(request, 'LMS/answer ticket.html', context)
