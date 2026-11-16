struct MyOther;
struct CompareBase { bool FUN_00a5e600(MyOther* other); };
struct MyOther : CompareBase { unsigned char FUN_00a952e0(MyOther* other); };
unsigned char MyOther::FUN_00a952e0(MyOther* other) {
    unsigned char result = FUN_00a5e600(other);
    if (!result)
        return result;
    return (unsigned char)(*(int*)((char*)this + 0xac) == *(int*)((char*)other + 0xac));
}
