namespace std {
class bad_alloc {
public:
    virtual ~bad_alloc();
    bad_alloc(const char* message = 0);
    const char* message;
    bool ownsMessage;
};
}

void* __cdecl FUN_0065e430(unsigned int count)
{
    if (count <= 0u)
        count = 0;
    else if (0xffffffffu / count < 32u)
        throw std::bad_alloc();

    return ::operator new(count * 32u);
}
