struct TextureSlotB63 { int unk00; int unk04; OwnerStandIn* receiver; };
struct TextureContainerB63 { int unk00; TextureSlotB63* node; void FUN_00ba3aa0(unsigned int index, void* item); };
struct TextureAllocationManagerB63 { void* FUN_00aa3e40(unsigned int bytes); };
extern TextureAllocationManagerB63 DAT_011f6238;
inline void* operator new(unsigned int bytes) { return DAT_011f6238.FUN_00aa3e40(bytes); }
struct TextureManagerB63 { RefBase* FUN_00b6e110(void* settings, int dimensions, void* p1, void* p2, void* p3); };
extern void* DAT_011f4748;
struct TextureOwnerB63 {
    int unk000;
int unk004;
int unk008;
int unk00c;
int unk010;
int unk014;
int unk018;
int unk01c;
int unk020;
int unk024;
int unk028;
int unk02c;
int unk030;
int unk034;
int unk038;
int unk03c;
int unk040;
int unk044;
int unk048;
int unk04c;
int unk050;
int unk054;
int unk058;
int unk05c;
int unk060;
int unk064;
int unk068;
int unk06c;
int unk070;
int unk074;
int unk078;
int unk07c;
int unk080;
int unk084;
int unk088;
int unk08c;
int unk090;
    TextureContainerB63 container;
    int FUN_00b63c60();
};
int TextureOwnerB63::FUN_00b63c60() {
    if (!container.node->receiver) {
        ISTexture* created = new ISTexture;
        container.FUN_00ba3aa0(2, &created);
    }
    OwnerStandIn** getterSlot = &container.node->receiver;
    if (!reinterpret_cast<FUN_00ba3770_struct*>(*getterSlot)->FUN_00ba3770()) {
        OwnerStandIn** receiverSlot = &container.node->receiver;
        (*receiverSlot)->FUN_00ba37a0(
            reinterpret_cast<TextureManagerB63*>(DAT_011f91a8)->FUN_00b6e110(DAT_011f4748, 32, 0, 0, 0));
    }
    OwnerStandIn** finalSlot = &container.node->receiver;
    return reinterpret_cast<FUN_00ba3770_struct*>(*finalSlot)->FUN_00ba3770();
}