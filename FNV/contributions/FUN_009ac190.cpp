struct ReferenceHeader
{
    unsigned int type;
    unsigned int flags;
    unsigned int size;
};

struct ReferencePayload
{
    unsigned int identifier;
};

struct ReferenceNode : ReferenceHeader, ReferencePayload
{
};

struct FUN_009ac190_object
{
    ReferencePayload* FUN_009ac190();
};

ReferencePayload* FUN_009ac190_object::FUN_009ac190()
{
    return *reinterpret_cast<ReferenceNode**>(reinterpret_cast<char*>(this) + 0xdc);
}
