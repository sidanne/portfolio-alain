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
        "<b>• Visiteur</b> — internaute non authentifié. Ses seuls cas "
        "d'utilisation sont : consulter le site vitrine, consulter la liste "
        "des événements et créer un compte. Dès qu'il se connecte, il "
        "devient bénévole ; « Se connecter » et « Réinitialiser son mot de "
        "passe » sont donc rattachés au Bénévole, pas au Visiteur.",
        G.BULL))
    S.append(Paragraph(
        "<b>• Bénévole</b> — visiteur qui s'est authentifié. Le lien de "
        "<b>généralisation</b> (flèche à triangle creux) indique qu'un "
        "bénévole <i>est un</i> visiteur : il hérite de ses cas d'utilisation "
        "(consulter le site et les événements, créer un compte) et y ajoute "
        "les siens : se connecter, réinitialiser son mot de passe, gérer son "
        "profil, s'inscrire à un événement, rejoindre la liste d'attente, "
        "se désinscrire, consulter son historique, télécharger une "
        "attestation, laisser un avis.", G.BULL))
    S.append(Paragraph(
        "<b>• Administrateur</b> — membre de Terra Sana qui gère le module "
        "depuis l'espace d'administration. Il dispose de ses propres cas "
        "d'authentification et de gestion de compte (se connecter, "
        "réinitialiser son mot de passe, gérer son profil) et pilote le "
        "module : gestion des événements, validation des inscriptions, "
        "communication, gestion des bénévoles, consultation des avis, "
        "tableau de bord et export.", G.BULL))
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
        "<b>inclut</b> « Envoyer un email de confirmation ». L'envoi de cette "
        "notification au bénévole concerné fait <i>systématiquement</i> "
        "partie du traitement : il n'y a pas de validation ou de refus sans "
        "email de confirmation. La relation « include » exprime précisément "
        "ce comportement obligatoire et réutilisable.", G.BULL))
    S.append(sp(0.1))
    S.append(Paragraph(
        "« Envoyer des emails groupés » est en revanche un cas d'utilisation "
        "<i>indépendant</i> : l'administrateur peut, à tout moment, notifier "
        "l'ensemble des bénévoles inscrits à un événement (rappel, "
        "changement de lieu, annulation), sans que cette action soit liée à "
        "une validation d'inscription précise.", BODY))
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
        "Le diagramme présente les huit entités du modèle de données avec "
        "leurs attributs, leurs méthodes et leurs associations nommées. Les "
        "liens entre classes sont représentés uniquement par les associations "
        "(les clés étrangères ne sont donc pas affichées comme attributs). "
        "AppUser, Event, Review et Registration sont créées dans le cadre du "
        "TFE ; Admin, Project, BlogPost et ContactMessage proviennent du "
        "site existant.", BODY))
    S.append(sp(0.1))
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
            "l'identité et le profil complet (coordonnées, compétences, "
            "disponibilités), l'authentification (connexion, mot de passe "
            "oublié / réinitialisé), le niveau de fidélité (Bronze / Argent "
            "/ Or) et le téléchargement de l'attestation.")],
        [tb("<b>Event</b>"),
         tb("Un événement organisé par Terra Sana : date, lieu, nombre de "
            "places, statut (ouvert / complet / annulé / clôturé), visuel. "
            "Seconde entité centrale du module.")],
        [tb("<b>Registration</b>"),
         tb("Entité <b>associative</b> entre AppUser et Event. Elle "
            "matérialise l'inscription et porte ses propres attributs : "
            "statut (RegistrationStatus : CONFIRMED / WAITING / REFUSED) et "
            "position dans la file d'attente. Une association « valide » avec "
            "Admin (0..1) trace l'administrateur qui l'a traitée.")],
        [tb("<b>Review</b>"),
         tb("Un avis laissé par un bénévole sur un événement auquel il a "
            "participé (note de 1 à 5 et commentaire).")],
        [tb("<b>Admin</b>"),
         tb("Compte d'administration existant. Il gère l'ensemble du module "
            "(événements, inscriptions, bénévoles, avis, tableau de bord) et "
            "les contenus déjà présents sur le site (Project, BlogPost, "
            "ContactMessage), tout en assurant la gestion de son propre "
            "compte (connexion, mot de passe, profil).")],
    ]
    S.append(grid([3.2*cm, CW-3.2*cm], rows))
    S.append(sp(0.25))

    S.append(Paragraph("2.2 Attributs, énumérations et méthodes", SEC2))
    S.append(Paragraph(
        "<b>• Identifiants</b> — chaque classe possède un identifiant "
        "<font face='Courier'>id : Long «PK»</font>. Les liens entre "
        "classes ne sont pas dupliqués sous forme d'attributs « clé "
        "étrangère » : ils sont portés par les associations nommées du "
        "diagramme (« effectue », « accueille », etc.).", G.BULL))
    S.append(Paragraph(
        "<b>• Énumérations</b> — trois attributs prennent leurs valeurs dans "
        "un ensemble fermé et sont typés par une énumération dédiée. Chaque "
        "énumération est représentée par sa propre boîte «enumeration» "
        "reliée à la classe utilisatrice par une flèche de dépendance "
        "(pointillés + pointe ouverte) : "
        "<font face='Courier'>EventStatus</font> "
        "(OPEN / FULL / CANCELLED / FINISHED) pour "
        "<font face='Courier'>Event.status</font>, "
        "<font face='Courier'>RegistrationStatus</font> "
        "(CONFIRMED / WAITING / REFUSED) pour "
        "<font face='Courier'>Registration.status</font>, et "
        "<font face='Courier'>Level</font> (BRONZE / ARGENT / OR) pour "
        "<font face='Courier'>AppUser.level</font>. Ce typage rend les "
        "valeurs autorisées explicites et évite les chaînes libres.", G.BULL))
    S.append(Paragraph(
        "<b>• Méthodes métier</b> — <font face='Courier'>confirm()</font>, "
        "<font face='Courier'>refuse()</font>, "
        "<font face='Courier'>promoteFromWaiting()</font> et "
        "<font face='Courier'>sendConfirmationEmail()</font> sur "
        "Registration ; <font face='Courier'>getAvailablePlaces()</font>, "
        "<font face='Courier'>isFull()</font> et "
        "<font face='Courier'>exportPDF()</font> sur Event ; "
        "<font face='Courier'>downloadAttestation()</font> et "
        "<font face='Courier'>getLevel()</font> sur AppUser.", G.BULL))
    S.append(Paragraph(
        "<b>• Sécurité (implémentation)</b> — les mots de passe ne sont jamais "
        "stockés en clair (hachage BCrypt côté Spring Security) et l'email de "
        "AppUser est unique en base ; ces règles sont portées par les "
        "contraintes de la base et la couche service.", G.BULL))
    S.append(sp(0.15))
    S.append(Paragraph(
        "Les méthodes de Project, BlogPost et ContactMessage "
        "(<font face='Courier'>activate()</font>, "
        "<font face='Courier'>publish()</font>, "
        "<font face='Courier'>reply()</font>, etc.) appartiennent à des "
        "fonctionnalités du site déjà existantes, hors du périmètre "
        "« Module Bénévoles &amp; Événements » : c'est pourquoi elles "
        "n'apparaissent pas dans le diagramme de cas d'utilisation, qui ne "
        "couvre que le nouveau module.", NOTE))
    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P6 — ANALYSE DU DIAGRAMME DE CLASSES (2)
    # ═══════════════════════════════════════════════════════
    S.append(Paragraph("2.3 Associations et cardinalités", SEC2))
    S.append(Paragraph(
        "Chaque association est nommée par un verbe métier et porte ses "
        "cardinalités. Associations propres au module TFE :", BODY))
    rows = [
        [th("Association"), th("Verbe"), th("Card."), th("Lecture")],
        [tb("AppUser → Registration"), tb("effectue"), tb("1 → 0..*"),
         tb("Un bénévole effectue plusieurs inscriptions ; chaque inscription "
            "appartient à un seul bénévole.")],
        [tb("Event → Registration"), tb("accueille"), tb("1 → 0..*"),
         tb("Un événement accueille plusieurs inscriptions ; chaque "
            "inscription concerne un seul événement.")],
        [tb("AppUser → Review"), tb("rédige"), tb("1 → 0..*"),
         tb("Un bénévole peut rédiger plusieurs avis.")],
        [tb("Review → Event"), tb("concerne"), tb("0..* → 1"),
         tb("Un avis concerne un seul événement ; un même événement peut en "
            "recevoir plusieurs.")],
        [tb("Admin → Registration"), tb("valide"), tb("0..1 → 0..*"),
         tb("Une inscription est traitée par au plus un administrateur (zéro "
            "tant qu'elle est en attente) ; un administrateur peut traiter "
            "plusieurs inscriptions.")],
    ]
    S.append(grid([3.9*cm, 1.9*cm, 1.9*cm, CW-7.7*cm], rows))
    S.append(sp(0.15))
    S.append(Paragraph(
        "L'administrateur, lui, pilote aussi bien les nouvelles entités que "
        "les contenus existants : il <b>crée</b> les Event (1 → 0..*), "
        "<b>valide</b> les Registration (0..1 → 0..*, puisqu'une inscription "
        "en attente n'a encore été traitée par personne), et <b>gère</b> / "
        "<b>publie</b> / <b>reçoit</b> respectivement les Project, BlogPost "
        "et ContactMessage du site. L'association <b>Admin — Registration</b> "
        "rend explicite le lien entre l'administrateur et la validation des "
        "inscriptions, plutôt que de le laisser seulement implicite via "
        "Event.", BODY))
    S.append(sp(0.1))
    S.append(Paragraph(
        "Le verbe « <b>accueille</b> » remplace ici « reçoit » pour "
        "Event — Registration, afin de ne pas réutiliser le même mot que "
        "pour Admin — ContactMessage et éviter toute ambiguïté de lecture.",
        NOTE))
    S.append(sp(0.15))
    S.append(Paragraph(
        "La classe <b>Registration</b> est le pivot du modèle : placée entre "
        "AppUser et Event, elle transforme une relation « plusieurs à "
        "plusieurs » (un bénévole s'inscrit à plusieurs événements, un "
        "événement accueille plusieurs bénévoles) en deux relations "
        "« un à plusieurs » exploitables, tout en offrant un emplacement "
        "naturel pour stocker le statut et la position en liste d'attente. "
        "La contrainte <font face='Courier'>{unique : par bénévole et "
        "événement}</font> garantit qu'un même bénévole ne peut s'inscrire "
        "qu'une seule fois au même événement.", BODY))
    S.append(sp(0.2))

    S.append(Paragraph("2.4 Choix de conception", SEC2))
    S.append(Paragraph(
        "<b>• Réutilisation de l'existant</b> — le compte Admin déjà présent "
        "pilote aussi bien les nouvelles entités que les contenus du site "
        "(Project, BlogPost, ContactMessage). On étend la base sans la "
        "réécrire ni dupliquer un compte de gestion. L'attribut « rôle » a "
        "été retiré : cette classe reprend déjà tous les comptes "
        "administrateur, sans notion de rôle multiple.", G.BULL))
    S.append(Paragraph(
        "<b>• Associations plutôt que clés étrangères</b> — les liens entre "
        "classes sont représentés uniquement par les associations "
        "(cardinalités et verbes métier). Les clés étrangères, redondantes "
        "au niveau conceptuel, ne sont plus affichées comme attributs — "
        "elles resteront bien sûr présentes dans le schéma MySQL généré.",
        G.BULL))
    S.append(Paragraph(
        "<b>• Énumérations pour les statuts et le niveau</b> — les valeurs "
        "fermées (statuts d'événement et d'inscription, niveau de fidélité) "
        "sont typées par des énumérations dédiées, plutôt que des chaînes "
        "libres. Cela renforce la validité des données et facilite la "
        "maintenance.", G.BULL))
    S.append(Paragraph(
        "<b>• Cohérence avec le code</b> — chaque classe correspond à une "
        "entité JPA (Spring Boot) et à une table MySQL ; les attributs, types "
        "et méthodes reflètent directement l'implémentation.", G.BULL))
    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P7 — COHÉRENCE ENTRE LES DEUX DIAGRAMMES
    # ═══════════════════════════════════════════════════════
    S.append(Paragraph("3. Cohérence entre les deux diagrammes", SEC1))
    S.append(Paragraph(
        "Chaque cas d'utilisation du diagramme 1 se traduit par une ou "
        "plusieurs opérations sur les classes du diagramme 2. Le tableau "
        "ci-dessous établit cette correspondance de façon exhaustive.", BODY))
    S.append(sp(0.15))
    rows = [
        [th("Cas d'utilisation"), th("Classe(s) / méthode(s)")],
        [tb("Créer un compte"), tb("AppUser.register()")],
        [tb("Se connecter"), tb("AppUser.login()")],
        [tb("Réinitialiser son mot de passe"),
         tb("AppUser.forgotPassword() / resetPassword()")],
        [tb("Gérer son profil"),
         tb("AppUser.updateProfile() ; AppUser.getLevel() (niveau affiché)")],
        [tb("S'inscrire à un événement"),
         tb("Registration (création) ; Event.getAvailablePlaces() / "
            "isFull()")],
        [tb("Rejoindre la liste d'attente"),
         tb("Registration (status = en attente, position)")],
        [tb("Se désinscrire"), tb("Registration.cancel()")],
        [tb("Consulter son historique"), tb("Registration (lecture, filtrée par bénévole)")],
        [tb("Télécharger une attestation"), tb("AppUser.downloadAttestation()")],
        [tb("Laisser un avis"), tb("Review.submitReview()")],
        [tb("Se connecter (admin)"), tb("Admin.login()")],
        [tb("Réinitialiser son mot de passe (admin)"),
         tb("Admin.forgotPassword() / resetPassword()")],
        [tb("Gérer son profil (admin)"),
         tb("Admin.updateProfile() ; Admin.changePassword()")],
        [tb("Gérer les événements"), tb("Event (création / modification) ; Event.updateStatus()")],
        [tb("Valider / refuser les inscriptions"),
         tb("Registration.confirm() / refuse() ; association Admin — "
            "Registration (« valide »)")],
        [tb("Envoyer un email de confirmation"),
         tb("Registration.sendConfirmationEmail()")],
        [tb("Envoyer des emails groupés"), tb("Event.sendGroupEmail()")],
        [tb("Gérer les bénévoles"), tb("AppUser (consultation, filtres)")],
        [tb("Consulter le tableau de bord"),
         tb("Agrégation sur Event, Registration et Review")],
        [tb("Exporter la liste des inscrits"), tb("Event.exportPDF()")],
        [tb("Consulter les avis"),
         tb("Review (lecture) ; Review.getAverageRating()")],
    ]
    S.append(grid([6.3*cm, CW-6.3*cm], rows))
    S.append(sp(0.2))
    S.append(Paragraph(
        "Seuls « Consulter le site vitrine » et « Consulter les événements » "
        "n'apparaissent pas dans le tableau : ce sont de simples "
        "consultations (pages publiques, lecture d'Event) qui ne "
        "correspondent à aucune méthode dédiée, ce qui est cohérent avec "
        "leur nature.", NOTE))

    doc.build(S)
    print(f"PDF généré : {OUT}")


if __name__ == "__main__":
    build()
