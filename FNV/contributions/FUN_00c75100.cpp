extern __declspec(thread) int g_tlsRoutingMode;

struct RoutingModeScope {
    int previousMode;

    RoutingModeScope() : previousMode(g_tlsRoutingMode) {
        g_tlsRoutingMode = 16;
    }
    ~RoutingModeScope() {
        g_tlsRoutingMode = previousMode;
    }
};

struct RouteTarget {
    virtual void Run(int mode);
};

struct RouteWrapper {
    RouteTarget* target;
    void FUN_00c75100();
};

void RouteWrapper::FUN_00c75100() {
    RoutingModeScope modeScope;
    if (target)
        target->Run(1);
}