struct FNVPosition3 { float x; float y; float z; };
struct FNVPositionReference { void** virtualFunctions; };
typedef void (__thiscall *FNVReadPosition)(FNVPositionReference*, FNVPosition3*);
extern __declspec(thread) unsigned char gTracePositionConditions;
extern void __cdecl LogPositionCondition(const char* message, ...);

bool __cdecl FUN_0059c230(FNVPositionReference* reference, int coordinate, void* unused, double& result)
{
    int requestedCoordinate = coordinate;
    if (reference != 0) {
        FNVPosition3 position;
        (reinterpret_cast<FNVReadPosition>(reference->virtualFunctions[92]))(reference, &position);
        switch (requestedCoordinate) {
        case 'X': result = position.x; break;
        case 'Y': result = position.y; break;
        case 'Z': result = position.z; break;
        }
        if (gTracePositionConditions)
            LogPositionCondition("GetStartingPos: %c >> %0.2f", requestedCoordinate, result);
    }
    return true;
}