from django.urls import path

from .views import UpdateCSSFormView

urlpatterns = [
    path('update_css/<int:pk>/', UpdateCSSFormView.as_view(), name='update_css')
]
