struct Pt3c64640
{
    float x;
    float y;
    float z;
    Pt3c64640() {}
};

extern Pt3c64640 DAT_011f426c;

struct Box0c64640
{
    unsigned short unk00;
    Pt3c64640 unk04[8];
    Pt3c64640 unk64[8];
    Box0c64640* FUN_00c64640();
};

Box0c64640* Box0c64640::FUN_00c64640()
{
    int i;
    {
    int n = 8; Pt3c64640* p = unk04;
    while (--n >= 0) p++;
    }
    {
    int m = 8;
    Pt3c64640* q = unk64;
    while (--m >= 0) q++;
    }
    unk00 = 0;
    for (i = 0; i < 8; i++)
    {
        unk04[i] = DAT_011f426c;
        unk64[i] = DAT_011f426c;
    }
    return this;}
