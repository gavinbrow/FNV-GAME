struct FUN_0069f920_Sub { void* __thiscall FUN_006a1920(); void* __thiscall FUN_006e8f80(unsigned int); };
struct FUN_006e2280 {
int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c;
int unk20, unk24, unk28, unk2c, unk30, unk34, unk38;
FUN_006e2280(int, int);
};
void* __cdecl operator new(unsigned int, void*);
void __cdecl operator delete(void*, void*);
struct FUN_0069f920_cls {
int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c;
FUN_0069f920_Sub unk20;
void* __thiscall FUN_0069f920(int, int);
};
void* __thiscall FUN_0069f920_cls::FUN_0069f920(int a,int b){
void* pNode = unk20.FUN_006a1920();
void* pPlace = unk20.FUN_006e8f80((unsigned int)pNode);
new(pPlace) FUN_006e2280(a,b);
return pNode;
}