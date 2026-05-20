// @ART-label: "Harmoniseur de couleurs Pro"
// @ART-colorspace: "rec2020"

import "_artlib";

// @ART-param: ["srcHue", "Couleur à remplacer (°)", 0.0, 360.0, 120.0, 1.0]
// @ART-param: ["wid", "Largeur de la plage", 0.0, 180.0, 30.0, 1.0]
// @ART-param: ["fea", "Adoucissement", 0.0, 90.0, 10.0, 1.0]
// @ART-param: ["tgtHue", "Nouvelle couleur (°)", 0.0, 360.0, 30.0, 1.0]
// @ART-param: ["strcurve", "Force (courbe)", 2, ["ControlPoints", 0.0, 0.5, 0.35, 0.35, 0.25, 0.5, 0.35, 0.35, 0.5, 0.5, 0.35, 0.35, 0.75, 0.5, 0.35, 0.35, 1.0, 0.5, 0.35, 0.35], [[0.0, 0.6, 0.3, 0.5], [0.25, 0.6, 0.5, 0.3], [0.5, 0.5, 0.6, 0.3], [0.75, 0.3, 0.6, 0.5], [1.0, 0.6, 0.3, 0.5]], 0, "$CTL_CHANNEL;Channel"]

void ART_main(
    varying float r,
    varying float g,
    varying float b,
    output varying float rout,
    output varying float gout,
    output varying float bout,
    float srcHue,
    float wid,
    float fea,
    float tgtHue,
    float strcurve[256]
)
{
    float hsl[3] = rgb2okhcl(r, g, b);
    float px_hue = hsl[0];
    float px_sat = hsl[1];
    float px_lum = hsl[2];

    float src_rad = srcHue * M_PI / 180.0;
    float tgt_rad = tgtHue * M_PI / 180.0;

    float dh_rad = px_hue - src_rad;
    if (dh_rad > M_PI) dh_rad = dh_rad - 2.0 * M_PI;
    if (dh_rad < -M_PI) dh_rad = dh_rad + 2.0 * M_PI;
    float dh_deg = dh_rad * 180.0 / M_PI;
    float adist;
    if (dh_deg < 0.0) adist = -dh_deg;
    else adist = dh_deg;

    float mask;
    if (adist <= wid) mask = 1.0;
    else if (adist <= wid + fea) mask = 1.0 - (adist - wid) / fea;
    else mask = 0.0;

    float h01 = px_hue / (2.0 * M_PI);
    if (h01 < 0.0) h01 = h01 + 1.0;
    if (h01 >= 1.0) h01 = h01 - 1.0;
    float str_val = luteval(strcurve, h01);

    float delta_rad = tgt_rad - px_hue;
    if (delta_rad > M_PI) delta_rad = delta_rad - 2.0 * M_PI;
    if (delta_rad < -M_PI) delta_rad = delta_rad + 2.0 * M_PI;
    float new_hue = px_hue + delta_rad * mask * str_val;

    float new_hsl[3];
    new_hsl[0] = new_hue;
    new_hsl[1] = px_sat;
    new_hsl[2] = px_lum;
    float new_rgb[3] = okhcl2rgb(new_hsl);
    rout = new_rgb[0];
    gout = new_rgb[1];
    bout = new_rgb[2];
}
