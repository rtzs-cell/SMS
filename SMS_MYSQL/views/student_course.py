from django.shortcuts import render, redirect

from SMS_MYSQL import models
from SMS_MYSQL.utils.bootstrap import BootStrapModelForm
from SMS_MYSQL.utils.form import StudentCourseEditModelForm, StudentCourseModelForm
from SMS_MYSQL.utils.raw import custom_sql_get_dict
from SMS_MYSQL.models import StudentCourse
# Create your views here.

# 采用modelform


def student_course_list(request):
    """ 选课 列表 """
    # data_dict = {}
    # search_data =request.GET.get('q', '')
    # if search_data:
    #     data_dict['students_id__contains'] = search_data
    #
    # # select  from Table order by level desc;
    # queryset = models.StudentCourse.objects.filter(**data_dict)
    s_id = request.GET.get('s_id', '').strip()
    c_id = request.GET.get('c_id', '').strip()
    search_data = {
        's_id': s_id,
        'c_id': c_id
    }
    ALL = "select * \
            from sms_mysql_studentcourse \
            where 1=1"
    sql_cmd = ALL
    if s_id:
        sql_cmd = sql_cmd + " and students_id = '%s' " % s_id

    if c_id:
        sql_cmd = sql_cmd + " and courses_id = '%s' " % c_id

    querydict = custom_sql_get_dict(sql_cmd)
    # print(sql_cmd)

    for d in querydict:
        # print(d)
        d['resit'] = StudentCourse.resit_choices[d['resit']][1]
    # print(querydict)

    # 查询结果一摸一样!
    # queryset = models.Students.objects.all()
    # print(queryset.values())
    return render(request, "student_course_list.html", {"queryset": querydict, "search_data": search_data})



def student_course_add(request):
    title = "添加选课信息"
    if request.method == "GET":
        form = StudentCourseModelForm()
        return render(request, "change.html", {"form": form, "title": title})

    #POST收到
    form = StudentCourseModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect("/student/course/list/")
    else:
        return render(request, "change.html", {"form": form,"title": title})


def student_course_edit(request, nid):
    ''' 编辑 '''
    title = "编辑选课信息==>"
    row_object = models.StudentCourse.objects.filter(id=nid).first()
    edit_info = row_object.students.student_id + '--' + row_object.courses.course_id
    title = title + edit_info
    if request.method == 'GET':
        form = StudentCourseEditModelForm(instance=row_object)
        return render(request, 'change.html', {"form": form, "title": title})

    # POST

    form = StudentCourseEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/student/course/list/")

    return render(request, 'change.html', {'form': form, "title": title})


def student_course_delete(request, nid):
    models.StudentCourse.objects.filter(id=nid).delete()
    return redirect("/student/course/list/")

