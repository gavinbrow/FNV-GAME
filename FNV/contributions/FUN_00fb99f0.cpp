struct FloatRecord
{
    float x;
    float y;
    float z;
    float w;
};

extern FloatRecord DAT_011fa0c0[37];

// @fnv 0x00fb99f0
void FUN_00fb99f0()
{
    FloatRecord* record = DAT_011fa0c0;
    int remaining = static_cast<int>(sizeof(DAT_011fa0c0) / sizeof(DAT_011fa0c0[0])) - 1;
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
