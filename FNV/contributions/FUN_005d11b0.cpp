struct ValueStore { virtual int Read(unsigned int index); };
struct GameManager { void FUN_0093a7c0(unsigned int index, int value); };
extern "C" GameManager* DAT_011dea3c;
extern bool __cdecl FUN_005accb0(unsigned int, unsigned int, unsigned int, unsigned int, unsigned int, unsigned int, unsigned int, unsigned int*, int*);
extern bool __cdecl FUN_005d1260(unsigned int);
bool __cdecl FUN_005d11b0(unsigned int input, unsigned int actor, unsigned int flags, unsigned int context, unsigned int extra, unsigned int script, unsigned int unused, unsigned int value)
{
    int delta;
    {
        unsigned int actorValueIndex;
        actorValueIndex = 0;
        delta = 0;
        if (!FUN_005accb0(input, actor, value, flags, context, extra, script, &actorValueIndex, &delta))
            return false;
        if (FUN_005d1260(actorValueIndex)) {
            int previous = reinterpret_cast<ValueStore*>(reinterpret_cast<char*>(DAT_011dea3c) + 0xa4)->Read(actorValueIndex);
            previous += delta;
            DAT_011dea3c->FUN_0093a7c0(actorValueIndex, previous);
        }
        return true;
    }
}