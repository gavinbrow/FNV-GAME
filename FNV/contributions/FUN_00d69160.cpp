struct Base {
    int FUN_00d68a70(int);
    void FUN_00d69010(int);
};
struct Sub {
    void FUN_00d69160(int);
};
void Sub::FUN_00d69160(int value)
{
    Base* base = reinterpret_cast<Base*>(reinterpret_cast<char*>(this) - 0x20);
    int result = base->FUN_00d68a70(value);
    if (result >= 0)
        base->FUN_00d69010(result);
}
