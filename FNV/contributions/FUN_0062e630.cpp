struct FUN_00cb75d0 {
    virtual void OnEvent();
    void* owner;
    unsigned int flags;
    void* context;
    unsigned int referenceCount;
    FUN_00cb75d0();
    ~FUN_00cb75d0();
};
struct FUN_0061ffb0 {
    virtual void Update();
    unsigned int state;
    FUN_0061ffb0();
    ~FUN_0061ffb0();
};
struct FUN_0048f200 {
    FUN_0048f200();
    ~FUN_0048f200();
};
struct FUN_0062e630 : FUN_00cb75d0, FUN_0061ffb0 {
    float scale;
    int* data;
    unsigned int capacity;
    unsigned int enabled;
    int predecessor;
    int successor;
    FUN_0048f200 synchronization;
    FUN_0062e630(float value);
};
FUN_0062e630::FUN_0062e630(float value) : scale(1.0f) {
    enabled = 1;
    data = new int;
    reinterpret_cast<FUN_0062e710_shell*>(this)->FUN_0062e710(value, 0, 0);
    predecessor = 0;
    successor = 0;
}