// @ART-label: "Ciel Boost"
// @ART-colorspace: "rec2020"

import "_artlib";

// @ART-param: ["skyHue", "Teinte du ciel", 0.0, 360.0, 240.0, 1.0]
// @ART-param: ["skyWidth", "Largeur de la zone", 0.0, 180.0, 50.0, 1.0]
// @ART-param: ["skyFeather", "Transition douce", 0.0, 90.0, 15.0, 1.0]
// @ART-param: ["strength", "Force", 0.0, 1.0, 0.8, 0.01]
// Courbe de contraste
// @ART-param: ["lumcurve", "Contraste (courbe)", 2, ["ControlPoints", 0.0, 0.0, 0.35, 0.35, 1.0, 1.0, 0.35, 0.35], [[0.0, 0.5, 0.5, 0.5], [1.0, 0.5, 0.5, 0.5]], 0, "$CTL_CHANNEL;Channel"]
// Curseur de saturation réduit
// @ART-param: ["satBoost", "Saturation (+/-)", -0.5, 1.0, 0.2, 0.01]
// Protection des nuages
// @ART-param: ["cloudThresh", "Protection nuages", 0.0, 1.0, 0.8, 0.01]

void ART_main(
    varying float r,
    varying float g,
    varying float b,
    output varying float rout,
    output varying float gout,
    output varying float bout,
    float skyHue,
    float skyWidth,
    float skyFeather,
    float strength,
    float lumcurve[256],
    float satBoost,
    float cloudThresh
)
{
    float pix[3] = rgb2okhcl(r, g, b);
    float h = pix[0];
    float s = pix[1];
    float l = pix[2];

    // ----- Masque de teinte (cible le bleu du ciel) -----
    float skyRad = skyHue * M_PI / 180.0;
    float dh = h - skyRad;
    if (dh > M_PI) {
        dh = dh - 2.0 * M_PI;
    }
    if (dh < -M_PI) {
        dh = dh + 2.0 * M_PI;
    }
    float ddeg = dh * 180.0 / M_PI;
    float adist;
    if (ddeg < 0.0) {
        adist = -ddeg;
    } else {
        adist = ddeg;
    }

    float mask;
    if (adist <= skyWidth) {
        mask = 1.0;
    } else if (adist <= skyWidth + skyFeather) {
        mask = 1.0 - (adist - skyWidth) / skyFeather;
    } else {
        mask = 0.0;
    }

    // ----- Protection des nuages (atténue l'effet sur les zones très claires) -----
    float cloudFactor = 1.0;
    if (l > cloudThresh) {
        cloudFactor = 1.0 - (l - cloudThresh) / (1.0 - cloudThresh);
        if (cloudFactor < 0.0) {
            cloudFactor = 0.0;
        }
    }
    mask = mask * cloudFactor;

    // ----- Application du contraste via la courbe de luminance -----
    float newL = luteval(lumcurve, l);
    float finalL = l + (newL - l) * mask * strength;

    // ----- Ajustement de la saturation -----
    float newS = s + satBoost;
    if (newS < 0.0) newS = 0.0;
    if (newS > 1.0) newS = 1.0;
    float finalS = s + (newS - s) * mask * strength;

    // ----- Reconstruction RGB -----
    float newPix[3];
    newPix[0] = h;
    newPix[1] = finalS;
    newPix[2] = finalL;
    float rgb[3] = okhcl2rgb(newPix);
    rout = rgb[0];
    gout = rgb[1];
    bout = rgb[2];
}
