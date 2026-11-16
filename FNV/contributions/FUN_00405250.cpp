extern int DAT_01012238;
void __cdecl FUN_00aa10f0(void* p);

struct C405250Node {
    C405250Node* next;
    void* payload;
};
struct FUN_00405310 {
    virtual ~FUN_00405310();
};
struct FUN_00405250 : public FUN_00405310 {
    unsigned int count;
    C405250Node** buckets;
    int reserved;
    unsigned char ownsData;
    virtual ~FUN_00405250();
};
FUN_00405250::~FUN_00405250()
{
    if (ownsData) {
        for (unsigned int i = 0; i < count; ++i) {
            C405250Node* node = buckets[i];
            while (node != 0) {
                C405250Node* current = node;
                node = node->next;
                FUN_00aa10f0(current->payload);
            }
        }
    }
}
