struct FormWithSaveCheck : TESForm { bool FUN_00565450(); };
struct ReconstructEntry { void FUN_00841250(FormWithSaveCheck*, int, int); void FUN_008418b0(int, int, int, FormWithSaveCheck*, int, int); };
struct ReconstructedCellStorage : FUN_008416c0 { unsigned int recordID; void* owner; unsigned int flags; unsigned int count; };
int __cdecl FUN_00544280(int, int);
struct SaveLoadDispatcher { int state00,state04,state08,state0c; ReconstructEntry* helper10; bool FUN_00853130(int,ReconstructEntry**); void FUN_00844700(int,ReconstructEntry*); void FUN_00841ca0(int,int,int,FormWithSaveCheck*,int,int); };
void SaveLoadDispatcher::FUN_00841ca0(int value,int formID,int context,FormWithSaveCheck* form,int flag,int offset) {
    int handle3;
    FormWithSaveCheck* referenceForm;
    ReconstructEntry* entry7;
    if (form != 0 && form->GetIsReference() && (referenceForm = form, referenceForm->FUN_00565450())) {
        if (helper10 == 0) helper10 = (ReconstructEntry*)new FUN_00841190;
        helper10->FUN_00841250(form,flag,offset);
    } else {
        handle3 = FUN_00544280(formID,context);
        entry7 = 0;
        if (!FUN_00853130(handle3,&entry7)) {
            entry7 = (ReconstructEntry*)new ReconstructedCellStorage;
            FUN_00844700(handle3,entry7);
        }
        entry7->FUN_008418b0(value,formID,context,form,flag,offset);
    }
}
