unsigned int gm_GetCurrentThreadId();
void FUN_0040fca0(unsigned long);
struct OSGlobals { unsigned int FUN_0044edb0(); };
extern OSGlobals* g_osGlobals;
struct TES { void FUN_00452490(int); bool FUN_00453a80(); void FUN_004539a0(int,int); };
extern TES* g_TES;
extern unsigned int DAT_011de70c;
struct ScrapHeapManager { static ScrapHeapManager& Instance(); void FUN_00aa5c80(); };
struct Worker { bool FUN_00529ea0(); void FUN_00650a30(int); };
Worker* FUN_00652110(); bool FUN_00652160(); int FUN_00652130(); void FUN_00652190();
void FUN_00869190(int); void FUN_00868d70(int); void FUN_00c459d0(int); void FUN_00aa7030();
struct BSSpinLock { bool FUN_0078d200(); void FUN_0040fba0(); };
extern BSSpinLock DAT_011f11a0;
struct IOManager { unsigned int FUN_00866da0(int);void FUN_00866dc0(int);void FUN_00866de0(int); };
extern IOManager* DAT_01202d98;
struct StateMachine {
 int unknown000;
 int unknown004;
 int unknown008;
 int unknown00c;
 int unknown010;
 int unknown014;
 int unknown018;
 int unknown01c;
 int unknown020;
 int unknown024;
 int unknown028;
 int unknown02c;
 int unknown030;
 int unknown034;
 int unknown038;
 int unknown03c;
 int unknown040;
 int unknown044;
 int unknown048;
 int unknown04c;
 int unknown050;
 int unknown054;
 int unknown058;
 int unknown05c;
 int unknown060;
 int unknown064;
 int unknown068;
 int unknown06c;
 int unknown070;
 int unknown074;
 int unknown078;
 int unknown07c;
 int unknown080;
 int unknown084;
 int unknown088;
 int unknown08c;
 int unknown090;
 int unknown094;
 int unknown098;
 int unknown09c;
 int unknown0a0;
 int unknown0a4;
 int unknown0a8;
 int unknown0ac;
 int unknown0b0;
 int unknown0b4;
 int unknown0b8;
 int unknown0bc;
 int unknown0c0;
 int unknown0c4;
 int unknown0c8;
 int unknown0cc;
 int unknown0d0;
 int unknown0d4;
 int unknown0d8;
 int unknown0dc;
 int unknown0e0;
 int unknown0e4;
 int unknown0e8;
 int unknown0ec;
 int unknown0f0;
 int unknown0f4;
 int unknown0f8;
 int unknown0fc;
 int unknown100;
 int unknown104;
 int unknown108;
 int unknown10c;
 int unknown110;
 int unknown114;
 int unknown118;
 int unknown11c;
 int unknown120;
 int unknown124;
 int unknown128;
 int unknown12c;
 int unknown130;
 int state;
 int FUN_00866a90(void*,unsigned int,bool*);
};
int StateMachine::FUN_00866a90(void* context,unsigned int step,bool* finished) {
 *finished=true;
 bool mainThread=gm_GetCurrentThreadId()==g_osGlobals->FUN_0044edb0();
 switch(step) {
 case 0:
  DAT_011de70c=0;
  if(mainThread)g_TES->FUN_00452490(0);
  break;
 case 1:
  ScrapHeapManager::Instance().FUN_00aa5c80();
  break;
 case 2:
  if(FUN_00652110() && FUN_00652110()->FUN_00529ea0() && FUN_00652160()) {
   if(FUN_00652130()==1)FUN_00652110()->FUN_00650a30(0);
   FUN_00652190();
  }
  break;
 case 5:
  if(mainThread) {
   FUN_00869190(0);
   if(g_TES->FUN_00453a80())step=step-1;
   else g_TES->FUN_004539a0(1,0);
   g_TES->FUN_00452490(0);
   FUN_00869190(1);
   FUN_00868d70(1);
  } else break;
 case 4:
  if(DAT_011f11a0.FUN_0078d200()) {
   FUN_00868d70(1);
   DAT_011f11a0.FUN_0040fba0();
  }
 case 3:
  FUN_00c459d0(1);
  break;
 case 6:
  if(mainThread)FUN_00aa7030();
  break;
 case 7:
  if(!*finished && mainThread){*finished=true;break;}
 case 8:
  if(!mainThread) {
   state=6;
   if(DAT_011de70c<15000) {
    if(DAT_01202d98->FUN_00866da0(0)==gm_GetCurrentThreadId()) {DAT_01202d98->FUN_00866dc0(0);DAT_01202d98->FUN_00866de0(0);}
    if(DAT_01202d98->FUN_00866da0(1)==gm_GetCurrentThreadId()) {DAT_01202d98->FUN_00866dc0(1);DAT_01202d98->FUN_00866de0(1);}
    FUN_0040fca0(1);
    DAT_011de70c=DAT_011de70c+1;
    step=step-1;
    break;
   } else if(!*finished)*finished=true;
  }
  break;
 }
 return step+1;
}
