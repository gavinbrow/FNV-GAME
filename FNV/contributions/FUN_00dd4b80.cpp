struct CountProvider {
 virtual void Destroy();
 virtual void Initialize();
 virtual void Reset();
 virtual void Update();
 virtual int GetCount();
};
struct BufferRequirements {
 int unk00; int unk04; int unk08; int additionalCount;
 int unk10; int unk14; int unk18; bool fixedCapacity;
 int FUN_00dd4b80(CountProvider* provider);
};
int BufferRequirements::FUN_00dd4b80(CountProvider* provider)
{
 int count = provider->GetCount() + additionalCount;
 int capacity = fixedCapacity ? 4096 : count;
 return capacity * 224 + count * 20;
}
