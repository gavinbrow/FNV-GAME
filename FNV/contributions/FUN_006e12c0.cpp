struct FUN_006e12c0_Class {
    virtual void v0();
    virtual int v1(int requested);
    virtual void v2();
    virtual int v3(int oldData, int requested);
    int currentData;
    int reserved08;
    int cachedKey;
    void __thiscall FUN_006d07d0(int replacement, int previous, int previousKey);
    void __thiscall FUN_006a8500();
    void __thiscall FUN_006e12c0(int newData, int searchKey);
};
void FUN_006e12c0_Class::FUN_006e12c0(int newData, int searchKey) {
    if (currentData) {
        if (searchKey == cachedKey) {
            currentData = v3(currentData, newData);
        } else {
            int replacement = v1(newData);
            FUN_006d07d0(replacement, currentData, searchKey);
            FUN_006a8500();
            currentData = replacement;
        }
    } else {
        currentData = v1(newData);
        cachedKey = newData;
    }
}