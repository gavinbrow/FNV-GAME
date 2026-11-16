struct FNVReferenceIterator {
    TESForm** FUN_006815c0();
    FNVReferenceIterator* FUN_00726070();
    void FUN_00470470();
    ~FNVReferenceIterator();
};
struct FNVReferenceManager {
    FNVReferenceIterator* FUN_00971c30(PlayerCharacter* player, int formType, int includeDisabled);
};
extern "C" PlayerCharacter* DAT_011dea3c;
extern "C" FNVReferenceManager DAT_011e0e80;
struct FNVPlayerScanner {
    void FUN_00962190();
};
typedef bool (__fastcall *FNVVirtualActorPredicate)(Actor*);
void FNVPlayerScanner::FUN_00962190() {
    FNVReferenceIterator* first = DAT_011e0e80.FUN_00971c30(DAT_011dea3c, 18, 0);
    FNVReferenceIterator* iterator = first;
    reinterpret_cast<unsigned char*>(DAT_011dea3c)[0x7c4] = 0;
    while (iterator != 0) {
        Actor* actor = 0;
        if (*iterator->FUN_006815c0() != 0 &&
            (*iterator->FUN_006815c0())->IsActor()) {
            actor = static_cast<Actor*>(*iterator->FUN_006815c0());
        }
        if (actor != 0 &&
            reinterpret_cast<FNVVirtualActorPredicate>((*reinterpret_cast<void***>(actor))[0xc1])(actor)) {
            reinterpret_cast<unsigned char*>(DAT_011dea3c)[0x7c4] = 1;
            break;
        }
        iterator = iterator->FUN_00726070();
    }
    if (first != 0) {
        first->FUN_00470470();
        delete first;
    }
}