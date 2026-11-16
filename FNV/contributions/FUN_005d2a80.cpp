struct SCRIPT_PARAMETER;
struct TESObjectREFR;
struct Script;
struct ScriptLocals;

struct WaterObj {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    int unk40;
    int unk44;
    int unk48;
    int unk4c;
    int unk50;
    int unk54;
    int unk58;
    int unk5c;
    unsigned char unk60, unk61, unk62;
    unsigned char f63;
    int unk64;
    int unk68;
    int unk6c;
    int unk70;
    int unk74;
    int unk78;
    unsigned char unk7c, unk7d, unk7e;
    unsigned char f7f;
    unsigned char f80;
    unsigned char f81;
    unsigned char unk82, unk83;
    int unk84;
    int unk88;
    int unk8c;
    int unk90;
    int unk94;
    int unk98;
    int unk9c;
    int unka0;
    int unka4;
    int unka8;
    int unkac;
    int unkb0;
    int unkb4;
    int unkb8;
    float fbc;
    float fc0;
    float fc4;
    int unkc8;
    int unkcc;
    int unkd0;
    int unkd4;
    int unkd8;
    int unkdc;
    int unke0;
    int unke4;
    int unke8;
    int unkec;
    int unkf0;
    int unkf4;
    int unkf8;
    int unkfc;
    int unk100;
    int unk104;
    int unk108;
    int unk10c;
    int unk110;
    int unk114;
    float f118;
    float f11c;
    float f120;
};

struct ObjB {
    WaterObj* FUN_00a59d30(int);
};
struct ObjA {
    ObjB* FUN_004e8030();
    void FUN_004e6370(int, int, int);
    void FUN_004e65d0();
};
struct HostMid {
    const char* FUN_00451cb0();
};
struct Host5d {
    ObjA* FUN_0070ec90();
    ObjA* FUN_0070ec90(void*);
    HostMid* FUN_00457070();
};


union PerfCount { long long quad; struct { unsigned int low; unsigned int high; }; };
struct SettingObj {
    unsigned char* FUN_00408d60();
    void FUN_004de2d0(int);
};
extern SettingObj DAT_011c7b6c;
extern SettingObj DAT_011c7c60;
extern SettingObj DAT_011c7bbc;

extern float DAT_011ff3ec;
extern float DAT_011ff3f4;
extern float DAT_011ff10c;
extern float DAT_011ff3f0;
extern float DAT_011ffe48;
extern float DAT_011ff414;
extern float DAT_011ffff0;
extern float DAT_01200014;
extern float DAT_01200018;
extern float DAT_0120001c;
extern float DAT_01200004;
extern float DAT_01200008;
extern float DAT_0120000c;
extern float DAT_01200010;
extern unsigned char DAT_011c7a65;

bool __cdecl FUN_005accb0(const SCRIPT_PARAMETER*, const char*, unsigned int*, TESObjectREFR*, TESObjectREFR*, Script*, ScriptLocals*, char*, float*);
int __cdecl FUN_00404dc0(const char*, const char*);
void __cdecl FUN_00703c00(const char*, ...);
void __cdecl FUN_0049c860(void*);
bool __cdecl FUN_005d2a40();
void __cdecl FUN_00406d00(char*, unsigned int, const char*, ...);
void __cdecl FUN_0040fbe0(const char*, int);
extern "C" __declspec(dllimport) int __stdcall QueryPerformanceCounter(long long*);
extern "C" __declspec(dllimport) int __stdcall QueryPerformanceFrequency(long long*);

bool __cdecl FUN_005d2a80(const SCRIPT_PARAMETER* parameters, const char* scriptData, TESObjectREFR* thisObject, TESObjectREFR* container, Script* script, ScriptLocals* locals, double& result, unsigned int& opcodeOffset)
{
    extern void __cdecl FUN_00703c00(const char*, ...);
    WaterObj* p;
    float value = 0.0f;
    char buf[512];
    if (!FUN_005accb0(parameters, scriptData, &opcodeOffset, thisObject, container, script, locals, buf, &value)) {
        FUN_00703c00("reflectamt, fresnel, opacity, speed, noise, reflect, refract, lod");
        return false;
    }
    p = 0;
    if (thisObject) {
        ObjB* water = ((Host5d*)DAT_011dea10)->FUN_0070ec90(thisObject)->FUN_004e8030();
        WaterObj* waterNode = water->FUN_00a59d30(3);
        p = waterNode;
    }
    if (!FUN_00404dc0(buf, "velocity")) {
    } else if (!FUN_00404dc0(buf, "direction")) {
        if (value >= 0.0f && value <= 360.0f) { }
    } else if (!FUN_00404dc0(buf, "amplitude")) {
    } else if (!FUN_00404dc0(buf, "frequency")) {
    } else if (!FUN_00404dc0(buf, "reflectamt")) {
        if (value >= 0.0f && value <= 1.0f) {
            if (p) {
                p->fbc = value;
                FUN_00703c00("set water reflectivity amount to %f", (double)value);
                p->f7f = 0;
            } else {
                DAT_011ff3ec = value;
                FUN_00703c00("set water reflectivity amount to %f", (double)value);
                DAT_011c7a65 = 1;
            }
        } else {
            FUN_00703c00("usage : mws reflectamt (0.0 - 1.0)", (double)value);
        }
    } else if (!FUN_00404dc0(buf, "distort")) {
        if (p) {
            p->fc4 = value;
            FUN_00703c00("set water distortion amount to %f", (double)value);
            p->f7f = 0;
        } else {
            DAT_011ff3f4 = value;
            FUN_00703c00("set water distortion amount to %f", (double)value);
            DAT_011c7a65 = 1;
        }
    } else if (!FUN_00404dc0(buf, "fresnel")) {
        if (value >= 0.0f && value <= 1.0f) {
            if (p) {
                p->f118 = value;
                FUN_00703c00("set fresnel term to %f", (double)value);
                p->f7f = 0;
            } else {
                DAT_011ff10c = value;
                FUN_00703c00("set fresnel term to %f", (double)value);
                DAT_011c7a65 = 1;
            }
        } else {
            FUN_00703c00("usage : mws fresnel (0.0 - 1.0)", (double)value);
        }
    } else if (!FUN_00404dc0(buf, "opacity")) {
        if (value >= 0.0f && value <= 100.0f) {
            if (p) {
                p->fc0 = value / 100.0f;
                FUN_00703c00("set water opacity to %d", (int)value);
                p->f7f = 0;
            } else {
                DAT_011ff3f0 = value / 100.0f;
                FUN_00703c00("set water opacity to %d", (int)value);
                DAT_011c7a65 = 1;
            }
        } else {
            FUN_00703c00("usage : mws opacity (0.0 - 100.0)", (double)value);
        }
    } else if (!FUN_00404dc0(buf, "blend")) {
    } else if (!FUN_00404dc0(buf, "noise")) {
        if (value >= 0.0f && value <= 100.0f) {
            if (p) {
                p->f11c = value;
                FUN_00703c00("set noise scale to %f", (double)value);
                p->f7f = 0;
            } else {
                DAT_011ffe48 = value;
                FUN_00703c00("set noise to %f", (double)value);
                DAT_011c7a65 = 1;
            }
        } else {
            FUN_00703c00("usage : mws noise (0.0 - 100.0)", (double)value);
        }
    } else if (!FUN_00404dc0(buf, "off")) {
        if (p) {
            p->f7f = 1;
        } else {
            DAT_011c7a65 = 0;
        }
    } else if (!FUN_00404dc0(buf, "displaceforce")) {
        if (value >= 0.0f && value <= 1.0f) {
            DAT_01200014 = value;
            DAT_011c7a65 = 1;
        }
    } else if (!FUN_00404dc0(buf, "displacevelocity")) {
        if (value >= 0.0f && value <= 1.0f) {
            DAT_01200018 = value;
            DAT_011c7a65 = 1;
        }
    } else if (!FUN_00404dc0(buf, "displacefalloff")) {
        if (value >= 0.0f && value <= 1.0f) {
            DAT_0120001c = value;
            DAT_011c7a65 = 1;
        }
    } else if (!FUN_00404dc0(buf, "displacedampener")) {
        if (value >= 0.0f && value <= 20.0f) {
            DAT_011ffff0 = value;
            DAT_011c7a65 = 1;
        }
    } else if (!FUN_00404dc0(buf, "rainforce")) {
        if (value >= 0.0f && value <= 1.0f) {
            DAT_01200004 = value;
            DAT_011c7a65 = 1;
        }
    } else if (!FUN_00404dc0(buf, "rainvelocity")) {
        if (value >= 0.0f && value <= 1.0f) {
            DAT_01200008 = value;
            DAT_011c7a65 = 1;
        }
    } else if (!FUN_00404dc0(buf, "rainfalloff")) {
        if (value >= 0.0f && value <= 1.0f) {
            DAT_0120000c = value;
            DAT_011c7a65 = 1;
        }
    } else if (!FUN_00404dc0(buf, "rainsize")) {
        if (value >= 0.0f && value <= 1.0f) {
            DAT_01200010 = value;
            DAT_011c7a65 = 1;
        }
    } else if (!FUN_00404dc0(buf, "reflect")) {
        if (p) {
            if (p->f80) {
                p->f80 = 0;
                FUN_00703c00("Toggle Reflections : OFF");
            } else {
                p->f80 = 1;
                FUN_00703c00("Toggle Reflections : ON");
            }
        } else {
            if (*DAT_011c7b6c.FUN_00408d60()) {
                DAT_011c7b6c.FUN_004de2d0(0);
                FUN_00703c00("Toggle Global Water Reflections : OFF");
            } else {
                DAT_011c7b6c.FUN_004de2d0(1);
                FUN_00703c00("Toggle Global Water Reflections : ON");
            }
        }
    } else if (!FUN_00404dc0(buf, "refract")) {
        if (p) {
            if (p->f81) {
                p->f81 = 0;
                FUN_00703c00("Toggle Refractions : OFF");
            } else {
                p->f80 = 1;
                FUN_00703c00("Toggle Refractions : ON");
            }
        } else {
            if (*DAT_011c7c60.FUN_00408d60()) {
                DAT_011c7c60.FUN_004de2d0(0);
                FUN_00703c00("Toggle Global Water Refractions : OFF");
            } else {
                DAT_011c7c60.FUN_004de2d0(1);
                FUN_00703c00("Toggle Global Water Refractions : ON");
            }
        }
    } else if (!FUN_00404dc0(buf, "depth")) {
        if (p) {
            if (p->f63) {
                p->f63 = 0;
                FUN_00703c00("Toggle Depth : OFF");
            } else {
                p->f63 = 1;
                FUN_00703c00("Toggle Depth : ON");
            }
        } else {
            if (*DAT_011c7bbc.FUN_00408d60()) {
                DAT_011c7bbc.FUN_004de2d0(0);
                FUN_00703c00("Toggle Global Water Depth : OFF");
            } else {
                DAT_011c7bbc.FUN_004de2d0(1);
                FUN_00703c00("Toggle Global Water Depth : ON");
            }
        }
    } else if (!FUN_00404dc0(buf, "fog")) {
        if (value >= 0.0f && value <= 100.0f) {
            if (p) {
                p->f120 = value / 100.0f;
                FUN_00703c00("set fog amount to %d", (int)value);
                p->f7f = 0;
            } else {
                DAT_011ff414 = value / 100.0f;
                FUN_00703c00("set fog amount to %d", (int)value);
                DAT_011c7a65 = 1;
            }
        }
    } else if (!FUN_00404dc0(buf, "lod")) {
        if (((Host5d*)DAT_011dea10)->FUN_0070ec90()) {
            ((Host5d*)DAT_011dea10)->FUN_0070ec90()->FUN_004e6370(1, 1, 1);
        }
        FUN_00703c00("Toggle LOD Water");
    } else if (!FUN_00404dc0(buf, "autowater")) {
        double secondsPerTick = 1000.0;
        long long freq;
        reinterpret_cast<unsigned int&>(freq) = 0;
        char msg[256];
        long long end;
        long long start;
        long long dt;
        QueryPerformanceFrequency(&start);
        secondsPerTick = (double)start * 0.000001;
        QueryPerformanceCounter(&freq);
        FUN_0049c860(((Host5d*)DAT_011dea10)->FUN_00457070());
        QueryPerformanceCounter(&end);
        dt = end - freq;
        FUN_00406d00(msg, 0xff, "GeneratePlaceableWaterForCell() for cell %s: Ticks: %I64d, Microseconds: %f",
                     ((Host5d*)DAT_011dea10)->FUN_00457070()->FUN_00451cb0(), dt, (double)dt / secondsPerTick);
        FUN_0040fbe0(msg, 0);
        if (!FUN_005d2a40()) {
            ((Host5d*)DAT_011dea10)->FUN_0070ec90()->FUN_004e65d0();
        }
    }
    return true;
}
