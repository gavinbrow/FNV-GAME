struct RecipeEntry;
struct MenuNode {
    MenuNode* FUN_00a03c90(MenuNode* context, int choice, int flags);
    RecipeEntry* FUN_00a1ddb0();
    int FUN_00a00f30(int key);
    void FUN_00700320(int key, int value);
    void FUN_00a01350(int key, int value, int flags);
    float FUN_00a011b0(int index);
    MenuNode* FUN_00a00e90(int key);
    void FUN_00a09200();
    void FUN_00a09130(int property, RecipeEntry* source, int key);
    void FUN_00a09080(int property, float value);
    void FUN_00a09410(int flags);
};

struct RecipeEntry {
    int m_status;
    int m_item;
    int m_data;
    RecipeEntry(RecipeEntry* parent, int* selection);
    int FUN_00a00f30(int key);
    void FUN_00700320(int key, int value);
    void FUN_00a01350(int key, int value, int flags);
};

struct RecipeList {
    int m_first;
    int m_last;
    void FUN_007a7eb0(RecipeEntry* recipe, int insertAt);
    void FUN_00905820(RecipeEntry* const& recipe);
};

extern "C" double DAT_01012060;
extern "C" char UNK_0106f860;
int __cdecl FUN_00a00940(const void* key, int fallback);

struct RecipePanel {
    int m_context;
    RecipeList m_recipes;
    MenuNode* m_parent;
    int m_unused10;
    int m_unused14;
    int m_defaultItem;
    unsigned short m_nextIndex;
    unsigned short m_flags;
    int m_updateCounter;
    int m_state;
    int m_lastAction;

    bool FUN_007242c0(int flags);
    void FUN_0072bb60();
    void FUN_007269d0(RecipeEntry* recipe);
    void FUN_0072c000();
    int FUN_00726c40();
    RecipeEntry* FUN_00729ae0(int selection, int updateChoice, int insertAt, int parentId);
};

RecipeEntry* RecipePanel::FUN_00729ae0(int selection, int updateChoice, int insertAt, int parentId)
{
    if (m_parent != 0 && (m_defaultItem != 0 || parentId != 0)) {
    RecipeEntry* current = m_parent->FUN_00a03c90(m_parent, parentId != 0 ? parentId : m_defaultItem, 0)->FUN_00a1ddb0();
    if (!current->FUN_00a00f30(0xfaa))
        current->FUN_00700320(0xfaa, -1);
    if (updateChoice != 0)
        current->FUN_00a01350(0xfc4, updateChoice, 1);

    if (insertAt != 0) {
        m_recipes.FUN_007a7eb0(new RecipeEntry(current, &selection), insertAt);
        if (FUN_007242c0(0))
            FUN_0072bb60();
    }
    else {
        m_recipes.FUN_00905820(new RecipeEntry(current, &selection));
        if (FUN_007242c0(0)) {
            FUN_007269d0(current);
            FUN_0072c000();
        }
        current->FUN_00700320(0xfac, m_nextIndex++);
    }

    if (FUN_00726c40() == 1) {
        if (m_parent->FUN_00a011b0(FUN_00a00940(&UNK_0106f860, -1)) > DAT_01012060) {
            MenuNode* notifier = m_parent->FUN_00a00e90(0xfb0);
            notifier->FUN_00a09200();
            notifier->FUN_00a09130(0x7d0, current, 0xfb0);
            notifier->FUN_00a09080(0x7d3, m_parent->FUN_00a011b0(FUN_00a00940(&UNK_0106f860, -1)));
            notifier->FUN_00a09410(0);
        }
    }
    return current;
    }
    else {
        return 0;
    }
}