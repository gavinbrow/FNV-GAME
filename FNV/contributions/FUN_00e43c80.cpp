
struct E43Arg { char data[0xb4]; float value; };
struct E43Result {float m_value,m_scale;float* m_outputValues;unsigned char m_byte12,m_byte13,m_byte14,m_byte15;};
struct StatusResult {unsigned char value;};
struct FUN_00e43c80_s {
 virtual void v0()=0; virtual void v1()=0; virtual void v2()=0; virtual void v3()=0;
 virtual float m_scale_value(E43Arg*,E43Result*)=0;
 virtual float m_primary_value(E43Arg*,E43Result*)=0;
 virtual StatusResult m_compute_status(E43Arg*,E43Result*)=0;
 virtual void m_finalize(float,E43Arg*,E43Result*)=0;
 float unk04,unk08,unk0c,unk10,unk14,unk18,unk1c,unk20,unk24;
 float* unk28;
 int unk2c;
 void FUN_00e43c80(float timeValue,E43Arg* pInput,E43Result* pOutput);
};
void FUN_00e43c80_s::FUN_00e43c80(float timeValue,E43Arg* pInput,E43Result* pOutput) {
 pOutput->m_byte13 = m_compute_status(pInput,pOutput).value;
 pOutput->m_scale=m_scale_value(pInput,pOutput);
 pOutput->m_value=m_primary_value(pInput,pOutput);
 for(int i=0;i<unk2c;++i) {
   float temp=unk28[i] * pOutput->m_scale;
   pOutput->m_outputValues[i]=temp;
 }
 m_finalize(timeValue,pInput,pOutput);
}
