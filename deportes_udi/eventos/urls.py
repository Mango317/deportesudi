from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Página principal
    path('', views.home, name='home'),
    

    # Páginas de autenticación (login y registro)
    path('login/', views.login_view, name='login'),
    
    path('register/', views.register_view, name='register'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('eventos/', views.index, name='eventos'),

    path('eventos/crear/', views.crear_evento, name='crear_evento'),
    
    path('eventos/editar/<int:evento_id>/', views.editar_evento, name='editar_evento'),
    
    path('eventos/eliminar/<int:evento_id>/', views.eliminar_evento, name='eliminar_evento'),

    path('eventos/inscribirse/<int:evento_id>/', views.inscribirse, name='inscribirse'),

    path('mis-inscripciones/', views.mis_inscripciones, name='mis_inscripciones'),

    path('cancelar-inscripcion/<int:inscripcion_id>/', views.cancelar_inscripcion, name='cancelar_inscripcion'),

    path('perfil/', views.perfil_usuario, name='profile'),

    path('panel-admin-eventos/', views.panel_admin_eventos, name='panel_admin_eventos'),

    path('panel_admin/', views.panel_admin, name='panel_admin'),

    # URLs para la gestión de usuarios (admin)
    path('panel/usuarios/<int:user_id>/', views.detalle_usuario_admin, name='detalle_usuario_admin'),
    path('panel/usuarios/editar/<int:user_id>/', views.editar_usuario_admin, name='editar_usuario_admin'),
    path('panel/usuarios/eliminar/<int:user_id>/', views.eliminar_usuario_admin, name='eliminar_usuario_admin'),

]