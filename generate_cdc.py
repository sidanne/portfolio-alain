#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère le cahier des charges Terra Sana sans le diagramme de classes (pages 15-18).
Sections 6 → 5 et 7 → 6.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

W, H = A4

# ---------------------------------------------------------------------------
# Page templates (cover = no footer / normal = footer)
# ---------------------------------------------------------------------------
def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    y = 1.7 * cm
    canvas.drawString(2.5 * cm, y, f"p. {doc.page}")
    canvas.drawCentredString(W / 2, y, "Youndjeu Tchouapi Alain")
    canvas.drawRightString(W - 2.5 * cm, y, "EAFC Uccle")
    canvas.restoreState()


def _no_footer(canvas, doc):
    pass


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
def S(name, **kw):
    defaults = dict(fontName="Helvetica", fontSize=10, leading=14)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)


COVER_H1  = S("ch1", fontName="Helvetica-Bold", fontSize=22, leading=28, alignment=TA_CENTER)
COVER_H2  = S("ch2", fontName="Helvetica-Bold", fontSize=14, leading=20, alignment=TA_CENTER)
COVER_P   = S("cp",  fontSize=12, leading=16, alignment=TA_CENTER)
COVER_SM  = S("csm", fontSize=11, leading=15, alignment=TA_CENTER)
COVER_BOT = S("cbot",fontName="Helvetica-Bold", fontSize=12, leading=16, alignment=TA_CENTER)

TOC_H = S("toch", fontName="Helvetica-Bold", fontSize=13, leading=18, spaceAfter=12)
TOC_1 = S("toc1", fontName="Helvetica-Bold", fontSize=10, leading=13, spaceAfter=1)
TOC_2 = S("toc2", fontSize=10, leading=13, leftIndent=18, spaceAfter=1)

BODY    = S("body", alignment=TA_JUSTIFY, spaceAfter=8)
BULLET  = S("bull", leftIndent=18, spaceAfter=4)
ITALIC  = S("ita",  fontName="Helvetica-Oblique", fontSize=9, leading=12, spaceAfter=4)
SEC1    = S("s1",   fontName="Helvetica-Bold", fontSize=14, leading=18, spaceBefore=10, spaceAfter=8)
SEC2    = S("s2",   fontName="Helvetica-Bold", fontSize=11, leading=14, spaceBefore=8,  spaceAfter=6)
SEC2B   = S("s2b",  fontName="Helvetica-Bold", fontSize=11, leading=14, spaceBefore=4,  spaceAfter=4)
TH      = S("th",   fontName="Helvetica-Bold", fontSize=9,  leading=12)
TB      = S("tb",   fontSize=9, leading=12)
TBI     = S("tbi",  fontName="Helvetica-Oblique", fontSize=9, leading=12)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
CONTENT_W = W - 5 * cm   # total content width (left+right margin = 5cm)

def th(txt): return Paragraph(txt, TH)
def tb(txt): return Paragraph(txt, TB)
def tbi(txt): return Paragraph(txt, TBI)

def grid_style(header_rows=1):
    ts = [
        ("FONTNAME",     (0, 0), (-1, header_rows - 1), "Helvetica-Bold"),
        ("FONTNAME",     (0, header_rows), (-1, -1),     "Helvetica"),
        ("FONTSIZE",     (0, 0), (-1, -1), 9),
        ("LEADING",      (0, 0), (-1, -1), 12),
        ("GRID",         (0, 0), (-1, -1), 0.5, colors.black),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
        ("LEFTPADDING",  (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]
    return TableStyle(ts)

def sp(n=1): return Spacer(1, n * 0.35 * cm)

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def build():
    out = "/home/user/portfolio-alain/CDC_TFE_Terra_Sana_Alain_modifie.pdf"

    # Two page templates: cover (no footer) and normal (footer)
    cover_frame  = Frame(2.5*cm, 2.5*cm, CONTENT_W, H - 5*cm, id="cover")
    normal_frame = Frame(2.5*cm, 2.8*cm, CONTENT_W, H - 5.3*cm, id="normal")

    doc = BaseDocTemplate(
        out, pagesize=A4,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
        topMargin=2.5*cm,  bottomMargin=2.8*cm,
    )
    doc.addPageTemplates([
        PageTemplate(id="Cover",  frames=[cover_frame],  onPage=_no_footer),
        PageTemplate(id="Normal", frames=[normal_frame], onPage=_footer),
    ])

    story = []

    # =========================================================
    # PAGE 1 – COUVERTURE
    # =========================================================
    story.append(Spacer(1, 2.5*cm))
    story.append(Paragraph("Bachelier en Informatique de Gestion", COVER_H1))
    story.append(sp(0.5))
    story.append(Paragraph("3ème année", COVER_P))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("Cahier des charges", COVER_H1))
    story.append(sp(0.5))
    story.append(Paragraph("Travail de Fin d'Études — Épreuve intégrée", COVER_P))
    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph("Module de gestion des bénévoles et des événements", COVER_H2))
    story.append(sp(0.5))
    story.append(Paragraph("Extension du site web vitrine de Terra Sana ASBL", COVER_P))
    story.append(Spacer(1, 2.5*cm))
    story.append(Paragraph("Encadreur scolaire : Marie-Christine Namur", COVER_SM))
    story.append(sp(0.3))
    story.append(Paragraph("Maître de stage : Didier Seraye", COVER_SM))
    story.append(sp(0.3))
    story.append(Paragraph("Travail présenté par Youndjeu Tchouapi Alain", COVER_SM))
    story.append(Spacer(1, 2.5*cm))
    story.append(Paragraph("<b>EAFC Uccle</b>", COVER_BOT))
    story.append(sp(0.3))
    story.append(Paragraph("2025-2026", COVER_P))

    # Switch to normal template (with footer) for all following pages
    story.append(PageBreak())
    from reportlab.platypus import NextPageTemplate
    story.insert(len(story)-1, NextPageTemplate("Normal"))

    # =========================================================
    # PAGE 2 – TABLE DES MATIÈRES (mise à jour)
    # =========================================================
    story.append(Paragraph("Table des matières", TOC_H))

    def toc_row(label, page, level=1):
        style = TOC_1 if level == 1 else TOC_2
        # Dots line using a table
        t = Table(
            [[Paragraph(label, style), Paragraph(str(page), style)]],
            colWidths=[CONTENT_W - 1*cm, 1*cm],
        )
        t.setStyle(TableStyle([
            ("ALIGN",       (1,0), (1,0), "RIGHT"),
            ("BOTTOMPADDING",(0,0),(-1,-1),1),
            ("TOPPADDING",  (0,0),(-1,-1),1),
            ("LINEBELOW",   (0,0),(0,0), 0.3, colors.lightgrey),
        ]))
        return t

    toc_entries = [
        ("1. Introduction", 3, 1),
        ("2. Fonctionnalités développées durant le stage", 4, 1),
        ("2.1 Contexte et objectif", 4, 2),
        ("2.2 Site public — 12 pages", 4, 2),
        ("2.3 Espace administrateur", 4, 2),
        ("2.4 API REST Backend — 17 endpoints", 4, 2),
        ("2.5 Base de données existante — 4 tables", 6, 2),
        ("2.6 Technologies utilisées", 6, 2),
        ("3. Nouvelles fonctionnalités TFE", 7, 1),
        ("3.1 Refonte graphique", 7, 2),
        ("3.2 Espace personnel bénévole", 7, 2),
        ("3.3 Gestion des événements — côté administrateur", 8, 2),
        ("3.4 Inscription aux événements — côté bénévole", 8, 2),
        ("3.5 Retours post-événement", 9, 2),
        ("3.6 Dashboard administrateur enrichi", 9, 2),
        ("3.7 Fonctionnalités avancées", 9, 2),
        ("3.8 Export PDF et attestation", 9, 2),
        ("4. Analyse technique", 10, 1),
        ("4.1 Nouvelles tables de la base de données", 10, 2),
        ("4.2 Nouveaux endpoints API REST", 12, 2),
        ("4.3 Nouvelles pages frontend", 14, 2),
        ("5. Répartition des tâches / Apport personnel", 15, 1),
        ("5.1 Travail réalisé durant le stage", 15, 2),
        ("5.2 Travail à réaliser dans le cadre du TFE", 15, 2),
        ("5.3 Tableau récapitulatif", 16, 2),
        ("6. Plan de travail", 17, 1),
        ("6.1 Calendrier officiel", 17, 2),
        ("6.2 Plan de développement", 17, 2),
        ("6.3 Dates clés personnelles", 17, 2),
        ("6.4 Contraintes et risques identifiés", 18, 2),
    ]
    for label, page, level in toc_entries:
        story.append(toc_row(label, page, level))

    story.append(PageBreak())

    # =========================================================
    # PAGE 3 – SECTION 1 : INTRODUCTION
    # =========================================================
    story.append(Paragraph("1. Introduction", SEC1))
    story.append(Paragraph(
        "Le présent document constitue le cahier des charges de mon Travail de Fin d'Études, "
        "réalisé dans le cadre de l'épreuve intégrée du Bachelier en Informatique de Gestion "
        "(3ème année) à l'EAFC Uccle, pour l'année académique 2025-2026.", BODY))
    story.append(Paragraph(
        "Mon stage a été effectué au sein de l'association Terra Sana ASBL, dont le siège est "
        "situé au 19 avenue des Volontaires à Auderghem, du 25 mars au 20 mai 2026, sous la "
        "supervision de Monsieur Didier Seraye, Responsable Administratif. Durant cette période, "
        "j'ai conçu et développé de zéro un site web complet servant de vitrine institutionnelle "
        "et de hub centralisé pour les 12 applications internes de l'association.", BODY))
    story.append(Paragraph(
        "Pour le TFE, je propose d'étendre ce projet en y intégrant un module complet de gestion "
        "des bénévoles et des événements. L'intégralité de ce module sera développée par mes "
        "soins, sans code préexistant.", BODY))
    story.append(Paragraph(
        "Aujourd'hui, Terra Sana gère ses bénévoles et ses activités de façon entièrement "
        "manuelle : les coordonnées sont éparpillées dans des fichiers Excel et des carnets "
        "papier, les inscriptions se font par téléphone ou par email, et le suivi des présences "
        "se fait à la main. Cette organisation engendre plusieurs difficultés concrètes :", BODY))
    for bullet in [
        "des doublons et pertes d'information quand plusieurs personnes modifient les mêmes fichiers",
        "aucune vue d'ensemble des places disponibles, d'où des activités surchargées ou sous-remplies",
        "des confirmations et relances envoyées une à une, un travail répétitif et chronophage",
        "aucun historique de participation, ni moyen simple de remercier les bénévoles ou de leur délivrer une attestation",
    ]:
        story.append(Paragraph(f"• {bullet}", BULLET))
    story.append(Paragraph(
        "Le module vise précisément à centraliser et automatiser ces tâches : un espace bénévole "
        "en ligne, une gestion des événements avec places et liste d'attente, des emails de "
        "confirmation automatiques et un historique exploitable (niveaux, attestations). "
        "L'association gagne ainsi en temps et en fiabilité, et les bénévoles disposent d'un "
        "outil simple et moderne.", BODY))
    story.append(PageBreak())

    # =========================================================
    # PAGE 4 – SECTION 2 : FONCTIONNALITÉS STAGE
    # =========================================================
    story.append(Paragraph("2. Fonctionnalités développées durant le stage", SEC1))
    story.append(Paragraph("2.1 Contexte et objectif", SEC2))
    story.append(Paragraph(
        "L'association Terra Sana ASBL ne disposait d'aucune présence numérique avant le stage. "
        "L'objectif était de concevoir et développer un site web moderne, multilingue et évolutif, "
        "permettant de présenter l'association au public et de centraliser l'accès à ses 12 "
        "applications internes via un hub de projets.", BODY))

    story.append(Paragraph("2.2 Site public — 12 pages développées", SEC2))
    pages_data = [
        [th("Page"), th("Description")],
        [tb("Accueil"), tb("Hero section, statistiques clés, aperçu des projets")],
        [tb("À propos"), tb("Mission, valeurs, engagements de l'association")],
        [tb("Projets (Hub)"), tb("Liste des 12 applications avec recherche et filtres")],
        [tb("Détail projet"), tb("Page individuelle par application")],
        [tb("Blog"), tb("Articles publiés par l'administrateur")],
        [tb("Contact"), tb("Formulaire avec validation et compteur de caractères")],
        [tb("Bénévolat"), tb("Formulaire de candidature bénévole")],
        [tb("Sponsors"), tb("Présentation des partenaires")],
        [tb("Confidentialité"), tb("Politique de confidentialité")],
        [tb("Conditions"), tb("Conditions générales d'utilisation")],
        [tb("Cookies"), tb("Politique de gestion des cookies")],
        [tb("Aide / FAQ"), tb("Questions fréquentes")],
    ]
    t = Table(pages_data, colWidths=[4*cm, CONTENT_W - 4*cm])
    t.setStyle(grid_style())
    story.append(t)
    story.append(sp())
    story.append(Paragraph(
        "<i>Le site est entièrement multilingue FR / EN / NL avec sélecteur de langue dans la "
        "barre de navigation.</i>", ITALIC))

    story.append(Paragraph("2.3 Espace administrateur — 2 pages sécurisées", SEC2))
    admin_data = [
        [th("Page"), th("Description")],
        [tb("Connexion (/login)"), tb("Authentification par identifiant + mot de passe, token JWT 24h")],
        [tb("Dashboard (/admin)"), tb("Gestion projets, articles de blog, messages reçus, changement de mot de passe")],
    ]
    t = Table(admin_data, colWidths=[4*cm, CONTENT_W - 4*cm])
    t.setStyle(grid_style())
    story.append(t)

    story.append(Paragraph("2.4 API REST Backend — 17 endpoints", SEC2))
    story.append(PageBreak())

    # =========================================================
    # PAGE 5 – TABLE ENDPOINTS EXISTANTS
    # =========================================================
    ep_data = [
        [th("Méthode"), th("Endpoint"), th("Accès")],
        [tb("POST"),   tb("/api/auth/login"),              tb("Public")],
        [tb("PUT"),    tb("/api/auth/changePassword"),     tb("Admin")],
        [tb("GET"),    tb("/api/projects"),                tb("Public")],
        [tb("GET"),    tb("/api/projects/{id}"),           tb("Public")],
        [tb("POST"),   tb("/api/projects"),                tb("Admin")],
        [tb("PUT"),    tb("/api/projects/{id}"),           tb("Admin")],
        [tb("DELETE"), tb("/api/projects/{id}"),           tb("Admin")],
        [tb("GET"),    tb("/api/posts"),                   tb("Public")],
        [tb("GET"),    tb("/api/posts/{id}"),              tb("Public")],
        [tb("POST"),   tb("/api/posts"),                   tb("Admin")],
        [tb("PUT"),    tb("/api/posts/{id}"),              tb("Admin")],
        [tb("DELETE"), tb("/api/posts/{id}"),              tb("Admin")],
        [tb("GET"),    tb("/api/contact"),                 tb("Admin")],
        [tb("POST"),   tb("/api/contact"),                 tb("Public")],
        [tb("PUT"),    tb("/api/contact/{id}/read"),       tb("Admin")],
        [tb("POST"),   tb("/api/contact/{id}/reply"),      tb("Admin")],
        [tb("DELETE"), tb("/api/contact/{id}"),            tb("Admin")],
    ]
    cw = [2.5*cm, CONTENT_W - 5.5*cm, 2.8*cm]
    t = Table(ep_data, colWidths=cw)
    t.setStyle(grid_style())
    story.append(t)
    story.append(PageBreak())

    # =========================================================
    # PAGE 6 – SECTIONS 2.5 ET 2.6
    # =========================================================
    story.append(Paragraph("2.5 Base de données existante — 4 tables", SEC2))
    db_data = [
        [th("Table"), th("Champs principaux"), th("Rôle")],
        [tb("admin"),
         tb("id, username, password, role"),
         tb("Compte administrateur unique, mot de passe haché (BCrypt)")],
        [tb("project"),
         tb("id, name, description, link, documentationLink, image, category, isActive, createdAt"),
         tb("Applications du hub")],
        [tb("blog_post"),
         tb("id, title, content, image, isPublished, createdAt"),
         tb("Articles du blog")],
        [tb("contact_message"),
         tb("id, name, email, message, isRead, createdAt"),
         tb("Messages des visiteurs")],
    ]
    cw2 = [3*cm, CONTENT_W - 7*cm, 3.8*cm]
    t = Table(db_data, colWidths=cw2)
    t.setStyle(grid_style())
    story.append(t)
    story.append(sp())

    story.append(Paragraph("2.6 Technologies utilisées", SEC2))
    tech_data = [
        [th("Technologie"), th("Version"), th("Usage")],
        [tb("React.js"),              tb("18.2.0"), tb("Frontend — pages, navigation, composants")],
        [tb("Spring Boot"),           tb("Java 21"), tb("Backend — API REST, logique métier")],
        [tb("Spring Security + JWT"), tb("0.11.5"),  tb("Authentification et sécurisation")],
        [tb("MySQL"),                 tb("9.1.0"),   tb("Base de données relationnelle")],
        [tb("BCrypt"),                tb("—"),        tb("Hachage sécurisé des mots de passe")],
        [tb("Git / GitHub"),          tb("—"),        tb("Versioning et hébergement du code source")],
        [tb("WAMP Server"),           tb("3.3.7"),   tb("Environnement local MySQL sous Windows")],
    ]
    cw3 = [4*cm, 2.5*cm, CONTENT_W - 6.7*cm]
    t = Table(tech_data, colWidths=cw3)
    t.setStyle(grid_style())
    story.append(t)
    story.append(PageBreak())

    # =========================================================
    # PAGE 7 – SECTION 3 : NOUVELLES FONCTIONNALITÉS TFE
    # =========================================================
    story.append(Paragraph("3. Nouvelles fonctionnalités TFE", SEC1))
    story.append(Paragraph(
        "Dans le cadre de l'épreuve intégrée, le projet est étendu avec un module complet de "
        "gestion des bénévoles et des événements. Ce module est entièrement nouveau : aucune ligne "
        "de code n'existait pour ces fonctionnalités à la fin du stage.", BODY))

    story.append(Paragraph("3.1 Refonte graphique du site", SEC2))
    story.append(Paragraph(
        "Toutes les pages existantes et nouvelles seront redessinées avec une charte graphique "
        "cohérente, appliquée sur l'ensemble du site y compris l'espace administrateur.", BODY))
    charte_data = [
        [th("Rôle"), th("Couleur"), th("Code hexadécimal")],
        [tb("Couleur principale"), tb("Vert forêt"),  tb("#2D6A4F")],
        [tb("Couleur secondaire"), tb("Vert clair"),  tb("#74C69D")],
        [tb("Accent"),             tb("Or"),           tb("#D4A017")],
        [tb("Fond"),               tb("Blanc crème"),  tb("#F8F4E3")],
        [tb("Texte"),              tb("Noir doux"),    tb("#1B1B1B")],
    ]
    cw4 = [4*cm, 3.5*cm, CONTENT_W - 7.7*cm]
    t = Table(charte_data, colWidths=cw4)
    t.setStyle(grid_style())
    story.append(t)
    story.append(sp())

    story.append(Paragraph("3.2 Espace personnel bénévole", SEC2))
    story.append(Paragraph(
        "Nouvelles pages : /benevoles/inscription — /benevoles/connexion — /benevoles/mon-espace",
        S("note", fontName="Helvetica-Oblique", fontSize=9, leading=12, spaceAfter=6)))
    benv_data = [
        [th("Fonctionnalité"), th("Description")],
        [tb("Création de compte"),   tb("Champs obligatoires : nom, prénom, email, mot de passe (haché BCrypt)")],
        [tb("Profil personnel"),     tb("Champs facultatifs : téléphone, date de naissance, ville et code postal, sexe, compétences, disponibilités, langue préférée (FR/EN/NL)")],
        [tb("Connexion sécurisée"),  tb("Token JWT dédié aux bénévoles, séparé du token administrateur")],
        [tb("Modification du profil"),tb("Le bénévole peut mettre à jour ses informations à tout moment")],
        [tb("Mot de passe oublié"),  tb("Email de réinitialisation avec token sécurisé (Gmail SMTP)")],
        [tb("Niveau bénévole"),      tb("Bronze (1-2 événements) / Argent (3-6) / Or (7+), calculé automatiquement")],
        [tb("Déconnexion"),          tb("Expiration automatique du token après 24h")],
    ]
    cw5 = [4*cm, CONTENT_W - 4*cm]
    t = Table(benv_data, colWidths=cw5)
    t.setStyle(grid_style())
    story.append(t)
    story.append(sp())
    story.append(Paragraph(
        "Conformément au principe de minimisation des données (RGPD), seules les informations "
        "strictement nécessaires à la création du compte sont obligatoires. Les autres champs "
        "restent facultatifs et servent uniquement à l'organisation des activités (localité), "
        "au contact (téléphone) et à l'assurance volontariat (date de naissance).", BODY))
    story.append(PageBreak())

    # =========================================================
    # PAGE 8 – SECTIONS 3.3 ET 3.4
    # =========================================================
    story.append(Paragraph("3.3 Gestion des événements — côté administrateur", SEC2))
    admin_ev_data = [
        [th("Fonctionnalité"), th("Description")],
        [tb("Créer un événement"), tb("Titre, description, date, lieu, nombre de places, photo")],
        [tb("Gérer les statuts"),  tb("OPEN / FULL / CANCELLED / FINISHED")],
        [tb("Valider / refuser"),  tb("L'administrateur accepte ou refuse les inscriptions")],
        [tb("Email groupé"),       tb("Envoi d'un email à tous les bénévoles inscrits")],
        [tb("Supprimer"),          tb("Suppression avec confirmation")],
    ]
    t = Table(admin_ev_data, colWidths=cw5)
    t.setStyle(grid_style())
    story.append(t)
    story.append(sp())

    story.append(Paragraph("3.4 Inscription aux événements — côté bénévole", SEC2))
    insc_data = [
        [th("Fonctionnalité"), th("Description")],
        [tb("Consulter"),       tb("Liste des événements à venir avec date, lieu et places restantes")],
        [tb("S'inscrire"),      tb("Inscription avec email de confirmation automatique")],
        [tb("Se désinscrire"),  tb("Désinscription possible avant la date de l'événement")],
        [tb("Liste d'attente"), tb("Si complet : inscription en file d'attente (status = WAITING)")],
        [tb("Notification"),    tb("Email automatique si une place se libère (WAITING → CONFIRMED)")],
    ]
    t = Table(insc_data, colWidths=cw5)
    t.setStyle(grid_style())
    story.append(t)
    story.append(PageBreak())

    # =========================================================
    # PAGE 9 – SECTIONS 3.5 À 3.8
    # =========================================================
    story.append(Paragraph("3.5 Retours post-événement", SEC2))
    retours_data = [
        [th("Fonctionnalité"),    th("Description")],
        [tb("Laisser un avis"),   tb("Après un événement terminé : note de 1 à 5 étoiles + commentaire")],
        [tb("Consulter les retours"), tb("L'administrateur voit tous les avis depuis le dashboard")],
        [tb("Moyenne des notes"), tb("Note moyenne affichée par événement")],
    ]
    t = Table(retours_data, colWidths=cw5)
    t.setStyle(grid_style())
    story.append(t)
    story.append(sp())

    story.append(Paragraph("3.6 Dashboard administrateur enrichi", SEC2))
    dash_data = [
        [th("Ajout"),                 th("Description")],
        [tb("Onglet Événements"),     tb("Créer, modifier, gérer les statuts, voir les inscrits par événement")],
        [tb("Onglet Bénévoles"),      tb("Liste complète avec filtres (compétence, disponibilité, langue)")],
        [tb("Gestion inscriptions"),  tb("Par événement : inscrits confirmés + liste d'attente")],
        [tb("Statistiques"),          tb("Nombre de bénévoles actifs, événements organisés, taux de participation")],
    ]
    t = Table(dash_data, colWidths=cw5)
    t.setStyle(grid_style())
    story.append(t)
    story.append(sp())

    story.append(Paragraph("3.7 Fonctionnalités avancées", SEC2))
    adv_data = [
        [th("Fonctionnalité"),       th("Description"),                                          th("Technologie")],
        [tb("Graphiques Chart.js"),  tb("Courbe des inscriptions par mois, taux de participation"), tb("Chart.js")],
        [tb("Pagination"),           tb("Sur la liste des événements et des bénévoles"),           tb("Spring Boot Pageable")],
        [tb("Badge notification"),   tb("Nombre d'inscriptions en attente dans la navbar admin"),  tb("React + API")],
        [tb("Tri et filtres avancés"),tb("Filtrer les événements par date, statut, lieu"),         tb("Spring JPA Query")],
        [tb("Niveaux bénévole"),     tb("Bronze / Argent / Or calculé automatiquement"),           tb("Spring Boot")],
    ]
    cw6 = [4*cm, CONTENT_W - 7.5*cm, 3.3*cm]
    t = Table(adv_data, colWidths=cw6)
    t.setStyle(grid_style())
    story.append(t)
    story.append(sp())

    story.append(Paragraph("3.8 Export PDF et attestation", SEC2))
    export_data = [
        [th("Fonctionnalité"),      th("Description"),                                                       th("Accès")],
        [tb("Export liste inscrits"), tb("L'administrateur exporte en PDF la liste des bénévoles inscrits à un événement"), tb("Admin")],
        [tb("Attestation bénévole"), tb("Le bénévole télécharge une attestation PDF de sa participation"),   tb("Bénévole")],
        [tb("Emails fonctionnels"),  tb("Confirmation, liste d'attente, groupe, réinitialisation — via Gmail SMTP"), tb("Automatique")],
    ]
    cw7 = [4*cm, CONTENT_W - 7*cm, 2.8*cm]
    t = Table(export_data, colWidths=cw7)
    t.setStyle(grid_style())
    story.append(t)
    story.append(PageBreak())

    # =========================================================
    # PAGE 10 – SECTION 4.1 TABLES BD (partie 1)
    # =========================================================
    story.append(Paragraph("4. Analyse technique", SEC1))
    story.append(Paragraph("4.1 Nouvelles tables de la base de données — 4 tables", SEC2))

    story.append(Paragraph("Table app_users — Bénévoles", SEC2B))
    users_data = [
        [th("Champ"), th("Type"), th("Contrainte"), th("Description")],
        [tb("id"),                tb("BIGINT"),       tb("PK, AUTO_INCREMENT"), tb("Identifiant unique")],
        [tb("firstName"),         tb("VARCHAR(100)"), tb("NOT NULL"),           tb("Prénom")],
        [tb("lastName"),          tb("VARCHAR(100)"), tb("NOT NULL"),           tb("Nom de famille")],
        [tb("email"),             tb("VARCHAR(200)"), tb("NOT NULL, UNIQUE"),   tb("Email de connexion")],
        [tb("password"),          tb("VARCHAR(255)"), tb("NOT NULL"),           tb("Mot de passe haché (BCrypt)")],
        [tb("phone"),             tb("VARCHAR(30)"),  tb("NULL"),               tb("Numéro de téléphone (facultatif)")],
        [tb("birthDate"),         tb("DATE"),         tb("NULL"),               tb("Date de naissance (facultatif)")],
        [tb("gender"),            tb("VARCHAR(20)"),  tb("NULL"),               tb("Sexe (facultatif)")],
        [tb("city"),              tb("VARCHAR(120)"), tb("NULL"),               tb("Ville (facultatif)")],
        [tb("postalCode"),        tb("VARCHAR(10)"),  tb("NULL"),               tb("Code postal (facultatif)")],
        [tb("skills"),            tb("TEXT"),         tb("NULL"),               tb("Compétences")],
        [tb("availability"),      tb("VARCHAR(200)"), tb("NULL"),               tb("Disponibilités")],
        [tb("preferredLanguage"), tb("VARCHAR(5)"),   tb("DEFAULT fr"),         tb("Langue préférée")],
        [tb("isActive"),          tb("BOOLEAN"),      tb("DEFAULT TRUE"),       tb("Compte actif ou désactivé")],
        [tb("resetToken"),        tb("VARCHAR(255)"), tb("NULL"),               tb("Token de réinitialisation")],
        [tb("resetTokenExpiry"),  tb("DATETIME"),     tb("NULL"),               tb("Expiration du token")],
        [tb("createdAt"),         tb("DATETIME"),     tb("NOT NULL"),           tb("Date d'inscription")],
    ]
    cw8 = [3.5*cm, 3*cm, 3*cm, CONTENT_W - 9.7*cm]
    t = Table(users_data, colWidths=cw8)
    t.setStyle(grid_style())
    story.append(t)
    story.append(sp())

    story.append(Paragraph("Table events — Événements", SEC2B))
    events_data_p1 = [
        [th("Champ"),    th("Type"),        th("Contrainte"),      th("Description")],
        [tb("id"),       tb("BIGINT"),      tb("PK, AUTO_INCREMENT"), tb("Identifiant unique")],
        [tb("admin_id"), tb("BIGINT"),      tb("FK → admin"),      tb("Administrateur créateur")],
    ]
    t = Table(events_data_p1, colWidths=cw8)
    t.setStyle(grid_style())
    story.append(t)
    story.append(PageBreak())

    # =========================================================
    # PAGE 11 – SECTION 4.1 (suite)
    # =========================================================
    events_data_p2 = [
        [th("Champ"),     th("Type"),          th("Contrainte"),    th("Description")],
        [tb("title"),     tb("VARCHAR(200)"),  tb("NOT NULL"),      tb("Titre de l'événement")],
        [tb("description"),tb("TEXT"),         tb("NOT NULL"),      tb("Description complète")],
        [tb("eventDate"), tb("DATETIME"),      tb("NOT NULL"),      tb("Date et heure")],
        [tb("location"),  tb("VARCHAR(300)"),  tb("NOT NULL"),      tb("Lieu")],
        [tb("maxPlaces"), tb("INT"),           tb("NOT NULL"),      tb("Nombre maximum de participants")],
        [tb("status"),    tb("VARCHAR(20)"),   tb("DEFAULT OPEN"),  tb("OPEN / FULL / CANCELLED / FINISHED")],
        [tb("imageUrl"),  tb("VARCHAR(500)"),  tb("NULL"),          tb("Photo de l'événement")],
        [tb("createdAt"), tb("DATETIME"),      tb("NOT NULL"),      tb("Date de création")],
    ]
    t = Table(events_data_p2, colWidths=cw8)
    t.setStyle(grid_style())
    story.append(t)
    story.append(sp())

    story.append(Paragraph("Table registrations — Inscriptions et liste d'attente", SEC2B))
    reg_data = [
        [th("Champ"),    th("Type"),        th("Contrainte"),      th("Description")],
        [tb("id"),       tb("BIGINT"),      tb("PK, AUTO_INCREMENT"), tb("Identifiant unique")],
        [tb("user_id"),  tb("BIGINT"),      tb("FK → app_users"),  tb("Bénévole inscrit")],
        [tb("event_id"), tb("BIGINT"),      tb("FK → events"),     tb("Événement concerné")],
        [tb("status"),   tb("VARCHAR(20)"), tb("NOT NULL"),        tb("CONFIRMED / WAITING / PENDING / REFUSED")],
        [tb("position"), tb("INT"),         tb("NULL"),            tb("Position dans la file d'attente (si WAITING)")],
        [tb("createdAt"),tb("DATETIME"),    tb("NOT NULL"),        tb("Date d'inscription")],
    ]
    t = Table(reg_data, colWidths=cw8)
    t.setStyle(grid_style())
    story.append(t)
    story.append(sp())

    story.append(Paragraph("Table reviews — Retours post-événement", SEC2B))
    rev_data = [
        [th("Champ"),    th("Type"),        th("Contrainte"),      th("Description")],
        [tb("id"),       tb("BIGINT"),      tb("PK, AUTO_INCREMENT"), tb("Identifiant unique")],
        [tb("user_id"),  tb("BIGINT"),      tb("FK → app_users"),  tb("Bénévole ayant laissé l'avis")],
        [tb("event_id"), tb("BIGINT"),      tb("FK → events"),     tb("Événement évalué")],
        [tb("rating"),   tb("INT"),         tb("NOT NULL (1-5)"),  tb("Note de 1 à 5 étoiles")],
        [tb("comment"),  tb("TEXT"),        tb("NULL"),            tb("Commentaire libre")],
        [tb("createdAt"),tb("DATETIME"),    tb("NOT NULL"),        tb("Date de l'avis")],
    ]
    t = Table(rev_data, colWidths=cw8)
    t.setStyle(grid_style())
    story.append(t)
    story.append(PageBreak())

    # =========================================================
    # PAGE 12 – SECTION 4.2 ENDPOINTS (partie 1)
    # =========================================================
    story.append(Paragraph("4.2 Nouveaux endpoints API REST — 30 endpoints", SEC2))

    story.append(Paragraph("Bénévoles — authentification et profil", SEC2B))
    benv_ep = [
        [th("Méthode"), th("Endpoint"),                        th("Accès")],
        [tb("POST"),    tb("/api/benevoles/register"),         tb("Public")],
        [tb("POST"),    tb("/api/benevoles/login"),            tb("Public")],
        [tb("POST"),    tb("/api/benevoles/forgot-password"),  tb("Public")],
        [tb("POST"),    tb("/api/benevoles/reset-password"),   tb("Public")],
        [tb("GET"),     tb("/api/benevoles/profile"),          tb("Bénévole connecté")],
        [tb("PUT"),     tb("/api/benevoles/profile"),          tb("Bénévole connecté")],
        [tb("PUT"),     tb("/api/benevoles/changePassword"),   tb("Bénévole connecté")],
        [tb("GET"),     tb("/api/benevoles/level"),            tb("Bénévole connecté")],
    ]
    cw_ep = [2.5*cm, CONTENT_W - 6.5*cm, 3.8*cm]
    t = Table(benv_ep, colWidths=cw_ep)
    t.setStyle(grid_style())
    story.append(t)
    story.append(sp())

    story.append(Paragraph("Événements", SEC2B))
    ev_ep = [
        [th("Méthode"), th("Endpoint"),                 th("Accès")],
        [tb("GET"),     tb("/api/events"),              tb("Public")],
        [tb("GET"),     tb("/api/events/{id}"),         tb("Public")],
        [tb("POST"),    tb("/api/events"),              tb("Admin")],
        [tb("PUT"),     tb("/api/events/{id}"),         tb("Admin")],
        [tb("DELETE"),  tb("/api/events/{id}"),         tb("Admin")],
        [tb("PUT"),     tb("/api/events/{id}/status"),  tb("Admin")],
        [tb("POST"),    tb("/api/events/{id}/email"),   tb("Admin")],
    ]
    t = Table(ev_ep, colWidths=cw_ep)
    t.setStyle(grid_style())
    story.append(t)
    story.append(sp())

    story.append(Paragraph("Inscriptions", SEC2B))
    insc_ep = [
        [th("Méthode"), th("Endpoint"),                               th("Accès")],
        [tb("POST"),    tb("/api/registrations/{eventId}"),           tb("Bénévole connecté")],
        [tb("DELETE"),  tb("/api/registrations/{eventId}"),           tb("Bénévole connecté")],
        [tb("GET"),     tb("/api/registrations/mes-inscriptions"),    tb("Bénévole connecté")],
        [tb("GET"),     tb("/api/registrations/event/{id}"),          tb("Admin")],
        [tb("PUT"),     tb("/api/registrations/{id}/validate"),       tb("Admin")],
        [tb("PUT"),     tb("/api/registrations/{id}/refuse"),         tb("Admin")],
    ]
    t = Table(insc_ep, colWidths=cw_ep)
    t.setStyle(grid_style())
    story.append(t)
    story.append(PageBreak())

    # =========================================================
    # PAGE 13 – SECTION 4.2 (suite)
    # =========================================================
    story.append(Paragraph("Retours, export et statistiques", SEC2B))
    stats_ep = [
        [th("Méthode"), th("Endpoint"),                          th("Accès")],
        [tb("POST"),    tb("/api/reviews"),                      tb("Bénévole connecté")],
        [tb("GET"),     tb("/api/reviews/event/{id}"),           tb("Public")],
        [tb("GET"),     tb("/api/reviews/admin"),                tb("Admin")],
        [tb("GET"),     tb("/api/benevoles/attestation"),        tb("Bénévole connecté")],
        [tb("GET"),     tb("/api/admin/events/{id}/export"),     tb("Admin")],
        [tb("GET"),     tb("/api/admin/benevoles"),              tb("Admin")],
        [tb("GET"),     tb("/api/admin/stats/inscriptions"),     tb("Admin")],
        [tb("GET"),     tb("/api/admin/stats/participation"),    tb("Admin")],
        [tb("GET"),     tb("/api/admin/notifications/count"),    tb("Admin")],
    ]
    t = Table(stats_ep, colWidths=cw_ep)
    t.setStyle(grid_style())
    story.append(t)
    story.append(PageBreak())

    # =========================================================
    # PAGE 14 – SECTION 4.3 PAGES FRONTEND
    # =========================================================
    story.append(Paragraph("4.3 Nouvelles pages frontend — 7 pages", SEC2))
    pages_fe = [
        [th("Route"),                           th("Page"),                                              th("Accès")],
        [tb("/benevoles/inscription"),           tb("Formulaire d'inscription bénévole"),               tb("Public")],
        [tb("/benevoles/connexion"),             tb("Connexion bénévole"),                              tb("Public")],
        [tb("/benevoles/mot-de-passe-oublie"),  tb("Demande de réinitialisation du mot de passe"),     tb("Public")],
        [tb("/benevoles/reinitialiser"),         tb("Saisie du nouveau mot de passe (via lien email)"), tb("Public")],
        [tb("/benevoles/mon-espace"),            tb("Profil, historique, attestation, niveau bénévole"),tb("Bénévole connecté")],
        [tb("/evenements"),                      tb("Liste des événements avec filtres et pagination"),  tb("Public")],
        [tb("/evenements/:id"),                  tb("Détail d'un événement + inscription"),             tb("Public / Bénévole")],
    ]
    cw_fe = [5*cm, CONTENT_W - 9*cm, 3.8*cm]
    t = Table(pages_fe, colWidths=cw_fe)
    t.setStyle(grid_style())
    story.append(t)
    story.append(PageBreak())

    # =========================================================
    # PAGE 15 – SECTION 5 (était 6) : RÉPARTITION DES TÂCHES
    # =========================================================
    story.append(Paragraph("5. Répartition des tâches / Apport personnel", SEC1))

    story.append(Paragraph("5.1 Travail réalisé durant le stage — base technique existante", SEC2))
    stage_data = [
        [th("Composant"),              th("Description"),                                                          th("Statut")],
        [tb("Site public multilingue"),tb("12 pages React (Accueil, À propos, Projets, Blog, Contact, Bénévolat…)"),tb("Existant")],
        [tb("Hub des 12 applications"),tb("Affichage dynamique avec recherche et filtres par catégorie"),          tb("Existant")],
        [tb("Panel administrateur"),   tb("Dashboard complet : projets, blog, messages, changement de mot de passe"),tb("Existant")],
        [tb("Authentification JWT"),   tb("Connexion admin sécurisée avec BCrypt"),                               tb("Existant")],
        [tb("API REST backend"),       tb("17 endpoints sur 4 ressources"),                                        tb("Existant")],
        [tb("Base de données MySQL"),  tb("4 tables : admin, project, blog_post, contact_message"),               tb("Existant")],
        [tb("Envoi d'emails"),         tb("Réponse aux messages via Gmail SMTP"),                                  tb("Existant")],
    ]
    cw9 = [3.8*cm, CONTENT_W - 6.8*cm, 2.8*cm]
    t = Table(stage_data, colWidths=cw9)
    t.setStyle(grid_style())
    story.append(t)
    story.append(sp())

    story.append(Paragraph("5.2 Travail à réaliser dans le cadre du TFE", SEC2))
    story.append(Paragraph(
        "Tout ce qui suit sera développé entièrement par moi, à domicile. Aucune de ces "
        "fonctionnalités n'existait à la fin du stage.", BODY))
    tfe_data = [
        [th("Composant"),              th("Description"),                                               th("Technologie")],
        [tb("Refonte graphique"),      tb("Nouvelle charte sur toutes les pages (public + admin)"),    tb("React / CSS")],
        [tb("Espace bénévole"),        tb("Inscription, connexion, profil, mot de passe oublié, niveau"),tb("React + Spring Boot")],
        [tb("Gestion événements"),     tb("CRUD admin, email groupé, export PDF liste inscrits"),      tb("React + Spring Boot")],
        [tb("Page événements"),        tb("Liste publique avec filtres, pagination, détail"),          tb("React")],
        [tb("Système inscription"),    tb("Inscription + email de confirmation automatique"),          tb("Spring Boot + JavaMail")],
        [tb("Liste d'attente"),        tb("status = WAITING + position dans Registration"),            tb("Spring Boot")],
        [tb("Retours événement"),      tb("Formulaire d'avis (note + commentaire)"),                  tb("React + Spring Boot")],
        [tb("Dashboard enrichi"),      tb("Onglets bénévoles + événements + statistiques"),           tb("React + Spring Boot")],
        [tb("Graphiques Chart.js"),    tb("Dashboard admin : courbes et statistiques"),               tb("Chart.js")],
        [tb("Pagination"),             tb("Événements et liste bénévoles"),                           tb("Spring Pageable")],
        [tb("Badge notification"),     tb("Inscriptions en attente dans la navbar admin"),            tb("React + API")],
    ]
    cw10 = [3.8*cm, CONTENT_W - 7.8*cm, 3.8*cm]
    t = Table(tfe_data, colWidths=cw10)
    t.setStyle(grid_style())
    story.append(t)
    story.append(PageBreak())

    # =========================================================
    # PAGE 16 – SECTION 5.3 TABLEAU RÉCAPITULATIF
    # =========================================================
    tfe_data2 = [
        [th("Composant"),          th("Description"),                                           th("Technologie")],
        [tb("Niveaux bénévole"),   tb("Bronze / Argent / Or calculé automatiquement"),         tb("Spring Boot")],
        [tb("Export PDF"),         tb("Attestation + liste inscrits par événement"),           tb("iText / JasperReports")],
        [tb("4 nouvelles tables BD"),tb("app_users, events, registrations, reviews"),          tb("MySQL")],
        [tb("30 nouveaux endpoints"),tb("API REST couvrant toutes les nouvelles fonctionnalités"),tb("Spring Boot REST")],
        [tb("7 nouvelles pages"),  tb("Espace bénévole + pages événements"),                  tb("React")],
    ]
    t = Table(tfe_data2, colWidths=cw10)
    t.setStyle(grid_style())
    story.append(t)
    story.append(sp())

    story.append(Paragraph("5.3 Tableau récapitulatif", SEC2))
    recap_data = [
        [th("Critère"),           th("Stage"),     th("TFE (apport personnel)")],
        [tb("Tables BD"),         tb("4"),         tb("+4 nouvelles (8 au total)")],
        [tb("Endpoints API"),     tb("17"),        tb("+30 nouveaux (47 au total)")],
        [tb("Pages frontend"),    tb("14"),        tb("+7 nouvelles (21 au total)")],
        [tb("Pages redessinées"), tb("0"),         tb("14 pages existantes refaites")],
        [tb("Module bénévoles"),  tb("Aucun"),     tb("Module complet (inscription, profil, niveaux)")],
        [tb("Gestion événements"),tb("Aucune"),    tb("Module complet (CRUD, inscriptions, retours)")],
    ]
    cw11 = [4*cm, 2.5*cm, CONTENT_W - 6.7*cm]
    t = Table(recap_data, colWidths=cw11)
    t.setStyle(grid_style())
    story.append(t)
    story.append(sp())
    story.append(Paragraph(
        "Le travail réalisé durant le stage constitue la fondation technique du projet "
        "(architecture, base de données initiale, site public, panel administrateur). Le TFE "
        "consiste à étendre significativement cette base en y ajoutant un module entièrement "
        "nouveau, ainsi qu'une refonte complète de l'interface graphique. L'intégralité du module "
        "TFE est développée de zéro par l'étudiant.", BODY))
    story.append(PageBreak())

    # =========================================================
    # PAGE 17 – SECTION 6 (était 7) : PLAN DE TRAVAIL
    # =========================================================
    story.append(Paragraph("6. Plan de travail", SEC1))

    story.append(Paragraph("6.1 Calendrier officiel — 2ème session", SEC2))
    cal_data = [
        [th("Date limite"), th("Échéance")],
        [tb("03/07/2026"),  tb("Remise du cahier des charges (PDF)")],
        [tb("28/08/2026"),  tb("Validation de l'analyse par l'encadreur scolaire")],
        [tb("15/09/2026"),  tb("Validation de l'application")],
        [tb("22/09/2026"),  tb("Remise du rapport écrit provisoire (PDF sur Teams)")],
        [tb("29/09/2026"),  tb("Remise du rapport écrit définitif (PDF + 5 exemplaires + GitHub)")],
        [tb("13/10/2026"),  tb("Défenses orales")],
    ]
    cw12 = [3*cm, CONTENT_W - 3*cm]
    t = Table(cal_data, colWidths=cw12)
    t.setStyle(grid_style())
    story.append(t)
    story.append(sp())

    story.append(Paragraph("6.2 Plan de développement", SEC2))
    dev_data = [
        [th("Phase"),                     th("Contenu"),                                                   th("Période"),          th("Statut")],
        [tb("Phase 1 Analyse & CDC"),      tb("Analyse de l'existant, rédaction du cahier des charges"),   tb("Mai – Juil. 2026"), tb("En cours")],
        [tb("Phase 2 Refonte graphique"),  tb("Application de la charte sur toutes les pages"),            tb("Début juil. 2026"), tb("À faire")],
        [tb("Phase 3 Backend nouvelles entités"), tb("Entités Java, repositories, controllers, JWT, Gmail SMTP"), tb("Juillet 2026"), tb("À faire")],
        [tb("Phase 4 Frontend bénévoles"), tb("Inscription, connexion, profil, mot de passe oublié"),      tb("Juil. – Août 2026"),tb("À faire")],
        [tb("Phase 5 Frontend événements"),tb("Liste, détail, inscription, retours"),                      tb("Août 2026"),        tb("À faire")],
        [tb("Phase 6 Fonctionnalités avancées"), tb("Chart.js, pagination, badge, filtres, niveaux"),     tb("Août – Sept. 2026"),tb("À faire")],
        [tb("Phase 7 Tests & corrections"),tb("Tests complets, corrections, validation encadreur"),        tb("Septembre 2026"),   tb("À faire")],
        [tb("Phase 8 Rapport & finalisation"), tb("Rapport écrit, GitHub, 5 exemplaires, soutenance"),    tb("Sept. – Oct. 2026"),tb("À faire")],
    ]
    cw13 = [4*cm, CONTENT_W - 9.5*cm, 3.5*cm, 1.8*cm]
    t = Table(dev_data, colWidths=cw13)
    t.setStyle(grid_style())
    story.append(t)
    story.append(sp())

    story.append(Paragraph("6.3 Dates clés personnelles", SEC2))
    dates_data = [
        [th("Date"),        th("Action")],
        [tb("03/07/2026"),  tb("Envoi du CDC finalisé à Madame Marie-Christine Namur")],
        [tb("28/08/2026"),  tb("Présentation de l'analyse validée (schéma BD + architecture)")],
        [tb("15/09/2026"),  tb("Application complète et fonctionnelle")],
        [tb("22/09/2026"),  tb("Rapport provisoire soumis sur Teams")],
        [tb("29/09/2026"),  tb("Rapport définitif + code GitHub + 5 exemplaires au secrétariat")],
        [tb("13/10/2026"),  tb("Défense orale devant le jury")],
    ]
    t = Table(dates_data, colWidths=cw12)
    t.setStyle(grid_style())
    story.append(t)
    story.append(PageBreak())

    # =========================================================
    # PAGE 18 – SECTION 6.4 CONTRAINTES ET RISQUES
    # =========================================================
    story.append(Paragraph("6.4 Contraintes et risques identifiés", SEC2))
    story.append(Paragraph(
        "Plusieurs contraintes techniques et organisationnelles ont été anticipées dès la phase "
        "d'analyse. Le tableau ci-dessous recense les principaux risques susceptibles d'affecter "
        "le projet, ainsi que les mesures concrètes prévues pour les limiter.", BODY))
    risks_data = [
        [th("Contrainte / Risque"),                       th("Mesure prévue")],
        [tb("Délai serré de la 2ème session\n(juillet à octobre 2026)"),
         tb("Découpage du travail en huit phases planifiées (point 6.2) et suivi régulier des dates clés afin de détecter tout retard au plus tôt.")],
        [tb("Dépendance au service Gmail SMTP pour l'envoi des e-mails"),
         tb("Utilisation d'un mot de passe d'application dédié ; en cas d'indisponibilité, les notifications restent consultables directement dans l'espace bénévole.")],
        [tb("Sécurité des données personnelles des bénévoles"),
         tb("Mots de passe chiffrés avec BCrypt, authentification par jeton JWT et contrôle des accès par rôle (administrateur / bénévole).")],
        [tb("Compatibilité navigateurs et affichage multilingue (FR/EN/NL)"),
         tb("Interface responsive testée sur les principaux navigateurs et relecture systématique des trois versions linguistiques avant la remise.")],
        [tb("Perte de code ou de données en cours de développement"),
         tb("Versionnage du projet sur GitHub avec sauvegardes régulières et base de données exportée à chaque étape importante.")],
    ]
    cw14 = [5*cm, CONTENT_W - 5*cm]
    t = Table(risks_data, colWidths=cw14)
    t.setStyle(grid_style())
    story.append(t)

    # Build
    doc.build(story)
    print(f"PDF généré : {out}")

if __name__ == "__main__":
    build()
