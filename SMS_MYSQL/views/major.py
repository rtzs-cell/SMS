from django.shortcuts import render, redirect

from SMS_MYSQL import models
from SMS_MYSQL.utils.bootstrap import BootStrapModelForm
from SMS_MYSQL.utils.form import MajorEditModelForm, MajorModelForm
# Create your views here.

# 采用modelform


def major_list(request):
    """ 专业列表 """
    data_dict = {}
    search_data =request.GET.get('q', '')
    if search_data:
        data_dict['major_id__contains'] = search_data

    # select  from Table order by level desc;
    queryset = models.Majors.objects.filter(**data_dict)

    return render(request, "major_list.html", {"queryset": queryset, "search_data": search_data})


def major_add(request):
    title = "添加专业信息"
    if request.method == "GET":
        form = MajorModelForm()
        return render(request, "change.html", {"form": form, "title": title})

    #POST收到
    form = MajorModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect("/major/list")
    else:
        return render(request, "change.html", {"form": form,"title": title})


def major_edit(request, nid):
    ''' 编辑 '''
    title = "编辑专业信息"
    row_object = models.Majors.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = MajorEditModelForm(instance=row_object)
        return render(request, 'change.html', {"form": form, "title": title})

    # POST

    form = MajorEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/major/list")

    return render(request, 'change.html', {'form': form, "title": title})


def major_delete(request, nid):
    models.Majors.objects.filter(id=nid).delete()
    return redirect("/major/list")

