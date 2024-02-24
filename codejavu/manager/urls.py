from django.urls import path
from .views import language_view, tag_list_view, setting_tag_limit_view

urlpatterns = [
    path('language', language_view, name='language'),

    path('tag-all', tag_list_view, name='view_tag'),

    path('setting/tag-limit', setting_tag_limit_view, name='tag_limit_setting'),
]
