struct HalfSpace {void* vtable;float nx;volatile float ny;float nz;float d;};struct Sphere{void* vtable;float cx,cy,cz,r;};struct Vec3{float x,y,z;};
bool __cdecl FUN_00e9cd10(float t, HalfSpace* plane, Vec3* v0,Sphere* sphere,Vec3* v1){
float dot=sphere->cy*plane->ny+sphere->cx*plane->nx+sphere->cz*plane->nz;
float distance=dot-plane->d;float radius=-sphere->r;if(distance>=radius)return true;
Vec3 relative;relative.x=v1->x-v0->x;relative.y=v1->y-v0->y;relative.z=v1->z-v0->z;
float speed=plane->ny*relative.y+relative.x*plane->nx+plane->nz*relative.z;
if(speed<=0.0f)return false;return distance+speed*t>=radius;}