from django.contrib import admin
from django.urls import path, include
from .import views, user_login
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('404', views.page_not_found, name='404'),
    path('base', views.base, name='base'),
    path('', views.home, name='home'),
    path('info', views.info, name='info'),
    path('courses', views.courses, name='courses'),
    path('courses/filter-data', views.filter_data, name="filter-data"),
    path('search', views.search_course, name='search_course'),
    path('course/<slug:slug>', views.course_details, name="course_details"),
    path('checkout/<slug:slug>', views.checkout, name='checkout'),
    path('my-course', views.my_course, name='my_course'),
    path('verify-payment/<slug:slug>/<int:pin>/<int:pk>', views.verify_payment, name='verify_payment'),
    path('verify-payment/success/<slug:slug>/<int:pk>', views.success, name='success'),
    path('verify-payment/failed', views.failed, name='failed'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', user_login.register, name='register'),
    path('doLogin', user_login.doLogin, name='doLogin'),
    path('accounts/profile', user_login.profile, name='profile'),
    path('accounts/profile/update', user_login.profile_update, name='profile_update'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)