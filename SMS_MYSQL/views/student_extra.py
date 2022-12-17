from django.db import connection

from django.shortcuts import render, redirect

from SMS_MYSQL import models
from SMS_MYSQL.utils.bootstrap import BootStrapModelForm

from SMS_MYSQL.utils.raw import custom_sql_get_dict
from SMS_MYSQL.models import TeachingPlan
# Create your views here.

# 采用modelform

from django import forms


# from django.forms import DateInput
#
# class UDateInput(DateInput):
#     input_type = 'date'


def student_extra_list(request):
    """ 学生额外信息列表 """
    # data_dict = {}
    # s_id =request.GET.get('q', '')
    # if s_id:
    #     data_dict['student_id__contains'] = s_id
    #
    # # select  from Table order by level desc;
    # queryset = models.Students.objects.filter(**data_dict)

    # 绕过模型层采用原生SQL
    s_id = request.GET.get('s_id', '').strip()
    search_data = {
        's_id': s_id,
    }
    # ST1 查出学号所对应专业号
    ST1 = "select majors_id \
                        from sms_mysql_students A, sms_mysql_classes B \
                        where A.classes_id=B.class_id and A.student_id='%s' " % s_id

    # ST2 对应专业的授课计划
    ST2 = "select majors_id,courses_id,tp_type,tp_semester \
                    from sms_mysql_teachingplan \
                    where majors_id=( %s ) " % ST1

    # ST3 将授课计划与课程表、选课表连接, 并查出对应学号课程号的记录
    ST3 = "select students_id, A.courses_id, tp_type, tp_semester, B.course_credit, grade \
            from sms_mysql_studentcourse A, sms_mysql_courses B, ( %s ) C \
            where A.students_id='%s' and A.courses_id = B.course_id and A.courses_id=C.courses_id " % (ST2, s_id)

    # ST4 查询所有课程平均成绩 注意：成绩非空！
    ST4 = "select sum(B.course_credit * grade) / sum(B.course_credit) avg_grade_all\
                from sms_mysql_studentcourse A, sms_mysql_courses B, ( %s ) C \
                where A.students_id='%s' and A.courses_id = B.course_id and A.courses_id=C.courses_id and grade is not NULL " % (ST2, s_id)


    # ST5 查询必修课平均成绩 注意：成绩非空！
    ST5 = "select sum(B.course_credit * grade) / sum(B.course_credit) avg_grade_compulsory\
                    from sms_mysql_studentcourse A, sms_mysql_courses B, ( %s ) C \
                    where A.students_id='%s' and A.courses_id = B.course_id and A.courses_id=C.courses_id and C.tp_type=1 and grade is not NULL " % (
    ST2, s_id)

    #查询学生对应授课教师

    # 查出学号所对应的班级
    ST6 = "select classes_id \
            from sms_mysql_students \
            where student_id='%s' " % s_id

    # 查出班级对应的教学职责记录
    ST7 = "select * \
            from sms_mysql_teachingduty \
            where classes_id=( %s ) " % ST6

    # 将ST7 与选课表、教师表进行连接，并选出响应记录
    ST8 = "select distinct C.teacher_id, C.teacher_name \
                from sms_mysql_teachers C, sms_mysql_studentcourse D, ( %s ) E  \
                where C.teacher_id=E.teachers_id and E.courses_id = D.courses_id and D.students_id='%s' " % (ST7, s_id)


    #print(ST3)
    querydict = {}
    querydict_all_avg_grade = {}
    querydict_compulsory_avg_grade ={}
    querydict_student_teacher = {}
    if s_id:
        querydict = custom_sql_get_dict(ST3)
        for d in querydict:
            d['tp_type'] = TeachingPlan.type_choices[d['tp_type']][1]
            d['tp_semester'] = TeachingPlan.semester_choices[d['tp_semester']][1]

        querydict_all_avg_grade = custom_sql_get_dict(ST4)
        querydict_compulsory_avg_grade = custom_sql_get_dict(ST5)
        querydict_student_teacher = custom_sql_get_dict(ST8)

    # print(querydict)
    # print(querydict_all_avg_grade)
    # print(querydict_compulsory_avg_grade)
    # print(querydict_student_teacher)

    # # 查询结果一摸一样!
    # # queryset = models.Students.objects.all()
    # # print(queryset.values())
    return render(request, "student_extra_list.html",
                  {'queryset': querydict,
                   'search_data': search_data,
                   'qst': querydict_student_teacher,
                   'aga': querydict_all_avg_grade,
                   'agc': querydict_compulsory_avg_grade})
