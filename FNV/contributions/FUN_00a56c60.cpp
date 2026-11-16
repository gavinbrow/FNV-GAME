
extern int (__stdcall *DAT_00fdf1c0)(void*);

struct S_00a56c60 : S_00a56c10 {
    void FUN_00a56c60(NiRefObject* nextFirst, NiRefObject* nextSecond);
};

void S_00a56c60::FUN_00a56c60(NiRefObject* nextFirst, NiRefObject* nextSecond)
{
    int (__stdcall *decrement)(void*) = DAT_00fdf1c4;
    NiRefObject* previous = _0C;
    if (previous != nextFirst) {
        if (previous != 0) {
            if (decrement(&previous->m_ref) == 0)
                previous->Unk_04();
        }
        _0C = nextFirst;
        if (nextFirst != 0)
            DAT_00fdf1c0(&nextFirst->m_ref);
    }

    previous = _10;
    if (previous != nextSecond) {
        if (previous != 0) {
            if (decrement(&previous->m_ref) == 0)
                previous->Unk_04();
        }
        _10 = nextSecond;
        if (nextSecond != 0)
            DAT_00fdf1c0(&nextSecond->m_ref);
    }
}
