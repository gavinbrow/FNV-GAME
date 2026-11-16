void* __cdecl FUN_004336f0(int wantedFormId, ContNode* first)
{
    void* result = 0;
    ContNode* node = first;
    while (node != 0 && !node->FUN_008256d0()) {
        void* record = *(void**)node->FUN_006815c0();
        if (*(int*)record == wantedFormId) {
            result = record;
            break;
        }
        node = node->GetNext();
    }
    return result;
}
