struct VtableOwner;
struct Selection { bool __thiscall FUN_0049c390(); };
struct Container { Selection* __thiscall FUN_00497280(unsigned short handle, unsigned int* output); };
typedef Container* (__thiscall* GetContainerMethod)(VtableOwner*);
struct VtableOwner {
    void** vtable;
    unsigned short __thiscall FUN_00897910(unsigned int mode, int value, bool empty, int reserved);
};

bool __cdecl FUN_0097f310(VtableOwner* object, int value)
{
    bool result = false;
    unsigned short handle = object->FUN_00897910(0x18, value, value == 0, 0);
    if (handle != 0) {
        Container* container = reinterpret_cast<GetContainerMethod>(object->vtable[121])(object);
        if (container != 0) {
            unsigned int output;
            if (container->FUN_00497280(handle, &output)->FUN_0049c390()) {
                result = true;
            }
        }
    }
    return result;
}