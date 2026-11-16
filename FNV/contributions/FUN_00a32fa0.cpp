
#include <intrin.h>
struct S00a32fa0_Ctl {
    virtual void V00(); virtual void V01(); virtual void V02(); virtual void V03();
    virtual void V04(); virtual void V05(); virtual void V06(); virtual void V07();
    virtual void V08(); virtual void V09(); virtual void V10(); virtual void V11();
    virtual void V12(); virtual void V13(); virtual void V14(); virtual void V15();
    virtual void V16(); virtual void V17(); virtual void V18(); virtual void V19();
    virtual void V20(); virtual void V21(); virtual void V22(); virtual void V23();
    virtual void V24(); virtual void V25(); virtual void V26(); virtual void V27();
    virtual void V28(); virtual void V29(); virtual void V30(); virtual void V31();
    virtual void V32(); virtual void V33(); virtual void V34(); virtual void V35();
    virtual void V36(); virtual void V37(); virtual void V38(); virtual void V39();
    virtual void V40(); virtual void V41(); virtual void V42(); virtual void V43();
    virtual void V44(); virtual void V45(); virtual void V46(); virtual void V47();
    virtual unsigned short GetInterpolatorIndex(const FUN_00a312d0& tag);
    virtual void V49(); virtual void V50(); virtual void V51(); virtual void V52();
    virtual RefObj* GetInterpolator(unsigned short index);
};
struct S00a32fa0_RO : RefObj {
    void DecRef() {
        if (!InterlockedDecrement(&m_refCount))
            Release();
    }
};
struct S00a32fa0_SP {
    RefObj* m_p;
    S00a32fa0_SP& operator=(const S00a32fa0_SP& o) {
        if (m_p != o.m_p) {
            RefObj* old = m_p;
            if (old && InterlockedDecrement(&old->m_refCount) == 0)
                old->Release();
            m_p = o.m_p;
            if (m_p)
                InterlockedIncrement(&m_p->m_refCount);
        }
        return *this;
    }
    S00a32fa0_SP& operator=(RefObj* p) {
        if (m_p != p) {
            if (m_p)
                ((S00a32fa0_RO*)m_p)->DecRef();
            m_p = p;
            if (m_p)
                InterlockedIncrement(&m_p->m_refCount);
        }
        return *this;
    }
    void Drop() {
        RefObj* old = m_p;
        _ReadWriteBarrier();
        if (old && InterlockedDecrement(&old->m_refCount) == 0)
            old->Release();
    }
};
struct S00a32fa0_Item {
    RefObj* interpolator;
    S00a32fa0_SP controller;
    void* blend;
    unsigned char blendIndex;
    unsigned char priority;
    unsigned char pad0e;
    unsigned char pad0f;
};
struct S00a32fa0_Tag { char* m_a[5]; };
struct S00a32fa0_Arr {
    __declspec(noalias) bool FUN_00a317e0(int index, RefObj** output);
};
struct S00a32fa0_Seq : FUN_00a32bc0_cls {
    float weight;
    void* textKeys;
    int cycleType;
    float frequency;
    float beginTime;
    float endTime;
    void FUN_00a32fa0(S00a32fa0_Seq* destination, int, int, bool remove);
};
extern int DAT_011f49e0;
extern unsigned short DAT_01096320;

void S00a32fa0_Seq::FUN_00a32fa0(S00a32fa0_Seq* destination, int, int, bool remove)
{
    if (remove) {
        for (unsigned int i = 0; i < destination->m_count; ++i) {
            S00a32fa0_SP object = {0};
            ((S00a32fa0_Arr*)destination)->FUN_00a317e0(i, &object.m_p);
            object.Drop();
            _ReadWriteBarrier();
        }
    }
    if (cycleType == 2 || cycleType == 0)
        destination->cycleType = cycleType;
    destination->frequency = frequency;
    destination->beginTime = beginTime;
    destination->endTime = endTime;
    for (unsigned int i = 0; i < m_count; ++i) {
        S00a32fa0_Item& item = ((S00a32fa0_Item*)m_pSlots)[i];
        S00a32fa0_Ctl* controller = (S00a32fa0_Ctl*)item.controller.m_p;
        if (item.interpolator && controller) {
            const FUN_00a312d0* info = (FUN_00a312d0*)&m_pInfos[i];
            unsigned short index = controller->GetInterpolatorIndex(*info);
            if (index != DAT_01096320) {
                RefObj* interpolator = controller->GetInterpolator(index);
                S00a32fa0_Tag tag;
                unsigned int newIndex = destination->FUN_00a32bc0(interpolator,
                    (unsigned int)new (&tag) FUN_00a312d0((FixedStr&)DAT_011f49e0, (FixedStr&)DAT_011f49e0, (FixedStr&)DAT_011f49e0, (FixedStr&)DAT_011f49e0, (FixedStr&)DAT_011f49e0), 0xff);
                ((FUN_00a30750_shell*)&tag)->FUN_00a30750();
                S00a32fa0_Item& newItem = ((S00a32fa0_Item*)destination->m_pSlots)[newIndex];
                newItem.blend = item.blend;
                newItem.controller = item.controller;
                newItem.priority = item.priority;
            }
        }
    }
}
