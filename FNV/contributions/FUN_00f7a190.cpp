class GlobalObject_0040c150
{
public:
    char data[12];
    GlobalObject_0040c150(const char* name, const char* value);
};
extern const char DAT_010636e4[];
extern const char DAT_010636f4[];
extern const char DAT_010636cc[];
extern const char DAT_010636dc[];
extern const char DAT_010636b0[];
extern const char DAT_010636c0[];
extern const char DAT_0106368c[];
extern const char DAT_0106369c[];
extern GlobalObject_0040c150* DAT_011d5730;
extern GlobalObject_0040c150* DAT_011d5734;
extern GlobalObject_0040c150* DAT_011d5738;
extern GlobalObject_0040c150* DAT_011d573c;
// @fnv 0x00f7a190
void FUN_00f7a190()
{
    DAT_011d5730 = new GlobalObject_0040c150(DAT_010636e4,DAT_010636f4);
    DAT_011d5734 = new GlobalObject_0040c150(DAT_010636cc,DAT_010636dc);
    DAT_011d5738 = new GlobalObject_0040c150(DAT_010636b0,DAT_010636c0);
    DAT_011d573c = new GlobalObject_0040c150(DAT_0106368c,DAT_0106369c);
}
