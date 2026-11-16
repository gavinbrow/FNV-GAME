extern void* __cdecl FUN_00c85750(void);
extern int DAT_010d07f4;
extern void __cdecl FUN_00dcda40(void*, void*, void*);
extern void __cdecl FUN_00c90940(void*, void*, int);

struct D4C2Place {};
inline void* operator new(unsigned int, void* p, D4C2Place) { __assume(p != 0); return p; }
inline void operator delete(void*, void*, D4C2Place) {}

struct BigType {
    int m_00;
    unsigned short m_04;
    unsigned short m_06;
    void* FUN_00c90b80(void);
};

struct ArrayField {
    int m_data;
    int m_size;
    int m_capacityAndFlags;
    __forceinline ArrayField() : m_data(0), m_size(0), m_capacityAndFlags(0x80000000) {}
};
struct SmallType {
    int m_00;
    unsigned short m_04;
    unsigned short m_06;
    int m_08;
    int m_0c;
    int m_10;
    int m_14;
    int m_18;
    int m_1c;
    int m_20;
    int m_24;
    int m_28;
    int m_2c;
    int m_30;
    int m_34;
    int m_38;
    int m_3c;
    unsigned char m_40;
    unsigned char m_41;
    unsigned char m_42;
    unsigned char m_43;
    ArrayField m_array;
    void FUN_00d065e0(void);
};

struct AllocType {
    virtual void vf00(void);
    virtual void* vf04(int);
};
struct HolderType {
    int m_00;
    int m_04;
    int m_08;
    int m_0c;
    AllocType* m_10;
};
struct ClientType {
    void FUN_00c91c50(void*);
    void FUN_00c93b30(void*);
};
struct ArrayType {
    SmallType** m_data;
    int m_size;
    int m_cap;
};
struct HostType {
    int m_00;
    int m_04;
    void* m_08;
    ArrayType m_0c;
    void FUN_00d4c2d0(ClientType*, unsigned char);
};

void HostType::FUN_00d4c2d0(ClientType* client, unsigned char value) {
    if (m_08 == 0) {
        HolderType* holder = (HolderType*)FUN_00c85750();
        BigType* big = (BigType*)holder->m_10->vf04(0xF0);
        big->m_04 = 0xF0;
        m_08 = big->FUN_00c90b80();
    }

    client->FUN_00c91c50(m_08);
    ArrayType* array = &m_0c;
    client->FUN_00c93b30(array);

    if (value != 0) {
        struct Local {
            unsigned char m_flag;
            int m_value;
        } local;

        local.m_flag = 0;
        local.m_value = 0;

        HolderType* holder = (HolderType*)FUN_00c85750();
        SmallType* small = (SmallType*)holder->m_10->vf04(0x50);
        small->m_04 = 0x50;
        small->FUN_00d065e0();

        small->m_00 = (int)&DAT_010d07f4;
        new (&small->m_array, D4C2Place()) ArrayField();

        FUN_00dcda40(&local, client, small);

        small->m_40 = 0;

        holder = (HolderType*)FUN_00c85750();
        if (array->m_size == (array->m_cap & 0x3fffffff)) {
            FUN_00c90940(holder->m_10, array, 4);
        }

        new (array->m_data + array->m_size, D4C2Place()) SmallType*(small);
        array->m_size++;
    }
}
