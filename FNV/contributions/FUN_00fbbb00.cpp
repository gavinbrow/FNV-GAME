// @fnv 0x00fbbb00
// Initialize a global object (constructor parameters 0 and 1000) and register cleanup.
struct S_00c46530_Class
{
    S_00c46530_Class* FUN_00c46530(unsigned short, unsigned short);
};
extern "C" int __cdecl FUN_00ec658f(void (__cdecl*)());
extern "C" void __cdecl FUN_00fdd640();
extern "C" unsigned int DAT_01202e20;
extern "C" unsigned int DAT_010c1c54;
void __cdecl FUN_00fbbb00()
{
    unsigned int x;
    unsigned int y;
    unsigned int z;
    unsigned int w;
    reinterpret_cast<S_00c46530_Class*>(&DAT_01202e20)->FUN_00c46530(0, 1000);
    DAT_01202e20 = reinterpret_cast<unsigned int>(&DAT_010c1c54);
    FUN_00ec658f(&FUN_00fdd640);
}
