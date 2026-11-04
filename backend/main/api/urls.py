from django.urls import path
from . import user_views,post_views,group_views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    
    path('auth/', obtain_auth_token),

    #user urls
    path("register/",user_views.UserRegisteringView.as_view(),name = "user-register"),
    path("profile/update/",user_views.ProfileUpdateView.as_view(),name = "user-update"),
    path("join_group/<int:group_id>/",user_views.JoinGroupView.as_view(),name = "group-join"),
    path("leave_group/<int:group_id>/",user_views.LeaveGroupView.as_view(),name = "group-leave"),
    path("user/follow/<int:user_being_followed_id>/<int:following>/",user_views.FollowAndUnFollowingViews.as_view(),name = "group-leave"),
    path("user/list/",user_views.ListUserView.as_view(),name = "user-list"),

    #post urls
    path("post/create/",post_views.createPostView2.as_view(), name="post-create"),
    path("post/delete/<int:post_id>/",post_views.DeletePostView.as_view(),name = "post-delete"),
    path("post/update/<int:post_id>/",post_views.UpdatePostView.as_view(),name = "post-update"),
    path("post/create/",post_views.createPostView2.as_view(), name="post-create"),
    path("post/list/",post_views.ListPostView.as_view(), name="post-list"),
    path("post/react/<int:post_id>/<int:like_post>/",post_views.LikeAndDislikeView.as_view(), name="post-list"),

    # Comment urls
    path("post/comment/<int:post_id>/",post_views.WriteCommentView.as_view(), name="comment-write"),


    #group urls
    path("group/create/", group_views.CreateGroupView.as_view(), name = "group-create"),
    path("group/delete/<int:group_id>/", group_views.DeleteGroupView.as_view(), name = "group-delete"),
    path("group/update/<int:group_id>/", group_views.UpdateGroupView.as_view(), name = "group-update"),
    path("group/list/", group_views.ListGroupsView.as_view(), name = "group-list"),
    path("group/add_members/<int:group_id>/<int:user_id>/", group_views.AddGroupMembersView.as_view(), name = "group-add_members"),
    path("group/add_admins/<int:group_id>/<int:user_id>/", group_views.AddGroupAdminView.as_view(), name = "group-add_admins"),
    path("group/remove_admins/<int:group_id>/<int:user_id>/", group_views.RemoveGroupAdminView.as_view(), name = "group-remove_admins"),
    path("group/remove_members/<int:group_id>/<int:user_id>/", group_views.RemoveGroupMemberView.as_view(), name = "group-remove_members"),

]


