struct Matrix
{
    float values[12];
    bool* FUN_00ce50e0(bool* output);
};

bool* Matrix::FUN_00ce50e0(bool* output)
{
    for (int index = 0; index < 12; ++index)
    {
        if (index != 3 && index != 11)
        {
            union FloatBits { float value; unsigned int bits; } item;
            item.value = values[index];
            if ((item.bits & 0x7f800000) == 0x7f800000)
            {
                *output = false;
                return output;
            }
        }
    }
    *output = true;
    return output;
}
