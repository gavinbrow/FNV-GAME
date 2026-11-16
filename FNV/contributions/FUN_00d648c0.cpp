struct AudioAllocator { virtual void v00(); virtual void v04(); virtual void v08(); virtual void v0C(); virtual void FreeArray(void*, unsigned int) throw(); };
struct AudioHolder { int unk00,unk04,unk08,unk0c; AudioAllocator* m_pAllocator; };
struct BSAudio; BSAudio* __cdecl FUN_00c85750();
extern int DAT_010d1918, DAT_010d18f8, DAT_010d18e8, DAT_010d18cc, DAT_010d18bc, DAT_010ccf7c;
struct AudioArray {
 void* m_pData; int m_iCount; unsigned int m_uCapBits;
 void Reset() { m_pData = 0; m_uCapBits = 0x80000000u; }
};
struct SweptViewer {
 int m_vptr00, unk04, m_vptr08, unk0c, unk10, unk14, unk18, unk1c, m_vptr20, m_vptr24, m_vptr28, m_vptr2c;
 AudioArray m_array;
 void FUN_00d64800(int); void FUN_00ddcc60_tail(); void FUN_00d648c0();
};
void SweptViewer::FUN_00d648c0() {
 m_vptr00=(int)&DAT_010d1918; m_vptr08=(int)&DAT_010d18f8;
 m_vptr20=(int)&DAT_010d18e8; m_vptr28=(int)&DAT_010d18cc; m_vptr2c=(int)&DAT_010d18bc;
 int i=m_array.m_iCount-1; if(i>=0) { do{ FUN_00d64800(i); --i; }while(i>=0); }
 AudioHolder* h=(AudioHolder*)FUN_00c85750(); AudioAllocator* a=h->m_pAllocator;
 m_array.m_iCount=0;
 unsigned int cap=m_array.m_uCapBits;
 if((cap&0x80000000u)==0) a->FreeArray(m_array.m_pData,(cap&0x3fffffffu)*4);
 m_array.Reset();
 m_vptr2c=(int)&DAT_010ccf7c;
 m_vptr28=(int)"pFU";
 return FUN_00ddcc60_tail();
}