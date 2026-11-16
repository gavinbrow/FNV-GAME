struct CFCA90Shape {int m_type,m_flags,m_state,m_reference; signed char m_subshapeOffset;};
struct CFCA90Range {char* m_end;};
struct CFCA90Object;
struct CFCA90Work {CFCA90Shape* m_firstShape;CFCA90Shape* m_secondShape;int m_flags;CFCA90Range* m_range;int m_scratchIndices[256];CFCA90Object* m_owner;};
void __cdecl FUN_00d019b0(void*,void*);
void __cdecl FUN_00d00270(void*,void*);
struct CFCA90Object {int m_type,m_state,m_flags;void* m_controller;int m_owner,m_detail;unsigned short m_remainingCount,m_padding;
void FUN_00cfca90(CFCA90Shape*,CFCA90Shape*,void*,CFCA90Range*);};
void CFCA90Object::FUN_00cfca90(CFCA90Shape* shapeA,CFCA90Shape* shapeB,void* unusedInput,CFCA90Range* range) {
 if(m_remainingCount-- !=0)return;
 char* partA=(char*)shapeA+shapeA->m_subshapeOffset;
 char* partB=(char*)shapeB+shapeB->m_subshapeOffset;
 unsigned short countB=*(unsigned short*)(partB+0xaa);
 unsigned short countA=*(unsigned short*)(partA+0xaa);
 unsigned short nextCount=countA<countB ? countA:countB;
 CFCA90Work work;
 work.m_firstShape=shapeA;work.m_secondShape=shapeB;work.m_range=range;
 m_remainingCount=nextCount;
 int entries=(int)(range->m_end-((char*)range+16))/48;
 work.m_owner=this;
 for(int i=entries-1;i>=0;--i)work.m_scratchIndices[i]=0;
 FUN_00d019b0(m_controller,&work);
 if(*(unsigned short*)(partA+0x204))FUN_00d00270(partA,&work);
 if(*(unsigned short*)(partB+0x204))FUN_00d00270(partB,&work);
}