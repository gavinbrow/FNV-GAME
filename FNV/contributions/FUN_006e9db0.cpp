struct RequestAssigner {
    void FUN_006e5cc0(PathingRequest*);
};
struct QueueAssigner {
    void FUN_006ebfb0(const NiPointer<ActorPathingMessageQueue>&);
};
struct PathingTaskShell : PathingTaskData {
    void FUN_006e9db0(PathingRequest* request, NiPointer<ActorPathingMessageQueue> queue);
};
void PathingTaskShell::FUN_006e9db0(PathingRequest* request,
                                     NiPointer<ActorPathingMessageQueue> queue)
{
    reinterpret_cast<RequestAssigner*>(&spRequest)->FUN_006e5cc0(request);
    reinterpret_cast<QueueAssigner*>(&spQueue)->FUN_006ebfb0(queue);
}