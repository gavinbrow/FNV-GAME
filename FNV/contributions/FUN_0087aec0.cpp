
struct PhysicsState {
    virtual void vfn_0000();
    virtual void vfn_0004();
    virtual void vfn_0008();
    virtual void vfn_000c();
    virtual void vfn_0010();
    virtual void vfn_0014();
    virtual void vfn_0018();
    virtual void vfn_001c();
    virtual void vfn_0020();
    virtual void vfn_0024();
    virtual void vfn_0028();
    virtual void vfn_002c();
    virtual void vfn_0030();
    virtual void vfn_0034();
    virtual void vfn_0038();
    virtual void vfn_003c();
    virtual void vfn_0040();
    virtual void vfn_0044();
    virtual void vfn_0048();
    virtual void vfn_004c();
    virtual void vfn_0050();
    virtual void vfn_0054();
    virtual void vfn_0058();
    virtual void vfn_005c();
    virtual void vfn_0060();
    virtual void vfn_0064();
    virtual void vfn_0068();
    virtual void vfn_006c();
    virtual void vfn_0070();
    virtual void vfn_0074();
    virtual void vfn_0078();
    virtual void vfn_007c();
    virtual void vfn_0080();
    virtual void vfn_0084();
    virtual void vfn_0088();
    virtual void vfn_008c();
    virtual void vfn_0090();
    virtual void vfn_0094();
    virtual void vfn_0098();
    virtual void vfn_009c();
    virtual void vfn_00a0();
    virtual void vfn_00a4();
    virtual void vfn_00a8();
    virtual void vfn_00ac();
    virtual void vfn_00b0();
    virtual void vfn_00b4();
    virtual void vfn_00b8();
    virtual void vfn_00bc();
    virtual void vfn_00c0();
    virtual void vfn_00c4();
    virtual void vfn_00c8();
    virtual void vfn_00cc();
    virtual void vfn_00d0();
    virtual void vfn_00d4();
    virtual void vfn_00d8();
    virtual void vfn_00dc();
    virtual void vfn_00e0();
    virtual void vfn_00e4();
    virtual void vfn_00e8();
    virtual void vfn_00ec();
    virtual void vfn_00f0();
    virtual void vfn_00f4();
    virtual void vfn_00f8();
    virtual void vfn_00fc();
    virtual void vfn_0100();
    virtual void vfn_0104();
    virtual void vfn_0108();
    virtual void vfn_010c();
    virtual void vfn_0110();
    virtual void vfn_0114();
    virtual void vfn_0118();
    virtual void vfn_011c();
    virtual void vfn_0120();
    virtual void vfn_0124();
    virtual void vfn_0128();
    virtual void vfn_012c();
    virtual void vfn_0130();
    virtual void vfn_0134();
    virtual void vfn_0138();
    virtual void vfn_013c();
    virtual void vfn_0140();
    virtual void vfn_0144();
    virtual void vfn_0148();
    virtual void vfn_014c();
    virtual void vfn_0150();
    virtual void vfn_0154();
    virtual void vfn_0158();
    virtual void vfn_015c();
    virtual void vfn_0160();
    virtual void vfn_0164();
    virtual void vfn_0168();
    virtual void vfn_016c();
    virtual void vfn_0170();
    virtual void vfn_0174();
    virtual void vfn_0178();
    virtual void vfn_017c();
    virtual void vfn_0180();
    virtual void vfn_0184();
    virtual void vfn_0188();
    virtual void vfn_018c();
    virtual void vfn_0190();
    virtual void vfn_0194();
    virtual void vfn_0198();
    virtual void vfn_019c();
    virtual void vfn_01a0();
    virtual void vfn_01a4();
    virtual void vfn_01a8();
    virtual void vfn_01ac();
    virtual void vfn_01b0();
    virtual void vfn_01b4();
    virtual void vfn_01b8();
    virtual void vfn_01bc();
    virtual void vfn_01c0();
    virtual void vfn_01c4();
    virtual void vfn_01c8();
    virtual void vfn_01cc();
    virtual int IsEligible();
};
struct ActorController {
    PhysicsState* FUN_00822b40();
};
struct EntityRef {
    ActorController* FUN_0059bb30();
};
struct FUN_0087aec0_shell : TaskQueueInterface {
    void FUN_0087aec0(EntityRef* reference);
    void FUN_0087d160(const FakeTask& task);
};
void FUN_0087aec0_shell::FUN_0087aec0(EntityRef* reference)
{
    if (reference) {
        FakeTask task;
        task.i0 = 0x12;
        if (reference->FUN_0059bb30()->FUN_00822b40()) {
            if (reference->FUN_0059bb30()->FUN_00822b40()->IsEligible()) {
                task.p1 = reference;
                FUN_0087d160(task);
            }
        } else {
            task.p1 = reference;
            FUN_0087d160(task);
        }
    }
}
