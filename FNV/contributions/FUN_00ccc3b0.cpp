extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(volatile long*);
struct FNVRefObj;
struct FNVRefVTable {
    void (__thiscall *m_method00)(FNVRefObj*);
    void (__thiscall *m_release)(FNVRefObj*);
};
struct FNVRefObj {
    FNVRefVTable* m_vtable;
    volatile long m_refcount;
};
struct FNVHolder {
    void* m_vtable;
    FNVRefObj* m_object;
};
struct FNVParam {
    FNVRefObj* __thiscall FUN_00a63430();
};
struct FNVTarget {
    void* m_vtable;
    void __thiscall FUN_00c84cc0(FNVParam*);
    void __thiscall FUN_00ccc3b0(FNVParam*);
};
typedef FNVHolder* (__thiscall *FNVQuery)(FNVTarget*, bool*);

void FNVTarget::FUN_00ccc3b0(FNVParam* param)
{
    bool initialized;
    FNVHolder* holder = reinterpret_cast<FNVQuery*>(m_vtable)[45](this, &initialized);
    FNVRefObj* object = param->FUN_00a63430();
    FNVRefObj* oldObject = holder->m_object;
    if (oldObject != object) {
        if (oldObject && InterlockedDecrement(&oldObject->m_refcount) == 0)
            oldObject->m_vtable->m_release(oldObject);
        holder->m_object = object;
        if (object)
            InterlockedIncrement(&object->m_refcount);
    }
    FUN_00c84cc0(param);
}