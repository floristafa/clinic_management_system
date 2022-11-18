from django.urls import path
from clinic_api import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
router.register('profile', views.UserProfileViewSet)
router.register('clinic', views.ClinicViewSet)
router.register('patient', views.PatientViewSet)
router.register('appointment', views.AppointmentViewSet)
router.register('service', views.ServiceViewSet)
router.register('report', views.ReportViewSet)
router.register('position', views.PositionViewSet)
router.register('invoice', views.InvoiceViewSet)


urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('', include(router.urls)),
    path('login/', views.UserLoginApiView.as_view()),
]