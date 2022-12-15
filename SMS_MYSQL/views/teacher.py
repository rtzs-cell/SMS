from django.shortcuts import render, redirect

from SMS_MYSQL import models
from SMS_MYSQL.utils.bootstrap import BootStrapModelForm
from SMS_MYSQL.utils.form import TeacherEditModelForm, TeacherModelForm
# Create your views here.

# 采用modelform


def teacher_list(request):
    """ 教师列表 """
    data_dict = {}
    search_data =request.GET.get('q', '')
    if search_data:
        data_dict['teacher_id__contains'] = search_data

    # select  from Table order by level desc;
    queryset = models.Teachers.objects.filter(**data_dict)

    return render(request, "teacher_list.html", {"queryset": queryset, "search_data": search_data})


def teacher_add(request):
    title = "添加教师信息"
    if request.method == "GET":
        form = TeacherModelForm()
        return render(request, "change.html", {"form": form, "title": title})

    #POST收到
    form = TeacherModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect("/teacher/list")
    else:
        return render(request, "change.html", {"form": form,"title": title})


def teacher_edit(request, nid):
    ''' 编辑 '''
    title = "编辑教师信息"
    row_object = models.Teachers.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = TeacherEditModelForm(instance=row_object)
        return render(request, 'change.html', {"form": form, "title": title})

    # POST

    form = TeacherEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/teacher/list")

    return render(request, 'change.html', {'form': form, "title": title})


def teacher_delete(request, nid):
    models.Teachers.objects.filter(id=nid).delete()
    return redirect("/teacher/list")

