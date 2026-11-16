
struct ContactCallDescriptor {
    int kind;
    void* firstManager;
    void* secondManager;
    void* owner;
    int reservedStatus;
    void* sourceTail;
    void* sourceContact;
    unsigned char state0, state1, state2, state3;
    void* sourceHeader;
    void* forwardedArgument;
    void* sourceProperties;
    int statusA, statusB;
};
struct ContactSource {
    void* unk00;
    int unk04, unk08;
    void* firstManager;
    void* secondManager;
    int unk14, member18, unk1c, unk20, unk24, unk28, member2c;
    int unk30,unk34,unk38,unk3c,unk40,unk44,unk48,unk4c,member50;
};
extern "C" void __cdecl FUN_00d00ca0(void*, ContactCallDescriptor*);
extern "C" void __cdecl FUN_00cfff00(void*, int*);
struct ContactContext {
    void FUN_00cfcd70(ContactSource* source, void* other);
};
void ContactContext::FUN_00cfcd70(ContactSource* source, void* other)
{
    ContactCallDescriptor info;
    info.owner = this;
    info.kind = 2;
    info.firstManager = source->firstManager;
    info.secondManager = source->secondManager;
    info.reservedStatus = 0;
    info.sourceTail = &source->member50;
    info.sourceContact = &source->member18;
    info.state0 = 0;
    info.state1 = 0;
    info.state2 = 0;
    info.sourceHeader = &source->unk04;
    info.forwardedArgument = other;
    info.sourceProperties = &source->member2c;
    info.statusA = 0;
    info.statusB = 0;
    void* first = source->firstManager;
    FUN_00d00ca0(*(void**)((char*)first + 8), &info);
    info.kind = 0;
    if (*(unsigned short*)((char*)source->firstManager + 0x204) != 0)
        FUN_00cfff00(source->firstManager, &info.kind);
    info.kind = 1;
    if (*(unsigned short*)((char*)source->secondManager + 0x204) != 0)
        FUN_00cfff00(source->secondManager, &info.kind);
}
