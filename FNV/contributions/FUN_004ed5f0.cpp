
struct FUN_00a69940
{
    unsigned int word0, word1, word2, word3;
    FUN_00a69940();
};
struct FUN_0048f200
{
    float x, y, z;
    FUN_0048f200();
    ~FUN_0048f200();
};
struct FUN_00633c90
{
    void* object;
    FUN_00633c90(int);
    ~FUN_00633c90();
    void FUN_0066b0d0(int);
};
struct FUN_004ed5f0
{
    unsigned int state;
    FUN_00a69940 first;
    FUN_00a69940 second;
    FUN_0048f200 translation0;
    FUN_0048f200 translation1;
    FUN_0048f200 translation2;
    FUN_0048f200 translation3;
    FUN_00633c90 pointer0;
    FUN_00633c90 pointer1;
    bool enabled;
    bool flag5d;
    bool flag5e;
    bool visible;
    bool selected;
    FUN_0048f200 rotation0;
    FUN_0048f200 rotation1;
    FUN_0048f200 rotation2;
    FUN_0048f200 rotation3;
    FUN_00633c90 pointer2;
    FUN_00633c90 pointer3;
    void* resource;
    void* listener;
    FUN_00633c90 pointer4;
    FUN_00633c90 pointer5;
    FUN_004ed5f0();
};
FUN_004ed5f0::FUN_004ed5f0()
    : pointer0(0), pointer1(0), pointer2(0), pointer3(0), pointer4(0), pointer5(0)
{
    pointer2.FUN_0066b0d0(0);
    pointer3.FUN_0066b0d0(0);
    pointer1.FUN_0066b0d0(0);
    selected = false;
    visible = false;
    enabled = false;
}
