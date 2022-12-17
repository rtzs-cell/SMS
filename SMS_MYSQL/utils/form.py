from django.core.exceptions import ValidationError
from django import forms

from SMS_MYSQL import models
from SMS_MYSQL.utils.bootstrap import BootStrapModelForm


class StudentModelForm(BootStrapModelForm):
    # 验证方式1：正则
    # mobile = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误！', ), ]
    # )
    class Meta:
        model = models.Students
        fields = "__all__"
        #exclude = ["level"]


    # 钩子方法 验证2
    def clean_student_id(self):
        txt_student_id = self.cleaned_data["student_id"]

        if len(txt_student_id) != 11:
            # 验证不通过
            raise ValidationError("格式错误！")

        exists_student_id = models.Students.objects.filter(student_id=txt_student_id).exists()
        if exists_student_id:
            raise ValidationError("学号已存在！")

        # pass
        return txt_student_id


class StudentEditModelForm(BootStrapModelForm):
    # 验证方式1：正则
    # mobile = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误！', ), ]
    # )
    # student_id = forms.CharField(
    #     label="学号",
    #     disabled=True,
    # )
    class Meta:
        model = models.Students
        fields = "__all__"
        #exclude = ["mobile"]



    # 钩子方法 验证2
    def clean_student_id(self):
        txt_student_id = self.cleaned_data["student_id"]

        if len(txt_student_id) != 11:
            # 验证不通过
            raise ValidationError("学号格式错误！")


        exists_student_id = models.Students.objects.exclude(id=self.instance.pk).filter(student_id=txt_student_id).exists()
        if exists_student_id:
            raise ValidationError("学号已存在！")
        # pass
        return txt_student_id


class ClassesModelForm(BootStrapModelForm):
    # 验证方式1：正则
    # mobile = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误！', ), ]
    # )
    class Meta:
        model = models.Classes
        fields = "__all__"
        #exclude = ["level"]


    # 钩子方法 验证2
    def clean_class_id(self):
        txt_class_id = self.cleaned_data["class_id"]

        if len(txt_class_id) != 8:
            # 验证不通过
            raise ValidationError("格式错误！")

        exists_class_id = models.Classes.objects.filter(class_id=txt_class_id).exists()
        if exists_class_id:
            raise ValidationError("学号已存在！")

        # pass
        return txt_class_id


class ClassesEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Classes
        fields = "__all__"

    # 钩子方法
    def clean_class_id(self):
        txt_class_id = self.cleaned_data["class_id"]

        if len(txt_class_id) != 8:
            # 验证不通过
            raise ValidationError("班号格式错误！")


        exists_class_id = models.Classes.objects.exclude(id=self.instance.pk).filter(class_id=txt_class_id).exists()
        if exists_class_id:
            raise ValidationError("班级号已存在！")
        # pass
        return txt_class_id


class CourseModelForm(BootStrapModelForm):
    # 验证方式1：正则
    # mobile = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误！', ), ]
    # )
    class Meta:
        model = models.Courses
        fields = "__all__"
        #exclude = ["level"]


    # 钩子方法 验证2
    def clean_course_id(self):
        txt_course_id = self.cleaned_data["course_id"]

        if len(txt_course_id) != 9:
            # 验证不通过
            raise ValidationError("格式错误！")

        exists_course_id = models.Courses.objects.filter(course_id=txt_course_id).exists()
        if exists_course_id:
            raise ValidationError("课程号已存在！")

        # pass
        return txt_course_id


class CourseEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Courses
        fields = "__all__"

    # 钩子方法
    def clean_course_id(self):
        txt_course_id = self.cleaned_data["course_id"]

        if len(txt_course_id) != 9:
            # 验证不通过
            raise ValidationError("课程号格式错误！")


        exists_course_id = models.Courses.objects.exclude(id=self.instance.pk).filter(course_id=txt_course_id).exists()
        if exists_course_id:
            raise ValidationError("课程号已存在！")
        # pass
        return txt_course_id


class MajorModelForm(BootStrapModelForm):
    class Meta:
        model = models.Majors
        fields = "__all__"

    # 钩子方法 验证
    def clean_major_id(self):
        txt_major_id = self.cleaned_data["major_id"]

        if len(txt_major_id) != 6:
            # 验证不通过
            raise ValidationError("专业号格式错误！")

        exists_major_id = models.Majors.objects.filter(major_id=txt_major_id).exists()
        if exists_major_id:
            raise ValidationError("专业号已存在！")

        # pass
        return txt_major_id


class MajorEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Majors
        fields = "__all__"

    # 钩子方法
    def clean_major_id(self):
        txt_major_id = self.cleaned_data["major_id"]

        if len(txt_major_id) != 6:
            # 验证不通过
            raise ValidationError("专业号格式错误！")


        exists_major_id = models.Majors.objects.exclude(id=self.instance.pk).filter(major_id=txt_major_id).exists()
        if exists_major_id:
            raise ValidationError("专业号已存在！")
        # pass
        return txt_major_id


class TeacherModelForm(BootStrapModelForm):
    class Meta:
        model = models.Teachers
        fields = "__all__"

    # 钩子方法 验证
    def clean_teacher_id(self):
        txt_teacher_id = self.cleaned_data["teacher_id"]

        if len(txt_teacher_id) != 4:
            # 验证不通过
            raise ValidationError("工号格式错误！")

        exists_teacher_id = models.Teachers.objects.filter(teacher_id=txt_teacher_id).exists()
        if exists_teacher_id:
            raise ValidationError("工号已存在！")

        # pass
        return txt_teacher_id


class TeacherEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Teachers
        fields = "__all__"

    # 钩子方法
    def clean_teacher_id(self):
        txt_teacher_id = self.cleaned_data["teacher_id"]

        if len(txt_teacher_id) != 4:
            # 验证不通过
            raise ValidationError("工号格式错误！")


        exists_teacher_id = models.Teachers.objects.exclude(id=self.instance.pk).filter(teacher_id=txt_teacher_id).exists()
        if exists_teacher_id:
            raise ValidationError("工号已存在！")
        # pass
        return txt_teacher_id


class TeachingPlanModelForm(BootStrapModelForm):
    class Meta:
        model = models.TeachingPlan
        fields = "__all__"

    # 钩子方法 验证


class TeachingPlanEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.TeachingPlan
        fields = "__all__"

    # 钩子方法


class TeachingDutyModelForm(BootStrapModelForm):
    class Meta:
        model = models.TeachingDuty
        fields = "__all__"

    # 钩子方法 验证


class TeachingDutyEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.TeachingDuty
        fields = "__all__"

    # 钩子方法


class StudentCourseModelForm(BootStrapModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["resit"].widget._empty_value = [1] #设置下拉列表默认值
        #self.fields["resit"].widget.attrs['disabled'] = True

    class Meta:
        model = models.StudentCourse
        fields = "__all__"
        exclude = ["resit"]
    # 钩子方法 验证


class StudentCourseEditModelForm(BootStrapModelForm):

    class Meta:
        model = models.StudentCourse
        fields = "__all__"
        exclude = ["students", 'courses']
