struct FloatRecord
{
    float x;
    float y;
    float z;
    float w;
};
extern FloatRecord DAT_01202048[16];

// @fnv 0x00fbab80
void FUN_00fbab80()
{
    FloatRecord* record = DAT_01202048;
    int remaining = 15;
    do
    {
        record->x = 0.0f;
        record->y = 0.0f;
        record->z = 0.0f;
        record->w = 0.0f;
        ++record;
    }
    while (--remaining >= 0);
}
