from django.shortcuts import redirect, render
from app.models import Course, Categories, Level, Video, UserCourse, Payment, Review
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from random import randint
import random


def base(request):
    return render(request, 'base.html')


def home(request):
    course = Course.objects.filter(status='PUBLISH').order_by('-id')[0:3]

    context = {'course': course}

    return render(request, 'main/home.html', context)


def info(request):
    return render(request, 'main/info.html')


def courses(request):
    category = Categories.get_all_category(Categories)
    level = Level.objects.all()
    course = Course.objects.all()
    freeCourse_count = Course.objects.filter(price=0).count()
    paidCourse_count = Course.objects.filter(price__gte=1).count()

    context = {'category': category, 'level': level, 'course': course, 'freeCourse_count': freeCourse_count, 'paidCourse_count': paidCourse_count}

    return render(request, 'main/courses.html', context)


def filter_data(request):
    categories = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')

    if price == ['PriceFree']:
        course = Course.objects.filter(price=0)
    elif price == ['PricePaid']:
        course = Course.objects.filter(price__gte=1)
    elif price == ['PriceAll']:
        course = Course.objects.all()
    elif categories:
        course = Course.objects.filter(category__id__in=categories).order_by('-id')
    elif level:
        course = Course.objects.filter(level__id__in=level).order_by('-id')
    else:
        course = Course.objects.all().order_by('id')

    t = render_to_string('ajax/course.html', {'course': course})

    return JsonResponse({'data': t})


def search_course(request):
    category = Categories.get_all_category(Categories)
    query = request.GET['query']
    course = Course.objects.filter(title__icontains=query)

    context = {
        'course': course,
        'category': category,
    }

    return render(request, 'search/search.html', context)


def course_details(request, slug):
    course_id = Course.objects.get(slug=slug)
    course = Course.objects.filter(slug=slug)
    time_duration = Video.objects.filter(course__slug=slug).aggregate(sum=Sum('time_duration'))
    messages = ''

    try:
        check_enroll = UserCourse.objects.get(user=request.user, course=course_id)
    except UserCourse.DoesNotExist:
        check_enroll = None

    if course.exists():
        course = course.first()
    else:
        return redirect('404')

    if request.method == "POST":
        name = request.POST.get('name')
        course_name = request.POST.get('course_name')
        review_course = request.POST.get('review_course')

        review = Review(
            name=name,
            course_name=course_name,
            review_course=review_course,
        )
        review.save()
        messages = 'Thank you for your review!'

    context = {
        'course': course,
        'time_duration': time_duration,
        'check_enroll': check_enroll,
        'messages': messages
    }

    return render(request, 'course/course_details.html', context)


def page_not_found(request):
    return render(request, 'error/404.html')


def checkout(request, slug):
    course = Course.objects.get(slug=slug)
    action = request.GET.get('action')

    if course.price == 0:
        course = UserCourse(
            user=request.user,
            course=course,
        )
        course.save()
        messages.success(request, 'Course Successfully Enrolled!')
        return redirect('my_course')

    elif action == 'create_payment':
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            university_name = request.POST.get('university_name')
            country = request.POST.get('country')
            city = request.POST.get('city')
            address_1 = request.POST.get('address_1')
            address_2 = request.POST.get('address_2')
            postcode = request.POST.get('postcode')
            phone = request.POST.get('phone')
            email = request.POST.get('email')

        pin = randint(10**(4-1), (10**4)-1)

        order_id = random.randrange(10000000, 99999999, 8)

        while True:
            check_order_id = Payment.objects.filter(order_id=order_id)

            if check_order_id:
                order_id = random.randrange(10000000, 99999999, 8)
            else:
                break

        payment = Payment(
            order_id=order_id,
            course=course,
            user=request.user,
            name=first_name.capitalize() + " " + last_name.capitalize(),
            university_name=university_name,
            country=country,
            city=city,
            address_1=address_1,
            address_2=address_2,
            postcode=postcode,
            phone=phone,
        )
        payment.save()

        return redirect('verify_payment', slug=course.slug, pk=payment.order_id, pin=pin)

    context = {
        'course': course
    }

    return render(request, 'checkout/checkout.html', context)


@csrf_exempt
def verify_payment(request, slug, pin, pk):
    course = Course.objects.get(slug=slug)
    payment = Payment.objects.get(order_id=pk)
    pin = pin

    if request.method == 'POST':
        pin_number = int(request.POST.get('pin_number'))

        if pin == pin_number:
            payment.payment_id = get_random_string(10, 'abcdef0123456789')
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            payment.user_course = user_course
            payment.save()
            return redirect('success', slug=course.slug, pk=payment.order_id)
        else:
            Payment.objects.filter(order_id=pk).delete()
            return redirect('failed')

    context = {
        'course': course,
        'payment': payment,
        'pin': pin
    }

    return render(request, 'checkout/verify_payment.html', context)


def success(request, slug, pk):
    course = Course.objects.get(slug=slug)
    payment = Payment.objects.get(order_id=pk)

    context = {
        'course': course,
        'payment': payment,
    }

    return render(request, 'checkout/success.html', context)


def failed(request):
    return render(request, 'checkout/failed.html')


def my_course(request):
    course = UserCourse.objects.filter(user=request.user)

    context = {
        'course': course
    }
    return render(request, 'course/my-course.html', context)
