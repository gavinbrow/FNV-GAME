class NiRTTI
{
public:
    void FUN_00a7b610(const char* name, const NiRTTI* baseType);
};

extern NiRTTI DAT_012043f0;
extern const NiRTTI DAT_011f4a80;
extern const char DAT_010c3a1c[];

// @fnv 0x00fbc9c0
void FUN_00fbc9c0()
{
    DAT_012043f0.FUN_00a7b610(DAT_010c3a1c, &DAT_011f4a80);
}
