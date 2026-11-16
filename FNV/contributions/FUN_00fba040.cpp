struct FloatFields
{
    float first;
    float second;
    float third;
    float fourth;
};

extern FloatFields DAT_011a9bd0;
extern FloatFields DAT_0120002c;

// @fnv 0x00fba040
void __cdecl FUN_00fba040()
{
    DAT_0120002c = DAT_011a9bd0;
}
