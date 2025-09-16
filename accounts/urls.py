from django.urls import path
from accounts.views import AdminDashboardView, organizer_dashboard, participant_dashboard, activation, create_role,edit_user,delete_user  ,add_user,dashboard_redirect,ProfileView,settings_view ,EditProfileView,CustomPasswordChangeView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('accounts/admin/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('accounts/organizer/dashboard/', organizer_dashboard, name='organizer_dashboard'),
    path('accounts/participant/dashboard/', participant_dashboard, name='participant_dashboard'),
    path('activate/<int:user_id>/<str:token>/', activation, name='activation'),
    path('accounts/admin/create-role/', create_role, name='create_role'),
    path('accounts/admin/add-user/', add_user, name='add_user'),
    path('accounts/admin/edit-user/<int:user_id>/', edit_user, name='edit_user'),
    path('accounts/admin/delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path('dashboard/', dashboard_redirect, name='dashboard_redirect'),
    path('password/change/<int:user_id>/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('accounts/profile/', ProfileView.as_view(), name='profile_view'),
    path('accounts/settings/', settings_view, name='settings_view'),
    path('accounts/profile/edit/<int:user_id>/', EditProfileView.as_view(), name='edit_profile'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    

]
