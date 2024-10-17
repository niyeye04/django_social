from django.urls import path
from . import user_views,post_views,group_views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    #user urls
    path('auth/', obtain_auth_token),
    path("register/",user_views.UserRegisteringView.as_view(),name = "user-register"),
    path("profile/update/",user_views.ProfileUpdateView.as_view(),name = "user-update"),
    path("join_group/<int:group_id>/",user_views.JoinGroupView.as_view(),name = "group-join"),

    #post urls
    path("post/create/",post_views.createPostView2.as_view(), name="post-create"),
    path("post/delete/<int:post_id>/",post_views.DeletePostView.as_view(),name = "post-delete"),
    path("post/update/<int:post_id>/",post_views.UpdatePostView.as_view(),name = "post-update"),

    #group urls
    path("group/create/", group_views.CreateGroupView.as_view(), name = "group-create"),
    path("group/delete/<int:group_id>/", group_views.DeleteGroupView.as_view(), name = "group-delete"),
    path("group/update/<int:group_id>/", group_views.UpdateGroupView.as_view(), name = "group-update"),
    path("group/list/", group_views.ListGroupsView.as_view(), name = "group-list"),
]
