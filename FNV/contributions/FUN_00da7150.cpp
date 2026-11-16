struct Inner {
    virtual void v00();
    virtual unsigned char Invoke(void* first, void* second);
    unsigned char state;
};
struct Wrapper {
    virtual void v00();
    unsigned char state;
    Inner* inner;
    unsigned char FUN_00da7150(void* first, void* second);
};
unsigned char Wrapper::FUN_00da7150(void* first, void* second) {
    inner->Invoke(second, first);
    return state = inner->state;
}




