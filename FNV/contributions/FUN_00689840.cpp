extern const float DAT_01012054;
float __cdecl FUN_00404010(float lhs, float rhs);

struct TrailEntry
{
    double FUN_004a7bd0();
    double FUN_0047c860();
    TrailEntry* FUN_004a8a90();
};

struct TraversalItem
{
    virtual void v0();
    virtual void v1();
    virtual void v2();
    virtual TraversalItem* v3();
    TrailEntry* FUN_0043b230();
    int FUN_00453470();
    TraversalItem* FUN_0043b4a0(int index);
};

struct FUN_00689840_Class
{
    float FUN_00689840(TraversalItem* entry);
};

float FUN_00689840_Class::FUN_00689840(TraversalItem* entry)
{
    float accumulator = DAT_01012054;
    TrailEntry* cursor = entry->FUN_0043b230();
    while (cursor != 0)
    {
        accumulator = FUN_00404010(accumulator, static_cast<float>(cursor->FUN_004a7bd0() - cursor->FUN_0047c860()));
        cursor = cursor->FUN_004a8a90();
    }

    TraversalItem* children = entry->v3();
    if (children != 0)
    {
        int count = children->FUN_00453470();
        for (int i = 0; i < count; ++i)
        {
            TraversalItem* child = children->FUN_0043b4a0(i);
            if (child != 0)
                accumulator = FUN_00404010(accumulator, FUN_00689840(child));
        }
    }
    return accumulator;
}