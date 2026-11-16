struct NavMeshPayload {
    bool FUN_0076b780(int mode);
};
struct NavMeshListNode {
    void* m_payload;
    unsigned int m_index;
    unsigned int m_state;
    NavMeshListNode* m_next;
    NavMeshListNode(NavMeshPayload* payload);
    bool FUN_0076a3b0(int mode);
    void FUN_00418900(NavMeshPayload* payload);
    void FUN_007a19a0(NavMeshPayload* payload);
};
void NavMeshListNode::FUN_007a19a0(NavMeshPayload* payload) {
    if (payload->FUN_0076b780(0)) return;
    NavMeshListNode* current = this;
    while (current->m_next) current = current->m_next;
    if (current->FUN_0076a3b0(0)) current->m_next = new NavMeshListNode(payload);
    else current->FUN_00418900(payload);
}