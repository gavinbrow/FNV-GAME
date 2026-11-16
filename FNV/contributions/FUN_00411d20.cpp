extern int DAT_0101444c;

struct ExtraBaseConstructor {
    ExtraBaseConstructor(unsigned char type);
    ~ExtraBaseConstructor();
};

struct ExtraPayloadConstructor {
    ExtraPayloadConstructor();
};

struct FUN_00411d20 : ExtraBaseConstructor {
    void* vtable;
    unsigned char extraType;
    unsigned char reserved05;
    unsigned short reserved06;
    void* next;
    ExtraPayloadConstructor payload;

    FUN_00411d20();
};

FUN_00411d20::FUN_00411d20()
    : ExtraBaseConstructor(0x85),
      vtable(&DAT_0101444c)
{
}