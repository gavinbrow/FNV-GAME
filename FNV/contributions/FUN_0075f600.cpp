struct CallbackTarget {
    virtual void unk_vf_00();
    virtual void unk_vf_01();
    virtual void unk_vf_02();
    virtual void unk_vf_03();
    virtual void unk_vf_04();
    virtual void unk_vf_05();
    virtual void unk_vf_06();
    virtual void unk_vf_07();
    virtual void unk_vf_08();
    virtual void unk_vf_09();
    virtual void unk_vf_10();
    virtual void unk_vf_11();
    virtual void unk_vf_12();
    virtual void unk_vf_13();
    virtual void unk_vf_14();
    virtual void unk_vf_15();
    virtual void unk_vf_16();
    virtual void unk_vf_17();
    virtual void unk_vf_18();
    virtual void unk_vf_19();
    virtual void unk_vf_20();
    virtual void unk_vf_21();
    virtual void unk_vf_22();
    virtual void unk_vf_23();
    virtual void unk_vf_24();
    virtual void unk_vf_25();
    virtual void unk_vf_26();
    virtual void unk_vf_27();
    virtual void unk_vf_28();
    virtual void unk_vf_29();
    virtual void unk_vf_30();
    virtual void unk_vf_31();
    virtual void unk_vf_32();
    virtual void unk_vf_33();
    virtual void unk_vf_34();
    virtual void unk_vf_35();
    virtual void unk_vf_36();
    virtual void unk_vf_37();
    virtual void unk_vf_38();
    virtual void unk_vf_39();
    virtual void unk_vf_40();
    virtual void unk_vf_41();
    virtual void unk_vf_42();
    virtual void unk_vf_43();
    virtual void unk_vf_44();
    virtual void unk_vf_45();
    virtual void unk_vf_46();
    virtual void unk_vf_47();
    virtual void unk_vf_48();
    virtual void unk_vf_49();
    virtual void unk_vf_50();
    virtual void unk_vf_51();
    virtual void unk_vf_52();
    virtual void unk_vf_53();
    virtual void unk_vf_54();
    virtual void unk_vf_55();
    virtual void unk_vf_56();
    virtual void unk_vf_57();
    virtual void HandleValue(void*);
};
struct ValueSource {
    CallbackTarget* FUN_009611e0();
};
struct InputState {
    bool FUN_0052aa80(int);
    ValueSource* FUN_00559450();
    void FUN_0066b0d0(int);
};
struct Screen {
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
    InputState input;
    void FUN_00a1d910();
};
struct Menu {
    Screen* FUN_00a03c90();
    void FUN_00700320(int, int);
};
struct GlobalView {
    void FUN_004a0370();
    void FUN_004a03c0();
};
extern SM7d6* DAT_011daac0;
Menu* __cdecl FUN_00a09030(int);
GlobalView* __cdecl FUN_004bc3f0();

void __cdecl FUN_0075f600()
{
    Menu* menu = FUN_00a09030(0x417);
    if (menu == 0) return;
    {
        Screen* screen = menu->FUN_00a03c90();
        if (screen != 0) {
            FUN_004bc3f0()->FUN_004a0370();
            if (screen->input.FUN_0052aa80(0)) {
                if (screen->input.FUN_00559450()->FUN_009611e0() != 0) {
                    CallbackTarget* target = screen->input.FUN_00559450()->FUN_009611e0();
                    target->HandleValue(screen->input.FUN_00559450());
                }
            }
            screen->input.FUN_0066b0d0(0);
            menu->FUN_00700320(0x1772, 1);
            screen->FUN_00a1d910();
            FUN_004bc3f0()->FUN_004a03c0();
        }
        DAT_011daac0->FUN_0075f6f0(0x2000000, 1);
    }
}
