from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import SpamMessageViewSet, SpamURLViewSet, SpamPhoneNumberViewSet

router = DefaultRouter()
router.register(r'spam-messages', SpamMessageViewSet)
router.register(r'spam-urls', SpamURLViewSet)
router.register(r'spam-phone-numbers', SpamPhoneNumberViewSet)

urlpatterns = [
    # Your custom views
    path('', views.home, name='home'),
    path('message/', views.predict_message, name='predict_message'),
    path('predict_url/', views.predict_url, name='predict_url'),
    path('phone/', views.check_number, name='check_number'),
    path('graph/', views.graph, name='cybercrime_graph'),
    path('report_spam/', views.report_spam, name='report_spam'),

    # REST API endpoints
    path('api/', include(router.urls)),
]
