struct FloatRecord
{
    float x;
    float y;
    float z;
    float w;
};
extern FloatRecord DAT_011ff578[31];

// @fnv 0x00fb9d70
void FUN_00fb9d70()
{
    FloatRecord* record = DAT_011ff578;
    int remaining = 30;
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
