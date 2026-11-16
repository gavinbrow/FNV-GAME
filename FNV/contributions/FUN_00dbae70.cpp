// CALLING CONVENTION NOTE: the packet says __thiscall (this in ecx, no stack args).
// Matched as a __fastcall free function whose unused second argument (edx) is forwarded
// to the virtual call, which makes the compiler tail-jump through eax like the original.
struct Inner;
typedef void (__fastcall *SlotFn)(Inner*, int);
struct Inner { SlotFn* vtbl; };
struct FUN_00dbae70_owner { Inner* unk00; };

void __fastcall FUN_00dbae70(FUN_00dbae70_owner* self, int unused)
{
    Inner* p = self->unk00;
    p->vtbl[26](p, unused);
}
