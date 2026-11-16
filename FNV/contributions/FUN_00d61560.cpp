struct FnvString
{
    const char* text;
    int FUN_00d61560(const char* other);
};

int FnvString::FUN_00d61560(const char* other)
{
    unsigned int i = 0;
    while (text[i] != 0)
    {
        if (other[i] == 0)
            break;
        if (text[i] != other[i])
            return 0;
        ++i;
    }
    return other[i] == 0;
}