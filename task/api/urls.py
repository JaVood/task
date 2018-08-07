from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from api import views


router = DefaultRouter()
router.register(r'groups', views.GroupViewSet)
router.register(r'elements', views.ElementViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^groups/(?P<pk>[0-9]+)/elements/$', views.elements_by_group),
    url(r'^groups/(?P<pk>[0-9]+)/groups/$', views.children_by_group),
]
