from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.urls import reverse

# Create your models here.


class Categories(models.Model):
    icon = models.ImageField(upload_to="Media/featured_img", null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_all_category(self):
        return Categories.objects.all().order_by('id')


class Level(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Language(models.Model):
    language = models.CharField(max_length=100)

    def __str__(self):
        return self.language


class Instructor(models.Model):
    instructor_profile = models.ImageField(upload_to="Media/instructor")
    name = models.CharField(max_length=100, null=True)
    instructor_title = models.CharField(max_length=100, null=True)
    about_instructor = models.TextField()

    def __str__(self):
        return self.name


class Course(models.Model):
    STATUS = (
        ('PUBLISH', 'PUBLISH'),
        ('DRAFT', 'DRAFT'),
    )

    featured_image = models.ImageField(upload_to="Media/featured_img", null=True)
    featured_video = models.CharField(max_length=300, null=True)
    title = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    semi_des = models.CharField(max_length=500, null=True)
    price = models.IntegerField(null=True, default=0)
    discount = models.IntegerField(null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    deadline = models.CharField(max_length=100, null=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=100, null=True)
    certificate = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("course_details", kwargs={'slug': self.slug})


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Course.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Course)


class What_you_learn(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=500)

    def __str__(self):
        return self.points


class Requirements(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=500)

    def __str__(self):
        return self.points


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name + " - " + self.course.title


class Video(models.Model):
    serial_number = models.IntegerField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    youtube_id = models.CharField(max_length=200)
    time_duration = models.IntegerField(null=True)
    preview = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    paid = models.BooleanField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name + " - " + self.course.title


class Payment(models.Model):
    order_id = models.CharField(max_length=100, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    user_course = models.ForeignKey(UserCourse, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    university_name = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address_1 = models.CharField(max_length=150, null=True, blank=True)
    address_2 = models.CharField(max_length=150, null=True, blank=True)
    postcode = models.CharField(max_length=4, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + " -- " + self.course.title


class Review(models.Model):
    name = models.CharField(max_length=100, null=True)
    course_name = models.CharField(max_length=200, null=True)
    review_course = models.TextField(max_length=1000, null=True)

    def __str__(self):
        return self.name + " reviews " + self.course_name