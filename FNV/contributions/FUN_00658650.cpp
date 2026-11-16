struct Cursor {
    void* unk00;
    void* unk04;
};

struct Iterator {
    void* unk00;
    void* unk04;
    void FUN_006590c0(Cursor* pos, int flags);
    bool FUN_0065dfd0(void* handle);
    float* FUN_0064dbd0();
};

class Mgr {
public:
    void FUN_0044a170(Iterator* iter);
    void* FUN_0065f550(Cursor* key);
    Mgr* FUN_00658650(float scale);
};

Mgr* Mgr::FUN_00658650(float scale)
{
    Iterator iter;
    Cursor key;
    Cursor cur;
    for (this->FUN_0044a170(&iter); iter.FUN_0065dfd0(this->FUN_0065f550(&key)); iter.FUN_006590c0(&cur, 0))
    {
        *iter.FUN_0064dbd0() *= scale;
    }
    return this;
}
