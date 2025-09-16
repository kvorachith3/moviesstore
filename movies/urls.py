from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='movies.index'),
    path('<int:id>/', views.show, name='movies.show'),
    path('<int:id>/review/create/', views.create_review,name='movies.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='movies.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='movies.delete_review'),
    path("movies/hidden/", views.HiddenMoviesView.as_view(), name="hidden_movies"),
    path("movies/<int:pk>/hide/", views.hide_movie, name="hide_movie"),
    path("movies/<int:pk>/unhide/", views.unhide_movie, name="unhide_movie"),
]