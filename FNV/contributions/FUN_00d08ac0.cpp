inline void* operator new(unsigned int, void* location) { return location; }
struct Target {
    int unk00;
};

struct Item1 {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    Target m_target;
};

struct Item2 {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    Target m_target;
};

struct AllocHolder {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    void* m_alloc;
};

void* FUN_00c85750();
void FUN_00c90940(void* alloc, void* array, int elemSize);

template <typename T>
struct hkArray {
    T* m_data;
    int m_size;
    int m_capacityAndFlags;

    void pushBack(AllocHolder* h, T val) {
        if (m_size == (m_capacityAndFlags & 0x3fffffff)) {
            FUN_00c90940(h->m_alloc, this, sizeof(T));
        }
        T* slot = m_data + m_size;
        __assume(slot != 0);
        new (slot) T(val);
        ++m_size;
    }
};

struct SubStruct1 {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    int unk20;
    int unk24;
    int unk28;
    int unk2C;
    int unk30;
    int unk34;
    int unk38;
    int unk3C;
    int unk40;
    int unk44;
    hkArray<Item1*> m_items;
};

struct Container {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    int unk20;
    int unk24;
    hkArray<SubStruct1*> m_array1;
    int unk34;
    int unk38;
    int unk3C;
    int unk40;
    int unk44;
    int unk48;
    int unk4C;
    int unk50;
    int unk54;
    int unk58;
    int unk5C;
    int unk60;
    int unk64;
    int unk68;
    int unk6C;
    int unk70;
    int unk74;
    int unk78;
    int unk7C;
    int unk80;
    int unk84;
    int unk88;
    int unk8C;
    int unk90;
    int unk94;
    int unk98;
    int unk9C;
    int unkA0;
    int unkA4;
    int unkA8;
    int unkAC;
    int unkB0;
    int unkB4;
    int unkB8;
    int unkBC;
    int unkC0;
    int unkC4;
    int unkC8;
    int unkCC;
    int unkD0;
    int unkD4;
    int unkD8;
    int unkDC;
    int unkE0;
    int unkE4;
    int unkE8;
    int unkEC;
    int unkF0;
    int unkF4;
    int unkF8;
    int unkFC;
    int unk100;
    int unk104;
    int unk108;
    int unk10C;
    hkArray<Item2*> m_array2;
};

void FUN_00d08ac0(hkArray<Target*>* out, int containerHandle) {
    Container* c = reinterpret_cast<Container*>(containerHandle);
    for (containerHandle = 0; containerHandle < c->m_array1.m_size; containerHandle++) {
        for (int j = 0; j < c->m_array1.m_data[containerHandle]->m_items.m_size; j++) {
            out->pushBack((AllocHolder*)FUN_00c85750(), &c->m_array1.m_data[containerHandle]->m_items.m_data[j]->m_target);
        }
    }
    for (int k = 0; k < c->m_array2.m_size; k++) {
        if (c->m_array2.m_data[k]->m_target.unk00) {
            out->pushBack((AllocHolder*)FUN_00c85750(), &c->m_array2.m_data[k]->m_target);
        }
    }
}
