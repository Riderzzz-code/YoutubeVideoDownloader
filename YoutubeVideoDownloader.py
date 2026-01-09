import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from yt_dlp import YoutubeDL


# Fonction pour mettre à jour la progression
def progress_hook(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
        downloaded_bytes = d.get('downloaded_bytes', 0)

        # Éviter la division par zéro
        if total_bytes > 0:
            percentage = (downloaded_bytes / total_bytes) * 100
            # Mise à jour de la barre de progression (valeur entre 0 et 1)
            progress_bar.set(percentage / 100)
            # Arrondi à l'unité pour l'affichage du pourcentage
            progress_label.configure(text=f"Progression : {int(percentage)}%")
            root.update_idletasks()  # Mise à jour de l'interface
    elif d['status'] == 'error':
        progress_label.configure(text="Erreur lors du téléchargement.")
    elif d['status'] == 'finished':
        progress_label.configure(text="Traitement en cours...")
        # Ne pas définir progress_bar à 1.0 ici pour éviter le remplissage au début
        # du deuxième téléchargement (vidéo + audio)


# Fonction pour télécharger une vidéo ou un fichier MP3
def download_video():
    url = video_url.get()
    folder = folder_path.get()
    format_choice = format_var.get()  # Choix : "video" ou "audio"

    # Vérification des champs
    if not url.strip():
        messagebox.showerror("Erreur", "Veuillez entrer une URL YouTube valide.")
        return

    if not folder.strip():
        messagebox.showerror("Erreur", "Veuillez sélectionner un dossier de destination.")
        return

    # Réinitialiser la barre de progression
    progress_var.set(0)
    progress_label.configure(text="Préparation du téléchargement...")

    # Configurer les options pour yt-dlp
    ydl_opts = {
        'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
        'quiet': False,
        'progress_hooks': [progress_hook],  # Fonction pour mettre à jour la progression
        'noprogress': False,  # S'assurer que les hooks de progression sont appelés
    }

    # Si l'utilisateur a sélectionné "audio", ajouter des options pour MP3
    if format_choice == "audio":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        # Téléchargement en vidéo avec la qualité choisie
        quality = quality_var.get()

        # Correspondance des qualités avec les formats yt-dlp
        if quality == "1080p":
            format_spec = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
        elif quality == "720p":
            format_spec = "bestvideo[height<=720]+bestaudio/best[height<=720]"
        elif quality == "480p":
            format_spec = "bestvideo[height<=480]+bestaudio/best[height<=480]"
        else:  # Qualité automatique (meilleure disponible)
            format_spec = "bestvideo+bestaudio/best"

        ydl_opts.update({
            'format': format_spec,
            'merge_output_format': 'mp4'
        })

    try:
        # Lancer le téléchargement avec yt-dlp dans une fonction séparée pour ne pas bloquer l'interface
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Réinitialiser l'interface après le téléchargement
        messagebox.showinfo("Succès", f"Le fichier a été téléchargé dans :\n{folder}")
        progress_bar.set(0)  # Réinitialiser la barre de progression
        progress_label.configure(text="Progression : 0%")

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite :\n{e}")
        print(f"Erreur : {e}")  # Debug dans la console
        progress_bar.set(0)
        progress_label.configure(text="Progression : 0%")


# Fonction pour parcourir les dossiers
def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)


# Fonction pour afficher/cacher le menu de qualité en fonction du choix de format
def toggle_quality_menu(*args):
    if format_var.get() == "video":
        # Placer le quality_frame après le format_frame
        quality_frame.pack(after=format_frame, pady=5)
    else:
        quality_frame.pack_forget()


# Création de l'interface principale
root = ctk.CTk()
root.title("Téléchargeur YouTube")
root.geometry("600x450")  # Un peu plus grand pour accueillir les nouveaux éléments

# Variables
video_url = ctk.StringVar()
folder_path = ctk.StringVar()
format_var = ctk.StringVar(value="video")  # Par défaut, "video"
quality_var = ctk.StringVar(value="720p")  # Par défaut, "720p"
progress_var = ctk.DoubleVar(value=0)  # Variable pour la barre de progression (valeurs entre 0 et 1)

# Observer les changements dans format_var
format_var.trace_add("write", toggle_quality_menu)

# Widgets
title_label = ctk.CTkLabel(root, text="Téléchargeur de vidéos YouTube", font=ctk.CTkFont(size=20, weight="bold"))
title_label.pack(pady=10)

url_label = ctk.CTkLabel(root, text="URL de la vidéo YouTube :")
url_label.pack(pady=5)

url_entry = ctk.CTkEntry(root, textvariable=video_url, width=400)
url_entry.pack(pady=5)

folder_label = ctk.CTkLabel(root, text="Dossier de destination :")
folder_label.pack(pady=5)

folder_frame = ctk.CTkFrame(root)
folder_frame.pack(pady=5)

folder_entry = ctk.CTkEntry(folder_frame, textvariable=folder_path, width=300)
folder_entry.pack(side="left", padx=5)

browse_button = ctk.CTkButton(folder_frame, text="Parcourir", command=browse_folder)
browse_button.pack(side="left")

# Options pour choisir entre vidéo et audio
format_label = ctk.CTkLabel(root, text="Choisissez le format :")
format_label.pack(pady=10)

format_frame = ctk.CTkFrame(root)
format_frame.pack(pady=5)

video_radio = ctk.CTkRadioButton(format_frame, text="Vidéo (MP4)", variable=format_var, value="video")
video_radio.pack(side="left", padx=10)

audio_radio = ctk.CTkRadioButton(format_frame, text="Audio (MP3)", variable=format_var, value="audio")
audio_radio.pack(side="left", padx=10)

# Menu déroulant pour choisir la qualité vidéo (visible uniquement quand "video" est sélectionné)
quality_frame = ctk.CTkFrame(root)
# Ne pas afficher le frame par défaut, la fonction toggle_quality_menu s'en chargera
# lors de l'initialisation

quality_label = ctk.CTkLabel(quality_frame, text="Qualité vidéo :")
quality_label.pack(side="left", padx=5)

quality_menu = ctk.CTkOptionMenu(quality_frame, variable=quality_var, values=["480p", "720p", "1080p"])
quality_menu.pack(side="left", padx=5)

# Appeler toggle_quality_menu pour initialiser correctement l'affichage du menu de qualité
toggle_quality_menu()

# Bouton de téléchargement
download_button = ctk.CTkButton(root, text="Télécharger", command=download_video, fg_color="green",
                                hover_color="darkgreen")
download_button.pack(pady=15)

# Barre de progression
progress_frame = ctk.CTkFrame(root)
progress_frame.pack(pady=10, fill="x", padx=20)

progress_bar = ctk.CTkProgressBar(progress_frame, width=500)
progress_bar.pack(pady=5)
progress_bar.set(0)  # Initialiser à 0

progress_label = ctk.CTkLabel(progress_frame, text="Progression : 0%")
progress_label.pack(pady=5)

# Lancement de l'interface
root.mainloop()