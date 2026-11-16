struct NiMemObject {
    static void* operator new(unsigned int size);
};
void __fastcall FUN_00a6d220(void* object);
extern float DAT_01015f5c;
extern int DAT_010be8e4;

struct NiCloningProcess {};
struct CloneableObj {
    void* vtable;
    void FUN_00a6cfe0(CloneableObj* object, void* argument);
};
struct FUN_00c28430_Object : CloneableObj {
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
    float value34;
};
struct FUN_00c28430_class : CloneableObj {
    FUN_00c28430_Object* FUN_00c28430(void* volatile argument);
};
FUN_00c28430_Object* FUN_00c28430_class::FUN_00c28430(void* volatile argument)
{
    FUN_00c28430_Object* object = (FUN_00c28430_Object*)NiMemObject::operator new(0x38);
    if (object) {
        FUN_00a6d220(object);
        object->value34 = DAT_01015f5c;
        object->vtable = &DAT_010be8e4;
        FUN_00a6cfe0(object, argument);
    } else {
        object = 0;
        void* copy = argument;
        FUN_00a6cfe0(object, copy);
    }
    return object;
}

