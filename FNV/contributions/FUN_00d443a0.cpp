struct Listener {
    virtual void slot00();
    virtual void slot04();
    virtual void slot08();
    virtual void slot0c();
    virtual void slot10();
    virtual void slot14();
    virtual void slot18();
    virtual void Notify(unsigned int);
};
struct Entry { int unk00; Listener* listener; };
struct Dispatcher {
    virtual void Finish(unsigned int);
    int unk04;
    int unk08;
    Entry* entries;
    int count;
    void __thiscall FUN_00d443a0(unsigned int);
};
void Dispatcher::FUN_00d443a0(unsigned int value) {
    for (int i = 0; i < count; ++i)
        entries[i].listener->Notify(value);
    Finish(1);
}
