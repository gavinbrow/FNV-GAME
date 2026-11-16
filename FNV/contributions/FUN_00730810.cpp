
struct Parent {
    void* vptr;
    Parent();
};
struct Section {
    unsigned int count;
    unsigned int capacity;
    Section();
    ~Section();
};
struct FUN_00730810 : Parent {
    Section section;
    void* container;
    void* selected;
    void* scrollbar;
    const char* templateName;
    unsigned short nextIndex;
    float totalHeight;
    float lastSelection;
    float lastScrollbar;
    unsigned short flags;
    FUN_00730810();
    void __thiscall FUN_007a1950(int, int);
};
extern void* DAT_01070890;
void __cdecl FUN_00721130(FUN_00730810*);
FUN_00730810::FUN_00730810() {
    vptr = &DAT_01070890;
    scrollbar = 0;
    selected = 0;
    container = 0;
    templateName = 0;
    flags = 0;
    nextIndex = 0;
    lastScrollbar = 0.0f;
    lastSelection = 0.0f;
    totalHeight = 0.0f;
    FUN_007a1950(0,1);
    FUN_00721130(this);
}
