import flet as ft
from controllers.cv_controller import CVController

def languages_view(user_id, page):
    lang_in = ft.TextField(label="Idioma")
    prof_in = ft.TextField(label="Nivel / Competencia (Ej: Nativo, Avanzado C1, Intermedio)")
    list_view = ft.ListView(expand=True, spacing=10)

    def refresh_list():
        list_view.controls.clear()
        items = CVController.get_items("languages", user_id)
        for item in items:
            list_view.controls.append(
                ft.ListTile(
                    title=ft.Text(item['language']),
                    subtitle=ft.Text(item['proficiency']),
                    trailing=ft.TextButton(
                     content=ft.Text("🗑️", size=18), # Emoji directo sin depender de ft.icons
                    on_click=lambda e, i=item['id']: delete_item(i)
                  )
                )
            )
        page.update()

    def add_item(e):
        CVController.add_item("languages", {"user_id": user_id, "language": lang_in.value, "proficiency": prof_in.value})
        lang_in.value = prof_in.value = ""
        refresh_list()

    def delete_item(item_id):
        CVController.delete_item("languages", item_id)
        refresh_list()

    refresh_list()
    return ft.Column([
        ft.Text("Módulo de Idiomas", size=22, weight=ft.FontWeight.BOLD),
        ft.Row([lang_in, prof_in]),
        ft.ElevatedButton("➕ Añadir Idioma", on_click=add_item, style=ft.ButtonStyle(bgcolor="#1A365D", color="white")),
        ft.Divider(),
        list_view
    ])