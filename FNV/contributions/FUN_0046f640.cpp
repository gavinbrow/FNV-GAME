
struct FNVObject {
    virtual ~FNVObject();
    short FUN_00418770();
    void* FUN_00418630();
    void FUN_00418600();
    int FUN_0055d310();
    unsigned int FUN_0040fe20();
    int FUN_00410220(int mode);
    int FUN_00418800();
    struct FNVCursor* FUN_005d43c0();
};

struct FNVRecordManager;
struct FNVCursor {
    FNVRecordManager* FUN_00418520();
    void FUN_0041aed0();
    void FUN_00418600();
};

struct FNVListNode {
    FNVObject** FUN_006815c0();
    FNVListNode* FUN_00726070();
};

struct FNVRecordGroup {
    FNVRecordManager* owner;
    FNVListNode* FUN_00559450();
    FNVRecordGroup* FUN_0044ddc0(int,int);
    FNVRecordGroup* FUN_0044ddc0(FNVObject*,int,int,int,void*,int,int,int,int);
};

struct FNVFile {
    FNVRecordGroup* FUN_0044ddc0(int selected, int all);
    FNVRecordGroup* FUN_0044ddc0(FNVObject*,int,int,int,void*,int,int,int,int);
};

struct FNVRecordManager {
    void FUN_00905330(FNVObject**);
    FNVRecordGroup* FUN_004bfba0(FNVRecordGroup*);
};

extern void* _DAT_011dea3c;

struct FUN_0046f640_shell { void FUN_0046f310(int source); void FUN_0046f640(FNVFile*,int,int); };

void FUN_0046f640_shell::FUN_0046f640(FNVFile* file, int remaining, int source) {
    FNVObject* current = 0;
    bool retrying;
    FNVRecordGroup* group = (*reinterpret_cast<FNVRecordManager**>(reinterpret_cast<unsigned char*>(this)+0x628))->FUN_004bfba0(file->FUN_0044ddc0(1,0));
    if (!group)
        return;

    FNVListNode* node = group->FUN_00559450();
    if (node)
        current = *node->FUN_006815c0();

    retrying = false;
    while (remaining) {
        bool unique;
        void* processed = 0;
        int count = 1;
        if (!node && retrying)
            return;

        if (node) {
            current = *node->FUN_006815c0();
            node = node->FUN_00726070();
            if (current) {
                count = current->FUN_00418770();
                if (count > 0) {
                    processed = current->FUN_00418630();
                    if (remaining >= count)
                        current->FUN_00418600();
                    if (remaining < count)
                        count = remaining;
                } else {
                    processed = 0;
                }
            }
            if (processed) {
                if (reinterpret_cast<FNVObject*>(processed)->FUN_0055d310()) {
                    FNVObject* input = 0;
                    if (current->FUN_0040fe20()) {
                        if (current->FUN_0040fe20() != 1 ||
                            !current->FUN_00410220(0x24))
                            input = current;
                    }
                    typedef void (__thiscall *SendFunc)(void*,FNVRecordGroup*);
                    reinterpret_cast<SendFunc>((*reinterpret_cast<void***>(processed))[0x17c/4])(
                        processed,group->FUN_0044ddc0(input,count,0,0,_DAT_011dea3c,0,0,1,0));
                    FNVRecordManager* firstRef = reinterpret_cast<FNVObject*>(processed)->FUN_005d43c0()->FUN_00418520();
                    unique = true;
                    if (firstRef) {
                        FNVRecordGroup* matching = firstRef->FUN_004bfba0(group->FUN_0044ddc0(1,0));
                        if (matching && matching->FUN_00559450()) {
                            FNVListNode* scan = matching->FUN_00559450();
                            while (scan && *scan->FUN_006815c0() && unique) {
                                if (*scan->FUN_006815c0() == current)
                                    unique = false;
                                else
                                    scan = scan->FUN_00726070();
                            }
                        }
                    }
                    firstRef = reinterpret_cast<FNVObject*>(_DAT_011dea3c)->FUN_005d43c0()->FUN_00418520();
                    if (firstRef) {
                        FNVRecordGroup* matching = firstRef->FUN_004bfba0(group->FUN_0044ddc0(1,0));
                        if (matching && matching->FUN_00559450()) {
                            FNVListNode* scan = matching->FUN_00559450();
                            while (scan && *scan->FUN_006815c0() && unique) {
                                if (*scan->FUN_006815c0() == current)
                                    unique = false;
                                else
                                    scan = scan->FUN_00726070();
                            }
                        }
                    }
                    if (unique && current && current->FUN_0040fe20() < 2 &&
                        current->FUN_00418770() <= 1 && !current->FUN_00418800()) {
                        group->owner->FUN_00905330(&current);
                        node = group->FUN_00559450();
                        delete current;
                        current = 0;
                    }
                    if (current &&
                         ((current->FUN_00418770() > 1 && current->FUN_0040fe20() < 2)
                           || current->FUN_0040fe20() < 1))
                        current = 0;
                } else {
                    reinterpret_cast<FNVObject*>(processed)->FUN_005d43c0()->FUN_0041aed0();
                    reinterpret_cast<FNVObject*>(processed)->FUN_005d43c0()->FUN_00418600();
                    typedef void (__thiscall* ProcessFunc)(void*,void*,int,int);
                    reinterpret_cast<ProcessFunc>((*reinterpret_cast<void***>(_DAT_011dea3c))[0x3d0/4])(
                         _DAT_011dea3c,processed,count,0);
                    group->owner->FUN_00905330(&current);
                    node = group->FUN_00559450();
                    if (current->FUN_0040fe20() < 2 &&
                        current->FUN_00418770() <= 1 &&
                        !current->FUN_00418800()) {
                        delete current;
                    }
                    current = 0;
                }
                remaining-=count;
                if (node) current = *node->FUN_006815c0(); else current=0;
            } else {
                if (!node)
                    remaining = 0;
                else
                    current = *node->FUN_006815c0();
            }
        } else {
            FUN_0046f310(source);
            current=0;
            processed=0;
            retrying=true;
            group=(*reinterpret_cast<FNVRecordManager**>(reinterpret_cast<unsigned char*>(this)+0x628))->FUN_004bfba0(file->FUN_0044ddc0(1,0));
            if (!group)
                return;
            node=group->FUN_00559450();
            if (node) current=*node->FUN_006815c0();
        }
    }
}
