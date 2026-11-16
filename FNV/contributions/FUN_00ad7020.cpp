struct StrSetX { int a; char flag; };
extern StrSetX g_str_011f6d9c;
extern "C" bool DAT_011f6da0;
extern bool DAT_01202800;
extern "C" __declspec(thread) unsigned int DAT_01272000[174];
struct BSAudioManager { void StartAudioThreads(); };
namespace sad7c50 { struct Settings; Settings* FUN_00ad9060(); }
class FUN_00aea150_Class { public: void FUN_00aea150(); };
inline unsigned int GetTls() { return DAT_01272000[173]; }
inline void SetTls(unsigned int v) { DAT_01272000[173] = v; }
inline bool& SelFlag() { return (&g_str_011f6d9c) ? DAT_011f6da0 : (DAT_01202800 = false); }
struct TlsScope {
    unsigned int oldValue;
    inline TlsScope() : oldValue(GetTls()) { DAT_01272000[173] = 11; }
    inline ~TlsScope() { SetTls(oldValue); }
};
struct AudioState {
    char pad0[4];
    bool ready, started, launchThreads;
    char pad1[13];
    FUN_00aea150_Class sub;
    void FUN_00ad7020(unsigned int initFlags);
};
// @fnv 0x00ad7020
void AudioState::FUN_00ad7020(unsigned int initFlags)
{
    TlsScope scope;
    if (!SelFlag())
    {
        ready = false;
        started = false;
        return;
    }
    sub.FUN_00aea150();
    if (launchThreads)
        reinterpret_cast<BSAudioManager*>(sad7c50::FUN_00ad9060())->StartAudioThreads();
    started = true;
}
