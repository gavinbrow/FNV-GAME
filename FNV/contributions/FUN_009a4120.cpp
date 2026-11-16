struct GameList
{
    unsigned int __thiscall FUN_0044ddc0();
    int* __thiscall FUN_006a7ad0(unsigned int index);
    void __thiscall FUN_009a4320(unsigned int index, int removeFlag);
    ~GameList();
};
struct GroupRegistry
{
    bool __thiscall FUN_00853130(void* key, GameList** result);
    void __thiscall FUN_00405430(void* key);
    void __thiscall FUN_009a4120(void* key, int value);
};
void __thiscall GroupRegistry::FUN_009a4120(void* key, int value)
{
    GameList* entries = 0;
    if (FUN_00853130(key, &entries))
    {
        for (unsigned int index = 0; index < entries->FUN_0044ddc0(); ++index)
        {
            if (*entries->FUN_006a7ad0(index) == value)
            {
                if (entries->FUN_0044ddc0() == 1)
                {
                    delete entries;
                    FUN_00405430(key);
                }
                else
                {
                    entries->FUN_009a4320(index, 1);
                }
                break;
            }
        }
    }
}