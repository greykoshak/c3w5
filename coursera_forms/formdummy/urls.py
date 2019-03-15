from django.urls import path

from . import views

# urlpatterns = [
#     path('', views.FormDummyView.as_view()),
# ]
# urlpatterns = [
#     path('', views.SchemaView.as_view()),
# ]

urlpatterns = [
    path('', views.MarshView.as_view()),
]