class FUN_006ecc40 {
public:
    virtual ~FUN_006ecc40();
    int value04;
    int value08;
    FUN_006ecc40();
};

class FUN_006ed0e0 {
public:
    int value00;
    int value04;
    int value08;
    FUN_006ed0e0();
    ~FUN_006ed0e0();
};

class FUN_006ec000 : public FUN_006ecc40 {
public:
    FUN_006ed0e0 nodes[256];

    FUN_006ec000();
    virtual ~FUN_006ec000();
    void FUN_006ed040(unsigned int count, FUN_006ed0e0* entries);
};

FUN_006ec000::FUN_006ec000()
{
    FUN_006ed040(256, nodes);
}
