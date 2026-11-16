extern "C" int DAT_01268748;
extern "C" const char* __cdecl FUN_00cf6170(void** value, void* object);
extern "C" void __cdecl FUN_00cf6920(void* owner, void* object, void* context);
struct FunctionContext {
    void __thiscall FUN_00c90360(void* context, void* object);
};
void __thiscall FunctionContext::FUN_00c90360(void* context, void* object) {
    void* const cachedObject = object;
    if (cachedObject != 0 && cachedObject != &DAT_01268748) {
        void* pointer;
        if (*FUN_00cf6170(&pointer, cachedObject)) {
            FUN_00cf6920(this, cachedObject, context);
        }
    }
}