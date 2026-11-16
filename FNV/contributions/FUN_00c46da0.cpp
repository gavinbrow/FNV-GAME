struct FUN_00c46da0_class : BaseForCall {
    bool __thiscall FUN_00c46da0(NiObject* other);
};
bool __thiscall FUN_00c46da0_class::FUN_00c46da0(NiObject* other)
{
    bool result = FUN_00a5e600(other);
    NiObject* comparison = other;
    if (static_cast<int>(static_cast<unsigned char>(static_cast<int>(
        *reinterpret_cast<int*>(reinterpret_cast<char*>(this) + 0xAC) ==
        *reinterpret_cast<int*>(reinterpret_cast<char*>(comparison) + 0xAC))))) {
        result = true;
    } else {
        result = false;
    }
    return result;
}