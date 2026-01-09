import os
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from yt_dlp import YoutubeDL

# Variables globales pour le suivi de la progression
current_progress = 0
is_downloading = False
download_completed = threading.Event()


# Fonction pour mettre à jour la progression (appelée par yt-dlp)
def progress_hook(d):
    global current_progress

    if d['status'] == 'downloading':
        # Calculer le pourcentage de progression
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
        downloaded_bytes = d.get('downloaded_bytes', 0)

        if total_bytes > 0:
            percentage = int((downloaded_bytes / total_bytes) * 100)
            # Mise à jour de la barre de progression seulement si la progression augmente
            if percentage > current_progress:
                current_progress = percentage
                progress_bar.set(percentage / 100)
                progress_label.configure(text=f"Progression : {percentage}%")
                root.update_idletasks()

    elif d['status'] == 'finished':
        progress_label.configure(text="Post-traitement en cours...")

    elif d['status'] == 'error':
        progress_label.configure(text="Erreur lors du téléchargement.")


# Fonction pour télécharger une vidéo ou un fichier MP3
def download_video():
    global current_progress, is_downloading

    # Empêcher les téléchargements multiples
    if is_downloading:
        return

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
    current_progress = 0
    progress_bar.set(0)
    progress_label.configure(text="Préparation du téléchargement...")

    is_downloading = True
    download_button.configure(state="disabled")  # Désactiver le bouton pendant le téléchargement

    # Options de base pour yt-dlp
    ydl_opts = {
        'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
    }

    # Configurer les options selon le format choisi
    if format_choice == "audio":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        })
    else:
        # Configuration pour la vidéo avec la qualité sélectionnée
        quality = quality_var.get()

        if quality == "1080p":
            format_spec = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
        elif quality == "720p":
            format_spec = "bestvideo[height<=720]+bestaudio/best[height<=720]"
        elif quality == "480p":
            format_spec = "bestvideo[height<=480]+bestaudio/best[height<=480]"
        else:
            format_spec = "bestvideo+bestaudio/best"

        ydl_opts.update({
            'format': format_spec,
            'merge_output_format': 'mp4'
        })

    # Fonction pour le thread de téléchargement
    def download_thread():
        global is_downloading, current_progress

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # Mettre à jour l'interface après le téléchargement (dans le thread principal)
            root.after(0, lambda: progress_bar.set(1.0))  # Mettre à 100%
            root.after(0, lambda: progress_label.configure(text="Téléchargement terminé !"))
            root.after(0, lambda: messagebox.showinfo("Succès", f"Le fichier a été téléchargé dans :\n{folder}"))
            root.after(0, lambda: reset_progress())

        except Exception as e:
            # Gérer les erreurs dans le thread principal
            root.after(0, lambda: messagebox.showerror("Erreur", f"Une erreur s'est produite :\n{e}"))
            root.after(0, lambda: reset_progress())

        finally:
            is_downloading = False
            root.after(0, lambda: download_button.configure(state="normal"))

    # Démarrer le téléchargement dans un thread séparé
    threading.Thread(target=download_thread, daemon=True).start()


# Fonction pour réinitialiser la progression
def reset_progress():
    global current_progress
    current_progress = 0
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

quality_label = ctk.CTkLabel(quality_frame, text="Qualité vidéo :")
quality_label.pack(side="left", padx=5)

quality_menu = ctk.CTkOptionMenu(quality_frame, variable=quality_var, values=["480p", "720p", "1080p"])
quality_menu.pack(side="left", padx=5)

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

# Appeler toggle_quality_menu pour initialiser correctement l'affichage du menu de qualité
toggle_quality_menu()

# Lancement de l'interface
root.mainloop()