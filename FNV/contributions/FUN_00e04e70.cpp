struct FUN_00e04e70_class {
    virtual void vf0(); virtual void vf1(); virtual void vf2(); virtual void vf3(); virtual void vf4(); virtual void vf5();
    virtual int vf6(void* first, void* second);
    int unknown04; void* value08; void* value0c;
    int FUN_00e04e70(void* first, void* second);
};
int FUN_00e04e70_class::FUN_00e04e70(void* first, void* second) {
    int result = vf6(first, second);
    value08 = 0;
    value0c = 0;
    return result;
}