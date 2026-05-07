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
FONT = "Helvetica"

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

def transition_avance_rgb(points):
    global matrice_pixels, matrice_temporaire

    rouge = (225 - points["R"][1]) / 120
    vert  = (225 - points["G"][1]) / 120
    bleu  = (225 - points["B"][1]) / 120

    matrice_temporaire = filtre_avance_rgb(matrice_pixels, rouge, vert, bleu)
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
        frame_intro.pack_forget()
        frame_principal.pack(fill="both", expand=True) 

        menu_fichier.entryconfig('Sauvegarder', state='normal')

        menu_edition.entryconfig('Annuler', state='normal')
        menu_edition.entryconfig('Rétablir', state='normal')
        menu_edition.entryconfig('Réinitialisé', state='normal')
        menu_edition.entryconfig('Retirer', state='normal')

        menu_reglages.entryconfig('Luminosité', state='normal')
        menu_reglages.entryconfig('Contraste', state='normal')
        menu_reglages.entryconfig('Sépia', state='normal')
        menu_couleur.entryconfig('Rouge', state='normal')
        menu_couleur.entryconfig('Vert', state='normal')
        menu_couleur.entryconfig('Bleu', state='normal')
        menu_couleur.entryconfig('Noir et Blanc', state='normal')
        menu_couleur.entryconfig('Avancé', state='normal')
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

def callback_retirer():
    global matrice_pixels, matrice_temporaire, archive_redo, archive_undo

    matrice_temporaire = None
    matrice_pixels = None
    archive_redo = []
    archive_undo = []

    canvas.delete('all')
    frame_principal.pack_forget()
    frame_intro.place(relx=0.5, rely=0.5, anchor="center")

    menu_fichier.entryconfig('Sauvegarder', state='disabled')

    menu_edition.entryconfig('Annuler', state='disabled')
    menu_edition.entryconfig('Rétablir', state='disabled')
    menu_edition.entryconfig('Réinitialisé', state='disabled')
    menu_edition.entryconfig('Retirer', state='disabled')

    menu_reglages.entryconfig('Luminosité', state='disabled')
    menu_reglages.entryconfig('Contraste', state='disabled')
    menu_reglages.entryconfig('Sépia', state='disabled')
    menu_couleur.entryconfig('Rouge', state='disabled')
    menu_couleur.entryconfig('Vert', state='disabled')
    menu_couleur.entryconfig('Bleu', state='disabled')
    menu_couleur.entryconfig('Noir et Blanc', state='disabled')
    menu_couleur.entryconfig('Avancé', state='disabled')
    menu_focus.entryconfig('Netteté', state='disabled')
    menu_focus.entryconfig('Flou', state='disabled')
    menu_focus.entryconfig('Flou Gaussien', state='disabled')
    menu_focus.entryconfig('Netteté Gaussien', state='disabled')
    menu_filtre.entryconfig('Fusion', state='disabled')

# Callbacks filtres

def callback_filtre_rouge():
    global matrice_pixels
    matrice_pixels  = filtre_rouge(matrice_pixels)
    rafraichir(matrice_pixels)

def callback_filtre_vert():
    global matrice_pixels
    matrice_pixels  = filtre_vert(matrice_pixels)
    rafraichir(matrice_pixels)

def callback_filtre_bleu():
    global matrice_pixels
    matrice_pixels  = filtre_bleu(matrice_pixels)
    rafraichir(matrice_pixels)

def callback_filtre_noir_blanc():
    global matrice_pixels
    matrice_pixels  = filtre_noir_blanc(matrice_pixels)
    rafraichir(matrice_pixels)

def callback_avance_rgb():

    global matrice_pixels, matrice_temporaire, dialogue_effet

    matrice_temporaire = np.array(matrice_pixels, copy=True)

    dialogue_effet = tk.Toplevel(fenetre_principale)
    dialogue_effet.title("Mode avancé RGB")
    dialogue_effet.geometry("700x650")
    dialogue_effet.configure(bg="#0f1116")
    dialogue_effet.grab_set()

    titre = tk.Label(dialogue_effet, text="Courbes RGB", bg="#0f1116", fg="white", font=(FONT, 20, "bold"))
    titre.pack(pady=20)

    canvas_courbe = tk.Canvas(dialogue_effet, width=600, height=450, bg="#181c24", highlightthickness=1, highlightbackground="#2d3445")
    canvas_courbe.pack(pady=10)

    points = {"R": [150, 225], "G": [300, 225], "B": [450, 225]}
    couleurs = {"R": "#ff4d4d", "G": "#53ff53", "B": "#5b7cff"}
    point_selectionne = [None]


    def dessiner():
        canvas_courbe.delete("all")
        largeur = 600
        hauteur = 450

        for i in range(0, largeur, 50):
            canvas_courbe.create_line(i, 0, i, hauteur, fill="#252b38")

        for i in range(0, hauteur, 50):
            canvas_courbe.create_line(0, i, largeur, i, fill="#252b38")

        canvas_courbe.create_line(0, hauteur / 2, largeur,hauteur / 2, fill="#555", dash=(4, 2))

        liste_points = [points[nom] for nom in ["R", "G", "B"]]
        for i in range(len(liste_points) - 1):
            x1, y1 = liste_points[i]
            x2, y2 = liste_points[i + 1]
            canvas_courbe.create_line(x1, y1, x2, y2, fill="#6c63ff", width=4, smooth=True)

        for nom, (x, y) in points.items():
            canvas_courbe.create_oval(x - 12, y - 12, x + 12, y + 12, fill=couleurs[nom], outline="white", width=2)
            canvas_courbe.create_text(x, y - 22, text=nom, fill="white", font=(FONT, 11, "bold"))

    def clique(event):
        for nom, (x, y) in points.items():
            if abs(event.x - x) < 15 and abs(event.y - y) < 15:
                point_selectionne[0] = nom

    def drag(event):
        nom = point_selectionne[0]
        if nom is None:
            return

        points[nom] = [points[nom][0], int(np.clip(event.y, 50, 400))]
        dessiner()
        transition_avance_rgb(points)

    def release(event):
        point_selectionne[0] = None

    frame_boutons = tk.Frame(dialogue_effet, bg="#0f1116")
    frame_boutons.pack(pady=20)

    bouton_appliquer = tk.Label(frame_boutons, text="Appliquer", bg="SlateBlue", fg="white", relief="flat", font=(FONT, 11, "bold"), padx=20, pady=8, cursor="pointinghand")
    bouton_appliquer.bind("<Button-1>", lambda x: applique_effet())
    bouton_appliquer.pack(side="left", padx=10)

    bouton_annuler = tk.Label(frame_boutons, text="Annuler", bg="DimGray", fg="white", relief="flat", font=(FONT, 11, "bold"), padx=20, pady=8, cursor="pointinghand")
    bouton_annuler.bind("<Button-1>", lambda x: annule_effet())
    bouton_annuler.pack(side="left", padx=10)

    canvas_courbe.bind("<Button-1>", clique)
    canvas_courbe.bind("<B1-Motion>", drag)
    canvas_courbe.bind("<ButtonRelease-1>", release)

    dessiner()

def callback_filtre_sepia():
    global matrice_pixels
    matrice_pixels  = filtre_sepia(matrice_pixels)
    rafraichir(matrice_pixels)

def callback_filtre_luminosite():
    global dialogue_effet, matrice_pixels, matrice_temporaire

    matrice_temporaire = np.array(matrice_pixels, copy=True)

    dialogue_effet = tk.Toplevel(fenetre_principale)
    dialogue_effet.title("Luminosité")
    dialogue_effet.geometry("360x220")
    dialogue_effet.configure(bg="#0f1116")
    dialogue_effet.grab_set()

    tk.Label(dialogue_effet, text="Luminosité", bg="#0f1116", fg="white", font=(FONT, 16, "bold")).pack(pady=20)
    tk.Label(dialogue_effet, text="Intensité", bg="#0f1116", fg="#aaaaaa", font=(FONT, 10)).pack(anchor="w", padx=30)

    slider = tk.Scale(dialogue_effet, from_=0.05, to=0.95, orient=tk.HORIZONTAL, length=280, resolution=0.01, digits=2, bg="#0f1116", fg="white", troughcolor="#2d3445", highlightthickness=0, activebackground="#6c63ff")
    slider.set(0.50)
    slider.pack(padx=30)
    slider.config(command=lambda x: transition_luminosite(slider))

    frame_boutons = tk.Frame(dialogue_effet, bg="#0f1116")
    frame_boutons.pack(pady=20)

    bouton_appliquer = tk.Label(frame_boutons, text="Appliquer", bg="SlateBlue", fg="white", font=(FONT, 11, "bold"), padx=20, pady=8, cursor="pointinghand")
    bouton_appliquer.bind("<Button-1>", lambda e: applique_effet())
    bouton_appliquer.pack(side=tk.LEFT, padx=10)

    bouton_annuler = tk.Label(frame_boutons, text="Annuler", bg="#252b38", fg="white", font=(FONT, 11, "bold"), padx=20, pady=8, cursor="pointinghand")
    bouton_annuler.bind("<Button-1>", lambda e: annule_effet())
    bouton_annuler.pack(side=tk.LEFT, padx=10)

def callback_filtre_contraste():
    global dialogue_effet, matrice_pixels, matrice_temporaire

    matrice_temporaire = np.array(matrice_pixels, copy=True)

    dialogue_effet = tk.Toplevel(fenetre_principale)
    dialogue_effet.title("Contraste")
    dialogue_effet.geometry("360x300")
    dialogue_effet.configure(bg="#0f1116")
    dialogue_effet.grab_set()

    tk.Label(dialogue_effet, text="Contraste", bg="#0f1116", fg="white", font=(FONT, 16, "bold")).pack(pady=20)
    tk.Label(dialogue_effet, text="Contraste", bg="#0f1116", fg="#aaaaaa", font=(FONT, 10)).pack(anchor="w", padx=30, pady=(0, 0))

    slider1 = tk.Scale(dialogue_effet, from_=-0.95, to=0.95, orient=tk.HORIZONTAL, length=280, resolution=0.01, digits=2, bg="#0f1116", fg="white", troughcolor="#2d3445", highlightthickness=0, activebackground="#6c63ff")
    slider1.set(0.0)
    slider1.pack(padx=30, pady=(0, 0))

    tk.Label(dialogue_effet, text="Pivot", bg="#0f1116", fg="#aaaaaa", font=(FONT, 10)).pack(anchor="w", padx=30, pady=(16, 0))

    slider2 = tk.Scale(dialogue_effet, from_=0.05, to=0.95, orient=tk.HORIZONTAL, length=280, resolution=0.01, digits=2, bg="#0f1116", fg="white", troughcolor="#2d3445", highlightthickness=0, activebackground="#6c63ff")
    slider2.set(0.50)
    slider2.pack(padx=30, pady=(0, 0))  

    slider1.config(command=lambda x: transition_contraste(slider1, slider2))
    slider2.config(command=lambda x: transition_contraste(slider1, slider2))

    frame_boutons = tk.Frame(dialogue_effet, bg="#0f1116")
    frame_boutons.pack(pady=20)

    bouton_appliquer = tk.Label(frame_boutons, text="Appliquer", bg="SlateBlue", fg="white", font=(FONT, 11, "bold"), padx=20, pady=8, cursor="pointinghand")
    bouton_appliquer.bind("<Button-1>", lambda e: applique_effet())
    bouton_appliquer.pack(side=tk.LEFT, padx=10)

    bouton_annuler = tk.Label(frame_boutons, text="Annuler", bg="#252b38", fg="white", font=(FONT, 11, "bold"), padx=20, pady=8, cursor="pointinghand")
    bouton_annuler.bind("<Button-1>", lambda e: annule_effet())
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
fenetre_principale.geometry("1200x850")
fenetre_principale.title("Pixaura")
fenetre_principale.configure(bg="#0f1116")

barre_haut = tk.Frame(fenetre_principale, bg="#161a22", height=50)
barre_haut.pack(fill="x", side="top")
label_titre = tk.Label(barre_haut, text="Pixaura - Éditeur d'image", bg="#161a22", fg="white", font=(FONT, 14, "bold"))
label_titre.pack(side="left", padx=20)

frame_intro = tk.Frame(fenetre_principale, bg="#0f1116")
frame_intro.place(relx=0.5, rely=0.5, anchor="center")
tk.Label(frame_intro, text="Ouvrez une image pour commencez", font=(FONT, 26, "bold"), fg="white", bg="#0f1116").pack()

frame_principal = tk.Frame(fenetre_principale, bg="#0f1116")

frame_image = tk.Frame(frame_principal, bg="#181c24", bd=0, highlightthickness=1, highlightbackground="#2d3445")
frame_image.pack(side="left", fill="both", expand=True, padx=20, pady=20)

canvas = tk.Canvas(frame_image, bg="#11151c", highlightthickness=0)
canvas.pack(fill="both", expand=True, padx=10, pady=10)

# Menu

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
menu_edition.add_command(label="Retirer", command=callback_retirer, state="disabled")

# menu filtre

menu_reglages = tk.Menu(menu_filtre, tearoff=0)
menu_filtre.add_cascade(label="Réglages", menu=menu_reglages)
menu_reglages.add_command(label='Luminosité', command=callback_filtre_luminosite, state="disabled")
menu_reglages.add_command(label='Contraste', command=callback_filtre_contraste, state="disabled")
menu_reglages.add_separator()
menu_reglages.add_command(label='Sépia', command=callback_filtre_sepia, state="disabled")

menu_couleur = tk.Menu(menu_reglages, tearoff=0)
menu_reglages.add_cascade(label='Couleurs', menu=menu_couleur)
menu_couleur.add_command(label='Rouge', command=callback_filtre_rouge, state='disabled')
menu_couleur.add_command(label='Vert', command=callback_filtre_vert, state="disabled")
menu_couleur.add_command(label='Bleu', command=callback_filtre_bleu, state='disabled')
menu_couleur.add_command(label='Noir et Blanc', command=callback_filtre_noir_blanc, state='disabled')
menu_couleur.add_command(label='Avancé', command=callback_avance_rgb, state='disabled')

menu_focus = tk.Menu(menu_filtre, tearoff=0)
menu_filtre.add_cascade(label="Flou et Netteté", menu=menu_focus)
menu_focus.add_command(label='Netteté', command=callback_filtre_nettete, state='disabled')
menu_focus.add_command(label='Netteté Gaussien', command=callback_filtre_nettete_gaussien, state='disabled')
menu_focus.add_command(label='Flou', command=callback_filtre_flou, state='disabled')
menu_focus.add_command(label='Flou Gaussien', command=callback_filtre_flou_gaussien, state='disabled')

menu_filtre.add_separator()
menu_filtre.add_command(label='Fusion', command=callback_filtre_fusion, state='disabled')