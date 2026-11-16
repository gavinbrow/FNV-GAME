void *__cdecl FUN_00aa1070(unsigned int size);
struct A472Input {
    int unk00;
    int position;
    unsigned int (__cdecl* read)(A472Input*,unsigned char*,unsigned int,unsigned int*,unsigned int);
    __forceinline void Read(void* data,unsigned int byteCount,unsigned int componentSize) {
        unsigned int elementSize=componentSize;
        position+=read(this,(unsigned char*)data,byteCount,&elementSize,1);
    }
};
struct A472Stream {
    char unk00[0x24c];
    A472Input* input;
};
class FUN_00a472b0_cls {
public:
    int unk00,unk04;
    void* m_pBuf08;
    unsigned int m_uiCount0C,m_uiExtra10;
    void FUN_00a5d610(A472Stream* stream);
    void FUN_00a472b0(A472Stream* stream);
};
void FUN_00a472b0_cls::FUN_00a472b0(A472Stream* stream) {
   FUN_00a5d610(stream);
   stream->input->Read(&m_uiCount0C,4,4);
   if(m_uiCount0C>0) {
      m_pBuf08=FUN_00aa1070(m_uiCount0C);
      stream->input->Read(m_pBuf08,m_uiCount0C,1);
   }
   stream->input->Read(&m_uiExtra10,4,4);
}