void __cdecl FUN_00c6ffc0();
struct ControllerShell {
    int& selectedMode() { return *reinterpret_cast<int*>((char*)this + 0x59c); }
    int& availableMode(int index) { return *reinterpret_cast<int*>((char*)this + 0x5a4 + index*4); }
    unsigned int& flags() { return *reinterpret_cast<unsigned int*>((char*)this + 0x414); }
    int FUN_00621a40();
    int FUN_00c6d960(int);
    void FUN_00c6d3f0(int);
    void FUN_00c70830(int);
    void CallVirtualReset(int value) {
        typedef void (__thiscall *VirtualFunc)(ControllerShell*, int);
        VirtualFunc* methods = *reinterpret_cast<VirtualFunc**>(this);
        methods[0x34](this, value);
    }
};
void ControllerShell::FUN_00c70830(int mode) {
    if (selectedMode() != mode && mode < 2 && availableMode(mode) != 0) {
        bool paused = (flags()>>15)&1;
        if (paused) FUN_00c6ffc0();
        selectedMode() = mode;
        FUN_00c6d3f0(FUN_00c6d960(FUN_00621a40()));
        if (paused) CallVirtualReset(0);
    }
}