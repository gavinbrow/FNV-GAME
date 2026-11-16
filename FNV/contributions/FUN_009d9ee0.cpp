struct LinkedObject {
    void __thiscall FUN_0069cfe0(void* ownerData);
};

struct FUN_009d9ee0_Class {
    void __thiscall FUN_009d9ee0(LinkedObject* linked);
};

void FUN_009d9ee0_Class::FUN_009d9ee0(LinkedObject* linked)
{
    linked->FUN_0069cfe0(reinterpret_cast<char*>(this) + 0xb4);
}
