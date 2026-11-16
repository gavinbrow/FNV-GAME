struct FNVInputStream
{
    void FUN_00864980(void* destination, unsigned int bytes);
    unsigned int FUN_00864a60();
};
struct FNVElements4
{
    void FUN_006f2290(unsigned int count, unsigned int flag);
    void* FUN_006a7ad0(unsigned int index);
};
struct FNVElements12
{
    void FUN_0069cea0(unsigned int count, unsigned int flag);
    void* FUN_006a7af0(unsigned int index);
};
struct FUN_006e51a0_shell
{
    void FUN_006e34f0(FNVInputStream* stream);
    void FUN_006e51a0(FNVInputStream* stream);
};
void FUN_006e51a0_shell::FUN_006e51a0(FNVInputStream* stream)
{
    FUN_006e34f0(stream);
    stream->FUN_00864980(reinterpret_cast<char*>(this) + 0xb0, 4);
    stream->FUN_00864980(reinterpret_cast<char*>(this) + 0xb4, 4);
    stream->FUN_00864980(reinterpret_cast<char*>(this) + 0xb8, 4);
    stream->FUN_00864980(reinterpret_cast<char*>(this) + 0xbc, 4);
    stream->FUN_00864980(reinterpret_cast<char*>(this) + 0xc0, 4);
    stream->FUN_00864980(reinterpret_cast<char*>(this) + 0xc4, 4);
    stream->FUN_00864980(reinterpret_cast<char*>(this) + 0xc8, 12);
    stream->FUN_00864980(reinterpret_cast<char*>(this) + 0xd4, 12);
    stream->FUN_00864980(reinterpret_cast<char*>(this) + 0xe0, 1);

    unsigned int count4 = stream->FUN_00864a60();
    reinterpret_cast<FNVElements4*>(reinterpret_cast<char*>(this) + 0xe4)->FUN_006f2290(count4, 1);
    for (unsigned int i = 0; i < count4; ++i) {
        void* item = reinterpret_cast<FNVElements4*>(reinterpret_cast<char*>(this) + 0xe4)->FUN_006a7ad0(i);
        stream->FUN_00864980(item, 4);
    }
    {
    unsigned int count12 = stream->FUN_00864a60();
    reinterpret_cast<FNVElements12*>(reinterpret_cast<char*>(this) + 0xf4)->FUN_0069cea0(count12, 1);
    for (unsigned int j = 0; j < count12; ++j) {
        void* item = reinterpret_cast<FNVElements12*>(reinterpret_cast<char*>(this) + 0xf4)->FUN_006a7af0(j);
        stream->FUN_00864980(item, 12);
    }
    }
}