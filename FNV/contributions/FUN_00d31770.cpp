struct Handler {
    virtual void v0();
    virtual void v1();
    virtual void v2();
    virtual void v3();
    virtual void v4();
    virtual void invoke(unsigned short item, int value);
};
struct Owner {
    virtual void clear(unsigned int mode);
    int unk04;
    Handler* callback;
    unsigned short* indices;
    int count;
    void FUN_00d31770(int value);
};
void Owner::FUN_00d31770(int value) {
    if (callback) {
        for(int index=0; index<count; ++index) {
            unsigned short item=indices[index];
            if(item!=0xffff)
                callback->invoke(item,value);
        }
    }
    clear(1);
}