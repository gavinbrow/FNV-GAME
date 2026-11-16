struct DeleteInterface { virtual void first(); virtual void second(); virtual void deleteObject(void*, unsigned short); };
struct Manager { int unk00; int unk04; int unk08; int unk0c; DeleteInterface* iface; };
Manager* __cdecl FUN_00c85750();
struct FUN_00cd2900_owner { int unk00; unsigned short unk04; void FUN_00cd2690(); void* FUN_00cd2900(unsigned flags); };
void* FUN_00cd2900_owner::FUN_00cd2900(unsigned flags) {
    FUN_00cd2690();
    if (flags & 1) {
        Manager* manager=FUN_00c85750();
        manager->iface->deleteObject(this,unk04);
    }
    return this;
}

