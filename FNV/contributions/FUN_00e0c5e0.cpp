struct Bins {
    float weights[8];
    unsigned short counts[8];
    int unk30; int unk34; int unk38; int unk3c;
    double value;
    void FUN_00e0c5e0(struct AxisData* data, struct Point* start, struct Point* end);
};
struct AxisData { int unk00; unsigned int xIndex; unsigned int yIndex; unsigned int mode; float xScale; float yScale; };
struct Point { int unk00; unsigned int x; unsigned int y; };
void Bins::FUN_00e0c5e0(AxisData* data, Point* start, Point* end)
{
    unsigned int x = data->xIndex;
    if (x <= 7) {
        weights[x] += (float)(end->x - start->x) * data->xScale;
        ++counts[x];
    }
    unsigned int y = data->yIndex;
    if (y <= 7) {
        weights[y] += (float)(end->y - start->y) * data->yScale;
        ++counts[y];
    }
    unsigned int mode = data->mode;
    if (mode == 0) value = (double)start->x * data->xScale;
    else if (mode == 1) value = (double)start->y * data->yScale;
}
