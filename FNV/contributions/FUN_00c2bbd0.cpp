extern void (__cdecl *DAT_011f38a0[])(void*);
extern unsigned char DAT_011f3758[];
struct AnimationKeyTrack {
 void* vtable; void* controller; void* animatedTarget; void* nextTrack;
 unsigned int startFrame; unsigned int endFrame; unsigned int m_uiNumKeys;
 void* m_pkKeys; int m_eType; unsigned char m_ucKeySize;
 void FUN_00c2bbd0(void* keys, unsigned int numKeys, int type);
};
void AnimationKeyTrack::FUN_00c2bbd0(void* keys,unsigned int numKeys,int type){
if(m_pkKeys) DAT_011f38a0[m_eType](m_pkKeys);
if(keys && numKeys){unsigned char size=DAT_011f3758[type+30];m_ucKeySize=size;m_pkKeys=keys;m_uiNumKeys=numKeys;m_eType=type;}
else{m_uiNumKeys=0;m_pkKeys=0;m_ucKeySize=0;}
}