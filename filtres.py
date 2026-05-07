import numpy as np
import math 
from scipy.signal import convolve2d 

# Algorithmes de filtre
def filtre_vert(matrice_pixels):
    resultat = np.array(matrice_pixels, copy=True) 

    resultat[:,:,0] = 0
    resultat[:,:,2] = 0

    return resultat

def filtre_sepia(matrice_pixels):
    max_value = float(np.iinfo(matrice_pixels.dtype).max)
    matrice_pixels = np.array(matrice_pixels, copy=True)

    R = matrice_pixels[:,:,0]
    G = matrice_pixels[:,:,1]
    B = matrice_pixels[:,:,2]

    resultat = np.array(matrice_pixels, copy=True).astype(float)

    resultat[:,:,0] = R * 0.76 + G * 0.25 + B * 0.34
    resultat[:,:,1] = R * 0.65 + G * 0.20 + B * 0.40
    resultat[:,:,2] = R * 0.53 + G * 0.20 + B * 0.27 

    resultat = resultat.clip(0, max_value).astype(np.uint8)

    return resultat

def filtre_luminosite(matrice_pixels, valeur_curseur):

    m = float(valeur_curseur)
    max_value = float(np.iinfo(matrice_pixels.dtype).max)
    gamma = math.log(m)/math.log(0.5)

    x = matrice_pixels.astype(float) / max_value
    resultat = (x ** gamma) * max_value

    return resultat.astype(np.uint8)

def filtre_contraste(matrice_pixels, contraste, pivot):

    gamma = 2 ** float(contraste) 
    pivot = float(pivot)
    pivot = max(0.001, min(0.999, pivot))

    x = matrice_pixels.astype(float) / 255.0

    masque_haut = x > pivot
    masque_bas = x <= pivot

    resultat = np.array(x, copy=True)
    resultat[masque_haut] = 1 - (1 - pivot) * ((1 - x[masque_haut]) / (1 - pivot))**gamma
    resultat[masque_bas] = pivot * (x[masque_bas] / pivot) ** gamma
    resultat *= 255

    return resultat.astype(np.uint8)

def filtre_flou(matrice_pixels):
    
    liste_noyau = [[1, 1, 1] for i in range(3)]
    kernel = np.array(liste_noyau) / 9

    matrice_flou = np.array(matrice_pixels, copy=True).astype(float)

    for i in range(3):
        matrice_flou[:,:,i] = convolve2d(matrice_pixels[:,:,i], kernel, mode="same", boundary="symm")

    matrice_flou = matrice_flou.astype(np.uint8)
    return matrice_flou

def filtre_nettete(matrice_pixels):
    I = matrice_pixels.astype(float)
    B = filtre_flou(I).astype(float)

    D = I - B
    resultat = I + D
    resultat = resultat.clip(0, 255).astype(np.uint8)

    return resultat

def filtre_fusion(matrice1, matrice2):
    matrice1 = matrice1.astype(float)
    matrice2 = matrice2.astype(float)

    matrice = np.round((matrice1 + matrice2) / 2)
    matrice = np.clip(matrice, 0, 255)

    return matrice.astype(np.uint8)

def filtre_flou_gaussien(matrice_pixels):

    liste_noyau = [[1, 2, 1], [2, 4, 2], [1, 2, 1]]
    kernel = np.array(liste_noyau) / 16

    matrice_flou = np.array(matrice_pixels, copy=True).astype(float)

    for i in range(3):
        matrice_flou[:,:,i] = convolve2d(matrice_pixels[:,:,i], kernel, mode="same", boundary="symm")

    matrice_flou = matrice_flou.astype(np.uint8)
    return matrice_flou

def filtre_nettete_gaussien(matrice_pixels):
    I = matrice_pixels.astype(float)
    B = filtre_flou_gaussien(I).astype(float)

    D = I - B
    resultat = I + D
    resultat = resultat.clip(0, 255).astype(np.uint8)

    return resultat

# filtre de couleurs 

def filtre_vert(matrice_pixels):
    resultat = np.array(matrice_pixels, copy=True) 

    resultat[:,:,0] = 0
    resultat[:,:,2] = 0

    return resultat

def filtre_bleu(matrice_pixels):
    resultat = np.array(matrice_pixels, copy=True) 

    resultat[:,:,0] = 0
    resultat[:,:,1] = 0

    return resultat

def filtre_rouge(matrice_pixels):
    resultat = np.array(matrice_pixels, copy=True) 

    resultat[:,:,1] = 0
    resultat[:,:,2] = 0

    return resultat

def filtre_noir_blanc(matrice_pixels):
    resultat = np.array(matrice_pixels, copy=True).astype(float)

    gris = (resultat[:,:,0] + resultat[:,:,1] + resultat[:,:,2]) / 3
    
    resultat[:,:,0] = gris
    resultat[:,:,1] = gris
    resultat[:,:,2] = gris

    resultat.clip(0, 255)

    return resultat.astype(np.uint8)