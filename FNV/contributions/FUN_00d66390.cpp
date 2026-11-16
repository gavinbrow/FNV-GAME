struct Viewer {
    int unk00, unk04, unk08, unk0c;
    void* callbackState;
};

struct Callback {
    virtual void slot0();
    virtual void slot1();
    virtual void slot2();
    virtual void slot3();
    virtual void slot4();
    virtual void notify(void* field, int global, void* value);
};

extern int DAT_01268ff0;

struct OwnerBase {
    Callback* callback;
    int unk04, unk08, unk0c;
};

struct ViewerList {
    void* unk00;
    void* unk04;
    Viewer** entries;
    volatile int count;
    int capacity;
    void FUN_00d66390(Viewer* target);
};

struct ViewerOwner : OwnerBase, ViewerList {};

void ViewerList::FUN_00d66390(Viewer* target)
{
    int index = 0;
    int length = count;
    if (length > 0) {
        Viewer** cursor = entries;
        do {
            if (*cursor == target) {
                if (index >= 0) {
                    --count;
                    int newCount = count;
                    if (newCount != index)
                        entries[index] = entries[newCount];

                    ViewerOwner* owner = static_cast<ViewerOwner*>(this);
                    owner->callback->notify(&target->callbackState,
                                             DAT_01268ff0,
                                             target->callbackState);
                    return;
                }
                return;
            }
            ++index;
            ++cursor;
        } while (index < length);
        return;
    }
    return;
}
