struct FUN_007ff820_shell : public FUN_007ff7c0_shell {
    bool FUN_007ff820();
};

struct AudioClock : public FUN_007ff8c0_shell {};
struct AudioFallback {};

float __fastcall FUN_006d2c40(AudioClock* clock);
bool __fastcall FUN_007faf10(FUN_007ff820_shell* surface);
void __fastcall FUN_007181d0(AudioFallback* fallback);
AudioFallback* __stdcall FUN_004b7210(int mode);

bool FUN_007ff820_shell::FUN_007ff820()
{
    if (*((unsigned char*)this + 0xec)) {
        if (!g_011db63c
            || !((AudioClock*)(unsigned int)g_011db63c)->FUN_007ff8c0()
            || *((float*)((char*)this + 0xe8)) == FUN_006d2c40((AudioClock*)(unsigned int)g_011db63c)) {
            FUN_007181d0(FUN_004b7210(0));
            return true;
        } else {
            *((float*)((char*)this + 0xe8)) = FUN_006d2c40((AudioClock*)(unsigned int)g_011db63c);
        }
    }
    return FUN_007faf10(this);
}