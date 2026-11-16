struct LinearTask
{
    unsigned int taskId;
    unsigned int flags;
    unsigned int state;
    ~LinearTask();
};

struct RenderTask
{
    unsigned int type;
    unsigned int index;
    unsigned int input;
    unsigned int output;
    unsigned int width;
    unsigned int height;
    unsigned int format;
    unsigned int options;
    ~RenderTask();
};

struct FUN_00ba3620
{
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    LinearTask linearTasks[3];
    RenderTask renderTasks[24];
    ~FUN_00ba3620();
};

FUN_00ba3620::~FUN_00ba3620()
{
}