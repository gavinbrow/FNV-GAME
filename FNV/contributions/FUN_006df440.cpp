struct IndexList {
    unsigned int __thiscall FUN_0044ddc0();
    unsigned short* __thiscall FUN_0069dec0(unsigned int index);
};

struct NavMeshKey;

struct NavMeshLookup {
    NavMeshLookup* __thiscall FUN_00559450();
    unsigned char* __thiscall FUN_006e1610(NavMeshLookup* rhs);
    bool __thiscall FUN_0069ad00(NavMeshKey* key);
    IndexList* __thiscall FUN_006911f0(unsigned int identifier);
};

struct NavMeshKey {
    NavMeshLookup* pointer;
    NavMeshKey();
    ~NavMeshKey();
    NavMeshLookup* __thiscall FUN_00559450();
};

struct NavMeshResults {
    unsigned char* data;
    unsigned int size;
    unsigned int capacity;
    unsigned int flags;
    void __thiscall FUN_008454f0(unsigned int value);
    void __thiscall FUN_006e10c0(unsigned int size, int mode);
    signed char* __thiscall FUN_006a62f0(unsigned int index);
};

struct FUN_006df440_owner {
    union {
        bool valid;
        unsigned int state;
    };
    NavMeshResults results;
    NavMeshLookup* lookup;
    unsigned int identifier;
    bool __thiscall FUN_006df440(NavMeshLookup* value);
};

bool FUN_006df440_owner::FUN_006df440(NavMeshLookup* value)
{
    unsigned char* const bytes = value->FUN_00559450()->FUN_006e1610(lookup->FUN_00559450());
    if (!bytes)
        return false;

    NavMeshKey key;
    if (!lookup->FUN_0069ad00(&key))
        return false;

    IndexList* const indices = key.FUN_00559450()->FUN_006911f0(identifier);
    if (!indices)
        return false;

    results.FUN_008454f0(0);
    results.FUN_006e10c0(indices->FUN_0044ddc0(), 1);
    valid = true;

    for (unsigned int index = 0; index < indices->FUN_0044ddc0(); ++index) {
        *results.FUN_006a62f0(index) = bytes[*indices->FUN_0069dec0(index)];
        if (*results.FUN_006a62f0(index) <= 0 || *results.FUN_006a62f0(index) == 0x7f)
            valid = false;
    }

    if (valid)
        results.FUN_008454f0(1);

    return true;
}