# Generated by Django 4.1.4 on 2022-12-15 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("SMS_MYSQL", "0003_studentcourse_teachers_delete_teacherschedule"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="studentcourse",
            name="teachers",
        ),
        migrations.CreateModel(
            name="TeacherSchedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "classes",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="SMS_MYSQL.classes",
                        to_field="class_id",
                        verbose_name="班级",
                    ),
                ),
                (
                    "courses",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="SMS_MYSQL.courses",
                        to_field="course_id",
                        verbose_name="课程",
                    ),
                ),
                (
                    "teachers",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="SMS_MYSQL.teachers",
                        to_field="teacher_id",
                        verbose_name="老师",
                    ),
                ),
            ],
            options={
                "unique_together": {("classes", "courses")},
            },
        ),
    ]