extern "C" void* DAT_0109b220;

struct ReferenceHandle
{
    volatile long* value;
    void operator=(const ReferenceHandle& other)
    {
        volatile long* next = other.value;
        if (value != next) {
            if (next != DAT_0109b220)
                InterlockedIncrement(next - 2);
            if (value != DAT_0109b220)
                InterlockedDecrement(value - 2);
            value = next;
        }
    }
};

struct RefCountedPair
{
    unsigned int identifier;
    ReferenceHandle handle;
    RefCountedPair* FUN_00a9be30(const RefCountedPair* other);
};

RefCountedPair* RefCountedPair::FUN_00a9be30(const RefCountedPair* other)
{
    identifier = other->identifier;
    handle = other->handle;
    return this;
}