struct FUN_004968b0 {
    virtual ~FUN_004968b0();
    int referenceCount;
    FUN_004968b0();
};
struct FUN_006e2080 {
    int data;
    int count;
    int capacity;
    int allocation;
    int flags;
    FUN_006e2080(unsigned int size);
    ~FUN_006e2080();
};
struct FUN_0042f800 {
    int x;
    int y;
    int z;
    int w;
    FUN_0042f800();
};
struct Position3 {
    int x;
    int y;
    int z;
};
struct FUN_006e1370 : FUN_004968b0 {
    FUN_006e2080 items;
    FUN_0042f800 range;
    int value2c;
    int value30;
    int value34;
    bool option38;
    bool option39;
    Position3 position;
    float size;
    FUN_006e1370(Position3 coordinates, float dimension);
    virtual ~FUN_006e1370();
};
FUN_006e1370::FUN_006e1370(Position3 coordinates, float dimension)
    : FUN_004968b0(), items(37), range()
{
    position = coordinates;
    size = dimension;
    value2c = 0;
    value30 = 0;
    value34 = 0;
    items.flags = 0;
    option38 = false;
    option39 = false;
}
