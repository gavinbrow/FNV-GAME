struct QueryObject { virtual void First(); virtual float Evaluate(int first, int second, int mode); int FUN_00e224d0(int first, int second, float threshold); };
int QueryObject::FUN_00e224d0(int first, int second, float threshold) {
    return Evaluate(first, second, 1) <= threshold;
}
