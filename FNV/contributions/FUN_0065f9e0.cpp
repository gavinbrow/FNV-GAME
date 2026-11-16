namespace std {
class bad_alloc {
public:
    bad_alloc(const char* message);
    virtual ~bad_alloc();
    virtual const char* what() const;
private:
    const char* message_;
    bool owns_message_;
};
}
extern "C" void __cdecl FUN_0065f9e0(int count, int unused)
{
    if ((unsigned int)count <= 0u) {
        count = 0;
    } else if (0xffffffffu / (unsigned int)count < 6u) {
        throw std::bad_alloc(0);
    }
    ::operator new((unsigned int)count * 6u);
}
