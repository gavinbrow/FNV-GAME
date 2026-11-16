
struct UpdateOptions {
    unsigned char enabled;
    UpdateOptions(bool value) : enabled(value) {}
};

struct ObjectView {
    virtual void Reserved0();
    virtual void Reserved1();
    virtual void Reserved2();
    virtual void Reserved3();
    virtual void Reserved4();
    virtual void Reserved5();
    virtual void Reserved6();
    virtual void Reserved7();
    virtual int GetKind();

    ObjectView* FUN_00cdf6c0();
    void FUN_00cdf290(struct ComponentEntry* entry, UpdateOptions options);
    void FUN_00cb8fe0(struct ComponentEntry* entry, UpdateOptions options);
};

struct ComponentEntry {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    ObjectView* view;
};

struct ObjectCount {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int count;
};

struct ObjectContext {
    void* unk00;
    void* unk04;
    void* unk08;
    void* unk0c;
    void* unk10;
    ComponentEntry** entries;
    void* unk18;
    void* unk1c;
    int* indices;
    void* unk24;
    void* unk28;
    ObjectCount* length;
};

void __cdecl FUN_00c7a380(ObjectContext* context)
{
    const int count = context->length->count;
    for (int index = 0; index < count; ++index) {
        int entryIndex = context->indices[index] - 1;
        if (entryIndex >= 0) {
            ComponentEntry* entry = context->entries[entryIndex];
            if (entry != 0) {
                ObjectView* view = entry->view;
                if (view->GetKind() == 13)
                    view = view->FUN_00cdf6c0();
                if (view != 0) {
                    int kind = view->GetKind();
                    switch (kind) {
                    case 2:
                        view->FUN_00cb8fe0(entry, false);
                        break;
                    case 7:
                        view->FUN_00cdf290(entry, false);
                        break;
                    }
                }
            }
        }
    }
}