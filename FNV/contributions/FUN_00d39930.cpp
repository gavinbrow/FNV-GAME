struct ReceiverBase { virtual void Release(unsigned int value); int unk04; };
struct NoteDispatcher {
    virtual void Unknown00(unsigned int, void*);
    virtual void Unknown04(unsigned int, void*);
    virtual void Unknown08(unsigned int, void*);
    virtual void Unknown0C(unsigned int, void*);
    virtual void Unknown10(unsigned int, void*);
    virtual void Dispatch(unsigned int id, void* value);
};
struct FUN_00d39930_class : ReceiverBase {
    NoteDispatcher* dispatcher;
    unsigned short receiverIds[3];
    void __thiscall FUN_00d39930(void* value);
};
void FUN_00d39930_class::FUN_00d39930(void* value)
{
    unsigned short* id = receiverIds;
    int count = 3;
    do {
        unsigned int current = *id;
        if ((unsigned short)current != 0xFFFF)
            dispatcher->Dispatch(current, value);
        ++id;
    } while (--count != 0);
    if (this)
        Release(1);
}
