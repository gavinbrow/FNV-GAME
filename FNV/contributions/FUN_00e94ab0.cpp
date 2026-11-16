void* __cdecl NiMalloc(unsigned int size);
void* __cdecl _fnv_zlib_memset(void* dest, int value, unsigned int size);

struct GeometryBase { virtual void slot();
    unsigned int unk04;
    unsigned int unk08;
    GeometryBase();
};
struct GeometryMap {
    int* table;
    unsigned int bucketCount;
    void* buckets;
    unsigned int itemCount;
    GeometryMap() {
        table = &DAT_010f0f94;
        bucketCount = 37;
        itemCount = 0;
        buckets = NiMalloc(148);
        _fnv_zlib_memset(buckets, 0, bucketCount * 4);
        table = &DAT_010f0fb4;
    }
};
struct FUN_00e94ab0 : GeometryBase { virtual void slot();
    GeometryMap map;
    FUN_00e94ab0();
};
FUN_00e94ab0::FUN_00e94ab0()
{

}


