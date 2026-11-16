struct S00ac5490_Str { void FUN_0044a730(int, int); };
extern S00ac5490_Str DAT_011f8ba4;
extern "C" int __cdecl FUN_00ec658f(void (__cdecl *)());
extern "C" void __cdecl FUN_00fdc490();

struct StringInitContext {
    unsigned int state0;
    unsigned int state1;
    unsigned int state2;
    unsigned int state3;
    unsigned int state4;
    unsigned int allocatorStorage;
    char *allocatorPointer;
    unsigned int registrationState;
};
// @fnv 0x00fb8790
void FUN_00fb8790()
{
    StringInitContext context;
    context.allocatorPointer = reinterpret_cast<char*>(&context.allocatorStorage) + 3;
    DAT_011f8ba4.FUN_0044a730(0, 0);
    FUN_00ec658f(&FUN_00fdc490);
}