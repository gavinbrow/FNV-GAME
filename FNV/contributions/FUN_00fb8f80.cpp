// @fnv 0x00fb8f80
// Cache startup state. Only the two constructor argument objects
// are identified; the preceding unreferenced frame fields remain unknown.
struct lessS {};
struct ValT {};
template <typename Value> struct TreeAllocator {};

struct CacheConstructionFrame
{
    unsigned int unknown00;
    unsigned int unknown04;
    unsigned int unknown08;
    unsigned int unknown0c;
    unsigned int unknown10;
    unsigned int unknown14;
    unsigned int unknown18;
    unsigned int unknown1c;
    unsigned int unknown20;
    unsigned int unknown24;
    unsigned char unknown28;
    unsigned char unknown29;
    lessS comparison;
    TreeAllocator<ValT> allocator;
};
struct S00b37660_Cache
{
    void FUN_00b3b770(const lessS& comparison, const TreeAllocator<ValT>& allocator);
};
extern "C" S00b37660_Cache DAT_011f8e2c;
extern "C" void FUN_00fdc690();
extern "C" int __cdecl atexit(void (__cdecl *function)());

void FUN_00fb8f80()
{
    CacheConstructionFrame frame;
    DAT_011f8e2c.FUN_00b3b770(frame.comparison, frame.allocator);
    atexit(&FUN_00fdc690);
}
