import flet as ft
import sqlite3

def skills_view(page: ft.Page, user_id):
    # Campos de entrada basados en tu estructura de base de datos
    category_in = ft.TextField(
        label="Categoría (Ej: Lenguajes, Frameworks, Herramientas)", 
        width=500,
        hint_text="Backend, Frontend, Bases de Datos..."
    )
    skills_list_in = ft.TextField(
        label="Habilidades / Tecnologías (Separadas por comas)", 
        width=500,
        hint_text="Python, PHP, JavaScript, Node.js"
    )
    
    # Lista visual para renderizar lo que viene de la DB
    skills_list_view = ft.ListView(height=200, spacing=10, scroll=ft.ScrollMode.AUTO)
    status_text = ft.Text("", color="green", weight=ft.FontWeight.BOLD)

    def load_skills():
        skills_list_view.controls.clear()
        try:
            conn = sqlite3.connect("cv_generator.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT id, category, skills_list FROM skills WHERE user_id = ?", 
                (user_id,)
            )
            rows = cursor.fetchall()
            
            for row in rows:
                cat = row["category"]
                s_list = row["skills_list"]
                item_id = row["id"]

                # Añadimos la tarjeta sin elementos que rompan el ciclo
                skills_list_view.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Column([
                                ft.Text(f"🛠️ {cat}", weight=ft.FontWeight.BOLD, color="black", size=16),
                                ft.Text(f"{s_list}", color="grey700", size=14),
                            ], expand=True),
                            # CORREGIDO: Usamos TextButton con emoji para evitar fallas de Material Icons
                            ft.TextButton(
                                content=ft.Text("🗑️ Borrar", color="red700", weight=ft.FontWeight.BOLD),
                                on_click=lambda e, id_del=item_id: delete_skill(id_del)
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        bgcolor="#F8FAFC",
                        padding=12,
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
            print(f"Error al cargar habilidades de la DB: {ex}")
        page.update()

    def save_skill(e):
        if not category_in.value or not skills_list_in.value:
            status_text.value = "⚠️ Ambos campos son completamente obligatorios."
            status_text.color = "red"
            page.update()
            return

        try:
            conn = sqlite3.connect("cv_generator.db")
            cursor = conn.cursor()
            
            query = """
            INSERT INTO skills (user_id, category, skills_list)
            VALUES (?, ?, ?)
            """
            
            cursor.execute(query, (
                user_id,
                category_in.value.strip(),
                skills_list_in.value.strip()
            ))
            
            conn.commit()
            conn.close()

            status_text.value = "✅ ¡Bloque de habilidades añadido con éxito!"
            status_text.color = "green"
            
            category_in.value = ""
            skills_list_in.value = ""
            
            # Recargamos la lista leyendo directo de la DB
            load_skills()
            
        except Exception as ex:
            status_text.value = f"❌ Error al guardar: {ex}"
            status_text.color = "red"
        page.update()

    def delete_skill(item_id):
        try:
            conn = sqlite3.connect("cv_generator.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM skills WHERE id = ?", (item_id,))
            conn.commit()
            conn.close()
            
            status_text.value = "🗑️ Categoría eliminada."
            status_text.color = "blue700"
            load_skills()
        except Exception as ex:
            status_text.value = f"❌ Error al eliminar: {ex}"
            status_text.color = "red"
            page.update()

    # Carga inicial al cambiar al menú de habilidades
    load_skills()

    return ft.Column([
        ft.Text("Módulo de Habilidades", size=22, weight=ft.FontWeight.BOLD, color="black"),
        ft.Text("Agrupa tus conocimientos por categorías técnicas para el formato Harvard ATS.", color="grey700"),
        ft.Container(height=10),
        category_in,
        skills_list_in,
        ft.Container(height=5),
        status_text,
        ft.Container(height=5),
        ft.FilledButton("Añadir Habilidades", on_click=save_skill, style=ft.ButtonStyle(bgcolor="#1A365D", color="white")),
        ft.Container(height=15),
        ft.Text("Tus Habilidades Almacenadas:", size=16, weight=ft.FontWeight.W_600, color="black"),
        skills_list_view
    ], spacing=10, scroll=ft.ScrollMode.AUTO)