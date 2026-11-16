float __cdecl FUN_00688f10(float base, int exponent)
{
    unsigned int power;
    if (exponent >= 0)
        power = exponent;
    else
        power = -exponent;

    float result = 1.0f;
    for (;; base = base * base)
    {
        if (power & 1)
            result = result * base;
        power >>= 1;
        if (power == 0)
            return exponent < 0 ? 1.0 / result : result;
    }
}