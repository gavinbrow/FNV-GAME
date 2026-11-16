extern "C" void __fastcall FUN_00717600(InterfaceManager*);
extern "C" void __cdecl FUN_00704170(int, int);
extern "C" void __cdecl FUN_007048f0(int, int, int);
extern "C" void __cdecl FUN_00704c10(int, int);

void __cdecl FUN_00703500(void)
{
    if (FUN_004b7210() != 0) {
        if (((InterfaceManagerPC*)FUN_004b7210())->GetKey()) {
            InterfaceManager* iMenu = FUN_004b7210();
            int pManager = (int)iMenu->FUN_00586150()->GetFloat(0x1771);
            if (pManager == 0) {
                FUN_00717600(FUN_004b7210());
                pManager = 0x3eb;
            }
            switch (pManager) {
            case 0x3ff:
                FUN_00704170(1, 0);
                break;
            case 0x3ea:
            case 0x40b:
            case 0x425:
                FUN_007048f0(1, 0, 1);
                break;
            case 0x3eb:
                FUN_00704c10(1, 0);
                break;
            }
        }
    }
}