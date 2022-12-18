from django.shortcuts import render, redirect

from SMS_MYSQL import models
from SMS_MYSQL.utils import page
from SMS_MYSQL.utils.bootstrap import BootStrapModelForm
from SMS_MYSQL.utils.form import TeachingPlanEditModelForm, TeachingPlanModelForm
# Create your views here.

# 采用modelform


def teaching_plan_list(request):
    """ 教学计划列表 """
    data_dict = {}
    search_data =request.GET.get('q', '')
    if search_data:
        data_dict['majors__major_name__contains'] = search_data

    # select  from Table order by level desc;
    queryset = models.TeachingPlan.objects.filter(**data_dict).order_by("majors__major_name")
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
    return render(request, "teaching_plan_list.html", {"queryset": queryset[page_object.start:page_object.end], 'page_html': page_html, "search_data": search_data})


def teaching_plan_add(request):
    title = "添加教学计划"
    if request.method == "GET":
        form = TeachingPlanModelForm()
        return render(request, "change.html", {"form": form, "title": title})

    #POST收到
    form = TeachingPlanModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect("/teaching/plan/list")
    else:
        return render(request, "change.html", {"form": form, "title": title})


def teaching_plan_edit(request, nid):
    ''' 编辑 '''
    title = "编辑教学计划"
    row_object = models.TeachingPlan.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = TeachingPlanEditModelForm(instance=row_object)
        return render(request, 'change.html', {"form": form, "title": title})

    # POST

    form = TeachingPlanEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/teaching/plan/list")

    return render(request, 'change.html', {'form': form, "title": title})


def teaching_plan_delete(request, nid):
    models.TeachingPlan.objects.filter(id=nid).delete()
    return redirect("/teaching/plan/list")

