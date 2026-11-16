extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long* value);
struct CloneHandle;
struct MeshObject {
    virtual void OnBeginDestroy();
    virtual void Destroy();
    volatile long refCount;
    CloneHandle __thiscall FUN_00c20fd0() throw();
};
struct CloneHandle {
    MeshObject* pointer;
    ~CloneHandle() throw() {
        if (pointer) {
            MeshObject* oldObject = pointer;
            if (InterlockedDecrement(&oldObject->refCount) == 0) {
                oldObject->Destroy();
            }
        }
    }
    void Clear() {
        if (pointer) {
            MeshObject* oldObject = pointer;
            if (InterlockedDecrement(&oldObject->refCount) == 0) {
                oldObject->Destroy();
            }
            pointer = 0;
        }
    }
    CloneHandle& __thiscall FUN_006e5cc0(const CloneHandle& other) throw();
};
struct MeshLookup {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    unsigned int unk30;
    unsigned int unk34;
    unsigned int unk38;
    unsigned int unk3c;
    unsigned int unk40;
    unsigned int unk44;
    unsigned int unk48;
    unsigned int unk4c;
    unsigned int unk50;
    unsigned int unk54;
    unsigned int unk58;
    unsigned int unk5c;
    unsigned int unk60;
    unsigned int unk64;
    unsigned int unk68;
    unsigned int unk6c;
    unsigned int unk70;
    unsigned int unk74;
    unsigned int unk78;
    unsigned int unk7c;
    unsigned int unk80;
    unsigned int unk84;
    unsigned int unk88;
    MeshObject** meshes;
    unsigned short unk90;
    unsigned short meshCount;
    void __thiscall FUN_00c21340(unsigned int index, CloneHandle* result);
};
void MeshLookup::FUN_00c21340(unsigned int index, CloneHandle* result)
{
    if (index >= meshCount) {
        result->Clear();
        return;
    }
    if (meshes[index] == 0) {
        result->Clear();
        return;
    }
    result->FUN_006e5cc0(meshes[index]->FUN_00c20fd0());
}