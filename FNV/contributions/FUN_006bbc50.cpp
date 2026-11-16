struct ItemResource {
    void FUN_00401970();
};

struct ResourceHolder {
    ItemResource* FUN_00559450();
};

struct Item {
    void* unk00;
    void* unk04;
    void* unk08;
    void* unk0C;
    void* unk10;
    void* unk14;
    void* unk18;
    ResourceHolder resource;
};

struct ItemPointer {
    Item* item;
};

struct FUN_0045cec0 {
    int first;
    int second;
    ~FUN_0045cec0();
};

struct FUN_00982610 {
    int first;
    int second;
    int third;
    int fourth;
    ~FUN_00982610();
};

struct FUN_006bf890 {
    int first;
    int second;
    int third;
    int fourth;
    int fifth;
    ~FUN_006bf890();
};

struct FUN_006bfad0 {
    ItemPointer* entries;
    unsigned int count;
    unsigned int capacity;
    unsigned int flags;

    unsigned int FUN_0044ddc0();
    ItemPointer* FUN_00877a30(unsigned int index);
    ~FUN_006bfad0();
};

struct FUN_006bbc50 {
    int identifier;
    FUN_0045cec0 first;
    FUN_00982610 second;
    FUN_006bf890 third;
    FUN_006bfad0 fourth;
    ~FUN_006bbc50();
};

FUN_006bbc50::~FUN_006bbc50()
{
    for (unsigned int i = 0; i < fourth.FUN_0044ddc0(); ++i) {
        if (fourth.FUN_00877a30(i)->item->resource.FUN_00559450()) {
            fourth.FUN_00877a30(i)->item->resource.FUN_00559450()->FUN_00401970();
        }
    }
}