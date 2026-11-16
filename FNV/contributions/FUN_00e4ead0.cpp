struct StatisticsResult { unsigned int field0,field1,field2,field3,field4,field5,field6,field7,field8,field9,field10,total0,total1; float rate; void FUN_00e4e660(); };
__declspec(noinline) void FUN_00e4e570(const unsigned short* values, unsigned int count, StatisticsResult* result) {
 result->field7=0; result->field8=0; result->field9=0;
 for(unsigned int i=0;i<count;i++){unsigned int v=values[i]>>6;
 result->field7+=((v>>2)&1)+((v>>1)&1)+(v&1);
 result->field8+=((v>>6)&1)+((v>>5)&1)+((v>>4)&1)+((v>>3)&1);
 result->field9+=((v>>9)&1)+((v>>8)&1)+((v>>7)&1);}
}
void __cdecl FUN_00e4ead0(const unsigned short* mask, unsigned int count, StatisticsResult* result) {
 result->rate=0.0f; StatisticsResult* total=result;
 total->total0=count*10; total->total1=0;
 total->field0=0; total->field1=0; total->field2=0; total->field3=0;
 total->field4=0; total->field5=0; total->field6=0; total->field10=0;
 for(unsigned int i=0;count>i;i++){
 if (((*(mask+i))&3)==2) result->field4+=3;
 if ((0xc&(*(mask+i)))==8) result->field5+=4;
 if ((0x30&mask[i])==0x20) result->field6+=3;}
 FUN_00e4e570(mask,count,result);
 result->field0=3*count-total->field7-total->field4;
 result->field1=count*4-total->field5-total->field8;
 result->field2=count*3-total->field9-result->field6;
 if(total->field9+(total->field7+total->field8)>0)
 total->rate=(float)result->total0/(float)(total->field9+(total->field7+total->field8));
 else result->rate=0.0f;
}