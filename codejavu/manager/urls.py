from django.urls import path
from .views import language_view, language_list_view, language_update_view, language_delete_view, tag_list_view


urlpatterns = [
    path('add/language', language_view, name='add_language'),
    path('get/language', language_list_view, name='get_language'),
    path('delete/language', language_delete_view, name='delete_language'),
    path('update/language', language_update_view, name='update_language'),

    path('get/tag', tag_list_view, name='view_tag'),
]
