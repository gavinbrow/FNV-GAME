struct Prefix32 { int unk00; int unk04; int unk08; int unk0C; int unk10; int unk14; int unk18; int unk1C; };
struct Context { void FUN_00c93920(void* value); };
struct Secondary {
 int unk00; int unk04; int child;
 void FUN_00de2950(Context* context);
};
struct Owner : Prefix32, Secondary {};
void Secondary::FUN_00de2950(Context* context) {
 Owner* owner = reinterpret_cast<Owner*>(reinterpret_cast<char*>(this) - sizeof(Prefix32));
 void* value;
 if (owner)
  value = &child;
 else
  value = 0;
 context->FUN_00c93920(value);
}
