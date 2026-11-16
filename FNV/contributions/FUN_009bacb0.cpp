class NiNode;
template<class T> struct NiPointer { T* pointer; NiPointer(T*); ~NiPointer(); NiPointer& operator=(T*); };
struct ProjectileData { float FUN_00507e10(); };
struct Projectile { ProjectileData* FUN_004181e0(); unsigned int FUN_00476c90(); };
struct FUN_009bacb0 {
    unsigned char flagsA,flagsB,flagsC,state;
    float elapsed,total;
    NiPointer<NiNode> first,second;
    ProjectileData* data;
    unsigned int handle;
    void* context;
    FUN_009bacb0(Projectile*,void*);
    void FUN_009baf50(void*);
};
FUN_009bacb0::FUN_009bacb0(Projectile* projectile,void* value) : first(0), second(0) {
    first=0;
    second=0;
    data=projectile ? projectile->FUN_004181e0() : 0;
    handle=projectile ? projectile->FUN_00476c90() : 0;
    context=value;
    flagsA=0;
    flagsB=0;
    flagsC=0;
    elapsed=0.0f;
    total=data->FUN_00507e10();
    FUN_009baf50(value);
}
