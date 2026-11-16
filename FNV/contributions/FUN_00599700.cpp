struct TextValue {
    char* text;
    unsigned short length;
    unsigned short capacity;
    TextValue* FUN_00559450(int flag);
    ~TextValue();
};
struct StringRecord {
    TextValue name;
    float first;
    float second;
    void FUN_004037f0(TextValue*);
    void FUN_00599700(TextValue value, float firstValue, float secondValue);
};
void StringRecord::FUN_00599700(TextValue value, float firstValue, float secondValue) {
    FUN_004037f0(value.FUN_00559450(0));
    first = firstValue;
    second = secondValue;
}
