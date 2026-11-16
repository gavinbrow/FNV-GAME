struct BGSDecalEmitter {
    void FUN_004a2d50();
    bool FUN_004f1540();
    ~BGSDecalEmitter();
};

struct DecalEmitterNode {
    BGSDecalEmitter* emitter;
    DecalEmitterNode* next;
};

struct DecalEmitterList {
    DecalEmitterNode* head;
    DecalEmitterNode* tail;
    unsigned int count;
    DecalEmitterNode* FUN_00559450();
    BGSDecalEmitter** FUN_0057cbe0(DecalEmitterNode** cursor);
    void FUN_0049f590(DecalEmitterNode** cursor);
};

struct PendingDecalList {
    void* head;
    void* tail;
    unsigned int count;
};

struct DecalCleanupOwner {
    void* queryTexture;
    unsigned int clearQueryTexture;
    PendingDecalList pendingSimpleDecals;
    DecalEmitterList decalEmitters;
    void FUN_004a03f0();
};

void DecalCleanupOwner::FUN_004a03f0()
{
    DecalEmitterNode* cursor = decalEmitters.FUN_00559450();
    while (cursor != 0) {
        DecalEmitterNode* previous = cursor;
        BGSDecalEmitter* emitter = *decalEmitters.FUN_0057cbe0(&cursor);
        if (emitter != 0) {
            emitter->FUN_004a2d50();
            if (emitter->FUN_004f1540()) {
                decalEmitters.FUN_0049f590(&previous);
                delete emitter;
                emitter = 0;
            }
        }
    }
}