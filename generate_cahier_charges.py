#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cahier des charges du TFE — document autonome (court).
Réutilise les styles de generate_cdc.py.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, NextPageTemplate,
    Paragraph, Spacer, PageBreak,
)

import generate_cdc as G
from generate_cdc import (
    W, H, ML, MR, CW,
    BODY, SEC1, SEC2, SEC2B, BULL, ITAL, NOTE, TOC_H,
    CV_SCHOOL, CV_YEAR, CV_TITLE, CV_SUB, CV_MOD, CV_EXT, CV_INFO, CV_INST,
    sp, grid, th, tb, toc_line,
)

OUT = "/home/user/portfolio-alain/Cahier_des_charges_TFE_Terra_Sana_Alain.pdf"


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
    S.append(Spacer(1, 1.8*cm))
    S.append(Paragraph("Bachelier en Informatique de Gestion", CV_SCHOOL))
    S.append(sp(0.3))
    S.append(Paragraph("3ème année", CV_YEAR))
    S.append(Spacer(1, 2.2*cm))
    S.append(Paragraph("Cahier des charges", CV_TITLE))
    S.append(sp(0.4))
    S.append(Paragraph("Travail de Fin d'Études — Épreuve intégrée", CV_SUB))
    S.append(Spacer(1, 1.8*cm))
    S.append(Paragraph("Module de gestion des bénévoles et des événements", CV_MOD))
    S.append(sp(0.3))
    S.append(Paragraph("Extension du site web vitrine de Terra Sana ASBL", CV_EXT))
    S.append(Spacer(1, 2.5*cm))
    S.append(Paragraph("Encadreur scolaire : Marie-Christine Namur", CV_INFO))
    S.append(sp(0.2))
    S.append(Paragraph("Maître de stage : Didier Seraye", CV_INFO))
    S.append(sp(0.2))
    S.append(Paragraph("Travail présenté par Youndjeu Tchouapi Alain", CV_INFO))
    S.append(Spacer(1, 2.5*cm))
    S.append(Paragraph("<b>EAFC Uccle</b>", CV_INST))
    S.append(sp(0.3))
    S.append(Paragraph("2025-2026", CV_YEAR))
    S.append(NextPageTemplate("Normal"))
    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P2 — TABLE DES MATIÈRES
    # ═══════════════════════════════════════════════════════
    S.append(Paragraph("Table des matières", TOC_H))
    toc = [
        ("1. Contexte et présentation",                   3,  1),
        ("1.1 Présentation de Terra Sana ASBL",           3,  2),
        ("1.2 Situation actuelle",                        3,  2),
        ("1.3 Sources d'information",                     4,  2),
        ("2. Objectifs et périmètre du projet",           5,  1),
        ("2.1 Objectif général",                          5,  2),
        ("2.2 Périmètre fonctionnel",                     5,  2),
        ("2.3 Acteurs",                                   5,  2),
        ("3. Description fonctionnelle",                  6,  1),
        ("3.1 Espace bénévole",                           6,  2),
        ("3.2 Gestion des événements",                    6,  2),
        ("3.3 Inscriptions et liste d'attente",           7,  2),
        ("3.4 Retours et niveaux de fidélité",            7,  2),
        ("3.5 Notifications et documents",                7,  2),
        ("4. Contraintes du projet",                      8,  1),
        ("5. Livrables attendus",                         9,  1),
        ("6. Planning et échéances",                     10,  1),
    ]
    for label, page, level in toc:
        S.append(toc_line(label, page, level))
    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P3 — 1. CONTEXTE ET PRÉSENTATION
    # ═══════════════════════════════════════════════════════
    S.append(Paragraph("1. Contexte et présentation", SEC1))

    S.append(Paragraph("1.1 Présentation de Terra Sana ASBL", SEC2))
    S.append(Paragraph(
        "Terra Sana ASBL est une association sans but lucratif belge dont le siège social "
        "est situé au 19 avenue des Volontaires à Auderghem. L'association œuvre dans les "
        "domaines de la santé naturelle, de l'alimentation saine et du bien-être global. Elle "
        "organise régulièrement des ateliers, des conférences et des activités communautaires, "
        "animés en grande partie par des bénévoles engagés. Pour gérer ses différents pôles "
        "d'activité, l'association dispose de 12 applications internes spécialisées, dont "
        "l'accès est centralisé depuis le site web développé durant le stage.", BODY))

    S.append(Paragraph("1.2 Situation actuelle", SEC2))
    S.append(Paragraph(
        "Avant le stage, Terra Sana ne possédait aucune présence numérique. La communication "
        "avec les bénévoles et le public se faisait exclusivement par téléphone et par email, "
        "et la gestion administrative reposait entièrement sur des fichiers Excel et des "
        "documents papier.", BODY))
    S.append(Paragraph(
        "Le stage (25 mars – 20 mai 2026) a permis de mettre en place la base technique du "
        "projet : un site vitrine multilingue (FR / EN / NL), un hub centralisant les 12 "
        "applications internes, un espace d'administration sécurisé (JWT), une base de "
        "données MySQL et un backend Spring Boot exposant 17 endpoints REST.", BODY))
    S.append(Paragraph(
        "En revanche, la gestion des bénévoles et des événements reste entièrement manuelle. "
        "Cette organisation engendre plusieurs difficultés concrètes :", BODY))
    for b in [
        "des doublons et pertes d'information quand plusieurs personnes modifient les mêmes fichiers ;",
        "aucune vue d'ensemble des places disponibles, d'où des activités surchargées ou sous-remplies ;",
        "des confirmations et relances envoyées une à une, un travail répétitif et chronophage ;",
        "aucun historique de participation, ni moyen de remercier les bénévoles ou de leur "
        "délivrer une attestation.",
    ]:
        S.append(Paragraph(f"• {b}", BULL))
    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P4 — 1.3 Sources d'information
    # ═══════════════════════════════════════════════════════
    S.append(Paragraph("1.3 Sources d'information", SEC2))
    S.append(Paragraph(
        "Les informations utilisées pour concevoir le module proviennent de plusieurs sources "
        "complémentaires réunies pendant et après le stage :", BODY))
    for b in [
        "des entretiens avec Monsieur Didier Seraye (Responsable Administratif de Terra Sana) "
        "afin de comprendre les besoins réels, le fonctionnement quotidien de l'association et "
        "les points de friction dans la gestion actuelle des bénévoles et des événements ;",
        "l'analyse des documents et fichiers Excel utilisés à ce jour pour identifier les "
        "données à structurer (identité des bénévoles, historiques d'ateliers, listes d'inscrits) ;",
        "la documentation officielle des technologies retenues (Spring Boot, React, Spring "
        "Security, JavaMail, iText) ainsi que les bonnes pratiques REST et de sécurité ;",
        "les consignes de l'EAFC Uccle pour la rédaction du présent cahier des charges et la "
        "structuration du projet de fin d'études.",
    ]:
        S.append(Paragraph(f"• {b}", BULL))
    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P5 — 2. OBJECTIFS ET PÉRIMÈTRE
    # ═══════════════════════════════════════════════════════
    S.append(Paragraph("2. Objectifs et périmètre du projet", SEC1))

    S.append(Paragraph("2.1 Objectif général", SEC2))
    S.append(Paragraph(
        "L'objectif du TFE est de <b>concevoir et développer un module complet de gestion des "
        "bénévoles et des événements</b>, intégré au site web déjà réalisé pendant le stage. "
        "Ce module doit permettre à Terra Sana ASBL de centraliser et d'automatiser ce qui "
        "était jusqu'ici tenu à la main dans des fichiers Excel et par email, afin de gagner "
        "en temps, en fiabilité et en qualité de service auprès de ses bénévoles.", BODY))

    S.append(Paragraph("2.2 Périmètre fonctionnel", SEC2))
    S.append(Paragraph(
        "Le module à livrer couvre les fonctionnalités suivantes, développées entièrement par "
        "l'étudiant après la fin du stage :", BODY))
    for b in [
        "création et gestion de comptes bénévoles (inscription, connexion, profil, mot de "
        "passe oublié) ;",
        "gestion complète des événements par l'administrateur (création, modification, "
        "statut, suppression) ;",
        "inscription et désinscription des bénévoles aux événements, avec liste d'attente "
        "automatique lorsque l'événement est complet ;",
        "validation ou refus des inscriptions par l'administrateur, avec envoi automatique "
        "d'e-mails de confirmation ;",
        "consultation par le bénévole de son historique de participations et téléchargement "
        "d'une attestation PDF ;",
        "dépôt d'avis (note + commentaire) après un événement terminé ;",
        "calcul automatique d'un niveau de fidélité du bénévole (Bronze / Argent / Or) ;",
        "tableau de bord enrichi pour l'administrateur avec statistiques et export PDF.",
    ]:
        S.append(Paragraph(f"• {b}", BULL))
    S.append(Paragraph(
        "Le détail complet des fonctionnalités, ainsi que les diagrammes UML et le modèle de "
        "données, sont présentés dans le document d'analyse joint au présent cahier des "
        "charges.", NOTE))

    S.append(Paragraph("2.3 Acteurs", SEC2))
    S.append(grid([3.3*cm, CW-3.3*cm], [
        [th("Acteur"), th("Rôle")],
        [tb("<b>Visiteur</b>"),
         tb("Internaute non authentifié. Il peut consulter le site vitrine, la liste des "
            "événements et créer un compte.")],
        [tb("<b>Bénévole</b>"),
         tb("Visiteur qui s'est créé un compte. Il peut se connecter, gérer son profil, "
            "s'inscrire aux événements, se désinscrire, consulter son historique, télécharger "
            "une attestation et laisser des avis.")],
        [tb("<b>Administrateur</b>"),
         tb("Compte de gestion existant. Il pilote les événements, valide les inscriptions, "
            "envoie des e-mails, gère les bénévoles et consulte le tableau de bord.")],
    ]))
    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P6 — 3. DESCRIPTION FONCTIONNELLE
    # ═══════════════════════════════════════════════════════
    S.append(Paragraph("3. Description fonctionnelle", SEC1))
    S.append(Paragraph(
        "Cette section résume les fonctionnalités à réaliser dans le cadre du TFE. Le détail "
        "de chaque fonctionnalité, les règles de gestion associées ainsi que les diagrammes "
        "UML sont présentés dans le document d'analyse joint.", BODY))

    S.append(Paragraph("3.1 Espace bénévole", SEC2))
    S.append(Paragraph(
        "L'application propose un espace personnel accessible à tout bénévole enregistré. "
        "Il permet la création d'un compte (nom, prénom, email, mot de passe hachés BCrypt), "
        "la connexion sécurisée par jeton JWT (24h), la mise à jour du profil (téléphone, "
        "ville, compétences, disponibilités, langue préférée) et la réinitialisation du mot "
        "de passe par e-mail. Conformément au principe de minimisation des données (RGPD), "
        "seules les informations strictement nécessaires sont obligatoires ; les autres sont "
        "facultatives.", BODY))

    S.append(Paragraph("3.2 Gestion des événements", SEC2))
    S.append(Paragraph(
        "L'administrateur crée les événements en indiquant le titre, la description, la date, "
        "le lieu, le nombre maximum de participants et une illustration. Il pilote le statut "
        "de l'événement (ouvert, complet, annulé, clôturé), valide ou refuse les inscriptions, "
        "et peut envoyer un e-mail groupé à tous les bénévoles inscrits (rappel, changement "
        "de lieu, annulation).", BODY))
    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P7 — 3.3, 3.4, 3.5
    # ═══════════════════════════════════════════════════════
    S.append(Paragraph("3.3 Inscriptions et liste d'attente", SEC2))
    S.append(Paragraph(
        "Le bénévole s'inscrit à un événement en un clic depuis la page de détail. Si "
        "l'événement est complet, il est automatiquement placé en <b>liste d'attente</b> avec "
        "une position calculée en fonction de l'ordre d'arrivée. Il peut se désinscrire "
        "librement tant que l'événement n'est pas commencé. Lorsqu'une place se libère "
        "(désinscription confirmée), le premier bénévole en liste d'attente est <b>promu "
        "automatiquement</b> et notifié par e-mail. Un même bénévole ne peut s'inscrire "
        "qu'une seule fois au même événement.", BODY))

    S.append(Paragraph("3.4 Retours et niveaux de fidélité", SEC2))
    S.append(Paragraph(
        "À la fin d'un événement, un bénévole ayant effectivement participé peut déposer un "
        "avis (note de 1 à 5 + commentaire libre) qui alimente une <b>note moyenne</b> par "
        "événement. L'application calcule automatiquement un <b>niveau de fidélité</b> à "
        "partir du nombre de participations confirmées : <b>BRONZE</b> (1 à 2 événements), "
        "<b>ARGENT</b> (3 à 6), <b>OR</b> (7 et plus). Un e-mail est envoyé à chaque "
        "changement de niveau.", BODY))

    S.append(Paragraph("3.5 Notifications et documents", SEC2))
    S.append(Paragraph(
        "Le module envoie systématiquement des e-mails automatiques via <b>Gmail SMTP</b> : "
        "confirmation ou refus d'inscription, entrée en liste d'attente, promotion depuis la "
        "liste d'attente, changement de niveau, réinitialisation de mot de passe et e-mails "
        "groupés à un événement. Deux exports <b>PDF</b> sont également disponibles : "
        "l'attestation de participation téléchargeable par le bénévole et la liste des "
        "inscrits téléchargeable par l'administrateur.", BODY))
    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P8 — 4. CONTRAINTES
    # ═══════════════════════════════════════════════════════
    S.append(Paragraph("4. Contraintes du projet", SEC1))

    S.append(Paragraph("Contraintes techniques", SEC2B))
    S.append(Paragraph(
        "Le module doit s'intégrer à l'architecture existante mise en place pendant le "
        "stage :", BODY))
    S.append(grid([4.0*cm, 2.3*cm, CW-6.5*cm], [
        [th("Technologie"),           th("Version"),  th("Rôle")],
        [tb("React.js"),              tb("18.2.0"),   tb("Frontend — pages, navigation, composants")],
        [tb("Spring Boot"),           tb("Java 21"),  tb("Backend — API REST, logique métier")],
        [tb("Spring Security + JWT"), tb("0.11.5"),   tb("Authentification et sécurisation des accès")],
        [tb("MySQL"),                 tb("9.1.0"),    tb("Base de données relationnelle")],
        [tb("BCrypt"),                tb("—"),        tb("Hachage sécurisé des mots de passe")],
        [tb("Gmail SMTP + JavaMail"), tb("—"),        tb("Envoi des e-mails automatiques")],
        [tb("iText / JasperReports"), tb("—"),        tb("Génération des documents PDF")],
        [tb("WAMP Server"),           tb("3.3.7"),    tb("Environnement local MySQL sous Windows")],
    ]))
    S.append(sp(0.25))

    S.append(Paragraph("Contraintes de sécurité et de conformité", SEC2B))
    for b in [
        "les mots de passe ne sont jamais stockés en clair (hachage BCrypt) ;",
        "l'email de chaque bénévole est unique dans le système ;",
        "les endpoints d'administration sont accessibles uniquement au compte administrateur ;",
        "seules les données strictement nécessaires sont obligatoires à l'inscription (RGPD, "
        "minimisation des données).",
    ]:
        S.append(Paragraph(f"• {b}", BULL))
    S.append(sp(0.15))

    S.append(Paragraph("Contraintes de délai et d'environnement", SEC2B))
    for b in [
        "le développement est réalisé après le stage, entièrement à domicile ;",
        "l'application est développée et présentée en environnement local (WAMP Server sous "
        "Windows) ; aucun déploiement en ligne n'est prévu dans le cadre de ce TFE ;",
        "les échéances officielles de la 2ème session (juillet à octobre 2026) doivent être "
        "respectées (voir section 6).",
    ]:
        S.append(Paragraph(f"• {b}", BULL))
    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P9 — 5. LIVRABLES
    # ═══════════════════════════════════════════════════════
    S.append(Paragraph("5. Livrables attendus", SEC1))
    S.append(Paragraph(
        "À la fin du TFE, les livrables suivants seront remis :", BODY))
    S.append(grid([5.5*cm, CW-5.5*cm], [
        [th("Livrable"), th("Description")],
        [tb("Code source complet"),
         tb("Frontend React et backend Spring Boot, versionnés sur GitHub, incluant les "
            "scripts SQL de création et de peuplement de la base.")],
        [tb("Application fonctionnelle"),
         tb("Module de gestion des bénévoles et des événements opérationnel, démontrable en "
            "environnement local (WAMP Server sous Windows).")],
        [tb("Rapport écrit"),
         tb("Rapport écrit complet regroupant le présent cahier des charges, l'analyse "
            "fonctionnelle (cas d'utilisation, règles de gestion), le modèle de données "
            "(diagramme de classes et dictionnaire de données), les choix techniques et le "
            "planning.")],
        [tb("Diagrammes UML"),
         tb("Diagramme de cas d'utilisation et diagramme de classes, réalisés selon la "
            "notation UML standard, validés par l'encadreur scolaire.")],
        [tb("Base de données"),
         tb("Schéma MySQL complet des 8 tables (4 existantes + 4 nouvelles) avec les "
            "contraintes et les index nécessaires.")],
        [tb("Exemplaires papier"),
         tb("Cinq exemplaires du rapport écrit définitif à remettre au secrétariat de "
            "l'EAFC Uccle.")],
        [tb("Défense orale"),
         tb("Présentation et démonstration du projet devant le jury de l'épreuve intégrée.")],
    ]))
    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # P10 — 6. PLANNING
    # ═══════════════════════════════════════════════════════
    S.append(Paragraph("6. Planning et échéances", SEC1))
    S.append(Paragraph(
        "Le tableau ci-dessous reprend les échéances officielles de la 2ème session imposées "
        "par l'EAFC Uccle :", BODY))
    S.append(grid([2.8*cm, CW-2.8*cm], [
        [th("Date limite"), th("Échéance")],
        [tb("03/07/2026"),  tb("Remise du rapport écrit (analyse initiale)")],
        [tb("28/08/2026"),  tb("Validation de l'analyse par l'encadreur scolaire")],
        [tb("15/09/2026"),  tb("Validation de l'application")],
        [tb("22/09/2026"),  tb("Remise du rapport écrit provisoire (PDF sur Teams)")],
        [tb("29/09/2026"),  tb("Remise du rapport écrit définitif (PDF + 5 exemplaires + GitHub)")],
        [tb("13/10/2026"),  tb("Défenses orales")],
    ]))
    S.append(sp(0.25))
    S.append(Paragraph(
        "Le découpage du travail en phases de développement, ainsi que les risques identifiés "
        "et les mesures prévues pour les limiter, sont détaillés dans le document d'analyse.",
        NOTE))

    doc.build(S)
    print(f"PDF généré : {OUT}")


if __name__ == "__main__":
    build()
