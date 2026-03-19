"""
Template Scripts TikTok — PDF Cash IA
"""
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from .utils import (
    W, H, ML, MR, TW, DARK, GRAY, LGRAY, BORDER,
    clean, hex_to_color, wrap_text, text_height,
    draw_header, draw_footer, draw_cta_box, draw_brand_footer, cover_base
)

BOTTOM = 50
RED  = colors.HexColor("#EE1D52")
CYAN = colors.HexColor("#69C9D0")

def generate_tiktok(content, color=None, author="Expert Contenu Digital"):
    ac_hex = "#EE1D52"
    AC = RED

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    c.setTitle(clean(content.title or "Scripts TikTok"))
    c.setAuthor(clean(author))
    c.setCreator("PDF Cash IA")

    page_num = 0
    chapters = content.chapters or []
    price = clean(content.price_suggested or "")

    def new_page(section):
        nonlocal page_num
        c.showPage()
        page_num += 1
        draw_footer(c, page_num, AC)
        return draw_header(c, content.title or "", section, AC)

    def section_badge(label, y, bg_color):
        c.setFillColor(bg_color)
        c.rect(ML, y - 22, TW, 22, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(colors.white)
        c.drawString(ML + 8, y - 15, label)
        return y - 26

    # PAGE 1 — COUVERTURE
    c.showPage()
    page_num += 1
    cover_base(c, "PACK SCRIPTS TIKTOK", content.title or "", content.subtitle or "",
               content.tagline or "", price, author, AC,
               f"{len(chapters)} scripts  |  Accroches virales  |  Hashtags inclus")

    # PAGE 2 — GUIDE D'UTILISATION
    y = new_page("GUIDE D'UTILISATION")
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(DARK)
    c.drawString(ML, y, "Comment utiliser ces scripts")
    y -= 24
    c.setStrokeColor(AC)
    c.setLineWidth(3)
    c.line(ML, y, ML + 30, y)
    y -= 16

    tips = [
        "Lis le script a voix haute 2-3 fois avant de filmer",
        "Adapte les exemples a ta ville et situation personnelle",
        "Filme en vertical 9:16 avec bonne lumiere",
        "Parle avec energie — le dynamisme est essentiel sur TikTok",
        "Ajoute une musique tendance depuis la bibliotheque TikTok",
        "Poste entre 18h et 21h pour maximiser la portee",
        "Reponds aux commentaires dans les 30 premieres minutes",
        "Utilise les hashtags suggeres + 2-3 hashtags populaires"
    ]
    for i, tip in enumerate(tips):
        c.setFillColor(RED if i % 2 == 0 else CYAN)
        c.rect(ML, y - 26, 26, 26, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(colors.white)
        c.drawString(ML, y - 18, str(i+1))
        c.setFont("Helvetica", 10)
        c.setFillColor(DARK)
        th = text_height(c, tip, TW - 36, "Helvetica", 10)
        wrap_text(c, tip, ML + 34, y - 8, TW - 36, "Helvetica", 10, DARK)
        y -= max(32, th + 14)

    # SCRIPTS — 1 par page
    for i, ch in enumerate(chapters[:6]):
        y = new_page(f"SCRIPT {str(i+1).zfill(2)}")

        # Badge script
        c.setFillColor(RED)
        c.rect(ML, y - 44, 44, 44, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.white)
        c.drawCentredString(ML + 22, y - 12, "SCRIPT")
        c.setFont("Helvetica-Bold", 22)
        c.drawCentredString(ML + 22, y - 32, str(i+1).zfill(2))

        # Titre
        ch_title = clean(ch.title or f"Script {i+1}")
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(DARK)
        wrap_text(c, ch_title, ML + 54, y - 10, TW - 54, "Helvetica-Bold", 14, DARK)
        y -= 52

        # Ligne accent
        c.setStrokeColor(RED)
        c.setLineWidth(1.5)
        c.line(ML, y, W - MR, y)
        y -= 14

        # Durée
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(LGRAY)
        c.drawString(ML, y, "Duree estimee : 45 - 60 secondes  |  Format : Vertical 9:16")
        y -= 18

        # Contenu découpé en sections
        content_text = clean(ch.content or "")
        lines = [l.strip() for l in content_text.split('.') if len(l.strip()) > 5]
        total = len(lines)

        accroche = '. '.join(lines[:max(1, total//5)])
        developpement = '. '.join(lines[max(1, total//5):max(2, total*3//4)])
        cta_text = '. '.join(lines[max(2, total*3//4):]) or "Abonne-toi pour plus de conseils !"
        hashtags = "#tiktok #business #afrique #viral #conseils #argent"

        # ACCROCHE
        y = section_badge("ACCROCHE  (0 - 3 secondes)", y, RED)
        ah = text_height(c, accroche, TW - 20, "Helvetica-Bold", 11)
        wrap_text(c, accroche, ML + 10, y, TW - 20, "Helvetica-Bold", 11, DARK)
        y -= ah + 14

        # DÉVELOPPEMENT
        y = section_badge("DEVELOPPEMENT  (3 - 45 secondes)", y, CYAN)
        dh = text_height(c, developpement, TW - 20, "Helvetica", 10, 3)
        wrap_text(c, developpement, ML + 10, y, TW - 20, "Helvetica", 10, DARK, 3)
        y -= dh + 14

        # CTA
        y = section_badge("APPEL A L'ACTION  (45 - 60 secondes)", y, colors.HexColor("#1A1A2E"))
        cth = text_height(c, cta_text, TW - 20, "Helvetica-Bold", 10)
        wrap_text(c, cta_text, ML + 10, y, TW - 20, "Helvetica-Bold", 10, DARK)
        y -= cth + 14

        # HASHTAGS
        y = section_badge("HASHTAGS", y, colors.HexColor("#333355"))
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(RED)
        c.drawString(ML + 10, y, hashtags)
        y -= 20

    # PAGE FINALE — CTA
    y = new_page("POINTS CLES")
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(DARK)
    c.drawString(ML, y, "Points Cles")
    y -= 20
    c.setStrokeColor(AC)
    c.setLineWidth(3)
    c.line(ML, y, ML + 30, y)
    y -= 14

    for k in (content.key_takeaways or []):
        kt = clean(k)
        if not kt:
            continue
        kh = text_height(c, kt, TW - 16, "Helvetica", 10)
        c.setStrokeColor(AC)
        c.setLineWidth(3)
        c.line(ML, y, ML, y - kh - 4)
        wrap_text(c, kt, ML + 12, y, TW - 16, "Helvetica", 10, DARK)
        y -= kh + 14

    y -= 10
    y = draw_cta_box(c, content.call_to_action or "Commence a filmer maintenant !", price, y, AC)
    draw_brand_footer(c, y - 10, AC)

    c.save()
    buf.seek(0)
    return buf.read()
