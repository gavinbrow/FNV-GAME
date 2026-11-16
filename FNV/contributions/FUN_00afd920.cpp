int __cdecl FUN_00ec3bad(int value);
struct AllocatorToken { unsigned char state; };
struct FUN_00afd920_Class {
    int value;
    void __thiscall FUN_00afd920();
};
void FUN_00afd920_Class::FUN_00afd920() {
    AllocatorToken allocator = {};
    AllocatorToken copy = allocator;
    FUN_00afd920_Class* self = this;
    self->value = FUN_00ec3bad(self->value);
}