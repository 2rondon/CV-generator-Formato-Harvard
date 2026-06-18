import flet as ft

def login_view(page: ft.Page, on_login_success):
    # Campos de texto con la propiedad de iconos y autofoco moderna
    username_field = ft.TextField(
        label="Usuario", 
        width=300, 
        prefix_icon="PERSON", 
        autofocus=True,
        focused_border_color="#1A365D" # <-- NUEVO: Color del borde al hacer clic
    )
    
    password_field = ft.TextField(
        label="Contraseña", 
        password=True, 
        can_reveal_password=True, 
        width=300, 
        prefix_icon="LOCK",
        focused_border_color="#1A365D" # <-- NUEVO: Color del borde al hacer clic
    )
    
    # Texto para manejo de errores de autenticación (usando string plano para el color)
    error_text = ft.Text(value="", color="red700") # <-- MODIFICADO: Un rojo más visible

    # Manejador del evento de inicio de sesión
    def handle_login(e):
        # Importación local para evitar bucles de carga pesados en la raíz del archivo
        from controllers.auth_controller import AuthController
        
        # Validar credenciales en la base de datos
        success, res = AuthController.login_user(username_field.value, password_field.value)
        
        if success:
            # 'res' contiene el user_id retornado por el controlador
            on_login_success(res) 
        else:
            # 'res' contiene el mensaje de error en caso de fallo
            error_text.value = res
            page.update()

    # Retornamos la columna alineada. Al ser inyectada con page.add(), 
    # page.vertical_alignment y page.horizontal_alignment de main.py harán el resto.
    return ft.Column(
        [
            # <-- MODIFICADO: Añadido color institucional al título principal
            ft.Text("Generador de CV Estándar Harvard", size=24, weight=ft.FontWeight.BOLD, color="#1A365D"),
            ft.Text("Inicia sesión para continuar", size=14, color="grey600"),
            ft.Container(height=10),
            username_field,
            password_field,
            error_text,
            ft.Container(height=5),
            # Botón moderno unificado (ft.Button en lugar de ft.ElevatedButton)
            ft.Button(
                "Iniciar Sesión", 
                on_click=handle_login, 
                width=300,
                # <-- NUEVO: Estilo de fondo y letras para que no sea gris plano
                style=ft.ButtonStyle(
                    color="white",       # Texto blanco
                    bgcolor="#1A365D"   # Fondo azul marino
                )
            ),
            # Enrutamiento inmune a la pantalla gris usando la función global personalizada
            ft.TextButton(
                "¿No tienes cuenta? Regístrate aquí", 
                on_click=lambda _: page.data["navigate"]("/register"),
                style=ft.ButtonStyle(color="#1A365D") # <-- NUEVO: Texto azul marino
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15
    )