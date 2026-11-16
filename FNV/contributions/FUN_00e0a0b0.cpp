struct QuadExtent
{
    float min;
    float max;
};

struct QuadElement
{
    unsigned primitiveID;
    unsigned secondaryID;
    QuadExtent extent;
    unsigned originalID;
};

struct QuadRange
{
    QuadElement* m_elements;
    int m_numElements;
    int m_numTotal;
};

struct QuadCenter
{
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    int unk20;
    int unk24;
    int unk28;
    int unk2C;
    int unk30;
    int unk34;
    int unk38;
    int unk3C;
    int unk40;
    int unk44;
    int unk48;
    int unk4C;
    int unk50;
    int unk54;
    int unk58;
    int unk5C;
    int unk60;
    float m_x;
    float m_y;
};

int __cdecl FUN_00cbfef0(float f);

class QuadSplitter
{
public:
    __declspec(noalias) void FUN_00e0a950(int quadrant, QuadCenter* center, int context, int* total, int* counter, QuadElement** cur, QuadElement** mid, QuadElement** p2, QuadElement** p3);
    __declspec(noalias) void FUN_00e0acb0(QuadElement** p0, QuadElement** mid, QuadElement** p2, QuadElement** p3, QuadElement** p4, QuadElement** p5, QuadCenter* center);
    void FUN_00e0a0b0(QuadRange* in, QuadCenter* center, int context, QuadRange* outA, QuadRange* outB);
};

void QuadSplitter::FUN_00e0a0b0(QuadRange* in, QuadCenter* center, int context, QuadRange* outA, QuadRange* outB)
{
    int total = in->m_numTotal;
    int counter = 0;
    QuadElement* cur;
    QuadElement* p0;
    QuadElement* m;
    QuadElement* p2;
    QuadElement* p3;
    QuadElement* p4;
    QuadElement* mid;
    QuadElement* end;
    QuadElement* p5;

    p0 = in->m_elements;
    mid = p0 + in->m_numElements;
    end = p0 + (in->m_numElements + in->m_numTotal);
    p2 = end;
    p3 = end;
    p5 = end;
    cur = (p0 != 0) ? p0 : p0;

    while (cur < mid)
    {
        int quadrant = 0;
        if (cur->extent.min < center->m_x)
        {
            if (cur->extent.max <= center->m_y)
                quadrant = 1;
            else
                quadrant = 3;
        }
        else if (cur->extent.max > center->m_y)
            quadrant = 2;

        FUN_00e0a950(quadrant, center, context, &total, &counter, &cur, &mid, &p2, &p3);
    }

    p4 = p3;
    FUN_00e0acb0(&p0, &mid, &p2, &p4, &p3, &p5, center);

    m = mid;
    outA->m_numElements = m - p0;
    outA->m_numTotal = FUN_00cbfef0((float)outA->m_numElements * total / in->m_numElements);
    outB->m_numElements = p4 - p2;
    outB->m_numTotal = total - outA->m_numTotal;
    outA->m_elements = p0;
    outB->m_elements = m + outA->m_numTotal;

    if (outB->m_numTotal != 0)
    {
        QuadElement* dst = outB->m_elements;
        QuadElement* last = p4;
        for (; p2 < last; ++p2)
            *dst++ = *p2;
    }
}