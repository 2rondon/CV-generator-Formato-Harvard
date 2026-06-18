import os
from controllers.cv_controller import CVController
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generar_harvard_pdf(user_id, filename="Mi_CV_Harvard_Sistemas.pdf"):
    # Recolección segura usando tu arquitectura nativa de controladores
    experiences = CVController.get_items("experience", user_id)
    educations = CVController.get_items("education", user_id)
    skills = CVController.get_items("skills", user_id)
    
    try: languages = CVController.get_items("languages", user_id)
    except Exception: languages = []
        
    try: activities = CVController.get_items("activities", user_id)
    except Exception: activities = []
        
    try:
        profiles = CVController.get_items("profile", user_id)
        profile = profiles[0] if profiles else None
    except Exception:
        profile = None

    # Configuración de ReportLab
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    story = []
    
    name_style = ParagraphStyle('HN', fontName='Helvetica-Bold', fontSize=20, leading=24, alignment=1, spaceAfter=4, textColor=colors.HexColor("#1A365D"))
    contact_style = ParagraphStyle('HC', fontName='Helvetica', fontSize=10, leading=14, alignment=1, spaceAfter=15, textColor=colors.HexColor("#4A5568"))
    section_heading = ParagraphStyle('HS', fontName='Helvetica-Bold', fontSize=12, leading=16, spaceBefore=12, spaceAfter=4, textColor=colors.HexColor("#1A365D"))
    body_style = ParagraphStyle('HB', fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor("#2D3748"))
    
    # --- ENCABEZADO HARVARD (BÚSQUEDA FLEXIBLE DE NOMBRE) ---
    if profile:
        # Intentar obtener el nombre combinando posibles variantes de llaves
        first = profile.get('first_name') or profile.get('nombre') or profile.get('name') or ""
        last = profile.get('last_name') or profile.get('apellido') or ""
        full = profile.get('full_name') or f"{first} {last}".strip()
        
        if not full:
            full = "MI CURRÍCULUM VITAE"
            
        story.append(Paragraph(full.upper(), name_style))
        
        # Datos de contacto tolerantes a campos None
        email = profile.get('email') or ""
        phone = profile.get('phone') or profile.get('telefono') or ""
        loc = profile.get('location') or profile.get('ubicacion') or ""
        
        # --- NUEVO: EXTRAER Y LIMPIAR LA URL DE LINKEDIN ---
        linkedin = profile.get('linkedin') or profile.get('linkedin_url') or profile.get('red_social') or ""
        if linkedin and str(linkedin).lower() != 'none':
            # Limpieza visual estilo Harvard (remueve protocolos de URL pesados)
            linkedin = linkedin.replace("https://www.", "").replace("http://", "").replace("https://", "").replace("www.", "")
        else:
            linkedin = ""
        
        # Construimos la lista filtrando elementos vacíos o con la cadena 'none'
        parts = [p for p in [email, phone, loc, linkedin] if p and str(p).lower() != 'none']
        c_info = " | ".join(parts)
        story.append(Paragraph(c_info, contact_style))
    else:
        story.append(Paragraph("MI CURRÍCULUM VITAE", name_style))
        story.append(Paragraph("Completa tus Datos Personales en el menú lateral", contact_style))
        
    def render_linea(titulo):
        story.append(Paragraph(titulo.upper(), section_heading))
        t = Table([['']], colWidths=[532])
        t.setStyle(TableStyle([('LINEABOVE', (0,0), (-1,-1), 1, colors.HexColor("#1A365D")), ('BOTTOMPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0)]))
        story.append(t)
        story.append(Spacer(1, 6))

    # Bloque: Experiencia
    if experiences:
        render_linea("Experiencia Laboral")
        for exp in experiences:
            comp = exp.get('company') or exp.get('empresa') or ""
            pos = exp.get('position') or exp.get('cargo') or exp.get('rol') or ""
            l_exp = exp.get('location') or exp.get('lugar') or ""
            sd = exp.get('start_date') or exp.get('fecha_inicio') or ""
            ed = exp.get('end_date') or exp.get('fecha_fin') or "Presente"
            desc = exp.get('description') or exp.get('descripcion') or ""

            t1 = Table([[Paragraph(f"<b>{comp}</b>", body_style), Paragraph(l_exp, ParagraphStyle('R', parent=body_style, alignment=2))]], colWidths=[382, 150])
            t1.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('PADDING', (0,0), (-1,-1), 0)]))
            story.append(t1)
            
            t2 = Table([[Paragraph(f"<i>{pos}</i>", body_style), Paragraph(f"{sd} – {ed}", ParagraphStyle('R2', parent=body_style, alignment=2))]], colWidths=[382, 150])
            t2.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('PADDING', (0,0), (-1,-1), 0)]))
            story.append(t2)
            
            if desc:
                story.append(Spacer(1, 3))
                story.append(Paragraph(f"• {desc}", body_style))
            story.append(Spacer(1, 10))

    # Bloque: Educación
    if educations:
        render_linea("Educación")
        for edu in educations:
            inst = edu.get('institution') or edu.get('institucion') or ""
            deg = edu.get('degree') or edu.get('titulo') or ""
            l_edu = edu.get('location') or edu.get('lugar') or ""
            g_date = edu.get('graduation_date') or edu.get('fecha_graduacion') or ""

            t1 = Table([[Paragraph(f"<b>{inst}</b>", body_style), Paragraph(l_edu, ParagraphStyle('R', parent=body_style, alignment=2))]], colWidths=[382, 150])
            t1.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('PADDING', (0,0), (-1,-1), 0)]))
            story.append(t1)
            t2 = Table([[Paragraph(deg, body_style), Paragraph(g_date, ParagraphStyle('R2', parent=body_style, alignment=2))]], colWidths=[382, 150])
            t2.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('PADDING', (0,0), (-1,-1), 0)]))
            story.append(t2)
            story.append(Spacer(1, 10))

    # Bloque: Habilidades
    if skills:
        render_linea("Habilidades Técnicas")
        for sk in skills:
            cat = sk.get('category') or sk.get('categoria') or ""
            s_list = sk.get('skills_list') or sk.get('habilidades') or ""
            story.append(Paragraph(f"<b>{cat}:</b> {s_list}", body_style))
            story.append(Spacer(1, 4))

    # --- BLOQUE IDIOMAS ---
    if languages:
        story.append(Spacer(1, 4))
        render_linea("Idiomas")
        for lang in languages:
            i_nombre = lang.get('language_name') or lang.get('language') or lang.get('idioma') or lang.get('nombre') or "Idioma"
            i_nivel = lang.get('proficiency') or lang.get('level') or lang.get('nivel') or "Nivel no especificado"
            
            story.append(Paragraph(f"• <b>{i_nombre}</b> — {i_nivel}", body_style))
            story.append(Spacer(1, 4))

    # Bloque: Actividades
    if activities:
        story.append(Spacer(1, 4))
        render_linea("Actividades Extracurriculares")
        for act in activities:
            org = act.get('organization') or act.get('organizacion') or ""
            rol = act.get('role') or act.get('rol') or act.get('posicion') or ""
            rango = act.get('date_range') or act.get('fechas') or ""
            desc_act = act.get('description') or act.get('descripcion') or ""
            
            story.append(Paragraph(f"<b>{org}</b> — <i>{rol}</i> ({rango})", body_style))
            if desc_act:
                story.append(Paragraph(f"• {desc_act}", body_style))
            story.append(Spacer(1, 4))

    doc.build(story)
    return os.path.abspath(filename)