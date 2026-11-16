struct Payload { const char* name; float value; int id; };
extern float DAT_0104da48;
extern const char DAT_010ce7fc[];
void FUN_00d37280(int, int, int, Payload*);
void FUN_00d378a0(int a, int b, int c, int d)
{
    Payload p;
    p.name = DAT_010ce7fc;
    p.value = DAT_0104da48;
    p.id = d;
    FUN_00d37280(b, a, c, &p);
}
