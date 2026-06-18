import flet as ft
import sqlite3

def education_view(page: ft.Page, user_id):
    # Campos de entrada alineados con tus columnas de la base de datos
    institution_in = ft.TextField(label="Institución / Universidad", width=500)
    degree_in = ft.TextField(label="Título / Carrera (Degree)", width=500)
    location_in = ft.TextField(label="Ubicación (Ej: Caracas, Venezuela)", width=500)
    graduation_date_in = ft.TextField(label="Fecha de Graduación (Ej: Nov 2025)", width=500)
    
    # Lista visual para mostrar los estudios guardados abajo
    education_list = ft.ListView(height=200, spacing=10, scroll=ft.ScrollMode.AUTO)
    status_text = ft.Text("", color="green", weight=ft.FontWeight.BOLD)

    def load_education():
        education_list.controls.clear()
        try:
            # Consulta SQL directa a la DB para leer de forma limpia
            conn = sqlite3.connect("cv_generator.db")
            conn.row_factory = sqlite3.Row  
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT id, institution, degree, location, graduation_date FROM education WHERE user_id = ?", 
                (user_id,)
            )
            rows = cursor.fetchall()
            
            for row in rows:
                inst = row["institution"]
                deg = row["degree"]
                loc = row["location"]
                date = row["graduation_date"]
                item_id = row["id"]

                education_list.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Column([
                                ft.Text(f"🎓 {deg}", weight=ft.FontWeight.BOLD, color="black"),
                                ft.Text(f"🏫 {inst} — 📍 {loc}", color="grey700", size=14),
                                ft.Text(f"📅 Graduación: {date}", color="grey600", size=12),
                            ], expand=True),
                            # CORREGIDO: Usamos TextButton con emoji para evitar fallas de Material Icons
                            ft.TextButton(
                                content=ft.Text("🗑️ Borrar", color="red700", weight=ft.FontWeight.BOLD),
                                on_click=lambda e, id_del=item_id: delete_education(id_del)
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        bgcolor="#F8FAFC",
                        padding=10,
                        border_radius=6,
                        border=ft.Border(
                            ft.BorderSide(1, "#E2E8F0"),
                            ft.BorderSide(1, "#E2E8F0"),
                            ft.BorderSide(1, "#E2E8F0"),
                            ft.BorderSide(1, "#E2E8F0")
                        )
                    )
                )
            conn.close()
        except Exception as ex:
            print(f"Error al cargar educación de la DB: {ex}")
        page.update()

    def save_education(e):
        if not institution_in.value or not degree_in.value:
            status_text.value = "⚠️ La institución y el título son obligatorios."
            status_text.color = "red"
            page.update()
            return

        try:
            conn = sqlite3.connect("cv_generator.db")
            cursor = conn.cursor()
            
            query = """
            INSERT INTO education (user_id, institution, degree, location, graduation_date)
            VALUES (?, ?, ?, ?, ?)
            """
            
            cursor.execute(query, (
                user_id,
                institution_in.value,
                degree_in.value,
                location_in.value,
                graduation_date_in.value
            ))
            
            conn.commit()
            conn.close()

            status_text.value = "✅ ¡Educación añadida con éxito!"
            status_text.color = "green"
            
            # Limpiamos los campos del formulario
            institution_in.value = ""
            degree_in.value = ""
            location_in.value = ""
            graduation_date_in.value = ""
            
            # Forzamos recarga directa
            load_education()
            
        except Exception as ex:
            status_text.value = f"❌ Error al guardar: {ex}"
            status_text.color = "red"
        page.update()

    def delete_education(item_id):
        try:
            conn = sqlite3.connect("cv_generator.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM education WHERE id = ?", (item_id,))
            conn.commit()
            conn.close()

            status_text.value = "🗑️ Registro eliminado."
            status_text.color = "blue700"
            load_education()
        except Exception as ex:
            status_text.value = f"❌ Error al eliminar: {ex}"
            status_text.color = "red"
            page.update()

    load_education()

    return ft.Column([
        ft.Text("Módulo de Educación", size=22, weight=ft.FontWeight.BOLD, color="black"),
        ft.Text("Agrega tus títulos universitarios, técnicos o cursos de formación.", color="grey700"),
        ft.Container(height=10),
        institution_in,
        degree_in,
        location_in,
        graduation_date_in,
        ft.Container(height=5),
        status_text,
        ft.Container(height=5),
        ft.FilledButton("Añadir Educación", on_click=save_education, style=ft.ButtonStyle(bgcolor="#1A365D", color="white")),
        ft.Container(height=15),
        ft.Text("Educación Almacenada:", size=16, weight=ft.FontWeight.W_600, color="black"),
        education_list
    ], spacing=10, scroll=ft.ScrollMode.AUTO)