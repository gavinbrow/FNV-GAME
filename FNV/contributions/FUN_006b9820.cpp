bool __cdecl FUN_006b9820(const float *a, const float *b, const float *c, const float *position, float *weights)
{
    float inverse;
    float determinant = (b[0] - a[0]) * (c[1] - a[1])
                      - (c[0] - a[0]) * (b[1] - a[1]);
    if (determinant == 0.0)
        return false;

    inverse = 1.0f / determinant;
    weights[0] = ((b[0] - position[0]) * (c[1] - position[1])
                 - (c[0] - position[0]) * (b[1] - position[1])) * inverse;
    weights[1] = ((c[0] - position[0]) * (a[1] - position[1])
                 - (a[0] - position[0]) * (c[1] - position[1])) * inverse;
    weights[2] = ((a[0] - position[0]) * (b[1] - position[1])
                 - (b[0] - position[0]) * (a[1] - position[1])) * inverse;
    return true;
}