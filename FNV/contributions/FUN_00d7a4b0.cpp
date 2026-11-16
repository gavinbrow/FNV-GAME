struct RandomGenerator {
    unsigned int stateFlags;
    unsigned int seed;
    void FUN_00d7a4b0(float* components);
};
void RandomGenerator::FUN_00d7a4b0(float* components)
{
    seed = seed * 1664525u + 1013904223u;
    components[0] = (float)((float)seed * 2.3283064365386963e-10) * 2.0 - 1.0;
    seed = seed * 1664525u + 1013904223u;
    components[1] = (float)((float)seed * 2.3283064365386963e-10) * 2.0 - 1.0;
    seed = seed * 1664525u + 1013904223u;
    components[2] = (float)((float)seed * 2.3283064365386963e-10) * 2.0 - 1.0;
    seed = seed * 1664525u + 1013904223u;
    components[3] = (float)((float)seed * 2.3283064365386963e-10) * 2.0 - 1.0;
}