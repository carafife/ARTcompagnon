// @ART-label: "Contraste 3 plages"
// Powered By Carafife And DeepSeek V4
// @ART-param: ["shadow", "Ombres", -0.3, 0.3, 0.0, 0.01]
// @ART-param: ["mid", "Tons moyens", -0.5, 0.5, 0.0, 0.01]
// @ART-param: ["high", "Lumières", -0.2, 0.2, 0.0, 0.01]

void ART_main(
    varying float r,
    varying float g,
    varying float b,
    output varying float rout,
    output varying float gout,
    output varying float bout,
    float shadow,
    float mid,
    float high
)
{
    float L = 0.2126 * r + 0.7152 * g + 0.0722 * b;

    // Poids des plages (0‑1)
    float wS = 0.0;
    float wM = 0.0;
    float wH = 0.0;

    if (L <= 0.33) {
        wS = 1.0 - L / 0.33;
        wM = L / 0.33;
    }
    if (L > 0.33 && L <= 0.66) {
        wS = 0.0;
        wM = 1.0 - (L - 0.33) / 0.33;
        wH = (L - 0.33) / 0.33;
    }
    if (L > 0.66) {
        wS = 0.0;
        wM = 1.0 - (L - 0.66) / 0.34;
        if (wM < 0.0) wM = 0.0;
        wH = (L - 0.66) / 0.34;
        if (wH > 1.0) wH = 1.0;
    }

    // --- Effets des curseurs ---
    float Lnew = L;

    // Ombres : simple décalage (positif = éclaircit)
    Lnew = Lnew + shadow * wS;

    // Tons moyens : contraste local autour de 0.5
    float Lm = L;
    if (L < 0.5) {
        Lm = L - mid * (0.5 - L);
    }
    if (L > 0.5) {
        Lm = L + mid * (L - 0.5);
    }
    if (Lm < 0.0) Lm = 0.0;
    if (Lm > 1.0) Lm = 1.0;
    Lnew = Lnew + (Lm - L) * wM;

    // Lumières : simple décalage (positif = éclaircit)
    Lnew = Lnew + high * wH;

    // Clamp final
    if (Lnew < 0.0) Lnew = 0.0;
    if (Lnew > 1.0) Lnew = 1.0;

    // Application aux canaux (préservation teinte/saturation)
    float factor = 1.0;
    if (L > 0.0001) {
        factor = Lnew / L;
    }
    rout = r * factor;
    gout = g * factor;
    bout = b * factor;
}
