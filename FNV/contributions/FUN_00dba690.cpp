struct Inner
{
    virtual void v0();
    virtual void v1();
    virtual void v2();
    virtual void v3();
};
struct This
{
    Inner* object;
    void FUN_00dba690();
};
void This::FUN_00dba690()
{
    object->v3();
}
