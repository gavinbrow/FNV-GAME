struct FUN_006815c0 { void* object; FUN_006815c0(); ~FUN_006815c0(); };
struct FUN_0065de30 { unsigned int value; FUN_0065de30(const FUN_0065de30&); unsigned int FUN_0044abd0(int flag); };
struct FUN_008c71b0 { unsigned int value; FUN_008c71b0(void* owner); ~FUN_008c71b0(); };
void* __cdecl operator new(unsigned int size, unsigned int allocation);
void __cdecl operator delete(void* object, unsigned int allocation);
struct FUN_0065dc90 : FUN_006815c0 { FUN_0065de30 member; FUN_0065dc90(FUN_0065de30 argument); };
FUN_0065dc90::FUN_0065dc90(FUN_0065de30 argument)
  : FUN_006815c0(), member(argument) {
    object = new (member.FUN_0044abd0(1)) FUN_008c71b0(this);
}