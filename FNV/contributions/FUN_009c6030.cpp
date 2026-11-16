struct Vector3 {
    float x, y, z;
    void __thiscall FUN_00439ef0(Vector3* dest, void* context);
    void __thiscall FUN_004a0c10();
};
struct OrientationSource {
    float __thiscall FUN_00966980();
};
struct OrientationObject {
    void** vtable;
    float __thiscall FUN_00931d70();
    void __thiscall FUN_00931d90(float value);
    OrientationSource* __thiscall FUN_004181e0();
    void __thiscall FUN_009c6030(Vector3 input);
};
extern "C" float __cdecl FUN_004b1460(float);
extern "C" float __cdecl FUN_004b13c0(Vector3*);
extern "C" float __cdecl FUN_00408840(float);
extern const double DAT_01012060;
extern const double DAT_01018c00;
typedef void* (__thiscall *GetContextFn)(OrientationObject*);
typedef float (__thiscall *GetAngleFn)(OrientationObject*, int);
typedef void (__thiscall *SetAngleFn)(OrientationObject*, float);
void OrientationObject::FUN_009c6030(Vector3 input) {
    Vector3 c;
    input.FUN_00439ef0(&c, ((GetContextFn*)vtable)[125](this));
    Vector3 b = c;
    b.FUN_004a0c10();
    float e = ((GetAngleFn*)vtable)[175](this, 0);
    float d = FUN_00931d70();
    float a = FUN_004181e0()->FUN_00966980();
    if (a == DAT_01012060) {
        d = -FUN_004b1460(b.z / (1.0f - b.z * b.z));
    }
    e = FUN_004b13c0(&b);
    if (a == DAT_01012060 ||
        FUN_00408840(e - ((GetAngleFn*)vtable)[175](this, 0)) <= DAT_01018c00) {
        ((SetAngleFn*)vtable)[177](this, e);
    }
    FUN_00931d90(d);
}