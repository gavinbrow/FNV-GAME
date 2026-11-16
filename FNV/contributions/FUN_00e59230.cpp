
void __cdecl FUN_00e59230(float* samples, unsigned int count)
{
    float* current = &samples[count - 1];
    unsigned int processed = 1;
    if (static_cast<int>(count - 1) >= 4) {
        unsigned int groups = ((count - 5) >> 2) + 1;
        processed = groups * 4 + 1;
        do {
            current[0] -= current[-1];
            current[-1] -= current[-2];
            current[-2] -= current[-3];
            current[-3] -= current[-4];
            current -= 4;
        } while (--groups != 0);
    }
    if (processed < count) {
        unsigned int remaining = count - processed;
        do {
            current[0] -= current[-1];
            --current;
        } while (--remaining != 0);
    }
}