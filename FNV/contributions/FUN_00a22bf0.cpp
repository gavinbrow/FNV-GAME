struct InputDevice {
    virtual unsigned long __stdcall QueryInterface() = 0;
    virtual unsigned long __stdcall AddRef() = 0;
    virtual unsigned long __stdcall Release() = 0;
    virtual unsigned long __stdcall GetCapabilities() = 0;
    virtual unsigned long __stdcall EnumObjects() = 0;
    virtual unsigned long __stdcall GetProperty() = 0;
    virtual unsigned long __stdcall SetProperty() = 0;
    virtual unsigned long __stdcall Acquire() = 0;
    virtual unsigned long __stdcall Unacquire() = 0;
};
struct InputInterface {
    virtual unsigned long __stdcall QueryInterface() = 0;
    virtual unsigned long __stdcall AddRef() = 0;
    virtual unsigned long __stdcall Release() = 0;
};

struct NiAllocator { void __thiscall FUN_00aa4060(void*); };
extern NiAllocator DAT_011f6238;

struct InputManagerClose {
    unsigned int unk00;
    unsigned int flags;
    InputInterface* directInput;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    InputDevice* keyboard;
    InputDevice* mouse;
    void __thiscall FUN_00a252d0(int);
    void __thiscall FUN_00a22bf0();
};
void InputManagerClose::FUN_00a22bf0()
{
    if (flags & 1) {
        FUN_00a252d0(0);
    }
    if (keyboard) {
        keyboard->Unacquire();
        keyboard->Release();
    }
    if (mouse) {
        mouse->Unacquire();
        mouse->Release();
    }
    directInput->Release();
    if (*(void**)((char*)this + 0x1b84)) {
        void* buffer = *(void**)((char*)this + 0x1b84);
        DAT_011f6238.FUN_00aa4060(buffer);
    }
}
