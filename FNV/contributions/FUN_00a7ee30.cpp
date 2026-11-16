struct Vec88 {

 float x,y,z;

 Vec88() {}

 Vec88(float a,float b,float c):x(a),y(b),z(c) {}

 Vec88 operator+(const Vec88& v) const { return Vec88(x+v.x,y+v.y,z+v.z); }

 Vec88 operator-(const Vec88& v) const { return Vec88(x-v.x,y-v.y,z-v.z); }

 Vec88 operator*(float f) const { return Vec88(x*f,y*f,z*f); }

 float LengthSquared() const { return x*x+y*y+z*z; }

};

extern Vec88 DAT_011f426c;

extern "C" double __cdecl sqrt(double);

struct Bound88 {

 Vec88 center; float radius;

 void FUN_00a7ee30(int count,const Vec88* points);

};

void Bound88::FUN_00a7ee30(int count,const Vec88* points) {

 if(count <= 0) { center=DAT_011f426c; radius=0; return; }

 Vec88 minimum=points[0];

 Vec88 maximum=points[0];

 int maxSquared=1;
 if(count-1>=4) {
  unsigned int groups = ((unsigned int)(count-5)>>2)+1;
  const float* cursor=&points[1].z;
  maxSquared = groups*4+1;
  do {
 

  if(minimum.x>cursor[-2]) minimum.x=cursor[-2];

  if(minimum.y>cursor[-1]) minimum.y=cursor[-1];

  if(minimum.z>cursor[0]) minimum.z=cursor[0];

  if(maximum.x<cursor[-2]) maximum.x=cursor[-2];

  if(maximum.y<cursor[-1]) maximum.y=cursor[-1];

  if(maximum.z<cursor[0]) maximum.z=cursor[0];


  if(minimum.x>cursor[1]) minimum.x=cursor[1];

  if(minimum.y>cursor[2]) minimum.y=cursor[2];

  if(minimum.z>cursor[3]) minimum.z=cursor[3];

  if(maximum.x<cursor[1]) maximum.x=cursor[1];

  if(maximum.y<cursor[2]) maximum.y=cursor[2];

  if(maximum.z<cursor[3]) maximum.z=cursor[3];


  if(minimum.x>cursor[4]) minimum.x=cursor[4];

  if(minimum.y>cursor[5]) minimum.y=cursor[5];

  if(minimum.z>cursor[6]) minimum.z=cursor[6];

  if(maximum.x<cursor[4]) maximum.x=cursor[4];

  if(maximum.y<cursor[5]) maximum.y=cursor[5];

  if(maximum.z<cursor[6]) maximum.z=cursor[6];


  if(minimum.x>cursor[7]) minimum.x=cursor[7];

  if(minimum.y>cursor[8]) minimum.y=cursor[8];

  if(minimum.z>cursor[9]) minimum.z=cursor[9];

  if(maximum.x<cursor[7]) maximum.x=cursor[7];

  if(maximum.y<cursor[8]) maximum.y=cursor[8];

  if(maximum.z<cursor[9]) maximum.z=cursor[9];
   cursor+=12;
  } while(--groups);
 }
 if(maxSquared<count) {
  const float* tailCursor=&points[maxSquared].z;
  int remaining=count-maxSquared;
  do {
 

  if(minimum.x>tailCursor[-2]) minimum.x=tailCursor[-2];

  if(minimum.y>tailCursor[-1]) minimum.y=tailCursor[-1];

  if(minimum.z>tailCursor[0]) minimum.z=tailCursor[0];

  if(maximum.x<tailCursor[-2]) maximum.x=tailCursor[-2];

  if(maximum.y<tailCursor[-1]) maximum.y=tailCursor[-1];

  if(maximum.z<tailCursor[0]) maximum.z=tailCursor[0];
   tailCursor+=3;
  }while(--remaining);
 }
 center=(minimum + maximum)*0.5f;

 float delta=0.0f;

 for(maxSquared=0;maxSquared<count;maxSquared++) {

  Vec88 i=points[maxSquared]-center;

  float squared=i.LengthSquared();

  if(squared > delta) delta=squared;

 }

 volatile float rounding = (float)sqrt(delta);
 radius=rounding;

}

