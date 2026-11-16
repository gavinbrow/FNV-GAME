struct FourComponentValue
{
    float first;
    float second;
    float third;
    float fourth;
};

extern FourComponentValue DAT_011ff4c8[11];

// @fnv 0x00fb9d40
void FUN_00fb9d40()
{
    FourComponentValue* record = DAT_011ff4c8;

    for (int remaining = 10; remaining >= 0; --remaining)
    {
        record->first = 0.0f;
        record->second = 0.0f;
        record->third = 0.0f;
        record->fourth = 0.0f;
        ++record;
    }
}
