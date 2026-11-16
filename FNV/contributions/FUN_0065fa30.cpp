namespace std {
class bad_alloc {
public:
    virtual ~bad_alloc();
    bad_alloc(const char* message = 0);
    const char* description;
    int ownsMessage;
};
}
void* __cdecl FUN_0065fa30(unsigned int count) {
    if (count <= 0) {
        count = 0;
    } else {
        if (0xffffffffu / count < 1u)
            throw std::bad_alloc();
    }
    return ::operator new(count);
}