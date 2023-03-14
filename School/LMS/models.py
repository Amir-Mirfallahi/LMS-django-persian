from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    grade = models.IntegerField(choices=((7, 7), (8, 8), (9, 9)))
    clas = models.CharField(choices=(("A", 'a'), ('B', "b"), ("C", "c")), max_length=30)

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class_subject = models.CharField(max_length=300)

class Score(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    choices = (
        ("semester1", "ترم اول"),
        ("semester1 mostamar", "مستمر ترم اول"),
        ("semester1 exam", "پایانی ترم اول"),
        ("semester2", "ترم دوم"),
        ("semester2 mostamar", "مستمر ترم دوم"),
        ("semester2 exam", "پایانی ترم دوم")
    )
    title = models.CharField(max_length=100, choices=choices)
    SUBJECTS = (
        ('ریاضی', 'ریاضی'),
        ('علوم', 'علوم'),
        ('مطالعات اجتماعی', 'مطالعات اجتماعی'),
        ('ادبیات فارسی', 'ادبیات فارسی'),
        ('عربی', 'عربی'),
        ('قرآن', 'قرآن'),
        ('پیام های آسمان', 'پیام های آسمان'),
        ('نگارش', 'نگارش'),
        ('تفکر و سبک زندگی', 'تفکر و سبک زندگی'),
        ('ورزش', 'ورزش'),
        ('فرهنگ و هنر', 'فرهنگ و هنر'),
        ('کار و فناوری', 'کار و فناوری'),
        ('انگلیسی', 'انگلیسی'),
        ('انضباط', 'انضباط')
    )
    subject = models.CharField(max_length=50, choices=SUBJECTS)
    score = models.FloatField()
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    ROLE = (
        ("Teacher", "Teacher"),
        ("Student", "Student"),
    )
    role = models.CharField(choices=ROLE, max_length=30)
# homework model:
class Homework(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_grade = models.CharField(max_length=5)
    # all subjects
    SUBJECTS = (
        ('ریاضی', 'ریاضی'),
        ('علوم', 'علوم'),
        ('مطالعات اجتماعی', 'مطالعات اجتماعی'),
        ('ادبیات فارسی', 'ادبیات فارسی'),
        ('عربی', 'عربی'),
        ('قرآن', 'قرآن'),
        ('پیام های آسمان', 'پیام های آسمان'),
        ('نگارش', 'نگارش'),
        ('تفکر و سبک زندگی', 'تفکر و سبک زندگی'),
        ('ورزش', 'ورزش'),
        ('فرهنگ و هنر', 'فرهنگ و هنر'),
        ('کار و فناوری', 'کار و فناوری'),
        ('انگلیسی', 'انگلیسی'),
        ('انضباط', 'انضباط')
    )
    subject = models.CharField(max_length=80, choices=SUBJECTS)
    homework = models.TextField(max_length=750)
    check_date = models.DateField()

class Exam(models.Model):
    teacher = models.ForeignKey(User, models.CASCADE)
    class_grade = models.CharField(max_length=5)
    subject = models.CharField(max_length=100)
    descriptions = models.TextField(max_length=250)
    date = models.CharField(max_length=20)
    status = models.BooleanField()

class ExamScore(models.Model):
    exam_id = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, models.CASCADE)
    exam_score = models.FloatField(null=True)

class Notification(models.Model):
    CHOICES = (
        ('همه کاربران', 'همه کاربران'),
        ('همه معلمان', 'همه معلمان'),
        ('همه دانش آموزان', 'همه دانش آموزان'),

    )
    to = models.CharField(choices=CHOICES, max_length=100)
    from_user = models.ForeignKey(User, models.CASCADE)
    message = models.TextField(max_length=600)
class PrivateTicket(models.Model):
    to_user = models.ForeignKey(Teacher, models.CASCADE, related_name='to_user')
    from_user = models.ForeignKey(User, models.CASCADE, related_name='from_user')
    message = models.TextField(max_length=600)
    status = models.BooleanField()
    reply = models.TextField(max_length=1000, null=True)
class SupportTicket(models.Model):
    from_user = models.ForeignKey(User, models.CASCADE, related_name='FromUser')
    message = models.TextField(max_length=600)
    status = models.BooleanField()
    reply = models.TextField(max_length=1000, null=True)
class SampleExam(models.Model):
    SUBJECTS = (
        ('ریاضی', 'ریاضی'),
        ('علوم', 'علوم'),
        ('مطالعات اجتماعی', 'مطالعات اجتماعی'),
        ('ادبیات فارسی', 'ادبیات فارسی'),
        ('عربی', 'عربی'),
        ('قرآن', 'قرآن'),
        ('پیام های آسمان', 'پیام های آسمان'),
        ('نگارش', 'نگارش'),
        ('تفکر و سبک زندگی', 'تفکر و سبک زندگی'),
        ('ورزش', 'ورزش'),
        ('فرهنگ و هنر', 'فرهنگ و هنر'),
        ('کار و فناوری', 'کار و فناوری'),
        ('انگلیسی', 'انگلیسی')
    )
    GRADES = (
        ('7', '7'),
        ('8', '8'),
        ('9', '9')
    )
    subject = models.CharField(max_length=50, choices=SUBJECTS)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    grade = models.CharField(max_length=5, choices=GRADES)
    file = models.FileField(upload_to='static/pdf')

class Request(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    title = models.TextField()
    feedback = models.TextField()
class Festival(models.Model):
    title = models.CharField(max_length=200)
    until_date = models.CharField(max_length=100)
    parts = models.TextField(max_length=1000)

class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=275)
    content = models.TextField(max_length=5000)
    uploaded_time = models.CharField(default=timezone.now(), max_length=100)

    def __str__(self):
        return self.title