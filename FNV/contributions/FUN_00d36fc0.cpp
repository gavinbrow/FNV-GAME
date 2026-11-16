struct Handler {
    virtual void slot0();
    virtual void slot1();
    virtual void slot2();
    virtual void slot3();
    virtual void slot4();
    virtual void process(unsigned short index, int argument);
};
struct Owner {
    virtual ~Owner();
    int unk04;
    Handler* handler;
    unsigned short* values;
    int count;
    void FUN_00d36fc0(int argument);
};
void Owner::FUN_00d36fc0(int argument) {
    int length = count;
    for (int i = 0; i < length; ++i) {
        unsigned short index = values[i];
        if (index != 0xffff)
            handler->process(index, argument);
    }
    delete this;
}