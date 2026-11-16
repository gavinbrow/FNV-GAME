struct FUN_00e611d0_Object
{
    unsigned char unk00;
    unsigned char unk01;
    unsigned char unk02;
    unsigned char unk03;
    unsigned char unk04;
    unsigned char unk05;
    unsigned char unk06;
    unsigned char unk07;
    int unk08;
    int unk0C;
    unsigned char unk10;
    unsigned char unk11;
    unsigned char unk12;
    unsigned char unk13;
    unsigned char unk14;
    unsigned char unk15;
    unsigned char unk16;
    unsigned char unk17;
    int unk18;
};

struct FUN_00c85750_Result
{
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
};

FUN_00c85750_Result* __cdecl FUN_00c85750();
void __cdecl FUN_00e60d40(int, int, int, int, int);
void __cdecl FUN_00e61090(int, int, int, int, int);

void __cdecl FUN_00e611d0(FUN_00e611d0_Object* object, int value)
{
    switch (object->unk14)
    {
        case 0:
        {
            FUN_00c85750_Result* result = FUN_00c85750();
            FUN_00e60d40(
                object->unk00,
                object->unk08,
                object->unk0C,
                value,
                result->unk10);
            break;
        }

        case 1:
        {
            if ((static_cast<unsigned int>(object->unk00) - 3U) <= 1U)
            {
                FUN_00e61090(
                    object->unk00,
                    object->unk18,
                    object->unk08,
                    0,
                    value);
            }
            break;
        }
    }
}