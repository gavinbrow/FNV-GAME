struct Vec3 { float x, y, z; void __thiscall FUN_00416870(float,float,float); };
struct ActionSource { Vec3* __thiscall FUN_00439e90(); };
struct ObjectPart { ActionSource* __thiscall FUN_005c3420(Vec3*,Vec3*,Vec3*); void* __thiscall FUN_006dd4f0(); };
struct Object { float __thiscall FUN_006d2c40(); float __thiscall FUN_006d2c20(); ObjectPart* __thiscall FUN_0048d150(); };
struct ElevationProvider { bool __thiscall FUN_005547c0(Vec3*,float*); };
extern bool __cdecl FUN_006d34d0(Object*,Vec3*);
extern float __cdecl FUN_004a4240();
extern float __cdecl FUN_00476b70(float,float);
extern float __cdecl FUN_004e44d0(float);
extern float __cdecl FUN_004e4490(float);
void __cdecl FUN_006d33c0(Object* object,Vec3* result) {
if(FUN_006d34d0(object,result)) return;
float a=FUN_004a4240();
float g;
float b=FUN_00476b70(object->FUN_006d2c20(),object->FUN_006d2c40());
Vec3 f;
f.FUN_00416870(FUN_004e4490(a)*b,FUN_004e44d0(a)*b,0.0f);
Vec3 c;
Vec3 e;
*result = *object->FUN_0048d150()->FUN_005c3420(&c,&e,&f)->FUN_00439e90();
ElevationProvider* d=static_cast<ElevationProvider*>(object->FUN_0048d150()->FUN_006dd4f0());
if(!d) return;
if(!d->FUN_005547c0(result,&g)) return;
result->z=g;
}