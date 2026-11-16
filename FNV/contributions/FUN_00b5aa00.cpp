struct PaletteFieldFlags {
    unsigned int __thiscall FUN_00b5aa00() const;
};

unsigned int __thiscall PaletteFieldFlags::FUN_00b5aa00() const
{
    const unsigned char* const fieldBytes =
        reinterpret_cast<const unsigned char*>(this);

    return (((fieldBytes[0xe9] == 0) * 2 |
             (fieldBytes[0xe8] == 0)) * 2 |
             (fieldBytes[0xe7] == 0)) * 2 |
             (fieldBytes[0xe6] == 0);
}