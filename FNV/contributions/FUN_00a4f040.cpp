extern int DAT_0109928c;
extern int EmptyFS;
extern "C" __declspec(dllimport) void __stdcall CoTaskMemFree(void*);
struct BaseController { void FUN_00a572d0(); };
struct MyController : BaseController {
    void* volatile vtable;
    unsigned int field04;
    unsigned int field08;
    unsigned int field0c;
    unsigned int field10;
    unsigned int field14;
    unsigned int field18;
    unsigned int field1c;
    unsigned int field20;
    unsigned int field24;
    unsigned int field28;
    unsigned int field2c;
    unsigned int field30;
    unsigned int field34;
    unsigned int field38;
    unsigned int field3c;
    unsigned int field40;
    unsigned char* volatile sharedStorage;
    MyController* FUN_00a4f040(unsigned int destroyFlag);
};
void __cdecl FUN_00aa1460(void*, unsigned int);
MyController* MyController::FUN_00a4f040(unsigned int destroyFlag) {
    this->vtable = &DAT_0109928c;
    unsigned char* storage = this->sharedStorage;
    if (storage != (unsigned char*)EmptyFS) {
        CoTaskMemFree(storage - 8);
    }
    this->FUN_00a572d0();
    if ((destroyFlag & 1) != 0) {
        FUN_00aa1460(this, sizeof(*this));
    }
    return this;
}