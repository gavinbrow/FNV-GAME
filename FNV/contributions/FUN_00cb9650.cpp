// FUN_00cb9650 @ 0x00cb9650, 97 bytes, __cdecl caller-pops
// flags: /MT /O2 /GS /EHsc /Gy
// Recursive child-visitor: controller fetch/set via members, virtual node
// fetch (vtable slot 3), loop over children (ptr @0xA0, count u16 @0xA6).

struct FUN_00cb9650_Node {
    int unk00;
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
    void** children;          // 0xA0
    unsigned short unkA4;     // 0xA4
    unsigned short count;     // 0xA6
};

struct FUN_00cb9650_Object {
    virtual void vf00();
    virtual void vf04();
    virtual void vf08();
    virtual FUN_00cb9650_Node* vf0C();

    void* FUN_00a5c570(const void* typeInfo);
    void FUN_00a5c480(int value);
};

extern const char DAT_012683f4[];

void __cdecl FUN_00cb9650(FUN_00cb9650_Object* object)
{
    if (object != 0) {
        void* controller = object->FUN_00a5c570(DAT_012683f4);
        if (controller != 0) {
            object->FUN_00a5c480((int)controller);
        }

        FUN_00cb9650_Node* node = object->vf0C();
        if (node != 0) {
            for (unsigned int index = 0; index < node->count; ++index) {
                FUN_00cb9650((FUN_00cb9650_Object*)node->children[index]);
            }
        }
    }
}
