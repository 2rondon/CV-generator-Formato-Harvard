import flet as ft
from controllers.cv_controller import CVController

def activities_view(page: ft.Page, user_id):
    org_in = ft.TextField(label="Organización / Fundación", width=500)
    role_in = ft.TextField(label="Rol / Posición")
    date_in = ft.TextField(label="Rango de Fechas (Ej: 2023 - 2026)")
    desc_in = ft.TextField(label="Descripción de la actividad corta", width=500)
    list_view = ft.ListView(height=200, spacing=10, scroll=ft.ScrollMode.AUTO)

    def refresh_list():
        list_view.controls.clear()
        try:
            items = CVController.get_items("activities", user_id)
            for item in items:
                list_view.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Column([
                                ft.Text(f"🏆 {item['role']} en {item['organization']}", weight=ft.FontWeight.BOLD, color="black"),
                                ft.Text(f"📅 {item['date_range']}", color="grey700", size=14),
                                ft.Text(f"📝 {item['description']}", color="grey600", size=12),
                            ], expand=True),
                            # Botón de borrar con texto/emoji para evitar fallas con ft.icons
                            ft.TextButton(
                                content=ft.Text("🗑️ Borrar", color="red700", weight=ft.FontWeight.BOLD),
                                on_click=lambda e, i=item['id']: delete_item(i)
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
        except Exception as ex:
            print(f"Error al cargar actividades: {ex}")
        page.update()

    def add_item(e):
        if not org_in.value or not role_in.value:
            return
        
        CVController.add_item("activities", {
            "user_id": user_id, 
            "organization": org_in.value.strip(), 
            "role": role_in.value.strip(),
            "date_range": date_in.value.strip(), 
            "description": desc_in.value.strip()
        })
        org_in.value = role_in.value = date_in.value = desc_in.value = ""
        refresh_list()

    def delete_item(item_id):
        CVController.delete_item("activities", item_id)
        refresh_list()

    refresh_list()
    
    return ft.Column([
        ft.Text("Actividades Extra-curriculares y Organizaciones", size=22, weight=ft.FontWeight.BOLD, color="black"),
        ft.Text("Añade voluntariados, roles de liderazgo o proyectos institucionales.", color="grey700"),
        ft.Container(height=10),
        org_in, 
        ft.Row([role_in, date_in], width=500), 
        desc_in,
        ft.Container(height=5),
        # CORREGIDO: Usamos FilledButton apuntando a add_item en saltos de línea limpios
        ft.FilledButton(
            "➕ Añadir Actividad", 
            on_click=add_item, 
            style=ft.ButtonStyle(bgcolor="#1A365D", color="white") 
        ),
        ft.Container(height=15),
        ft.Text("Actividades Guardadas:", size=16, weight=ft.FontWeight.W_600, color="black"),
        list_view
    ], spacing=10, scroll=ft.ScrollMode.AUTO)