
struct ConfigValue { unsigned type, identifier; const void* data; };
struct MessageBuffer {
    char* destination;
    unsigned capacity, length;
    void FUN_00cb1600(char*, unsigned);
    MessageBuffer* FUN_00cc01c0(const char*);
    MessageBuffer* FUN_00cc05a0(const void*);
    void FUN_00cc00e0();
};
struct DiagnosticLogger {
    virtual void open(); virtual void close(); virtual void flush();
    virtual void report(int, unsigned, const char*, const char*, int);
};
extern DiagnosticLogger* DAT_01268360;
extern const char str_010ecd20[],str_010eccfc[],str_010ecd0c[],str_010eccc8[];
struct ConfigTable {
    ConfigValue* FUN_00e5c5d0(const char*);
    ConfigValue* FUN_00e5c5b0(const char*);
    ConfigValue* FUN_00e5c5f0(const char*);
    int FUN_00e5c7a0(const char*, bool, unsigned*);
};
int ConfigTable::FUN_00e5c7a0(const char* name, bool reportMissing, unsigned* value) {
    ConfigValue* entry = FUN_00e5c5d0(name);
    if (entry) {
        *value = *static_cast<const unsigned*>(entry->data);
        return 0;
    }
    entry = FUN_00e5c5b0(name);
    if (entry) {
        *value = *static_cast<const unsigned char*>(entry->data) != 0;
        return 0;
    }
    entry = FUN_00e5c5f0(name);
    if (entry) {
        *value = *static_cast<const unsigned*>(entry->data);
        return 0;
    }
    if (reportMissing) {
        MessageBuffer buffer;
        unsigned text[128];
        buffer.FUN_00cb1600(reinterpret_cast<char*>(text), 512);
        buffer.FUN_00cc01c0(str_010ecd20)->FUN_00cc01c0(name)->FUN_00cc01c0(str_010eccfc)->FUN_00cc05a0(this)->FUN_00cc01c0(str_010ecd0c);
        DAT_01268360->report(1, 0xabbaab81u, reinterpret_cast<char*>(text), str_010eccc8, 90);
        buffer.FUN_00cc00e0();
    }
    return 1;
}
