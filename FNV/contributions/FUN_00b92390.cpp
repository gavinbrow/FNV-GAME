extern "C" char DAT_010b5ad4;
extern "C" char DAT_010b33c4;
extern "C" char DAT_01011584;
extern "C" char DAT_010b0820;
extern "C" char DAT_010b5acc;
extern "C" char DAT_010a93ec;
extern "C" int __cdecl FUN_00b4f380(int value);
extern "C" void* __cdecl FUN_00ec61c0(void* destination, int value, unsigned int size);

struct ShaderConstants {
    unsigned int value00, value01, value02, value03, value04;
    unsigned int value05, value06, value07, value08, value09;
    unsigned int value10, value11, value12, value13, value14;
};

struct ShaderPassParameters {
    const void* shader;
    const void* renderer;
    const void* state;
    unsigned int mode;
    ShaderConstants constants;
};

struct ShaderEffect {
    void** vtable;
    void __thiscall FUN_00b92390();
};

typedef void (__thiscall *ConfigureEffect)(
    ShaderEffect*, ShaderPassParameters*, ShaderPassParameters*,
    const void*, const void*, int);
typedef void (__thiscall *FinalizeEffect)(ShaderEffect*);

void __thiscall ShaderEffect::FUN_00b92390() {
    ShaderPassParameters first;
    first.shader = &DAT_010b5ad4;
    first.renderer = &DAT_010b33c4;
    first.state = &DAT_01011584;
    first.mode = 0;
    FUN_00ec61c0(&first.constants, 0, sizeof(first.constants));

    ShaderPassParameters second;
    second.shader = &DAT_010b0820;
    second.renderer = &DAT_010b33c4;
    second.state = &DAT_01011584;
    second.mode = 0;
    FUN_00ec61c0(&second.constants, 0, sizeof(second.constants));

    int enabled = FUN_00b4f380(1);
    ConfigureEffect configure = (ConfigureEffect)vtable[0x13c / 4];
    configure(this, &first, &second, &DAT_010b5acc,
              &DAT_010a93ec, enabled);

    FinalizeEffect finalize = (FinalizeEffect)vtable[0x14c / 4];
    finalize(this);
}