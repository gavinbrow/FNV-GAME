struct NiParticleBase {
    void* vtable;
    unsigned int unknown04;
    unsigned int unknown08;
    unsigned int unknown0c;
    unsigned int unknown10;
    unsigned int unknown14;
    unsigned int unknown18;
    unsigned int unknown1c;
    unsigned int unknown20;
    unsigned int unknown24;
    unsigned int unknown28;
    unsigned int unknown2c;
    unsigned int unknown30;
    unsigned int unknown34;
    unsigned int unknown38;
    unsigned int unknown3c;
    unsigned int unknown40;
    unsigned int unknown44;
    unsigned int unknown48;
    unsigned int unknown4c;
    unsigned int unknown50;
    unsigned int unknown54;
    unsigned int unknown58;
    unsigned int unknown5c;
    unsigned int unknown60;
    unsigned int unknown64;
    unsigned int unknown68;
    unsigned int unknown6c;
    unsigned int unknown70;
    unsigned int unknown74;
    unsigned int unknown78;
    unsigned int unknown7c;
    unsigned int unknown80;
    unsigned int unknown84;
    unsigned int unknown88;
    unsigned int unknown8c;
    unsigned int unknown90;
    unsigned int unknown94;
    unsigned int unknown98;
    void __thiscall FUN_00a5ecb0(int);
};
struct NiParticleBuffer {
    void* data;
    unsigned int count;
    unsigned short capacity;
    unsigned short used;
    unsigned short growth;
    unsigned short flags;
    void __thiscall FUN_0060bef0(int);
};
struct NiParticleSubobject {
    void* first;
    void* second;
    void* third;
    void* fourth;
    void __thiscall FUN_00a69940();
};
struct NiParticleObject : NiParticleBase {
    NiParticleBuffer buffer;
    NiParticleSubobject firstMember;
    NiParticleSubobject secondMember;
};
extern void* __cdecl FUN_00aa13e0(unsigned int);
extern const char DAT_010a1024;
NiParticleObject* __cdecl FUN_00a9aea0() {
    NiParticleObject* object =
        (NiParticleObject*)FUN_00aa13e0(0xcc);
    if (object) {
        object->FUN_00a5ecb0(0);
        object->vtable = (void*)&DAT_010a1024;
        object->firstMember.FUN_00a69940();
        object->secondMember.FUN_00a69940();
        object->buffer.FUN_0060bef0(2);
        object->buffer.flags = 0;
        return object;
    }
    return 0;
}