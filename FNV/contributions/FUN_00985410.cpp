struct EventVector
{
    unsigned int x;
    unsigned int y;
    unsigned int z;
    unsigned int w;
    void FUN_0097ede0();
};
struct TimeStamp
{
    unsigned int value;
    void FUN_004300a0();
};
struct TimeValue
{
    float value;
    void FUN_00435de0(float time);
};
float __cdecl FUN_00435dd0();
extern float DAT_0108d540;
struct EventSource
{
    EventVector FUN_00575650();
};
struct EventRecord
{
    EventSource* source;
    unsigned int status;
    EventVector primary;
    EventVector secondary;
    EventVector tertiary;
    EventVector quaternary;
    unsigned short type;
    unsigned short subtype;
    TimeValue initialTime;
    TimeValue previousTime;
    TimeStamp start;
    TimeValue timeNow;
    TimeStamp last;
    TimeValue endTime;
    unsigned char started;
    unsigned char ended;
    EventRecord* FUN_00985410(EventSource* src, unsigned short eventType);
};
EventRecord* EventRecord::FUN_00985410(EventSource* src, unsigned short eventType)
{
    source = src;
    status = 0;
    primary.FUN_0097ede0();
    secondary.FUN_0097ede0();
    tertiary.FUN_0097ede0();
    quaternary.FUN_0097ede0();
    type = eventType;
    subtype = 0;
    initialTime.FUN_00435de0(-DAT_0108d540);
    previousTime.FUN_00435de0(-DAT_0108d540);
    start.FUN_004300a0();
    timeNow.FUN_00435de0(FUN_00435dd0());
    last.FUN_004300a0();
    endTime.FUN_00435de0(-DAT_0108d540);
    started = 0;
    ended = 0;
    primary = src->FUN_00575650();
    return this;
}