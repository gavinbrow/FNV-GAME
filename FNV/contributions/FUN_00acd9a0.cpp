int __cdecl FUN_00ecda70(void* resource);
struct ResourceOwner { virtual void unusedVirtual(); virtual int query(int index);
unsigned int m_unknown04;
unsigned int m_unknown08;
unsigned int m_unknown0c;
unsigned int m_unknown10;
unsigned int m_unknown14;
unsigned int m_unknown18;
unsigned int m_unknown1c;
unsigned int m_unknown20;
unsigned int m_unknown24;
unsigned int m_unknown28;
unsigned int m_unknown2c;
unsigned int m_unknown30;
unsigned int m_unknown34;
unsigned int m_unknown38;
unsigned int m_unknown3c;
unsigned int m_unknown40;
unsigned int m_unknown44;
unsigned int m_unknown48;
void* m_resource; int FUN_00acd9a0();
};
int ResourceOwner::FUN_00acd9a0() {
    int value; int invalid;
    return (m_resource != 0 && (value = query(-1), invalid = -1, ((unsigned char)(short)(invalid == value)) == 0)
        && FUN_00ecda70(m_resource) < 0) ? -1 : 0;
}