struct CrimeCleanup {
    ~CrimeCleanup();
};

struct FUN_00975b60_shell : ProcessLists {
    void FUN_00975b60(BGSLoadGameBuffer* buffer);
};

void FUN_00975b60_shell::FUN_00975b60(BGSLoadGameBuffer* buffer)
{
    fPlayerActionCommentTimer = 0.0f;
    fPlayerKnockObjectCommentTimer = 0.0f;
    iCrimeNumber = 0;

    for (unsigned int index = 0; index < 5; ++index) {
        BSSimpleList<Crime*>* list = GlobalCrimeListArray[index];
        while (list && list->GetItem()) {
            Crime* entry = list->GetItem();
            delete (CrimeCleanup*)entry;
            list->RemoveHead();
        }
        delete list;
        GlobalCrimeListArray[index] = 0;
    }
}