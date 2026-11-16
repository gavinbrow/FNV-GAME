#include "h_e1bbadcaffc3.h"
extern "C" void* DAT_0109fd0c;

struct RegistrationManager
{
    void** vtable;
    void Deregister(void* object)
    {
        typedef void (__thiscall *Function)(RegistrationManager*, void*);
        Function callback = reinterpret_cast<Function>(vtable[62]);
        callback(this, object);
    }
};
extern RegistrationManager* DAT_011f4748;

struct RefCounted
{
    void** vtable;
    volatile long m_uiRefCount;
    void DecRefCount()
    {
        if (InterlockedDecrement(&m_uiRefCount) == 0)
        {
            typedef void (__thiscall *DeleteFunction)(RefCounted*);
            reinterpret_cast<DeleteFunction>(vtable[1])(this);
        }
    }
};

void __cdecl FUN_00aa1460(void* object, unsigned int size);

struct TextureEffectMatch
{
    void** m_vtable;
    void FUN_00a69030();
    TextureEffectMatch* FUN_00a92bd0(unsigned int flags);
};

TextureEffectMatch* TextureEffectMatch::FUN_00a92bd0(unsigned int flags)
{
    m_vtable = reinterpret_cast<void**>(&DAT_0109fd0c);
    if (DAT_011f4748)
        DAT_011f4748->Deregister(this);
    RefCounted* resource = *reinterpret_cast<RefCounted**>(reinterpret_cast<char*>(this) + 0x124);
    if (resource)
        resource->DecRefCount();
    FUN_00a69030();
    if (flags & 1)
        FUN_00aa1460(this, 0x15c);
    return this;
}