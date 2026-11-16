
struct NavigationRequest {
    int stored;
    bool FUN_00690860(void* output);
    int FUN_006b6390(bool enable);
};
struct BoundNavigationMap {
    bool FUN_00853130(int entry, NavigationRequest** request);
    void FUN_00405430(int entry);
};
struct ScopedNavPointer {
    void* current;
    void FUN_0042fb00();
    void FUN_0042fa40();
    void* FUN_00559450(int index);
    ScopedNavPointer() { FUN_0042fb00(); }
    ~ScopedNavPointer() { FUN_0042fa40(); }
};
struct ActiveResolver {
    void* FUN_00484e60();
};
struct VerifiedPath {
    bool FUN_00471c20();
};
struct NavigationOwner {
    virtual void UnknownVirtual00() = 0;
    virtual void UnknownVirtual01() = 0;
    virtual void UnknownVirtual02() = 0;
    virtual void UnknownVirtual03() = 0;
    virtual void UnknownVirtual04() = 0;
    virtual void UnknownVirtual05() = 0;
    virtual void UnknownVirtual06() = 0;
    virtual void UnknownVirtual07() = 0;
    virtual void UnknownVirtual08() = 0;
    virtual void UnknownVirtual09() = 0;
    virtual void UnknownVirtual10() = 0;
    virtual void UnknownVirtual11() = 0;
    virtual void UnknownVirtual12() = 0;
    virtual void UnknownVirtual13() = 0;
    virtual void UnknownVirtual14() = 0;
    virtual void UnknownVirtual15() = 0;
    virtual void UnknownVirtual16() = 0;
    virtual void UnknownVirtual17() = 0;
    virtual void UnknownVirtual18() = 0;
    virtual void UnknownVirtual19() = 0;
    virtual void UnknownVirtual20() = 0;
    virtual void UnknownVirtual21() = 0;
    virtual void UnknownVirtual22() = 0;
    virtual void UnknownVirtual23() = 0;
    virtual void UnknownVirtual24() = 0;
    virtual void UnknownVirtual25() = 0;
    virtual void UnknownVirtual26() = 0;
    virtual void UnknownVirtual27() = 0;
    virtual void UnknownVirtual28() = 0;
    virtual void UnknownVirtual29() = 0;
    virtual void UnknownVirtual30() = 0;
    virtual void UnknownVirtual31() = 0;
    virtual void UnknownVirtual32() = 0;
    virtual void UnknownVirtual33() = 0;
    virtual void UnknownVirtual34() = 0;
    virtual void UnknownVirtual35() = 0;
    virtual void UnknownVirtual36() = 0;
    virtual void UnknownVirtual37() = 0;
    virtual void UnknownVirtual38() = 0;
    virtual void UnknownVirtual39() = 0;
    virtual void UnknownVirtual40() = 0;
    virtual void UnknownVirtual41() = 0;
    virtual void UnknownVirtual42() = 0;
    virtual void UnknownVirtual43() = 0;
    virtual void UnknownVirtual44() = 0;
    virtual void UnknownVirtual45() = 0;
    virtual void UnknownVirtual46() = 0;
    virtual void UnknownVirtual47() = 0;
    virtual void UnknownVirtual48() = 0;
    virtual void UnknownVirtual49() = 0;
    virtual void SetNavigationState(int);
    void FUN_006b7b70(NavigationRequest* request);
    void FUN_006b6a00(int identifier);
};
void NavigationOwner::FUN_006b6a00(int identifier)
{
    NavigationRequest* entry;
    if (reinterpret_cast<BoundNavigationMap*>(reinterpret_cast<char*>(this)+0x1c)->FUN_00853130(identifier,&entry)) {
        FUN_006b7b70(entry);
        bool isAccepted = false;
        ScopedNavPointer pointer;
        if (entry->FUN_00690860(&pointer)) {
            VerifiedPath* active = reinterpret_cast<VerifiedPath*>(reinterpret_cast<ActiveResolver*>(pointer.FUN_00559450(0))->FUN_00484e60());
            if (active && active->FUN_00471c20())
                isAccepted = true;
        }
        {
            NavigationRequest* selected = entry;
            NavigationRequest* target = selected;
            target ? target->FUN_006b6390(true) : 0;
        }
        reinterpret_cast<BoundNavigationMap*>(reinterpret_cast<char*>(this)+0x1c)->FUN_00405430(identifier);
        if (isAccepted)
            SetNavigationState(1);
    }
}
