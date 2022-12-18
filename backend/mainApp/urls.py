from django.urls import path
from .views import localSchemaAPI, globalSchemaAPI , makeConnection


urlpatterns = [
    # path('', views.hello),
    path('LocalSchema', localSchemaAPI.as_view()),
    path('GlobalSchema', globalSchemaAPI.as_view()),
    path('GlobalSchema/Connection', makeConnection),
    
]
