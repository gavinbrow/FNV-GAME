struct RuntimeRecord
{
    float field0;
    float field4;
    float field8;
    float field12;
};

extern RuntimeRecord DAT_01201b30[63];

// @fnv 0x00fba8f0
void FUN_00fba8f0()
{
    RuntimeRecord* record = DAT_01201b30;
    int remaining = 62;
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
