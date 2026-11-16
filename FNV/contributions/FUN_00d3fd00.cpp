void __cdecl FUN_00d3fce0(AgentFuncs*);
void __cdecl FUN_00d3fd00(Agent* agent) {
    AgentFuncs funcs;
    funcs.e = 0;
    funcs.f = 0;
    FUN_00d3fce0(&funcs);
    agent->FUN_00cfbbe0(&funcs, 1, 1);
}