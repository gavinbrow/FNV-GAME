// Reconstructed source for FUN_00d119c0 (forwarding thunk, 24 bytes).
// Target shape:
//   mov edx, [esp+4]            ; handle (first stack arg)
//   mov eax, [edx]              ; handle->unk00 (entry index)
//   shl eax, 4                  ; * 16 (entry stride)
//   add eax, [ecx+0xA0]         ; + &this->entries
//   mov [esp+4], eax            ; forward as first stack arg
//   jmp FUN_00d11650            ; __thiscall tail call, ecx = this preserved

struct UnkHandle {
    int unk00; // entry index read at [handle]
};

struct SweepEntry { // 16-byte entry, matches shl eax,4 stride
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
};

// Tail-call target observed forwarding (this, handle, entry) with edx = handle kept live:
// __fastcall helper taking (self in ecx, handle in edx, entry on stack).
void __fastcall FUN_00d11650(void* self, UnkHandle* handle, SweepEntry* entry);

// Stand-in owner class for the __thiscall thunk; fnvcheck matches the name FUN_00d119c0.
struct FUN_00d119c0_owner {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    int unk20;
    int unk24;
    int unk28;
    int unk2C;
    int unk30;
    int unk34;
    int unk38;
    int unk3C;
    int unk40;
    int unk44;
    int unk48;
    int unk4C;
    int unk50;
    int unk54;
    int unk58;
    int unk5C;
    int unk60;
    int unk64;
    int unk68;
    int unk6C;
    int unk70;
    int unk74;
    int unk78;
    int unk7C;
    int unk80;
    int unk84;
    int unk88;
    int unk8C;
    int unk90;
    int unk94;
    int unk98;
    int unk9C;
    SweepEntry* unkA0; // entry array base pointer at this+0xA0

    void FUN_00d119c0(UnkHandle* handle);
};

void FUN_00d119c0_owner::FUN_00d119c0(UnkHandle* handle) {
    FUN_00d11650(this, handle, this->unkA0 + handle->unk00);
}
