struct BoundsNode { unsigned short m00,m02,m04,m06,m08,m0A,m0C,m0E,m10,m12; };
struct FUN_00d9a4d0_cls { BoundsNode* __thiscall FUN_00d9a4d0(unsigned short key); };
struct FUN_00d9b450_cls { int m00,m04,m08,m0C,m10,m14,m18; FUN_00d9a4d0_cls m1c; void __thiscall FUN_00d9b450(BoundsNode* a1,unsigned short a2,unsigned short a3); };
void FUN_00d9b450_cls::FUN_00d9b450(BoundsNode* a1,unsigned short a2,unsigned short a3) {
 a1->m12=a3;
 if(a1->m10&0x8000) return;
 BoundsNode* n1=m1c.FUN_00d9a4d0(a1->m0C);
 BoundsNode* n2=m1c.FUN_00d9a4d0(a1->m0E);
 n1->m10=(n1->m10&0x8000)|a2;
 n2->m10=(n2->m10&0x8000)|a2;
 FUN_00d9b450(n1,a1->m0C,a1->m0E);
 FUN_00d9b450(n2,a1->m0E,a3);
 unsigned short b=n2->m06, c=n1->m06; a1->m06=c<b?c:b;
 b=n2->m00; c=n1->m00; a1->m00=c>b?c:b;
 b=n2->m08; c=n1->m08; a1->m08=c<b?c:b;
 b=n2->m02; c=n1->m02; a1->m02=c>b?c:b;
 b=n2->m0A; c=n1->m0A; a1->m0A=c<b?c:b;
 b=n2->m04; c=n1->m04; a1->m04=c>b?c:b;
}