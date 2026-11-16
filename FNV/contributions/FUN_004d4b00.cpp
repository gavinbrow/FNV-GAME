struct Entry_004d4b00 {
    ~Entry_004d4b00();
    int FUN_0044ddc0();
};
struct Iterator_004d4b00 {
    ~Iterator_004d4b00();
};
struct Output_004d4b00 {
    void FUN_005ae3d0(Entry_004d4b00**);
};
struct Host_004d4b00 {
    Iterator_004d4b00* FUN_004ca200();
    Entry_004d4b00* FUN_004ca330(Iterator_004d4b00*);
    void FUN_004d4b00(int type, Output_004d4b00* output);
};
void Host_004d4b00::FUN_004d4b00(int type, Output_004d4b00* output)
{
    if (type == 0 || output == 0) return;
    Iterator_004d4b00* iterator = FUN_004ca200();
    Entry_004d4b00* entry = 0;
    bool found5 = false;
    do {
        entry = FUN_004ca330(iterator);
        if (entry != 0) {
            if (entry->FUN_0044ddc0() == type) {
                found5 = true;
                output->FUN_005ae3d0(&entry);
            } else {
                delete entry;
                if (found5)
                    break;
            }
        }
    } while (entry != 0);
    delete iterator;
}
