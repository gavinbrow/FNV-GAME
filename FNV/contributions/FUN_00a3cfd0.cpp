struct WriteStream {
 void* data00; unsigned int position04; unsigned int unk08;
 unsigned int (__cdecl *write0c)(WriteStream*,const void*,unsigned int,unsigned int*,int);
 __forceinline void Write(const void* data) {
   unsigned int size = 4;
   position04 += write0c(this,data,4,&size,1);
 }
};
struct NiStream {
 WriteStream* GetWriter() {return *reinterpret_cast<WriteStream**>((char*)this+0x250);}
};
struct NiObject_Ext:NiObject {void FUN_00a89af0(NiStream*);};
struct FUN_00a3cfd0_shell:NiFloatData {void FUN_00a3cfd0(NiStream*);};
extern void (__cdecl *DAT_011f3a50[])(NiStream*,NiFloatKey*,unsigned int);
void FUN_00a3cfd0_shell::FUN_00a3cfd0(NiStream* stream){
 reinterpret_cast<NiObject_Ext*>(this)->FUN_00a89af0(stream);
 stream->GetWriter()->Write(&m_uiNumKeys);
 if(m_uiNumKeys>0){stream->GetWriter()->Write(&m_eType); DAT_011f3a50[m_eType](stream,m_pkKeys,m_uiNumKeys);}
}