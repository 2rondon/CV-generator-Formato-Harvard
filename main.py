import flet as ft
from database.connection import init_db
from views.login_view import login_view
from views.register_view import register_view
from views.dashboard_view import dashboard_view

def main(page: ft.Page):
    page.title = "Generador de Currículums Estilo Harvard"
    page.window_width = 1100
    page.window_height = 750
    page.window_resizable = True
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Alineamos el contenido de la página al centro para que las vistas luzcan profesionales
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Inicializar Base de Datos de forma segura (Descoméntala si ya está lista)
    init_db()

    # Estado de la sesión
    page.data = {"user_id": None}

    # Callback al iniciar sesión con éxito
    def on_login_success(user_id):
        page.data["user_id"] = user_id
        navigate_to("/dashboard")

    # Función de enrutamiento personalizada (Inmune a la pantalla gris)
    def navigate_to(route):
    # Limpiamos por completo todos los controles residuales de la pantalla
     page.clean() 
    
     if route == "/login":
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        # CORREGIDO: Le pasamos 'on_login_success' como segundo argumento
        page.add(login_view(page, on_login_success))
        
     elif route == "/register":
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.add(register_view(page))
        
     elif route == "/dashboard":
        # Extraemos de forma segura el ID de usuario guardado en el estado
        u_id = page.data.get("user_id", 1)
        
        # Ajustamos la alineación de la página para el panel de control
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.START
        
        # Inyectamos la vista directamente en la raíz limpia de la página
        page.add(dashboard_view(page, u_id))
        
    # Forzamos a Flet a redibujar el lienzo desde cero
    page.update()

    # expone la función de navegación globalmente para poder usarla desde las vistas
    page.data["navigate"] = navigate_to

    # Carga inicial de la app
    navigate_to("/login")

if __name__ == "__main__":
    ft.run(main)