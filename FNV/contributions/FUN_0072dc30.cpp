struct ListObj;
struct NodeS;
struct PtrObj {
    PtrObj* FUN_00559450();
    void** FUN_006815c0();
    void FUN_005ae3d0(void** pp);
};
struct EntryObj {
    ~EntryObj();
    void* FUN_0044ddc0();
    const char* FUN_004be2d0();
    int FUN_004459e0(int a);
    PtrObj* FUN_00559450();
    void* FUN_00726070();
};
struct NodeS {
    void* m_00; void* m_04;
    NodeS* FUN_00726070();
    EntryObj** FUN_006815c0();
};
struct ListObj {
    virtual void vtbl000();
    virtual int PredHead();
    virtual void vtbl002();
    virtual void vtbl003();
    virtual void vtbl004();
    virtual void vtbl005();
    virtual void vtbl006();
    virtual void vtbl007();
    virtual void Virt20(void* fn);
    void* m_04; void* m_08; void* m_0c; void* m_10; void* m_14;
    void* m_18; void* m_1c; void* m_20; void* m_24; void* m_28; void* m_2c;
    void FUN_0071a200(int a);
    int FUN_0071a320(void* e, const char* s, int a, int b);
    void FUN_00719ef0(void* a, void* fn, int b, int c, int d, int e);
    void FUN_007314c0(void* fn, int a, int b);
    void FUN_00730bb0(void* fn);
    unsigned int FUN_0071ae60();
    void FUN_00731360(int a);
    void FUN_007312e0();
    void* FUN_007d6e90(int a, int b);
};
struct LocalList {
    void* m_00; void* m_04;
    LocalList();
    ~LocalList();
    void FUN_00470470();
};
struct NewObj {
    void* m_00;
    int m_04;
    void* m_08;
    NewObj(void* a, int b);
    PtrObj* FUN_00559450();
    const char* FUN_004be2d0();
};
struct DataSource { void FUN_004d4b00(int arg, LocalList* out); };
struct DataHandler {
    void* FUN_00740960();
    void FUN_0046f310(void* a);
};
struct TileLike {
    void FUN_00700320(int a, int b);
};
extern DataHandler* g_dataHandler;
struct PlayerCharacter;
extern PlayerCharacter* g_thePlayer;
extern int DAT_011d8fb4;
void* __cdecl FUN_004bf220(void* a);
class InventoryEntry;
bool __cdecl FUN_0072e6c0(EntryObj* e);
unsigned char __cdecl FUN_004b71d0();
void* __cdecl FUN_004b7210();
void __cdecl AddHeadImpl(void* list, void** pp);
void __cdecl FUN_0072f210();
void __cdecl FUN_0072f070();
struct IMObj {
    void FUN_00715860(void* a);
};

struct Self72 {
    virtual void vtbl000();
    virtual void vtbl001();
    virtual void vtbl002();
    virtual void Virt0c(int a, int b);
    virtual void Virt10(int a, int b);
        int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    int unk40;
    int unk44;
    int unk48;
    int unk4c;
    int unk50;
    int unk54;
    int unk58;
    int unk5c;
    int unk60;
    int unk64;
    int unk68;
    int unk6c;
    int unk70;
    int unk74;
    int unk78;
    int unk7c;
    void* m_80;
        int unk84;
    int unk88;
    int unk8c;
    int unk90;
    int unk94;
    int unk98;
    int unk9c;
    int unka0;
    int m_a4;
    ListObj m_a8;
    ListObj m_d8;
    ListObj* m_108;
    NodeS m_10c;
    NodeS m_114;
    void FUN_0072db60();
    void __thiscall FUN_0072dc30(int arg);
};

void __thiscall Self72::FUN_0072dc30(int arg)
{
    long i = 0;
    if (m_108 != 0) {
        if (m_108->PredHead()) {
            m_108->FUN_007312e0();
        }
    }
    if (arg != 0) {
        LocalList b;
        void* n;
        n = FUN_004bf220((void*)g_thePlayer);
        void* res = g_dataHandler->FUN_00740960();
        if (n != 0) {
            ((DataSource*)n)->FUN_004d4b00(arg, &b);
            m_a8.FUN_0071a200(arg);
            NodeS* kZero = (NodeS*)&b;
            for (; kZero != 0 && *kZero->FUN_006815c0() != 0; kZero = kZero->FUN_00726070()) {
                if (!(bool)FUN_0072e570((InventoryEntry*)*kZero->FUN_006815c0())) {
                    m_a8.FUN_0071a320(*kZero->FUN_006815c0(), (*kZero->FUN_006815c0())->FUN_004be2d0(), 0, 0);
                } else {
                    delete *kZero->FUN_006815c0();
                }
            }
            b.FUN_00470470();
        }
        if (res != 0) {
            ((DataSource*)res)->FUN_004d4b00(arg, &b);
            m_d8.FUN_0071a200(arg);
            NodeS* kZero;
            kZero = (NodeS*)&b;
            for (; kZero != 0 && *kZero->FUN_006815c0() != 0; kZero = kZero->FUN_00726070()) {
                if (!(bool)FUN_0072e6c0(*kZero->FUN_006815c0())) {
                    m_d8.FUN_0071a320(*kZero->FUN_006815c0(), (*kZero->FUN_006815c0())->FUN_004be2d0(), 0, 0);
                } else {
                    delete *kZero->FUN_006815c0();
                }
            }
            b.FUN_00470470();
        }
    } else {
        g_dataHandler->FUN_0046f310(m_80);
        m_a8.FUN_00719ef0((void*)g_thePlayer, (void*)::FUN_0072e570, 0, 0, 0, 0);
        m_d8.FUN_00719ef0(m_80, (void*)FUN_0072e6c0, 0, 0, 0, 1);
    }
    {
        NodeS* kZero;
        kZero = &m_10c;
        for (; kZero != 0 && *kZero->FUN_006815c0() != 0; kZero = kZero->FUN_00726070()) {
            if (arg == 0 || (*kZero->FUN_006815c0())->FUN_0044ddc0() == (void*)arg) {
            int tmp;
            NewObj* r = new NewObj((*kZero->FUN_006815c0())->FUN_0044ddc0(), (int)(*kZero->FUN_006815c0())->FUN_00726070());
            void* _tempExtra;
            _tempExtra = (*kZero->FUN_006815c0())->FUN_00559450() ? *(void**)(*kZero->FUN_006815c0())->FUN_00559450()->FUN_006815c0() : 0;
            tmp = 0;
            if (0 != _tempExtra) {
                r->FUN_00559450()->FUN_005ae3d0(&_tempExtra);
            }
            tmp = m_a8.FUN_0071a320(r, r->FUN_004be2d0(), 0, 0);
            ((TileLike*)tmp)->FUN_00700320(DAT_011d8fb4, 1);
            }
        }
    }
    {
        NodeS* kZero;
        kZero = &m_114;
        for (; kZero != 0 && *kZero->FUN_006815c0() != 0; kZero = kZero->FUN_00726070()) {
            if (arg == 0 || (*kZero->FUN_006815c0())->FUN_0044ddc0() == (void*)arg) {
            long tmp;
            NewObj* r;
            void* _tempExtra;
            r = new NewObj((*kZero->FUN_006815c0())->FUN_0044ddc0(), (int)(*kZero->FUN_006815c0())->FUN_00726070());
            _tempExtra = (*kZero->FUN_006815c0())->FUN_00559450() ? *(void**)(*kZero->FUN_006815c0())->FUN_00559450()->FUN_006815c0() : 0;
            tmp = 0;
            if (_tempExtra != 0) {
                r->FUN_00559450()->FUN_005ae3d0(&_tempExtra);
            }
            tmp = m_d8.FUN_0071a320(r, r->FUN_004be2d0(), 0, 0);
            ((TileLike*)tmp)->FUN_00700320(DAT_011d8fb4, 1);
            }
        }
    }
    m_a8.FUN_007314c0((void*)FUN_0072eac0, 0, 0x7fffffff);
    m_a8.FUN_007314c0((void*)FUN_0072f210, 0, 0x7fffffff);
    m_a8.FUN_00730bb0((void*)FUN_007304b0);
    m_a8.Virt20((void*)FUN_0072f070);
    m_d8.FUN_007314c0((void*)FUN_0072f210, 0, 0x7fffffff);
    m_d8.FUN_00730bb0((void*)FUN_007304b0);
    m_d8.Virt20((void*)FUN_0072f070);
    if (0 == m_108) {
        if (FUN_004b71d0()) {
            m_108 = &m_d8;
        }
    }
    if (0 != m_108) {
        if (m_108->FUN_0071ae60() > 0) {
            m_108->FUN_00731360(1);
        } else {
            m_a4 = -1;
            Virt0c((m_108 == &m_a8) ? 4 : 9, 0);
            m_a4 = 3;
            if (m_108->FUN_0071ae60() > 0) {
                m_108->FUN_00731360(1);
            } else {
                Virt10((m_108 == &m_a8) ? 1 : 0, 0);
                if (FUN_004b71d0()) {
                    ((IMObj*)FUN_004b7210())->FUN_00715860(m_108->FUN_007d6e90(0xfc3, 1));
                }
            }
        }
    }
    FUN_0072db60();
}
