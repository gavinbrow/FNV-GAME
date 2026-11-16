
extern __declspec(thread) unsigned int g_tlsMemoryMode;
int __cdecl FUN_00c802d0(int);
void* __cdecl FUN_00aa13e0(unsigned int);
struct FUN_00c894d0 {
 unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
 FUN_00c894d0(int, int, int, int, int);
 static void* operator new(unsigned int count) { return FUN_00aa13e0(count); }
};
struct ScopedMemoryMode {
 unsigned int previousMode;
 explicit ScopedMemoryMode(unsigned int mode) : previousMode(g_tlsMemoryMode) { g_tlsMemoryMode=mode; }
 ~ScopedMemoryMode(){g_tlsMemoryMode=previousMode;}
};
FUN_00c894d0* __cdecl FUN_00c89540(int first, int second, int resourceId, int finalArgument) {
 ScopedMemoryMode scopedMode(16);
 FUN_00c894d0* result = 0;
 if (resourceId != 0) {
   int info = FUN_00c802d0(resourceId);
   if (info != 0) {
     result = new FUN_00c894d0(first,second,resourceId,info,finalArgument);
   }
 }
 return result;
}
