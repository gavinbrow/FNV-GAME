struct ArrayElement_006ebd30 {
    int first;
    int second;
    int third;
    ~ArrayElement_006ebd30();
};

struct Base_006ebd30 {
    virtual ~Base_006ebd30();
    int state;
    int flags;
};

struct FUN_006ebd30 : Base_006ebd30 {
    ArrayElement_006ebd30 elements[256];
    virtual ~FUN_006ebd30();
};

FUN_006ebd30::~FUN_006ebd30() {
}