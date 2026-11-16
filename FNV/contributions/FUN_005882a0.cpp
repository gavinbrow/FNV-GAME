
struct FNVEmitter;
struct FNVLinkedNode {
    FNVEmitter** FUN_006815c0();
    FNVLinkedNode* FUN_00726070();
};
struct FNVLinkedList {
    FNVLinkedNode* FUN_00460140();
};
extern FNVLinkedList* DAT_011c3f2c;
struct FNVElement {
    int data0;
    int data4;
    FNVElement();
};
struct FNVEmitter {
    FNVEmitter* FUN_00586390(int type);
    void FUN_005884e0(FNVElement* element);
    FNVElement* FUN_005882a0(bool createNew);
};

FNVElement* FNVEmitter::FUN_005882a0(bool createNew)
{
    FNVElement* result = 0;
    if (FUN_00586390(2) && !createNew) {
        result = FUN_00586390(2)->FUN_005882a0(false);
    } else {
        result = new FNVElement;
        FUN_005884e0(result);
        if (!createNew) {
            FNVLinkedNode* node = DAT_011c3f2c->FUN_00460140();
            while (node) {
                FNVEmitter* emitter = *node->FUN_006815c0();
                if (emitter && emitter->FUN_00586390(2) == this) {
                    emitter->FUN_005884e0(result);
                }
                node = node->FUN_00726070();
            }
        }
    }
    return result;
}
