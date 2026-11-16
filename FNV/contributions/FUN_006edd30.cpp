struct Position_006edd30 {
    float x;
    float y;
    float z;
    float FUN_004b6190(const Position_006edd30*);
};
struct PositionArray_006edd30 {
    void FUN_006971e0(Position_006edd30*, unsigned short);
};
struct PositionIndex_006edd30 {
    PositionArray_006edd30* source;
    unsigned short itemIndex;
};
struct PositionCollection_006edd30 {
    PositionIndex_006edd30* FUN_006dad90(unsigned int);
};
struct Stamp_006edd30 {
    unsigned int FUN_0068efb0();
};
struct LocationContext_006edd30 {
    Stamp_006edd30* stampSource;
    unsigned short index;
    unsigned short flags;
    unsigned int formID;
};
struct ContextProvider_006edd30 {
    LocationContext_006edd30* FUN_006ced70();
};
struct PointerList_006edd30 {
    void* entries;
    unsigned int capacity;
    unsigned int size;
    unsigned int flags;
    unsigned int revision;
    unsigned int* FUN_006f2270();
    void FUN_007cb2e0(void**);
};
struct Location_006edd30 {
    Position_006edd30 position;
    unsigned int unknown0C;
    unsigned int unknown10;
    unsigned int unknown14;
    unsigned int unknown18;
    unsigned int unknown1C;
    unsigned int unknown20;
    unsigned int stamp;
    unsigned short index;
    unsigned short flags;
    PointerList_006edd30 relatedPaths;
};
struct PathEdge_006edd30 {
    unsigned int nodeKey;
    Location_006edd30* location;
    unsigned int stamp;
    unsigned short index;
    unsigned short flags;
    unsigned int nextIndex;
    unsigned char active;
    unsigned char color;
    unsigned short padding16;
    unsigned int state;
};
struct Path_006edd30 {
    Location_006edd30* start;
    Location_006edd30* finish;
    unsigned int unknown08;
    unsigned int unknown0C;
    unsigned int unknown10;
    unsigned int unknown14;
    unsigned int unknown18;
    unsigned int unknown1C;
    unsigned int unknown20;
    unsigned int unknown24;
    unsigned int unknown28;
    unsigned int unknown2C;
    unsigned int unknown30;
    unsigned int unknown34;
    float distance;
    unsigned int stamp;
    unsigned short index;
    unsigned short flag42;
    unsigned int formID;
    unsigned int state;
    PathEdge_006edd30* startEdge;
    PathEdge_006edd30* finishEdge;
};
struct FUN_006edd30_shell {
    unsigned int unknown00;
    unsigned int unknown04;
    unsigned int unknown08;
    unsigned int unknown0C;
    unsigned int unknown10;
    unsigned int unknown14;
    unsigned int unknown18;
    unsigned int unknown1C;
    PositionCollection_006edd30* positions;
    ContextProvider_006edd30* contexts;
    unsigned int unknown28;
    unsigned int unknown2C;
    unsigned int unknown30;
    unsigned int unknown34;
    unsigned int unknown38;
    unsigned int unknown3C;
    PointerList_006edd30 starts;
    PointerList_006edd30 ends;
    PointerList_006edd30 startEdges;
    PointerList_006edd30 endEdges;
    PointerList_006edd30 paths;
    Location_006edd30* FUN_006edc40();
    PathEdge_006edd30* FUN_006edfc0();
    Path_006edd30* FUN_006ee070();
    void FUN_006edd30(const Position_006edd30* start, const Position_006edd30* finish);
};
void FUN_006edd30_shell::FUN_006edd30(const Position_006edd30* start, const Position_006edd30* finish)
{
    Location_006edd30* startLocation2 = FUN_006edc40();
    LocationContext_006edd30* context_2 = contexts->FUN_006ced70();
    startLocation2->stamp = context_2->stampSource->FUN_0068efb0();
    startLocation2->index = context_2->index;
    startLocation2->position = *start;

    Location_006edd30* finishLocation = FUN_006edc40();
    finishLocation->stamp = context_2->stampSource->FUN_0068efb0();
    finishLocation->index = context_2->index;
    finishLocation->position = *finish;

    PathEdge_006edd30* startEdge = FUN_006edfc0();
    startEdge->nodeKey = *starts.FUN_006f2270();
    startEdge->location = startLocation2;
    startEdge->stamp = context_2->stampSource->FUN_0068efb0();
    startEdge->index = context_2->index;
    startEdge->nextIndex = 0xffffffff;
    startEdge->state = 0;
    startEdge->active = 1;

    PathEdge_006edd30* finishEdge4 = FUN_006edfc0();
    finishEdge4->nodeKey = *ends.FUN_006f2270();
    finishEdge4->location = finishLocation;
    finishEdge4->stamp = context_2->stampSource->FUN_0068efb0();
    finishEdge4->index = context_2->index;
    finishEdge4->nextIndex = 0xffffffff;
    finishEdge4->state = 0;
    finishEdge4->active = 1;

    Path_006edd30* path5 = FUN_006ee070();
    path5->start = startLocation2;
    path5->finish = finishLocation;
    path5->stamp = context_2->stampSource->FUN_0068efb0();
    path5->index = context_2->index;
    path5->formID = context_2->formID;
    path5->state = 0;
    path5->startEdge = startEdge;
    path5->finishEdge = finishEdge4;
    startLocation2->relatedPaths.FUN_007cb2e0((void**)&path5);
    finishLocation->relatedPaths.FUN_007cb2e0((void**)&path5);

    Position_006edd30 firstPositionVal;
    Position_006edd30 lastPosition;
    positions->FUN_006dad90(0)->source->FUN_006971e0(&firstPositionVal, positions->FUN_006dad90(0)->itemIndex);
    positions->FUN_006dad90(1)->source->FUN_006971e0(&lastPosition, positions->FUN_006dad90(1)->itemIndex);
    path5->distance = firstPositionVal.FUN_004b6190(&lastPosition);

    starts.FUN_007cb2e0((void**)&startLocation2);
    ends.FUN_007cb2e0((void**)&finishLocation);
    startEdges.FUN_007cb2e0((void**)&startEdge);
    endEdges.FUN_007cb2e0((void**)&finishEdge4);
    paths.FUN_007cb2e0((void**)&path5);
}
