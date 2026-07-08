#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Document séparé — Diagrammes UML (cas d'utilisation + classes) et analyse.
Réutilise les fonctions de dessin et les styles de generate_cdc.py.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, NextPageTemplate,
    Paragraph, Spacer, PageBreak, KeepTogether,
)

import generate_cdc as G
from generate_cdc import (
    W, H, ML, MR, CW,
    diag_use_case, diag_classes,
    BODY, SEC1, SEC2, ITAL, NOTE,
    CV_TITLE, CV_SUB, CV_MOD, CV_EXT, CV_INFO, CV_INST, CV_YEAR,
    sp, grid, th, tb,
)

OUT = "/home/user/portfolio-alain/Diagrammes_UML_Terra_Sana_Alain.pdf"


def build():
    cov_fr = Frame(ML, 2.0*cm, CW, H-4.0*cm, id="cover")
    nor_fr = Frame(ML, 2.5*cm, CW, H-5.0*cm, id="normal")

    doc = BaseDocTemplate(OUT, pagesize=A4,
        leftMargin=ML, rightMargin=MR,
        topMargin=2.5*cm, bottomMargin=2.5*cm)
    doc.addPageTemplates([
        PageTemplate(id="Cover",  frames=[cov_fr], onPage=G._no_footer),
        PageTemplate(id="Normal", frames=[nor_fr], onPage=G._footer),
    ])

    S = []

    # ═══════════════════════════════════════════════════════
    # P1 — COUVERTURE
    # ═══════════════════════════════════════════════════════
    S.append(Spacer(1, 2.2*cm))
    S.append(Paragraph("Diagrammes UML", CV_TITLE))
    S.append(sp(0.4))
    S.append(Paragraph("Diagramme de cas d'utilisation &amp; diagramme de classes",
                       CV_SUB))
    S.append(Spacer(1, 1.6*cm))
    S.append(Paragraph("Module de gestion des bénévoles et des événements", CV_MOD))
    S.append(sp(0.3))
    S.append(Paragraph("Extension du site web vitrine de Terra Sana ASBL", CV_EXT))
    S.append(Spacer(1, 1.6*cm))
    S.append(Paragraph(
        "Document complémentaire au cahier des charges (déjà transmis). "
        "Il rassemble les deux diagrammes demandés ainsi qu'une analyse "
        "détaillée, en particulier pour le diagramme de classes.",
        ITAL))
    S.append(Spacer(1, 1.4*cm))
    S.append(Paragraph("Encadreur scolaire : Marie-Christine Namur", CV_INFO))
    S.append(sp(0.2))
    S.append(Paragraph("Maître de stage : Didier Seraye", CV_INFO))
    S.append(sp(0.2))
    S.append(Paragraph("Travail présenté par Youndjeu Tchouapi Alain", CV_INFO))
    S.append(Spacer(1, 1.8*cm))
    S.append(Paragraph("<b>EAFC Uccle</b>", CV_INST))
    S.append(sp(0.3))
    S.append(Paragraph("2025-2026", CV_YEAR))
    S.append(NextPageTemplate("Normal"))
    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P2 — DIAGRAMME DE CAS D'UTILISATION
    # ═══════════════════════════════════════════════════════
    S.append(Paragraph("1. Diagramme de cas d'utilisation", SEC1))
    S.append(Paragraph(
        "Le diagramme ci-dessous décrit les interactions entre les acteurs et "
        "le module. Il distingue le périmètre côté bénévole du périmètre "
        "d'administration, tout en restant dans une seule frontière système "
        "puisqu'il s'agit d'une même application.", BODY))
    S.append(sp(0.2))
    S.append(diag_use_case())
    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P3 — ANALYSE DU DIAGRAMME DE CAS D'UTILISATION
    # ═══════════════════════════════════════════════════════
    S.append(Paragraph("1.1 Les acteurs", SEC2))
    S.append(Paragraph(
        "Trois acteurs interagissent avec le module :", BODY))
    S.append(Paragraph(
        "<b>• Visiteur</b> — internaute non authentifié. Il peut consulter le "
        "site vitrine et la liste des événements, puis créer un compte pour "
        "aller plus loin.", G.BULL))
    S.append(Paragraph(
        "<b>• Bénévole</b> — visiteur qui s'est authentifié. Le lien de "
        "<b>généralisation</b> (flèche à triangle creux) indique qu'un "
        "bénévole <i>est un</i> visiteur : il hérite de toutes ses "
        "possibilités et y ajoute les siennes (inscription aux événements, "
        "profil, historique, attestations, avis).", G.BULL))
    S.append(Paragraph(
        "<b>• Administrateur</b> — membre de Terra Sana qui gère le module "
        "depuis l'espace d'administration (événements, inscriptions, "
        "communication, tableau de bord).", G.BULL))
    S.append(sp(0.15))

    S.append(Paragraph("1.2 Les relations «include» et «extend»", SEC2))
    S.append(Paragraph(
        "Deux relations de dépendance enrichissent le modèle et traduisent "
        "des règles métier concrètes :", BODY))
    S.append(Paragraph(
        "<b>• «extend»</b> — « Rejoindre la liste d'attente » <b>étend</b> "
        "« S'inscrire à un événement ». C'est un comportement <i>optionnel</i>, "
        "déclenché uniquement sous condition : lorsque l'événement a atteint "
        "son nombre maximum de places, le bénévole est basculé en liste "
        "d'attente au lieu d'être inscrit directement.", G.BULL))
    S.append(Paragraph(
        "<b>• «include»</b> — « Valider / refuser les inscriptions » "
        "<b>inclut</b> « Envoyer des emails ». L'envoi d'une notification au "
        "bénévole concerné fait <i>systématiquement</i> partie du traitement : "
        "il n'y a pas de validation ou de refus sans email de confirmation. "
        "La relation « include » exprime précisément ce comportement "
        "obligatoire et réutilisable.", G.BULL))
    S.append(sp(0.15))
    S.append(Paragraph(
        "Rappel de notation : trait plein + triangle creux = généralisation ; "
        "flèche en pointillés + pointe ouverte = dépendance «include» / "
        "«extend».", NOTE))
    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P4 — DIAGRAMME DE CLASSES
    # ═══════════════════════════════════════════════════════
    S.append(Paragraph("2. Diagramme de classes", SEC1))
    S.append(Paragraph(
        "Le diagramme présente le modèle de données du module. Les cinq "
        "classes du haut sont créées dans le cadre du TFE ; les trois classes "
        "situées sous le séparateur existent déjà dans la base actuelle et "
        "sont rappelées pour montrer leur rattachement à l'administrateur.",
        BODY))
    S.append(sp(0.2))
    S.append(diag_classes())
    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P5 — ANALYSE DU DIAGRAMME DE CLASSES (1)
    # ═══════════════════════════════════════════════════════
    S.append(Paragraph("2.1 Rôle de chaque classe", SEC2))
    rows = [
        [th("Classe"), th("Rôle dans le module")],
        [tb("<b>AppUser</b>"),
         tb("Représente un bénévole. Entité centrale du TFE : porte "
            "l'identité, l'authentification (email unique, mot de passe "
            "chiffré) et les méthodes métier (niveau de fidélité, génération "
            "d'attestation).")],
        [tb("<b>Event</b>"),
         tb("Un événement organisé par Terra Sana : date, lieu, nombre de "
            "places, statut (ouvert / complet / clôturé), visuel. Seconde "
            "entité centrale du module.")],
        [tb("<b>Registration</b>"),
         tb("Classe d'<b>association</b> entre AppUser et Event. Elle "
            "matérialise l'inscription et porte ses propres attributs : "
            "statut (confirmée / en attente / refusée) et position dans la "
            "file d'attente.")],
        [tb("<b>Review</b>"),
         tb("Un avis laissé par un bénévole sur un événement auquel il a "
            "participé (note de 1 à 5 et commentaire).")],
        [tb("<b>Admin</b>"),
         tb("Compte d'administration qui gère l'ensemble du module et les "
            "contenus existants du site.")],
    ]
    S.append(grid([3.2*cm, CW-3.2*cm], rows))
    S.append(sp(0.25))

    S.append(Paragraph("2.2 Attributs et contraintes remarquables", SEC2))
    S.append(Paragraph(
        "<b>• Sécurité</b> — les mots de passe (AppUser, Admin) ne sont jamais "
        "stockés en clair : la contrainte <font face='Courier'>{BCrypt}</font> "
        "rappelle qu'ils sont hachés. L'email de AppUser porte la contrainte "
        "<font face='Courier'>{UNIQUE}</font> pour empêcher les doublons de "
        "compte.", G.BULL))
    S.append(Paragraph(
        "<b>• Intégrité</b> — la note d'un avis est bornée par "
        "<font face='Courier'>{1..5}</font> ; le champ "
        "<font face='Courier'>status</font> d'Event et de Registration prend "
        "ses valeurs dans un ensemble fermé (énumération).", G.BULL))
    S.append(Paragraph(
        "<b>• Méthodes métier</b> — <font face='Courier'>getLevel()</font> "
        "calcule le niveau de fidélité du bénévole à partir de son nombre de "
        "participations ; <font face='Courier'>generateAttestation()</font> "
        "produit l'attestation PDF. Elles sont placées dans le troisième "
        "compartiment des classes concernées.", G.BULL))
    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P6 — ANALYSE DU DIAGRAMME DE CLASSES (2)
    # ═══════════════════════════════════════════════════════
    S.append(Paragraph("2.3 Associations et cardinalités", SEC2))
    rows = [
        [th("Association"), th("Card."), th("Lecture")],
        [tb("AppUser — Registration"), tb("1 → 0..*"),
         tb("Un bénévole possède plusieurs inscriptions ; une inscription "
            "appartient à un seul bénévole.")],
        [tb("Event — Registration"), tb("1 → 0..*"),
         tb("Un événement reçoit plusieurs inscriptions ; une inscription "
            "concerne un seul événement.")],
        [tb("AppUser — Review"), tb("1 → 0..*"),
         tb("Un bénévole peut rédiger plusieurs avis.")],
        [tb("Event — Review"), tb("1 → 0..*"),
         tb("Un événement peut recevoir plusieurs avis.")],
        [tb("Admin — Event"), tb("1 → 0..*"),
         tb("Un administrateur crée et gère de nombreux événements.")],
        [tb("Admin — Registration"), tb("1 → 0..*"),
         tb("L'administrateur valide ou refuse les inscriptions.")],
    ]
    S.append(grid([4.6*cm, 1.9*cm, CW-6.5*cm], rows))
    S.append(sp(0.2))
    S.append(Paragraph(
        "La classe <b>Registration</b> est le pivot du modèle : en la plaçant "
        "entre AppUser et Event, on transforme une relation « plusieurs à "
        "plusieurs » (un bénévole s'inscrit à plusieurs événements, un "
        "événement accueille plusieurs bénévoles) en deux relations « un à "
        "plusieurs » exploitables, tout en offrant un endroit naturel pour "
        "stocker le statut et la position en liste d'attente.", BODY))
    S.append(sp(0.2))

    S.append(Paragraph("2.4 Choix de conception", SEC2))
    S.append(Paragraph(
        "<b>• Séparation visuelle</b> — les classes existantes (Project, "
        "BlogPost, ContactMessage) sont regroupées sous un séparateur en "
        "pointillés. On voit d'un coup d'œil ce qui est ajouté par le TFE et "
        "ce qui préexiste, sans réécrire l'existant.", G.BULL))
    S.append(Paragraph(
        "<b>• Réutilisation de l'administrateur</b> — l'Admin déjà présent "
        "pilote aussi les nouvelles entités (liens en pointillés vers les "
        "classes existantes), ce qui évite de dupliquer un compte de gestion.",
        G.BULL))
    S.append(Paragraph(
        "<b>• Cohérence avec le code</b> — chaque classe correspond à une "
        "entité JPA (Spring Boot) et à une table MySQL ; les attributs et "
        "types reflètent directement le schéma de la base.", G.BULL))
    S.append(sp(0.2))
    S.append(Paragraph(
        "Les deux diagrammes sont cohérents entre eux : chaque cas "
        "d'utilisation manipule une ou plusieurs de ces classes "
        "(« S'inscrire à un événement » crée une Registration, « Laisser un "
        "avis » crée une Review, « Gérer les événements » agit sur Event, "
        "etc.).", NOTE))

    doc.build(S)
    print(f"PDF généré : {OUT}")


if __name__ == "__main__":
    build()
