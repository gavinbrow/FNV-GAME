extern float DAT_0104da48;

struct ContactSource {
    int unk00; int unk04; int unk08; int unk0C;
    int unk10; int unk14; int unk18; int unk1C;
    int unk20; int unk24; int unk28;
    unsigned int m_collisionFilterInfo;
    void FUN_00c905b0();
};

struct ContactHit;

struct ContactListener {
    virtual void v00(); virtual void v04(); virtual void v08(); virtual void v0C();
    virtual void v10(); virtual void v14(); virtual void v18();
    virtual void OnEnter(ContactHit* hit);
    virtual void OnStay(ContactHit* hit);
};

struct ContactHandler {
    int unk00; int unk04; int unk08; int unk0C; int unk10; int unk14; int unk18; int unk1C;
    ContactListener* m_listener;
};

struct ContactUser {
    int unk000;
    int unk004;
    int unk008;
    int unk00C;
    int unk010;
    int unk014;
    int unk018;
    int unk01C;
    int unk020;
    int unk024;
    int unk028;
    int unk02C;
    int unk030;
    int unk034;
    int unk038;
    int unk03C;
    int unk040;
    int unk044;
    int unk048;
    int unk04C;
    int unk050;
    int unk054;
    int unk058;
    int unk05C;
    int unk060;
    int unk064;
    int unk068;
    int unk06C;
    int unk070;
    int unk074;
    int unk078;
    int unk07C;
    int unk080;
    int unk084;
    int unk088;
    int unk08C;
    int unk090;
    int unk094;
    int unk098;
    int unk09C;
    int unk0A0;
    int unk0A4;
    int unk0A8;
    int unk0AC;
    int unk0B0;
    int unk0B4;
    int unk0B8;
    int unk0BC;
    int unk0C0;
    int unk0C4;
    int unk0C8;
    int unk0CC;
    int unk0D0;
    int unk0D4;
    int unk0D8;
    int unk0DC;
    int unk0E0;
    int unk0E4;
    int unk0E8;
    int unk0EC;
    int unk0F0;
    int unk0F4;
    int unk0F8;
    int unk0FC;
    int unk100;
    int unk104;
    int unk108;
    int unk10C;
    int unk110;
    int unk114;
    int unk118;
    int unk11C;
    int unk120;
    int unk124;
    int unk128;
    int unk12C;
    int unk130;
    int unk134;
    int unk138;
    int unk13C;
    int unk140;
    int unk144;
    int unk148;
    int unk14C;
    int unk150;
    int unk154;
    int unk158;
    int unk15C;
    int unk160;
    int unk164;
    int unk168;
    int unk16C;
    int unk170;
    int unk174;
    int unk178;
    int unk17C;
    int unk180;
    int unk184;
    int unk188;
    int unk18C;
    int unk190;
    int unk194;
    int unk198;
    int unk19C;
    int unk1A0;
    int unk1A4;
    int unk1A8;
    int unk1AC;
    int unk1B0;
    int unk1B4;
    int unk1B8;
    int unk1BC;
    int unk1C0;
    int unk1C4;
    int unk1C8;
    int unk1CC;
    int unk1D0;
    int unk1D4;
    int unk1D8;
    int unk1DC;
    int unk1E0;
    int unk1E4;
    int unk1E8;
    int unk1EC;
    int unk1F0;
    int unk1F4;
    int unk1F8;
    int unk1FC;
    int unk200;
    int unk204;
    int unk208;
    int unk20C;
    int unk210;
    int unk214;
    int unk218;
    int unk21C;
    int unk220;
    int unk224;
    int unk228;
    int unk22C;
    int unk230;
    int unk234;
    int unk238;
    int unk23C;
    int unk240;
    int unk244;
    int unk248;
    int unk24C;
    int unk250;
    int unk254;
    int unk258;
    int unk25C;
    int unk260;
    int unk264;
    int unk268;
    int unk26C;
    int unk270;
    int unk274;
    int unk278;
    int unk27C;
    int unk280;
    int unk284;
    int unk288;
    int unk28C;
    int unk290;
    int unk294;
    int unk298;
    int unk29C;
    int unk2A0;
    int unk2A4;
    int unk2A8;
    int unk2AC;
    int unk2B0;
    int unk2B4;
    int unk2B8;
    int unk2BC;
    int unk2C0;
    int unk2C4;
    int unk2C8;
    int unk2CC;
    int unk2D0;
    int unk2D4;
    int unk2D8;
    int unk2DC;
    int unk2E0;
    int unk2E4;
    int unk2E8;
    int unk2EC;
    int unk2F0;
    int unk2F4;
    int unk2F8;
    int unk2FC;
    int unk300;
    int unk304;
    int unk308;
    int unk30C;
    int unk310;
    int unk314;
    int unk318;
    int unk31C;
    int unk320;
    int unk324;
    int unk328;
    int unk32C;
    int unk330;
    int unk334;
    int unk338;
    int unk33C;
    int unk340;
    int unk344;
    int unk348;
    int unk34C;
    ContactHandler* m_handler;
};

struct ContactOwner {
    int unk00; int unk04;
    ContactUser* m_user;
    void* getUserData() const { return m_user; }
};

struct ContactCollidable;
__forceinline void getUserOut(const ContactCollidable* c, ContactUser*& out);
struct ContactCollidable {
    int unk00; int unk04; int unk08; int unk0C;
    signed char m_ownerOffset;
    void* getOwner() const { return (char*)this + m_ownerOffset; }
};

struct ContactHit {
    int m_00; int m_04; int m_08; int m_0c;
    int m_10; int m_14; int m_18; int m_1c;
    int m_20; int m_24; int m_28; int m_2c;
    int m_30; int m_34; int m_38; int m_3c;
    int m_40; int m_44;
    ContactCollidable* m_collidable;
    int m_4c;
    int m_50; int m_54; int m_58; int m_5c;
    int m_60; int m_64; int m_68; int m_6c;
};

struct CopyBlock8 {
    unsigned int m_lo;
    unsigned int m_hi;
};

template <int N> struct MemCpyAligned {
    static __forceinline void copy(void* dst, const void* src)
    {
        const CopyBlock8* s = (const CopyBlock8*)src;
        CopyBlock8* d = (CopyBlock8*)dst;
        for (int i=0; i<N/8; i++) d[i]=s[i];
        if (N==4) *(unsigned int*)dst=*(const unsigned int*)src;
    }
};

__forceinline void getUserOut(const ContactCollidable* c, ContactUser*& out)
{
    ContactOwner* owner = (ContactOwner*)c->getOwner();
    out = owner ? owner->m_user : 0;
}

__forceinline void* getUserData(const ContactCollidable* c)
{
    const ContactOwner* owner = (const ContactOwner*)c->getOwner();
    return owner ? owner->getUserData() : 0;
}

__forceinline ContactUser* getUser(const ContactCollidable* c)
{
    ContactOwner* owner = (ContactOwner*)c->getOwner();
    return owner ? owner->m_user : 0;
}

__forceinline ContactUser* getUser2(const ContactCollidable* c)
{
    ContactOwner* owner = (ContactOwner*)c->getOwner();
    if (!owner) {
        return 0;
    }
    return owner->m_user;
}

template <class T> struct ContactArray {
    T* m_data;
    int m_size;
    int m_capacityAndFlags;
    int getSize() const { return m_size; }
    T& operator[](int i) { return m_data[i]; }
    void removeAt(int index)
    {
        m_size--;
        if (m_size != index) {
            MemCpyAligned<sizeof(T)>::copy(&m_data[index], &m_data[m_size]);
        }
    }
};

struct TriggerCollector : FUN_00cd3410 {
    ContactArray<ContactSource*>& sources() { return *(ContactArray<ContactSource*>*)&m_a1; }
    ContactArray<int>& states() { return *(ContactArray<int>*)&m_a2; }
    ContactArray<ContactHit>& hits() { return *(ContactArray<ContactHit>*)&m_a3; }
    void FUN_00cd32b0();
};

void TriggerCollector::FUN_00cd32b0()
{
    double val = DAT_0104da48;
    int& cnt=m_iHitsSize;
    cnt = 0;
    m_earlyOutDistance = (float)val;
    int i;
    for (i = 0; i < states().getSize(); i++) {
        unsigned int layer = sources()[i]->m_collisionFilterInfo & 0x7f;
        ContactOwner* owner = (ContactOwner*)hits()[i].m_collidable->getOwner();
        void* ud = owner ? owner->getUserData() : 0;
        ContactUser* user = (ContactUser*)ud;
        if (user) {
            ContactHandler* handler = user->m_handler;
            if (handler) {
                switch (layer) {
                case 14:
                case 16: {
                    ContactListener* listener = handler->m_listener;
                    if (listener) {
                        int state = states()[i];
                        if (state == 0) {
                            listener->OnEnter(&hits()[i]);
                        } else if (state == 1) {
                            listener->OnStay(&hits()[i]);
                        }
                    }
                    break;
                }
                }
            }
        }
    }
    for (i = states().getSize() - 1; i >= 0; i--) {
        if (states()[i] == 1) {
            sources()[i]->FUN_00c905b0();
            sources().removeAt(i);
            hits().removeAt(i);
            states().removeAt(i);
        } else {
            states()[i] = 1;
        }
    }
}
