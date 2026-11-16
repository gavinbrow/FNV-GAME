struct __declspec(align(16)) D36270Data {
    void* vtable;
    void* a;
    void* b;
    void* c;
    void* d;
    void* e;
    void* f;
    void* g;
    void* h;
    void* i;
    void* j;
    void* k;
    unsigned char flag0;
    unsigned char flag1;
    unsigned char flag2;
};
void FUN_00d36270(D36270Data*);
struct D362Script {
    void FUN_00cfbd60(D36270Data*, int row, int column);
};
extern unsigned char DAT_01268ad5;
void FUN_00d362c0(D362Script* script) {
    D36270Data data;
    data.flag0 = 0; data.flag1 = 0; data.flag2 = 0;
    data.f = 0; data.g = 0; data.h = 0; data.i = 0; data.j = 0;
    FUN_00d36270(&data);
    script->FUN_00cfbd60(&data, 8, 8);
    data.flag1 = 1; data.flag2 = 1;
    script->FUN_00cfbd60(&data, 7, 8);
    script->FUN_00cfbd60(&data, 8, 7);
    script->FUN_00cfbd60(&data, 7, 7);
    *(unsigned char*)((char*)script + 0x1e22) = 1;
    DAT_01268ad5 = 1;
}