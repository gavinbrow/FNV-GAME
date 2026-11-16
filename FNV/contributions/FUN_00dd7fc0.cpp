struct WorkItem {
    int unk00;
    WorkItem* next;
    int unk08;
    int value;
};

struct WorkProcessor {
    virtual void first();
    virtual void second();
    virtual void third();
    virtual void fourth();
    virtual void process(WorkItem*, int);
};

struct QueueOwner {
    int unk00; int unk04; int unk08; int unk0c;
    int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c;
    int unk30; int unk34; int unk38; int unk3c;
    int unk40; int unk44; int unk48; int unk4c;
    int unk50; int unk54; int unk58; int unk5c;
    int unk60; int unk64; int unk68; int unk6c;
    int unk70; int unk74; int unk78; int unk7c;
    int unk80; int unk84; int unk88; int unk8c;
    int unk90; int unk94;
    WorkProcessor* processor;
    int unk9c;
    int unka0;
    WorkItem sentinel;
    void FUN_00dd7fc0();
    void FUN_00dd7f10();
};

void QueueOwner::FUN_00dd7fc0() {
    WorkItem* current = sentinel.next;
    if (current != &sentinel) {
        do {
            int value = current->value;
            WorkProcessor* handler = processor;
            WorkItem* next = current->next;
            handler->process(current, value);
            current = next;
        } while (current != &sentinel);
    }
    FUN_00dd7f10();
}

