from django.conf.urls import url,include
from . import views

urlpatterns =[
 url(r'^HouseData/$',views.viewHouseholds, name = 'households'),
 url(r'^crop/$',views.CropsDistribution, name = 'CropsDistribution')
]
