import flet as ft
import sqlite3
from controllers.cv_controller import CVController

def personal_data_view(page: ft.Page, user_id):
    # Campos mapeados exactamente a las columnas de tu tabla 'profile'
    name_in = ft.TextField(label="Nombre Completo", width=500)
    email_in = ft.TextField(label="Correo Electrónico", width=500)
    phone_in = ft.TextField(label="Teléfono", width=500)
    linkedin_in = ft.TextField(label="Enlace a LinkedIn", width=500)
    
    # Mensaje de confirmación en pantalla
    status_text = ft.Text("", color="green", weight=ft.FontWeight.BOLD)

    def load_existing_data():
        try:
            # Buscamos en tu tabla existente 'profile'
            items = CVController.get_items("profile", user_id)
            if items:
                # Rellenamos usando los nombres exactos de tus columnas
                data = items[0]
                name_in.value = data.get("full_name", "")
                email_in.value = data.get("email", "")
                phone_in.value = data.get("phone", "")
                linkedin_in.value = data.get("linkedin", "")
        except Exception as ex:
            print(f"Nota al cargar perfil: {ex}")

    def save_data(e):
        if not name_in.value or not email_in.value:
            status_text.value = "⚠️ El nombre y el correo son obligatorios."
            status_text.color = "red"
            page.update()
            return

        try:
            # Conexión directa a la base de datos para evitar el problema de la columna 'id'
            conn = sqlite3.connect("cv_generator.db")
            cursor = conn.cursor()
            
            # Usamos INSERT OR REPLACE que gestiona la actualización de forma nativa por user_id
            query = """
            INSERT OR REPLACE INTO profile (user_id, full_name, email, phone, linkedin)
            VALUES (?, ?, ?, ?, ?)
            """
            
            cursor.execute(query, (
                user_id,
                name_in.value,
                email_in.value,
                phone_in.value,
                linkedin_in.value,
            ))
            
            conn.commit()
            conn.close()
            
            status_text.value = "✅ ¡Perfil guardado con éxito!"
            status_text.color = "green"
        except Exception as ex:
            status_text.value = f"❌ Error al guardar: {ex}"
            status_text.color = "red"
            
        page.update()

    # Cargar los datos del perfil inmediatamente al abrir la vista
    load_existing_data()

    return ft.Column([
        ft.Text("Módulo de Datos Personales", size=22, weight=ft.FontWeight.BOLD, color="black"),
        ft.Text("Esta información se guardará en tu perfil y aparecerá en el CV Harvard.", color="grey700"),
        ft.Container(height=10),
        name_in, 
        email_in, 
        phone_in,
        linkedin_in,
        ft.Container(height=5),
        status_text,
        ft.Container(height=5),
        ft.ElevatedButton("Guardar Datos Personales", on_click=save_data, bgcolor="#1A365D", color="white"),
    ], spacing=10, scroll=ft.ScrollMode.AUTO)