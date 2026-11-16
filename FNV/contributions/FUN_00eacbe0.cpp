
extern "C" unsigned int __cdecl strlen(const char*);
extern "C" void* __cdecl FUN_00aa1070(unsigned int);
extern "C" int __cdecl FUN_00a305b0(char*, unsigned int, const char*, ...);
extern const char str_010f18a4[];
extern const char str_010f1898[];
extern const char str_010f1884[];
extern const double DAT_01017a40;
struct Stream0 {
    int unk00;
    int unk04;
    unsigned short capacity08;
    unsigned short size0a;
    unsigned short unk0c;
    unsigned short grow0e;
    void FUN_0096ad30(unsigned int);
    void FUN_0096ae90(unsigned int, char**);
};
struct StringPart0 { char* FUN_00a59af0(const char*); };
struct Display0 {
    int unk00;
    StringPart0 child04;
    int unk08;
    int unk0c;
    float rate10;
    void FUN_00eacbe0(char* text, Stream0* out);
};
void Display0::FUN_00eacbe0(char* text, Stream0* out) {
    char* original;
    unsigned int bytes = strlen(text) + 13;
    original = text;
    text = (char*)FUN_00aa1070(bytes);
    FUN_00a305b0(text, bytes, str_010f18a4, original);
    unsigned int size = out->size0a;
    if (size >= out->capacity08) out->FUN_0096ad30(size + out->grow0e);
    out->FUN_0096ae90(size, &text);
    text = child04.FUN_00a59af0(str_010f1898);
    size = out->size0a;
    if (size >= out->capacity08) out->FUN_0096ad30(size + out->grow0e);
    out->FUN_0096ae90(size, &text);
    bytes = strlen(original) + 30;
    text = (char*)FUN_00aa1070(bytes);
    int scaled = (int)(rate10 * DAT_01017a40);
    FUN_00a305b0(text, bytes, str_010f1884, (float)scaled / DAT_01017a40);
    size = out->size0a;
    if (size >= out->capacity08) out->FUN_0096ad30(size + out->grow0e);
    out->FUN_0096ae90(size, &text);
}
