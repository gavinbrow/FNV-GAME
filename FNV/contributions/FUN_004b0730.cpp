struct FUN_00658930_class { unsigned int __thiscall FUN_00658930() const; };
struct NiFormArray { void*& __thiscall FUN_00877a30(unsigned int index); };
unsigned int __fastcall FUN_0044ddc0(void* note);
struct ReceiverEntry { unsigned int type; void (__cdecl *callback)(void*, void*); };
struct FUN_004b0730_class { int unk00; void* unk04; int unk08; void __thiscall FUN_004b0730(void* note); };
void FUN_004b0730_class::FUN_004b0730(void* note)
{
    for (int i = 0; i < ((FUN_00658930_class*)((char*)this + 8))->FUN_00658930(); ++i) {
        if (((ReceiverEntry*)((NiFormArray*)((char*)this + 8))->FUN_00877a30(i))->type == FUN_0044ddc0(note)) {
            ((ReceiverEntry*)((NiFormArray*)((char*)this + 8))->FUN_00877a30(i))->callback(unk04, note);
        }
    }
}
