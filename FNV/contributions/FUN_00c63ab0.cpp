extern "C" void* VTABLE_010a0d24;
extern "C" void* VTABLE_010c38ac;
struct Vector3i { int x; int y; int z; };
struct FUN_00c63ab0 {
    void* vtable;
    int field04;
    int field08;
    int parameter0c;
    unsigned short count10;
    unsigned short status12;
    unsigned int entries[8];
    Vector3i bounds;
    void __thiscall FUN_00a7b2e0();
    FUN_00c63ab0(int parameter);
};
FUN_00c63ab0::FUN_00c63ab0(int parameter)
{
    FUN_00a7b2e0();
    vtable = &VTABLE_010a0d24;
    parameter0c = parameter;
    vtable = &VTABLE_010c38ac;
    int index;
    Vector3i* coordinate = &bounds;
    coordinate->z = 0;
    coordinate->x = 0;
    coordinate->y = 0;
    count10 = 0;
    for (index = 0; index < 8; ++index) {
        entries[index] = 0;
    }
}
