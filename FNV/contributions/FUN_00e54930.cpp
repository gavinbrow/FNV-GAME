int __cdecl FUN_00e54930(float **array, int count)
{
    if (count <= 0)
        return -1;

    const float *values = *array;
    float minimum = values[0];
    int minimumIndex = 0;
    int index = 1;

    if (count - 1 >= 4) {
        const int limit = count - 3;
        const float *p = values + 3;
        do {
            if (p[-2] < minimum) {
                minimum = p[-2];
                minimumIndex = index;
            }
            if (p[-1] < minimum) {
                minimum = p[-1];
                minimumIndex = index + 1;
            }
            if (p[0] < minimum) {
                minimum = p[0];
                minimumIndex = index + 2;
            }
            if (p[1] < minimum) {
                minimum = p[1];
                minimumIndex = index + 3;
            }
            index += 4;
            p += 4;
        } while (index < limit);
    }

    if (index < count) {
        const float *p = values + index;
        do {
            if (*p < minimum) {
                minimum = *p;
                minimumIndex = index;
            }
            ++index;
            ++p;
        } while (index < count);
    }

    return minimumIndex;
}