extern "C" void __cdecl Deallocate(void*);
inline Random::~Random() {}
struct FUN_00b436b0 : Random {
 float xi;
 float* sx;
 float* sfx;
 bool NotReady;
 virtual ~FUN_00b436b0();
};
FUN_00b436b0::~FUN_00b436b0()
{
    if (!NotReady) {
        float* bufferA = sx;
        Deallocate(bufferA);
        float* bufferB = sfx;
        Deallocate(bufferB);
    }
}