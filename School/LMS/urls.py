from django.urls import path
from .views import (
    # admin
        register_user_admin,
        SelectClassTeacher,
        SelectClassStudent,
        manage_ticket_notification,
        edit_notification,
        answer_support_ticket,
    #student
        student_score,
        student_homework,
        student_exam,
        make_ticket,
    #teacher
        manage_score,
        teacher_update_scores,
        manage_homework,
        manage_exam,
        edit_exam,
        delete_exam,
        edit_examScore,
        change_student_examscore,
        answer_ticket,

)

urlpatterns = [
    # admin views:
    path('register/', register_user_admin),
    path('register/teacher-class', SelectClassTeacher),
    path('register/student-class', SelectClassStudent),
    path('manage-tickets-notifs/', manage_ticket_notification),
    path('manage-tickets-notifs/<int:id>/edit-notif/', edit_notification),
    path('manage-tickets-notifs/<int:id>/answer/', answer_support_ticket),
    # teachers views:
    path('manage-scores/', manage_score),
    path('manage-scores/<str:subject>/<str:student>/', teacher_update_scores),
    path('manage-homeworks/', manage_homework),
    path('manage-exams/', manage_exam),
    path('manage-exams/<int:id>/edit/', edit_exam),
    path('manage-exams/<int:id>/scores/', edit_examScore),
    path('manage-exams/<int:id>/scores/<int:student_id>', change_student_examscore),
    path('manage-exams/<int:id>/delete/', delete_exam),
    path('tickets/<int:id>/answer/', answer_ticket),
    # students views:
    path('scores/', student_score),
    path('homeworks/', student_homework),
    path('exams/', student_exam),
    path('tickets/', make_ticket)
]
