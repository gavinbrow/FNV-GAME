struct PendingOperations {
    void __thiscall FUN_00cf7690();
};

struct WorldWithPending : hkpWorld {
    void __thiscall FUN_00c91160();
};

void __thiscall WorldWithPending::FUN_00c91160()
{
    ((PendingOperations*)m_pendingOperations)->FUN_00cf7690();
}
