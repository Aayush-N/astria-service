import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


class Department(models.Model):
    """
    Description: Stores the departments
    """
    name = models.CharField(max_length=50)

    def __str__(self):
    	return self.name


class Designation(models.Model):
    """
    Description: Stores Designations
    """
    text = models.CharField(max_length=50)

    def __str__(self):
    	return self.text

class Semester(models.Model):
    """
	Semester: Holds the semester and section value
	"""

    sem = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
    	return self.sem


class UserType(models.Model):
    """
	UserType: We consider every recipient of a feedback as a user, if feedback has to be given
	to a new user a new user type has to be created.
	"""

    name = models.CharField("Type of User", max_length=50)

    def __str__(self):
        return self.name
        

@python_2_unicode_compatible
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(default=True)
    year = models.CharField(max_length=50, null=True)
    highest_qualification = models.CharField(blank=True,null=True, max_length=25)
    date_of_joining = models.DateField(null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='form', null=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, related_name='form', null=True)
    held_designation_from = models.DateField(null=True)
    phone = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=150, null=True)
    teaching_experience = models.IntegerField(default=0)
    research_experience = models.IntegerField(default=0)
    industry_experience = models.IntegerField(default=0)
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE, null=True)

    elective = models.ManyToManyField("subject", null=True, blank=True)
    batch = models.CharField("Lab Batch", max_length=50, null=True, blank=True)
    sub_batch = models.CharField("Lab Sub Batch", max_length=50, null=True, blank=True)

    # Below Field denotes the designation of the user
    user_type = models.ManyToManyField("UserType")

    # If a user abonds the feedback, partially done becomes true then
    # the user is restricted from giving feedback.
    partially_done = models.BooleanField(default=False)
    done = models.BooleanField(default=False)

    def is_faculty(self):
        faculty = UserType.objects.get(name="Faculty")
        if faculty in self.user_type.all():
            return True
        return False

    def is_hod(self):
        hod = UserType.objects.get(name="Hod")
        if hod in self.user_type.all():
            return True
        return False

    def is_student(self):
        student = UserType.objects.get(name="Student")
        if student in self.user_type.all():
            return True
        else:
            return False

    def is_principal(self):
        principal = UserType.objects.get(name="Principal")
        if principal in self.user_type.all():
            return True
        else:
            return False

    def get_user_type(self):
        return self.user_type.all()

    def __str__(self):
        return self.username


class Subject(models.Model):
    """
	Subject: Holds details about each subject
	"""

    name = models.CharField("Subject Name", max_length=50)
    code = models.CharField("Subject Code", max_length=50)

    theory = models.BooleanField(default=True)
    elective = models.BooleanField(default=False)
    project = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name + "->" + self.code)


class Teaches(models.Model):
    """
	Teaches: Holds details about the subject that the teacher teaches.
	It links the Subject and the Teacher with the sem, sec and department that they are teaching.
	We are storing sem, sec, deaprtment of the student to get the name of the teacher by matching the
	details with the user table.

	Note: Even if one student studies an elective in another department under the other department teacher,
	a new row has to be added.
	"""

    teacher = models.ForeignKey("user", on_delete=models.CASCADE)
    subject = models.ForeignKey("subject", on_delete=models.CASCADE)

    sem = models.ForeignKey("Semester", on_delete=models.CASCADE)
    sec = models.CharField("Student's Section", max_length=50)
    department = models.ForeignKey("Department", on_delete=models.CASCADE)

    batch = models.CharField("Student's Batch", max_length=50, null=True, blank=True)
    sub_batch = models.CharField(
        "Student's sub batch", max_length=50, null=True, blank=True
    )
    ug = models.BooleanField(default=False)

    count = models.IntegerField("Student Count", default=0, null=True, blank=True)

    def __str__(self):
        return self.teacher.first_name + " -> " + self.subject.name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
