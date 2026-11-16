struct FUN_006815c0 {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    FUN_006815c0();
};

struct FUN_004b4910_Source {
    unsigned short FUN_00456650();
    int FUN_00461130();
    int FUN_0049ec60();
};

int __cdecl FUN_004b4a10(unsigned short a1, int a2, int a3, int a4);

FUN_006815c0* __cdecl FUN_004b4910(FUN_004b4910_Source* source)
{
    FUN_006815c0* elements = 0;
    if (!source || !source->FUN_00456650()) {
        return 0;
    }
    elements = new FUN_006815c0[source->FUN_00456650()];
    FUN_004b4a10(source->FUN_00456650(), source->FUN_0049ec60(), (int)elements, source->FUN_00461130());
    return elements;
}