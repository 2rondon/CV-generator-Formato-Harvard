import flet as ft
from controllers.cv_controller import CVController

def experience_view(page: ft.Page, user_id):
    comp_in = ft.TextField(label="Empresa", width=400)
    role_in = ft.TextField(label="Cargo / Rol", width=400)
    loc_in = ft.TextField(label="Ubicación", width=150)
    start_in = ft.TextField(label="Fecha Inicio (Ej: May 2022)", width=150)
    end_in = ft.TextField(label="Fecha Fin (Ej: Actualidad)", width=150)
    
    desc_in = ft.TextField(
        label="Logros y Responsabilidades (Separa con saltos de línea para viñetas ATS)", 
        multiline=True, 
        min_lines=3,
        width=400
    )
    
    # IMPORTANTE: Eliminamos expand=True y le damos una altura fija controlada para tu versión
    list_view = ft.ListView(height=200, spacing=10, scroll=ft.ScrollMode.AUTO)

    def refresh_list():
        list_view.controls.clear()
        try:
            items = CVController.get_items("experience", user_id)
            for item in items:
                list_view.controls.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Column([
                                    ft.Text(f"{item['role']} en {item['company']}", weight=ft.FontWeight.BOLD, color="black"),
                                    ft.Text(f"{item['start_date']} - {item['end_date']} | {item['location']}", color="grey700", size=13),
                                ], expand=True),
                                # Botón de eliminar seguro sin iconos conflictivos
                                ft.Container(
                                    content=ft.Text("✖", color="red", weight=ft.FontWeight.BOLD),
                                    on_click=lambda e, i=item['id']: delete_item(i),
                                    padding=10
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        bgcolor="#F3F4F6",
                        padding=10,
                        border_radius=6
                    )
                )
        except Exception as ex:
            print(f"Error al obtener experiencia: {ex}")
            
        page.update()

    def add_item(e):
        if comp_in.value and role_in.value:
            CVController.add_item("experience", {
                "user_id": user_id, 
                "company": comp_in.value, 
                "role": role_in.value,
                "location": loc_in.value, 
                "start_date": start_in.value, 
                "end_date": end_in.value, 
                "description": desc_in.value
            })
            comp_in.value = role_in.value = loc_in.value = start_in.value = end_in.value = desc_in.value = ""
            refresh_list()

    def delete_item(item_id):
        CVController.delete_item("experience", item_id)
        refresh_list()

    # Carga inicial
    refresh_list()
    
    return ft.Column([
        ft.Text("Módulo de Experiencia Profesional", size=22, weight=ft.FontWeight.BOLD, color="black"),
        ft.Container(height=5),
        comp_in, 
        role_in, 
        ft.Row([start_in, end_in, loc_in], spacing=10), 
        desc_in,
        ft.Container(height=5),
        # Botón sin icono de sistema rígido para evitar fallas
        ft.ElevatedButton("Añadir Experiencia", on_click=add_item, bgcolor="#1A365D", color="white"),
        ft.Container(height=10),
        ft.Text("Experiencias registradas:", size=14, weight=ft.FontWeight.W_600, color="black"),
        list_view
    ], spacing=10, scroll=ft.ScrollMode.AUTO)