extern const float DAT_010986e8;
extern const float DAT_01015f5c;
struct KeyTrackData { float m_00; int unk04,unk08,unk0c,unk10,m_14,m_18,m_1c,unk20,unk24,unk28; unsigned char m_2c,m_2d,m_2e; float* m_30; float* m_34; float* m_38; };
struct KeyDesc { int unk00,unk04; unsigned int m_08; KeyTrackData* m_0c; volatile int m_10; unsigned char m_14; };
struct FUN_00a48ac0_cls { int unk00,unk04,unk08,unk0c,unk10,unk14,unk18; KeyDesc* m_1c; void FUN_00a48ac0(float*,float*); };
void FUN_00a48ac0_cls::FUN_00a48ac0(float* outLo,float* outHi) {
KeyDesc* p=m_1c;
if (p) {
unsigned int count=p->m_08; int type=p->m_10; unsigned char stride=p->m_14; KeyTrackData* base=p->m_0c;
if(count>0) {
if(type==4) {
float temp;float lo=DAT_010986e8;float hi=DAT_01015f5c;
unsigned char* ps=&base->m_2c; float** pk=&base->m_30;
int n=3;
do {
float* key=*pk;
temp=key[0];int cnt=*(int*)((char*)pk-0x1c); unsigned char s=*ps;if(temp<lo)lo=temp;temp=*(float*)((char*)key+(cnt-1)*s);if(temp>hi)hi=temp;
pk++;ps++;
} while (--n);
*outLo=lo; *outHi=hi;return;
}
*outLo=base->m_00; *outHi=*(float*)((char*)base+(count-1)*stride);return;
}
}
*outLo=0.0f;*outHi=0.0f;
}