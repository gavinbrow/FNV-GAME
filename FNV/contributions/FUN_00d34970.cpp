extern float DAT_0104da48;
extern unsigned char DAT_010ce7fc;
struct D34970Context {
    void* pointer;
    float maxDistance;
    int option;
};
extern "C" void __cdecl FUN_00d339d0(int first, int second, int third, D34970Context* context);
void __cdecl FUN_00d34970(int arg0, int arg1, int arg2, int arg3) {
    D34970Context context;
    context.pointer = &DAT_010ce7fc;
    context.maxDistance = DAT_0104da48;
    context.option = arg3;
    FUN_00d339d0(arg1, arg0, arg2, &context);
}