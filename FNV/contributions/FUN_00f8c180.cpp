// @fnv 0x00f8c180
struct GO { GO(int); ~GO(); };
struct Fader { bool enabled; int *pointer; float data[4]; GO go; };
extern "C" int DAT_0106ea2c, DAT_0106ea20;
extern "C" Fader s_faders[3] = {
    {true, &DAT_0106ea2c, {}, GO(0)},
    {false, &DAT_0106ea2c, {}, GO(0)},
    {false, &DAT_0106ea20, {}, GO(0)}
};
