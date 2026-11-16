namespace std {
template<> class basic_string<char, char_traits<char>, allocator<char> > {
public:
    void* _Myproxy;

    union { char _Buf[16]; char* _Ptr; } _Bx;
    unsigned int _Mysize;
    unsigned int _Myres;
    char* _Myptr();
    bool _Inside(const char*);
    bool _Grow(unsigned int, bool);
    void _Eos(unsigned int);
    void _Tidy(bool, unsigned int);
    basic_string* FUN_007ab250(unsigned int, unsigned int, basic_string*, unsigned int, unsigned int);
    basic_string* FUN_007ab0a0(unsigned int, unsigned int, const char*, unsigned int);
};
}
extern unsigned int DAT_010173f0;
extern void __cdecl FUN_00ec30e8();
extern void __cdecl FUN_0044d580(char*, unsigned int, const char*, unsigned int);

std::basic_string<char, std::char_traits<char>, std::allocator<char> >*
std::basic_string<char, std::char_traits<char>, std::allocator<char> >::FUN_007ab0a0(
    unsigned int pos, unsigned int count, const char* src, unsigned int srcCount)
{
    if (_Inside(src)) {
        return FUN_007ab250(pos, count, this, (unsigned int)(src - _Myptr()), srcCount);
    }
    if (_Mysize < pos)
        FUN_00ec30e8();
    if (_Mysize - pos < count)
        count = _Mysize - pos;
    if (DAT_010173f0 - srcCount <= _Mysize - count)
        FUN_00ec30b0();
    unsigned int tail = _Mysize - count - pos;
    if (srcCount < count)
        FUN_0044d580(_Myptr() + pos + srcCount, _Myres - pos - srcCount,
                     _Myptr() + pos + count, tail);
    if (srcCount > 0 || count > 0) {
        unsigned int newSize = (_Mysize + srcCount) - count;
        if (_Grow(newSize, false)) {
            if (count < srcCount)
                FUN_0044d580(_Myptr() + pos + srcCount, _Myres - pos - srcCount,
                             _Myptr() + pos + count, tail);
            FUN_0044ccd0(_Myptr() + pos, _Myres - pos, src, srcCount);
            _Eos(newSize);
        }
    }
    return this;
}









