extern int __cdecl FUN_00cb10d0(int value);
struct Router_d62100 {
    int unk00;
    int unk04;
    int unk08;
    int m_context;
};
struct FUN_00d62100_Class {
    int __thiscall FUN_00d62630(int context, int first, int second, int third);
    int __thiscall FUN_00d62100(int first, int second, int third);
};
int FUN_00d62100_Class::FUN_00d62100(int first, int second, int third)
{
    if (third < 0)
        third = FUN_00cb10d0(second);
    Router_d62100* router = static_cast<Router_d62100*>(FUN_00c85750());
    return FUN_00d62630(router->m_context, first, second, third);
}