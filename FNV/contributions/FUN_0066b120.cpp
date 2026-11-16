
extern void* __cdecl FUN_00aa13e0(unsigned int size);
extern void* __cdecl FUN_00401000(unsigned int size);
extern float DAT_01016b78;
extern void* __cdecl FUN_0066b660();

struct FUN_00b4e150 {
    virtual ~FUN_00b4e150();
    FUN_00b4e150();
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
unsigned int unk8c;
unsigned int unk90;
unsigned int unk94;
unsigned int unk98;
unsigned int unk9c;
unsigned int unka0;
unsigned int unka4;
unsigned int unka8;
unsigned int unkac;
unsigned int unkb0;
unsigned int unkb4;
unsigned int unkb8;
unsigned int unkbc;
unsigned int unkc0;
unsigned int unkc4;
unsigned int unkc8;
unsigned int unkcc;
unsigned int unkd0;
unsigned int unkd4;
unsigned int unkd8;
unsigned int unkdc;
unsigned int unke0;
};
struct TreePointer {
    void* m_pObject;
    TreePointer(void* p);
    ~TreePointer();
    void FUN_0066b0d0(void* p);
    struct TreeLists* FUN_00559450();
};
struct TreeLists {
    unsigned short FUN_00669990();
    unsigned short FUN_006699d0();
    void* FUN_0066a630();
};
struct FUN_00a5ecb0 {
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
unsigned int unk8c;
unsigned int unk90;
unsigned int unk94;
unsigned int unk98;
unsigned int unk9c;
unsigned int unka0;
unsigned int unka4;
unsigned int unka8;
    FUN_00a5ecb0(int initial);
    static void* operator new(unsigned int size) { return FUN_00aa13e0(size); }
};
struct FUN_0051cf00 {
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
unsigned int unk8c;
unsigned int unk90;
unsigned int unk94;
unsigned int unk98;
unsigned int unk9c;
unsigned int unka0;
unsigned int unka4;
unsigned int unka8;
unsigned int unkac;
unsigned int unkb0;
    FUN_0051cf00();
    void FUN_0051d000(int enabled);
    void FUN_006404b0(float size, float a, float b, float c);
    static void* operator new(unsigned int size) { return FUN_00aa13e0(size); }
};
struct FUN_006694e0 {
    void* m_pObject;
    FUN_006694e0();
    ~FUN_006694e0();
    void FUN_0066b0d0(void* p);
    static void* operator new[](unsigned int size) { return FUN_00401000(size); }
};
struct FUN_0066b640 {
    virtual void v00();virtual void v04();virtual void v08();virtual void v0c();
    virtual void v10();virtual void v14();virtual void v18();virtual void v1c();
    virtual void v20();virtual void v24();virtual void v28();virtual void v2c();
    virtual void v30();virtual void v34();virtual void v38();virtual void v3c();
    virtual void v40();virtual void v44();virtual void v48();virtual void v4c();
    virtual void v50();virtual void v54();virtual void v58();virtual void v5c();
    virtual void v60();virtual void v64();virtual void v68();virtual void v6c();
    virtual void v70();virtual void v74();virtual void v78();virtual void v7c();
    virtual void v80();virtual void v84();virtual void v88();virtual void v8c(void*);
    unsigned int unk04, unk08, unk0c, unk10;
    FUN_0066b640();
    void FUN_00c6b980(void* p);
    static void* operator new(unsigned int size) { return FUN_00aa13e0(size); }
};
struct FUN_0066b120 : FUN_00b4e150 {
    TreePointer m_e4;
    FUN_006694e0* m_e8;
    FUN_006694e0* m_ec;
    TreePointer m_f0;
    float m_f4;
    virtual ~FUN_0066b120();
    FUN_0066b120(void* initial, void* external);

    void FUN_00b4dec0(int n);
    void FUN_004902f0(int n);
    void FUN_00a93ea0(int type, void* p);
    void FUN_00a5bca0(void* p);
};

FUN_0066b120::FUN_0066b120(void* initial, void* external)
    : m_e4(0), m_f0(0)
{
    FUN_00b4dec0(6);
    m_e4.FUN_0066b0d0(initial);
    FUN_004902f0(1);
    FUN_00a5ecb0* pkFirst = new FUN_00a5ecb0(0); FUN_00a93ea0(0,pkFirst); pkFirst = new FUN_00a5ecb0(0); FUN_00a93ea0(1,pkFirst);
    FUN_0066b640* pController;
    FUN_0051cf00* controller = new FUN_0051cf00();
    controller->FUN_0051d000(1);
    controller->FUN_006404b0(DAT_01016b78, 1.0f, 0.0f, 0.0f);
    FUN_00a93ea0(2, controller);

    unsigned short count;
    unsigned short i = m_e4.FUN_00559450()->FUN_00669990();
    if (i != 0) {
        m_e8 = new FUN_006694e0[i];
        for (count = 0; count < i; ++count)
            m_e8[count].FUN_0066b0d0(0);
    } else {
        m_e8 = 0;
    }
    i = m_e4.FUN_00559450()->FUN_006699d0();
    if (i != 0) {
        m_ec = new FUN_006694e0[i];
        for (count = 0; count < i; ++count)
            m_ec[count].FUN_0066b0d0(0);
    } else {
        m_ec = 0;
    }
    m_f0.FUN_0066b0d0(0);
    FUN_00a5bca0(FUN_0066b660());
    void* chosen = external ? external : m_e4.FUN_00559450()->FUN_0066a630();
    if (chosen) {
        pController = new FUN_0066b640();
        pController->FUN_00c6b980(external ? external : m_e4.FUN_00559450()->FUN_0066a630());
        pController->v8c(this);
    }
    m_f4 = 0.0f;
}
