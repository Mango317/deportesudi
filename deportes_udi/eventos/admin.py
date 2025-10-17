from django.contrib import admin
from .models import Evento, Inscripcion
from django.contrib.admin.sites import AdminSite

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'hora', 'lugar', 'creador')
    search_fields = ('nombre', 'lugar', 'creador__username')
    list_filter = ('fecha',)

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'fecha_inscripcion')
    search_fields = ('usuario__username', 'evento__nombre')
    list_filter = ('fecha_inscripcion',)

# =====================================================
# Personalización del panel de administración
# =====================================================
class MyAdminSite(admin.AdminSite):
    site_header = "Panel de Administración - Deportes UDI"
    site_title = "Administración Deportes UDI"
    index_title = "Bienvenido al panel de control de Deportes UDI"

    class Media:
        css = {
            'all': ('admin/css/custom.css',)
        }

# Instancia del nuevo sitio
custom_admin_site = MyAdminSite(name='custom_admin')

# =====================================================
# Registro de modelos en el nuevo admin
# =====================================================
@admin.register(Evento, site=custom_admin_site)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'hora', 'lugar', 'creador')
    search_fields = ('nombre', 'lugar', 'creador__username')
    list_filter = ('fecha',)

@admin.register(Inscripcion, site=custom_admin_site)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'fecha_inscripcion')
    search_fields = ('usuario__username', 'evento__nombre')
    list_filter = ('fecha_inscripcion',)