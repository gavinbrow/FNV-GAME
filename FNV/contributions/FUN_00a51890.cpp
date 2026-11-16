extern void* __cdecl FUN_00aa13e0(unsigned int);
extern const float DAT_01099c2c;extern int DAT_01099c34;
struct ColorInterpolatorLayout {void* volatile m_vtable;int unk04;
int unk08;
int unk0c;
int unk10;
int unk14;
int unk18;
int unk1c;
int unk20;
int unk24;
int unk28;
int unk2c;
int unk30; volatile float m_fStartValue,m_fEndValue;
void FUN_00a51ab0(int,unsigned int,int);ColorInterpolatorLayout* FUN_00a51890(NiCloningProcess&);};
ColorInterpolatorLayout* ColorInterpolatorLayout::FUN_00a51890(NiCloningProcess& process){
ColorInterpolatorLayout* __restrict result=(ColorInterpolatorLayout*)FUN_00aa13e0(0x3c);
if(result){result->FUN_00a51ab0(0,0xffff,0);result->m_vtable=&DAT_01099c34;result->m_fStartValue=DAT_01099c2c;result->m_fEndValue=DAT_01099c2c;}else result=0;
((NiBSplineColorInterpolator*)this)->FUN_00a51a60((FUN_00a50110_obj*)result,process);
result->m_fStartValue=m_fStartValue;result->m_fEndValue=m_fEndValue;return result;}