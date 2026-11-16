struct Vector3 {
 float x,y,z;
 Vector3() {}
 Vector3(float x0,float y0,float z0):x(x0),y(y0),z(z0) {}
};
struct Matrix3 {float m00,m01,m02,m10,m11,m12,m20,m21,m22;};
struct StoredPosition {float unk00;Vector3 position;};
extern "C" double DAT_01012070;
extern "C" float __cdecl FUN_00eb5450(const Vector3*,const Matrix3*,void*,void*);
struct CollisionGeometry {
 int unk00,unk04,unk08,unk0C,unk10,unk14,unk18,unk1C,unk20,unk24,unk28,unk2C,unk30,unk34;
 StoredPosition* base; Matrix3 basis; float scaling; int param64,param68;
 float __thiscall FUN_00eb5bf0(const Vector3*,const Vector3*,float);
};
float __thiscall CollisionGeometry::FUN_00eb5bf0(const Vector3* motion,const Vector3* translation,float amount) {
 Vector3 scaled(motion->x*amount,motion->y*amount,motion->z*amount);
 const Vector3& p=base->position;
 Vector3 newPoint(p.x+scaled.x,p.y+scaled.y,p.z+scaled.z);
 Matrix3 adjusted=basis;
 Vector3 axis(translation->x*amount,translation->y*amount,translation->z*amount);
 adjusted.m00=adjusted.m00+axis.x;
 adjusted.m01=axis.y+adjusted.m01;
 adjusted.m02=axis.z+adjusted.m02;
 return (float)(FUN_00eb5450(&newPoint,&adjusted,&param64,&param68)*scaling-DAT_01012070);
}