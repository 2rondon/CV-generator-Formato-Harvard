import flet as ft
import os
import webbrowser  
from tkinter import filedialog, Tk
from views.experience_view import experience_view
from views.education_view import education_view
from views.skills_view import skills_view
from views.certifications_view import certifications_view
from views.personal_data_view import personal_data_view
from views.languages_view import languages_view
from views.activities_view import activities_view
from views.about_view import about_view

def dashboard_view(page: ft.Page, user_id):
    page.window_width = 1100
    page.window_height = 700
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.padding = 0  
    page.update()

    def handle_logout(e):
        page.data["user_id"] = None  
        page.padding = 10 
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.data["navigate"]("/login")  

    # --- LÓGICA DE APERTURA DIRECTA CON WEBBROWSER ---
    def click_abrir_y_descargar_pdf(e):
        try:
            import sys
            from tkinter import filedialog, Tk
            from utils.pdf_generator import generar_harvard_pdf
            
            # Ocultamos temporalmente los canales de salida para que los logs internos de las APIs de Windows
            # creados por Tkinter no se envíen en crudo a la consola asíncrona de Flet CLI
            original_stdout = sys.stdout
            original_stderr = sys.stderr
            
            # 1. Creamos la instancia oculta de Tkinter
            root = Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            # Redirección de flujos para aislamiento seguro durante el diálogo
            sys.stdout = open(os.devnull, 'w')
            sys.stderr = open(os.devnull, 'w')
            
            # 2. Abrimos el cuadro de diálogo con textos planos cortos
            ruta_destino = filedialog.asksaveasfilename(
                title="Guardar CV",
                initialfile="Mi_CV_Formato_Harvard.pdf",
                defaultextension=".pdf",
                filetypes=[("Archivos PDF", "*.pdf")]
            )
            
            root.destroy()
            
            # Restauramos inmediatamente las salidas estándar del sistema
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            
            # 3. Procesamos el resultado del guardado
            if ruta_destino:
                generar_harvard_pdf(user_id, filename=ruta_destino)
                
                page.snack_bar = ft.SnackBar(
                    ft.Text("PDF guardado con exito en la ruta seleccionada."),
                    bgcolor="green700",
                    duration=4000
                )
                page.snack_bar.open = True
            else:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Guardado cancelado por el usuario."),
                    bgcolor="orange800",
                    duration=3000
                )
                page.snack_bar.open = True
                
        except Exception as ex:
            # Aseguramos la restauración de salidas incluso en caso de fallo crítico
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            
            page.snack_bar = ft.SnackBar(
                ft.Text("Error al procesar o guardar el PDF."),
                bgcolor="red700",
                duration=5000
            )
            page.snack_bar.open = True
        page.update()

    # --- COMPONENTES DE LA INTERFAZ ORIGINAL ---
    pdf_list_view = ft.ListView(height=180, spacing=10, scroll=ft.ScrollMode.AUTO)
    pdf_list_view.controls.append(
        ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text("📄 Mi_CV_Harvard_Formato.pdf", weight=ft.FontWeight.BOLD, color="black"),
                    ft.Text("Estructura unificada ATS", color="grey700", size=13),
                ], expand=True),
                ft.FilledButton("Ver / Descargar", on_click=click_abrir_y_descargar_pdf, style=ft.ButtonStyle(bgcolor="#1A365D", color="white"))
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor="#EFF6FF", 
            padding=12,
            border_radius=6
        )
    )

    content_area = ft.Container(
        content=ft.Column([
            ft.Text("Panel Principal", size=26, weight=ft.FontWeight.BOLD, color="black"),
            ft.Text("Gestiona, visualiza y descarga tus currículums con formato Harvard ATS.", color="grey700"),
            ft.Container(height=15),
            ft.FilledButton("⚙️ Generar y Abrir PDF en el Navegador", on_click=click_abrir_y_descargar_pdf, style=ft.ButtonStyle(bgcolor="#1E293B", color="white")),
            ft.Container(height=15),
            ft.Text("Tus Documentos Guardados:", size=16, weight=ft.FontWeight.W_600, color="black"),
            pdf_list_view
        ], spacing=10),
        bgcolor="white", padding=30, width=1100, height=1100,   
    )

    # --- NAVEGACIÓN TOTALMENTE SÍNCRONA Y FLUIDA ---
    def change_menu_selection(e, section_key):
        if section_key == "dashboard":
            content_area.content = ft.Column([
                ft.Text("Panel Principal", size=26, weight=ft.FontWeight.BOLD, color="black"),
                ft.Text("Gestiona, visualiza y descarga tus currículums con formato Harvard ATS.", color="grey700"),
                ft.Container(height=15),
                ft.FilledButton("⚙️ Generar y Abrir PDF en el Navegador", on_click=click_abrir_y_descargar_pdf, style=ft.ButtonStyle(bgcolor="#1E293B", color="white")),
                ft.Container(height=15),
                ft.Text("Tus Documentos Guardados:", size=16, weight=ft.FontWeight.W_600, color="black"),
                pdf_list_view
            ], spacing=10)
        elif section_key == "datos":
            content_area.content = personal_data_view(page=page, user_id=user_id)
        elif section_key == "experiencia":
            content_area.content = experience_view(page=page, user_id=user_id)
        elif section_key == "educacion":
            content_area.content = education_view(page=page, user_id=user_id)
        elif section_key == "habilidades":
            content_area.content = skills_view(page=page, user_id=user_id)
        elif section_key == "certificaciones":
            content_area.content = certifications_view(page=page, user_id=user_id)
        elif section_key == "idiomas":
            content_area.content = languages_view(page=page, user_id=user_id)
        elif section_key == "actividades":
            content_area.content = activities_view(page=page, user_id=user_id)
        elif section_key == "about":
            content_area.content = about_view(page=page, user_id=user_id)
        page.update()

    sidebar = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text("CV Generator", size=22, color="white", weight=ft.FontWeight.BOLD),
                    ft.Text("Estilo Harvard", size=12, color="blue200"),
                ]), padding={"top": 20, "bottom": 15, "left": 15}
            ),
            ft.Container(content=ft.Text("📊 Dashboard", color="white", weight=ft.FontWeight.W_500), padding=12, on_click=lambda e: change_menu_selection(e, "dashboard")),
            ft.Container(content=ft.Text("👤 Datos Personales", color="white", weight=ft.FontWeight.W_500), padding=12, on_click=lambda e: change_menu_selection(e, "datos")),
            ft.Container(content=ft.Text("💼 Experiencia Laboral", color="white", weight=ft.FontWeight.W_500), padding=12, on_click=lambda e: change_menu_selection(e, "experiencia")),
            ft.Container(content=ft.Text("🎓 Educación", color="white", weight=ft.FontWeight.W_500), padding=12, on_click=lambda e: change_menu_selection(e, "educacion")),
            ft.Container(content=ft.Text("🛠️ Habilidades", color="white", weight=ft.FontWeight.W_500), padding=12, on_click=lambda e: change_menu_selection(e, "habilidades")),
            ft.Container(content=ft.Text("🌐 Idiomas", color="white", weight=ft.FontWeight.W_500), padding=12, on_click=lambda e: change_menu_selection(e, "idiomas")),
            ft.Container(content=ft.Text("🏆 Actividades", color="white", weight=ft.FontWeight.W_500), padding=12, on_click=lambda e: change_menu_selection(e, "actividades")),
            ft.Container(content=ft.Text("📜 Certificaciones", color="white", weight=ft.FontWeight.W_500), padding=12, on_click=lambda e: change_menu_selection(e, "certificaciones")),
            ft.Divider(color="blue700", height=30),
            ft.Container(content=ft.Text("ℹ️ Acerca de", color="white", weight=ft.FontWeight.W_500), padding=12, on_click=lambda e: change_menu_selection(e, "about")),
            ft.Divider(color="blue700", height=15),
            ft.Container(content=ft.Text("🚪 Cerrar Sesión", color="#FCA5A5", weight=ft.FontWeight.BOLD), padding=12, bgcolor="#7F1D1D", border_radius=4, on_click=handle_logout)
        ], spacing=2),
        width=150, height=1150, bgcolor="#1E293B"
    )

    return ft.Row([sidebar, content_area], spacing=1)