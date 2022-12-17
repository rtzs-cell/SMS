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


def student_expel_list(request):
    """ 学生额外信息列表 """
    # 绕过模型层采用原生SQL

    # ST1 查出所有不及格选课信息的学号 课程号 学分
    ST1 = "select  A.students_id, A.courses_id, B.course_credit \
            from sms_mysql_studentcourse A, sms_mysql_courses B \
            where A.courses_id=B.course_id and A.grade<60 and A.grade is not NULL"
    # print(custom_sql_get_dict(ST1))
    # ST2 查出所有学号对应的专业号
    ST2 = "select  C.student_id, D.majors_id\
            from sms_mysql_students C, sms_mysql_classes D \
            where C.classes_id=D.class_id "
    #print(custom_sql_get_dict(ST2))
    # ST3 将ST1，ST2 与 授课计划连接 得到 不及格的必修课学号 总学分 总数
    ST3 = "select  E.students_id, sum(E.course_credit) sum_compulsory_credit, count(*) count_compulsory \
            from ( %s ) E, ( %s ) F, sms_mysql_teachingplan G \
            where G.tp_type=1 and E.students_id=F.student_id and E.courses_id=G.courses_id and F.majors_id=G.majors_id \
            group by E.students_id " % (ST1, ST2)
    #print(custom_sql_get_dict(ST3))
    # ST4 将ST1，ST2 与 授课计划连接 得到 不及格的选修课学号 总学分 总数
    ST4 = "select  H.students_id, sum(H.course_credit) sum_option_credit, count(*) count_option \
                from ( %s ) H, ( %s ) I, sms_mysql_teachingplan J \
                where J.tp_type=0 and H.students_id=I.student_id and H.courses_id=J.courses_id and I.majors_id=J.majors_id \
                group by H.students_id  " % (ST1, ST2)
    #print(custom_sql_get_dict(ST4))
    # ST5 将ST3和ST4连接得到结果
    ST5 = "select  K.students_id, K.sum_compulsory_credit, K.count_compulsory, L.sum_option_credit, L.count_option \
                    from ( %s ) K, ( %s ) L \
                    where K.students_id=L.students_id and (K.sum_compulsory_credit>=7 or L.sum_option_credit>=12)" % (ST3, ST4)


    #print(ST3)
    querydict = {}
    querydict = custom_sql_get_dict(ST5)
    #print(querydict)
    # # # 查询结果一摸一样!
    # # # queryset = models.Students.objects.all()
    # # # print(queryset.values())
    # return render(request, "student_extra_list.html",
    #               {'queryset': querydict,
    #                'search_data': search_data,
    #                'qst': querydict_student_teacher,
    #                'aga': querydict_all_avg_grade,
    #                'agc': querydict_compulsory_avg_grade})
    return render(request, "student_expel_list.html", {"queryset": querydict})
