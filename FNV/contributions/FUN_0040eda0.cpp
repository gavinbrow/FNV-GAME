extern void* DAT_0101421c;

struct CleanupBase {
    ~CleanupBase();
};

struct FUN_00633c90 {
    FUN_00633c90(unsigned int value);
    ~FUN_00633c90();
    void FUN_0066b0d0(void* value);
    void* value;
};

struct FUN_0040eda0 : BSExtraData, CleanupBase {
    FUN_00633c90 first;
    FUN_00633c90 second;
    FUN_0040eda0(void* value);
};

FUN_0040eda0::FUN_0040eda0(void* value)
    : BSExtraData(1),
      first((m_vtable = (void**)&DAT_0101421c, 0)),
      second(0)
{
    first.FUN_0066b0d0(value);
    second.FUN_0066b0d0(0);
}