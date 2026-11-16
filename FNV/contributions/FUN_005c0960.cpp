bool __cdecl FUN_005accb0(int first, int second, int last, int third, int fourth, int fifth, int sixth, signed char* extracted);
bool __cdecl FUN_0059c2d0(int third, int component, int zero, int seventh);

bool __cdecl FUN_005c0960(int first, int second, int third, int fourth, int fifth, int sixth, int seventh, int last)
{
    signed char component;
    if (!FUN_005accb0(first, second, last, third, fourth, fifth, sixth, &component))
        return false;
    return FUN_0059c2d0(third, component, 0, seventh);
}