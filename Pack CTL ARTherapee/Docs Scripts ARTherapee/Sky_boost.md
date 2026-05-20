## 3. Sky Boost (ciel)

**But** : redonner du contraste et de la saturation aux ciels sans toucher aux nuages ni au reste de l’image.

### Paramètres

- **Teinte du ciel** – la couleur de référence du ciel (par défaut 240° pour un bleu standard).  
- **Largeur de la zone** – étendue autour de cette teinte pour englober toutes les nuances de bleu.  
- **Transition douce** – adoucit la limite entre ciel modifié et zones non modifiées.  
- **Force** – intensité globale (0 = rien, 1 = maximum).  
- **Contraste (courbe)** – courbe de luminance appliquée uniquement au ciel. Ligne droite par défaut (pas de changement). Créez une courbe en S pour donner du punch.  
- **Saturation (+/-)** – curseur simple pour booster (+) ou réduire (−) la saturation du ciel.  
- **Protection nuages** – seuil de luminance au-dessus duquel l’effet diminue (les nuages blancs sont préservés).

### Exemple : ciel terne → ciel profond

1. **Teinte du ciel** = 240.  
2. **Largeur de la zone** = 50 (inclut les bleus clairs et foncés).  
3. **Transition douce** = 15.  
4. **Force** = 0.8.  
5. **Contraste** : créez une courbe en S (abaissez le point à 0.4, remontez celui à 0.6).  
6. **Saturation** = 0.2 (boost modéré).  
7. **Protection nuages** = 0.8 (les zones très claires sont épargnées).

### Astuce
Si le ciel devient trop artificiel, baissez la force ou réduisez la courbe de contraste. Pour protéger davantage les nuages, diminuez le seuil de protection.
