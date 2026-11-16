struct InputProvider {
    virtual void reserved0();
    virtual void reserved1();
    virtual void GetData(unsigned char** data, int* length);
};
struct MessageContext {
    void* unk00;
    void* unk04;
    void* unk08;
    void* unk0c;
    void* active;
};
MessageContext* __cdecl FUN_00c85750();
struct MessageSink {
    void __thiscall FUN_00cb1870(void* active, unsigned int value, InputProvider* source);
};
struct MessageProcessor {
    void* unk00;
    void* unk04;
    MessageSink sink;
    void __thiscall FUN_00dd9600(InputProvider* source);
};
void MessageProcessor::FUN_00dd9600(InputProvider* source)
{
    unsigned char* bytes = 0;
    int length = 0;
    source->GetData(&bytes, &length);
    for (int i = 0; i < length; ++i) {
        unsigned char value = bytes[i];
        MessageContext* context = FUN_00c85750();
        sink.FUN_00cb1870(context->active, value, source);
    }
}
