from django.urls import path
from .views import tag_list_view, tag_update_view, tag_delete_view,\
    tag_view, snippet_view, snippet_list_view, snippet_delete_view, snippet_update_view, snippet_details_view

urlpatterns = [
    path('tag/create', tag_view, name='add_tag'),
    path('tag/list', tag_list_view, name='get_tag'),
    path('tag/delete', tag_delete_view, name='delete_tag'),
    path('tag/update', tag_update_view, name='update_tag'),

    path('snippet/create', snippet_view, name='add_snippet'),
    path('snippet/list', snippet_list_view, name='get_snippet'),
    path('snippet/<int:snippet_id>', snippet_details_view, name='snippet_detail'),
    path('snippet/delete', snippet_delete_view, name='delete_snippet'),
    path('snippet/update', snippet_update_view, name='snippet'),
]
