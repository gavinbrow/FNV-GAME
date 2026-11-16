struct TimedAction { void FUN_00573170(TESObjectREFR*, int, int, int); };
struct TimedRecord { TimedAction* action; float deadline; };
struct TimedListEntry { bool FUN_008256d0(); TimedRecord** FUN_006815c0(); TimedListEntry* FUN_00726070(); };
struct ExtraDataTiming { TimedListEntry* FUN_0041eda0(); float FUN_0041f020(); void FUN_0041eff0(float); };
extern Twin_0084d030 DAT_011f6394;
class FUN_0056a380_shell {
public:
    virtual void v00(); virtual void v04(); virtual void v08(); virtual void v0c();
    virtual void v10(); virtual void v14(); virtual void v18(); virtual void v1c();
    virtual void v20(); virtual void v24(); virtual void v28(); virtual void v2c();
    virtual void v30(); virtual void v34(); virtual void v38(); virtual void v3c();
    virtual void v40(); virtual void v44(); virtual void v48(); virtual void v4c(unsigned int);
    unsigned char FUN_0056a380();
};
unsigned char FUN_0056a380_shell::FUN_0056a380()
{
    float extraTime;
    {
        float finalTime;
        {
            unsigned char found;
            {
                float current;
                {
                    TimedListEntry* entry;
                    found = 0;
                    extraTime = DAT_011f6394.QFloat();
                    entry = ((ExtraDataTiming*)FUN_005d43c0((TESObjectREFR*)this))->FUN_0041eda0();
                    current = ((ExtraDataTiming*)FUN_005d43c0((TESObjectREFR*)this))->FUN_0041f020();
                    finalTime = current + extraTime;
                    while (entry && !entry->FUN_008256d0()) {
                        TimedRecord* record = *entry->FUN_006815c0();
                        if (record->deadline > current) {
                            if (record->deadline <= finalTime)
                                record->action->FUN_00573170((TESObjectREFR*)this, 0, 0, 1);
                            else
                                found = 1;
                        }
                        entry = entry->FUN_00726070();
                    }
                }
                if (!found) {
                    v4c(0x4000000);
                    finalTime = 0.0f;
                }
                ((ExtraDataTiming*)FUN_005d43c0((TESObjectREFR*)this))->FUN_0041eff0(finalTime);
                return found;
            }
        }
    }
}