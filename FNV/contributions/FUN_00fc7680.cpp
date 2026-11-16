struct Pt3;

class ProjectionQuery
{
public:
    void InitFromParams(float value, const Pt3* point);
};

extern ProjectionQuery DAT_0126fa68;
extern const Pt3 DAT_011f426c;
extern void __cdecl FUN_00fde3c0();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00fc7680
void __cdecl FUN_00fc7680()
{
    DAT_0126fa68.InitFromParams(1.0f, &DAT_011f426c);
    atexit(FUN_00fde3c0);
}
