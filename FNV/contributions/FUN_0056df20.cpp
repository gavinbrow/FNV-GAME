struct __declspec(align(16)) FUN_0056ded0 {
 unsigned char transformData[64];
 FUN_0056ded0();
};
struct NiTransform { float rotation[9]; float translation[3]; float scale; };
FUN_0056ded0& __cdecl FUN_0056df80(FUN_0056ded0& destination,const NiTransform& source);
struct FUN_0056df20_Class {
 void FUN_0056e050(FUN_0056ded0*);
 void FUN_0056df20(const NiTransform& src);
};
// Built from prior 2026-10-25 contributions, with byte-addressable transform storage.
void FUN_0056df20_Class::FUN_0056df20(const NiTransform& src) {
 FUN_0056ded0 local;
 FUN_0056e050(&FUN_0056df80(local,src));
}