namespace std {
struct exception {
    virtual ~exception() throw();
    const char* message;
    bool ownsMessage;
};
struct bad_alloc : public exception {
    bad_alloc(const char* = 0) throw();
};
}
extern "C" void __cdecl FUN_0064e430(int count, int unused)
{
    if ((unsigned int)count <= 0u)
        count = 0;
    else if (0xffffffffu / (unsigned int)count < 16u)
        throw std::bad_alloc();
    ::operator new((unsigned int)count * 16u);
}
