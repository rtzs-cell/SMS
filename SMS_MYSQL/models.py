from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Majors(models.Model):
    """专业表"""
    major_id = models.CharField(verbose_name="专业号", max_length=16, unique=True)
    major_name = models.CharField(verbose_name="专业名", max_length=32, unique=True)
    def __str__(self):
        return self.major_name

class Classes(models.Model):
    """班级表"""
    class_id = models.CharField(verbose_name="班号", max_length=16, unique=True)

    # 专业号关联专业表的专业号
    majors = models.ForeignKey(verbose_name="专业", to="Majors", to_field="major_id", on_delete=models.PROTECT)

    semester_choices = (
        (0, "大一上"),
        (1, "大一下"),
        (2, "大二上"),
        (3, "大二下"),
        (4, "大三上"),
        (5, "大三下"),
        (6, "大四上"),
        (7, "大四下"),
    )
    class_semester = models.SmallIntegerField(verbose_name="学期", choices=semester_choices, default=0)
    def __str__(self):
        return self.class_id

class Students(models.Model):
    """ 学生表 """
    student_id = models.CharField(verbose_name="学号", max_length=16, unique=True)
    student_name = models.CharField(verbose_name="姓名", max_length=16)
    gender_choices = (
        (0, "男"),
        (1, "女")
    )
    student_gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices, default=0)
    student_birthday = models.DateField(verbose_name="出生年月", null=True, blank=True)

    # 学生所关联的班级班号
    classes = models.ForeignKey(verbose_name="班级", to="Classes", to_field="class_id", null=True, blank=True,
                                on_delete=models.PROTECT)

    def __str__(self):
        return self.student_id


class Courses(models.Model):
    course_id = models.CharField(verbose_name="课程号", max_length=16, unique=True)
    course_name = models.CharField(verbose_name="课程名", max_length=32)
    course_credit = models.DecimalField(verbose_name="学分", max_digits=2, decimal_places=1, default=0)

    def __str__(self):
        return self.course_name

class Teachers(models.Model):
    """ 教师表 """
    teacher_id = models.CharField(verbose_name="工号", max_length=16, unique=True)
    teacher_name = models.CharField(verbose_name="姓名", max_length=16)
    gender_choices = (
        (0, "男"),
        (1, "女")
    )
    teacher_gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices, default=0)

    def __str__(self):
        return self.teacher_name


class TeachingPlan(models.Model):
    """专业授课计划表"""
    majors = models.ForeignKey(verbose_name="专业", to="Majors", to_field="major_id", on_delete=models.PROTECT)
    courses = models.ForeignKey(verbose_name="课程", to="Courses", to_field="course_id", on_delete=models.PROTECT)
    type_choices = (
        (0, "选修"),
        (1, "必修"),
    )
    tp_type = models.SmallIntegerField(verbose_name="课程性质", choices=type_choices, default=0)
    semester_choices = (
        (0, "大一上"),
        (1, "大一下"),
        (2, "大二上"),
        (3, "大二下"),
        (4, "大三上"),
        (5, "大三下"),
        (6, "大四上"),
        (7, "大四下"),
    )
    tp_semester = models.SmallIntegerField(verbose_name="学期", choices=semester_choices, default=0)

    class Meta:
        unique_together = [
            ('majors', 'courses'),
        ]


class StudentCourse(models.Model):
    """学生选课表"""
    students = models.ForeignKey(verbose_name="学生", to="Students", to_field="student_id", on_delete=models.PROTECT)
    courses = models.ForeignKey(verbose_name="课程", to="Courses", to_field="course_id", on_delete=models.PROTECT)
    resit_choices = (
        (0, "否"),
        (1, "是")
    )
    resit = models.SmallIntegerField(verbose_name="是否补考", choices=resit_choices, default=resit_choices[0][0])
    grade = models.SmallIntegerField(verbose_name="成绩", null=True, blank=True, default=None, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        unique_together = [
            ('students', 'courses')
        ]


class TeachingDuty(models.Model):
    """教师授课负责表"""
    classes = models.ForeignKey(verbose_name="班级", to="Classes", to_field="class_id", on_delete=models.PROTECT)
    courses = models.ForeignKey(verbose_name="课程", to="Courses", to_field="course_id", on_delete=models.PROTECT)
    teachers = models.ForeignKey(verbose_name="老师", to="Teachers", to_field="teacher_id", on_delete=models.PROTECT)

    class Meta:
        unique_together = [
            ('classes', 'courses')
        ]


class Admin(models.Model):
    """管理员"""
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
