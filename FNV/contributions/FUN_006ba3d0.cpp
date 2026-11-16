struct Point2 {
    float x;
    float y;
    Point2();
    Point2 FUN_004e8880(const Point2* rhs) const;
    Point2 FUN_004dfe30(const Point2& rhs) const;
    double FUN_00595c80() const;
};
extern "C" Point2 __cdecl FUN_00532fd0(float scale, const Point2& value);
extern "C" const double DAT_01012060;

Point2* __cdecl FUN_006ba3d0(Point2* result, Point2* a, Point2* b, Point2* c, Point2* d)
{
    float intersection;
    float crossB = (c->x - b->x) * (d->y - b->y) - (c->y - b->y) * (d->x - b->x);
    float total = (c->x - a->x) * (d->y - a->y) - (c->y - a->y) * (d->x - a->x);
    float crossA = (a->x - c->x) * (b->y - c->y) - (a->y - c->y) * (b->x - c->x);
    intersection = (crossA + total) - crossB;
    float fraction = crossA / (crossA - intersection);

    Point2 crossC = c->FUN_004dfe30(FUN_00532fd0(fraction, d->FUN_004e8880(c)));
    if (crossB * total > DAT_01012060) {
        if (crossC.FUN_004e8880(a).FUN_00595c80() < crossC.FUN_004e8880(b).FUN_00595c80()) {
            *result = *a;
            return result;
        } else {
            *result = *b;
            return result;
        }
    } else {
        *result = crossC;
        return result;
    }
}