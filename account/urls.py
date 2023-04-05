from django.urls import path,include
from rest_framework import routers
from . import views 

from account.views import(
    forgot_password,
    registration_view,
    account_properties_view,
    update_account_view,
    does_account_exist_view,
    ChangePasswordView,
    login_view,
    logout_view,
    profile_view,
)
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'account'


router = routers.DefaultRouter()



urlpatterns = [
    path('check_if_account_exists/', does_account_exist_view, name="check_if_account_exists"),
    path('change_password/', ChangePasswordView.as_view(), name="change_password"),
    path('forgot_password/', forgot_password, name="forgot_password"),
    path('properties/', account_properties_view, name="properties"),
    path('properties/update/', update_account_view, name="update"),
    path('login/', login_view, name="login"), 
    path('logout/', logout_view, name="logout"), 
    path('profile/', profile_view, name="profile"), 
    path('register/', registration_view, name="register"),

    


]

urlpatterns += router.urls
