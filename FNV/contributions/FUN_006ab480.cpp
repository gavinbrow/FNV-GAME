// FUN_006ab480 - destructor of a polymorphic class (28 bytes, /Od /GS /EHsc).
//
// Target shape:
//   push ebp / mov ebp,esp / push ecx / mov [ebp-4],ecx : thiscall frame, this slot at [ebp-4]
//   mov eax,[ebp-4] / mov [eax],0x106b87c               : vftable store -> class is polymorphic
//   mov ecx,[ebp-4] / call 0x6a6b00                     : thiscall helper called from the body
//   mov esp,ebp / pop ebp / ret                         : plain epilogue (no EH state, no cookie,
//                                                        : and no this-return -> destructor, not ctor)
//
// The vftable store happens before the helper call, so the class has no
// destructible bases or members (no EH state, no trailing base-dtor call).
// 0x6a6b00 is not declared in the packet, so it gets its own stand-in owner
// struct, called on this exactly like the machine code shows.
// The single virtual is pure so that no second function symbol carrying the
// class name is emitted (the destructor must be the one found by name).

struct HelperOwner            // stand-in owner of the helper at 0x006a6b00
{
    void __thiscall FUN_006a6b00();
};

struct FUN_006ab480            // the polymorphic class this destructor belongs to
{
    virtual void vfn_0000() = 0;
    ~FUN_006ab480();
};

FUN_006ab480::~FUN_006ab480()
{
    ((HelperOwner*)this)->FUN_006a6b00();
}
