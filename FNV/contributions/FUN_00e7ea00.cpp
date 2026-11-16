
extern int DAT_011bf558;
extern int DAT_0126f6c0;
extern int DAT_0126f6c4;
extern int DAT_0126f6c8;
extern int DAT_011a9608;
struct PassState {
    int status;
    unsigned int handle;
    void* texture;
    int reserved;
    Holder_00e89060* holder;
    void FUN_00e7dc90(void* item);
    void FUN_00e7e940();
    void FUN_00e7ea00();
};
typedef void (__thiscall* DeviceStageFn)(void*,unsigned int,int,void*,int);
typedef void (__thiscall* DeviceStateFn)(void*,unsigned int,int);
typedef void (__thiscall* DeviceDisableFn)(void*,unsigned int,int,int,int);
typedef int (__thiscall* ObjectQueryFn)(void*,void*,char*,char*,int*);
typedef void (__stdcall* DeviceFinishFn)(void*,unsigned int,int,int);
void PassState::FUN_00e7ea00() {
    union { bool needsStage; char byteA; };
    if (handle < (unsigned int)DAT_011bf558) {
        void* replacement = 0;
        needsStage = false;
        bool valid = holder->FUN_00e89060(11,replacement,needsStage);
        void* chosen = valid ? replacement : (void*)handle;
        void* d = (void*)DAT_0126f6c8;
        ((DeviceStageFn)(*(void***)d)[48])(d,handle,11,chosen,0);
    }
    int queryResult=0;
    char byteB;
    int resultInfo;
    if (texture) {
        void* service = ((void**)DAT_0126f6c4)[0x8c4/4];
        queryResult = ((ObjectQueryFn)(*(void***)service)[3])(service,texture,&byteA,&byteB,&resultInfo);
    }
    {
       void* d = (void*)DAT_0126f6c8;
       ((DeviceStateFn)(*(void***)d)[55])(d,handle,queryResult);
    }
    if(queryResult) {
        if(!byteB) {
            void* d = (void*)DAT_0126f6c8;
            ((DeviceDisableFn)(*(void***)d)[51])(d,handle,7,0,0);
        }
        FUN_00e7dc90((void*)resultInfo);
        FUN_00e7e940();
    }
    if(status == 6) {
        void* output = (void*)DAT_0126f6c0;
        ((DeviceFinishFn)(*(void***)output)[69])(output,handle,10,DAT_011a9608);
    }
}