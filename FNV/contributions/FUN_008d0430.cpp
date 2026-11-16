struct FUN_006fd980_shell;

class Mgr
{
public:
    FUN_006fd980_shell* _ref_00726070();
};

class BaseProcess
{
public:
    virtual ~BaseProcess();
    Mgr packageInfo;
    FUN_006fd980_shell* FUN_008d0430();
};

// @fnv 0x008d0430
FUN_006fd980_shell* BaseProcess::FUN_008d0430()
{
    return packageInfo._ref_00726070();
}
