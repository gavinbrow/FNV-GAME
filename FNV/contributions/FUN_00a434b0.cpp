struct TrackFlags { unsigned char value; };
struct SampleTrack { unsigned int unk00; unsigned int unk04; unsigned int count; float* times; float* values; TrackFlags flags; };
float __cdecl FUN_00a26b40(float, float*, float*, unsigned int, unsigned int*, TrackFlags);
struct FUN_00a434b0_shell { unsigned int unk00; unsigned int unk04; float previousTime; unsigned int unk0c; unsigned int unk10; float previousValue; float valueDelta; unsigned int sampleIndex; SampleTrack* track; bool __thiscall FUN_00a434b0(float time, int, int); };
bool __thiscall FUN_00a434b0_shell::FUN_00a434b0(float time, int, int) {
 SampleTrack* t=track;
unsigned int count=t->count; float* values=t->values; TrackFlags flags=t->flags; float* times=t->times;
 if(count>0) {
    unsigned int index=sampleIndex;
    float value=FUN_00a26b40(time,times,values,count,&index,flags);
    sampleIndex=index;
    if(previousTime>time && previousValue>value) {
      valueDelta=(1.0f-previousValue)+value;
    } else { valueDelta=value-previousValue; }
    previousValue=value;
 }
 previousTime=time;
 return true;
}