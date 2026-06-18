import flet as ft

def register_view(page: ft.Page):
    # Campos de texto para el registro de usuarios
    username_field = ft.TextField(
        label="Nuevo Usuario", 
        width=300, 
        prefix_icon="PERSON_ADD", 
        autofocus=True
    )
    
    password_field = ft.TextField(
        label="Contraseña", 
        password=True, 
        can_reveal_password=True, 
        width=300, 
        prefix_icon="LOCK_OUTLINE"
    )
    
    confirm_password_field = ft.TextField(
        label="Confirmar Contraseña", 
        password=True, 
        can_reveal_password=True, 
        width=300, 
        prefix_icon="LOCK"
    )
    
    error_text = ft.Text(value="", color="red400")
    success_text = ft.Text(value="", color="green400")

    # Manejador del evento de registro
    def handle_register(e):
        # Limpiar mensajes previos
        error_text.value = ""
        success_text.value = ""
        
        # Validación básica inicial
        if not username_field.value or not password_field.value:
            error_text.value = "Todos los campos son obligatorios"
            page.update()
            return
            
        if password_field.value != confirm_password_field.value:
            error_text.value = "Las contraseñas no coinciden"
            page.update()
            return

        # Importación local para evitar bloqueos en la carga inicial
        from controllers.auth_controller import AuthController
        
        # Intentar registrar al usuario en la base de datos
        success, message = AuthController.register_user(username_field.value, password_field.value)
        
        if success:
            success_text.value = "¡Registro exitoso! Redirigiendo al login..."
            page.update()
            # Esperar un breve momento o redirigir directamente de forma segura
            page.data["navigate"]("/login")
        else:
            error_text.value = message
            page.update()

    # Devolvemos la columna limpia. Al usar el enrutador directo con page.add(),
    # main.py se encargará de centrar perfectamente toda la interfaz.
    return ft.Column(
        [
            ft.Text("Crear Nueva Cuenta", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Regístrate para empezar a diseñar tu CV", size=14, color="grey500"),
            ft.Container(height=10),
            username_field,
            password_field,
            confirm_password_field,
            error_text,
            success_text,
            ft.Container(height=5),
            # Botón de acción principal
            ft.Button(
                "Registrarse", 
                on_click=handle_register, 
                width=300
            ),
            # Botón para regresar usando el nuevo enrutador personalizado
            ft.TextButton(
                "¿Ya tienes cuenta? Inicia sesión aquí", 
                on_click=lambda _: page.data["navigate"]("/login")
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15
    )