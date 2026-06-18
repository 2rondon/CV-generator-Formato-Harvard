import flet as ft
from controllers.cv_controller import CVController

def certifications_view(page: ft.Page, user_id):
    name_in = ft.TextField(label="Nombre de la Certificación", width=400)
    authority_in = ft.TextField(label="Autoridad Emisora / Institución", width=400)
    date_in = ft.TextField(label="Fecha de Expedición (Ej: Nov 2025)", width=200)
    
    list_view = ft.ListView(height=220, spacing=10, scroll=ft.ScrollMode.AUTO)

    def refresh_list():
        list_view.controls.clear()
        try:
            items = CVController.get_items("certifications", user_id)
            for item in items:
                list_view.controls.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Column([
                                    ft.Text(item['name'], weight=ft.FontWeight.BOLD, color="black"),
                                    ft.Text(f"Emitido por: {item['authority']} | {item['issue_date']}", color="grey700", size=13),
                                ], expand=True),
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
            print(f"Error al obtener certificaciones: {ex}")
            
        page.update()

    def add_item(e):
        if name_in.value and authority_in.value:
            CVController.add_item("certifications", {
                "user_id": user_id, 
                "name": name_in.value,
                "authority": authority_in.value,
                "issue_date": date_in.value
            })
            name_in.value = authority_in.value = date_in.value = ""
            refresh_list()

    def delete_item(item_id):
        CVController.delete_item("certifications", item_id)
        refresh_list()

    refresh_list()
    
    return ft.Column([
        ft.Text("Módulo de Certificaciones y Cursos", size=22, weight=ft.FontWeight.BOLD, color="black"),
        ft.Container(height=5),
        name_in, 
        authority_in,
        date_in,
        ft.Container(height=5),
        ft.ElevatedButton("Añadir Certificación", on_click=add_item, bgcolor="#1A365D", color="white"),
        ft.Container(height=10),
        ft.Text("Certificaciones Almacenadas:", size=14, weight=ft.FontWeight.W_600, color="black"),
        list_view
    ], spacing=10, scroll=ft.ScrollMode.AUTO)