struct FUN_0065de30 {
    void* value;
    explicit FUN_0065de30(void* source);
    FUN_0065de30(const FUN_0065de30& other);
};
struct FUN_007ab050_Class {
    void FUN_0044a7b0(FUN_0065de30 value);
    void FUN_0044a730(unsigned int a, unsigned int b);
    void FUN_0044a580(unsigned int a, unsigned int b, unsigned int c);
    FUN_007ab050_Class* FUN_007ab050(unsigned int a, unsigned int b, unsigned int c, void* source);
};
FUN_007ab050_Class* FUN_007ab050_Class::FUN_007ab050(unsigned int a, unsigned int b, unsigned int c, void* source)
{
    FUN_0044a7b0(FUN_0065de30(source));
    FUN_0044a730(0, 0);
    FUN_0044a580(a, b, c);
    return this;
}