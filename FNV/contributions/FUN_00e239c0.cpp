struct EntryHandler
{
    virtual void First();
    virtual void Second();
    virtual void Process(void* entry, unsigned int size);
};
struct ServiceContext
{
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    EntryHandler* handler;
};
ServiceContext* __cdecl FUN_00c85750();

struct EntryList
{
    void** entries;
    int count;
    int unk08;
    int unk0c;
    int unk10;
    void FUN_00e239c0();
};
void EntryList::FUN_00e239c0()
{
    int i = 0;
    while (i < count)
    {
        void* entry = entries[i];
        ServiceContext* context = FUN_00c85750();
        context->handler->Process(entry, 0x288);
        ++i;
    }
    count = 0;
    unk0c = 0;
    unk10 = 0;
}
