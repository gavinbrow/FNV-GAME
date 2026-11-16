struct ValueItem { virtual ~ValueItem(); };
struct BaseMap {
    virtual ~BaseMap();
    void* FUN_004b9ba0();
    void FUN_006b7f20(void**, unsigned int*, ValueItem**);
    void FUN_008447e0();
};
struct FUN_00841720 : BaseMap {
    virtual ~FUN_00841720();
};
FUN_00841720::~FUN_00841720()
{
    void* position = FUN_004b9ba0();
    while (position != 0) {
        ValueItem* item;
        {
            unsigned int key = 0;
            item = 0;
            FUN_006b7f20(&position, &key, &item);
        }
        delete item;
    }
}