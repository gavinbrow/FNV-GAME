struct FUN_009fceb0_object {
    virtual void __stdcall first_virtual() {}
    virtual void __stdcall second_virtual() {}
};

int __stdcall FUN_009fceb0(FUN_009fceb0_object* object, int* target)
{
    if (target == 0)
        return 0x80004003;

    *target = reinterpret_cast<int>(object);
    object->second_virtual();
    return 0;
}