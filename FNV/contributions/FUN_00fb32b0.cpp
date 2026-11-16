// @fnv 0x00fb32b0
// Initialize a global setting and register its destruction at process exit.
struct FUN_00a0d710_class
{
    FUN_00a0d710_class* FUN_00a0d710(unsigned int);
};
extern "C" int __cdecl FUN_00ec658f(void (__cdecl*)());
extern "C" void __cdecl FUN_00fda020();
extern "C" unsigned int DAT_011f3308;
extern "C" unsigned int DAT_01094e3c;
void __cdecl FUN_00fb32b0()
{
    unsigned int x;
    unsigned int y;
    unsigned int z;
    reinterpret_cast<FUN_00a0d710_class*>(&DAT_011f3308)->FUN_00a0d710(0x25);
    *reinterpret_cast<unsigned int*>(&DAT_011f3308) = reinterpret_cast<unsigned int>(&DAT_01094e3c);
    FUN_00ec658f(&FUN_00fda020);
}
