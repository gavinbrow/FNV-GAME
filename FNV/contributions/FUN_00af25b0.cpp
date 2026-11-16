struct PoolX
{
    void* FUN_00aa3e40(unsigned int size);
};

extern PoolX DAT_011f6238;

template <class T>
struct BSSimpleList
{
    T item;
    BSSimpleList* next;

    BSSimpleList(const T& value) : item(value), next(0)
    {
    }

    static void* operator new(unsigned int size)
    {
        return DAT_011f6238.FUN_00aa3e40(size);
    }

    void FUN_00af25b0(const T& value);
};

// @fnv 0x00af25b0
template <>
void BSSimpleList<unsigned char*>::FUN_00af25b0(unsigned char* const& value)
{
    if (value == 0)
    {
        return;
    }

    BSSimpleList* current = this;

    while (current->next != 0)
    {
        current = current->next;
    }

    if (current->item != 0)
    {
        current->next = new BSSimpleList(value);
    }
    else
    {
        current->item = value;
    }
}
