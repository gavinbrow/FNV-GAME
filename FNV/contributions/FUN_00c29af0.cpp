struct Vector3f {
    float x, y, z;
};
extern Vector3f _DAT_011a946c;
extern Vector3f _DAT_011a9478;
struct CollisionHelper {
    int __thiscall FUN_00c29900(float, unsigned int, unsigned int, unsigned int,
                                 unsigned int, float, float, Vector3f, Vector3f);
};
extern CollisionHelper* __cdecl FUN_00aa13e0(unsigned int);

int __cdecl FUN_00c29af0()
{
    CollisionHelper* helper = FUN_00aa13e0(0x100);
    if (helper) {
        return helper->FUN_00c29900(1.0f, 0, 0, 0, 0,
                                     1.0f, 1.0f, _DAT_011a946c,
                                     _DAT_011a9478);
    }
    return 0;
}