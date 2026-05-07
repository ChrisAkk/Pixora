# 🎨 UVSQolor — Éditeur de filtres photo

UVSQolor est une application desktop de traitement d'image développée en Python avec Tkinter. Elle permet d'ouvrir une image, d'y appliquer différents filtres (couleur, luminosité, flou, netteté, fusion...) et de sauvegarder le résultat.

Projet réalisé en L1 Informatique à l'Université Paris-Saclay (UVSQ).

---

## ✨ Fonctionnalités

### 🎨 Filtres de couleur
- **Rouge / Vert / Bleu** — Isole un canal de couleur
- **Noir et Blanc** — Conversion en niveaux de gris
- **Sépia** — Effet vintage chaud

### ☀️ Réglages
- **Luminosité** — Slider interactif avec aperçu en temps réel (correction gamma)
- **Contraste** — Réglage du contraste et du pivot avec aperçu en temps réel

### 🔍 Flou & Netteté
- **Flou** — Flou par convolution (noyau moyen 3×3)
- **Flou Gaussien** — Flou par noyau gaussien 3×3
- **Netteté** — Accentuation par masque flou
- **Netteté Gaussienne** — Accentuation par masque gaussien

### 🖼️ Autres
- **Fusion** — Fusionne deux images en les moyennant pixel par pixel

### 📁 Gestion de fichiers
- Ouvrir une image (PNG, JPG, etc.)
- Sauvegarder l'image modifiée
- Annuler / Rétablir les modifications
- Réinitialiser à l'image d'origine

---

## 🛠️ Stack technique

| Technologie | Rôle |
|---|---|
| Python | Langage principal |
| Tkinter | Interface graphique desktop |
| Pillow (PIL) | Chargement et affichage des images |
| NumPy | Manipulation des matrices de pixels |
| SciPy | Convolution 2D pour les filtres flou/netteté |

---

## 🚀 Installation

### Prérequis
- Python 3.8+

### Étapes

```bash
# 1. Clone le repo
git clone https://github.com/ChrisAkk/UVSQolor.git
cd UVSQolor

# 2. Installe les dépendances
pip install pillow numpy scipy

# 3. Lance l'application
python main.py
```

---

## 📁 Structure du projet

```
UVSQolor/
├── main.py         # Point d'entrée — lance la fenêtre principale
├── interface.py    # Interface Tkinter, menus, callbacks et gestion de l'état
├── filtres.py      # Algorithmes de traitement d'image (NumPy / SciPy)
├── img/
│   └── paysage.jpg # Image d'exemple
└── LICENSE
```

---

## 🎓 Contexte

Projet réalisé en première année de licence informatique à l'**UVSQ** (Université de Versailles Saint-Quentin-en-Yvelines / Paris-Saclay). L'objectif était d'implémenter des algorithmes de traitement d'image from scratch en manipulant directement les matrices de pixels.