struct NiBoundingVolume {
    virtual ~NiBoundingVolume();
};

struct NiHalfSpaceBV : NiBoundingVolume {
    void SetPlane();
};

struct NiStream;
struct NiSphere { void SaveBinary(NiStream&); };
struct NiColor { void SaveBinary(NiStream&); };
struct NiBoundingVolume_SaveHelper { void SaveBinary(NiStream&); };
struct FUN_00e9cb80_Holder { void FUN_00e9cb80(NiStream&); };
struct Q
{
    bool FUN_00a92660(const Q&) const;
};
struct BVProxy
{
    virtual void _f0();
    virtual void _f1();
    virtual void _f2();
    virtual int _f3() const;
};
struct Holder00e9cc20
{
    int FUN_00e9cc20(const NiBoundingVolume&) const;
};
struct NiPoint3 { float x; float y; float z; };
extern NiPoint3 DAT_011a9478;
extern NiPoint3 DAT_011f426c;
extern NiPoint3 _NiPoint3_ZERO;

struct P03MM { void* Allocate(unsigned int); };
extern P03MM g_memoryManager;

struct FUN_00e9e700_Helper {
    NiBoundingVolume* FUN_00e9e680(const NiPoint3&, const NiPoint3&);
};

NiBoundingVolume* FUN_00e9e700();

struct D_00e9e980
{
    char _00[8];
    void** m_pp;
    char _0C[2];
    unsigned short m_cnt;
    char _10[4];
    int m_found;
};

struct FUN_00e9e780_Virtual
{
    virtual void Call(void* p);
};

NiBoundingVolume* __cdecl FUN_00e9e780(void* p)
{
    FUN_00e9e700_Helper* helper =
        static_cast<FUN_00e9e700_Helper*>(g_memoryManager.Allocate(0x20));

    NiBoundingVolume* result;

    if (helper)
        result = helper->FUN_00e9e680(DAT_011f426c, DAT_011a9478);
    else
        result = 0;

    reinterpret_cast<FUN_00e9e780_Virtual*>(result)->Call(p);
    return result;
}