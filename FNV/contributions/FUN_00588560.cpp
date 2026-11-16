struct FUN_00588560_shell : TESWorldSpace {
    TESObjectREFR* FUN_00588560(void* apMatch);
};

extern int __cdecl FUN_00404dc0(void* apReference, void* apMatch);

typedef void* (__thiscall* TESObjectREFR_GetForm)(TESObjectREFR*);

TESObjectREFR* FUN_00588560_shell::FUN_00588560(void* apMatch)
{
    TESObjectREFR* pResult = 0;
    if (apMatch) {
        void* pPosition = reinterpret_cast<MapX*>(cellMap)->GetFirstPos();
        while (pPosition && !pResult) {
            TESObjectREFR* pReference = 0;
            unsigned int uiKey;
            reinterpret_cast<NiTMap*>(cellMap)->GetNext(pPosition, uiKey, reinterpret_cast<void*&>(pReference));
            if (pReference &&
                !FUN_00404dc0(
                    (reinterpret_cast<TESObjectREFR_GetForm*>(*reinterpret_cast<void**>(pReference)))[76](pReference),
                    apMatch)) {
                pResult = pReference;
            }
        }
    }
    return pResult;
}