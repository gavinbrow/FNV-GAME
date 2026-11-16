struct FUN_00438fc0_file {
    unsigned int FUN_004726b0();
    void FUN_00472890(void*, unsigned int);
    bool FUN_00401680();
};

struct NiPoint3 {
    float x;
    float y;
    float z;
    unsigned char FUN_00438fc0(FUN_00438fc0_file* pFile);
};

void __cdecl FUN_00401080(float*, BSIntToType<4>);

unsigned char NiPoint3::FUN_00438fc0(FUN_00438fc0_file* pFile)
{
    char result = 0;
    if (pFile != 0) {
        if (pFile->FUN_004726b0() == 0x4f424d58) {
            pFile->FUN_00472890(this, 12);
            if (pFile->FUN_00401680()) {
                FUN_00401080(&x, BSIntToType<4>());
                FUN_00401080(&y, BSIntToType<4>());
                FUN_00401080(&z, BSIntToType<4>());
            }
            result = 1;
        }
    }
    return result;
}