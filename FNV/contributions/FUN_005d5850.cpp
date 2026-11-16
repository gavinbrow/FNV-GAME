struct ToggleSetting_005d5850 {

    bool* FUN_00408d60();

    void FUN_004de2d0(bool value);

    float* FUN_00403e20();

    void FUN_004ed780(float value);

};

extern ToggleSetting_005d5850 DAT_011f15a4;

extern ToggleSetting_005d5850 DAT_011f15b0;

extern ToggleSetting_005d5850 DAT_011f15d0;

extern ToggleSetting_005d5850 DAT_011f15ec;

extern ToggleSetting_005d5850 DAT_011f1674;

extern ToggleSetting_005d5850 DAT_011f1680;

extern ToggleSetting_005d5850 DAT_011f168c;

extern ToggleSetting_005d5850 DAT_011f16c0;

extern ToggleSetting_005d5850 DAT_011f16e0;

extern ToggleSetting_005d5850 DAT_011f1814;

extern ToggleSetting_005d5850 DAT_011f1824;

extern ToggleSetting_005d5850 DAT_011f1858;

extern ToggleSetting_005d5850 DAT_011f1878;

extern ToggleSetting_005d5850 DAT_011f197c;

extern ToggleSetting_005d5850 DAT_011f1b24;

extern ToggleSetting_005d5850 DAT_011f1ba0;

extern ToggleSetting_005d5850 DAT_011f1c30;

extern ToggleSetting_005d5850 DAT_011f1c4c;

extern ToggleSetting_005d5850 DAT_011f1c70;

extern const char DAT_01011584[];

extern const char DAT_01011f58[];

extern const char DAT_010399b8[];

extern const char DAT_010399bc[];

extern const char DAT_0103c6b4[];

extern const char DAT_0103c6c8[];

extern const char DAT_0103c6e8[];

extern const char DAT_0103c6f0[];

extern const char DAT_0103c71c[];

extern const char DAT_0103c724[];

extern const char DAT_0103c750[];

extern const char DAT_0103c758[];

extern const char DAT_0103c78c[];

extern const char DAT_0103c798[];

extern const char DAT_0103c7a0[];

extern const char DAT_0103c7d0[];

extern const char DAT_0103c7d8[];

extern const char DAT_0103c800[];

extern const char DAT_0103c808[];

extern const char DAT_0103c810[];

extern const char DAT_0103c83c[];

extern const char DAT_0103c844[];

extern const char DAT_0103c870[];

extern const char DAT_0103c87c[];

extern const char DAT_0103c884[];

extern const char DAT_0103c8ac[];

extern const char DAT_0103c8b4[];

extern const char DAT_0103c8d8[];

extern const char DAT_0103c8e0[];

extern const char DAT_0103c904[];

extern const char DAT_0103c90c[];

extern const char DAT_0103c930[];

extern const char DAT_0103c938[];

extern const char DAT_0103c95c[];

extern const char DAT_0103c964[];

extern const char DAT_0103c988[];

extern const char DAT_0103c990[];

extern const char DAT_0103c9c4[];

extern const char DAT_0103c9d4[];

extern const char DAT_0103c9dc[];

extern const char DAT_0103ca08[];

extern const char DAT_0103ca18[];

extern const char DAT_0103ca24[];

extern const char DAT_0103ca4c[];

extern const char DAT_0103ca58[];

extern const char DAT_0103ca60[];

extern const char DAT_0103ca90[];

extern const char DAT_0103ca9c[];

extern const char DAT_0103cacc[];

extern const char DAT_0103cad4[];

extern const double DAT_0101ffa0;

extern const double DAT_0103c7c8;

struct TLSData_005d5850 { unsigned char state; };

extern __declspec(thread) TLSData_005d5850 tls_005d5850;

void __cdecl FUN_004046f0(char* dest, const char* src);

unsigned int __cdecl FUN_00ec6130(const char* str);

int __cdecl FUN_00404dc0(const char* a, const char* b);

void __cdecl FUN_00703c00(const char* format, ...);
void __cdecl FUN_00703c00(const char* format, double val);

bool __cdecl FUN_005d5850(const SCRIPT_PARAMETER* apParameters, const char* apCompiledParams, TESObjectREFR* apRefObject, TESObjectREFR* apContainer, Script* apScript, ScriptLocals* apScriptLocals, double& afReturnValue, unsigned int& auiOffset)

{

    char name[512];

    FUN_004046f0(name, DAT_01011584);

    if (!ExtractArgs(apParameters, apCompiledParams, &auiOffset, apRefObject, apContainer, apScript, apScriptLocals, name))

        return false;

    if (FUN_00ec6130(name) == 0) {

        bool anyOn = *DAT_011f1680.FUN_00408d60() ||

            *DAT_011f1ba0.FUN_00408d60() ||

            *DAT_011f1878.FUN_00408d60() ||

            *DAT_011f1858.FUN_00408d60() ||

            *DAT_011f1b24.FUN_00408d60() ||

            *DAT_011f1674.FUN_00408d60() ||

            *DAT_011f1814.FUN_00408d60() ||

            *DAT_011f168c.FUN_00408d60() ||

            *DAT_011f16e0.FUN_00408d60() ||

            *DAT_011f16c0.FUN_00408d60() ||

            *DAT_011f15a4.FUN_00408d60() ||

            *DAT_011f15b0.FUN_00408d60() ||

            *DAT_011f1824.FUN_00408d60() ||

            *DAT_011f15d0.FUN_00408d60() ||

            *DAT_011f197c.FUN_00408d60() ||

            *DAT_011f1c4c.FUN_00408d60() ||

            *DAT_011f15ec.FUN_00408d60();

        DAT_011f1680.FUN_004de2d0(!anyOn);

        DAT_011f1ba0.FUN_004de2d0(!anyOn);

        DAT_011f1878.FUN_004de2d0(!anyOn);

        DAT_011f1858.FUN_004de2d0(!anyOn);

        DAT_011f1b24.FUN_004de2d0(!anyOn);

        DAT_011f1674.FUN_004de2d0(!anyOn);

        DAT_011f168c.FUN_004de2d0(!anyOn);

        DAT_011f1814.FUN_004de2d0(!anyOn);

        DAT_011f16e0.FUN_004de2d0(!anyOn);

        DAT_011f16c0.FUN_004de2d0(!anyOn);

        DAT_011f15a4.FUN_004de2d0(!anyOn);

        DAT_011f15b0.FUN_004de2d0(!anyOn);

        DAT_011f1824.FUN_004de2d0(!anyOn);

        DAT_011f15d0.FUN_004de2d0(!anyOn);

        DAT_011f197c.FUN_004de2d0(!anyOn);

        DAT_011f1c4c.FUN_004de2d0(!anyOn);

        DAT_011f15ec.FUN_004de2d0(!anyOn);

        if (reinterpret_cast<const unsigned char*>(&tls_005d5850)[0x268])

            FUN_00703c00(DAT_0103cad4, anyOn ? DAT_010399b8 : DAT_010399bc);

    } else if (!FUN_00404dc0(name, DAT_0103cacc)) {

        DAT_011f1680.FUN_004de2d0(!*DAT_011f1680.FUN_00408d60());

        if (reinterpret_cast<const unsigned char*>(&tls_005d5850)[0x268])

            FUN_00703c00(DAT_0103ca9c, *DAT_011f1680.FUN_00408d60() ? DAT_010399bc : DAT_010399b8);

    } else if (!FUN_00404dc0(name, DAT_0103ca90)) {

        DAT_011f16c0.FUN_004de2d0(!*DAT_011f16c0.FUN_00408d60());

        if (reinterpret_cast<const unsigned char*>(&tls_005d5850)[0x268])

            FUN_00703c00(DAT_0103ca60, *DAT_011f16c0.FUN_00408d60() ? DAT_010399bc : DAT_010399b8);

    } else if (!FUN_00404dc0(name, DAT_0103ca58) || !FUN_00404dc0(name, DAT_0103ca4c)) {

        DAT_011f1674.FUN_004de2d0(!*DAT_011f1674.FUN_00408d60());

        if (reinterpret_cast<const unsigned char*>(&tls_005d5850)[0x268])

            FUN_00703c00(DAT_0103ca24, *DAT_011f1674.FUN_00408d60() ? DAT_010399bc : DAT_010399b8);

    } else if (!FUN_00404dc0(name, DAT_0103ca18) || !FUN_00404dc0(name, DAT_0103ca08)) {

        DAT_011f16e0.FUN_004de2d0(!*DAT_011f16e0.FUN_00408d60());

        if (reinterpret_cast<const unsigned char*>(&tls_005d5850)[0x268])

            FUN_00703c00(DAT_0103c9dc, *DAT_011f16e0.FUN_00408d60() ? DAT_010399bc : DAT_010399b8);

    } else if (!FUN_00404dc0(name, DAT_0103c9d4) || !FUN_00404dc0(name, DAT_0103c9c4)) {

        DAT_011f168c.FUN_004de2d0(!*DAT_011f168c.FUN_00408d60());

        if (reinterpret_cast<const unsigned char*>(&tls_005d5850)[0x268])

            FUN_00703c00(DAT_0103c990, *DAT_011f168c.FUN_00408d60() ? DAT_010399bc : DAT_010399b8);

    } else if (!FUN_00404dc0(name, DAT_0103c988)) {

        DAT_011f1ba0.FUN_004de2d0(!*DAT_011f1ba0.FUN_00408d60());

        if (reinterpret_cast<const unsigned char*>(&tls_005d5850)[0x268])

            FUN_00703c00(DAT_0103c964, *DAT_011f1ba0.FUN_00408d60() ? DAT_010399bc : DAT_010399b8);

    } else if (!FUN_00404dc0(name, DAT_0103c95c)) {

        DAT_011f1878.FUN_004de2d0(!*DAT_011f1878.FUN_00408d60());

        if (reinterpret_cast<const unsigned char*>(&tls_005d5850)[0x268])

            FUN_00703c00(DAT_0103c938, *DAT_011f1878.FUN_00408d60() ? DAT_010399bc : DAT_010399b8);

    } else if (!FUN_00404dc0(name, DAT_0103c930)) {

        DAT_011f1858.FUN_004de2d0(!*DAT_011f1858.FUN_00408d60());

        if (reinterpret_cast<const unsigned char*>(&tls_005d5850)[0x268])

            FUN_00703c00(DAT_0103c90c, *DAT_011f1858.FUN_00408d60() ? DAT_010399bc : DAT_010399b8);

    } else if (!FUN_00404dc0(name, DAT_0103c904)) {

        DAT_011f1b24.FUN_004de2d0(!*DAT_011f1b24.FUN_00408d60());

        if (reinterpret_cast<const unsigned char*>(&tls_005d5850)[0x268])

            FUN_00703c00(DAT_0103c8e0, *DAT_011f1b24.FUN_00408d60() ? DAT_010399bc : DAT_010399b8);

    } else if (!FUN_00404dc0(name, DAT_0103c8d8)) {

        DAT_011f1814.FUN_004de2d0(!*DAT_011f1814.FUN_00408d60());

        if (reinterpret_cast<const unsigned char*>(&tls_005d5850)[0x268])

            FUN_00703c00(DAT_0103c8b4, *DAT_011f1814.FUN_00408d60() ? DAT_010399bc : DAT_010399b8);

    } else if (!FUN_00404dc0(name, DAT_0103c8ac)) {

        DAT_011f15b0.FUN_004de2d0(!*DAT_011f15b0.FUN_00408d60());

        if (reinterpret_cast<const unsigned char*>(&tls_005d5850)[0x268])

            FUN_00703c00(DAT_0103c884, *DAT_011f15b0.FUN_00408d60() ? DAT_010399bc : DAT_010399b8);

    } else if (!FUN_00404dc0(name, DAT_0103c87c) || !FUN_00404dc0(name, DAT_0103c870)) {

        DAT_011f1824.FUN_004de2d0(!*DAT_011f1824.FUN_00408d60());

        if (reinterpret_cast<const unsigned char*>(&tls_005d5850)[0x268])

            FUN_00703c00(DAT_0103c844, *DAT_011f1824.FUN_00408d60() ? DAT_010399bc : DAT_010399b8);

    } else if (!FUN_00404dc0(name, DAT_0103c83c)) {

        DAT_011f15a4.FUN_004de2d0(!*DAT_011f15a4.FUN_00408d60());

        if (reinterpret_cast<const unsigned char*>(&tls_005d5850)[0x268])

            FUN_00703c00(DAT_0103c810, *DAT_011f15a4.FUN_00408d60() ? DAT_010399bc : DAT_010399b8);

    } else if (!FUN_00404dc0(name, DAT_0103c808)) {

        DAT_011f1c30.FUN_004de2d0(!*DAT_011f1c30.FUN_00408d60());

        if (reinterpret_cast<const unsigned char*>(&tls_005d5850)[0x268])

            FUN_00703c00(DAT_0103c7d8, *DAT_011f1c30.FUN_00408d60() ? DAT_0103c800 : DAT_01011f58);

    } else if (!FUN_00404dc0(name, DAT_0103c7d0)) {

        DAT_011f1c70.FUN_004ed780((float)(*DAT_011f1c70.FUN_00403e20() - DAT_0101ffa0));

        if (*DAT_011f1c70.FUN_00403e20() <= DAT_0103c7c8)

            DAT_011f1c70.FUN_004ed780(1.0f);

        if (reinterpret_cast<const unsigned char*>(&tls_005d5850)[0x268])

            FUN_00703c00(DAT_0103c7a0, *DAT_011f1c70.FUN_00403e20());

    } else if (!FUN_00404dc0(name, DAT_0103c798) || !FUN_00404dc0(name, DAT_0103c78c)) {

        DAT_011f15d0.FUN_004de2d0(!*DAT_011f15d0.FUN_00408d60());

        if (reinterpret_cast<const unsigned char*>(&tls_005d5850)[0x268])

            FUN_00703c00(DAT_0103c758, *DAT_011f15d0.FUN_00408d60() ? DAT_010399bc : DAT_010399b8);

    } else if (!FUN_00404dc0(name, DAT_0103c750)) {

        DAT_011f197c.FUN_004de2d0(!*DAT_011f197c.FUN_00408d60());

        if (reinterpret_cast<const unsigned char*>(&tls_005d5850)[0x268])

            FUN_00703c00(DAT_0103c724, *DAT_011f197c.FUN_00408d60() ? DAT_010399bc : DAT_010399b8);

    } else if (!FUN_00404dc0(name, DAT_0103c71c)) {

        DAT_011f1c4c.FUN_004de2d0(!*DAT_011f1c4c.FUN_00408d60());

        if (reinterpret_cast<const unsigned char*>(&tls_005d5850)[0x268])

            FUN_00703c00(DAT_0103c6f0, *DAT_011f1c4c.FUN_00408d60() ? DAT_010399bc : DAT_010399b8);

    } else if (!FUN_00404dc0(name, DAT_0103c6e8)) {

        DAT_011f15ec.FUN_004de2d0(!*DAT_011f15ec.FUN_00408d60());

        if (reinterpret_cast<const unsigned char*>(&tls_005d5850)[0x268])

            FUN_00703c00(DAT_0103c6c8, *DAT_011f15ec.FUN_00408d60() ? DAT_010399bc : DAT_010399b8);

    } else if (reinterpret_cast<const unsigned char*>(&tls_005d5850)[0x268]) {

        FUN_00703c00(DAT_0103c6b4, name);

    }

    return true;

}

