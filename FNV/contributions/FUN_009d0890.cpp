class FUN_009d0890_base
{
public:
    virtual ~FUN_009d0890_base();
    unsigned int m_04;
    unsigned int m_08;
    unsigned int m_0c;
    FUN_009d0890_base();
};

struct FUN_00906f60
{
    unsigned int m_00;
    unsigned int m_04;
    FUN_00906f60();
};

struct FUN_009d0890_Vec3
{
    unsigned int x;
    unsigned int y;
    unsigned int z;
};

class FUN_009d0890 : public FUN_009d0890_base
{
public:
    virtual ~FUN_009d0890();
    unsigned int m_10;
    FUN_009d0890_Vec3 m_14;
    FUN_00906f60 m_20;
    FUN_00906f60 m_28;
    FUN_00906f60 m_30;
    FUN_00906f60 m_38;
    FUN_00906f60 m_40;

    FUN_009d0890();
};

FUN_009d0890::FUN_009d0890()
    : FUN_009d0890_base(), m_10(0),
      m_14(*reinterpret_cast<const FUN_009d0890_Vec3*>(&DAT_011f426c))
{
}
