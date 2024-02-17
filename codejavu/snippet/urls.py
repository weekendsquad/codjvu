from django.urls import path
from .views import tag_view, snippet_view

urlpatterns = [
    path('tag', tag_view, name='tag'),
    path('snippet/<int:snippet_id>', snippet_view, name='snippet'),
    path('snippet', snippet_view, name='snippet'),
]
