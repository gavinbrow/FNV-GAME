struct ProbeResult {
    void* value;
    ~ProbeResult();
    void* FUN_00458b50();
};

struct ProbeArray {
    unsigned int FUN_00620b80();
    ProbeResult FUN_00464f60(unsigned int index);
};

struct ProbeHolder {
    ProbeArray* FUN_0070ec90();
};

struct ProbeCell {
    ProbeHolder* FUN_005875a0();
};

struct ProbeGrid {
    bool FUN_00425fd0();
    int FUN_00544c30();
    int FUN_00544c60();
    ProbeCell* FUN_0054ddd0(int x, int y);
};

bool __cdecl FUN_005d4a40(void* self, void* value, int mode, float x, float y);

struct Searcher {
    ProbeGrid* FUN_0059bb30();
    bool FUN_006908f0();
};

bool Searcher::FUN_006908f0()
{
    if (FUN_0059bb30()->FUN_00425fd0()) {
        return true;
    }

    bool result = true;
    int cellX2 = FUN_0059bb30()->FUN_00544c30();
    int cellY8 = FUN_0059bb30()->FUN_00544c60();

    float xWorld = (float)(cellX2 << 12);
    ProbeHolder* kWest = FUN_0059bb30()->FUN_0054ddd0(cellX2 - 1, cellY8)->FUN_005875a0();
    if (kWest != 0 && kWest->FUN_0070ec90() != 0) {
        for (unsigned int westIdx = 0; westIdx < kWest->FUN_0070ec90()->FUN_00620b80(); ++westIdx) {
            if (!FUN_005d4a40(this, kWest->FUN_0070ec90()->FUN_00464f60(westIdx).FUN_00458b50(), 1, xWorld, 0.0f)) {
                result = false;
            }
        }
    }

    xWorld = (float)(cellX2 << 12) + 4096.0;
    ProbeHolder* east = FUN_0059bb30()->FUN_0054ddd0(cellX2 + 1, cellY8)->FUN_005875a0();
    if (east != 0 && east->FUN_0070ec90() != 0) {
        for (unsigned int eastIdx = 0; eastIdx < east->FUN_0070ec90()->FUN_00620b80(); ++eastIdx) {
            if (!FUN_005d4a40(this, east->FUN_0070ec90()->FUN_00464f60(eastIdx).FUN_00458b50(), 1, xWorld, 0.0f)) {
                result = false;
            }
        }
    }

    float yWorld = (float)(cellY8 << 12);
    ProbeHolder* southVal = FUN_0059bb30()->FUN_0054ddd0(cellX2, cellY8 - 1)->FUN_005875a0();
    if (southVal != 0 && southVal->FUN_0070ec90() != 0) {
        for (unsigned int southIdx = 0; southIdx < southVal->FUN_0070ec90()->FUN_00620b80(); ++southIdx) {
            if (!FUN_005d4a40(this, southVal->FUN_0070ec90()->FUN_00464f60(southIdx).FUN_00458b50(), 0, 0.0f, yWorld)) {
                result = false;
            }
        }
    }

    yWorld = (float)(cellY8 << 12) + 4096.0;
    ProbeHolder* north2 = FUN_0059bb30()->FUN_0054ddd0(cellX2, cellY8 + 1)->FUN_005875a0();
    if (north2 != 0 && north2->FUN_0070ec90() != 0) {
        for (unsigned int northIdx = 0; northIdx < north2->FUN_0070ec90()->FUN_00620b80(); ++northIdx) {
            if (!FUN_005d4a40(this, north2->FUN_0070ec90()->FUN_00464f60(northIdx).FUN_00458b50(), 0, 0.0f, yWorld)) {
                result = false;
            }
        }
    }

    return result;
}
