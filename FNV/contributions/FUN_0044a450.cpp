struct FUN_00ec7944 {
    virtual ~FUN_00ec7944();
    unsigned int unknown04;
    unsigned int unknown08;
    FUN_00ec7944(const FUN_00ec7944& other);
};
struct FUN_0044a500 {
    FUN_0044a500(const FUN_0044a500& other);
    ~FUN_0044a500();
};
struct FUN_0044a450 : FUN_00ec7944 {
    FUN_0044a500 value;
    virtual ~FUN_0044a450();
    FUN_0044a450(const FUN_0044a450& other);
};
FUN_0044a450::FUN_0044a450(const FUN_0044a450& other)
    : FUN_00ec7944(other), value(other.value) {
}