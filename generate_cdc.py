#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cahier des charges Terra Sana — version améliorée.
Améliorations : présentation ASBL, MoSCoW, maquettes, tests, signatures.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, NextPageTemplate,
    Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Image,
)
import os
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.graphics.shapes import (
    Drawing, Rect, Ellipse, Line, String, Circle, Polygon,
)
from reportlab.graphics import renderPDF

W, H = A4
ML = 2.5 * cm
MR = 2.5 * cm
CW = W - ML - MR   # ~16.2 cm

# ─────────────────────────────────────────────────────────────
# Couleurs
# ─────────────────────────────────────────────────────────────
GREEN_D = colors.HexColor("#2D6A4F")
GREEN_L = colors.HexColor("#74C69D")
GOLD    = colors.HexColor("#D4A017")
CREAM   = colors.HexColor("#F8F4E3")
C_GRAY  = colors.Color(0.88, 0.88, 0.88)
C_LGRAY = colors.Color(0.95, 0.95, 0.95)
C_WHITE = colors.white

# ─────────────────────────────────────────────────────────────
# Pied de page
# ─────────────────────────────────────────────────────────────
def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8.5)
    y = 1.5 * cm
    canvas.drawString(ML, y, f"p. {doc.page}")
    canvas.drawCentredString(W / 2, y, "Youndjeu Tchouapi Alain")
    canvas.drawRightString(W - MR, y, "EAFC Uccle")
    canvas.restoreState()

def _no_footer(canvas, doc): pass

# ─────────────────────────────────────────────────────────────
# Styles
# ─────────────────────────────────────────────────────────────
def S(name, **kw):
    d = dict(fontName="Helvetica", fontSize=10, leading=14)
    d.update(kw)
    return ParagraphStyle(name, **d)

CV_SCHOOL = S("csch", fontName="Helvetica-Bold", fontSize=14, leading=18, alignment=TA_CENTER)
CV_YEAR   = S("cyr",  fontSize=11, leading=15, alignment=TA_CENTER)
CV_TITLE  = S("ctit", fontName="Helvetica-Bold", fontSize=20, leading=26, alignment=TA_CENTER)
CV_SUB    = S("csub", fontSize=11, leading=15, alignment=TA_CENTER)
CV_MOD    = S("cmod", fontName="Helvetica-Bold", fontSize=13, leading=17, alignment=TA_CENTER)
CV_EXT    = S("cext", fontSize=10.5, leading=14, alignment=TA_CENTER)
CV_INFO   = S("cinf", fontSize=10.5, leading=16, alignment=TA_CENTER)
CV_INST   = S("cins", fontName="Helvetica-Bold", fontSize=12, leading=16, alignment=TA_CENTER)

TOC_H = S("toch", fontName="Helvetica-Bold", fontSize=12, leading=17, spaceAfter=10)
BODY  = S("body", alignment=TA_JUSTIFY, spaceAfter=7, leading=14)
BULL  = S("bull", leftIndent=16, spaceAfter=4, leading=14)
ITAL  = S("ital", fontName="Helvetica-Oblique", fontSize=9, leading=12, spaceAfter=5)
NOTE  = S("note", fontName="Helvetica-Oblique", fontSize=9, leading=12, spaceAfter=5, leftIndent=8)
SEC1  = S("s1",  fontName="Helvetica-Bold", fontSize=12, leading=16, spaceBefore=10, spaceAfter=7)
SEC2  = S("s2",  fontName="Helvetica-Bold", fontSize=10.5, leading=14, spaceBefore=8, spaceAfter=5)
SEC2B = S("s2b", fontName="Helvetica-Bold", fontSize=10, leading=13, spaceBefore=5, spaceAfter=4)
TH    = S("th",  fontName="Helvetica-Bold", fontSize=9, leading=12)
TB    = S("tb",  fontSize=9, leading=12)
WF    = S("wf",  fontSize=8, leading=10, alignment=TA_CENTER)
WFB   = S("wfb", fontName="Helvetica-Bold", fontSize=8, leading=10, alignment=TA_CENTER)
WFL   = S("wfl", fontSize=7.5, leading=10, alignment=TA_LEFT)

# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────
def th(t): return Paragraph(t, TH)
def tb(t): return Paragraph(t, TB)
def wf(t): return Paragraph(t, WF)
def wfb(t): return Paragraph(t, WFB)
def wfl(t): return Paragraph(t, WFL)
def sp(h=0.3): return Spacer(1, h * cm)

def grid(cw, data, hdr=1):
    t = Table(data, colWidths=cw, repeatRows=hdr)
    t.setStyle(TableStyle([
        ("FONTNAME",      (0,0),    (-1, hdr-1), "Helvetica-Bold"),
        ("FONTNAME",      (0,hdr),  (-1,-1),      "Helvetica"),
        ("FONTSIZE",      (0,0),    (-1,-1),       9),
        ("LEADING",       (0,0),    (-1,-1),       12),
        ("GRID",          (0,0),    (-1,-1),       0.5, colors.black),
        ("VALIGN",        (0,0),    (-1,-1),       "TOP"),
        ("TOPPADDING",    (0,0),    (-1,-1),       4),
        ("BOTTOMPADDING", (0,0),    (-1,-1),       4),
        ("LEFTPADDING",   (0,0),    (-1,-1),       5),
        ("RIGHTPADDING",  (0,0),    (-1,-1),       5),
    ]))
    return t

PC = 1.0 * cm  # colonne page dans TDM

def toc_line(label, page, level=1):
    bold   = (level == 1)
    fn     = "Helvetica-Bold" if bold else "Helvetica"
    fs     = 10
    indent = 0.0 if level == 1 else 18.0
    page_str = str(page)
    avail  = CW - indent - PC - 4
    lw     = stringWidth(label, fn, fs)
    dw     = stringWidth(".", fn, fs)
    n      = max(3, int((avail - lw - stringWidth(" ", fn, fs)) / dw))
    left   = label + " " + "." * n
    ls = S("ls", fontName=fn, fontSize=fs, leading=14)
    rs = S("rs", fontName=fn, fontSize=fs, leading=14, alignment=TA_RIGHT)
    t = Table([[Paragraph(left, ls), Paragraph(page_str, rs)]],
              colWidths=[CW - PC, PC])
    t.setStyle(TableStyle([
        ("LEFTPADDING",  (0,0),(0,0), indent),
        ("RIGHTPADDING", (0,0),(0,0), 2),
        ("LEFTPADDING",  (1,0),(1,0), 2),
        ("RIGHTPADDING", (1,0),(1,0), 0),
        ("TOPPADDING",   (0,0),(-1,-1), 1.5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 1.5),
        ("VALIGN",       (0,0),(-1,-1), "BOTTOM"),
    ]))
    return t

# ─────────────────────────────────────────────────────────────
# UML diagram helpers
# ─────────────────────────────────────────────────────────────
_BLK = colors.black
_GRN = colors.HexColor("#2D6A4F")
_GRL = colors.HexColor("#E8F5ED")
_WHT = colors.white
_GRY = colors.HexColor("#AAAAAA")

def _ds(d, x, y, t, anchor='middle', fs=7.5, bold=False, col=None):
    fn = "Helvetica-Bold" if bold else "Helvetica"
    d.add(String(x, y, t, textAnchor=anchor, fontSize=fs,
                 fontName=fn, fillColor=col or _BLK))

def _dl(d, x1, y1, x2, y2, dash=None, w=0.8, col=None):
    kw = dict(strokeColor=col or _BLK, strokeWidth=w, fillColor=None)
    if dash:
        kw['strokeDashArray'] = dash
    d.add(Line(x1, y1, x2, y2, **kw))

def _dr(d, x, y, w, h, fill=_WHT, stroke=_BLK, sw=0.9):
    d.add(Rect(x, y, w, h, fillColor=fill, strokeColor=stroke, strokeWidth=sw))

def _actor(d, cx, cy, name):
    """UML stick figure; cy = vertical centre of body."""
    r = 9
    d.add(Circle(cx, cy+28, r, fillColor=_WHT, strokeColor=_BLK, strokeWidth=0.9))
    _dl(d, cx, cy+19, cx, cy+3)
    _dl(d, cx-14, cy+15, cx+14, cy+15)
    _dl(d, cx, cy+3, cx-11, cy-15)
    _dl(d, cx, cy+3, cx+11, cy-15)
    _ds(d, cx, cy-29, name, fs=7.5, bold=True)

def _uc(d, cx, cy, text, rx=70, ry=18):
    """Use-case ellipse with wrapped text."""
    d.add(Ellipse(cx, cy, rx, ry, fillColor=_GRL, strokeColor=_GRN, strokeWidth=1))
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        lines = lines if len(t) <= 22 else (lines + [cur])
        cur = t if len(t) <= 22 else w
    if cur:
        lines.append(cur)
    if len(lines) == 1:
        _ds(d, cx, cy-3, lines[0])
    elif len(lines) == 2:
        _ds(d, cx, cy+4, lines[0])
        _ds(d, cx, cy-7, lines[1])
    else:
        for i, ln in enumerate(lines[:3]):
            _ds(d, cx, cy+6-i*10, ln, fs=7)

def _class_box(d, x, top_y, title, attrs, methods=None, w=128):
    """UML class compartment box; (x, top_y) = top-left corner."""
    nh = 18
    ah = len(attrs) * 11 + 7
    mh = (len(methods) * 11 + 7) if methods else 0
    # name
    _dr(d, x, top_y - nh, w, nh, fill=_GRN)
    _ds(d, x + w/2, top_y - nh + 4, title, bold=True, col=_WHT)
    # attributes
    _dr(d, x, top_y - nh - ah, w, ah)
    for i, a in enumerate(attrs):
        _ds(d, x + 4, top_y - nh - 10 - i*11, a, anchor='start', fs=6.5)
    # methods (optional)
    if methods:
        _dr(d, x, top_y - nh - ah - mh, w, mh)
        for i, m in enumerate(methods):
            _ds(d, x + 4, top_y - nh - ah - 10 - i*11, m, anchor='start', fs=6.5)
    return nh + ah + mh  # total height

def _arr_open(d, x, y, direction='up'):
    """Hollow triangle arrowhead (generalization / inheritance)."""
    if direction == 'up':
        pts = [x, y, x-6, y-10, x+6, y-10]
    else:
        pts = [x, y, x-6, y+10, x+6, y+10]
    d.add(Polygon(pts, fillColor=_WHT, strokeColor=_BLK, strokeWidth=0.8))

def _arr_v(d, x, y, direction='up'):
    """Open V arrowhead (dependency: «include» / «extend»)."""
    if direction == 'up':
        _dl(d, x, y, x-5, y-8, w=0.7); _dl(d, x, y, x+5, y-8, w=0.7)
    else:
        _dl(d, x, y, x-5, y+8, w=0.7); _dl(d, x, y, x+5, y+8, w=0.7)

def _card(d, x, y, text):
    """Cardinality label near a relationship line."""
    _ds(d, x, y, text, fs=6.5, col=colors.HexColor("#333333"))

# ─── Use-case diagram ────────────────────────────────────────
def diag_use_case():
    DW, DH = 459, 575
    d = Drawing(DW, DH)
    _dr(d, 0, 0, DW, DH, fill=_WHT, stroke=None)

    # System boundary
    SX, SY, SW, SH = 72, 12, 318, 548
    _dr(d, SX, SY, SW, SH, sw=1.5)
    _ds(d, SX+SW/2, SY+SH-13,
        "Système — Module Bénévoles & Événements", bold=True, fs=8)

    # Vertical divider
    mid = SX + SW//2
    _dl(d, mid, SY+22, mid, SY+SH-24, dash=[4,3], w=0.5, col=_GRY)
    _ds(d, SX + SW//4,      SY+24, "Côté bénévole", fs=6.5, bold=True, col=_GRN)
    _ds(d, SX + 3*SW//4,    SY+24, "Administration", fs=6.5, bold=True, col=_GRN)

    # Left use cases
    LX = SX + SW//4
    l_ucs = [
        (LX, 522, "Consulter le site vitrine"),
        (LX, 468, "Consulter les événements"),
        (LX, 414, "Créer un compte"),
        (LX, 360, "Se connecter"),
        (LX, 306, "Gérer son profil"),
        (LX, 252, "S'inscrire à un événement"),
        (LX, 198, "Rejoindre la liste d'attente"),
        (LX, 144, "Consulter son historique"),
        (LX, 90,  "Télécharger une attestation"),
        (LX, 36,  "Laisser un avis"),
    ]
    for cx, cy, txt in l_ucs:
        _uc(d, cx, cy, txt, rx=66, ry=17)

    # Right use cases
    RX = SX + 3*SW//4
    r_ucs = [
        (RX, 506, "Se connecter (admin)"),
        (RX, 430, "Gérer les événements"),
        (RX, 354, "Valider / refuser inscriptions"),
        (RX, 278, "Envoyer emails groupés"),
        (RX, 202, "Gérer les bénévoles"),
        (RX, 126, "Consulter le dashboard"),
        (RX, 50,  "Exporter liste inscrits"),
    ]
    for cx, cy, txt in r_ucs:
        _uc(d, cx, cy, txt, rx=66, ry=17)

    # Actors
    _actor(d, 36, 470, "Visiteur")
    _actor(d, 36, 200, "Bénévole")
    # Généralisation Bénévole → Visiteur (trait plein + triangle creux :
    # un bénévole est un visiteur authentifié)
    _dl(d, 36, 240, 36, 428, w=0.9)
    _arr_open(d, 36, 438, 'up')
    _ds(d, 60, 336, "(est un)", fs=5.5, col=_GRY)

    _actor(d, 432, 290, "Administrateur")

    # Associations
    for _, cy, _ in l_ucs[:2]:
        _dl(d, 50, 488, LX-66, cy, w=0.6)
    for _, cy, _ in l_ucs[2:]:
        _dl(d, 50, 218, LX-66, cy, w=0.6)
    for _, cy, _ in r_ucs:
        _dl(d, 414, 308, RX+66, cy, w=0.6)

    # Relation «extend» : Rejoindre la liste d'attente ↦ S'inscrire à un
    # événement (comportement optionnel, déclenché si l'événement est complet)
    _dl(d, LX, 215, LX, 233, dash=[3,2], w=0.7)
    _arr_v(d, LX, 235, 'up')
    _ds(d, LX+32, 227, "«extend»", fs=5.8, col=_GRN)

    # Relation «include» : Valider/refuser inscriptions ↦ Envoyer emails
    # (chaque validation/refus déclenche systématiquement une notification)
    _dl(d, RX, 337, RX, 297, dash=[3,2], w=0.7)
    _arr_v(d, RX, 295, 'down')
    _ds(d, RX+34, 318, "«include»", fs=5.8, col=_GRN)

    return d

# ─── Class diagram : image fournie par l'auteur ──────────────
_CLASS_IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "assets", "diagramme_classes.png")

def img_classes(max_h=600):
    """Diagramme de classes (image de l'auteur), mis à l'échelle."""
    from reportlab.lib.utils import ImageReader
    iw, ih = ImageReader(_CLASS_IMG).getSize()
    ratio = ih / iw
    w = CW
    h = w * ratio
    if h > max_h:                  # limité par la hauteur disponible
        h = max_h
        w = h / ratio
    return Image(_CLASS_IMG, width=w, height=h)

# ─────────────────────────────────────────────────────────────
# Construction
# ─────────────────────────────────────────────────────────────
def build():
    out = "/home/user/portfolio-alain/CDC_TFE_Terra_Sana_Alain_modifie.pdf"

    cov_fr = Frame(ML, 2.0*cm, CW, H-4.0*cm, id="cover")
    nor_fr = Frame(ML, 2.5*cm, CW, H-5.0*cm, id="normal")

    doc = BaseDocTemplate(out, pagesize=A4,
        leftMargin=ML, rightMargin=MR,
        topMargin=2.5*cm, bottomMargin=2.5*cm)
    doc.addPageTemplates([
        PageTemplate(id="Cover",  frames=[cov_fr], onPage=_no_footer),
        PageTemplate(id="Normal", frames=[nor_fr], onPage=_footer),
    ])

    S_ = []   # story

    # ═══════════════════════════════════════════════════════
    # P1 — COUVERTURE
    # ═══════════════════════════════════════════════════════
    S_.append(Spacer(1, 1.8*cm))
    S_.append(Paragraph("Bachelier en Informatique de Gestion", CV_SCHOOL))
    S_.append(sp(0.3))
    S_.append(Paragraph("3ème année", CV_YEAR))
    S_.append(Spacer(1, 2.0*cm))
    S_.append(Paragraph("Cahier des charges", CV_TITLE))
    S_.append(sp(0.4))
    S_.append(Paragraph("Travail de Fin d'Études — Épreuve intégrée", CV_SUB))
    S_.append(Spacer(1, 1.8*cm))
    S_.append(Paragraph("Module de gestion des bénévoles et des événements", CV_MOD))
    S_.append(sp(0.3))
    S_.append(Paragraph("Extension du site web vitrine de Terra Sana ASBL", CV_EXT))
    S_.append(Spacer(1, 2.5*cm))
    S_.append(Paragraph("Encadreur scolaire : Marie-Christine Namur", CV_INFO))
    S_.append(sp(0.2))
    S_.append(Paragraph("Maître de stage : Didier Seraye", CV_INFO))
    S_.append(sp(0.2))
    S_.append(Paragraph("Travail présenté par Youndjeu Tchouapi Alain", CV_INFO))
    S_.append(Spacer(1, 2.5*cm))
    S_.append(Paragraph("<b>EAFC Uccle</b>", CV_INST))
    S_.append(sp(0.3))
    S_.append(Paragraph("2025-2026", CV_YEAR))
    S_.append(NextPageTemplate("Normal"))
    S_.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P2 — TABLE DES MATIÈRES
    # ═══════════════════════════════════════════════════════
    S_.append(Paragraph("Table des matières", TOC_H))
    toc = [
        ("1. Introduction",                                        3,  1),
        ("2. Fonctionnalités développées durant le stage",         4,  1),
        ("2.1 Contexte et objectif",                               4,  2),
        ("2.2 Site public — 12 pages",                             4,  2),
        ("2.3 Espace administrateur",                               4,  2),
        ("2.4 API REST Backend — 17 endpoints",                    4,  2),
        ("2.5 Base de données existante — 4 tables",               6,  2),
        ("2.6 Technologies utilisées",                             6,  2),
        ("3. Nouvelles fonctionnalités TFE",                       7,  1),
        ("3.1 Refonte graphique",                                  7,  2),
        ("3.2 Espace personnel bénévole",                          7,  2),
        ("3.3 Gestion des événements — côté administrateur",       8,  2),
        ("3.4 Inscription aux événements — côté bénévole",         8,  2),
        ("3.5 Retours post-événement",                             9,  2),
        ("3.6 Dashboard administrateur enrichi",                   9,  2),
        ("3.7 Fonctionnalités avancées",                           9,  2),
        ("3.8 Export PDF et attestation",                          9,  2),
        ("4. Analyse technique",                                   10,  1),
        ("4.1 Nouvelles tables de la base de données",            10,  2),
        ("4.2 Nouveaux endpoints API REST",                       12,  2),
        ("4.3 Nouvelles pages frontend",                          14,  2),
        ("4.4 Diagramme de cas d'utilisation",                    15,  2),
        ("4.5 Diagramme de classes",                              16,  2),
        ("5. Répartition des tâches / Apport personnel",          17,  1),
        ("5.1 Travail réalisé durant le stage",                   17,  2),
        ("5.2 Travail à réaliser dans le cadre du TFE",           17,  2),
        ("5.3 Tableau récapitulatif",                             18,  2),
        ("6. Plan de travail",                                    19,  1),
        ("6.1 Calendrier officiel",                               19,  2),
        ("6.2 Plan de développement",                             19,  2),
        ("6.3 Dates clés personnelles",                           19,  2),
        ("6.4 Contraintes et risques identifiés",                 20,  2),
    ]
    for label, page, level in toc:
        S_.append(toc_line(label, page, level))
    S_.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P3 — 1. INTRODUCTION
    # ═══════════════════════════════════════════════════════
    S_.append(Paragraph("1. Introduction", SEC1))

    S_.append(Paragraph("<b>Présentation de Terra Sana ASBL</b>", SEC2B))
    S_.append(Paragraph(
        "Terra Sana ASBL est une association sans but lucratif belge dont le siège social est "
        "situé au 19 avenue des Volontaires à Auderghem. L'association œuvre dans les domaines "
        "de la santé naturelle, de l'alimentation saine et du bien-être global. Elle organise "
        "régulièrement des ateliers, des conférences et des activités communautaires, animés en "
        "grande partie par des bénévoles engagés. Pour gérer ses différents pôles d'activité, "
        "l'association dispose de 12 applications internes spécialisées, dont l'accès est "
        "centralisé depuis le site web développé durant le stage.", BODY))
    S_.append(Paragraph(
        "Avant le stage, Terra Sana ne possédait aucune présence numérique. La communication "
        "avec les bénévoles et le public se faisait exclusivement par téléphone et par email, "
        "et la gestion administrative reposait entièrement sur des fichiers Excel et des "
        "documents papier.", BODY))

    S_.append(Paragraph("<b>Contexte du TFE</b>", SEC2B))
    S_.append(Paragraph(
        "Le présent document constitue le cahier des charges de mon Travail de Fin d'Études, "
        "réalisé dans le cadre de l'épreuve intégrée du Bachelier en Informatique de Gestion "
        "(3ème année) à l'EAFC Uccle, pour l'année académique 2025-2026.", BODY))
    S_.append(Paragraph(
        "Mon stage s'est déroulé au sein de Terra Sana ASBL du 25 mars au 20 mai 2026, sous la "
        "supervision de Monsieur Didier Seraye, Responsable Administratif. Durant cette période, "
        "j'ai conçu et développé de zéro un site web complet servant de vitrine institutionnelle "
        "et de hub centralisé pour les 12 applications internes de l'association.", BODY))
    S_.append(Paragraph(
        "Pour le TFE, je propose d'étendre ce projet en y intégrant un module complet de gestion "
        "des bénévoles et des événements. L'intégralité de ce module sera développée par mes "
        "soins, sans code préexistant. Le développement et la démonstration seront réalisés "
        "entièrement en environnement local (WAMP Server sous Windows).", BODY))

    S_.append(Paragraph("<b>Problématique</b>", SEC2B))
    S_.append(Paragraph(
        "Aujourd'hui, Terra Sana gère ses bénévoles et ses activités de façon entièrement "
        "manuelle. Cette organisation engendre plusieurs difficultés concrètes :", BODY))
    for b in [
        "des doublons et pertes d'information quand plusieurs personnes modifient les mêmes fichiers",
        "aucune vue d'ensemble des places disponibles, d'où des activités surchargées ou sous-remplies",
        "des confirmations et relances envoyées une à une, un travail répétitif et chronophage",
        "aucun historique de participation, ni moyen de remercier les bénévoles ou de leur délivrer une attestation",
    ]:
        S_.append(Paragraph(f"• {b}", BULL))
    S_.append(Paragraph(
        "Le module développé dans le cadre du TFE vise à centraliser et automatiser ces tâches : "
        "espace bénévole en ligne, gestion des événements avec places et liste d'attente, "
        "emails de confirmation automatiques et historique exploitable (niveaux, attestations). "
        "L'association gagne ainsi en temps et en fiabilité.", BODY))
    S_.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P4 — 2. FONCTIONNALITÉS STAGE
    # ═══════════════════════════════════════════════════════
    S_.append(Paragraph("2. Fonctionnalités développées durant le stage", SEC1))
    S_.append(Paragraph("2.1 Contexte et objectif", SEC2))
    S_.append(Paragraph(
        "L'association Terra Sana ASBL ne disposait d'aucune présence numérique avant le stage. "
        "L'objectif était de concevoir et développer un site web moderne, multilingue et évolutif, "
        "permettant de présenter l'association au public et de centraliser l'accès à ses "
        "12 applications internes via un hub de projets.", BODY))

    S_.append(Paragraph("2.2 Site public — 12 pages développées", SEC2))
    c2 = [3.8*cm, CW-3.8*cm]
    S_.append(grid(c2, [
        [th("Page"), th("Description")],
        [tb("Accueil"),         tb("Hero section, statistiques clés, aperçu des projets")],
        [tb("À propos"),        tb("Mission, valeurs, engagements de l'association")],
        [tb("Projets (Hub)"),   tb("Liste des 12 applications avec recherche et filtres")],
        [tb("Détail projet"),   tb("Page individuelle par application")],
        [tb("Blog"),            tb("Articles publiés par l'administrateur")],
        [tb("Contact"),         tb("Formulaire avec validation et compteur de caractères")],
        [tb("Bénévolat"),       tb("Formulaire de candidature bénévole")],
        [tb("Sponsors"),        tb("Présentation des partenaires")],
        [tb("Confidentialité"), tb("Politique de confidentialité")],
        [tb("Conditions"),      tb("Conditions générales d'utilisation")],
        [tb("Cookies"),         tb("Politique de gestion des cookies")],
        [tb("Aide / FAQ"),      tb("Questions fréquentes")],
    ]))
    S_.append(sp(0.3))
    S_.append(Paragraph("<i>Le site est entièrement multilingue FR / EN / NL avec sélecteur "
                        "de langue dans la barre de navigation.</i>", ITAL))

    S_.append(Paragraph("2.3 Espace administrateur — 2 pages sécurisées", SEC2))
    S_.append(grid(c2, [
        [th("Page"), th("Description")],
        [tb("Connexion (/login)"), tb("Authentification par identifiant + mot de passe, token JWT 24h")],
        [tb("Dashboard (/admin)"), tb("Gestion projets, articles de blog, messages reçus, changement de mot de passe")],
    ]))
    S_.append(Paragraph("2.4 API REST Backend — 17 endpoints", SEC2))
    S_.append(PageBreak())

    # P5 — endpoints existants
    cep = [2.3*cm, CW-5.5*cm, 3.0*cm]
    S_.append(grid(cep, [
        [th("Méthode"), th("Endpoint"), th("Accès")],
        [tb("POST"),   tb("/api/auth/login"),           tb("Public")],
        [tb("PUT"),    tb("/api/auth/changePassword"),  tb("Admin")],
        [tb("GET"),    tb("/api/projects"),             tb("Public")],
        [tb("GET"),    tb("/api/projects/{id}"),        tb("Public")],
        [tb("POST"),   tb("/api/projects"),             tb("Admin")],
        [tb("PUT"),    tb("/api/projects/{id}"),        tb("Admin")],
        [tb("DELETE"), tb("/api/projects/{id}"),        tb("Admin")],
        [tb("GET"),    tb("/api/posts"),                tb("Public")],
        [tb("GET"),    tb("/api/posts/{id}"),           tb("Public")],
        [tb("POST"),   tb("/api/posts"),                tb("Admin")],
        [tb("PUT"),    tb("/api/posts/{id}"),           tb("Admin")],
        [tb("DELETE"), tb("/api/posts/{id}"),           tb("Admin")],
        [tb("GET"),    tb("/api/contact"),              tb("Admin")],
        [tb("POST"),   tb("/api/contact"),              tb("Public")],
        [tb("PUT"),    tb("/api/contact/{id}/read"),    tb("Admin")],
        [tb("POST"),   tb("/api/contact/{id}/reply"),   tb("Admin")],
        [tb("DELETE"), tb("/api/contact/{id}"),         tb("Admin")],
    ]))
    S_.append(PageBreak())

    # P6 — 2.5 et 2.6
    S_.append(Paragraph("2.5 Base de données existante — 4 tables", SEC2))
    S_.append(grid([3.2*cm, CW-7.2*cm, 3.8*cm], [
        [th("Table"), th("Champs principaux"), th("Rôle")],
        [tb("admin"),           tb("id, username, password, role"), tb("Compte administrateur unique, mot de passe haché (BCrypt)")],
        [tb("project"),         tb("id, name, description, link, documentationLink, image, category, isActive, createdAt"), tb("Applications du hub")],
        [tb("blog_post"),       tb("id, title, content, image, isPublished, createdAt"), tb("Articles du blog")],
        [tb("contact_message"), tb("id, name, email, message, isRead, createdAt"), tb("Messages des visiteurs")],
    ]))
    S_.append(sp(0.4))
    S_.append(Paragraph("2.6 Technologies utilisées", SEC2))
    S_.append(grid([4.0*cm, 2.5*cm, CW-6.7*cm], [
        [th("Technologie"),        th("Version"), th("Usage")],
        [tb("React.js"),           tb("18.2.0"), tb("Frontend — pages, navigation, composants")],
        [tb("Spring Boot"),        tb("Java 21"), tb("Backend — API REST, logique métier")],
        [tb("Spring Security + JWT"), tb("0.11.5"), tb("Authentification et sécurisation")],
        [tb("MySQL"),              tb("9.1.0"),  tb("Base de données relationnelle")],
        [tb("BCrypt"),             tb("—"),      tb("Hachage sécurisé des mots de passe")],
        [tb("Git / GitHub"),       tb("—"),      tb("Versioning et hébergement du code source")],
        [tb("WAMP Server"),        tb("3.3.7"),  tb("Environnement local MySQL sous Windows")],
    ]))
    S_.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P7 — 3. NOUVELLES FONCTIONNALITÉS
    # ═══════════════════════════════════════════════════════
    S_.append(Paragraph("3. Nouvelles fonctionnalités TFE", SEC1))
    S_.append(Paragraph(
        "Dans le cadre de l'épreuve intégrée, le projet est étendu avec un module complet de "
        "gestion des bénévoles et des événements. Ce module est entièrement nouveau : aucune "
        "ligne de code n'existait pour ces fonctionnalités à la fin du stage.", BODY))

    S_.append(Paragraph("3.1 Refonte graphique du site", SEC2))
    S_.append(Paragraph(
        "Toutes les pages existantes et nouvelles seront redessinées avec une charte graphique "
        "cohérente, appliquée sur l'ensemble du site y compris l'espace administrateur.", BODY))
    S_.append(grid([4.0*cm, 3.5*cm, CW-7.7*cm], [
        [th("Rôle"),               th("Couleur"),    th("Code hexadécimal")],
        [tb("Couleur principale"), tb("Vert forêt"), tb("#2D6A4F")],
        [tb("Couleur secondaire"), tb("Vert clair"), tb("#74C69D")],
        [tb("Accent"),             tb("Or"),          tb("#D4A017")],
        [tb("Fond"),               tb("Blanc crème"), tb("#F8F4E3")],
        [tb("Texte"),              tb("Noir doux"),   tb("#1B1B1B")],
    ]))
    S_.append(sp(0.4))

    S_.append(Paragraph("3.2 Espace personnel bénévole", SEC2))
    S_.append(Paragraph("Nouvelles pages : /benevoles/inscription — /benevoles/connexion — /benevoles/mon-espace", NOTE))
    c2 = [4.0*cm, CW-4.0*cm]
    S_.append(grid(c2, [
        [th("Fonctionnalité"),       th("Description")],
        [tb("Création de compte"),   tb("Champs obligatoires : nom, prénom, email, mot de passe (haché BCrypt)")],
        [tb("Profil personnel"),     tb("Champs facultatifs : téléphone, date de naissance, ville et code postal, sexe, compétences, disponibilités, langue préférée (FR/EN/NL)")],
        [tb("Connexion sécurisée"),  tb("Token JWT dédié aux bénévoles, séparé du token administrateur")],
        [tb("Modification du profil"),tb("Le bénévole peut mettre à jour ses informations à tout moment")],
        [tb("Mot de passe oublié"),  tb("Email de réinitialisation avec token sécurisé (Gmail SMTP)")],
        [tb("Niveau bénévole"),      tb("Bronze (1-2 événements) / Argent (3-6) / Or (7+) — calculé automatiquement après chaque participation confirmée. Badge affiché sur le profil et notification email envoyée lors d'un changement de niveau.")],
        [tb("Déconnexion"),          tb("Expiration automatique du token après 24h")],
    ]))
    S_.append(sp(0.3))
    S_.append(Paragraph(
        "Conformément au principe de minimisation des données (RGPD), seules les informations "
        "strictement nécessaires à la création du compte sont obligatoires. Les autres champs "
        "restent facultatifs et servent uniquement à l'organisation des activités (localité), "
        "au contact (téléphone) et à l'assurance volontariat (date de naissance).", BODY))
    S_.append(PageBreak())

    # P8 — 3.3 et 3.4
    S_.append(Paragraph("3.3 Gestion des événements — côté administrateur", SEC2))
    S_.append(grid(c2, [
        [th("Fonctionnalité"),  th("Description")],
        [tb("Créer un événement"), tb("Titre, description, date, lieu, nombre de places, photo")],
        [tb("Gérer les statuts"),  tb("OPEN / FULL / CANCELLED / FINISHED")],
        [tb("Valider / refuser"),  tb("L'administrateur accepte ou refuse les inscriptions")],
        [tb("Email groupé"),       tb("Envoi d'un email à tous les bénévoles inscrits")],
        [tb("Supprimer"),          tb("Suppression avec confirmation")],
    ]))
    S_.append(sp(0.4))

    S_.append(Paragraph("3.4 Inscription aux événements — côté bénévole", SEC2))
    S_.append(grid(c2, [
        [th("Fonctionnalité"),  th("Description")],
        [tb("Consulter"),       tb("Liste des événements à venir avec date, lieu et places restantes")],
        [tb("S'inscrire"),      tb("Inscription avec email de confirmation automatique")],
        [tb("Se désinscrire"),  tb("Désinscription possible avant la date de l'événement")],
        [tb("Liste d'attente"), tb("Si complet : inscription en file d'attente (status = WAITING)")],
        [tb("Notification"),    tb("Email automatique si une place se libère (WAITING → CONFIRMED)")],
    ]))
    S_.append(PageBreak())

    # P9 — 3.5 à 3.8
    S_.append(Paragraph("3.5 Retours post-événement", SEC2))
    S_.append(grid(c2, [
        [th("Fonctionnalité"),        th("Description")],
        [tb("Laisser un avis"),       tb("Après un événement terminé : note de 1 à 5 étoiles + commentaire")],
        [tb("Consulter les retours"), tb("L'administrateur voit tous les avis depuis le dashboard")],
        [tb("Moyenne des notes"),     tb("Note moyenne affichée par événement")],
    ]))
    S_.append(sp(0.4))

    S_.append(Paragraph("3.6 Dashboard administrateur enrichi", SEC2))
    S_.append(grid(c2, [
        [th("Ajout"),                th("Description")],
        [tb("Onglet Événements"),    tb("Créer, modifier, gérer les statuts, voir les inscrits par événement")],
        [tb("Onglet Bénévoles"),     tb("Liste complète avec filtres (compétence, disponibilité, langue)")],
        [tb("Gestion inscriptions"), tb("Par événement : inscrits confirmés + liste d'attente")],
        [tb("Statistiques"),         tb("Nombre de bénévoles actifs, événements organisés, taux de participation")],
    ]))
    S_.append(sp(0.4))

    S_.append(Paragraph("3.7 Fonctionnalités avancées", SEC2))
    S_.append(grid([4.0*cm, CW-7.5*cm, 3.3*cm], [
        [th("Fonctionnalité"),        th("Description"),                                                th("Technologie")],
        [tb("Graphiques Chart.js"),   tb("Courbe des inscriptions par mois, taux de participation"),   tb("Chart.js")],
        [tb("Pagination"),            tb("Sur la liste des événements et des bénévoles"),              tb("Spring Boot Pageable")],
        [tb("Badge notification"),    tb("Nombre d'inscriptions en attente dans la navbar admin"),     tb("React + API")],
        [tb("Tri et filtres avancés"),tb("Filtrer les événements par date, statut, lieu"),             tb("Spring JPA Query")],
        [tb("Niveaux bénévole"),      tb("Bronze / Argent / Or calculé automatiquement"),              tb("Spring Boot")],
    ]))
    S_.append(sp(0.4))

    S_.append(Paragraph("3.8 Export PDF et attestation", SEC2))
    S_.append(grid([4.0*cm, CW-7.0*cm, 2.8*cm], [
        [th("Fonctionnalité"),        th("Description"),                                                             th("Accès")],
        [tb("Export liste inscrits"), tb("L'administrateur exporte en PDF la liste des bénévoles inscrits à un événement"), tb("Admin")],
        [tb("Attestation bénévole"),  tb("Le bénévole télécharge une attestation PDF de sa participation"),         tb("Bénévole")],
        [tb("Emails fonctionnels"),   tb("Confirmation, liste d'attente, groupe, réinitialisation — via Gmail SMTP"),tb("Automatique")],
    ]))
    S_.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P10 — 4.1 TABLES BD
    # ═══════════════════════════════════════════════════════
    S_.append(Paragraph("4. Analyse technique", SEC1))
    S_.append(Paragraph("4.1 Nouvelles tables de la base de données — 4 tables", SEC2))
    cbd = [3.3*cm, 3.0*cm, 3.2*cm, CW-9.7*cm]

    S_.append(Paragraph("Table app_users — Bénévoles", SEC2B))
    S_.append(grid(cbd, [
        [th("Champ"),           th("Type"),        th("Contrainte"),       th("Description")],
        [tb("id"),              tb("BIGINT"),      tb("PK, AUTO_INCREMENT"),tb("Identifiant unique")],
        [tb("firstName"),       tb("VARCHAR(100)"),tb("NOT NULL"),          tb("Prénom")],
        [tb("lastName"),        tb("VARCHAR(100)"),tb("NOT NULL"),          tb("Nom de famille")],
        [tb("email"),           tb("VARCHAR(200)"),tb("NOT NULL, UNIQUE"),  tb("Email de connexion")],
        [tb("password"),        tb("VARCHAR(255)"),tb("NOT NULL"),          tb("Mot de passe haché (BCrypt)")],
        [tb("phone"),           tb("VARCHAR(30)"), tb("NULL"),              tb("Numéro de téléphone (facultatif)")],
        [tb("birthDate"),       tb("DATE"),        tb("NULL"),              tb("Date de naissance (facultatif)")],
        [tb("gender"),          tb("VARCHAR(20)"), tb("NULL"),              tb("Sexe (facultatif)")],
        [tb("city"),            tb("VARCHAR(120)"),tb("NULL"),              tb("Ville (facultatif)")],
        [tb("postalCode"),      tb("VARCHAR(10)"), tb("NULL"),              tb("Code postal (facultatif)")],
        [tb("skills"),          tb("TEXT"),        tb("NULL"),              tb("Compétences")],
        [tb("availability"),    tb("VARCHAR(200)"),tb("NULL"),              tb("Disponibilités")],
        [tb("preferredLanguage"),tb("VARCHAR(5)"), tb("DEFAULT fr"),        tb("Langue préférée")],
        [tb("isActive"),        tb("BOOLEAN"),     tb("DEFAULT TRUE"),      tb("Compte actif ou désactivé")],
        [tb("resetToken"),      tb("VARCHAR(255)"),tb("NULL"),              tb("Token de réinitialisation")],
        [tb("resetTokenExpiry"),tb("DATETIME"),    tb("NULL"),              tb("Expiration du token")],
        [tb("createdAt"),       tb("DATETIME"),    tb("NOT NULL"),          tb("Date d'inscription")],
    ]))
    S_.append(sp(0.4))
    S_.append(Paragraph("Table events — Événements (début)", SEC2B))
    S_.append(grid(cbd, [
        [th("Champ"),    th("Type"),   th("Contrainte"),       th("Description")],
        [tb("id"),       tb("BIGINT"), tb("PK, AUTO_INCREMENT"),tb("Identifiant unique")],
        [tb("admin_id"), tb("BIGINT"), tb("FK → admin"),       tb("Administrateur créateur")],
    ]))
    S_.append(PageBreak())

    # P11
    S_.append(grid(cbd, [
        [th("Champ"),      th("Type"),          th("Contrainte"),   th("Description")],
        [tb("title"),      tb("VARCHAR(200)"),  tb("NOT NULL"),     tb("Titre de l'événement")],
        [tb("description"),tb("TEXT"),          tb("NOT NULL"),     tb("Description complète")],
        [tb("eventDate"),  tb("DATETIME"),      tb("NOT NULL"),     tb("Date et heure")],
        [tb("location"),   tb("VARCHAR(300)"),  tb("NOT NULL"),     tb("Lieu")],
        [tb("maxPlaces"),  tb("INT"),           tb("NOT NULL"),     tb("Nombre maximum de participants")],
        [tb("status"),     tb("VARCHAR(20)"),   tb("DEFAULT OPEN"), tb("OPEN / FULL / CANCELLED / FINISHED")],
        [tb("imageUrl"),   tb("VARCHAR(500)"),  tb("NULL"),         tb("Photo de l'événement")],
        [tb("createdAt"),  tb("DATETIME"),      tb("NOT NULL"),     tb("Date de création")],
    ]))
    S_.append(sp(0.4))
    S_.append(Paragraph("Table registrations — Inscriptions et liste d'attente", SEC2B))
    S_.append(grid(cbd, [
        [th("Champ"),    th("Type"),        th("Contrainte"),       th("Description")],
        [tb("id"),       tb("BIGINT"),      tb("PK, AUTO_INCREMENT"),tb("Identifiant unique")],
        [tb("user_id"),  tb("BIGINT"),      tb("FK → app_users"),   tb("Bénévole inscrit")],
        [tb("event_id"), tb("BIGINT"),      tb("FK → events"),      tb("Événement concerné")],
        [tb("status"),   tb("VARCHAR(20)"), tb("NOT NULL"),         tb("CONFIRMED / WAITING / PENDING / REFUSED")],
        [tb("position"), tb("INT"),         tb("NULL"),             tb("Position dans la file d'attente (si WAITING)")],
        [tb("createdAt"),tb("DATETIME"),    tb("NOT NULL"),         tb("Date d'inscription")],
    ]))
    S_.append(sp(0.4))
    S_.append(Paragraph("Table reviews — Retours post-événement", SEC2B))
    S_.append(grid(cbd, [
        [th("Champ"),    th("Type"),        th("Contrainte"),       th("Description")],
        [tb("id"),       tb("BIGINT"),      tb("PK, AUTO_INCREMENT"),tb("Identifiant unique")],
        [tb("user_id"),  tb("BIGINT"),      tb("FK → app_users"),   tb("Bénévole ayant laissé l'avis")],
        [tb("event_id"), tb("BIGINT"),      tb("FK → events"),      tb("Événement évalué")],
        [tb("rating"),   tb("INT"),         tb("NOT NULL (1-5)"),   tb("Note de 1 à 5 étoiles")],
        [tb("comment"),  tb("TEXT"),        tb("NULL"),             tb("Commentaire libre")],
        [tb("createdAt"),tb("DATETIME"),    tb("NOT NULL"),         tb("Date de l'avis")],
    ]))
    S_.append(PageBreak())

    # P12 — 4.2 endpoints (1)
    S_.append(Paragraph("4.2 Nouveaux endpoints API REST — 30 endpoints", SEC2))
    cep2 = [2.3*cm, CW-6.1*cm, 3.6*cm]

    S_.append(Paragraph("Bénévoles — authentification et profil", SEC2B))
    S_.append(grid(cep2, [
        [th("Méthode"), th("Endpoint"),                       th("Accès")],
        [tb("POST"),    tb("/api/benevoles/register"),        tb("Public")],
        [tb("POST"),    tb("/api/benevoles/login"),           tb("Public")],
        [tb("POST"),    tb("/api/benevoles/forgot-password"), tb("Public")],
        [tb("POST"),    tb("/api/benevoles/reset-password"),  tb("Public")],
        [tb("GET"),     tb("/api/benevoles/profile"),         tb("Bénévole connecté")],
        [tb("PUT"),     tb("/api/benevoles/profile"),         tb("Bénévole connecté")],
        [tb("PUT"),     tb("/api/benevoles/changePassword"),  tb("Bénévole connecté")],
        [tb("GET"),     tb("/api/benevoles/level"),           tb("Bénévole connecté")],
    ]))
    S_.append(sp(0.4))
    S_.append(Paragraph("Événements", SEC2B))
    S_.append(grid(cep2, [
        [th("Méthode"), th("Endpoint"),                th("Accès")],
        [tb("GET"),     tb("/api/events"),             tb("Public")],
        [tb("GET"),     tb("/api/events/{id}"),        tb("Public")],
        [tb("POST"),    tb("/api/events"),             tb("Admin")],
        [tb("PUT"),     tb("/api/events/{id}"),        tb("Admin")],
        [tb("DELETE"),  tb("/api/events/{id}"),        tb("Admin")],
        [tb("PUT"),     tb("/api/events/{id}/status"), tb("Admin")],
        [tb("POST"),    tb("/api/events/{id}/email"),  tb("Admin")],
    ]))
    S_.append(sp(0.4))
    S_.append(Paragraph("Inscriptions", SEC2B))
    S_.append(grid(cep2, [
        [th("Méthode"), th("Endpoint"),                             th("Accès")],
        [tb("POST"),    tb("/api/registrations/{eventId}"),         tb("Bénévole connecté")],
        [tb("DELETE"),  tb("/api/registrations/{eventId}"),         tb("Bénévole connecté")],
        [tb("GET"),     tb("/api/registrations/mes-inscriptions"),  tb("Bénévole connecté")],
        [tb("GET"),     tb("/api/registrations/event/{id}"),        tb("Admin")],
        [tb("PUT"),     tb("/api/registrations/{id}/validate"),     tb("Admin")],
        [tb("PUT"),     tb("/api/registrations/{id}/refuse"),       tb("Admin")],
    ]))
    S_.append(PageBreak())

    # P13 — 4.2 (suite)
    S_.append(Paragraph("Retours, export et statistiques", SEC2B))
    S_.append(grid(cep2, [
        [th("Méthode"), th("Endpoint"),                        th("Accès")],
        [tb("POST"),    tb("/api/reviews"),                    tb("Bénévole connecté")],
        [tb("GET"),     tb("/api/reviews/event/{id}"),         tb("Public")],
        [tb("GET"),     tb("/api/reviews/admin"),              tb("Admin")],
        [tb("GET"),     tb("/api/benevoles/attestation"),      tb("Bénévole connecté")],
        [tb("GET"),     tb("/api/admin/events/{id}/export"),   tb("Admin")],
        [tb("GET"),     tb("/api/admin/benevoles"),            tb("Admin")],
        [tb("GET"),     tb("/api/admin/stats/inscriptions"),   tb("Admin")],
        [tb("GET"),     tb("/api/admin/stats/participation"),  tb("Admin")],
        [tb("GET"),     tb("/api/admin/notifications/count"),  tb("Admin")],
    ]))
    S_.append(PageBreak())

    # P14 — 4.3
    S_.append(Paragraph("4.3 Nouvelles pages frontend — 7 pages", SEC2))
    S_.append(grid([5.0*cm, CW-9.0*cm, 3.8*cm], [
        [th("Route"),                          th("Page"),                                              th("Accès")],
        [tb("/benevoles/inscription"),          tb("Formulaire d'inscription bénévole"),               tb("Public")],
        [tb("/benevoles/connexion"),            tb("Connexion bénévole"),                              tb("Public")],
        [tb("/benevoles/mot-de-passe-oublie"), tb("Demande de réinitialisation du mot de passe"),     tb("Public")],
        [tb("/benevoles/reinitialiser"),        tb("Saisie du nouveau mot de passe (via lien email)"), tb("Public")],
        [tb("/benevoles/mon-espace"),           tb("Profil, historique, attestation, niveau bénévole"),tb("Bénévole connecté")],
        [tb("/evenements"),                     tb("Liste des événements avec filtres et pagination"),  tb("Public")],
        [tb("/evenements/:id"),                 tb("Détail d'un événement + inscription"),             tb("Public / Bénévole")],
    ]))
    S_.append(PageBreak())

    # P15 — 4.4 Diagramme de cas d'utilisation
    S_.append(Paragraph("4.4 Diagramme de cas d'utilisation", SEC2))
    S_.append(Paragraph(
        "Le diagramme ci-dessous représente les interactions entre les acteurs du système "
        "et les fonctionnalités offertes par le module TFE. Trois acteurs sont identifiés : "
        "le Visiteur (non authentifié), le Bénévole (qui étend le Visiteur) et l'Administrateur.", BODY))
    S_.append(sp(0.2))
    S_.append(diag_use_case())
    S_.append(PageBreak())

    # P16 — 4.5 Diagramme de classes
    S_.append(Paragraph("4.5 Diagramme de classes", SEC2))
    S_.append(Paragraph(
        "Le diagramme de classes présente les huit entités Java de l'application, leurs attributs "
        "(avec clés primaires «PK» et étrangères «FK»), leurs méthodes et leurs associations. Les "
        "entités AppUser, Event, Review et Registration sont créées dans le cadre du TFE ; Admin, "
        "Project, BlogPost et ContactMessage proviennent du site existant.", BODY))
    S_.append(sp(0.2))
    S_.append(img_classes(max_h=600))
    S_.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P17 — 5. RÉPARTITION DES TÂCHES
    # ═══════════════════════════════════════════════════════
    S_.append(Paragraph("5. Répartition des tâches / Apport personnel", SEC1))
    S_.append(Paragraph("5.1 Travail réalisé durant le stage — base technique existante", SEC2))
    S_.append(grid([3.8*cm, CW-6.8*cm, 2.8*cm], [
        [th("Composant"),               th("Description"),                                                           th("Statut")],
        [tb("Site public multilingue"), tb("12 pages React (Accueil, À propos, Projets, Blog, Contact, Bénévolat…)"),tb("Existant")],
        [tb("Hub des 12 applications"), tb("Affichage dynamique avec recherche et filtres par catégorie"),           tb("Existant")],
        [tb("Panel administrateur"),    tb("Dashboard complet : projets, blog, messages, changement de mot de passe"),tb("Existant")],
        [tb("Authentification JWT"),    tb("Connexion admin sécurisée avec BCrypt"),                                tb("Existant")],
        [tb("API REST backend"),        tb("17 endpoints sur 4 ressources"),                                         tb("Existant")],
        [tb("Base de données MySQL"),   tb("4 tables : admin, project, blog_post, contact_message"),                tb("Existant")],
        [tb("Envoi d'emails"),          tb("Réponse aux messages via Gmail SMTP"),                                   tb("Existant")],
    ]))
    S_.append(sp(0.4))
    S_.append(Paragraph("5.2 Travail à réaliser dans le cadre du TFE", SEC2))
    S_.append(Paragraph(
        "Tout ce qui suit sera développé entièrement par moi, à domicile. Aucune de ces "
        "fonctionnalités n'existait à la fin du stage.", BODY))
    ctfe = [3.8*cm, CW-7.8*cm, 3.8*cm]
    S_.append(grid(ctfe, [
        [th("Composant"),                th("Description"),                                               th("Technologie")],
        [tb("Refonte graphique"),        tb("Nouvelle charte sur toutes les pages (public + admin)"),    tb("React / CSS")],
        [tb("Espace bénévole"),          tb("Inscription, connexion, profil, mot de passe oublié, niveau"),tb("React + Spring Boot")],
        [tb("Gestion événements"),       tb("CRUD admin, email groupé, export PDF liste inscrits"),      tb("React + Spring Boot")],
        [tb("Page événements"),          tb("Liste publique avec filtres, pagination, détail"),          tb("React")],
        [tb("Système inscription"),      tb("Inscription + email de confirmation automatique"),          tb("Spring Boot + JavaMail")],
        [tb("Liste d'attente"),          tb("status = WAITING + position dans Registration"),            tb("Spring Boot")],
        [tb("Retours événement"),        tb("Formulaire d'avis (note + commentaire)"),                  tb("React + Spring Boot")],
        [tb("Dashboard enrichi"),        tb("Onglets bénévoles + événements + statistiques"),           tb("React + Spring Boot")],
        [tb("Graphiques Chart.js"),      tb("Dashboard admin : courbes et statistiques"),               tb("Chart.js")],
        [tb("Pagination"),               tb("Événements et liste bénévoles"),                           tb("Spring Pageable")],
        [tb("Badge notification"),       tb("Inscriptions en attente dans la navbar admin"),            tb("React + API")],
        [tb("Niveaux bénévole"),         tb("Bronze / Argent / Or calculé automatiquement"),            tb("Spring Boot")],
        [tb("Export PDF"),               tb("Attestation + liste inscrits par événement"),              tb("iText / JasperReports")],
        [tb("4 nouvelles tables BD"),    tb("app_users, events, registrations, reviews"),               tb("MySQL")],
        [tb("30 nouveaux endpoints"),    tb("API REST couvrant toutes les nouvelles fonctionnalités"),  tb("Spring Boot REST")],
        [tb("7 nouvelles pages"),        tb("Espace bénévole + pages événements"),                      tb("React")],
    ]))
    S_.append(PageBreak())

    # P18 — 5.3
    S_.append(Paragraph("5.3 Tableau récapitulatif", SEC2))
    S_.append(grid([4.5*cm, 2.5*cm, CW-7.2*cm], [
        [th("Critère"),            th("Stage"),   th("TFE (apport personnel)")],
        [tb("Tables BD"),          tb("4"),       tb("+4 nouvelles (8 au total)")],
        [tb("Endpoints API"),      tb("17"),      tb("+30 nouveaux (47 au total)")],
        [tb("Pages frontend"),     tb("14"),      tb("+7 nouvelles (21 au total)")],
        [tb("Pages redessinées"),  tb("0"),       tb("14 pages existantes refaites")],
        [tb("Module bénévoles"),   tb("Aucun"),   tb("Module complet (inscription, profil, niveaux)")],
        [tb("Gestion événements"), tb("Aucune"),  tb("Module complet (CRUD, inscriptions, retours)")],
    ]))
    S_.append(sp(0.4))
    S_.append(Paragraph(
        "Le travail réalisé durant le stage constitue la fondation technique du projet "
        "(architecture, base de données initiale, site public, panel administrateur). Le TFE "
        "consiste à étendre significativement cette base en y ajoutant un module entièrement "
        "nouveau, ainsi qu'une refonte complète de l'interface graphique. L'intégralité du module "
        "TFE est développée de zéro par l'étudiant.", BODY))
    S_.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P19 — 6. PLAN DE TRAVAIL
    # ═══════════════════════════════════════════════════════
    S_.append(Paragraph("6. Plan de travail", SEC1))
    S_.append(Paragraph("6.1 Calendrier officiel — 2ème session", SEC2))
    ccal = [3.0*cm, CW-3.0*cm]
    S_.append(grid(ccal, [
        [th("Date limite"), th("Échéance")],
        [tb("03/07/2026"),  tb("Remise du cahier des charges (PDF)")],
        [tb("28/08/2026"),  tb("Validation de l'analyse par l'encadreur scolaire")],
        [tb("15/09/2026"),  tb("Validation de l'application")],
        [tb("22/09/2026"),  tb("Remise du rapport écrit provisoire (PDF sur Teams)")],
        [tb("29/09/2026"),  tb("Remise du rapport écrit définitif (PDF + 5 exemplaires + GitHub)")],
        [tb("13/10/2026"),  tb("Défenses orales")],
    ]))
    S_.append(sp(0.4))
    S_.append(Paragraph("6.2 Plan de développement", SEC2))
    S_.append(grid([4.2*cm, CW-9.5*cm, 3.2*cm, 1.9*cm], [
        [th("Phase"),                             th("Contenu"),                                                   th("Période"),          th("Statut")],
        [tb("Phase 1 — Analyse & CDC"),            tb("Analyse de l'existant, rédaction du cahier des charges"),   tb("Mai – Juil. 2026"), tb("En cours")],
        [tb("Phase 2 — Refonte graphique"),        tb("Application de la charte sur toutes les pages"),            tb("Début juil. 2026"), tb("À faire")],
        [tb("Phase 3 — Backend"),                  tb("Entités Java, repositories, controllers, JWT, Gmail SMTP"), tb("Juillet 2026"),     tb("À faire")],
        [tb("Phase 4 — Frontend bénévoles"),       tb("Inscription, connexion, profil, mot de passe oublié"),      tb("Juil. – Août 2026"),tb("À faire")],
        [tb("Phase 5 — Frontend événements"),      tb("Liste, détail, inscription, retours"),                      tb("Août 2026"),        tb("À faire")],
        [tb("Phase 6 — Fonctionnalités avancées"), tb("Chart.js, pagination, badge, filtres, niveaux"),            tb("Août – Sept. 2026"),tb("À faire")],
        [tb("Phase 7 — Tests & corrections"),      tb("Tests complets, corrections, validation encadreur"),        tb("Septembre 2026"),   tb("À faire")],
        [tb("Phase 8 — Rapport & finalisation"),   tb("Rapport écrit, GitHub, 5 exemplaires, soutenance"),         tb("Sept. – Oct. 2026"),tb("À faire")],
    ]))
    S_.append(sp(0.4))
    S_.append(Paragraph("6.3 Dates clés personnelles", SEC2))
    S_.append(grid(ccal, [
        [th("Date"),       th("Action")],
        [tb("03/07/2026"), tb("Envoi du CDC finalisé à Madame Marie-Christine Namur")],
        [tb("28/08/2026"), tb("Présentation de l'analyse validée (schéma BD + architecture)")],
        [tb("15/09/2026"), tb("Application complète et fonctionnelle")],
        [tb("22/09/2026"), tb("Rapport provisoire soumis sur Teams")],
        [tb("29/09/2026"), tb("Rapport définitif + code GitHub + 5 exemplaires au secrétariat")],
        [tb("13/10/2026"), tb("Défense orale devant le jury")],
    ]))
    S_.append(PageBreak())

    # P20 — 6.4
    S_.append(Paragraph("6.4 Contraintes et risques identifiés", SEC2))
    S_.append(Paragraph(
        "Plusieurs contraintes techniques et organisationnelles ont été anticipées dès la phase "
        "d'analyse. Le tableau ci-dessous recense les principaux risques susceptibles d'affecter "
        "le projet, ainsi que les mesures concrètes prévues pour les limiter.", BODY))
    S_.append(grid([5.0*cm, CW-5.0*cm], [
        [th("Contrainte / Risque"), th("Mesure prévue")],
        [tb("Délai serré de la 2ème session\n(juillet à octobre 2026)"),
         tb("Découpage du travail en huit phases planifiées (point 6.2) afin de garantir les fonctionnalités essentielles en priorité.")],
        [tb("Dépendance au service Gmail SMTP pour l'envoi des e-mails"),
         tb("Utilisation d'un mot de passe d'application dédié ; en cas d'indisponibilité, les notifications restent consultables directement dans l'espace bénévole.")],
        [tb("Sécurité des données personnelles des bénévoles"),
         tb("Mots de passe chiffrés avec BCrypt, authentification par jeton JWT et contrôle des accès par rôle (administrateur / bénévole).")],
        [tb("Compatibilité navigateurs et affichage multilingue (FR/EN/NL)"),
         tb("Interface responsive testée sur les principaux navigateurs et relecture systématique des trois versions linguistiques avant la remise.")],
        [tb("Perte de code ou de données"),
         tb("Versionnage sur GitHub avec sauvegardes régulières et base de données exportée à chaque étape importante.")],
        [tb("Environnement de développement\net de démonstration"),
         tb("L'application est développée et présentée en environnement local (WAMP Server sous Windows). Aucun déploiement en ligne n'est prévu dans le cadre de ce TFE.")],
    ]))
    S_.append(PageBreak())

    doc.build(S_)
    print(f"PDF généré : {out}")

if __name__ == "__main__":
    build()
