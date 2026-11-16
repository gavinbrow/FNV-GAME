struct LookupEntry {
    unsigned int FUN_00726070();
};
struct LookupResult {
    LookupEntry* entry;
    LookupResult(int initialState);
    ~LookupResult();
    LookupEntry* FUN_00559450();
};
void __cdecl FUN_00a61b90(void* object, LookupResult* result);
void __cdecl FUN_00a61f30(LookupEntry* entry);
struct LookupHandler {
    bool FUN_00456800(void* object, unsigned int limit);
};
bool LookupHandler::FUN_00456800(void* object, unsigned int limit)
{
    LookupResult result(0);
    FUN_00a61b90(object, &result);
    if (result.FUN_00559450() != 0)
    {
        if (result.FUN_00559450()->FUN_00726070() <= limit + 2)
        {
            FUN_00a61f30(result.FUN_00559450());
            return true;
        }
    }
    return false;
}
