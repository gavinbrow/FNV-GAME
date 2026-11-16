// Based on prior 2026-10-22 WIP by another contributor; rechecked by GPT-6.
#include "h_257f6998865a.h"
#include "h_173e1c54dad8.h"
#include "h_55de62c42fc8.h"
#include "h_468f728dbbb6.h"
#include "h_1af38281db46.h"
#include "h_f4fd41bc9389.h"

template <class Alloc, class K, class V> class NiTMapBase {
public:
    bool GetAt(const K key, V& val) const;
};

class NiCloningProcess {
public:
    NiTMapBase<NiTPointerAllocator<unsigned int>, NiObject*, NiObject*>* m_pkCloneMap;
};

struct NiObjectCloneBase {
    void ProcessClone(NiCloningProcess& kCloning);
};

inline void* FirstPos(const NiTFixedStringMap_NiAVObject___& m)
{
    for (unsigned int i = 0; i < m.m_uiHashSize; i++) {
        if (m.m_ppkHashTable[i])
            return m.m_ppkHashTable[i];
    }
    return 0;
}

struct PaletteShell : public NiDefaultAVObjectPalette {
    void FUN_00a6e5b0(NiCloningProcess& kCloning);
};

void PaletteShell::FUN_00a6e5b0(NiCloningProcess& kCloning)
{
    ((NiObjectCloneBase*)this)->ProcessClone(kCloning);

    NiFixedString kName;
    NiObject*& pkClone = reinterpret_cast<NiObject*&>(kName.m_kHandle);
    pkClone = 0;
    kCloning.m_pkCloneMap->GetAt(this, pkClone);
    PaletteShell* pkDest = (PaletteShell*)pkClone;

    if (m_pkScene) {
        kCloning.m_pkCloneMap->GetAt(m_pkScene, pkClone);
        pkDest->m_pkScene = (NiAVObject*)pkClone;
    }

    if (m_kHash.m_kAllocator.m_uiCount) {
        void* pos = FirstPos(m_kHash);
        while (pos) {
            kName.m_kHandle = EmptyFS.m_kHandle;
            NiAVObject* pkObj;
            m_kHash.GetNext(pos, kName, pkObj);
            if (kName.m_kHandle && pkObj) {
                NiObject* pkObjClone;
                if (kCloning.m_pkCloneMap->GetAt(pkObj, pkObjClone))
                    pkDest->SetAVObject(kName, (NiAVObject*)pkObjClone);
            }
            if (kName.m_kHandle != EmptyFS.m_kHandle)
                InterlockedDecrement((volatile long*)(kName.m_kHandle - 8));
        }
    }
}
