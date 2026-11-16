Holder* FUN_00c85750();
struct hkpMultiSphereAgent {
    unsigned int vptr;
    unsigned short unk04;
    hkpMultiSphereAgent* __thiscall FUN_00d44b00(int a, int b, int c, int d);
};
void* __cdecl FUN_00d44cc0(int a, int b, int c, int d) {
    Holder* holder = FUN_00c85750();
    hkpMultiSphereAgent* object = (hkpMultiSphereAgent*)holder->allocator->Allocate(0x38);
    object->unk04 = 0x38;
    return object->FUN_00d44b00(a, b, c, d);
}
