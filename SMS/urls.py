"""SMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from SMS_MYSQL.views import account, admin, student, classes, course, major, teacher, teaching_plan, teaching_duty, student_course, student_extra, student_expel

urlpatterns = [
    # path("admin/", admin.site.urls),
    #管理员
    path("admin/list/", admin.admin_list),
    path("admin/add/", admin.admin_add),
    path("admin/<int:nid>/delete/", admin.admin_delete),
    path("admin/<int:nid>/edit/", admin.admin_edit),
    path("admin/<int:nid>/reset/", admin.admin_reset),

    #登录
    path("login/", account.login),
    path("logout/", account.logout),
    path("image/code/", account.image_code),

    # 学生管理
    path("student/list/", student.student_list),
    path("student/add/", student.student_add),
    path("student/<int:nid>/edit/", student.student_edit),
    path("student/<int:nid>/delete/", student.student_delete),

    # 班级管理
    path("classes/list/", classes.classes_list),
    path("classes/add/", classes.classes_add),
    path("classes/<int:nid>/edit/", classes.classes_edit),
    path("classes/<int:nid>/delete/", classes.classes_delete),

    # 课程管理
    path("course/list/", course.course_list),
    path("course/add/", course.course_add),
    path("course/<int:nid>/edit/", course.course_edit),
    path("course/<int:nid>/delete/", course.course_delete),

    # 专业管理
    path("major/list/", major.major_list),
    path("major/add/", major.major_add),
    path("major/<int:nid>/edit/", major.major_edit),
    path("major/<int:nid>/delete/", major.major_delete),

    # 教师管理
    path("teacher/list/", teacher.teacher_list),
    path("teacher/add/", teacher.teacher_add),
    path("teacher/<int:nid>/edit/", teacher.teacher_edit),
    path("teacher/<int:nid>/delete/", teacher.teacher_delete),

    # 授课计划管理
    path("teaching/plan/list/", teaching_plan.teaching_plan_list),
    path("teaching/plan/add/", teaching_plan.teaching_plan_add),
    path("teaching/plan/<int:nid>/edit/", teaching_plan.teaching_plan_edit),
    path("teaching/plan/<int:nid>/delete/", teaching_plan.teaching_plan_delete),

    # 授课职责管理
    path("teaching/duty/list/", teaching_duty.teaching_duty_list),
    path("teaching/duty/add/", teaching_duty.teaching_duty_add),
    path("teaching/duty/<int:nid>/edit/", teaching_duty.teaching_duty_edit),
    path("teaching/duty/<int:nid>/delete/", teaching_duty.teaching_duty_delete),

    # 选课管理
    path("student/course/list/", student_course.student_course_list),
    path("student/course/add/", student_course.student_course_add),
    path("student/course/<int:nid>/edit/", student_course.student_course_edit),
    path("student/course/<int:nid>/delete/", student_course.student_course_delete),

    # 学生额外信息查询
    path("student/extra/list/", student_extra.student_extra_list),

    # 即将开除学生查询
    path("student/expel/list/", student_expel.student_expel_list),

]
