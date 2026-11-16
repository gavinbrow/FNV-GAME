#include <xmmintrin.h>
struct Matrix { __m128 columns[4]; };
struct Receiver { void FUN_00c7f640(Matrix*,const __m128*); };
struct BodySlot { void* body; __forceinline void* getBody() { if (this) return body; return 0; } };
struct CollisionOwner {
void* vtable; void* unk04; void* node;
void FUN_00a29680(); void FUN_00c8e670(Receiver*);
__forceinline BodySlot* GetSlot() { char* base=(char*)node; if(base){FUN_00a29680(); base+=16; FUN_00a29680(); if(base) return (BodySlot*)base;} return 0; }
};
extern float DAT_0104ffb8; extern float DAT_01011d78; extern float DAT_01017d00;
void CollisionOwner::FUN_00c8e670(Receiver* target) {
__m128 second, first; __declspec(align(16)) Matrix source;
typedef void (__thiscall *GetSource)(CollisionOwner*,Matrix*);
((GetSource)((void**)vtable)[61])(this,&source);
BodySlot* slot=GetSlot(); void* body=slot?slot->getBody():0;
if(body) {
typedef void (__thiscall *Dispatch)(void*, Matrix*, float, Receiver*);
((Dispatch)((void**)*(void* volatile*)body)[7])(body,&source,DAT_01017d00,target);
} else {
first=_mm_setr_ps(DAT_0104ffb8,DAT_0104ffb8,DAT_0104ffb8,DAT_01011d78);
second=_mm_setr_ps(DAT_01017d00,DAT_01017d00,DAT_01017d00,DAT_01011d78);
target->FUN_00c7f640(&source,&first);
((Receiver*)((char*)target+16))->FUN_00c7f640(&source,&second);
}
}