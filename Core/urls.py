from django.urls import path
from . import views
app_name = "Core"
urlpatterns = [
    path('', views.Login.as_view(), name = "login"),
    path('Trangchu/', views.WelcomeClass.as_view(), name='Welcome'),
    path('Chonbienso/', views.chonbienso.as_view(), name = "chonbienso"),
    path('nhandienHinhAnh/', views.nhandienHinhAnh, name = "nhandienHinhAnh"),
    path('nhandienAnh/', views.nhandienAnh, name = "nhandienanh"),
    path('detect_webbycamera/', views.DetectCamera.as_view(), name="detect_webbycamera"),
    path('postajax/', views.postFriend, name = "post_friend"),
    path('Taikhoan/', views.TaiKhoan.as_view(), name = "taikhoan"),
    path('Giaxe/', views.GiaXe.as_view(), name = "giaxe"),
    path('save_loaixe/', views.save_loaixe, name = "save_loaixe"),
    path('xoa_loaixe/id=', views.xoa_loaixe, name = "xoa_loaixe"),
    path('save_time/', views.save_time, name = "save_time"),
    path('save_giaxe/', views.save_giaxe, name = "save_giaxe"),
    path('nhandienbienso/', views.NhanDienBienSo.as_view(), name = "nhandienbienso"),
    path('batcamera/', views.BatCameRa, name = "batcamera"),
    path('traxe/', views.TraXe, name = "traxe"),
    path('dangkyxethang/', views.dangkyxethang.as_view(), name = "dangkyxethang"),
]

