struct OwnedRecord {
    ~OwnedRecord();
};
struct ListElement {
    OwnedRecord** FUN_006815c0();
    ListElement* FUN_00726070();
    void FUN_00470470();
    ~ListElement();
};
struct RecordList {
    ListElement* head;
    unsigned int count;
    void FUN_00851540();
};
void RecordList::FUN_00851540() {
    ListElement* current = head;
    while (current != 0) {
        delete *current->FUN_006815c0();
        current = current->FUN_00726070();
    }
    if (head != 0) {
        head->FUN_00470470();
        delete head;
        head = 0;
    }
    count = 0;
}