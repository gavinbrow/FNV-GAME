extern "C" char* DAT_0109b220;
extern "C" int DAT_010c09cc;
extern "C" void (__stdcall *DAT_00fdf1c0)(char*);
extern "C" void (__stdcall *DAT_00fdf1c4)(char*);
struct ParticleModifier {
    void* vtable;
    unsigned int referenceCount;
    char* name;
    unsigned int order;
    void* target;
    bool active;
    void __thiscall FUN_00a5d3a0();
    ParticleModifier* __thiscall FUN_00c316a0(char* volatile* newName, unsigned int newOrder);
};
ParticleModifier* __thiscall ParticleModifier::FUN_00c316a0(char* volatile* newName, unsigned int newOrder) {
    FUN_00a5d3a0();
    vtable = &DAT_010c09cc;
    name = DAT_0109b220;
    order = newOrder;
    target = 0;
    active = true;
    char* replacement = *newName;
    if (name != replacement) {
        if (replacement != DAT_0109b220)
            DAT_00fdf1c0(replacement - 8);
        if (name != DAT_0109b220)
            DAT_00fdf1c4(name - 8);
        name = replacement;
    }
    return this;
}