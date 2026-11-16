struct FUN_00cc05f0Target {
    virtual void unused0();
    virtual void unused1();
    virtual void unused2();
    virtual void unused3();
    virtual void Invoke(const char* value, int mode);
};
struct RequestReceiver { int unk00; int unk04; FUN_00cc05f0Target* unk08; RequestReceiver* FUN_00cc05f0(void* request); };
RequestReceiver* RequestReceiver::FUN_00cc05f0(void* request) {
    int* values = (int*)request;
    if (values[0]) unk08->Invoke((const char*)values[0], values[1] - 1);
    else unk08->Invoke("(null)", 6);
    return this;
}
