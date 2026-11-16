struct SeekableStream {
    virtual int __stdcall vfn_00() = 0;
    virtual int __stdcall vfn_04() = 0;
    virtual int __stdcall vfn_08() = 0;
    virtual int __stdcall GetPosition(__int64* position) = 0;
};

struct OffsetStream {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0C;
    unsigned int unk10;
    unsigned int unk14;
    SeekableStream* underlying;
    unsigned int unk1C;
    __int64 baseOffset;
    int FUN_009f9db0(__int64* position);
};

int OffsetStream::FUN_009f9db0(__int64* position)
{
    if (underlying == 0) {
        return (int)0x80040213;
    }

    int result = underlying->GetPosition(position);
    if (result >= 0) {
        *position -= baseOffset;
        return 0;
    }
    return result;
}