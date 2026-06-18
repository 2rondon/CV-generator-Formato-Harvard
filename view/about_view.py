import flet as ft

def about_view(page: ft.Page, user_id=None):
    # Ajustes estructurales de la vista alineados con el content_area de tu proyecto
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    
    title_section = ft.Column([
        ft.Text("Acerca del Software", size=26, weight=ft.FontWeight.BOLD, color="black"),
        ft.Text("Información del desarrollador, versión del sistema y canales de soporte.", color="grey700"),
        ft.Container(height=10),
    ], spacing=5)

    # Bloque 1: Información del Desarrollador Profesional (Sin módulos de border)
    developer_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("👤", size=22), 
                ft.Text("Perfil Profesional", size=18, weight=ft.FontWeight.BOLD, color="#1A365D"),
            ], alignment=ft.MainAxisAlignment.START),
            ft.Divider(color="#E2E8F0", height=2),
            ft.Text("Ing. Anderson E. Rondon Laya", size=16, weight=ft.FontWeight.BOLD, color="black"),
            ft.Text("Ingeniero de Sistemas", size=13, color="grey700", italic=True),
            ft.Container(height=5),
            ft.Row([
                ft.Text("📍", size=16),
                ft.Text("Caracas, Venezuela", size=13, color="grey800"),
            ]),
            ft.Row([
                ft.Text("🔗", size=16),
                ft.Text("LinkedIn: linkedin.com/in/ing-anderson-rondon-laya", size=13, color="blue800", selectable=True),
            ]),
            ft.Row([
                ft.Text("💻", size=16),
                ft.Text("Versión del Software: v1.0.2", size=13, color="grey800", weight=ft.FontWeight.BOLD),
            ]),
        ], spacing=10),
        bgcolor="#F8FAFC",
        padding=20,
        border_radius=8  # Usamos solo radio para dar forma, sin invocar ft.border
    )

    # Bloque 2: Canales de Contribuciones y Donaciones (Sin módulos de border)
    donations_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("❤️", size=22), 
                ft.Text("Apoyo al Proyecto / Donaciones", size=18, weight=ft.FontWeight.BOLD, color="#B91C1C"),
            ], alignment=ft.MainAxisAlignment.START),
            ft.Text(
                "Si este software te ha sido de utilidad para optimizar tus procesos y flujos de trabajo, "
                "puedes apoyar su mantenimiento y la integración de nuevas mejoras a través de los siguientes canales:",
                size=13, color="grey700"
            ),
            ft.Divider(color="#FEE2E2", height=2),
            
            # Sub-Bloque: PayPal
            ft.Container(
                content=ft.Row([
                    ft.Text("💳", size=20),
                    ft.Column([
                        ft.Text("PayPal", size=14, weight=ft.FontWeight.BOLD, color="black"),
                        ft.Text("rondonanderson24@gmail.com", size=13, color="grey800", selectable=True),
                    ], spacing=2)
                ]),
                bgcolor="#EFF6FF", padding=12, border_radius=6
            ),
            
            # Sub-Bloque: Binance Crypto
            ft.Container(
                content=ft.Row([
                    ft.Text("🪙", size=20),
                    ft.Column([
                        ft.Text("Binance Pay (Cualquier monto en USDT o USDC)", size=14, weight=ft.FontWeight.BOLD, color="black"),
                        ft.Text("Correo: anderson.rondon256@gmail.com", size=13, color="grey800", selectable=True),
                        ft.Text("ID de Binance: 357365998", size=13, color="grey800", weight=ft.FontWeight.BOLD, selectable=True),
                    ], spacing=2)
                ]),
                bgcolor="#FEFCE8", padding=12, border_radius=6
            ),
        ], spacing=12),
        bgcolor="#FFFDFD",
        padding=20,
        border_radius=8  # Usamos solo radio para dar forma, sin invocar ft.border
    )

    # Contenedor unificado para inyectar directo en el content_area del Dashboard
    return ft.Column([
        title_section,
        developer_card,
        ft.Container(height=10),
        donations_card
    ], spacing=10, scroll=ft.ScrollMode.AUTO, width=800, height=890)