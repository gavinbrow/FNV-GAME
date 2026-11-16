class SkySound {
public:
    void* field00;
    void* field04;
    void* field08;
    unsigned int field0c;
    void* field10;
    void* field14;
};

SkySound** __fastcall FUN_006815c0(void* node);
void* __fastcall FUN_00726070(void* node);

struct FUN_0063e060_shell {
    unsigned char pad0[0xfc];
    void* pSkySoundList;
    bool FUN_0063e060(void* pWeather, unsigned int uiType);
};

bool FUN_0063e060_shell::FUN_0063e060(void* pWeather, unsigned int uiType) {
    for (void* node = pSkySoundList; node != 0 && *FUN_006815c0(node) != 0; node = FUN_00726070(node)) {
        if ((*FUN_006815c0(node))->field14 == pWeather && (*FUN_006815c0(node))->field0c == uiType)
            return true;
    }
    return false;
}
