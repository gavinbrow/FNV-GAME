#include <math.h>

namespace FrustumPlanes {

struct Vector {

 float x,y,z;

 Vector(){}

 Vector(float a,float b,float c):x(a),y(b),z(c){}

 Vector operator*(float value)const{Vector result;result.x=x*value;result.y=y*value;result.z=z*value;return result;}

 Vector operator+(const Vector& value)const{Vector result;result.x=x+value.x;result.y=y+value.y;result.z=z+value.z;return result;}

 Vector operator-()const{Vector result;result.x=-x;result.y=-y;result.z=-z;return result;}

};

inline Vector multiplyVector(const Vector& v,float scalar){return v*scalar;}
struct Transform {float m00,m01,m02,m10,m11,m12,m20,m21,m22;Vector position;float scale;};

struct Frustum {float left,right,top,bottom,nearDistance,farDistance;bool orthographic;};

struct Plane {float x,y,z,d;Plane(const Vector&,const Vector&);};

struct Planes {Plane data[6];void FUN_00a74e10(const Frustum*,const Transform*);};

void Planes::FUN_00a74e10(const Frustum* f,const Transform* transform){

 Vector position=transform->position;

 Vector direction(transform->m00,transform->m10,transform->m20);

 Vector up(transform->m01,transform->m11,transform->m21);

 Vector right(transform->m02,transform->m12,transform->m22);

 Vector point=position+multiplyVector(direction,f->nearDistance);

 data[0]=Plane(direction,point);

 point=position+direction*f->farDistance;

 data[1]=Plane(-direction,point);

 if(f->orthographic){

 float leftValue=f->left;point=position+right*leftValue;data[2]=Plane(right,point);

 point=position+right*f->right;data[3]=Plane(-right,point);

 point=position+up*f->top;data[4]=Plane(-up,point);

 float bottomValue=f->bottom;point=position+up*bottomValue;data[5]=Plane(up,point);

 }else{

 float inverse=1.0f/(float)sqrt((float)(1.0+(float)(f->left*f->left)));

 float coefficient=-f->left*inverse;Vector normal=direction*coefficient+right*inverse;data[2]=Plane(normal,position);

 inverse=1.0f/(float)sqrt((float)(1.0+(float)(f->right*f->right)));

 coefficient=f->right*inverse;float opposite=-inverse;normal=direction*coefficient+right*opposite;data[3]=Plane(normal,position);

 inverse=1.0f/(float)sqrt((float)(1.0+(float)(f->top*f->top)));

 coefficient=inverse*f->top;opposite=-inverse;normal=direction*coefficient+up*opposite;data[4]=Plane(normal,position);

 inverse=1.0f/(float)sqrt((float)(1.0+(float)(f->bottom*f->bottom)));

 coefficient=-f->bottom*inverse;normal=direction*coefficient+up*inverse;data[5]=Plane(normal,position);

 }

}

}

