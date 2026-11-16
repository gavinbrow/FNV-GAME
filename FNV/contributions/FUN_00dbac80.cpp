struct Target {
    virtual void method00();
    virtual void method04();
    virtual void method08();
    virtual void method0c();
    virtual void method10();
    virtual void method14();
    virtual void method18();
    virtual void method1c();
    virtual void method20();
    virtual void method24();
    virtual void method28();
    virtual void method2c();
    virtual void apply(void* value);
};
struct Wrapper {
    Target* target;
    void* value;
    void FUN_00dbac80();
};
void Wrapper::FUN_00dbac80() {
    target->apply(value);
}
