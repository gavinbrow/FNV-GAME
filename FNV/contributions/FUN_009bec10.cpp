class GameObject {
public:
    void** vtable;
    bool __thiscall FUN_00444d00(unsigned int flags);
    void __thiscall FUN_009bec10(float value);
};

typedef void (__thiscall *VirtualCall)(GameObject*, float);

void __thiscall GameObject::FUN_009bec10(float value)
{
    if (!FUN_00444d00(0x80)) {
        ((VirtualCall)(vtable[190]))(this, value);
    }
}
