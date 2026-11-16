struct C97E80PendingOperation {
    unsigned char m_type;
    void* m_action;
};
struct C97E80Action {
    virtual void function00();
    virtual void function04();
    virtual void function08();
    virtual void function0C();
    virtual void function10();
    virtual void function14();
    virtual int getReferenceCount();
    unsigned int unk04, unk08, unk0C, unk10, unk14, unk18, unk1C;
    unsigned int unk20, unk24, unk28, unk2C, unk30, unk34, unk38, unk3C, unk40;
    void* m_owner44;
};
struct C97E80Owner {
    int unk00, unk04;
    hkpWorld* m_world;
};
struct C97E80PendingShell {
    void __thiscall FUN_00c91160(C97E80PendingOperation* operation);
};
struct C97E80RemoveShell {
    void __thiscall FUN_00c97510(void* owner);
};
struct C97E80ActionChangeShell {
    void __thiscall FUN_00cf3040(hkpWorld* world);
};
struct C97E80ReleaseShell {
    void __thiscall FUN_00c905b0();
};
struct C97E80CleanupShell {
    void __thiscall FUN_00c91120();
    void __thiscall FUN_00c91140();
};
void __cdecl FUN_00cb3dd0(hkpWorld* world, C97E80Action* action, int flags);
struct C97E80Return { bool m_status; };
struct C97E80World : hkpWorld {
    C97E80Return __thiscall FUN_00c97e80(C97E80Action* action);
};
C97E80Return __thiscall C97E80World::FUN_00c97e80(C97E80Action* action) {
    if (m_criticalOperationsLockCount) {
        C97E80PendingOperation operation;
        operation.m_type = 9;
        operation.m_action = action;
        ((C97E80PendingShell*)this)->FUN_00c91160(&operation);
        C97E80Return r = {false};
        return r;
    }

    m_criticalOperationsLockCount = 1;
    if (action->getReferenceCount() == 1 &&
        ((C97E80Owner*)action->m_owner44)->m_world == this) {
        ((C97E80RemoveShell*)this)->FUN_00c97510(action->m_owner44);
    }
    ((RefObj*)action)->FUN_00c90510();
    FUN_00cb3dd0(this, action, 1);
    ((C97E80ActionChangeShell*)action)->FUN_00cf3040(this);
    ((C97E80ReleaseShell*)action)->FUN_00c905b0();
    --m_criticalOperationsLockCount;
    if (m_criticalOperationsLockCount == 0 && !m_blockExecutingPendingOperations) {
        if (m_pendingOperationsCount) {
            ((C97E80CleanupShell*)this)->FUN_00c91120();
        }
        if (m_pendingOperationQueueCount == 1 && m_pendingBodyOperationsCount) {
            ((C97E80CleanupShell*)this)->FUN_00c91140();
        }
    }
    C97E80Return r = {true};
    return r;
}