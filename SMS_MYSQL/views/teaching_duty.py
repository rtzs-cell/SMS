from django.shortcuts import render, redirect

from SMS_MYSQL import models
from SMS_MYSQL.utils import page
from SMS_MYSQL.utils.bootstrap import BootStrapModelForm
from SMS_MYSQL.utils.form import TeachingDutyEditModelForm, TeachingDutyModelForm
# Create your views here.

# 采用modelform


def teaching_duty_list(request):
    """ 授课职责列表 """
    data_dict = {}
    search_data = ''
    search_data =request.GET.get('q', '')
    if search_data:
        data_dict['teachers__teacher_name__contains'] = search_data

    # select  from Table order by level desc;
    queryset = models.TeachingDuty.objects.filter(**data_dict).order_by("teachers__teacher_name")
    # 分页
    current_page = request.GET.get('page')
    page_object = page.Pagination(current_page=current_page,
                                  all_count=queryset.count(),
                                  base_url=request.path_info,
                                  query_params=request.GET,
                                  per_page=10,
                                  )
    page_html = page_object.page_html()
    # "queryset": queryset[page_object.start:page_object.end], 'page_html': page_html,
    return render(request, "teaching_duty_list.html", {"queryset": queryset[page_object.start:page_object.end], 'page_html': page_html, "search_data": search_data})


def teaching_duty_add(request):
    title = "添加授课职责"
    if request.method == "GET":
        form = TeachingDutyModelForm()
        return render(request, "change.html", {"form": form, "title": title})

    #POST收到
    form = TeachingDutyModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect("/teaching/duty/list")
    else:
        return render(request, "change.html", {"form": form, "title": title})


def teaching_duty_edit(request, nid):
    ''' 编辑 '''
    title = "编辑教学计划"
    row_object = models.TeachingDuty.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = TeachingDutyEditModelForm(instance=row_object)
        return render(request, 'change.html', {"form": form, "title": title})

    # POST

    form = TeachingDutyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/teaching/duty/list")

    return render(request, 'change.html', {'form': form, "title": title})


def teaching_duty_delete(request, nid):
    models.TeachingDuty.objects.filter(id=nid).delete()
    return redirect("/teaching/duty/list")

