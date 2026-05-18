## Guide du module « Color Harmonizer » (simple)

**But** : Changer la teinte d’une plage de couleurs (par exemple transformer des verts en orangés) tout en conservant la luminosité et la saturation.

### Comment l’activer dans ART

1. Ouvrez votre photo.
2. Dans l’onglet **Couleur / Spécial** (ou équivalent), ajoutez un module **CTL Script**.
3. Dans le menu déroulant du module, choisissez **« Color Harmonizer »**.

### Les cinq curseurs

| Curseur | Rôle | Exemple |
|---------|------|---------|
| **Teinte source** | Couleur à modifier (0 = rouge, 120 = vert, 240 = bleu). | 120 pour les verts. |
| **Largeur plage** | Étendue autour de la teinte source (en degrés). | 30° couvre les verts et verts-jaunes. |
| **Adoucissement** | Transition douce aux bords de la plage. | 10° évite une coupure brutale. |
| **Teinte cible** | Nouvelle couleur désirée. | 30° donne un orangé. |
| **Force** | Intensité de l’effet (0 = aucun, 1 = remplacement complet). | 0,7 pour un effet visible mais naturel. |

### Exemple pas à pas : rendre un feuillage orangé

1. **Teinte source** = 120 (vert pur).
2. **Largeur plage** = 30 (inclut les jaune-vert et vert-bleu).
3. **Adoucissement** = 10.
4. **Teinte cible** = 30 (orangé).
5. **Force** = 1.0 pour voir l’effet maximum, puis réduisez si besoin.

### Conseils

- Placez la **force à 1** et une **largeur faible** au début pour bien visualiser la zone affectée.
- Ajustez la largeur pour englober toutes les nuances que vous voulez modifier.
- Utilisez l’adoucissement pour éviter les cassures entre les zones modifiées et non modifiées.

---

## Guide du module « Color Harmonizer Pro »

**But** : Le même que le simple, mais avec une **courbe de force** qui permet de moduler l’intensité en fonction de la teinte d’origine. Par exemple, appliquer plus d’effet sur les verts clairs et moins sur les verts foncés.

### Activation

Ajoutez un module **CTL Script** et choisissez **« Color Harmonizer Pro (HSL curve) »**.

### Les paramètres

Identiques au simple pour **Teinte source**, **Teinte cible**, **Largeur plage** et **Adoucissement**.

**La courbe « Force »** remplace le curseur de force unique. Elle se présente comme un graphique éditable :

- L’axe horizontal représente la teinte de chaque pixel (0 = rouge, 0.33 = vert, 0.66 = bleu).
- L’axe vertical représente la force appliquée (0 = aucun effet, 1 = effet maximal).

Par défaut, la courbe est une ligne horizontale à **0,5** (force de 50 %). Vous pouvez cliquer-déplacer les points pour créer une forme personnalisée.

### Exemple : effet progressif sur les verts

- Teinte source = 120, cible = 30, largeur = 40.
- Dans la courbe de force, laissez la valeur à 0.5 pour une force modérée, ou créez une bosse au centre (environ 0.33 sur l’axe horizontal) pour renforcer l’effet uniquement sur les verts moyens.

### Conseils

- Pour un effet constant, gardez la courbe plate.
- Pour un effet sélectif, créez une « bosse » autour de la teinte source.
- Vous pouvez même annuler l’effet pour certaines teintes en plaçant la courbe à 0.

---

