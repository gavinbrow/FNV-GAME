#include "h_9317cf800937.h"
typedef void (__cdecl *NiBoolSaveKeysFunction)(NiStream&, NiBoolKey*, unsigned int);
extern "C" NiBoolSaveKeysFunction DAT_011f3ac8[NiAnimationKey::NUMKEYTYPES];
struct NiBinaryWriter {
 void* m_vtable;
 unsigned int m_uiAbsoluteCurrentPos;
 void* m_pfnRead;
 unsigned int (__cdecl *m_pfnWrite)(NiBinaryWriter*,const void*,unsigned int,unsigned int*,unsigned int);
template<class T> inline void BinaryWrite(const T& value) { 
 unsigned int size=sizeof(T);
 m_uiAbsoluteCurrentPos += m_pfnWrite(this,&value,size,&size,1);
 }
};
template<class T> inline void WriteValue(NiStream& stream,const T& value) {
 reinterpret_cast<NiBinaryWriter*>(stream.m_pkOstr)->BinaryWrite(value);
}struct NiBoolDataSaver {
 void* m_vtable; unsigned int m_uiRefCount; unsigned int m_uiNumKeys; NiBoolKey* m_pkKeys;
 NiAnimationKey::KeyType m_eType; unsigned char m_ucKeySize;
 void FUN_00a89af0(NiStream&); void FUN_00a53b20(NiStream&);
};
void NiBoolDataSaver::FUN_00a53b20(NiStream& stream){
 FUN_00a89af0(stream);
 WriteValue(stream,m_uiNumKeys);
 if(m_uiNumKeys>0){WriteValue(stream,m_eType);DAT_011f3ac8[m_eType](stream,m_pkKeys,m_uiNumKeys);}
}