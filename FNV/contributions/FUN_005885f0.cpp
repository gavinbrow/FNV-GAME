extern const double DAT_010231b0;
struct CELL_SHELL : public TESObjectCELL {
    bool FUN_0054da20(const NiPoint3* point, float distance,
                      const NiPoint3* otherPoint, float otherDistance,
                      int options, unsigned int context);
    float FUN_0054fb70(const NiPoint3* point);
};
struct WORLD_SHELL : public TESWorldSpace {
    CELL_SHELL* FUN_005875a0(int, int);
    void FUN_005885f0(const NiPoint3* point, float distance,
                      const NiPoint3* otherPoint, float otherDistance,
                      int options, unsigned int context);
};
void WORLD_SHELL::FUN_005885f0(const NiPoint3* point, float distance,
                                  const NiPoint3* otherPoint, float otherDistance,
                                  int options, unsigned int context)
{
    if (options == 0) return;
    {
        int found = 1;
        int j = 0;
        int width = (int)point->x >> 12;
        int i;
        int x;
        {
            CELL_SHELL* cell;
            {
                int y = (int)point->y >> 12;
                cell = FUN_005875a0(width, y);
        if (cell != 0) {
            if (!cell->FUN_0054da20(point, distance, otherPoint, otherDistance, options, context))
                return;
        }
        {
            while (found != 0) {
                width -= 1;
                y -= 1;
                j += 2;
                found = 0;
                for (i = 0; i < j; i++) {
                    cell = FUN_005875a0(width, y);
                    if (cell != 0 &&
                        (distance == DAT_010231b0 || cell->FUN_0054fb70(point) < distance) &&
                        (otherDistance == DAT_010231b0 || cell->FUN_0054fb70(otherPoint) < otherDistance)) {
                        found += 1;
                        if (!cell->FUN_0054da20(point, distance, otherPoint, otherDistance, options, context))
                            return;
                    }
                    width += 1;
                }
                for (x = 0; x < j; x++) {
                    cell = FUN_005875a0(width, y);
                    if (cell != 0 &&
                        (distance == DAT_010231b0 || cell->FUN_0054fb70(point) < distance) &&
                        (otherDistance == DAT_010231b0 || cell->FUN_0054fb70(otherPoint) < otherDistance)) {
                        found += 1;
                        if (!cell->FUN_0054da20(point, distance, otherPoint, otherDistance, options, context))
                            return;
                    }
                    y += 1;
                }
                for (i = 0; i < j; i++) {
                    cell = FUN_005875a0(width, y);
                    if (cell != 0 &&
                        (distance == DAT_010231b0 || cell->FUN_0054fb70(point) < distance) &&
                        (otherDistance == DAT_010231b0 || cell->FUN_0054fb70(otherPoint) < otherDistance)) {
                        found += 1;
                        if (!cell->FUN_0054da20(point, distance, otherPoint, otherDistance, options, context))
                            return;
                    }
                    width -= 1;
                }
                for (x = 0; x < j; x++) {
                    cell = FUN_005875a0(width, y);
                    if (cell != 0 &&
                        (distance == DAT_010231b0 || cell->FUN_0054fb70(point) < distance) &&
                        (otherDistance == DAT_010231b0 || cell->FUN_0054fb70(otherPoint) < otherDistance)) {
                        found += 1;
                        if (!cell->FUN_0054da20(point, distance, otherPoint, otherDistance, options, context))
                            return;
                    }
                    y -= 1;
                }
            }
            cell = (CELL_SHELL*)GetInteriorCell();
            if (cell != 0)
                cell->FUN_0054da20(point, distance, otherPoint, otherDistance, options, context);
        }
        }
        }
    }
}
