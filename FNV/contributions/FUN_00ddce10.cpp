extern double DAT_010cd5a8;
extern double DAT_0101ff40;
int FUN_00ddce10(float angle)
{
    int index = 0;
    float candidate;
    while (index < 31) {
        candidate = (float)((double)index * DAT_010cd5a8 - DAT_0101ff40);
        if (candidate >= angle) {
            if (angle > 0.0f && candidate != angle)
                --index;
            return index;
        }
        ++index;
    }
    return index;
}
