extern unsigned int g_01268188;
extern unsigned int g_012685f4;
extern const char DAT_0108febc[];
extern const char DAT_010c52bc[];

struct BaseObject {
    const char* classTable;
    unsigned int unknown04;
    unsigned int unknown08;
    BaseObject();
};

struct MiddleObject : BaseObject {
    unsigned int initialized0c;
    MiddleObject() : initialized0c(0) {
        classTable = DAT_0108febc;
        ++g_01268188;
    }
    ~MiddleObject();
};

struct FUN_00c7f9e0 : MiddleObject {
    FUN_00c7f9e0(void* context);
    void FUN_00c89dd0(void* context);
};

FUN_00c7f9e0::FUN_00c7f9e0(void* context) : MiddleObject()
{
    classTable = DAT_010c52bc;
    FUN_00c89dd0(context ? (char*)context + 4 : 0);
    ++g_012685f4;
}
