
extern "C" void* DAT_011de45c;
extern "C" char UNK_0104ad80[];
extern "C" char UNK_0104adc0[];
extern "C" char UNK_010156a8[];
extern "C" char UNK_01015718[];
extern "C" char UNK_01015588[];
extern "C" char UNK_01015500[];
extern "C" char UNK_010154a0[];
extern "C" char UNK_01015440[];
void __cdecl FUN_005b5e40(const char*, ...);
void* __cdecl FUN_004839c0(void*);
struct StreamReader {
    bool FUN_00862110();
    void FUN_008579e0(void*, unsigned int);
    unsigned int FUN_00825c00();
    void* FUN_004fd3c0();
    unsigned char FUN_008df040();
    void FUN_0060e680(unsigned int);
};
struct QuestInput {
    void FUN_00484c50(unsigned int, unsigned int);
    void FUN_00484d00(void*, unsigned int);
    unsigned char* FUN_005a8080();
    void* FUN_0060db40(unsigned char);
    void FUN_0060d670();
};
struct StageSave {
    void FUN_0067fdb0(unsigned char);
    void* FUN_0060f2c0(unsigned char);
};
struct StageEntry {
    void* FUN_008d8520();
    void FUN_00407800(void*);
};
struct SavedDate {
    unsigned int value;
    void FUN_004b1000(const Date*);
    void FUN_007b3fa0(unsigned int);
};
struct LogValue {
    short low, high;
    LogValue();
    ~LogValue();
    unsigned short FUN_004b1030();
    unsigned short FUN_004b1050();
};
void FUN_00483710(LogValue*);
struct LocalsState {
    void FUN_005a9950();
    void* FUN_0041af70(unsigned int);
};
typedef unsigned int (__thiscall *TagMethod)(void*);
struct QuestLoader : TESQuest {
    void FUN_0060e0d0(unsigned int flags, unsigned int extra);
};
void QuestLoader::FUN_0060e0d0(unsigned int flags, unsigned int extra)
{
    ((QuestInput*)this)->FUN_00484c50(flags, extra);
    unsigned short sizeRead = 0;
    unsigned int start = 0;
    if (((StreamReader*)DAT_011de45c)->FUN_00862110()) {
        unsigned int tag;
        ((StreamReader*)DAT_011de45c)->FUN_008579e0(&tag, 4);
        if (tag != 0x424c4f4b) {
            void* entry = ((StreamReader*)DAT_011de45c)->FUN_004fd3c0();
            if (entry) {
                void* view = FUN_004839c0(*(void**)entry);
                FUN_005b5e40(UNK_01015718, UNK_0104ad80, 0xfaf,
                    *(void**)entry, ((TagMethod*)*(void**)view)[76](view), *(unsigned char*)((char*)entry+9), *(unsigned int*)((char*)entry+5));
            } else {
                FUN_005b5e40(UNK_010156a8, UNK_0104ad80, 0xfaf,
                             ((StreamReader*)DAT_011de45c)->FUN_008df040());
            }
        }
        start = ((StreamReader*)DAT_011de45c)->FUN_00825c00();
        ((StreamReader*)DAT_011de45c)->FUN_008579e0(&sizeRead, 2);
    }
    if (flags & 2) {
        unsigned char enabled;
        ((QuestInput*)this)->FUN_00484d00(&enabled, 1);
        *((QuestInput*)this)->FUN_005a8080() = enabled;
    }
    if (flags & 0x80000000) {
        unsigned char stageCount;
        ((QuestInput*)this)->FUN_00484d00(&stageCount, 1);
        for (int i = 0; i < stageCount; ++i) {
            unsigned char stageId;
            unsigned char isComplete;
            ((QuestInput*)this)->FUN_00484d00(&stageId, 1);
            ((QuestInput*)this)->FUN_00484d00(&isComplete, 1);
            StageSave* questStage = (StageSave*)((QuestInput*)this)->FUN_0060db40(stageId);
            if (questStage) {
                questStage->FUN_0067fdb0(isComplete);
            } else {
                FUN_005b5e40(UNK_0104adc0, stageId, this->GetEditorName());
            }
            {
            unsigned char itemCount;
            ((QuestInput*)this)->FUN_00484d00(&itemCount, 1);
            for (int j = 0; j < itemCount; ++j) {
                Date date;
                {
                unsigned char itemId;
                ((QuestInput*)this)->FUN_00484d00(&itemId, 1);
                ((StreamReader*)DAT_011de45c)->FUN_008579e0(&date, 4);
                if (questStage) {
                    StageEntry* item = (StageEntry*)questStage->FUN_0060f2c0(itemId);
                    if (item) {
                        
                        if (((LogValue*)&date)->FUN_004b1030() == 0 && ((LogValue*)&date)->FUN_004b1050() == 0) {
                            SavedDate* old = (SavedDate*)item->FUN_008d8520();
                            if (old) {
                                delete (Date*)old;
                                item->FUN_00407800(0);
                            }
                        } else {
                            SavedDate* old = (SavedDate*)item->FUN_008d8520();
                            if (old) {
                                old->FUN_004b1000(&date);
                            } else {
                                old = (SavedDate*)new Date(date);
                                item->FUN_00407800(old);
                            }
                        }
                    }
                }
                }
            }
            }
        }
        this->cCurrentStage = 0;
        ((QuestInput*)this)->FUN_0060d670();
    }
    if (flags & 0x40000000) {
        if (!this->pScriptLocals) {
            ScriptLocals* replacement = new ScriptLocals;
{
            ((LocalsState*)replacement)->FUN_005a9950();
            delete replacement;
            ((StreamReader*)DAT_011de45c)->FUN_0060e680(0x40000000);
}
        } else {
            ((LocalsState*)this->pScriptLocals)->FUN_005a9950();
        }
    }
    if (((StreamReader*)DAT_011de45c)->FUN_00862110()) {
        void* entry;
        {
        unsigned int actual = ((StreamReader*)DAT_011de45c)->FUN_00825c00();
        entry = ((StreamReader*)DAT_011de45c)->FUN_004fd3c0();
    if (entry) {
            void* view = FUN_004839c0(*(void**)entry);
            if (actual > start + sizeRead)
                FUN_005b5e40(UNK_01015588, actual - (start + sizeRead), UNK_0104ad80,
                    0x1010, *(void**)entry, ((TagMethod*)*(void**)view)[76](view), *(unsigned char*)((char*)entry+9), *(unsigned int*)((char*)entry+5));
            else if (actual < start + sizeRead)
                FUN_005b5e40(UNK_01015500, (start + sizeRead) - actual, UNK_0104ad80,
                    0x1010, *(void**)entry, ((TagMethod*)*(void**)view)[76](view), *(unsigned char*)((char*)entry+9), *(unsigned int*)((char*)entry+5));
        } else {
            if (actual > start + sizeRead)
                FUN_005b5e40(UNK_010154a0, actual - (start + sizeRead), UNK_0104ad80,
                    0x1010, ((StreamReader*)DAT_011de45c)->FUN_008df040());
            else if (actual < start + sizeRead)
                FUN_005b5e40(UNK_01015440, (start + sizeRead) - actual, UNK_0104ad80,
                    0x1010, ((StreamReader*)DAT_011de45c)->FUN_008df040());
        }
        }
    }
}
