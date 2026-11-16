extern "C" void __cdecl __debugbreak();
extern const char DAT_010d3574[];
extern const char DAT_0103d078[];
extern const char DAT_010d3540[];
struct Service {
    struct VTable {
        void* f0;
        void* f4;
        void* f8;
        int (__thiscall *fC)(Service*,int,int,char*,const char*,int);
    };
    VTable *vt;
};
extern Service* DAT_01268360;
struct Buffer {
    int m00;
    int m04;
    int m08;
    void FUN_00cb1600(char* storage, int cap);
    Buffer* FUN_00cc01c0(const char* x, int n, const char* y);
    Buffer* FUN_00cc01c0();
    Buffer* FUN_00cc02d0();
    void FUN_00cc00e0();
};
struct FUN_00d74f10_class {
    int unk00;
    int unk04;
    char* item08;
    int FUN_00d74f10();
};
int FUN_00d74f10_class::FUN_00d74f10() {
    char* node = item08;
    void* storage[128];
    Buffer b;
    if (!node[0x1b5]) {
        b.FUN_00cb1600((char*)storage, 512);
        b.FUN_00cc01c0(DAT_010d3574, *(int*)(node+0x1b0),DAT_0103d078)->FUN_00cc02d0()->FUN_00cc01c0();
        int ret = DAT_01268360->vt->fC(DAT_01268360,3,0x79f9d886,(char*)storage,DAT_010d3540,0x148);
        if (ret != 0) __debugbreak();
        b.FUN_00cc00e0();
    }
    return *(int*)(item08 + 0x58);
}
