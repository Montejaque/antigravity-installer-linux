from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, HRFlowable
import re

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"docs/GUIA_USUARIO.md"
OUT=ROOT/"dist/Guia-Ayuda-Antigravity.pdf"
YELLOW=colors.HexColor("#F3D54E")
DARK=colors.HexColor("#252525")
MUTED=colors.HexColor("#646464")

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def build():
    regular=ROOT/"assets/fonts/Inter-Regular.ttf"
    bold=ROOT/"assets/fonts/Inter-Bold.ttf"
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("Inter",str(regular)))
        pdfmetrics.registerFont(TTFont("Inter-Bold",str(bold)))
        normal,strong="Inter","Inter-Bold"
    else:
        normal,strong="Helvetica","Helvetica-Bold"
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CoverX",fontName=strong,fontSize=24,leading=29,textColor=DARK,spaceAfter=8))
    styles.add(ParagraphStyle(name="SubX",fontName=normal,fontSize=9,leading=13,textColor=MUTED,spaceAfter=12))
    styles.add(ParagraphStyle(name="HeadX",fontName=strong,fontSize=12,leading=16,textColor=DARK,spaceBefore=10,spaceAfter=5,keepWithNext=True))
    styles.add(ParagraphStyle(name="BodyX",fontName=normal,fontSize=8.5,leading=12,textColor=DARK,spaceAfter=4))
    styles.add(ParagraphStyle(name="BulletX",fontName=normal,fontSize=8.2,leading=11,leftIndent=12,firstLineIndent=-8,spaceAfter=3))
    story=[Paragraph("ANTIGRAVITY INSTALLER",styles["CoverX"]),Paragraph("GUÍA DE AYUDA · LINUX x86_64 · VERSIÓN 1.1.3<br/>PUNTO VUELA MONTEJAQUE",styles["SubX"]),HRFlowable(width="100%",thickness=4,color=YELLOW,spaceAfter=12)]
    for raw in SOURCE.read_text(encoding="utf-8").splitlines():
        line=raw.strip()
        if not line or line.startswith("# ") or line.startswith("**Punto Vuela"): continue
        if line.startswith("## "):
            story.append(Paragraph(esc(line[3:]),styles["HeadX"])); continue
        if line.startswith("- "):
            story.append(Paragraph("• "+esc(line[2:].replace("`","")),styles["BulletX"])); continue
        if line.startswith("```"): continue
        line=re.sub(r"\*\*(.*?)\*\*",r"\1",line).replace("`","")
        story.append(Paragraph(esc(line),styles["BodyX"]))
    OUT.parent.mkdir(parents=True,exist_ok=True)
    doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=20*mm,bottomMargin=20*mm,title="Guía de ayuda · Antigravity Installer",author="Francisco Javier Gallego Orellana · Punto Vuela Montejaque")
    def footer(canvas,document):
        canvas.saveState()
        w,h=A4
        canvas.setFillColor(YELLOW); canvas.rect(0,h-5*mm,w,5*mm,stroke=0,fill=1)
        canvas.setFont(normal,7); canvas.setFillColor(MUTED)
        canvas.drawString(18*mm,9*mm,"Punto Vuela Montejaque · montejaque@puntosvuela.es")
        canvas.drawRightString(w-18*mm,9*mm,str(document.page))
        canvas.restoreState()
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    print(OUT)

if __name__=="__main__": build()
