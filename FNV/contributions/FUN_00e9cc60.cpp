struct AffineMatrix {float r00,r01,r02,r10,r11,r12,r20,r21,r22,t0,t1,t2,scale;};
struct NiPlane4 {void* vtable; NiPoint3 normal; float distance; void FUN_00e9cc60(const NiPlane4& source,const AffineMatrix& matrix);};
void NiPlane4::FUN_00e9cc60(const NiPlane4& source,const AffineMatrix& matrix){
NiPoint3 transformed; const volatile float& x=source.normal.x; const volatile float& m=matrix.r00;
transformed.x=m*x+matrix.r01*source.normal.y+matrix.r02*source.normal.z;
transformed.y=matrix.r10*source.normal.x+matrix.r11*source.normal.y+matrix.r12*source.normal.z;
transformed.z=matrix.r20*source.normal.x+matrix.r21*source.normal.y+matrix.r22*source.normal.z;
const volatile NiPoint3& t=transformed;
float translation=matrix.t0*t.x+matrix.t1*t.y+matrix.t2*t.z;
double newDistance = static_cast<volatile float&>(translation);
newDistance += matrix.scale*source.distance;
float result=(float)newDistance; normal=transformed; distance=result;}