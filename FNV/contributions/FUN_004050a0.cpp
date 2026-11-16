struct MapAccess{void* FUN_004b9ba0();void FUN_006b7f20(void** position,int* key,void** value);};
struct EffectProcess {
virtual void unknown00()=0;virtual void unknown04()=0;virtual void unknown08()=0;
virtual void unknown0c()=0;virtual bool ProcessEffect(void* effect)=0;
bool FUN_00404d30();bool FUN_004050a0();};
bool EffectProcess::FUN_004050a0(){
bool result=FUN_00404d30();
if(result){
    int key;
    {
        void* position=((MapAccess*)((char*)this+0x10c))->FUN_004b9ba0();
        while(position!=0){
            void* effect;
            ((MapAccess*)((char*)this+0x10c))->FUN_006b7f20(&position,&key,&effect);
            if(effect!=0) result &= ProcessEffect(effect);
        }
    }
}
return result;
}