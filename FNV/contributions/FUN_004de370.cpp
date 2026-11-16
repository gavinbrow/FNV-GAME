struct ConstructorBase
{
    ConstructorBase(int setting, float value);
    ~ConstructorBase();
    virtual void BaseAction();
};

struct ConstructorObserver
{
    virtual void OnDestructed();
    virtual void OnConstructed(ConstructorBase* instance);
};

ConstructorObserver* __cdecl FUN_004de490();

struct FUN_004de370 : ConstructorBase
{
    FUN_004de370(int setting, float value);
    virtual void Update();
};

FUN_004de370::FUN_004de370(int setting, float value)
    : ConstructorBase(setting, value)
{
    FUN_004de490()->OnConstructed(this);
}