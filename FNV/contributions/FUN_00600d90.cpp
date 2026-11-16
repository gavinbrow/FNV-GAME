
struct FUN_00600d90_node {
    FUN_00600d90_node* next;
    void* value;
};

void __cdecl FUN_00aa10f0(void* value);

struct FUN_00600e50 {
    virtual ~FUN_00600e50();
    unsigned int bucketCount;
    FUN_00600d90_node** buckets;
    unsigned int reserved;
    unsigned char ownsValues;
};

struct FUN_00600d90 : FUN_00600e50 {
    virtual ~FUN_00600d90();
};

FUN_00600d90::~FUN_00600d90()
{
    if (ownsValues) {
        for (unsigned int i = 0; i < bucketCount; ++i) {
            FUN_00600d90_node* node = buckets[i];
            while (node != 0) {
                FUN_00600d90_node* current = node;
                node = node->next;
                FUN_00aa10f0(current->value);
            }
        }
    }
}
