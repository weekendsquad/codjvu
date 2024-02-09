from django.urls import path
from .views import tag_list_public_view, tag_list_private_view, tag_update_view, tag_delete_view,\
    tag_view, snippet_view, snippet_list_view, snippet_delete_view, snippet_update_view, snippet_details_view

urlpatterns = [
    path('add/tag', tag_view, name='add_tag'),
    path('get/tag/public', tag_list_public_view, name='get_tag_public'),
    path('get/tag/private', tag_list_private_view, name='get_tag_private'),
    path('delete/tag', tag_delete_view, name='delete_tag'),
    path('update/tag', tag_update_view, name='update_tag'),

    path('add/snippet', snippet_view, name='add_snippet'),
    path('get/snippet/list',snippet_list_view , name='get_snippet'),
    path('get/snippet/<int:snippet_id>', snippet_details_view, name='snippet_detail'),
    path('delete/snippet', snippet_delete_view, name='delete_snippet'),
    path('update/snippet', snippet_update_view, name='snippet'),
]
