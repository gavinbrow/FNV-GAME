extern const unsigned int DAT_010f1ca4;
namespace fnv_00a14a20
{
    void* NiMalloc(unsigned int size);
}
extern "C" void* FUN_00ec61c0(void* destination, int value, unsigned int size);

struct FUN_00ec2f00_item;

struct FUN_00ec2f00_cls
{
    const unsigned int* vtable;
    unsigned int bucketCount;
    FUN_00ec2f00_item** buckets;
    unsigned int count;

    FUN_00ec2f00_cls* FUN_00ec3020(unsigned int requestedBuckets);
};

// @fnv 0x00ec3020
FUN_00ec2f00_cls* FUN_00ec2f00_cls::FUN_00ec3020(unsigned int requestedBuckets)
{
    vtable = &DAT_010f1ca4;
    bucketCount = requestedBuckets;
    count = 0;
    unsigned int allocationSize = bucketCount * sizeof(FUN_00ec2f00_item*);
    buckets = static_cast<FUN_00ec2f00_item**>(fnv_00a14a20::NiMalloc(allocationSize));
    unsigned int bytesToClear = bucketCount * sizeof(FUN_00ec2f00_item*);
    void* destination = buckets;
    FUN_00ec61c0(destination, 0, bytesToClear);
    return this;
}
