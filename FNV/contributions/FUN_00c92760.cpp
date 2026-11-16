struct Shape64 {};
struct Container64 {
    void __thiscall FUN_00d064a0(Shape64* shape);
};
struct Shape64List {
    Shape64** data;
    int count;
};
struct Element64 {
    int unk00; int unk04; int unk08; int unk0C; int unk10; int unk14;
    int unk18; int unk1C; int unk20; int unk24; int unk28; int unk2C;
    int unk30; int unk34; int unk38; int unk3C; int unk40; int unk44;
    Shape64List shapes;
};
struct Context64 {
    int unk00; int unk04; int unk08; int unk0C; int unk10;
    int unk14; int unk18; int unk1C; int unk20; int unk24;
    Element64** elements;
    int elementCount;
};
unsigned char* __cdecl FUN_00c92760(unsigned char* result, Context64* context, Container64* volatile container)
{
    Element64** element = context->elements;
    if (element != context->elements + context->elementCount)
    {
        do
        {
            Shape64List* shapes = &(*element)->shapes;
            int index = 0;
            if (shapes->count > 0)
            {
                do
                {
                    container->FUN_00d064a0(shapes->data[index]);
                    ++index;
                } while (index < shapes->count);
            }
            ++element;
        } while (element != context->elements + context->elementCount);
    }
    *result = context->elementCount > 0;
    return result;
}