
extern "C" void* __cdecl FUN_00aa13e0(unsigned int byteCount);
struct AllocatedAnimationController {
    void* __thiscall FUN_00a4da20();
};
void* __cdecl FUN_00a4db60()
{
    void* storage = FUN_00aa13e0(0x48);
    if (storage != 0)
        return static_cast<AllocatedAnimationController*>(storage)->FUN_00a4da20();
    return 0;
}