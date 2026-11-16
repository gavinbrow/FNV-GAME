struct FUN_00dbc670_storage {
void* vtbl;
int unk04;
int unk08;
int unk0C;
int unk10;
int unk14;
int unk18;
int unk1C;
int unk20;
int unk24;
int unk28;
int unk2C;
int unk30;
int unk34;
int unk38;
int unk3C;
int unk40;
int unk44;
int unk48;
int unk4C;
int unk50;
int unk54;
int unk58;
int unk5C;
int unk60;
int unk64;
int unk68;
int unk6C;
int unk70;
int unk74;
int unk78;
int unk7C;
int unk80;
int unk84;
int unk88;
int unk8C;
int unk90;
int unk94;
int unk98;
int unk9C;
int unkA0;
int unkA4;
int unkA8;
int unkAC;
int unkB0;
int unkB4;
int unkB8;
int unkBC;
int unkC0;
int unkC4;
int unkC8;
int unkCC;
int unkD0;
};
struct FUN_00dbc670_shell {
    void FUN_00dbc670();
    void FUN_00dbda50(int, int, int);
    int FUN_00dbd620(int, int);
    void FUN_00dbc6e0();
};
struct GlobalDispatch {
    virtual int V0(); virtual int V1(); virtual int V2();
    virtual int Dispatch(int, int, int, int, int);
};
extern GlobalDispatch* DAT_01269b74;
int __cdecl FUN_00d484a0(int a1, int a2, int a3, int a4, int useLocal, int a6)
{
    if (a3) {
        if (useLocal) {
            FUN_00dbc670_storage message;
            FUN_00dbc670_shell* shell = (FUN_00dbc670_shell*)&message;
            shell->FUN_00dbc670();
            shell->FUN_00dbda50(a1, a2, a6);
            int result = shell->FUN_00dbd620(a3, a4);
            shell->FUN_00dbc6e0();
            return result;
        }
        return DAT_01269b74->Dispatch(a1, a2, a3, a4, a6);
    }
    return 1;
}
