struct ManagedSceneEntry {
    unsigned int state;
    unsigned int identifier;
    unsigned int priority;
    unsigned int flags;
    unsigned int timestamp;

    __forceinline ManagedSceneEntry() {
        reinterpret_cast<S751*>(this)->FUN_004751d0();
    }
};

struct ManagedSceneHolder {
    unsigned int mode;
    ManagedSceneEntry* current;
    void FUN_00478600();
};

void ManagedSceneHolder::FUN_00478600()
{
    if (!current)
        current = new ManagedSceneEntry;
}
