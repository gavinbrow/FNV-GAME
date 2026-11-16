struct InputObject { void* vtable; };
struct InputRecord { int unk00; int unk04; int unk08; int type; };
struct InputData { InputObject* unk00; InputRecord** unk04; int unk08; int unk0C; int unk10; int unk14; int unk18; int unk1C; int unk20; };
struct ResultData {
    char unk00; char unk01; char unk02; char unk03; char unk04; char unk05; char unk06; char unk07;
    char unk08; char unk09; char unk0A; unsigned char unk0B; int unk0C;
    void __thiscall FUN_00dafe70(void* a, void* b, void* c);
    void __thiscall FUN_00dafcd0(void* a, void* b, void* c);
};
void* __cdecl FUN_00d418d0(InputData* input, unsigned char* status, ResultData* result)
{
    InputObject* first = input->unk00;
    void* table = first->vtable;
    InputRecord* record = *input->unk04;
    if (record->type == 3) result->FUN_00dafe70(table, record, &input->unk20);
    else result->FUN_00dafcd0(table, record, &input->unk20);
    status[2] = 0;
    result->unk0B &= 0xEF;
    result->unk0C = 0;
    unsigned int size = (unsigned char)*((char*)result + 0x0D) + 4 * (unsigned char)*((char*)result + 0x0E);
    size += (unsigned char)result->unk0C;
    return (char*)result + ((size * 2 + 0x1F) & 0xFFFFFFF0);
}
