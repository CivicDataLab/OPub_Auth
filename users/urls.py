from django.urls import path

from . import views

urlpatterns = [
    path("verify_user_token", views.verify_user_token, name="verify_user_token"),
    path("check_user", views.check_user, name="check_user"),
    path("check_user_access", views.check_user_access, name="check_user_access"),
    path("create_user_role", views.create_user_role, name="create_user_role"),
    path("get_users", views.get_users, name="get_users"),
    path("update_user_role", views.update_user_role, name="update_user_role"),
    path(
        "update_dataset_owner", views.update_dataset_owner, name="update_dataset_owner"
    ),
    path("get_user_count", views.get_user_count, name="get_user_count"),
    path("get_access_datasets", views.get_access_datasets, name="get_access_datasets"),
    path("get_sys_token", views.get_sys_token, name="get_sys_token"),
    path("get_user_info", views.get_user_info, name="get_user_info"),
    path("update_datasetreq", views.update_datasetreq, name="update_datasetreq"),
    path("get_org_requestor", views.get_org_requestor, name="get_org_requestor"),
]
