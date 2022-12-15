from django.db import models


# Create your models here.

class Majors(models.Model):
    """专业表"""
    major_id = models.CharField(verbose_name="专业号", max_length=16, unique=True)
    major_name = models.CharField(verbose_name="专业名", max_length=32, unique=True)


class Classes(models.Model):
    """班级表"""
    class_id = models.CharField(verbose_name="班号", max_length=16, unique=True)

    # 专业号关联专业表的专业号
    majors = models.ForeignKey(verbose_name="专业", to="Majors", to_field="major_id", on_delete=models.PROTECT)

    semester_choices = (
        (1, "大一上"),
        (2, "大一下"),
        (3, "大二上"),
        (4, "大二下"),
        (5, "大三上"),
        (6, "大三下"),
        (7, "大四上"),
        (8, "大四下"),
    )
    class_semester = models.SmallIntegerField(verbose_name="学期", choices=semester_choices, default=1)


class Students(models.Model):
    """ 学生表 """
    student_id = models.CharField(verbose_name="学号", max_length=16, unique=True)
    student_name = models.CharField(verbose_name="姓名", max_length=16)
    gender_choices = (
        (1, "男"),
        (2, "女")
    )
    student_gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    student_age = models.IntegerField(verbose_name="年龄")
    student_birthday = models.DateField(verbose_name="出生年月")

    # 学生所关联的班级班号
    classes = models.ForeignKey(verbose_name="班级", to="Classes", to_field="class_id", null=True, blank=True,
                                on_delete=models.PROTECT)


class Courses(models.Model):
    course_id = models.CharField(verbose_name="课程号", max_length=16, unique=True)
    course_name = models.CharField(verbose_name="课程名", max_length=32)
    course_credit = models.DecimalField(verbose_name="学分", max_digits=2, decimal_places=1, default=0)


class Teachers(models.Model):
    """ 教师表 """
    teacher_id = models.CharField(verbose_name="工号", max_length=16, unique=True)
    teacher_name = models.CharField(verbose_name="姓名", max_length=16)
    teacher_age = models.IntegerField(verbose_name="年龄")
    gender_choices = (
        (1, "男"),
        (2, "女")
    )
    teacher_gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class TeachingPlan(models.Model):
    """专业授课计划表"""
    majors = models.ForeignKey(verbose_name="专业", to="Majors", to_field="major_id", on_delete=models.PROTECT)
    courses = models.ForeignKey(verbose_name="课程", to="Courses", to_field="course_id", on_delete=models.PROTECT)
    tp_choices = (
        (1, "必修"),
        (2, "选修"),
    )
    tp_type = models.SmallIntegerField(verbose_name="课程性质", choices=tp_choices)
    semester_choices = (
        (1, "大一上"),
        (2, "大一下"),
        (3, "大二上"),
        (4, "大二下"),
        (5, "大三上"),
        (6, "大三下"),
        (7, "大四上"),
        (8, "大四下"),
    )
    tp_semester = models.SmallIntegerField(verbose_name="学期", choices=semester_choices)

    class Meta:
        unique_together = [
            ('majors', 'courses'),
        ]


class StudentCourse(models.Model):
    """学生选课表"""
    students = models.ForeignKey(verbose_name="学生", to="Students", to_field="student_id", on_delete=models.PROTECT)
    courses = models.ForeignKey(verbose_name="课程", to="Courses", to_field="course_id", on_delete=models.PROTECT)
    resit_choices = (
        (1, "是"),
        (0, "否")
    )
    resit = models.SmallIntegerField(verbose_name="是否补考", choices=resit_choices)

    class Meta:
        unique_together = [
            ('students', 'courses')
        ]


class TeacherSchedule(models.Model):
    """教师授课负责表"""
    teachers = models.ForeignKey(verbose_name="老师", to="Teachers", to_field="teacher_id", on_delete=models.PROTECT)
    classes = models.ForeignKey(verbose_name="班级", to="Classes", to_field="class_id", on_delete=models.PROTECT)
    courses = models.ForeignKey(verbose_name="课程", to="Courses", to_field="course_id", on_delete=models.PROTECT)

    class Meta:
        unique_together = [
            ('teachers', 'classes')
        ]

