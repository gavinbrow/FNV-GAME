struct DispatchObject;
typedef int (__thiscall *DispatchAction)(DispatchObject*, void*);
struct DispatchObject {
    void** vtable;
    void* unk04;
    DispatchObject* unk08;
    int type;
    int Dispatch(void* argument) {
        return reinterpret_cast<DispatchAction>(vtable[0x38])(this, argument);
    }
};
struct DispatchContainer { void* unk00; void* argument; void* unk08; void* objectLink; };
typedef void* (__thiscall *GetTarget)(DispatchObject*);
int __cdecl FUN_00c80020(DispatchContainer* container) {
    void* link = container->objectLink;
    if (!link) link = container;
    DispatchObject* target = 0;
    if (link) {
        DispatchObject* object = *reinterpret_cast<DispatchObject**>(link);
        int type = object->type;
        if (type == 8 || type == 10) {
            void* result = reinterpret_cast<GetTarget>(object->vtable[4])(object);
            if (result) {
                char* wrapper = static_cast<char*>(result) - 0x10;
                if (wrapper) target = *reinterpret_cast<DispatchObject**>(wrapper + 8);
                else target = 0;
            } else target = 0;
        } else {
            DispatchObject* checked = *reinterpret_cast<DispatchObject**>(link);
            if (checked && type == 9) target = checked->unk08;
        }
    }
    int result = 0x24;
    if (target) result = target->Dispatch(container->argument);
    return result;
}