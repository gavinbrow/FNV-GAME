struct NiPoint3 { float x; float y; float z; };
struct CA8B80Command;
struct CA8B80Queue { void __thiscall Push(CA8B80Command*); };
struct FUN_00ca8a30_Class {
    int m_0; int m_4; CA8B80Queue* m_8;
    void __thiscall FUN_00ca8a30(NiPoint3*);
    void __thiscall FUN_00561800(NiPoint3*);
};
struct FUN_00ca8a30_Local {
    unsigned char m_b; FUN_00ca8a30_Class* m_p;
    float m_x; float m_y; float m_z;
};
void __thiscall FUN_00ca8a30_Class::FUN_00ca8a30(NiPoint3* p)
{
    if (m_8 && *(int*)((char*)m_8 + 0x94)) {
        FUN_00ca8a30_Local l;
        l.m_p = this;
        l.m_x = p->x;
        l.m_b = 0x1a;
        l.m_y = p->y;
        l.m_z = p->z;
        m_8->Push((CA8B80Command*)&l);
    } else {
        FUN_00561800(p);
    }
}