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
    Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether,
)
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

def _uc(d, cx, cy, text, rx=70, ry=18, fs=7.5):
    """Use-case ellipse with wrapped text."""
    d.add(Ellipse(cx, cy, rx, ry, fillColor=_GRL, strokeColor=_GRN, strokeWidth=1))
    maxlen = round(22 * 7.5 / fs)
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        lines = lines if len(t) <= maxlen else (lines + [cur])
        cur = t if len(t) <= maxlen else w
    if cur:
        lines.append(cur)
    lh = fs + 2.5
    if len(lines) == 1:
        _ds(d, cx, cy-fs/2.5, lines[0], fs=fs)
    elif len(lines) == 2:
        _ds(d, cx, cy+lh/2-3, lines[0], fs=fs)
        _ds(d, cx, cy-lh/2-3, lines[1], fs=fs)
    else:
        for i, ln in enumerate(lines[:3]):
            _ds(d, cx, cy+lh-4-i*lh, ln, fs=fs-0.5)

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

def _arr_h(d, x, y, direction='right'):
    """Open V arrowhead pointing horizontally."""
    if direction == 'right':
        _dl(d, x, y, x-8, y-5, w=0.7); _dl(d, x, y, x-8, y+5, w=0.7)
    else:
        _dl(d, x, y, x+8, y-5, w=0.7); _dl(d, x, y, x+8, y+5, w=0.7)

def _card(d, x, y, text):
    """Cardinality label near a relationship line."""
    _ds(d, x, y, text, fs=6.5, col=colors.HexColor("#333333"))

# ─── Use-case diagram ────────────────────────────────────────
def _evenly(top, bottom, n):
    """n positions en y, régulièrement espacées entre top et bottom."""
    if n == 1:
        return [(top + bottom) / 2]
    step = (top - bottom) / (n - 1)
    return [top - i * step for i in range(n)]

def diag_use_case():
    DW, DH = 459, 592
    d = Drawing(DW, DH)
    _dr(d, 0, 0, DW, DH, fill=_WHT, stroke=None)

    # System boundary
    SX, SY, SW, SH = 72, 12, 318, 588
    top_edge = SY + SH
    _dr(d, SX, SY, SW, SH, sw=1.5)
    _ds(d, SX+SW/2, top_edge-13,
        "Système — Module Bénévoles & Événements", bold=True, fs=8)

    # Vertical divider
    mid = SX + SW//2
    header_y = top_edge - 32
    _dl(d, mid, SY+18, mid, header_y+10, dash=[4,3], w=0.5, col=_GRY)
    _ds(d, SX + SW//4,      header_y, "Côté bénévole", fs=6.5, bold=True, col=_GRN)
    _ds(d, SX + 3*SW//4,    header_y, "Administration", fs=6.5, bold=True, col=_GRN)

    ell_top, ell_bottom = header_y - 28, SY + 26

    # Left use cases (Visiteur : 0-2 ; Bénévole : 3-11, hérite de 0-2)
    # « Se connecter » et « Réinitialiser son mot de passe » appartiennent
    # au Bénévole : dès que le Visiteur les exécute, il devient Bénévole.
    LX = SX + SW//4
    l_labels = [
        "Consulter le site vitrine",
        "Consulter les événements",
        "Créer un compte",
        "Se connecter",
        "Réinitialiser son mot de passe",
        "Gérer son profil",
        "S'inscrire à un événement",
        "Rejoindre la liste d'attente",
        "Se désinscrire",
        "Consulter son historique",
        "Télécharger une attestation",
        "Laisser un avis",
    ]
    l_y = _evenly(ell_top, ell_bottom, len(l_labels))
    l_ucs = [(LX, y, t) for y, t in zip(l_y, l_labels)]
    for cx, cy, txt in l_ucs:
        _uc(d, cx, cy, txt, rx=64, ry=15, fs=6.6)

    # Right use cases (Administration) — l'admin gère aussi son propre
    # compte (mot de passe, profil), indépendamment de celui du bénévole
    RX = SX + 3*SW//4
    r_labels = [
        "Se connecter (admin)",
        "Réinitialiser son mot de passe (admin)",
        "Gérer son profil (admin)",
        "Gérer les événements",
        "Valider / refuser les inscriptions",
        "Envoyer un email de confirmation",
        "Envoyer des emails groupés",
        "Gérer les bénévoles",
        "Consulter le tableau de bord",
        "Exporter la liste des inscrits",
        "Consulter les avis",
    ]
    r_y = _evenly(ell_top, ell_bottom, len(r_labels))
    r_ucs = [(RX, y, t) for y, t in zip(r_y, r_labels)]
    for cx, cy, txt in r_ucs:
        _uc(d, cx, cy, txt, rx=66, ry=16, fs=6.6)

    # Actors
    v_cy = l_y[1]          # Visiteur : centré sur ses 3 cas d'utilisation
    b_cy = l_y[7]          # Bénévole : centré sur ses 9 cas d'utilisation
    a_cy = r_y[5]          # Administrateur : centré sur la colonne droite
    _actor(d, 36, v_cy, "Visiteur")
    _actor(d, 36, b_cy, "Bénévole")
    # Généralisation Bénévole → Visiteur (trait plein + triangle creux :
    # un bénévole est un visiteur authentifié)
    _dl(d, 36, b_cy+40, 36, v_cy-42, w=0.9)
    _arr_open(d, 36, v_cy-32, 'up')
    _ds(d, 60, (b_cy+v_cy)/2, "(est un)", fs=5.5, col=_GRY)

    _actor(d, 432, a_cy, "Administrateur")

    # Associations
    # Visiteur : consulter le site, consulter les événements, créer un compte
    for _, cy, _ in l_ucs[:3]:
        _dl(d, 50, v_cy+18, LX-64, cy, w=0.6)
    # Bénévole : se connecter et toutes les actions authentifiées
    for _, cy, _ in l_ucs[3:]:
        _dl(d, 50, b_cy+18, LX-64, cy, w=0.6)
    for _, cy, _ in r_ucs:
        _dl(d, 414, a_cy+18, RX+66, cy, w=0.6)

    # Relation «extend» : Rejoindre la liste d'attente ↦ S'inscrire à un
    # événement (comportement optionnel, déclenché si l'événement est complet)
    y_join, y_sub = l_y[7], l_y[6]
    _dl(d, LX, y_join+15, LX, y_sub-15, dash=[3,2], w=0.7)
    _arr_v(d, LX, y_sub-13, 'up')
    _ds(d, LX+32, (y_join+y_sub)/2, "«extend»", fs=5.8, col=_GRN)

    # Relation «include» : Valider/refuser inscriptions ↦ Envoyer un email
    # de confirmation (chaque décision déclenche systématiquement un email)
    y_valid, y_mail = r_y[4], r_y[5]
    _dl(d, RX, y_valid-16, RX, y_mail+16, dash=[3,2], w=0.7)
    _arr_v(d, RX, y_mail+14, 'down')
    _ds(d, RX+34, (y_valid+y_mail)/2, "«include»", fs=5.8, col=_GRN)

    return d

# ─── Class diagram : version vectorielle nette (noir & blanc) ─
def _cbox(d, x, top, title, attrs, methods=None, w=128, fs=6.5, rh=9, nh=14):
    """Boîte de classe UML classique (nom / attributs / méthodes),
    un seul contour, texte vectoriel toujours net."""
    ah = len(attrs) * rh + 6
    mh = (len(methods) * rh + 6) if methods else 0
    total = nh + ah + mh
    _dr(d, x, top - total, w, total, fill=_WHT, stroke=_BLK, sw=1.0)
    _ds(d, x + w/2, top - nh + 4, title, bold=True, fs=fs + 0.8)
    _dl(d, x, top - nh, x + w, top - nh, w=1.0)
    for i, a in enumerate(attrs):
        _ds(d, x + 4, top - nh - 8 - i*rh, a, anchor='start', fs=fs)
    if methods:
        _dl(d, x, top - nh - ah, x + w, top - nh - ah, dash=[2, 2], w=0.7)
        for i, m in enumerate(methods):
            _ds(d, x + 4, top - nh - ah - 8 - i*rh, m, anchor='start', fs=fs)
    return total

def _enumbox(d, x, top, name, values, w=78, fs=6.3, rh=7.5):
    """Boîte d'énumération UML : «enumeration» sur 1 ligne, nom en dessous,
    puis liste des valeurs. (x, top) = coin haut-gauche."""
    nh = 20  # entête sur 2 lignes (stéréotype + nom)
    vh = len(values) * rh + 6
    total = nh + vh
    _dr(d, x, top - total, w, total, fill=_WHT, stroke=_BLK, sw=1.0)
    _ds(d, x + w/2, top - 7, "«enumeration»", fs=fs, col=_GRY)
    _ds(d, x + w/2, top - 16, name, bold=True, fs=fs + 0.6)
    _dl(d, x, top - nh, x + w, top - nh, w=1.0)
    for i, v in enumerate(values):
        _ds(d, x + 4, top - nh - 8 - i*rh, v, anchor='start', fs=fs)
    return total

def diag_classes():
    DW, DH = 459, 665
    d = Drawing(DW, DH)
    _dr(d, 0, 0, DW, DH, fill=_WHT, stroke=None)
    rh, nh, fs = 8.5, 12.5, 6.8

    # ── Admin ─ x=148, top=660 ───────────────────────────────
    # (rôle retiré : cette classe reprend déjà tous les comptes
    # « administrateur » ; les clés étrangères sont retirées car
    # les liens entre classes sont représentés par les associations.)
    _cbox(d, 148, 660, "Admin", [
        "id : Long  «PK»", "username : String", "password : String",
    ], ["login() : String", "changePassword() : void",
        "forgotPassword() : void", "resetPassword() : void",
        "updateProfile() : void"],
        w=112, fs=fs, rh=rh, nh=nh)

    # ── Project / BlogPost / ContactMessage ─ top=543 ────────
    _cbox(d, 2, 543, "Project", [
        "id : Long  «PK»", "name : String",
        "description : String", "link : String",
        "documentationLink : String", "image : String",
        "category : String", "isActive : Boolean",
        "createdAt : LocalDateTime",
    ], ["activate() : void", "deactivate() : void"], w=108, fs=fs, rh=rh, nh=nh)

    _cbox(d, 116, 543, "BlogPost", [
        "id : Long  «PK»", "title : String",
        "content : String", "image : String",
        "isPublished : Boolean", "createdAt : LocalDateTime",
    ], ["publish() : void", "unpublish() : void"], w=108, fs=fs, rh=rh, nh=nh)

    _cbox(d, 230, 543, "ContactMessage", [
        "id : Long  «PK»", "name : String",
        "email : String", "message : String",
        "isRead : Boolean", "createdAt : LocalDateTime",
    ], ["markAsRead() : void", "reply() : void"], w=108, fs=fs, rh=rh, nh=nh)

    # ── Event ─ x=342, top=543 ───────────────────────────────
    _cbox(d, 342, 543, "Event", [
        "id : Long  «PK»", "title : String",
        "description : String", "eventDate : LocalDateTime",
        "location : String", "maxPlaces : Integer",
        "status : EventStatus", "imageUrl : String",
        "createdAt : LocalDateTime",
    ], ["getAvailablePlaces() : Integer", "updateStatus() : void",
        "sendGroupEmail() : void", "isFull() : Boolean",
        "exportPDF() : byte[]"], w=110, fs=fs, rh=rh, nh=nh)

    # ── AppUser ─ x=2, top=375 — inclut le niveau bénévole ────
    _cbox(d, 2, 375, "AppUser", [
        "id : Long  «PK»", "firstName : String", "lastName : String",
        "email : String", "password : String", "phone : String",
        "birthDate : LocalDate", "gender : String", "city : String",
        "postalCode : String", "skills : String", "availability : String",
        "preferredLanguage : String", "isActive : Boolean",
        "level : Level",
        "resetToken : String", "resetTokenExpiry : LocalDateTime",
        "createdAt : LocalDateTime",
    ], ["register() : void", "login() : String",
        "forgotPassword() : void", "resetPassword() : void",
        "updateProfile() : void", "getLevel() : String",
        "downloadAttestation() : byte[]"], w=150, fs=fs, rh=rh, nh=nh)

    # ── Review ─ x=192, top=375 ──────────────────────────────
    _cbox(d, 192, 375, "Review", [
        "id : Long  «PK»", "rating : Integer",
        "comment : String", "createdAt : LocalDateTime",
    ], ["submitReview() : void", "getAverageRating() : Double"],
        w=118, fs=fs, rh=rh, nh=nh)

    # ── Registration ─ x=190, top=120 ────────────────────────
    _cbox(d, 190, 120, "Registration", [
        "id : Long  «PK»", "status : RegistrationStatus",
        "position : Integer", "createdAt : LocalDateTime",
        "{unique : par bénévole et événement}",
    ], ["confirm() : void", "refuse() : void", "cancel() : void",
        "promoteFromWaiting() : void", "sendConfirmationEmail() : void"],
        w=145, fs=fs, rh=rh, nh=nh)

    # ── Associations Admin → classes existantes ──────────────
    # Admin: top=660, height=92.5 → bottom=567. Lignes partent de y=566.
    _dl(d, 158, 566, 56, 544)
    _card(d, 162, 559, "1"); _card(d, 50, 548, "0..*")
    _ds(d, 107, 553, "gère", fs=6.2, bold=True)

    _dl(d, 180, 566, 170, 544)
    _card(d, 184, 559, "1"); _card(d, 158, 548, "0..*")
    _ds(d, 175, 553, "publie", fs=6.2, bold=True)

    _dl(d, 202, 566, 284, 544)
    _card(d, 198, 559, "1"); _card(d, 288, 548, "0..*")
    _ds(d, 243, 553, "reçoit", fs=6.2, bold=True)

    _dl(d, 224, 566, 397, 544)
    _card(d, 220, 559, "1"); _card(d, 392, 548, "0..*")
    _ds(d, 310, 553, "crée", fs=6.2, bold=True)

    # Admin → Registration («valide») : ligne coudée pour ne pas
    # traverser ContactMessage. Cardinalité 0..1 remontée à côté
    # d'Admin (à l'entrée de l'association), comme demandé.
    _dl(d, 252, 566, 339, 566)
    _dl(d, 339, 566, 339, 122)
    _dl(d, 339, 122, 250, 122)
    _card(d, 258, 561, "0..1"); _card(d, 240, 126, "0..*")
    _ds(d, 344, 350, "valide", anchor='start', fs=6.2, bold=True)

    # ── Associations du module TFE ────────────────────────────
    # rédige : attache au niveau du bandeau-titre des deux boîtes,
    # pour ne pas croiser le texte des attributs
    _dl(d, 152, 376, 192, 376)
    _card(d, 154, 380, "1"); _card(d, 170, 380, "0..*")
    _ds(d, 172, 368, "rédige", fs=6.2, bold=True)

    _dl(d, 100, 140, 200, 118)
    _card(d, 104, 134, "1"); _card(d, 204, 124, "0..*")
    _ds(d, 140, 129, "effectue", fs=6.2, bold=True)

    # Event → Registration renommée « accueille » (pour ne pas dupliquer
    # le verbe « reçoit » déjà utilisé pour Admin → ContactMessage).
    # Route coudée par le bord droit pour contourner la boîte EventStatus.
    _dl(d, 445, 401, 445, 122)
    _dl(d, 445, 122, 335, 122)
    _card(d, 440, 395, "1"); _card(d, 337, 128, "0..*")
    _ds(d, 448, 260, "accueille", anchor='start', fs=6.2, bold=True)

    _dl(d, 300, 377, 420, 401)
    _card(d, 296, 381, "0..*"); _card(d, 424, 394, "1")
    _ds(d, 300, 388, "concerne", fs=6.2, bold=True)

    # ── Énumérations ─────────────────────────────────────────
    # Placées dans les zones libres du diagramme, avec flèches
    # de dépendance (pointillés + pointe ouverte) partant de
    # la classe qui utilise l'énumération.

    # EventStatus : à droite du bloc central, entre Event et
    # AppUser/Review (zone libre x=345-425, y=310-370)
    _enumbox(d, 345, 370, "EventStatus",
        ["OPEN", "FULL", "CANCELLED", "FINISHED"], w=80)
    # Flèche depuis Event (bord bas) vers EventStatus (bord haut)
    _dl(d, 397, 400, 385, 372, dash=[3, 2], w=0.7)
    _arr_v(d, 385, 372, 'down')

    # Level : dans le coin bas-gauche, sous AppUser
    _enumbox(d, 15, 110, "Level",
        ["BRONZE", "ARGENT", "OR"], w=68)
    # Flèche depuis AppUser (bord bas) vers Level (bord haut)
    _dl(d, 49, 138, 49, 112, dash=[3, 2], w=0.7)
    _arr_v(d, 49, 112, 'down')

    # RegistrationStatus : à droite de Registration
    _enumbox(d, 345, 105, "RegistrationStatus",
        ["CONFIRMED", "WAITING", "REFUSED"], w=95)
    # Flèche depuis Registration (bord droit) vers RegistrationStatus (bord gauche)
    _dl(d, 335, 82, 343, 82, dash=[3, 2], w=0.7)
    _arr_h(d, 345, 82, 'right')

    return d

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
    S_.append(Spacer(1, 2.2*cm))
    S_.append(Paragraph("Rapport écrit", CV_TITLE))
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
        ("1.1 Présentation de Terra Sana ASBL",                    3,  2),
        ("1.2 Sources d'information",                              3,  2),
        ("1.3 Cahier des charges du TFE",                          3,  2),
        ("1.4 Contexte du TFE",                                    4,  2),
        ("1.5 Problématique",                                      4,  2),
        ("2. Travail réalisé durant le stage",                     5,  1),
        ("2.1 Composants livrés à la fin du stage",                5,  2),
        ("2.2 Technologies utilisées",                             5,  2),
        ("3. Nouvelles fonctionnalités du module TFE",             6,  1),
        ("3.1 Refonte graphique",                                  6,  2),
        ("3.2 Espace personnel bénévole",                          6,  2),
        ("3.3 Gestion des événements",                             7,  2),
        ("3.4 Inscription aux événements",                         7,  2),
        ("3.5 Retours post-événement",                             8,  2),
        ("3.6 Dashboard administrateur enrichi",                   8,  2),
        ("3.7 Fonctionnalités avancées",                           8,  2),
        ("3.8 Export PDF et attestation",                          8,  2),
        ("4. Analyse fonctionnelle",                               9,  1),
        ("4.1 Diagramme de cas d'utilisation",                     9,  2),
        ("4.2 Règles de gestion",                                 11,  2),
        ("5. Persistance des données",                             13,  1),
        ("5.1 Diagramme de classes",                              13,  2),
        ("5.2 Dictionnaire de données",                           15,  2),
        ("6. Apport personnel dans le cadre du TFE",              19,  1),
        ("7. Plan de travail",                                    20,  1),
        ("7.1 Calendrier et phases de développement",             20,  2),
        ("7.2 Échéances officielles et dates clés",               21,  2),
        ("7.3 Contraintes et risques identifiés",                 21,  2),
    ]
    for label, page, level in toc:
        S_.append(toc_line(label, page, level))
    S_.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P3 — 1. INTRODUCTION
    # ═══════════════════════════════════════════════════════
    S_.append(Paragraph("1. Introduction", SEC1))

    S_.append(Paragraph("1.1 Présentation de Terra Sana ASBL", SEC2))
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

    S_.append(Paragraph("1.2 Sources d'information", SEC2))
    S_.append(Paragraph(
        "Les informations utilisées pour concevoir l'application proviennent de plusieurs "
        "sources complémentaires réunies pendant et après le stage :", BODY))
    for b in [
        "des entretiens avec Monsieur Didier Seraye (Responsable Administratif de Terra Sana) "
        "afin de comprendre les besoins réels, le fonctionnement quotidien de l'association et "
        "les points de friction dans la gestion actuelle des bénévoles et des événements ;",
        "l'analyse des documents et fichiers Excel utilisés à ce jour pour identifier les "
        "données à structurer (identité des bénévoles, historiques d'ateliers, listes d'inscrits) ;",
        "la documentation officielle des technologies retenues (Spring Boot, React, Spring "
        "Security, JavaMail, iText) ainsi que les bonnes pratiques REST et de sécurité ;",
        "les consignes de l'EAFC Uccle pour la rédaction du présent rapport et la structuration "
        "du projet de fin d'études.",
    ]:
        S_.append(Paragraph(f"• {b}", BULL))

    S_.append(Paragraph("1.3 Cahier des charges du TFE", SEC2))
    S_.append(Paragraph(
        "Ce projet de TFE consiste à <b>étendre le site vitrine développé pendant le stage</b> "
        "en y intégrant un <b>module complet de gestion des bénévoles et des événements</b>. "
        "La demande initiale de Terra Sana ASBL est de centraliser et d'automatiser ce qui "
        "était jusqu'ici tenu à la main dans des fichiers Excel et par email.", BODY))
    S_.append(Paragraph(
        "Le module à livrer doit permettre concrètement :", BODY))
    for b in [
        "aux bénévoles de créer un compte, se connecter, gérer leur profil et consulter leur historique ;",
        "aux bénévoles de s'inscrire aux événements, rejoindre une liste d'attente si l'événement "
        "est complet, se désinscrire et laisser un avis après participation ;",
        "à l'administrateur de créer et gérer les événements, valider ou refuser les inscriptions, "
        "notifier les bénévoles par email et exporter les listes en PDF ;",
        "au bénévole de télécharger une attestation de participation à la fin d'un événement ;",
        "à l'application de calculer automatiquement un niveau de fidélité (Bronze / Argent / Or) "
        "à partir du nombre de participations confirmées.",
    ]:
        S_.append(Paragraph(f"• {b}", BULL))
    S_.append(Paragraph(
        "Ces fonctionnalités sont détaillées dans la section 3 et analysées dans les sections 4 "
        "(diagrammes UML et règles de gestion) et 5 (modèle de données).", BODY))
    S_.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P4 — 1.4 Contexte du TFE + 1.5 Problématique
    # ═══════════════════════════════════════════════════════
    S_.append(Paragraph("1.4 Contexte du TFE", SEC2))
    S_.append(Paragraph(
        "Le présent rapport écrit accompagne mon Travail de Fin d'Études, réalisé dans le cadre "
        "de l'épreuve intégrée du Bachelier en Informatique de Gestion (3ème année) à l'EAFC "
        "Uccle, pour l'année académique 2025-2026.", BODY))
    S_.append(Paragraph(
        "Mon stage s'est déroulé au sein de Terra Sana ASBL du 25 mars au 20 mai 2026, sous la "
        "supervision de Monsieur Didier Seraye. Durant cette période, j'ai conçu et développé "
        "de zéro un site web complet servant de vitrine institutionnelle et de hub centralisé "
        "pour les 12 applications internes de l'association.", BODY))
    S_.append(Paragraph(
        "Le module de gestion des bénévoles et des événements est développé après le stage, "
        "entièrement par mes soins, sans code préexistant. Le développement et la démonstration "
        "sont réalisés en environnement local (WAMP Server sous Windows).", BODY))

    S_.append(Paragraph("1.5 Problématique", SEC2))
    S_.append(Paragraph(
        "Aujourd'hui, Terra Sana gère ses bénévoles et ses activités de façon entièrement "
        "manuelle. Cette organisation engendre plusieurs difficultés concrètes :", BODY))
    for b in [
        "des doublons et pertes d'information quand plusieurs personnes modifient les mêmes fichiers ;",
        "aucune vue d'ensemble des places disponibles, d'où des activités surchargées ou sous-remplies ;",
        "des confirmations et relances envoyées une à une, un travail répétitif et chronophage ;",
        "aucun historique de participation, ni moyen de remercier les bénévoles ou de leur délivrer une attestation.",
    ]:
        S_.append(Paragraph(f"• {b}", BULL))
    S_.append(Paragraph(
        "Le module développé dans le cadre du TFE vise à centraliser et automatiser ces tâches : "
        "espace bénévole en ligne, gestion des événements avec places et liste d'attente, "
        "emails de confirmation automatiques et historique exploitable (niveaux, attestations). "
        "L'association gagne ainsi en temps et en fiabilité.", BODY))
    S_.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P5 — 2. TRAVAIL RÉALISÉ DURANT LE STAGE (compact)
    # ═══════════════════════════════════════════════════════
    S_.append(Paragraph("2. Travail réalisé durant le stage", SEC1))
    S_.append(Paragraph(
        "L'association Terra Sana ASBL ne disposait d'aucune présence numérique avant le stage. "
        "L'objectif était de concevoir et développer un site web moderne, multilingue et évolutif, "
        "permettant de présenter l'association au public et de centraliser l'accès à ses "
        "12 applications internes via un hub de projets. Le module TFE, développé après le stage, "
        "s'ajoute à cette base et ne se substitue pas à elle.", BODY))

    S_.append(Paragraph("2.1 Composants livrés à la fin du stage", SEC2))
    S_.append(grid([4.2*cm, CW-4.2*cm], [
        [th("Composant"),             th("Description")],
        [tb("Site public multilingue"),
         tb("12 pages React (Accueil, À propos, Projets, Détail projet, Blog, Contact, "
            "Bénévolat, Sponsors, Confidentialité, Conditions, Cookies, Aide/FAQ), "
            "trilingue FR / EN / NL avec sélecteur de langue.")],
        [tb("Hub des 12 applications"),
         tb("Affichage dynamique de l'ensemble des applications internes de l'association, "
            "avec recherche et filtres par catégorie.")],
        [tb("Espace administrateur"),
         tb("Deux pages sécurisées : connexion (JWT 24h) et dashboard permettant la gestion "
            "des projets, des articles de blog, des messages de contact et le changement "
            "de mot de passe.")],
        [tb("API REST backend"),
         tb("17 endpoints exposés sur 4 ressources (auth, projects, posts, contact), "
            "sécurisés par JWT et rôle administrateur.")],
        [tb("Base de données"),
         tb("Base MySQL comprenant 4 tables : admin, project, blog_post et contact_message "
            "(le schéma détaillé est repris dans le dictionnaire de données, section 5.2).")],
        [tb("Envoi d'e-mails"),
         tb("Réponse aux messages de contact via Gmail SMTP.")],
    ]))
    S_.append(sp(0.3))

    S_.append(Paragraph("2.2 Technologies utilisées", SEC2))
    S_.append(grid([4.0*cm, 2.5*cm, CW-6.7*cm], [
        [th("Technologie"),           th("Version"), th("Usage")],
        [tb("React.js"),              tb("18.2.0"),  tb("Frontend — pages, navigation, composants")],
        [tb("Spring Boot"),           tb("Java 21"), tb("Backend — API REST, logique métier")],
        [tb("Spring Security + JWT"), tb("0.11.5"),  tb("Authentification et sécurisation")],
        [tb("MySQL"),                 tb("9.1.0"),   tb("Base de données relationnelle")],
        [tb("BCrypt"),                tb("—"),       tb("Hachage sécurisé des mots de passe")],
        [tb("Git / GitHub"),          tb("—"),       tb("Versioning et hébergement du code source")],
        [tb("WAMP Server"),           tb("3.3.7"),   tb("Environnement local MySQL sous Windows")],
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
    # SECTION 4. ANALYSE FONCTIONNELLE
    # (cas d'utilisation + règles de gestion)
    # ═══════════════════════════════════════════════════════
    S_.append(Paragraph("4. Analyse fonctionnelle", SEC1))
    S_.append(Paragraph("4.1 Diagramme de cas d'utilisation", SEC2))
    S_.append(Paragraph(
        "Le diagramme ci-dessous représente les interactions entre les acteurs du système "
        "et les fonctionnalités offertes par le module TFE. Trois acteurs sont identifiés : "
        "le Visiteur (non authentifié, qui devient bénévole dès qu'il crée un compte), le "
        "Bénévole (qui étend le Visiteur par généralisation) et l'Administrateur.", BODY))
    S_.append(sp(0.2))
    S_.append(diag_use_case())
    S_.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # 4.2 RÈGLES DE GESTION
    # ═══════════════════════════════════════════════════════
    S_.append(Paragraph("4.2 Règles de gestion", SEC2))
    S_.append(Paragraph(
        "Les règles de gestion décrivent les contraintes métier que l'application doit "
        "respecter. Elles complètent les cas d'utilisation en explicitant les conditions et "
        "les invariants attendus. Elles sont regroupées ci-dessous par thématique.", BODY))

    S_.append(Paragraph("Comptes bénévoles", SEC2B))
    for r in [
        "<b>RG-01</b> — L'adresse email d'un bénévole est unique dans le système : elle sert "
        "d'identifiant de connexion et empêche la création de doublons.",
        "<b>RG-02</b> — Le mot de passe compte au moins 8 caractères et est stocké haché "
        "(BCrypt) ; il n'est jamais consultable en clair.",
        "<b>RG-03</b> — Un compte bénévole peut être désactivé sans être supprimé "
        "(<font face='Courier'>isActive = false</font>), afin de conserver l'historique des "
        "inscriptions passées.",
        "<b>RG-04</b> — La demande de réinitialisation du mot de passe utilise un jeton "
        "à usage unique valable 30 minutes, envoyé par email.",
    ]:
        S_.append(Paragraph(f"• {r}", BULL))

    S_.append(Paragraph("Événements", SEC2B))
    for r in [
        "<b>RG-05</b> — Chaque événement porte obligatoirement une date, un lieu et un nombre "
        "maximum de participants.",
        "<b>RG-06</b> — Le statut d'un événement évolue automatiquement : <b>OPEN</b> par défaut, "
        "<b>FULL</b> dès que toutes les places sont prises, <b>FINISHED</b> une fois la date "
        "passée, <b>CANCELLED</b> uniquement sur décision explicite de l'administrateur.",
        "<b>RG-07</b> — Un événement passé (FINISHED ou CANCELLED) n'accepte plus de "
        "nouvelles inscriptions.",
    ]:
        S_.append(Paragraph(f"• {r}", BULL))

    S_.append(Paragraph("Inscriptions et liste d'attente", SEC2B))
    for r in [
        "<b>RG-08</b> — Un bénévole ne peut s'inscrire qu'une seule fois au même événement "
        "(contrainte d'unicité sur le couple bénévole + événement).",
        "<b>RG-09</b> — Si l'événement est complet au moment de l'inscription, le bénévole "
        "est placé automatiquement en liste d'attente (<font face='Courier'>status = WAITING</font>) "
        "avec une position calculée en fonction de l'ordre d'arrivée.",
        "<b>RG-10</b> — Toute inscription reste en attente de validation ; l'administrateur "
        "doit explicitement la confirmer ou la refuser.",
        "<b>RG-11</b> — Un email de confirmation est envoyé automatiquement au bénévole lors "
        "de chaque validation ou refus.",
        "<b>RG-12</b> — Lorsqu'une place se libère (désinscription confirmée), le premier "
        "bénévole en liste d'attente est promu automatiquement (WAITING → CONFIRMED) et notifié "
        "par email.",
        "<b>RG-13</b> — Le bénévole peut se désinscrire librement tant que l'événement n'est "
        "pas commencé.",
    ]:
        S_.append(Paragraph(f"• {r}", BULL))
    S_.append(PageBreak())

    # 4.2 suite — règles de gestion (2ème page)
    S_.append(Paragraph("Avis (retours post-événement)", SEC2B))
    for r in [
        "<b>RG-14</b> — Seul un bénévole ayant effectivement participé à un événement "
        "(inscription <font face='Courier'>CONFIRMED</font>) peut laisser un avis.",
        "<b>RG-15</b> — Un avis ne peut être laissé qu'après la fin de l'événement "
        "(<font face='Courier'>status = FINISHED</font>).",
        "<b>RG-16</b> — Un bénévole ne peut laisser qu'un seul avis par événement.",
        "<b>RG-17</b> — La note est obligatoirement comprise entre 1 et 5.",
    ]:
        S_.append(Paragraph(f"• {r}", BULL))

    S_.append(Paragraph("Niveau de fidélité", SEC2B))
    for r in [
        "<b>RG-18</b> — Le niveau du bénévole est calculé automatiquement à partir de son "
        "nombre de participations confirmées : <b>BRONZE</b> (1 à 2 événements), "
        "<b>ARGENT</b> (3 à 6), <b>OR</b> (7 et plus).",
        "<b>RG-19</b> — Un email de notification est envoyé au bénévole lors du passage à "
        "un nouveau niveau.",
    ]:
        S_.append(Paragraph(f"• {r}", BULL))

    S_.append(Paragraph("Attestations et exports", SEC2B))
    for r in [
        "<b>RG-20</b> — Une attestation PDF de participation ne peut être générée que si le "
        "bénévole a au moins une participation confirmée à un événement terminé.",
        "<b>RG-21</b> — L'export PDF de la liste des inscrits d'un événement est réservé à "
        "l'administrateur.",
    ]:
        S_.append(Paragraph(f"• {r}", BULL))

    S_.append(Paragraph("Sécurité et accès", SEC2B))
    for r in [
        "<b>RG-22</b> — Toute action nécessitant un compte est protégée par un jeton JWT "
        "valable 24 heures ; l'expiration force la reconnexion.",
        "<b>RG-23</b> — Les endpoints d'administration sont accessibles uniquement aux "
        "comptes disposant du rôle administrateur.",
        "<b>RG-24</b> — Les tokens de bénévole et d'administrateur sont émis séparément, "
        "avec des secrets et des durées de vie distincts.",
    ]:
        S_.append(Paragraph(f"• {r}", BULL))
    S_.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # SECTION 5. MODÈLE DE DONNÉES
    # (diagramme de classes + dictionnaire de données)
    # ═══════════════════════════════════════════════════════
    S_.append(Paragraph("5. Persistance des données", SEC1))
    S_.append(Paragraph("5.1 Diagramme de classes", SEC2))
    S_.append(Paragraph(
        "Le diagramme de classes présente les huit entités du modèle, leurs attributs, leurs "
        "méthodes et leurs associations nommées. Les liens entre classes sont représentés "
        "uniquement par les associations (les clés étrangères ne sont pas dupliquées comme "
        "attributs). Les entités AppUser, Event, Review et Registration sont créées dans le "
        "cadre du TFE ; Admin, Project, BlogPost et ContactMessage proviennent du site "
        "existant. Trois énumérations (EventStatus, RegistrationStatus, Level) typent les "
        "attributs à valeurs fermées et sont reliées aux classes qui les utilisent par une "
        "flèche de dépendance.", BODY))
    S_.append(sp(0.2))
    S_.append(diag_classes())
    S_.append(PageBreak())

    # 5.2 Dictionnaire de données (tables existantes + nouvelles)
    S_.append(Paragraph("5.2 Dictionnaire de données", SEC2))
    S_.append(Paragraph(
        "Le dictionnaire ci-dessous reprend l'ensemble des tables de la base MySQL, à la fois "
        "celles héritées du stage et les quatre nouvelles tables créées pour le module TFE. "
        "Il précise, pour chaque champ, le type, les contraintes et le rôle métier.", BODY))
    cbd = [3.3*cm, 3.0*cm, 3.2*cm, CW-9.7*cm]

    # Tables existantes (séparées, une par une, comme les nouvelles tables)
    S_.append(Paragraph("Tables héritées du stage", SEC2B))
    S_.append(Paragraph("<b>admin</b> — Compte administrateur unique", SEC2B))
    S_.append(grid(cbd, [
        [th("Champ"), th("Type"), th("Contrainte"), th("Description")],
        [tb("id"),       tb("BIGINT"),        tb("PK, AUTO_INCREMENT"), tb("Identifiant.")],
        [tb("username"), tb("VARCHAR(100)"),  tb("NOT NULL, UNIQUE"),    tb("Identifiant de connexion.")],
        [tb("password"), tb("VARCHAR(255)"),  tb("NOT NULL"),            tb("Mot de passe haché (BCrypt).")],
    ]))
    S_.append(sp(0.3))
    S_.append(Paragraph("<b>project</b> — Applications du hub", SEC2B))
    S_.append(grid(cbd, [
        [th("Champ"), th("Type"), th("Contrainte"), th("Description")],
        [tb("id"),           tb("BIGINT"),       tb("PK, AUTO_INCREMENT"),   tb("Identifiant.")],
        [tb("name"),         tb("VARCHAR(200)"), tb("NOT NULL"),             tb("Nom de l'application.")],
        [tb("description"),  tb("TEXT"),         tb("NOT NULL"),             tb("Présentation.")],
        [tb("link, documentationLink"), tb("VARCHAR(500)"), tb("NULL"),      tb("URL vers l'app et sa doc.")],
        [tb("image, category"),         tb("VARCHAR"),      tb("NULL"),      tb("Illustration et catégorie.")],
        [tb("isActive"),     tb("BOOLEAN"),      tb("DEFAULT TRUE"),         tb("Visible ou non sur le hub.")],
        [tb("createdAt"),    tb("DATETIME"),     tb("NOT NULL"),             tb("Date de création.")],
    ]))
    S_.append(PageBreak())
    S_.append(Paragraph("<b>blog_post</b> — Articles du blog", SEC2B))
    S_.append(grid(cbd, [
        [th("Champ"), th("Type"), th("Contrainte"), th("Description")],
        [tb("id"),           tb("BIGINT"),       tb("PK, AUTO_INCREMENT"),   tb("Identifiant.")],
        [tb("admin_id"),     tb("BIGINT"),       tb("FK → admin"),           tb("Auteur de l'article.")],
        [tb("title, content, image"), tb("VARCHAR/TEXT"), tb("NOT NULL"),    tb("Contenu de l'article.")],
        [tb("isPublished"),  tb("BOOLEAN"),      tb("DEFAULT FALSE"),        tb("Publié ou brouillon.")],
        [tb("createdAt"),    tb("DATETIME"),     tb("NOT NULL"),             tb("Date de rédaction.")],
    ]))
    S_.append(sp(0.3))
    S_.append(Paragraph("<b>contact_message</b> — Messages du formulaire de contact", SEC2B))
    S_.append(grid(cbd, [
        [th("Champ"), th("Type"), th("Contrainte"), th("Description")],
        [tb("id"),           tb("BIGINT"),       tb("PK, AUTO_INCREMENT"),   tb("Identifiant.")],
        [tb("name, email, message"),  tb("VARCHAR/TEXT"), tb("NOT NULL"),    tb("Contenu du message.")],
        [tb("isRead"),       tb("BOOLEAN"),      tb("DEFAULT FALSE"),        tb("Traité ou non.")],
        [tb("createdAt"),    tb("DATETIME"),     tb("NOT NULL"),             tb("Date de réception.")],
    ]))
    S_.append(PageBreak())

    # Nouvelles tables TFE (détaillées)
    S_.append(Paragraph("Nouvelles tables du module TFE", SEC2B))
    S_.append(Paragraph("<b>app_users</b> — Bénévoles", SEC2B))
    S_.append(grid(cbd, [
        [th("Champ"),           th("Type"),        th("Contrainte"),        th("Description")],
        [tb("id"),              tb("BIGINT"),      tb("PK, AUTO_INCREMENT"), tb("Identifiant.")],
        [tb("firstName"),       tb("VARCHAR(100)"),tb("NOT NULL"),           tb("Prénom.")],
        [tb("lastName"),        tb("VARCHAR(100)"),tb("NOT NULL"),           tb("Nom.")],
        [tb("email"),           tb("VARCHAR(200)"),tb("NOT NULL, UNIQUE"),   tb("Email de connexion (RG-01).")],
        [tb("password"),        tb("VARCHAR(255)"),tb("NOT NULL"),           tb("Haché BCrypt (RG-02).")],
        [tb("phone, birthDate, gender"), tb("—"), tb("NULL"),                tb("Coordonnées facultatives.")],
        [tb("city, postalCode"),tb("VARCHAR"),     tb("NULL"),               tb("Localité.")],
        [tb("skills, availability"), tb("TEXT / VARCHAR"), tb("NULL"),       tb("Compétences et disponibilités.")],
        [tb("preferredLanguage"),tb("VARCHAR(5)"), tb("DEFAULT fr"),         tb("Langue préférée (FR/EN/NL).")],
        [tb("level"),           tb("VARCHAR(10)"), tb("DEFAULT BRONZE"),     tb("BRONZE / ARGENT / OR (RG-18).")],
        [tb("isActive"),        tb("BOOLEAN"),     tb("DEFAULT TRUE"),       tb("Compte actif (RG-03).")],
        [tb("resetToken"),      tb("VARCHAR(255)"),tb("NULL"),               tb("Jeton de réinitialisation (RG-04).")],
        [tb("resetTokenExpiry"),tb("DATETIME"),    tb("NULL"),               tb("Expiration du jeton.")],
        [tb("createdAt"),       tb("DATETIME"),    tb("NOT NULL"),           tb("Date d'inscription.")],
    ]))
    S_.append(sp(0.3))
    S_.append(Paragraph("<b>events</b> — Événements", SEC2B))
    S_.append(grid(cbd, [
        [th("Champ"),      th("Type"),         th("Contrainte"),   th("Description")],
        [tb("id"),         tb("BIGINT"),       tb("PK, AUTO_INCREMENT"), tb("Identifiant.")],
        [tb("admin_id"),   tb("BIGINT"),       tb("FK → admin"),   tb("Administrateur créateur.")],
        [tb("title"),      tb("VARCHAR(200)"), tb("NOT NULL"),     tb("Titre.")],
        [tb("description"),tb("TEXT"),         tb("NOT NULL"),     tb("Description complète.")],
        [tb("eventDate"),  tb("DATETIME"),     tb("NOT NULL"),     tb("Date et heure (RG-05).")],
        [tb("location"),   tb("VARCHAR(300)"), tb("NOT NULL"),     tb("Lieu.")],
        [tb("maxPlaces"),  tb("INT"),          tb("NOT NULL"),     tb("Nombre de places (RG-05).")],
        [tb("status"),     tb("VARCHAR(20)"),  tb("DEFAULT OPEN"), tb("OPEN/FULL/CANCELLED/FINISHED (RG-06).")],
        [tb("imageUrl"),   tb("VARCHAR(500)"), tb("NULL"),         tb("Illustration.")],
        [tb("createdAt"),  tb("DATETIME"),     tb("NOT NULL"),     tb("Date de création.")],
    ]))
    S_.append(PageBreak())

    S_.append(Paragraph("<b>registrations</b> — Inscriptions et liste d'attente", SEC2B))
    S_.append(grid(cbd, [
        [th("Champ"),        th("Type"),       th("Contrainte"),                            th("Description")],
        [tb("id"),           tb("BIGINT"),     tb("PK, AUTO_INCREMENT"),                    tb("Identifiant.")],
        [tb("user_id"),      tb("BIGINT"),     tb("FK → app_users"),                        tb("Bénévole inscrit.")],
        [tb("event_id"),     tb("BIGINT"),     tb("FK → events"),                           tb("Événement concerné.")],
        [tb("validatedBy_id"),tb("BIGINT"),    tb("FK → admin, NULL"),                      tb("Admin ayant traité (RG-10).")],
        [tb("status"),       tb("VARCHAR(20)"),tb("NOT NULL"),                              tb("CONFIRMED/WAITING/REFUSED.")],
        [tb("position"),     tb("INT"),        tb("NULL"),                                  tb("Position en liste (RG-09).")],
        [tb("createdAt"),    tb("DATETIME"),   tb("NOT NULL"),                              tb("Date d'inscription.")],
        [tb("—"),            tb("—"),          tb("UNIQUE(user_id, event_id)"),             tb("Contrainte d'unicité (RG-08).")],
    ]))
    S_.append(sp(0.3))
    S_.append(Paragraph("<b>reviews</b> — Retours post-événement", SEC2B))
    S_.append(grid(cbd, [
        [th("Champ"),     th("Type"),      th("Contrainte"),        th("Description")],
        [tb("id"),        tb("BIGINT"),    tb("PK, AUTO_INCREMENT"), tb("Identifiant.")],
        [tb("user_id"),   tb("BIGINT"),    tb("FK → app_users"),     tb("Auteur (RG-14).")],
        [tb("event_id"),  tb("BIGINT"),    tb("FK → events"),        tb("Événement évalué.")],
        [tb("rating"),    tb("INT"),       tb("NOT NULL, CHECK 1..5"),tb("Note (RG-17).")],
        [tb("comment"),   tb("TEXT"),      tb("NULL"),               tb("Commentaire libre.")],
        [tb("createdAt"), tb("DATETIME"),  tb("NOT NULL"),           tb("Date de l'avis.")],
        [tb("—"),         tb("—"),         tb("UNIQUE(user_id, event_id)"), tb("Un seul avis par événement (RG-16).")],
    ]))
    S_.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # SECTION 6. APORT PERSONNEL (compact, sans répétition)
    # ═══════════════════════════════════════════════════════
    S_.append(Paragraph("6. Apport personnel dans le cadre du TFE", SEC1))
    S_.append(Paragraph(
        "Le travail réalisé durant le stage (section 2) constitue la fondation technique du "
        "projet : site public, hub des applications, panel administrateur, authentification "
        "JWT et base de données de départ. Toutes les fonctionnalités présentées en section 3 "
        "sont, elles, entièrement conçues et développées par moi, à domicile, après le stage, "
        "à partir de cette base. Le tableau ci-dessous en donne une vue synthétique et chiffrée.",
        BODY))
    S_.append(sp(0.2))
    S_.append(grid([4.5*cm, 2.5*cm, CW-7.2*cm], [
        [th("Critère"),                th("Stage"),   th("TFE (apport personnel)")],
        [tb("Tables BD"),              tb("4"),       tb("+4 nouvelles (8 au total)")],
        [tb("Endpoints API REST"),     tb("17"),      tb("+30 nouveaux (47 au total)")],
        [tb("Pages frontend"),         tb("14"),      tb("+7 nouvelles (21 au total)")],
        [tb("Pages redessinées"),      tb("0"),       tb("14 pages existantes refaites")],
        [tb("Module bénévoles"),       tb("aucun"),   tb("module complet (inscription, profil, niveaux)")],
        [tb("Gestion des événements"), tb("aucune"),  tb("module complet (CRUD, inscriptions, retours)")],
        [tb("Envois d'e-mails automatiques"), tb("réponses au contact"),
                                                     tb("confirmation, liste d'attente, groupe, réinitialisation, changement de niveau")],
        [tb("Export PDF"),             tb("aucun"),   tb("attestation bénévole + liste inscrits par événement")],
    ]))
    S_.append(sp(0.3))
    S_.append(Paragraph(
        "Les bibliothèques et outils spécifiques ajoutés pour le TFE, en complément de la pile "
        "technique du stage (section 2.2), sont : <b>JavaMail / Gmail SMTP</b> pour les emails, "
        "<b>Chart.js</b> pour les graphiques du dashboard, <b>Spring Pageable</b> pour la "
        "pagination et <b>iText / JasperReports</b> pour la génération des PDF.", BODY))
    S_.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # SECTION 7. PLAN DE TRAVAIL
    # ═══════════════════════════════════════════════════════
    S_.append(Paragraph("7. Plan de travail", SEC1))

    S_.append(Paragraph("7.1 Calendrier et phases de développement", SEC2))
    S_.append(Paragraph(
        "Le tableau ci-dessous combine les échéances officielles de la 2ème session et le "
        "découpage du travail en phases. Chaque phase est positionnée dans la période "
        "correspondante pour tenir les remises fixées par l'EAFC Uccle.", BODY))
    S_.append(grid([4.3*cm, CW-9.5*cm, 3.4*cm, 1.8*cm], [
        [th("Phase"),                             th("Contenu"),
         th("Période"),           th("Statut")],
        [tb("Phase 1 — Analyse & rapport écrit"),
         tb("Analyse de l'existant, cahier des charges, diagrammes UML, dictionnaire de données"),
         tb("Mai – juil. 2026"),  tb("En cours")],
        [tb("Phase 2 — Refonte graphique"),
         tb("Application de la nouvelle charte sur toutes les pages (public + admin)"),
         tb("Début juil. 2026"),  tb("À faire")],
        [tb("Phase 3 — Backend TFE"),
         tb("Entités JPA, repositories, controllers, sécurité JWT, envoi d'e-mails Gmail SMTP"),
         tb("Juillet 2026"),      tb("À faire")],
        [tb("Phase 4 — Frontend bénévoles"),
         tb("Inscription, connexion, profil, mot de passe oublié, espace personnel"),
         tb("Juil. – août 2026"), tb("À faire")],
        [tb("Phase 5 — Frontend événements"),
         tb("Liste, détail, inscription, liste d'attente, retours post-événement"),
         tb("Août 2026"),         tb("À faire")],
        [tb("Phase 6 — Fonctionnalités avancées"),
         tb("Chart.js, pagination, badges, filtres, niveaux, export PDF"),
         tb("Août – sept. 2026"), tb("À faire")],
        [tb("Phase 7 — Tests & corrections"),
         tb("Tests complets, corrections, validation par l'encadreur"),
         tb("Septembre 2026"),    tb("À faire")],
        [tb("Phase 8 — Finalisation"),
         tb("Rapport écrit définitif, dépôt GitHub, 5 exemplaires, préparation soutenance"),
         tb("Sept. – oct. 2026"), tb("À faire")],
    ]))
    S_.append(PageBreak())

    S_.append(Paragraph("7.2 Échéances officielles et dates clés personnelles", SEC2))
    S_.append(Paragraph(
        "Les échéances officielles imposées par l'EAFC Uccle pour la 2ème session sont reprises "
        "ci-dessous, avec l'action personnelle correspondante :", BODY))
    S_.append(grid([2.8*cm, 3.5*cm, CW-6.3*cm], [
        [th("Date limite"), th("Échéance officielle"),                             th("Action personnelle prévue")],
        [tb("03/07/2026"),  tb("Remise du rapport écrit (analyse)"),               tb("Envoi de la version validée à l'encadreur.")],
        [tb("28/08/2026"),  tb("Validation de l'analyse par l'encadreur"),         tb("Prise en compte des retours, correctifs.")],
        [tb("15/09/2026"),  tb("Validation de l'application"),                     tb("Application complète et fonctionnelle en local.")],
        [tb("22/09/2026"),  tb("Rapport écrit provisoire (PDF sur Teams)"),        tb("Version relue soumise sur Teams.")],
        [tb("29/09/2026"),  tb("Rapport écrit définitif (PDF + 5 exemplaires + GitHub)"), tb("Dépôt secrétariat + push final GitHub.")],
        [tb("13/10/2026"),  tb("Défense orale"),                                   tb("Préparation de la présentation et démonstration.")],
    ]))
    S_.append(sp(0.4))

    S_.append(Paragraph("7.3 Contraintes et risques identifiés", SEC2))
    S_.append(Paragraph(
        "Plusieurs contraintes techniques et organisationnelles ont été anticipées dès la phase "
        "d'analyse. Le tableau ci-dessous recense les principaux risques et les mesures "
        "prévues pour les limiter.", BODY))
    S_.append(grid([5.0*cm, CW-5.0*cm], [
        [th("Contrainte / Risque"), th("Mesure prévue")],
        [tb("Délai serré de la 2ème session (juillet à octobre 2026)"),
         tb("Découpage du travail en huit phases planifiées (section 7.1) afin de garantir les fonctionnalités essentielles en priorité.")],
        [tb("Dépendance au service Gmail SMTP pour l'envoi des e-mails"),
         tb("Utilisation d'un mot de passe d'application dédié ; en cas d'indisponibilité, les notifications restent consultables directement dans l'espace bénévole.")],
        [tb("Sécurité des données personnelles des bénévoles"),
         tb("Mots de passe chiffrés avec BCrypt, authentification par jeton JWT et contrôle des accès par rôle (règles RG-02, RG-22, RG-23).")],
        [tb("Compatibilité navigateurs et affichage multilingue (FR/EN/NL)"),
         tb("Interface responsive testée sur les principaux navigateurs et relecture systématique des trois versions linguistiques avant la remise.")],
        [tb("Perte de code ou de données"),
         tb("Versionnage sur GitHub avec sauvegardes régulières et base de données exportée à chaque étape importante.")],
        [tb("Environnement de développement et de démonstration"),
         tb("L'application est développée et présentée en environnement local (WAMP Server sous Windows). Aucun déploiement en ligne n'est prévu dans le cadre de ce TFE.")],
    ]))
    S_.append(PageBreak())

    doc.build(S_)
    print(f"PDF généré : {out}")

if __name__ == "__main__":
    build()
