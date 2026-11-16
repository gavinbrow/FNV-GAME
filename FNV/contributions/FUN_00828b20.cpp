extern int g_011dcc58;
float __cdecl FUN_00828dc0(int owner, int key);

int __cdecl FUN_00828b20(int a, int b)
{
    int idA = a;
    int idB = b;
    float valueA = FUN_00828dc0(g_011dcc58, idA);
    float valueB = FUN_00828dc0(g_011dcc58, idB);
    if (valueA == valueB) {
        return 0;
    } else if (valueA < valueB) {
        return 1;
    } else {
        return -1;
    }
}
