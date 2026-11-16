struct S00b37660_Cache; extern S00b37660_Cache DAT_011f8e2c;
struct GlobalFree { ~GlobalFree(); };
struct TreeCleanup { char* allocation; void FUN_00b3ba90(); ~TreeCleanup(){FUN_00b3ba90();} };
struct S00b37660_Cache:GlobalFree {TreeCleanup tree;};
inline GlobalFree::~GlobalFree(){ int spare[34]; delete DAT_011f8e2c.tree.allocation; }
S00b37660_Cache DAT_011f8e2c;
