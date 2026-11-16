struct Owner { void FUN_00cd10a0(int); };
struct FUN_00cd1f60_cls { void FUN_00cd1f60(int); };
void FUN_00cd1f60_cls::FUN_00cd1f60(int value) {
    Owner* owner = *(Owner**)((char*)this - 0x50);
    if (owner)
        owner->FUN_00cd10a0(value);
}
