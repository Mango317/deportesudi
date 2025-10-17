from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Evento, Inscripcion
from django.contrib import messages
from django.db.models import Count


# Página de inicio
def home(request):
    return render(request, 'eventos/home.html')

# Página de lista de eventos

@login_required
def index(request):
    eventos = Evento.objects.all()
    inscripciones_usuario = Inscripcion.objects.filter(usuario=request.user).values_list('evento_id', flat=True)

    context = {
        'eventos': eventos,
        'inscripciones_usuario': inscripciones_usuario
    }
    return render(request, 'eventos/index.html', context)

# Detalle de un evento
def detalle_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    return render(request, 'eventos/detalle_evento.html', {'evento': evento})

# Vista de Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'eventos/registracion/login.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'eventos/registracion/login.html')


# Vista de Registro
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'eventos/register.html', {'error': 'El usuario ya existe'})

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('home')

    return render(request, 'eventos/register.html')


@login_required
def dashboard(request):
    if request.user.is_superuser or request.user.is_staff:
        eventos = Evento.objects.annotate(num_inscripciones=Count('inscripcion')).all()
        inscripciones = Inscripcion.objects.all()
        usuarios = User.objects.all()
        total_usuarios = User.objects.count()
        total_eventos = Evento.objects.count()
        total_inscripciones = Inscripcion.objects.count()

        context = {
            'eventos': eventos,
            'inscripciones': inscripciones,
            'usuarios': usuarios,
            'total_usuarios': total_usuarios,
            'total_eventos': total_eventos,
            'total_inscripciones': total_inscripciones,
        }
        return render(request, 'eventos/dashboard_admin.html', context)
    return render(request, 'eventos/dashboard.html')

@login_required
def crear_evento(request):
    from .models import Evento
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        deporte = request.POST.get('deporte')
        lugar = request.POST.get('lugar')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        cupos = request.POST.get('cupos')
        nivel = request.POST.get('nivel')
        observaciones = request.POST.get('observaciones')

        Evento.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            deporte=deporte,
            lugar=lugar,
            fecha=fecha,
            hora=hora,
            cupos=cupos,
            nivel=nivel,
            observaciones=observaciones,
            creador=request.user
        )
        return redirect('eventos')

    return render(request, 'eventos/crear_evento.html', {
        'deportes': Evento.DEPORTES,
        'niveles': Evento.NIVELES,
    })

@login_required
def inscribirse(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    ya_inscrito = Inscripcion.objects.filter(usuario=request.user, evento=evento).exists()

    if not ya_inscrito:
        Inscripcion.objects.create(usuario=request.user, evento=evento)

    return redirect('eventos')
# =====================================================
@login_required
def mis_inscripciones(request):
    inscripciones = Inscripcion.objects.filter(usuario=request.user).select_related('evento')

    context = {
        'inscripciones': inscripciones
    }
    return render(request, 'eventos/mis_inscripciones.html', context)
# =====================================================
@login_required
def cancelar_inscripcion(request, inscripcion_id):
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id, usuario=request.user)
    inscripcion.delete()
    messages.success(request, "Te has dado de baja del evento exitosamente.")
    return redirect('mis_inscripciones')
# =====================================================

@login_required
def perfil_usuario(request):
    return render(request, 'eventos/perfil.html', {'usuario': request.user})

@login_required
def panel_admin_eventos(request):
    """Vista del panel para listar todos los eventos (solo admin/staff)."""
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')

    eventos = Evento.objects.all().order_by('-fecha')
    return render(request, 'eventos/panel_admin_eventos.html', {'eventos': eventos})


@login_required
def editar_evento(request, evento_id):
    """Permite editar un evento existente."""
    if not request.user.is_staff:
        messages.error(request, "No tienes permiso para editar eventos.")
        return redirect('home')

    evento = get_object_or_404(Evento, id=evento_id)

    if request.method == 'POST':
        evento.nombre = request.POST.get('nombre')
        evento.descripcion = request.POST.get('descripcion')
        evento.deporte = request.POST.get('deporte')
        evento.lugar = request.POST.get('lugar')
        evento.fecha = request.POST.get('fecha')
        evento.hora = request.POST.get('hora')
        evento.cupos = request.POST.get('cupos')
        evento.nivel = request.POST.get('nivel')
        evento.observaciones = request.POST.get('observaciones')
        evento.save()

        messages.success(request, "✅ Evento actualizado correctamente.")
        return redirect('panel_admin_eventos')

    return render(request, 'eventos/editar_evento.html', {'evento': evento})


@login_required
def eliminar_evento(request, evento_id):
    """Elimina un evento del sistema."""
    if not request.user.is_staff:
        messages.error(request, "No tienes permiso para eliminar eventos.")
        return redirect('home')

    evento = get_object_or_404(Evento, id=evento_id)
    evento.delete()
    messages.success(request, "🗑 Evento eliminado correctamente.")
    return redirect('panel_admin_eventos')


@login_required
def detalle_evento_admin(request, evento_id):
    """Muestra los detalles de un evento (versión admin)."""
    if not request.user.is_staff:
        messages.error(request, "No tienes permiso para ver este evento.")
        return redirect('home')

    evento = get_object_or_404(Evento, id=evento_id)
    return render(request, 'eventos/detalle_evento_admin.html', {'evento': evento})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def panel_admin(request):
    return render(request, 'eventos/panel_admin.html')

@login_required
@user_passes_test(lambda u: u.is_staff)
def detalle_usuario_admin(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    return render(request, 'eventos/detalle_usuario_admin.html', {'usuario': usuario})

@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_usuario_admin(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')
        usuario.is_staff = request.POST.get('is_staff') == 'on' == 'on'
        usuario.save()
        messages.success(request, 'Usuario actualizado correctamente.')
        return redirect('dashboard')
    return render(request, 'eventos/editar_usuario_admin.html', {'usuario': usuario})

@login_required
@user_passes_test(lambda u: u.is_staff)
def eliminar_usuario_admin(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    usuario.delete()
    messages.success(request, 'Usuario eliminado correctamente.')
    return redirect('dashboard')
