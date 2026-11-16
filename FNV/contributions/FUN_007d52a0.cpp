

extern "C" const char str_0107702c[];

extern double DAT_01012060;

extern float DAT_0105559c;

extern unsigned int DAT_011dac64;

extern bool __cdecl FUN_00703d50();

extern void __cdecl FUN_00717280(int);

extern unsigned int __cdecl FUN_00457fe0();

extern int __cdecl FUN_0072fa60(int);

extern "C" int __cdecl FUN_00a00940(const char*, int);

extern void __cdecl FUN_00703e80(const char*, int, int, int, int, int, float, float, const char*, int);

extern void __cdecl FUN_007cfe40();

extern "C" __declspec(dllimport) unsigned long __stdcall GetTickCount();



struct InputDevice_7d {

    int FUN_00a24180(unsigned int, int);

    bool FUN_00a24fc0(unsigned int, int, unsigned char);

    int FUN_00a23a30();

    int FUN_00a23a50(unsigned int, int);

    int FUN_00a236b0(int);

    int FUN_00a234c0(int, unsigned int, int);

    int FUN_00a236d0(int);

    unsigned int FUN_00a235f0(int, int);

    int FUN_00a24660(int, int);

    void FUN_00a25180(unsigned int, int, unsigned char);

    int FUN_00a23390(int,int);

};

struct MenuTile_7d {

    bool FUN_00a07fc0(int);

    double FUN_00a011b0(int);

    void FUN_00700320(int, int);

    void FUN_00a01350(int, const char*);

};

struct ActionEntry_7d {

    int first;

    int second;

    int third;

    unsigned int actionCode;

};

struct ActionList_7d {

    ActionEntry_7d* FUN_007a1910();

    void FUN_007d74f0(bool);

    void FUN_007d7b50(bool);

    void FUN_007314c0(void (__cdecl*)(), int, int);

};

struct DialogSetting_7d {

    const char* FUN_004c69f0();

    const char* FUN_00403df0();
    const char* FUN_00403df0(int);

};

extern DialogSetting_7d g_011d4750;

extern DialogSetting_7d g_011d3108;

extern DialogSetting_7d* g_011d5730[];



struct StartMenuInput_7d : StartMenu {

    bool FUN_004a4080(unsigned int flag);

    void FUN_007d01b0();

    void FUN_007d61e0(int index, int value, unsigned int trait, float delay);

    bool FUN_007ce8f0();

    void FUN_0075f6f0(int index, bool enable);

    bool FUN_007d52a0();

};



static InputDevice_7d* GetInputDevice_7d()

{

    return reinterpret_cast<InputDevice_7d*>(g_osGlobals->FUN_00877720());

}



static void ShowInvalidBindingMessage_7d()

{

    const char* details = reinterpret_cast<DialogSetting_7d*>(&g_011d38b8)->FUN_004c69f0();

    const char* label = g_011d4750.FUN_00403df0();

    FUN_00703e80(label, 0, 0, 0, 1, 0x12, 0.0f, 0.0f, details, 0);

}



bool StartMenuInput_7d::FUN_007d52a0()

{

    if (FUN_004a4080(0x1000)) {

    if (reinterpret_cast<MenuTile_7d*>(pTiles[2])->FUN_00a07fc0(FUN_00a00940(str_0107702c, -1))) {

        if (reinterpret_cast<MenuTile_7d*>(pTiles[2])->FUN_00a011b0(FUN_00a00940(str_0107702c, -1)) == DAT_01012060) {

            FUN_007d01b0();

            FUN_007d61e0(2, 1, FUN_00a00940(str_0107702c, -1), DAT_0105559c);

            reinterpret_cast<MenuTile_7d*>(pTiles[15])->FUN_00700320(0x1004, !static_cast<int>(FUN_004b71d0()));

        } else if (FUN_007ce8f0() && !FUN_00703d50()) {

            bool mapped = false;

            

            const unsigned int action = reinterpret_cast<ActionList_7d*>(&lbOptions)->FUN_007a1910()->actionCode;

            



            switch ((*reinterpret_cast<const int*>(reinterpret_cast<const char*>(this) + 0x1c8))) {
            case 0: {

                unsigned int key = 0;
                while ((key & 0x100) == 0) {

                    if ((reinterpret_cast<InputDevice_7d*>(g_osGlobals->FUN_00877720()))->FUN_00a24180(key, 1)) {

                        mapped = (reinterpret_cast<InputDevice_7d*>(g_osGlobals->FUN_00877720()))->FUN_00a24fc0(action, 0, static_cast<unsigned char>(key)) || key == 1;

                        FUN_00717280(10);

                        if (!mapped)

                            {

                    FUN_00703e80(g_011d4750.FUN_00403df0(), 0, 0, 0, 1, 0x12, 0.0f, 0.0f, reinterpret_cast<DialogSetting_7d*>(&g_011d38b8)->FUN_004c69f0(), 0);

                }

                        break;

                    }
                    ++key;

                }

            } break;
            case 1: {

                for (int key = 0; !mapped && key < (reinterpret_cast<InputDevice_7d*>(g_osGlobals->FUN_00877720()))->FUN_00a23a30(); ++key) {

                    if ((reinterpret_cast<InputDevice_7d*>(g_osGlobals->FUN_00877720()))->FUN_00a23a50(key, 1)) {

                        FUN_00717280(10);

                        mapped = (reinterpret_cast<InputDevice_7d*>(g_osGlobals->FUN_00877720()))->FUN_00a24fc0(action, 1, static_cast<unsigned char>(key));

                    }

                }

                if ((reinterpret_cast<InputDevice_7d*>(g_osGlobals->FUN_00877720()))->FUN_00a24660(0x1c, 1)) {

                    mapped = true;

                    (reinterpret_cast<InputDevice_7d*>(g_osGlobals->FUN_00877720()))->FUN_00a25180(action, 1, 0xff);

                    FUN_00717280(10);

                }

            } break;
            case 2: {

                for (int key = 0; !mapped && key < (reinterpret_cast<InputDevice_7d*>(g_osGlobals->FUN_00877720()))->FUN_00a236b0(0); ++key) {

                    if ((reinterpret_cast<InputDevice_7d*>(g_osGlobals->FUN_00877720()))->FUN_00a234c0(0, key, 1)) {

                        mapped = (reinterpret_cast<InputDevice_7d*>(g_osGlobals->FUN_00877720()))->FUN_00a24fc0(action, 2, static_cast<unsigned char>(key));

                        FUN_00717280(10);

                    }

                }

                for (int key = 0; !mapped && key < (reinterpret_cast<InputDevice_7d*>(g_osGlobals->FUN_00877720()))->FUN_00a236d0(0); ++key) {

                    unsigned int mappedKey = (reinterpret_cast<InputDevice_7d*>(g_osGlobals->FUN_00877720()))->FUN_00a235f0(0, key);

                    mapped = mappedKey != 0xffffffff &&

                             FUN_00457fe0() >= DAT_011dac64 &&

                             (reinterpret_cast<InputDevice_7d*>(g_osGlobals->FUN_00877720()))->FUN_00a24fc0(action, 2, static_cast<unsigned char>(mappedKey));

                    FUN_00717280(10);

                    if (mapped)

                        DAT_011dac64 = GetTickCount() + 100;

                }

                if ((reinterpret_cast<InputDevice_7d*>(g_osGlobals->FUN_00877720()))->FUN_00a24660(0x1c, 1)) {

                    mapped = true;

                    (reinterpret_cast<InputDevice_7d*>(g_osGlobals->FUN_00877720()))->FUN_00a25180(action, 2, 0xff);

                    FUN_00717280(10);

                }

            } break;
            }

            if (mapped) {

                reinterpret_cast<ActionList_7d*>(&lbOptions)->FUN_007d74f0(true);

                reinterpret_cast<ActionList_7d*>(&lbOptions)->FUN_007d7b50(true);

                reinterpret_cast<ActionList_7d*>(&lbOptions)->FUN_007314c0(&FUN_007cfe40, 0, 0x7fffffff);

                reinterpret_cast<MenuTile_7d*>(pTiles[16])->FUN_00a01350(0xfc4, g_011d5730[*reinterpret_cast<const int*>(reinterpret_cast<const char*>(this) + 0x1c8)]->FUN_00403df0(1));

                FUN_0075f6f0(2, true);

            }

        }



        if (FUN_004b71d0() && FUN_007ce8f0()) {

            int b;
            int a;
            b = (reinterpret_cast<InputDevice_7d*>(g_osGlobals->FUN_00877720()))->FUN_00a23390(0, 9);
            a = (reinterpret_cast<InputDevice_7d*>(g_osGlobals->FUN_00877720()))->FUN_00a23390(0, 10);

            if (FUN_0072fa60(b) > 0x21f1 || FUN_0072fa60(a) > 0x21f1) {

                FUN_00717280(10);

                {

                    FUN_00703e80(g_011d3108.FUN_00403df0(), 0, 0, 0, 1, 0x12, 0.0f, 0.0f, reinterpret_cast<DialogSetting_7d*>(&g_011d38b8)->FUN_004c69f0(), 0);

                }

            }

        }

    }

    return true;

    } else {
        return false;
    }
}

