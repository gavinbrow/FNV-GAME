struct Bound_af60 {
    float x;
    float y;
    float z;
    float radius;
};
extern Bound_af60 DAT_011f4288;
struct Props_af60 {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int m_1c;
    unsigned int m_20;
};
struct Geom_af60 {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    Bound_af60* m_20;
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
    int unk80;
    int unk84;
    int unk88;
    int unk8c;
    int unk90;
    int unk94;
    int unk98;
    int unk9c;
    int unka0;
    int unka4;
    Props_af60* m_a8;
    Bound_af60* GetBound() { return m_20 ? m_20 : &DAT_011f4288; }
};
struct Item_af60 {
    Geom_af60* m_00;
    unsigned short m_04;
};
struct Node1_af60 {
    Node1_af60* m_next;
    Node1_af60* m_prev;
    Item_af60* m_data;
};
struct NodeList1_af60 {
    Node1_af60* m_head;
    Node1_af60* m_tail;
    Node1_af60* m_free;
    int m_count;
    void RemoveHead()
    {
        Node1_af60* n = m_head;
        if (n) {
            if (n == m_tail) {
                m_tail = 0;
            }
            Node1_af60* next = 0;
            if (m_head->m_next) {
                next = n->m_next;
                next->m_prev = 0;
            }
            if (m_free) {
                m_free->m_prev = m_head;
            }
            m_head->m_next = m_free;
            m_count--;
            m_free = m_head;
            m_head = next;
        }
    }
};
struct List1_af60 {
    unsigned short unk00;
    unsigned short m_02;
    int unk04;
    int unk08;
    int unk0c;
    NodeList1_af60 m_list;
};
struct Sub2c_af60 {
    void FUN_00b64ec0();
};
struct Obj_af60 {
    virtual void v00(); virtual void v01(); virtual void v02(); virtual void v03();
    virtual void v04(); virtual void v05(); virtual void v06(); virtual void v07();
    virtual void v08(); virtual void v09(); virtual void v10(); virtual void v11();
    virtual void v12(); virtual void v13(); virtual void v14(); virtual void v15();
    virtual void v16(); virtual void v17(); virtual void v18(); virtual void v19();
    virtual void v20(); virtual void v21(); virtual void v22(); virtual void v23();
    virtual void v24(); virtual void v25(); virtual void v26(); virtual void v27();
    virtual void v28(); virtual void v29(); virtual void v30(); virtual void v31();
    virtual void v32(); virtual void v33(); virtual void v34(); virtual void v35();
    virtual void SetState(int a, int b, int c);
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
    Sub2c_af60 m_2c;
};
struct Entry_af60 {
    unsigned char m_flags;
    unsigned char unk01;
    unsigned short m_02;
    int unk04;
    Obj_af60* m_08;
    int m_0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    float m_20;
    void FUN_00b9a410();
};
struct Node2_af60 {
    Node2_af60* m_next;
    Node2_af60* m_prev;
    Entry_af60* m_data;
};
struct List2_af60 {
    Node2_af60* m_head;
    Node2_af60* m_tail;
    int m_count;
    void RemoveHead();
};
struct Lock_af60 {
    int m_owner;
    void FUN_0040fbf0(int a);
};
struct Mgr_af60 {
    void FUN_00aa4060(Entry_af60* e);
};
struct Point3_af60 {
    float x;
    float y;
    float z;
    Point3_af60(float ax, float ay, float az) : x(ax), y(ay), z(az) {}
};
struct Cam_af60 {
    int unk00;
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
    float m_68;
    int unk6c;
    int unk70;
    float m_74;
    int unk78;
    int unk7c;
    float m_80;
};
extern Lock_af60 DAT_011c5f80;
extern int DAT_011c5f84;
extern Node2_af60* DAT_011c5f58;
extern Mgr_af60 DAT_011f6238;
extern int DAT_011f91b8;
extern char DAT_011ad80f;
extern float DAT_01200458;
extern int DAT_011ff9dc;
extern int DAT_011ff9e4;
extern double DAT_01016978;
void __cdecl FUN_00b99990(int* p, int a);
void __cdecl FUN_00b97e30(int a, int b);
void __cdecl FUN_00b98320(float f, int a);
void __cdecl FUN_00b994f0(Item_af60* item, unsigned int a, int b, int c, int d);
extern "C" int __cdecl _isnan(double);
struct Renderer_af60 {
    int unk00;
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
    List1_af60* m_70[2];
    List2_af60 m_78[2];
    void FUN_00b9af60(int idx, Cam_af60* cam, bool flag, float maxDist);
};
inline void List2_af60::RemoveHead()
{
    Node2_af60* n = m_head;
    m_head = n->m_next;
    if (m_head) {
        m_head->m_prev = 0;
    } else {
        m_tail = 0;
    }
    n->m_data = 0;
    DAT_011c5f80.FUN_0040fbf0(0);
    n->m_prev = 0;
    n->m_next = DAT_011c5f58;
    DAT_011c5f84 -= 1;
    DAT_011c5f58 = n;
    if (DAT_011c5f84 == 0) {
        DAT_011c5f80.m_owner = 0;
    }
    m_count--;
}
static __forceinline float CalcDist(Item_af60* a, const Point3_af60& dir, bool flag)
{
    if (flag) {
        Bound_af60* b = a->m_00->GetBound();
        Bound_af60* b2 = a->m_00->GetBound();
        float d = b->x * dir.x + b->y * dir.y + b->z * dir.z;
        return d - b2->radius;
    }
    Bound_af60* b = a->m_00->GetBound();
    return b->x * dir.x + b->y * dir.y + b->z * dir.z;
}
void Renderer_af60::FUN_00b9af60(int idx, Cam_af60* cam, bool flag, float maxDist)
{
    Point3_af60 dir(cam->m_68, cam->m_74, cam->m_80);
    List1_af60* l1 = m_70[idx];
    Node1_af60* n = l1->m_list.m_head;
    Item_af60* a = n ? n->m_data : 0;
    float dist = 0.0f;
    if (a) {
        dist = CalcDist(a, dir, flag);
    }
    Entry_af60* e = m_78[idx].m_count ? m_78[idx].m_head->m_data : 0;
    maxDist -= DAT_01016978;
    do {
        while (e && (e->m_20 > dist || !a) && e->m_20 >= maxDist) {
            if ((e->m_flags & 1) > 0) {
                FUN_00b99990(&e->m_0c, 1);
            } else if (e->m_08) {
                e->m_08->SetState(1, 0x2f1, 1);
            }
            if (e->m_08) {
                e->m_08->m_2c.FUN_00b64ec0();
            }
            e->m_02 = 0;
            e->FUN_00b9a410();
            DAT_011f6238.FUN_00aa4060(e);
            m_78[idx].RemoveHead();
            e = m_78[idx].m_count ? m_78[idx].m_head->m_data : 0;
        }
        if (a && dist >= maxDist) {
            Props_af60* p = a->m_00->m_a8;
            if (p && !(DAT_011f91b8 == 9 && (p->m_1c == 0x15 || p->m_1c == 0x11))) {
                bool restore;
                if ((p->m_20 & 0x4000000) > 0 || (p->m_20 & 0x8000000) > 0) {
                    float f = DAT_01200458;
                    restore = true;
                    if (!DAT_011ad80f) {
                        f = 0.0f;
                    }
                    FUN_00b97e30(0, 1);
                    FUN_00b98320(f, 1);
                } else {
                    restore = false;
                }
                FUN_00b994f0(a, a->m_04, 1, 1, 1);
                if (restore) {
                    DAT_011ff9dc -= 1;
                    FUN_00b97e30(1, 0);
                    DAT_011ff9e4 -= 1;
                    FUN_00b98320(0.0f, 0);
                }
            }
            List1_af60* l = m_70[idx];
            if (l->m_list.m_head) {
                l->m_02--;
                l->m_list.RemoveHead();
            }
            l = m_70[idx];
            Node1_af60* node = l->m_list.m_head;
            a = node ? node->m_data : 0;
            if (a) {
                dist = CalcDist(a, dir, flag);
            }
        }
    } while (((a && dist >= maxDist) || (e && e->m_20 >= maxDist)) && !_isnan(dist));
}
