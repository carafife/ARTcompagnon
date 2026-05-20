// @ART-label: "Peau Douce (masque manuel)"
// @ART-colorspace: "rec2020"

import "_artlib";

// @ART-param: ["hueShift", "Correction teinte", -20.0, 20.0, 0.0, 0.5]
// Plage de saturation réduite à ±0.02
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
    float pix[3] = rgb2okhcl(r, g, b);
    float h = pix[0];
    float s = pix[1];
    float l = pix[2];

    // Correction teinte
    float hueShiftRad = hueShift * M_PI / 180.0;
    float newH = h + hueShiftRad * strength;

    // Saturation
    float newS = s + satAdj;
    if (newS < 0.0) newS = 0.0;
    if (newS > 1.0) newS = 1.0;
    float finalS = s + (newS - s) * strength;

    // Luminance
    float newL = l + lumAdj;
    if (newL < 0.0) newL = 0.0;
    if (newL > 1.0) newL = 1.0;
    float finalL = l + (newL - l) * strength;

    // Reconstruction
    float newPix[3];
    newPix[0] = newH;
    newPix[1] = finalS;
    newPix[2] = finalL;
    float rgb[3] = okhcl2rgb(newPix);
    rout = rgb[0];
    gout = rgb[1];
    bout = rgb[2];
}
