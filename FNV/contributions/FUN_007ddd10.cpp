struct TraitSI { float FUN_00a011b0(); };
struct DisplaySI { void FUN_00a012d0(int, float, bool); };
struct ActivitySI { virtual void v0(); virtual void v1(); virtual void v2(); virtual float v3(int); };
extern ActivitySI* g_011dea3c;
extern double g_01017b70,g_01011590,g_0101ff40,g_01064f50,g_01012060,g_01012070;
extern double __cdecl FUN_005c5420();
extern float __cdecl FUN_00404010(float,float);
extern float __cdecl FUN_004bd510(float,float);
struct StatsMenuSI { void* unk00; DisplaySI* unk04; TraitSI* FUN_00726070(int); void FUN_007ddd10(); };
void StatsMenuSI::FUN_007ddd10() {
    float scale;
    
    float adjustment;
    float currentValue;
    float unusedResult;
    scale=FUN_00726070(0x1008)->FUN_00a011b0()*g_01017b70;
    adjustment=(-scale/g_01011590)+(FUN_005c5420()*scale);
    currentValue=FUN_00404010(0.0f,(reinterpret_cast<ActivitySI*>(reinterpret_cast<char*>(g_011dea3c)+0xa4))->v3(0x4a));
    unusedResult=g_01064f50-(currentValue+adjustment)/g_01017b70*g_0101ff40;
    if(currentValue>g_01012060 && currentValue<g_01012070) currentValue=1.0f;
    else currentValue=FUN_004bd510(currentValue,1.0f);
    unk04->FUN_00a012d0(0x1010,currentValue,true);
}