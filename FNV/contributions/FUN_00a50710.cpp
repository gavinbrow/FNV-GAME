struct Point3 {
 float x,y,z;
 Point3() {}
 Point3(float px,float py,float pz) : x(px), y(py), z(pz) {}
};
struct BSplineData { void __thiscall FUN_00a52550(float time, float* output, int components, int offset, int handle); };
struct FUN_00a50710_shell {
 void* vtable; int unk04; float lastTime; float startTime; float endTime;
 BSplineData* data; int dataOffset; Point3 lastValue; unsigned int handle;
 bool __thiscall FUN_00a50710(float time, int unk, Point3* output);
};
bool FUN_00a50710_shell::FUN_00a50710(float time, int unk, Point3* output) {
 if (lastTime == time) { *output = lastValue; return true; }
 if (handle != 0xffff) {
   float sample[3];
   data->FUN_00a52550((time - startTime)/(endTime-startTime), sample, 3, dataOffset, handle);
   Point3 value(sample[0],sample[1],sample[2]);
   lastValue = value;
 }
 *output = lastValue; lastTime = time; return true;
}