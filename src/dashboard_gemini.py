"""Module de génération d'un tableau de bord PDF via l'API Google Gemini."""

import os
import re

import pandas as pd
from dotenv import load_dotenv
from google import genai
from xhtml2pdf import pisa

load_dotenv()

# Constantes globales
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Insérer un fichier de donnée (csv, json, xlsx, ...)
FICHIER_CSV = "election-municipale-2026-2nd-tour-resultats-par-commune.csv"

FICHIER_HTML_SORTIE = "Gemini_Dashboard.html"
FICHIER_PDF_SORTIE = "Gemini_Dashboard.pdf"


def generer_rapport_avec_gemini(csv_path, html_output_path, pdf_output_path):
    """Génère un rapport stratégique en PDF à l'aide de l'IA Gemini.

    Args:
        csv_path (str): Le chemin vers le fichier CSV source.
        html_output_path (str): Le chemin du fichier HTML intermédiaire.
        pdf_output_path (str): Le chemin du fichier PDF final.

    Returns:
        None
    """
    print(f"Lecture du fichier CSV : {csv_path}")

    try:
        df = pd.read_csv(csv_path, sep=";", encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, sep=";", encoding="latin1")

    df = df.fillna("N/A")

    colonnes = ", ".join(df.columns.tolist())
    nb_lignes = len(df)
    echantillon = df.head(5).to_dict(orient="records")

    client = genai.Client(api_key=GOOGLE_API_KEY)

    # Prompt à découper correctement pour la limite de charactère
    prompt = (
        "Tu es un Analyste Data Senior et un Expert UI/UX en conception de "
        "Tableaux de Bord de Direction (Executive Dashboards).\n"
        "Transforme ce résumé de données brutes en un rapport de pilotage "
        "stratégique en HTML/CSS, optimisé pour une impression pdf.\n\n"
        "Contexte des données :\n"
        "- Thématique : Caractéristiques des bassins aquatiques de Grand Paris Sud.\n"
        "- Territoire cible : Les communes de l'agglomération.\n"
        f"- Liste des colonnes : {colonnes}\n"
        f"- Nombre total d'enregistrements : {nb_lignes}\n"
        f"- Échantillon représentatif : {echantillon}\n\n"
        "Mission et Liberté d'expression :\n"
        "1. Analyse : Rédige un court paragraphe d'analyse managériale.\n"
        "2. KPIs : Déduis 4 indicateurs majeurs et place-les en haut sous forme de 'Cartes' alignées horizontalement.\n"
        "3. Focus Territorial : Crée une section détaillant la répartition par commune.\n"
        "4. Graphiques statiques : N'utilise AUCUN JavaScript. Crée des graphiques à barres horizontales directement en HTML/CSS (via des barres de progression).\n\n"
        "Contraintes Techniques (Spécifiques au moteur xhtml2pdf) :\n"
        "- MISE EN PAGE : 'display: flex', 'display: grid' et 'position: absolute/fixed' INTERDITS.\n"
        "- STRUCTURE : Tu DOIS utiliser des tableaux HTML (<table>, <tr>, <td>) avec des attributs width=\"X%\" pour aligner tes cartes de KPI et tes barres de progression.\n"
        "- TYPOGRAPHIE : Déclare une taille de police globale cohérente pour l'impression (ex: body en 10pt, h1 en 18pt).\n\n"
        "Design UI/UX (Premium Dark Mode pour Pilotage) :\n"
        "- Fond de page global (@page et body) : #0f172a.\n"
        "- Encarts / Cartes de données : #1e293b avec de fines bordures #334155.\n"
        "- Typographie : Sans-serif propre, texte principal #f8fafc et secondaire #94a3b8.\n"
        "- Couleurs d'accent : #38bdf8 (Bleu), #10b981 (Vert), #f59e0b (Orange).\n\n"
        "RÈGLE ABSOLUE DE PRODUCTION : Renvoie STRICTEMENT QUE le code HTML valide. Ne dis aucune phrase d'introduction. NE METS PAS les balises markdown. Ton premier mot doit être <!DOCTYPE html> et le dernier </html>."
    )

    print("Demande de génération du code HTML à Gemini...")

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    html_genere = response.text

    # Nettoyage Markdown de sécurité
    html_genere = re.sub(r"^```(html)?", "", html_genere, flags=re.IGNORECASE).strip()
    html_genere = re.sub(r"```$", "", html_genere).strip()

    print(f"Sauvegarde du fichier HTML : {html_output_path}")
    with open(html_output_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_genere)

    print(f"Transformation du HTML de l'IA en pdf (via xhtml2pdf) : {pdf_output_path}")
    try:
        with open(pdf_output_path, "w+b") as pdf_file:
            pisa_status = pisa.CreatePDF(html_genere, dest=pdf_file)

        if not pisa_status.err:
            print("Fichiers pdf générés avec succès.")
        else:
            print(f"Erreur lors de la mise en page du pdf : {pisa_status.err}")
    except Exception as error:
        print(f"Erreur critique lors de la génération du pdf : {error}")

    return None


if __name__ == "__main__":
    generer_rapport_avec_gemini(FICHIER_CSV, FICHIER_HTML_SORTIE, FICHIER_PDF_SORTIE)