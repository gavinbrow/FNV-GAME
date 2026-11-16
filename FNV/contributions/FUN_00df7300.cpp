struct Param;
struct This {
    float FUN_00df7230(Param*);
    bool* FUN_00df7300(bool*, Param*);
};
bool* This::FUN_00df7300(bool* out, Param* p)
{
    ((This*)((char*)this - 4))->FUN_00df7230(p);
    *out = true;
    return out;
}
