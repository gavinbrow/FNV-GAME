struct S00e0d180_Node;

struct S00e0d180_Array {
    S00e0d180_Node** m_data;
    int m_size;
    int m_capacityAndFlags;
    S00e0d180_Node*& operator[](int i) { return m_data[i]; }
};

struct S00e0d180_Node {
    float values[8];
    unsigned short counts[8];
    S00e0d180_Array children;
    double accumulatedValue;
    S00e0d180_Node* linked;
    const char* name;
    int flags;
    int unk54;
    void* operator new(unsigned int size) {
        return reinterpret_cast<FUN_00e0d000Heap&>(FUN_00c85750()->heap()).allocate(size);
    }
    S00e0d180_Node(S00e0d180_Node* parent, const char* name, int flags);
};

extern "C" void __cdecl FUN_00e0d180(void* first, void* second, int index, int limit, float amount)
{
    int lvl = index;
    if (lvl > 6) {
        lvl = 6;
    }
    index = 0;
    int i = 0;
    if (((S00e0d180_Node*)second)->children.m_size > 0) {
        double d = 1.0 - amount;
        int n = 0;
        do {
            S00e0d180_Node* src = ((S00e0d180_Node*)second)->children[i];
            S00e0d180_Node* dst;
            if (!FUN_00e0c690((unsigned int)((S00e0d180_Node*)second)->children[i]->name, &index, (FUN_00e0c690_owner*)first)) {
                void* slot = S00e0d180_Node::operator new(sizeof(S00e0d180_Node));
                if (slot) { int f = src->unk54; dst = ::new (slot) S00e0d180_Node((S00e0d180_Node*)first, src->name, f); }
                else dst = 0;
            } else {
                dst = ((S00e0d180_Node*)first)->children[index];
            }
            dst->values[lvl] = (float)((double)src->values[limit] * d + (double)dst->values[lvl]);
            dst->counts[lvl] = src->counts[limit];
            FUN_00e0d180(dst, src, lvl, limit, amount);
            n = ((S00e0d180_Node*)second)->children.m_size;
            if (index < n - 1) {
                ++index;
            }
            ++i;
        } while (i < n);
    }
}

