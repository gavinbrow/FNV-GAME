struct SkyState{bool FUN_0059ea80();};
SkyState* __cdecl FUN_0046dd00();
extern __declspec(thread) unsigned char tlsBytes[];
extern const char str_010351ec[];
void __cdecl FUN_00703c00(const char*, double);
bool __cdecl FUN_0059ea10(int first,int second,int third,double* output){
 SkyState* sky=FUN_0046dd00();
 *output = sky->FUN_0059ea80()?1.0f:0.0f;
 if(tlsBytes[0x268])FUN_00703c00(str_010351ec,*output);
 return true;
}