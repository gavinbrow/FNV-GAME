struct GlobalObjectO2_00d472a0 { int x; };
extern GlobalObjectO2_00d472a0 g_012690d4;
struct FUN_00cd12b0_cls { void FUN_00cd1330(int value, const void* category, const char* name, int flags); };
struct Prefix { FUN_00cd12b0_cls* owner; int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18; int unk1c; int unk20; int unk24; int unk28; int unk2c; int unk30; int unk34; int unk38; int unk3c; int unk40; int unk44; int unk48; int unk4c; int unk50; int unk54; int unk58; };
struct Context { int contextState; void FUN_00cd2020(int value); };
struct Owner : Prefix, Context {};
void Context::FUN_00cd2020(int value) {
    Owner* object = reinterpret_cast<Owner*>(reinterpret_cast<char*>(this) - sizeof(Prefix));
    FUN_00cd12b0_cls* target = object->owner;
    if (target) target->FUN_00cd1330(value, &g_012690d4, "Actions", 0);
}
