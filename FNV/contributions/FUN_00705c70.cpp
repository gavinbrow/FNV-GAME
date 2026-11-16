struct FUN_0047ee30_shell : public InterfaceManager {
    char FUN_0047ee30();
};

extern "C" char __cdecl FUN_00705c70()
{
    if (FUN_004b7210() && 
        reinterpret_cast<FUN_009373f0_shell*>(FUN_004b7210())->FUN_009373f0()) {
        return reinterpret_cast<FUN_0047ee30_shell*>(FUN_004b7210())->FUN_0047ee30();
    }
    return -1;
}
