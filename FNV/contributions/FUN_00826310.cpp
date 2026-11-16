struct FUN_008262e0 {
 unsigned int m00;
 unsigned int m04;
 unsigned int m08;
 unsigned int m0c;
 unsigned int m10;
 unsigned int m14;
 unsigned int m18;
 unsigned int m1c;
 unsigned int m20;
 unsigned int m24;
 unsigned int m28;
 unsigned int m2c;
 unsigned int m30;
 unsigned int m34;
 unsigned int m38;
 unsigned int m3c;
 unsigned int m40;
 unsigned int m44;
 unsigned int m48;
 FUN_008262e0(void* source, void* actor, void* target);
};
struct ParalysisController {
 virtual void v00();
 virtual void v04();
 virtual void v08();
 virtual void v0c();
 virtual void v10();
 virtual void v14();
 virtual void v18();
 virtual void v1c();
 virtual void v20();
 virtual void v24();
 virtual void v28();
 virtual void v2c();
 virtual void v30();
 virtual void v34();
 virtual void v38();
 virtual void v3c();
 virtual void v40();
 virtual void Register(void *effect);
 unsigned int vtableField04;
 void* actor08;
 void* target0c;
 unsigned int m10,m14,m18,m1c,m20,m24;
 void* source28;
 void* FUN_00826310();
};
void* ParalysisController::FUN_00826310()
{
    FUN_008262e0 *effect = new FUN_008262e0(source28,actor08,target0c);
    Register(effect);
    return effect;
}