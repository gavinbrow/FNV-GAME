// Adapted from an unverified prior attempt by another contributor; original author/model unknown.
struct S_d11790_Node { unsigned short min_y, min_z, max_y, max_z, min_x, max_x; unsigned short unk0c, unk0e; };
struct S_d11790_Edge { unsigned short value; unsigned short handle; };

typedef unsigned short S_d11790_Node::* S_d11790_Field;

static __forceinline void S_d11790_Fix(S_d11790_Node* nodes, S_d11790_Edge* edges, S_d11790_Node* node, S_d11790_Field field, unsigned h)
{
    unsigned i = node->*field;
    S_d11790_Edge* e = edges + i;
    while (e[0].value == e[-1].value) {
        unsigned p = e[-1].handle;
        if (!(h < p)) break;
        e[0] = e[-1];
        --e;
        nodes[p].*field = i;
        --i;
    }
    e->handle = h;
    unsigned short* currentField = &(node->*field);
    *currentField = i;
}

struct S_d11790_Sweep {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    int unk40;
    int unk44;
    int unk48;
    int unk4c;
    int unk50;
    int unk54;
    int unk58;
    int unk5c;
    int unk60;
    int unk64;
    int unk68;
    int unk6c;
    int unk70;
    int unk74;
    int unk78;
    int unk7c;
    int unk80;
    int unk84;
    int unk88;
    int unk8c;
    int unk90;
    int unk94;
    int unk98;
    int unk9c;
    S_d11790_Node* nodes;
    int unka4;
    int unka8;
    S_d11790_Edge* axis0;
    int unkb0;
    int unkb4;
    S_d11790_Edge* axis1;
    int unkbc;
    int unkc0;
    S_d11790_Edge* axis2;
    void FUN_00d11790(unsigned h);
};

void S_d11790_Sweep::FUN_00d11790(unsigned h)
{
    S_d11790_Node* nd = nodes;
    S_d11790_Node* n = &nd[h];
    S_d11790_Fix(nd, axis0, n, &S_d11790_Node::min_x, h);
    S_d11790_Fix(nd, axis0, n, &S_d11790_Node::max_x, h);
    S_d11790_Fix(nd, axis1, n, &S_d11790_Node::min_y, h);
    S_d11790_Fix(nd, axis1, n, &S_d11790_Node::max_y, h);
    S_d11790_Fix(nd, axis2, n, &S_d11790_Node::min_z, h);
    S_d11790_Fix(nd, axis2, n, &S_d11790_Node::max_z, h);
}


