
struct ScopedMenuAccess {
    int handle;
    ScopedMenuAccess(int kind, int enabled, const char* fileName, int line);
    ~ScopedMenuAccess();
};
struct MenuFrame;
struct MenuFrameProvider {
    MenuFrame* FUN_00877720();
};
struct MenuFrame {
    void FUN_00a237b0();
};
extern MenuFrameProvider* DAT_011dea0c;
struct MenuGate {
    bool FUN_00451530();
};
extern MenuGate* DAT_011dea10;
extern char DAT_0106ef50;
extern double DAT_01012070;
extern int DAT_011d8a90;

struct MenuComponent {
    virtual ~MenuComponent();
    bool FUN_00712380();
    bool FUN_00a01230(int);
    void FUN_00700320(int trait, int enable);
    MenuComponent* FUN_0056c7f0();
    void FUN_00450f90(int);
    void FUN_00a04640(int);
    void FUN_007123f0();
    void FUN_007123a0();
};
struct MenuActor {
    MenuComponent* FUN_00726070();
    int FUN_0059bb30();
    void FUN_007037c0(int mode);
};
struct MenuSource {
    MenuActor* FUN_00a03c90();
};
struct MenuList {
    int FUN_00559450();
    MenuSource** FUN_0057cbe0(int* frame);
};
struct MenuCollection {
    int bookkeeping;
    MenuList list;
};
struct MenuState {
    MenuCollection* FUN_00586150();
    int FUN_00714f00();
    int FUN_00714f70(int);
    void FUN_00712450(MenuComponent* source, float amount, float offset);
    void FUN_00711ea0();
};
float __cdecl FUN_00716660(MenuActor*);
double __cdecl FUN_00408840(float);
MenuComponent* __stdcall FUN_004e3270(float);
MenuComponent* __stdcall FUN_004e3270(int);
bool __cdecl FUN_004b71d0();

void MenuState::FUN_00711ea0()
{
    ScopedMenuAccess scope(13, 1, &DAT_0106ef50, 0xca1);
    MenuFrame* cursor = DAT_011dea0c->FUN_00877720();
    *reinterpret_cast<unsigned char*>(reinterpret_cast<char*>(this) + 0x11) = 0;
    int frame = FUN_00586150()->list.FUN_00559450();
    while (frame != 0) {
        MenuSource* src = *FUN_00586150()->list.FUN_0057cbe0(&frame);
        MenuActor* actor = 0;
        if (src) actor = src->FUN_00a03c90();
        if (actor && actor->FUN_00726070() && !actor->FUN_00726070()->FUN_00712380()) {
            float amount = FUN_00716660(actor);
            bool leftSlot = FUN_00408840(amount) == DAT_01012070;
            int selection = actor->FUN_0059bb30();
            int rightSlot = FUN_00714f00();
            int direction = FUN_00714f70(0);
            int threshold = FUN_00714f70(1);
            if (selection == 2) {
                bool shouldUpdate = ((rightSlot == 0 && direction == 0) ||
                                     (direction != 0 && threshold == 0 && direction == 1001));
                if (actor && leftSlot) {
                    actor->FUN_007037c0(4);
                    if (actor->FUN_00726070()->FUN_00a01230(0x1772)) {
                        if (actor->FUN_00726070()) {
                            delete actor->FUN_00726070();
                        }
                        actor = 0;
                        frame = 0;
                    } else {
                        actor->FUN_00726070()->FUN_00700320(0xfa3, 0);
                        FUN_00712450(actor->FUN_00726070()->FUN_0056c7f0(), 0.0f, 0.0f);
                        if (shouldUpdate) {
                            FUN_004e3270(0.0f)->FUN_007123f0();
                            FUN_004e3270(0)->FUN_007123a0();
                        }
                    }
                } else {
                    *reinterpret_cast<unsigned char*>(reinterpret_cast<char*>(this) + 0x11) = 1;
                    actor->FUN_00726070()->FUN_00700320(0xfa3, 1);
                    FUN_00712450(actor->FUN_00726070()->FUN_0056c7f0(), 1.0f - amount, 0.0f);
                    if (shouldUpdate) FUN_004e3270(1.0f - amount)->FUN_007123f0();
                }
            } else if (selection == 8) {
                bool shouldUpdate = ((rightSlot != 0 && direction == rightSlot && rightSlot != 1001) ||
                                     (threshold != 0 && threshold == rightSlot && direction == 1001));
                if (leftSlot) {
                    actor->FUN_00726070()->FUN_00700320(0xfa3, 1);
                    FUN_00712450(actor->FUN_00726070()->FUN_0056c7f0(), 1.0f, 0.0f);
                    actor->FUN_007037c0(1);
                    if (shouldUpdate) {
                        FUN_004e3270(1.0f)->FUN_007123f0();
                        FUN_004e3270(0)->FUN_007123a0();
                    }
                } else {
                    *reinterpret_cast<unsigned char*>(reinterpret_cast<char*>(this) + 0x11) = 1;
                    actor->FUN_00726070()->FUN_00700320(0xfa3, 1);
                    FUN_00712450(actor->FUN_00726070()->FUN_0056c7f0(), amount, 0.0f);
                    if (shouldUpdate) FUN_004e3270(amount)->FUN_007123f0();
                }
            }
        }
    }
    if (*reinterpret_cast<int*>(reinterpret_cast<char*>(this) + 0xc) == 4 &&
        (!*reinterpret_cast<unsigned char*>(reinterpret_cast<char*>(this) + 0x11) ||
         DAT_011dea10->FUN_00451530())) {
        cursor->FUN_00a237b0();
        *reinterpret_cast<int*>(reinterpret_cast<char*>(this) + 0xc) = 1;
        if (!FUN_004b71d0() ||
            *reinterpret_cast<unsigned char*>(reinterpret_cast<char*>(this) + 0x7d)) {
            reinterpret_cast<MenuComponent*>(*reinterpret_cast<void**>(reinterpret_cast<char*>(this) + 0x28))
                ->FUN_0056c7f0()->FUN_00450f90(1);
            reinterpret_cast<MenuComponent*>(*reinterpret_cast<void**>(reinterpret_cast<char*>(this) + 0x28))
                ->FUN_00700320(0xfa3, 0);
        }
        reinterpret_cast<MenuComponent*>(*reinterpret_cast<void**>(reinterpret_cast<char*>(this) + 0x28))
            ->FUN_00a04640(1);
        *reinterpret_cast<int*>(reinterpret_cast<char*>(this) + 0x14c) = 0;
    }
    DAT_011d8a90 = 99;
}
