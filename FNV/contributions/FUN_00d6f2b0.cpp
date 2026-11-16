
extern "C" double DAT_010c9300;
struct EventRecord {
    union { float accumulator; struct { unsigned char opcode; unsigned char option; unsigned short other; }; };
    unsigned short context6c;
    unsigned short context70;
    unsigned int inputBits;
    unsigned int valueBits;
};
struct RecordSource {
    volatile int& f60() const { return *reinterpret_cast<volatile int*>(reinterpret_cast<char*>(const_cast<RecordSource*>(this))+0x60); }
    volatile int& f6c() const { return *reinterpret_cast<volatile int*>(reinterpret_cast<char*>(const_cast<RecordSource*>(this))+0x6c); }
    volatile int& f70() const { return *reinterpret_cast<volatile int*>(reinterpret_cast<char*>(const_cast<RecordSource*>(this))+0x70); }
};
void __cdecl FUN_00d6f2b0(const RecordSource* source, EventRecord** dest, volatile unsigned int inputBits, volatile unsigned char option) {
    volatile EventRecord* record = *dest;
    double next = record->accumulator + DAT_010c9300;
    int n70 = source->f70();
    int n6c = source->f6c();
    int n60 = source->f60();
    record->accumulator = (float)next;
    record->context70 = (unsigned short)n70;
    unsigned int incoming = inputBits;
    record->valueBits = (unsigned int)n60;
    unsigned char flags = option;
    record->context6c = (unsigned short)n6c;
    record->inputBits = incoming;
    record->opcode = 1;
    record->option = flags;
    *dest = const_cast<EventRecord*>(record + 1);
}