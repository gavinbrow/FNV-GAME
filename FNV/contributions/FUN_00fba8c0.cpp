struct RuntimeRecord
{
    float field0;
    float field4;
    float field8;
    float field12;
};

extern RuntimeRecord DAT_012010f0[164];

// @fnv 0x00fba8c0
void FUN_00fba8c0()
{
    RuntimeRecord* record = DAT_012010f0;
    int remaining = 163;
    do
    {
        record->field0 = 0.0f;
        record->field4 = 0.0f;
        record->field8 = 0.0f;
        record->field12 = 0.0f;
        ++record;
    }
    while (--remaining >= 0);
}
