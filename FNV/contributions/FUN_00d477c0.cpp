struct D477C0Input { int unk00, unk04, unk08; void* value0c; };
struct D477C0Source { int FUN_00d46d40(); int FUN_00d46de0(); };
struct D477C0RegistryA {
    virtual void slot00(); virtual void slot04(); virtual void slot08();
    virtual void slot0c(); virtual void slot10(); virtual void slot14();
    virtual void slot18(); virtual void registerObject(D477C0Source*, int);
};
struct D477C0RegistryB {
    virtual void slot00(); virtual void slot04();
    virtual void slot08(); virtual void registerInput(D477C0Input*);
};
struct D477C0RegistryC {
    virtual void slot00(); virtual void slot04();
    virtual void slot08(); virtual void registerLink(void*, D477C0Source*);
};
void __stdcall FUN_00d477c0(D477C0Input* input, D477C0Source* source)
{
    D477C0RegistryA* registryA = *(D477C0RegistryA**)&DAT_01269b14;
    registryA->registerObject(source, source->FUN_00d46d40());
    D477C0RegistryB* registryB = *(D477C0RegistryB**)&DAT_01269b18;
    registryB->registerInput(input);
    if (source->FUN_00d46de0() > 0) {
        D477C0RegistryC* registryC = *(D477C0RegistryC**)&DAT_01269b10;
        registryC->registerLink(input->value0c, source);
    }
}