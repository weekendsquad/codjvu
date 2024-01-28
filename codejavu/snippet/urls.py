from django.urls import path
from .views import tag_list_view, \
    tag_update_view, tag_delete_view, tag_view


urlpatterns = [
    path('add/tag', tag_view, name='add_tag'),
    path('get/tag', tag_list_view, name='get_tag'),
    path('delete/tag', tag_delete_view, name='delete_tag'),
    path('update/tag', tag_update_view, name='update_tag'),
]
