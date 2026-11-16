void __cdecl FUN_00ec7c56();

struct FaceCoordinateRange {
    int referenceCount;
    int allocationCount;
    int stride;
    int* begin;
    int* end;
};

struct FaceCoordinateCursor {
    int owner;
    int* current;
    bool FUN_005ca4f0();
    FaceCoordinateRange* FUN_0060b980();
    FaceCoordinateCursor* FUN_0060b900(int count);
};

FaceCoordinateCursor* FaceCoordinateCursor::FUN_0060b900(int count) {
    if (!FUN_005ca4f0()) {
        FUN_00ec7c56();
    }
    do {
    } while (false);

    if (current + count > FUN_0060b980()->end ||
        current + count < FUN_0060b980()->begin) {
        FUN_00ec7c56();
    }
    do {
    } while (false);

    current += count;
    return this;
}