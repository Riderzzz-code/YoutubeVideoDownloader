# Téléchargeur Vidéo YouTube (YouTube Video Downloader)

Une application de bureau moderne et intuitive développée en Python pour télécharger facilement vos vidéos ou extraire l'audio de YouTube.

<img width="756" height="607" alt="image" src="https://github.com/user-attachments/assets/96a41907-ad3e-427c-b88e-1eff03ede957" />


## 🚀 Fonctionnalités

- **Téléchargement Vidéo** : Support des résolutions 480p, 720p et 1080p (format MP4).
- **Extraction Audio** : Conversion directe en format MP3 haute qualité (320kbps).

- **Interface Moderne** : Développée avec `customtkinter` pour un design élégant et réactif.
- **Suivi en Temps Réel** : Barre de progression dynamique et messages d'état.
- **Multi-threading** : L'interface reste fluide pendant que le téléchargement s'effectue en arrière-plan.

## 🛠️ Prérequis

Avant de commencer, assurez-vous d'avoir installé :

1. **Python 3.7+**
2. **FFmpeg** : Cet outil est **indispensable** pour que `yt-dlp` puisse fusionner la vidéo et l'audio ou convertir en MP3.
    - *Sur Windows* : Téléchargez via [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) et ajoutez-le à votre PATH.
    - *Sur macOS* : `brew install ffmpeg`
    - *Sur Linux* : `sudo apt install ffmpeg`

## 📦 Installation des dépendances

L'application utilise deux bibliothèques principales qu'il faut installer via `pip`. Ouvrez votre terminal (ou invite de commande) dans le dossier du projet et exécutez la commande suivante :

Bash

`pip install customtkinter yt-dlp`

### Détail des bibliothèques :

- `customtkinter` : Utilisé pour créer l'interface graphique moderne.
- `yt-dlp` : Le moteur puissant qui gère l'extraction et le téléchargement du contenu YouTube.

## 🎮 Lancement de l'application

Une fois les dépendances installées, lancez simplement le script principal avec la commande :

Bash

`python YoutubeVideoDownloader.py`

## 📖 Comment utiliser l'app ?

1. **Copiez l'URL** de la vidéo YouTube souhaitée.
2. **Collez l'URL** dans le champ prévu à cet effet.
3. **Choisissez le dossier** de destination en cliquant sur "Parcourir".
4. **Sélectionnez le format** (Vidéo ou Audio) et la qualité désirée.
5. **Cliquez sur "Télécharger"** et suivez la progression.
