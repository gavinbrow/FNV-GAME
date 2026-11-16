struct Sequence
{
    int unk00; int unk04; int unk08; int unk0c;
    short* values;
    int count;
};
bool* __cdecl FUN_00cdd5b0(bool* result, FUN_00cdd3f0_s* limits, Sequence* sequence)
{
    int i = 0;
    for (; i < sequence->count; ++i)
    {
        short value = sequence->values[i];
        if (value < 0 || value >= limits->field_0x1c)
        {
            *result = false;
            return result;
        }
    }
    *result = true;
    return result;
}
