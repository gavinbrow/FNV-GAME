struct SettingArray {
    unsigned int metadata;
    int* values;
    unsigned short capacity;
    unsigned short count;
    unsigned short activeCount;
    unsigned short growBy;
    void __thiscall FUN_0096ad30(unsigned int newSize);
    void __thiscall FUN_0096ae90(unsigned int index, int* value);
    void AddTextValue(int* value) {
        unsigned int index = count;
        if (index >= capacity)
            FUN_0096ad30(index + growBy);
        FUN_0096ae90(index, value);
    }
    __forceinline void AddNumericValue(int value) {
        unsigned int index = count;
        if (index >= capacity)
            FUN_0096ad30(index + growBy);
        if (index >= count) {
            count = (unsigned short)(index + 1);
            if (value != 0) ++activeCount;
        } else if (value != 0) {
            if (values[index] == 0) ++activeCount;
        } else if (values[index] != 0) {
            --activeCount;
        }
        values[index] = value;
    }
    __forceinline void AddFinal(int value) {
        unsigned int index = count;
        if (index >= capacity)
            FUN_0096ad30(index + growBy);
        if (index >= count) {
            count = (unsigned short)(index + 1);
            if (value != 0) ++activeCount;
        } else if (value != 0) {
            if (values[index] == 0) ++activeCount;
        } else if (values[index] != 0) {
            --activeCount;
        }
        values[index] = value;
    }
};
struct ShaderFlagEntry {
    unsigned int unknown00;
    unsigned short type;
    unsigned char unknown06;
    unsigned char secondary;
};
struct ShaderFlagList {
    unsigned int unknown00;
    ShaderFlagEntry** entries;
    unsigned int unknown08;
    unsigned int unknown0c;
    unsigned int count;
};
extern void __stdcall FUN_00a81600(SettingArray* target);
extern int __cdecl FUN_00a7d330(const char* text);
extern int __cdecl FUN_00a7d370(const char* text, int flag);
extern int __cdecl FUN_00a7d550(const char* text, float value);
extern int __cdecl FUN_00a7d4d0(const char* text, int value);
extern unsigned int __cdecl FUN_00a7d510(const char* text, unsigned int value);
extern int __cdecl FUN_00a7d5e0(const char* text, const char* value);
extern const char* __cdecl FUN_00b4f9d0(unsigned int value);
extern const char* DAT_01200464;
extern const char UNK_010b8950[];
extern const char UNK_010b8948[];
extern const char UNK_010b893c[];
extern const char UNK_010b892c[];
extern const char UNK_010b8920[];
extern const char UNK_010b8914[];
extern const char UNK_010b890c[];
extern const char UNK_010b88f8[];
extern const char UNK_010b88e8[];
extern const char UNK_010b88dc[];
extern const char UNK_010b88d4[];
extern const char UNK_010b88c8[];
extern const char UNK_010b88b4[];
extern const char UNK_010b889c[];
extern const char UNK_010b8890[];
extern const char UNK_010b8884[];
extern const char UNK_010b8874[];
extern const char UNK_010b885c[];
extern const char UNK_010b8854[];
extern const char UNK_010b8844[];
extern const char UNK_010b882c[];
extern const char UNK_010b8810[];
extern const char UNK_010b8800[];
extern const char UNK_010b87f0[];
extern const char UNK_010b87dc[];
extern const char UNK_010b87c8[];
extern const char UNK_010b87c0[];
extern const char UNK_010b87b0[];
extern const char UNK_010b879c[];
extern const char UNK_010b8788[];
extern const char UNK_010b877c[];
extern const char UNK_010b876c[];
extern const char UNK_010b875c[];
extern const char UNK_010b874c[];
extern const char UNK_010b873c[];
extern const char UNK_010b8734[];
extern const char UNK_010b8724[];
extern const char UNK_010b8714[];
extern const char UNK_010b8708[];
extern const char UNK_010b86ec[];
extern const char UNK_010b86e0[];
extern const char UNK_010b86d4[];
extern const char UNK_010b86c4[];
extern const char UNK_010b86b4[];
extern const char UNK_010b86a8[];
extern const char UNK_010b869c[];
extern const char UNK_010b8688[];
extern const char UNK_010b8674[];
extern const char UNK_010b8668[];
extern const char UNK_010b8658[];
extern const char UNK_010b8644[];
extern const char UNK_010b8634[];
extern const char UNK_010b8620[];
extern const char UNK_010b8614[];
extern const char UNK_010b85f4[];
extern const char UNK_010b85e4[];
extern const char UNK_010b85dc[];
extern const char UNK_010b85d0[];
extern const char UNK_010b85c4[];
extern const char UNK_010b85b4[];
extern const char UNK_010b85a4[];
extern const char UNK_010b858c[];
extern const char UNK_010b855c[];
extern const char UNK_010b8554[];
extern const char UNK_010b854c[];
extern const char UNK_010b8570[];
struct ShaderPropertyRecord {
    int unknown00, unknown04, unknown08, unknown0c;
    int unknown10, unknown14, unknown18, unknown1c;
    unsigned int flags[2];
    float alpha;
    float fade;
    float specular;
    int unknown34;
    int material;
    ShaderFlagList* flagsList;
    int unknown40, unknown44, unknown48, unknown4c;
    int unknown50, unknown54;
    int shaderType;
    float depth;
    void FUN_00ba9890(SettingArray* output);
};
void ShaderPropertyRecord::FUN_00ba9890(SettingArray* output) {
    FUN_00a81600(output);
    union { int token; volatile float scalar; } formatted;
    formatted.token = FUN_00a7d330(DAT_01200464);
    output->AddTextValue(&formatted.token);
    const char* flagNames[56] = {
        UNK_010b8950,
        UNK_010b8948,
        UNK_010b893c,
        UNK_010b892c,
        UNK_010b8920,
        UNK_010b8914,
        UNK_010b890c,
        UNK_010b88f8,
        UNK_010b88e8,
        UNK_010b88dc,
        UNK_010b88d4,
        UNK_010b88c8,
        UNK_010b88b4,
        UNK_010b889c,
        UNK_010b8890,
        UNK_010b8884,
        UNK_010b8874,
        UNK_010b885c,
        UNK_010b8854,
        UNK_010b8844,
        UNK_010b882c,
        UNK_010b8810,
        UNK_010b8800,
        UNK_010b87f0,
        UNK_010b87dc,
        UNK_010b87c8,
        UNK_010b87c0,
        UNK_010b87b0,
        UNK_010b879c,
        UNK_010b8788,
        UNK_010b877c,
        UNK_010b876c,
        UNK_010b875c,
        UNK_010b874c,
        UNK_010b873c,
        UNK_010b8734,
        UNK_010b8724,
        UNK_010b8714,
        UNK_010b8708,
        UNK_010b86ec,
        UNK_010b86e0,
        UNK_010b86d4,
        UNK_010b86c4,
        UNK_010b86b4,
        UNK_010b86a8,
        UNK_010b869c,
        UNK_010b8688,
        UNK_010b8674,
        UNK_010b8668,
        UNK_010b8658,
        UNK_010b8644,
        UNK_010b8634,
        UNK_010b8620,
        UNK_010b8614,
        UNK_010b85f4,
        UNK_010b85e4
    };
    unsigned int i = 0;
    unsigned int mask = 1;
    for (; i < 56; ++i) {
        if ((flags[i >> 5] & mask) > 0 && flagNames[i] != 0)
        { formatted.token = FUN_00a7d370(flagNames[i], 1);
          output->AddTextValue(&formatted.token); }
        mask = (mask << 1) | (mask >> 31);
    }
    if (alpha < 1.0f) {
        formatted.token = FUN_00a7d550(UNK_010b85dc, alpha);
        output->AddTextValue(&formatted.token);
    }
    if (fade < 1.0f) {
        formatted.token = FUN_00a7d550(UNK_010b85d0, fade);
        output->AddTextValue(&formatted.token);
    }
    if (depth > 0.0f) {
        formatted.token = FUN_00a7d550(UNK_010b85c4, depth);
        output->AddTextValue(&formatted.token);
    }
    if ((flags[0] & 0x80u) > 0) {
        formatted.scalar = specular;
        formatted.token = FUN_00a7d550(UNK_010b85b4, formatted.scalar);
        output->AddTextValue(&formatted.token);
    }
    int numericToken = FUN_00a7d4d0(UNK_010b85a4, shaderType);
    output->AddNumericValue(numericToken);
    numericToken = FUN_00a7d4d0(UNK_010b858c, material);
    output->AddNumericValue(numericToken);
    if (!flagsList) {
        formatted.token = FUN_00a7d330(UNK_010b8570);
        output->AddTextValue(&formatted.token);
        return;
    }
    unsigned int count = flagsList->count;
    formatted.token = FUN_00a7d510(UNK_010b855c, count);
    output->AddTextValue(&formatted.token);
    for (unsigned int index = 0; index < count; ++index) {
        ShaderFlagEntry* entry = flagsList->entries[index];
        unsigned short type = entry->type;
        if (type < 0x2f7) {
            const unsigned int code = type;
if(entry->secondary) { output->AddFinal(FUN_00a7d5e0(UNK_010b8554,FUN_00b4f9d0((unsigned int)entry->type))); } else {output->AddFinal(FUN_00a7d5e0(UNK_010b854c,FUN_00b4f9d0((unsigned int)entry->type))); }
        }
    }
}
