class NiPoint3 {
public:
    int FUN_0043c470();
};

NiNode* __fastcall FUN_0059bb30(NiAVObject* object);

struct FUN_0043c430_shell : NiAVObject {
    int FUN_0043c430();
};

int FUN_0043c430_shell::FUN_0043c430()
{
    return FUN_0059bb30(this) ? FUN_0059bb30(this)->FUN_0043c490().FUN_0043c470() : 0;
}
