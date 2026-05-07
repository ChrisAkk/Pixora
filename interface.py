import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk 
from filtres import *

# Définition des variables globales
canvas = None
matrice_pixels = None
matrice_temporaire = None
photo = None
nom_fichier = None
archive_undo = []
archive_redo = None

# Gestion de l'affichage
def rafraichir(matrice_pixels, archiver=True):
    global photo

    if archiver:
        archive_undo.append(matrice_pixels)

    img_rafraichie = Image.fromarray(matrice_pixels)
    photo = ImageTk.PhotoImage(img_rafraichie)

    canvas.delete("all")
    canvas.config(width=matrice_pixels.shape[1], height=matrice_pixels.shape[0])
    fenetre_principale.update_idletasks()
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)

def applique_effet():
    global matrice_pixels, matrice_temporaire, dialogue_effet
    matrice_pixels = np.array(matrice_temporaire, copy=True)
    rafraichir(matrice_pixels)
    dialogue_effet.destroy()

def annule_effet():
    global matrice_pixels, matrice_temporaire, dialogue_effet
    matrice_temporaire = None
    rafraichir(matrice_pixels)
    dialogue_effet.destroy()

# fonctions de transition pour les sliders

def transition_luminosite(valeur_slider):
    global matrice_pixels, matrice_temporaire

    x = valeur_slider.get()
    matrice_temporaire = filtre_luminosite(matrice_pixels, x)
    rafraichir(matrice_temporaire, archiver=False)

def transition_contraste(valeur_slider_1, valeur_slider_2):
    global matrice_pixels, matrice_temporaire

    x = valeur_slider_1.get()
    y = valeur_slider_2.get()
    matrice_temporaire = filtre_contraste(matrice_pixels, x, y)
    rafraichir(matrice_temporaire, archiver=False)

# --- Callbacks --- 

# Callbacks fichier 
def charger():
    global photo, matrice_pixels, canvas, nom_fichier

    nom_fichier = str(filedialog.askopenfilename(title="Ouvrir une image"))

    if nom_fichier != None:
        image_temp = Image.open(nom_fichier)

        largeur = fenetre_principale.winfo_width()
        hauteur = fenetre_principale.winfo_height()
        image_temp.thumbnail((largeur, hauteur), Image.Resampling.LANCZOS)

        matrice_pixels = np.array(image_temp)

def callback_ouvrir():
    global matrice_pixels

    charger()
    if matrice_pixels is not None:

        menu_fichier.entryconfig('Sauvegarder', state='normal')

        menu_edition.entryconfig('Annuler', state='normal')
        menu_edition.entryconfig('Rétablir', state='normal')
        menu_edition.entryconfig('Réinitialisé', state='normal')

        menu_reglages.entryconfig('Luminosité', state='normal')
        menu_reglages.entryconfig('Contraste', state='normal')
        menu_reglages.entryconfig('Sépia', state='normal')
        menu_couleur.entryconfig('Vert', state='normal')
        menu_couleur.entryconfig('Bleu', state='normal')
        menu_couleur.entryconfig('Rouge', state='normal')
        menu_couleur.entryconfig('Noir et Blanc', state='normal')
        menu_focus.entryconfig('Netteté', state='normal')
        menu_focus.entryconfig('Flou', state='normal')
        menu_focus.entryconfig('Flou Gaussien', state='normal')
        menu_focus.entryconfig('Netteté Gaussien', state='normal')
        menu_filtre.entryconfig('Fusion', state='normal')

        rafraichir(matrice_pixels)

def callback_sauvegarder():
    global matrice_pixels 

    chemin = filedialog.asksaveasfilename(title="Sauvergarder l'image", defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])

    if chemin:
        image = Image.fromarray(matrice_pixels)
        image.save(chemin)

def callback_quitter():
    fenetre_principale.destroy()

# Callbacks éditions

def callback_annuler():
    global archive_undo, archive_redo, matrice_pixels

    if len(archive_undo) > 1:
        archive_redo = archive_undo.pop()
        matrice_pixels = archive_undo[-1].copy()
        rafraichir(matrice_pixels, archiver=False)

def callback_retablir():
    global archive_redo, archive_undo, matrice_pixels

    if archive_redo is not None:
        matrice_pixels = archive_redo.copy()
        rafraichir(matrice_pixels)
        archive_redo = None

def callback_reinitialise():
    global archive_redo, archive_undo, matrice_pixels

    matrice_pixels = archive_undo[0].copy()
    rafraichir(matrice_pixels, archiver=False)

    while len(archive_undo) != 1:
        archive_undo.pop()
    archive_redo = None

# Callbacks filtres

def callback_filtre_vert():
    global matrice_pixels
    matrice_pixels  = filtre_vert(matrice_pixels)
    rafraichir(matrice_pixels)

def callback_filtre_bleu():
    global matrice_pixels
    matrice_pixels  = filtre_bleu(matrice_pixels)
    rafraichir(matrice_pixels)

def callback_filtre_rouge():
    global matrice_pixels
    matrice_pixels  = filtre_rouge(matrice_pixels)
    rafraichir(matrice_pixels)

def callback_filtre_noir_blanc():
    global matrice_pixels
    matrice_pixels  = filtre_noir_blanc(matrice_pixels)
    rafraichir(matrice_pixels)

def callback_filtre_sepia():
    global matrice_pixels
    matrice_pixels  = filtre_sepia(matrice_pixels)
    rafraichir(matrice_pixels)

def callback_filtre_luminosite():
    global dialogue_effet, matrice_pixels, matrice_temporaire

    matrice_temporaire = np.array(matrice_pixels, copy=True)
    
    dialogue_effet = tk.Toplevel(fenetre_principale)
    dialogue_effet.title("Luminosité")
    dialogue_effet.geometry("300x150")
    dialogue_effet.grab_set()
    slider = tk.Scale(dialogue_effet, from_=0.05, to=0.95, orient=tk.HORIZONTAL, length=200, resolution=0.01, digits=2)
    slider.set(0.50)
    slider.pack(pady=20)

    slider.config(command=lambda x: transition_luminosite(slider))

    frame_boutons = tk.Frame(dialogue_effet)
    frame_boutons.pack(side=tk.BOTTOM, pady=10)

    bouton_appliquer = tk.Button(frame_boutons, text="Appliquer", command=applique_effet)
    bouton_appliquer.pack(side=tk.LEFT, padx=10)

    bouton_annuler = tk.Button(frame_boutons, text="Annuler", command=annule_effet)
    bouton_annuler.pack(side=tk.LEFT, padx=10)

def callback_filtre_contraste():
    global dialogue_effet, matrice_pixels, matrice_temporaire

    matrice_temporaire = np.array(matrice_pixels, copy=True)
    
    dialogue_effet = tk.Toplevel(fenetre_principale)
    dialogue_effet.title("Contraste")
    dialogue_effet.geometry("300x300")
    dialogue_effet.grab_set()

    slider1 = tk.Scale(dialogue_effet, from_=-0.95, to=0.95, orient=tk.HORIZONTAL, length=200, resolution=0.01, digits=2, label='Contraste')
    slider1.set(0.0)
    slider1.pack(pady=20)

    slider2 = tk.Scale(dialogue_effet, from_=0.05, to=0.95, orient=tk.HORIZONTAL, length=200, resolution=0.01, digits=2, label='Pivot')
    slider2.set(0.50)
    slider2.pack(pady=20)

    slider1.config(command=lambda x: transition_contraste(slider1, slider2))
    slider2.config(command=lambda x: transition_contraste(slider1, slider2))

    frame_boutons = tk.Frame(dialogue_effet)
    frame_boutons.pack(side=tk.BOTTOM, pady=10)

    bouton_appliquer = tk.Button(frame_boutons, text="Appliquer", command=applique_effet)
    bouton_appliquer.pack(side=tk.LEFT, padx=10)

    bouton_annuler = tk.Button(frame_boutons, text="Annuler", command=annule_effet)
    bouton_annuler.pack(side=tk.LEFT, padx=10)

def callback_filtre_flou():
    global matrice_pixels
    matrice_pixels = filtre_flou(matrice_pixels)
    rafraichir(matrice_pixels)

def callback_filtre_nettete():
    global matrice_pixels
    matrice_pixels = filtre_nettete(matrice_pixels)
    rafraichir(matrice_pixels)

def callback_filtre_fusion():
    global matrice_pixels, matrice_temporaire

    deuxieme_fichier = str(filedialog.askopenfilename(title="Ouvrir une image"))

    if deuxieme_fichier != None:
        deuxieme_image = Image.open(deuxieme_fichier)

        largeur = matrice_pixels.shape[1]
        hauteur = matrice_pixels.shape[0]
        deuxieme_image = deuxieme_image.resize((largeur, hauteur), Image.Resampling.LANCZOS)

        matrice_pixels_2 = np.array(deuxieme_image)
        matrice_pixels = filtre_fusion(matrice_pixels, matrice_pixels_2)
        rafraichir(matrice_pixels)

def callback_filtre_flou_gaussien():
    global matrice_pixels
    matrice_pixels = filtre_flou_gaussien(matrice_pixels)
    rafraichir(matrice_pixels)

def callback_filtre_nettete_gaussien():
    global matrice_pixels
    matrice_pixels = filtre_nettete_gaussien(matrice_pixels)
    rafraichir(matrice_pixels)

# Création de la fenêtre principale

fenetre_principale = tk.Tk()
fenetre_principale.geometry("1000x800")
fenetre_principale.title('UVSQolor')

canvas = tk.Canvas(fenetre_principale)
canvas.pack()

menu_principale = tk.Menu(fenetre_principale)
fenetre_principale.config(menu=menu_principale)

menu_fichier = tk.Menu(menu_principale, tearoff=0)
menu_edition = tk.Menu(menu_principale, tearoff=0)
menu_filtre = tk.Menu(menu_principale, tearoff=0)
menu_principale.add_cascade(label="Fichier", menu=menu_fichier)
menu_principale.add_cascade(label="Édition", menu=menu_edition)
menu_principale.add_cascade(label="Filtre", menu=menu_filtre)

menu_fichier.add_command(label="Ouvrir", command=callback_ouvrir, state="normal")
menu_fichier.add_command(label="Sauvegarder", command=callback_sauvegarder, state="disabled") 
menu_fichier.add_command(label="Quitter", command=callback_quitter, state="normal") 

menu_edition.add_command(label="Annuler", command=callback_annuler, state="disabled") 
menu_edition.add_command(label="Rétablir", command=callback_retablir, state="disabled") 
menu_edition.add_command(label="Réinitialisé", command=callback_reinitialise, state="disabled") 

# menu filtre

menu_reglages = tk.Menu(menu_filtre, tearoff=0)
menu_filtre.add_cascade(label="Réglages", menu=menu_reglages)
menu_reglages.add_command(label='Luminosité', command=callback_filtre_luminosite, state="disabled")
menu_reglages.add_command(label='Contraste', command=callback_filtre_contraste, state="disabled")
menu_reglages.add_separator()
menu_reglages.add_command(label='Sépia', command=callback_filtre_sepia, state="disabled")

menu_couleur = tk.Menu(menu_reglages, tearoff=0)
menu_reglages.add_cascade(label='Couleurs', menu=menu_couleur)
menu_couleur.add_command(label='Vert', command=callback_filtre_vert, state="disabled")
menu_couleur.add_command(label='Bleu', command=callback_filtre_bleu, state='disabled')
menu_couleur.add_command(label='Rouge', command=callback_filtre_rouge, state='disabled')
menu_couleur.add_command(label='Noir et Blanc', command=callback_filtre_noir_blanc, state='disabled')

menu_focus = tk.Menu(menu_filtre, tearoff=0)
menu_filtre.add_cascade(label="Flou et Netteté", menu=menu_focus)
menu_focus.add_command(label='Netteté', command=callback_filtre_nettete, state='disabled')
menu_focus.add_command(label='Netteté Gaussien', command=callback_filtre_nettete_gaussien, state='disabled')
menu_focus.add_command(label='Flou', command=callback_filtre_flou, state='disabled')
menu_focus.add_command(label='Flou Gaussien', command=callback_filtre_flou_gaussien, state='disabled')

menu_filtre.add_separator()
menu_filtre.add_command(label='Fusion', command=callback_filtre_fusion, state='disabled')