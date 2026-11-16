struct ItemBinding
{
    int m_iId;
    int unk04;
    int unk08;
    int unk0c;
};

struct Item
{
    virtual ~Item();
    virtual void DeleteThis();

    volatile long m_uiRefCount;
    int unk08;
    unsigned int m_uiBindingCount;
    int unk10;
    ItemBinding* m_pBindings;
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
    int m_iFlag;
};

class Registry
{
public:
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
    Item** m_ppItems;
    unsigned short unk3c;
    unsigned short m_usItemCount;

    Item* __thiscall FUN_00a2e570(int iId, bool bFlag);
};

extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(
    volatile long*);
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(
    volatile long*);

Item::~Item()
{
}

void Item::DeleteThis()
{
}

Item* __thiscall Registry::FUN_00a2e570(int iId, bool bFlag)
{
    unsigned int uiIndex = 0;

    while (uiIndex < m_usItemCount)
    {
        Item* pItem = m_ppItems[uiIndex];

        if (pItem != 0)
        {
            InterlockedIncrement(&pItem->m_uiRefCount);

            if (!bFlag || pItem->m_iFlag != 0)
            {
                unsigned int uiBindingIndex = 0;

                while (uiBindingIndex < pItem->m_uiBindingCount)
                {
                    ItemBinding* pBinding = pItem->m_pBindings + uiBindingIndex;
                    int iBindingId = pBinding->m_iId;

                    if (iBindingId != 0 && iBindingId == iId)
                    {
                        if (InterlockedDecrement(&pItem->m_uiRefCount) == 0)
                        {
                            pItem->DeleteThis();
                        }

                        return pItem;
                    }

                    ++uiBindingIndex;
                }
            }

            if (InterlockedDecrement(&pItem->m_uiRefCount) == 0)
            {
                pItem->DeleteThis();
            }
        }

        ++uiIndex;
    }

    return 0;
}