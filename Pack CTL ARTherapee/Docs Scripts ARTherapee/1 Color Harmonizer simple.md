## 1. Color Harmonizer (simple)

**But** : remplacer une plage de couleurs par une autre, tout en gardant la luminosité et la saturation d’origine.

### Paramètres

- **Couleur à remplacer (°)** – la teinte à modifier (ex. 120 = vert, 30 = orange).  
- **Largeur de la plage** – combien de nuances autour de cette couleur sont incluses. Plus large = plus de pixels affectés.  
- **Adoucissement** – lisse la transition sur les bords de la plage (évite les cassures).  
- **Nouvelle couleur (°)** – la teinte finale souhaitée.  
- **Force** – intensité de l’effet : 0 = aucun, 1 = remplacement total.

### Exemple : verts → orangés

1. **Couleur à remplacer** = 120 (vert).  
2. **Largeur de la plage** = 30 (inclut vert‑jaune et vert‑bleu).  
3. **Adoucissement** = 10.  
4. **Nouvelle couleur** = 30 (orange).  
5. **Force** = 0.7 (effet visible mais naturel).

### Astuce
Mettez la force à 1.0 et la largeur petite au début pour bien voir la zone modifiée, puis ajustez.


Voici un tableau des teintes plus complet, que vous pouvez garder à côté de vos scripts **Color Harmonizer** (simple et Pro). Il couvre les principales couleurs et leurs nuances.

### Tableau des teintes (en degrés)

| **Couleur**              | **Degrés** | **Code visuel**       |
|--------------------------|------------|-----------------------|
| Rouge pur                | 0 / 360    | 🔴                    |
| Rouge orangé             | 15         | 🟠                    |
| Orange                   | 30         | 🟠                    |
| Orangé jaune             | 45         | 🟡                    |
| Jaune                    | 60         | 🟡                    |
| Jaune verdâtre           | 75         | 🟢                    |
| Vert chartreuse          | 90         | 🟢                    |
| Vert                     | 120        | 🟢                    |
| Vert bleuté              | 150        | 🟢                    |
| Cyan                     | 180        | 🔵                    |
| Bleu clair               | 210        | 🔵                    |
| Bleu                     | 240        | 🔵                    |
| Bleu violacé             | 270        | 🟣                    |
| Magenta                  | 300        | 🟣                    |
| Rose                     | 330        | 🟣                    |
| Rouge (retour)           | 360        | 🔴                    |

### Comment utiliser ce tableau

1. **Trouver la teinte à modifier** : repérez dans l’image la couleur dominante de la zone à harmoniser (par exemple, un feuillage vert ≈ 120°, un ciel bleu ≈ 240°).  
   - Pour plus de précision, utilisez la pipette d’ART en mode « HSL » (si disponible) ou un outil externe comme une roue chromatique en ligne.  
   - Si vous hésitez entre deux valeurs, arrondissez à la dizaine de degrés la plus proche.

2. **Choisir la nouvelle teinte** : dans le tableau, sélectionnez la couleur que vous souhaitez obtenir. Par exemple, pour transformer un vert en orangé, partez de 120° et visez 30°.

3. **Régler le module** :  
   - **Couleur à remplacer** = teinte source (ex. 120°).  
   - **Nouvelle couleur** = teinte cible (ex. 30°).  
   - Ajustez la largeur de plage pour englober les nuances voisines (ex. 20–40°).  
   - Utilisez l’adoucissement pour éviter les transitions brutales.

4. **Version Pro** : la courbe de force permet de moduler l’effet selon la teinte d’origine (axe horizontal de la courbe). Reportez-vous aux valeurs du tableau pour placer vos bosses ou creux exactement là où vous voulez renforcer/atténuer l’effet. Par exemple, autour de 0,33 (120° / 360° ≈ 0,33) pour le vert.

---

### Astuce mnémotechnique

- **Rouge** = 0/360  
- **Jaune** = 60  
- **Vert** = 120  
- **Cyan** = 180  
- **Bleu** = 240  
- **Magenta** = 300  

Les couleurs intermédiaires (orangé, chartreuse, bleu clair…) sont à mi-chemin entre ces repères. Une fois ces points mémorisés, vous pouvez rapidement estimer n’importe quelle teinte.

Ce tableau peut être affiché à côté de votre écran ou inséré dans votre logiciel de notes pour une consultation rapide pendant la retouche.
