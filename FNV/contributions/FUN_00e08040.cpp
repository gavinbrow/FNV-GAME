struct Node
{
    int unk00; unsigned char leaf; int unk08,unk0C,unk10,unk14,unk18,unk1C,unk20,unk24,unk28,unk2C,unk30,unk34;
    unsigned char complete;
    int unk3C,unk40,unk44,unk48,unk4C,unk50,unk54,unk58,unk5C,unk60,unk64,unk68,unk6C;
    Node* left; Node* right;
};
struct __declspec(align(8)) State
{
    int depth; bool retrying;
    int unk08,unk0C,unk10,unk14,unk18,unk1C,unk20,unk24,unk28,unk2C,unk30,unk34,unk38,unk3C,unk40,unk44;
    State() {}
    State(const State&,Node*,float*);
    void FUN_00e095d0(const State*,Node*,float*);
};
struct MergeInfo { bool changed; int index; int unk08,unk0C,unk10; };
struct CheckResult { bool value; CheckResult(bool v):value(v){} operator bool() const { return value; } };
struct Tracker { int unk00,unk04,unk08,count; };
void __stdcall FUN_00e06b20(Node*);
void __stdcall FUN_00e07510(Node*,void*,State*,MergeInfo*);
struct TreeOptimizer
{
    int unk00,unk04,unk08,unk0C; Tracker* tracker; int unk14,threshold,unk1C,unk20,limit,count,unk2C;
    float config30,config34,config38,config3C,config40,config44,config48,config4C,config50,config54,config58,config5C,config60,config64,config68,config6C;
    int period;
    CheckResult FUN_00e06af0(Node*,State*);
    int FUN_00e07c50(Node*,void*,State*);
    void FUN_00e06aa0(Node*);
    int FUN_00e07ca0(Node*,void*,State*,MergeInfo*);
    int FUN_00e08040(Node*,void*,State*);
};
int TreeOptimizer::FUN_00e08040(Node* node,void* context,State* state)
{
    if(node->complete) return 3;
    if(state->depth <= threshold && state->depth % period == 0 && !state->retrying)
    {
        state->retrying=true;
        int result=-1;
        int savedThreshold=threshold;
        while(!node->complete)
        {
            int previousCount=tracker->count;
            State copy=*state;
            result=FUN_00e08040(node,context,&copy);
            if(count>limit) break;
            if(previousCount==tracker->count)
            {
                if(threshold<0) break;
                threshold-=period;
            }
        }
        threshold=savedThreshold;
        state->retrying=false;
        return result;
    }
    if(node->leaf)
    {
        FUN_00e06b20(node);
        if(FUN_00e06af0(node,state)) return FUN_00e07c50(node,context,state);
    }
    else
    {
        MergeInfo info;
        info.changed=false;
        info.index=-1;
        FUN_00e07510(node,context,state,&info);
        int score=-1;
        {

        Node* rightChild=node->right;
        if(rightChild)
        {
            State copy;
            copy.FUN_00e095d0(state,rightChild,&config30);
            score=FUN_00e08040(rightChild,state,&copy);
            if(score>=0) FUN_00e06aa0(rightChild);
        }
        Node* leftChild=node->left;
        if(leftChild)
        {
            State copy;
            copy.FUN_00e095d0(state,leftChild,&config30);
            int leftResult=FUN_00e08040(leftChild,state,&copy);
            if(leftResult>=0)
            {
                FUN_00e06aa0(leftChild);
                if(score>=0 && FUN_00e06af0(node,state))
                {
                    ++count;
                    return FUN_00e07ca0(node,context,state,&info)+leftResult+score;
                }
            }
        }
    }
    }
    return -1;
}









