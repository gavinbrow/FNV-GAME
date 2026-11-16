
struct FNV_869F30_Renderer : NiRenderer {
    void __thiscall FUN_00483710();
};

struct FNV_869F30_Manager {
    void __thiscall FUN_00c3e310();
    void __thiscall FUN_00877d30();
    void __thiscall FUN_00c3e340();
};
extern FNV_869F30_Manager* DAT_01202d98;

struct FNV_869F30_World {
    void __thiscall FUN_00449030();
};
extern FNV_869F30_World* DAT_011c3b3c;

struct FNV_869F30_Service {
    virtual void method0();
    virtual void method1();
    virtual void method2();
    void __thiscall FUN_00b01130();
};
FNV_869F30_Service* __cdecl FUN_00aff100();
FNV_869F30_Service* __cdecl FUN_00453a70();
FNV_869F30_Service* __cdecl FUN_00b00a00();
void __cdecl FUN_008304a0();
void __cdecl FUN_0082f9c0();
void __cdecl FUN_0078d050();
void __cdecl FUN_0070ad30();

void __cdecl FUN_00869f30(int mode)
{
    switch (mode) {
    default:
        break;
    case 0:
        break;
    case 1:
        break;
    case 2:
        if (FUN_0043c4b0()) {
            static_cast<FNV_869F30_Renderer*>(FUN_0043c4b0())->FUN_00483710();
        }
        FUN_00867090();
        if (DAT_01202d98) {
            DAT_01202d98->FUN_00c3e310();
        }
        DAT_011c3b3c->FUN_00449030();
        DAT_01202d98->FUN_00877d30();
        DAT_01202d98->FUN_00c3e340();
        FUN_00aff100()->FUN_00b01130();
        FUN_00aff100()->method2();
        FUN_008304a0();
        FUN_0082f9c0();
        FUN_00453a70()->method2();
        FUN_0078d050();
        FUN_0070ad30();
        FUN_00b00a00()->method2();
        if (DAT_01202d98) {
            DAT_01202d98->FUN_00c3e310();
        }
        break;
    }
}
