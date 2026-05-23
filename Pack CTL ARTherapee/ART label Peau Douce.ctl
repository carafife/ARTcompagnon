// @ART-label: "Peau Douce (masque manuel)"
// @ART-colorspace: "rec2020"
// Powered By Carafife And DeepSeek V4

import "_artlib";

// @ART-param: ["hueShift", "Correction teinte", -20.0, 20.0, 0.0, 0.5]
// @ART-param: ["satAdj", "Saturation (+/-)", -0.02, 0.02, -0.01, 0.01]
// @ART-param: ["lumAdj", "Luminosité (+/-)", -0.05, 0.05, 0.0, 0.01]
// @ART-param: ["strength", "Force", 0.0, 1.0, 0.5, 0.01]

void ART_main(
    varying float r,
    varying float g,
    varying float b,
    output varying float rout,
    output varying float gout,
    output varying float bout,
    float hueShift,
    float satAdj,
    float lumAdj,
    float strength
)
{
    // Convertir RGB en OkHcl
    float h, s, l;
    rgb2okhcl(r, g, b, h, s, l);

    // Appliquer les ajustements
    float hueShiftRad = hueShift * M_PI / 180.0;
    float newH = h + hueShiftRad * strength;

    float newS = s + satAdj;
    if (newS < 0.0) newS = 0.0;
    if (newS > 1.0) newS = 1.0;
    float finalS = s + (newS - s) * strength;

    float newL = l + lumAdj;
    if (newL < 0.0) newL = 0.0;
    if (newL > 1.0) newL = 1.0;
    float finalL = l + (newL - l) * strength;

    // Convertir OkHcl en RGB
    okhcl2rgb(newH, finalS, finalL, rout, gout, bout);
}
