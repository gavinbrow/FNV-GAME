extern int DAT_010b0158;
extern int DAT_010b0674;
extern int DAT_010b066c;
extern int DAT_010a93ec;
extern int DAT_010a93cc;
void* __cdecl FUN_00ec61c0(void*, int, unsigned int);

struct ShaderArgument_00b8d3a0 {
    const void* source;
    unsigned int flags;
    unsigned int count;
    float components[16];
};

struct ShaderController_00b8d3a0 {
    void** vtable;
    void FUN_00b8d3a0();
};

typedef void (__thiscall *ConfigureShader_00b8d3a0)(
    ShaderController_00b8d3a0*,
    ShaderArgument_00b8d3a0*,
    ShaderArgument_00b8d3a0*,
    const int*, const int*, const int*);
typedef void (__thiscall *RunShader_00b8d3a0)(ShaderController_00b8d3a0*);

void ShaderController_00b8d3a0::FUN_00b8d3a0()
{
    ShaderArgument_00b8d3a0 first;
    first.source = &DAT_010b0158;
    first.flags = 0;
    first.count = 0;
    FUN_00ec61c0(first.components, 0, sizeof(first.components));

    ShaderArgument_00b8d3a0 second;
    second.source = &DAT_010b0674;
    second.flags = 0;
    second.count = 0;
    FUN_00ec61c0(second.components, 0, sizeof(second.components));

    ConfigureShader_00b8d3a0 configure =
        reinterpret_cast<ConfigureShader_00b8d3a0>(vtable[0x13c / 4]);
    configure(this, &first, &second,
        &DAT_010b066c, &DAT_010a93ec, &DAT_010a93cc);

    RunShader_00b8d3a0 run =
        reinterpret_cast<RunShader_00b8d3a0>(vtable[0x14c / 4]);
    run(this);
}