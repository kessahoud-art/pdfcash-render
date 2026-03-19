"""
Template Ebook — PDF Cash IA
Style identique au guide Facebook généré avec ReportLab
"""
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from .utils import (
    W, H, ML, MR, TW, DARK, GRAY, LGRAY, BORDER, GREEN, ORANGE,
    clean, hex_to_color, wrap_text, text_height,
    draw_header, draw_footer, section_title,
    tip_box, error_box, bullet_item,
    draw_cta_box, draw_brand_footer, metric_boxes, cover_base
)

BOTTOM = 50  # limite bas avant footer


def generate_ebook(content, color=None, author="Expert Digital Afrique"):
    """Génère un ebook complet en PDF. Retourne les bytes du PDF."""

    # Couleur accent
    ac_hex = (color.ac if color else None) or "#7c3aed"
    AC = hex_to_color(ac_hex)

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    c.setTitle(clean(content.title or "Ebook"))
    c.setAuthor(clean(author))
    c.setCreator("PDF Cash IA")

    page_num = 0
    chapters = content.chapters or []
    price = clean(content.price_suggested or "5 000 FCFA")

    # ────────────────────────────────────────
    # PAGE 1 — COUVERTURE
    # ────────────────────────────────────────
    c.showPage()
    page_num += 1

    nb = len(chapters)
    cover_base(
        c,
        label="EBOOK",
        title=content.title or "",
        subtitle=content.subtitle or "",
        tagline=content.tagline or "",
        price=price,
        author=author,
        ac_color=AC,
        infos=f"{nb} chapitres  |  Exemples en FCFA  |  Contexte africain"
    )

    # ────────────────────────────────────────
    # PAGE 2 — TABLE DES MATIÈRES
    # ────────────────────────────────────────
    c.showPage()
    page_num += 1
    draw_footer(c, page_num, AC)
    y = draw_header(c, content.title or "", "TABLE DES MATIERES", AC)

    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(DARK)
    c.drawString(ML, y, "Table des Matieres")
    y -= 26

    c.setStrokeColor(AC)
    c.setLineWidth(3)
    c.line(ML, y, ML + 30, y)
    y -= 16

    toc = content.table_of_contents or []
    for i, item in enumerate(toc[:7]):
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(AC)
        c.drawString(ML, y, str(i + 1).zfill(2))

        c.setFont("Helvetica", 11)
        c.setFillColor(DARK)
        c.drawString(ML + 36, y, clean(item))

        c.setStrokeColor(BORDER)
        c.setLineWidth(0.4)
        c.line(ML + 36, y - 4, W - MR, y - 4)
        y -= 20

    if content.description:
        y -= 14
        c.setStrokeColor(BORDER)
        c.setLineWidth(0.5)
        c.line(ML, y, W - MR, y)
        y -= 12
        c.setFont("Helvetica-Oblique", 10)
        c.setFillColor(GRAY)
        h = text_height(c, clean(content.description), TW, "Helvetica-Oblique", 10)
        wrap_text(c, clean(content.description), ML, y, TW, "Helvetica-Oblique", 10, GRAY)
        y -= h + 10

    # ────────────────────────────────────────
    # PAGES CHAPITRES
    # ────────────────────────────────────────
    for ci, ch in enumerate(chapters):
        c.showPage()
        page_num += 1
        draw_footer(c, page_num, AC)
        ch_title = clean(ch.title or f"Chapitre {ci + 1}")
        y = draw_header(c, content.title or "", ch_title[:35], AC)

        # Label chapitre
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(LGRAY)
        c.drawString(ML, y, f"CHAPITRE {str(ci + 1).zfill(2)}")
        y -= 14

        # Titre chapitre
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(AC)
        th = text_height(c, ch_title, TW, "Helvetica-Bold", 16)
        wrap_text(c, ch_title, ML, y, TW, "Helvetica-Bold", 16, AC)
        y -= th + 6

        # Ligne accent
        c.setStrokeColor(AC)
        c.setLineWidth(2)
        c.line(ML, y, ML + 50, y)
        y -= 14

        # Contenu
        content_text = clean(ch.content or "")
        paras = [p.strip() for p in content_text.split('\n') if p.strip() and len(p.strip()) > 2]

        for para in paras:
            # Détecter sous-titres
            is_heading = (
                (para.endswith(':') and len(para) < 80) or
                para.startswith('**') or
                (para[0].isdigit() and len(para) < 100 and ('.' in para[:3] or ')' in para[:3]))
            )

            if is_heading:
                head = para.replace('**', '').rstrip(':').lstrip('0123456789.) ')
                if not head or len(head) < 2:
                    continue
                if y < BOTTOM + 60:
                    c.showPage()
                    page_num += 1
                    draw_footer(c, page_num, AC)
                    y = draw_header(c, content.title or "", ch_title[:35], AC)
                y -= 6
                c.setFont("Helvetica-Bold", 11)
                c.setFillColor(AC)
                h = text_height(c, head, TW, "Helvetica-Bold", 11)
                wrap_text(c, head, ML, y, TW, "Helvetica-Bold", 11, AC)
                y -= h + 6
            else:
                ph = text_height(c, para, TW, "Helvetica", 11, 3)
                if y - ph < BOTTOM + 6:
                    c.showPage()
                    page_num += 1
                    draw_footer(c, page_num, AC)
                    y = draw_header(c, content.title or "", ch_title[:35], AC)
                wrap_text(c, para, ML, y, TW, "Helvetica", 11, DARK, 3)
                y -= ph + 12

        # Séparateur entre chapitres
        if ci < len(chapters) - 1:
            if y > BOTTOM + 20:
                y -= 8
                c.setStrokeColor(BORDER)
                c.setLineWidth(0.8)
                c.line(ML + TW / 3, y, ML + TW * 2 / 3, y)
                y -= 14

    # ────────────────────────────────────────
    # PAGE POINTS CLÉS + CONCLUSION
    # ────────────────────────────────────────
    c.showPage()
    page_num += 1
    draw_footer(c, page_num, AC)
    y = draw_header(c, content.title or "", "POINTS CLES", AC)

    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(DARK)
    c.drawString(ML, y, "Points Cles a Retenir")
    y -= 26

    c.setStrokeColor(AC)
    c.setLineWidth(3)
    c.line(ML, y, ML + 30, y)
    y -= 16

    for k in (content.key_takeaways or []):
        kt = clean(k)
        if not kt:
            continue
        kh = text_height(c, kt, TW - 20, "Helvetica", 11, 2)
        if y - kh < BOTTOM + 14:
            c.showPage()
            page_num += 1
            draw_footer(c, page_num, AC)
            y = draw_header(c, content.title or "", "POINTS CLES", AC)

        c.setStrokeColor(AC)
        c.setLineWidth(3)
        c.line(ML, y, ML, y - kh - 4)

        wrap_text(c, kt, ML + 14, y, TW - 20, "Helvetica", 11, DARK, 2)
        y -= kh + 16

    # CTA
    if y > BOTTOM + 80:
        y -= 20
    else:
        c.showPage()
        page_num += 1
        draw_footer(c, page_num, AC)
        y = draw_header(c, content.title or "", "CONCLUSION", AC)

    cta = clean(content.call_to_action or "Passe a l'action maintenant !")
    y = draw_cta_box(c, cta, price, y, AC)

    # Potentiel revenus
    if y > BOTTOM + 60:
        y -= 10
        pn = int(''.join(filter(str.isdigit, price)) or '5000') if price else 5000
        y = metric_boxes(c, [
            {"label": "10 ventes", "value": f"{pn*10:,} F".replace(",", " "), "color_hex": ac_hex},
            {"label": "50 ventes", "value": f"{pn*50:,} F".replace(",", " "), "color_hex": ac_hex},
            {"label": "100 ventes", "value": f"{pn*100:,} F".replace(",", " "), "color_hex": ac_hex},
        ], y, BORDER)

    # WhatsApp
    if content.sales_message and y > BOTTOM + 50:
        y -= 8
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(DARK)
        c.drawString(ML, y, "MESSAGE DE VENTE WHATSAPP")
        y -= 14
        c.setStrokeColor(GREEN)
        c.setLineWidth(3)
        msg = clean(content.sales_message)
        mh = text_height(c, msg, TW - 14, "Helvetica", 10, 2)
        c.line(ML, y, ML, y - mh - 4)
        wrap_text(c, msg, ML + 12, y, TW - 18, "Helvetica", 10, DARK, 2)
        y -= mh + 16

    # Facebook Ads
    if content.facebook_ads and content.facebook_ads.texte_principal and y > BOTTOM + 40:
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(DARK)
        c.drawString(ML, y, "SCRIPT FACEBOOK ADS")
        y -= 14
        c.setStrokeColor(colors.HexColor("#3B82F6"))
        c.setLineWidth(3)
        ads = clean(content.facebook_ads.texte_principal)
        ah = text_height(c, ads, TW - 14, "Helvetica", 10, 2)
        c.line(ML, y, ML, y - ah - 4)
        wrap_text(c, ads, ML + 12, y, TW - 18, "Helvetica", 10, DARK, 2)
        y -= ah + 14

    # Marque finale
    if y > BOTTOM + 25:
        draw_brand_footer(c, y - 10, AC)

    c.save()
    buf.seek(0)
    return buf.read()
