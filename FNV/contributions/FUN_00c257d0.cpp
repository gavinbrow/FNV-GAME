extern "C" void* __cdecl FUN_00aa13e0(unsigned int size);
extern unsigned int UNK_010be35c;
struct ParticleSystem { unsigned int* vtable; void __thiscall FUN_00c1b5c0(); };
struct ParticleOwner {
    void __thiscall FUN_00c1b6f0(ParticleSystem* object, unsigned int flags);
    ParticleSystem* __thiscall FUN_00c257d0(unsigned int flags);
};
ParticleSystem* ParticleOwner::FUN_00c257d0(unsigned int flags)
{
    ParticleSystem* object = static_cast<ParticleSystem*>(FUN_00aa13e0(0x110));
    if (object) {
        object->FUN_00c1b5c0();
        object->vtable = &UNK_010be35c;
    } else {
        object = 0;
    }
    this->FUN_00c1b6f0(object, flags);
    return object;
}