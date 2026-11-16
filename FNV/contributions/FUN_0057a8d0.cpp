struct ExtraDataHeader
{
    virtual ~ExtraDataHeader();
    ExtraDataHeader* next;
    unsigned int type;
};

struct ExtraDataPayload
{
    virtual ~ExtraDataPayload();
};

struct FUN_0057a8d0 : ExtraDataHeader
{
    ExtraDataPayload* payload;
    virtual ~FUN_0057a8d0();
};

FUN_0057a8d0::~FUN_0057a8d0()
{
    if (payload)
        delete payload;
}
