// @ART-label: "Peau Douce"
// Powered By Carafife And DeepSeek V4

// @ART-param: ["satAdj", "Saturation (+/-)", -0.1, 0.1, 0.0, 0.01]
// @ART-param: ["lumAdj", "Luminosité (+/-)", -0.1, 0.1, 0.0, 0.01]
// @ART-param: ["strength", "Force", 0.0, 1.0, 0.5, 0.1]

void ART_main(
    varying float r,
    varying float g,
    varying float b,
    output varying float rout,
    output varying float gout,
    output varying float bout,
    float satAdj,
    float lumAdj,
    float strength
)
{
    // Conversion simple RGB -> HSL
    float maxc = max(max(r, g), b);
    float minc = min(min(r, g), b);
    float l = (maxc + minc) / 2.0;
    
    float delta = maxc - minc;
    float s = 0.0;
    if (delta > 0.0) {
        s = delta / (1.0 - fabs(2.0 * l - 1.0));
    }
    
    // Appliquer les ajustements
    float newS = s + (satAdj * strength);
    if (newS < 0.0) newS = 0.0;
    if (newS > 1.0) newS = 1.0;
    
    float newL = l + (lumAdj * strength);
    if (newL < 0.0) newL = 0.0;
    if (newL > 1.0) newL = 1.0;
    
    // Blend avec original
    rout = r + (newL - l) * strength;
    gout = g + (newL - l) * strength;
    bout = b + (newL - l) * strength;
}
