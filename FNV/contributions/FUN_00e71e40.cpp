extern "C" __declspec(dllimport) void __stdcall fnv_EnterCriticalSection(void*);

extern "C" __declspec(dllimport) void __stdcall fnv_LeaveCriticalSection(void*);

extern "C" void __cdecl operator_delete_sized(void* pvMem, unsigned int uiSize);



struct Item;

struct Node;

struct ArrayObj;



struct TargetObj {

    bool Invoke(FUN_00e744b0_Src* p);

};



struct Map {

    bool Get(void* key, Node*& outVal);

    void Set(void* key, Node* val);

    bool Remove(void* key);

};



struct E71E40 {

    unsigned int unk_000; unsigned int unk_004; unsigned int unk_008; unsigned int unk_00c; unsigned int unk_010; unsigned int unk_014; unsigned int unk_018; unsigned int unk_01c;

    unsigned int unk_020; unsigned int unk_024; unsigned int unk_028; unsigned int unk_02c; unsigned int unk_030; unsigned int unk_034; unsigned int unk_038; unsigned int unk_03c;

    unsigned int unk_040; unsigned int unk_044; unsigned int unk_048; unsigned int unk_04c; unsigned int unk_050; unsigned int unk_054; unsigned int unk_058; unsigned int unk_05c;

    unsigned int unk_060; unsigned int unk_064; unsigned int unk_068; unsigned int unk_06c; unsigned int unk_070; unsigned int unk_074; unsigned int unk_078; unsigned int unk_07c;

    unsigned int cs1_080; unsigned int cs1_084; unsigned int cs1_088; unsigned int cs1_08c; unsigned int cs1_090; unsigned int cs1_094; unsigned int cs1_098; unsigned int cs1_09c;

    unsigned int cs1_0a0; unsigned int cs1_0a4; unsigned int cs1_0a8; unsigned int cs1_0ac; unsigned int cs1_0b0; unsigned int cs1_0b4; unsigned int cs1_0b8; unsigned int cs1_0bc;

    unsigned int cs1_0c0; unsigned int cs1_0c4; unsigned int cs1_0c8; unsigned int cs1_0cc; unsigned int cs1_0d0; unsigned int cs1_0d4; unsigned int cs1_0d8; unsigned int cs1_0dc;

    unsigned int cs1_0e0; unsigned int cs1_0e4; unsigned int cs1_0e8; unsigned int cs1_0ec; unsigned int cs1_0f0; unsigned int cs1_0f4; unsigned int cs1_0f8; unsigned int cs1_0fc;

    unsigned int cs2_100; unsigned int cs2_104; unsigned int cs2_108; unsigned int cs2_10c; unsigned int cs2_110; unsigned int cs2_114; unsigned int cs2_118; unsigned int cs2_11c;

    unsigned int cs2_120; unsigned int cs2_124; unsigned int cs2_128; unsigned int cs2_12c; unsigned int cs2_130; unsigned int cs2_134; unsigned int cs2_138; unsigned int cs2_13c;

    unsigned int cs2_140; unsigned int cs2_144; unsigned int cs2_148; unsigned int cs2_14c; unsigned int cs2_150; unsigned int cs2_154; unsigned int cs2_158; unsigned int cs2_15c;

    unsigned int cs2_160; unsigned int cs2_164; unsigned int cs2_168; unsigned int cs2_16c; unsigned int cs2_170; unsigned int cs2_174; unsigned int cs2_178; unsigned int cs2_17c;

    unsigned int cs2_180; unsigned int cs2_184; unsigned int cs2_188; unsigned int cs2_18c; unsigned int cs2_190; unsigned int cs2_194; unsigned int cs2_198; unsigned int cs2_19c;

    unsigned int cs2_1a0; unsigned int cs2_1a4; unsigned int cs2_1a8; unsigned int cs2_1ac; unsigned int cs2_1b0; unsigned int cs2_1b4; unsigned int cs2_1b8; unsigned int cs2_1bc;

    unsigned int cs2_1c0; unsigned int cs2_1c4; unsigned int cs2_1c8; unsigned int cs2_1cc; unsigned int cs2_1d0; unsigned int cs2_1d4; unsigned int cs2_1d8; unsigned int cs2_1dc;

    unsigned int cs2_1e0; unsigned int cs2_1e4; unsigned int cs2_1e8; unsigned int cs2_1ec; unsigned int cs2_1f0; unsigned int cs2_1f4; unsigned int cs2_1f8; unsigned int cs2_1fc;

    unsigned int cs2_200; unsigned int cs2_204; unsigned int cs2_208; unsigned int cs2_20c; unsigned int cs2_210; unsigned int cs2_214; unsigned int cs2_218; unsigned int cs2_21c;

    unsigned int cs2_220; unsigned int cs2_224; unsigned int cs2_228; unsigned int cs2_22c; unsigned int cs2_230; unsigned int cs2_234; unsigned int cs2_238; unsigned int cs2_23c;

    unsigned int cs2_240; unsigned int cs2_244; unsigned int cs2_248; unsigned int cs2_24c; unsigned int cs2_250; unsigned int cs2_254; unsigned int cs2_258; unsigned int cs2_25c;

    unsigned int cs2_260; unsigned int cs2_264; unsigned int cs2_268; unsigned int cs2_26c; unsigned int cs2_270; unsigned int cs2_274; unsigned int cs2_278; unsigned int cs2_27c;

    unsigned int cs2_280; unsigned int cs2_284; unsigned int cs2_288; unsigned int cs2_28c; unsigned int cs2_290; unsigned int cs2_294; unsigned int cs2_298; unsigned int cs2_29c;

    unsigned int cs2_2a0; unsigned int cs2_2a4; unsigned int cs2_2a8; unsigned int cs2_2ac; unsigned int cs2_2b0; unsigned int cs2_2b4; unsigned int cs2_2b8; unsigned int cs2_2bc;

    unsigned int cs2_2c0; unsigned int cs2_2c4; unsigned int cs2_2c8; unsigned int cs2_2cc; unsigned int cs2_2d0; unsigned int cs2_2d4; unsigned int cs2_2d8; unsigned int cs2_2dc;

    unsigned int cs2_2e0; unsigned int cs2_2e4; unsigned int cs2_2e8; unsigned int cs2_2ec; unsigned int cs2_2f0; unsigned int cs2_2f4; unsigned int cs2_2f8; unsigned int cs2_2fc;

    unsigned int cs2_300; unsigned int cs2_304; unsigned int cs2_308; unsigned int cs2_30c; unsigned int cs2_310; unsigned int cs2_314; unsigned int cs2_318; unsigned int cs2_31c;

    unsigned int cs2_320; unsigned int cs2_324; unsigned int cs2_328; unsigned int cs2_32c; unsigned int cs2_330; unsigned int cs2_334; unsigned int cs2_338; unsigned int cs2_33c;

    unsigned int cs2_340; unsigned int cs2_344; unsigned int cs2_348; unsigned int cs2_34c; unsigned int cs2_350; unsigned int cs2_354; unsigned int cs2_358; unsigned int cs2_35c;

    unsigned int cs2_360; unsigned int cs2_364; unsigned int cs2_368; unsigned int cs2_36c; unsigned int cs2_370; unsigned int cs2_374; unsigned int cs2_378; unsigned int cs2_37c;

    unsigned int cs2_380; unsigned int cs2_384; unsigned int cs2_388; unsigned int cs2_38c; unsigned int cs2_390; unsigned int cs2_394; unsigned int cs2_398; unsigned int cs2_39c;

    unsigned int cs2_3a0; unsigned int cs2_3a4; unsigned int cs2_3a8; unsigned int cs2_3ac; unsigned int cs2_3b0; unsigned int cs2_3b4; unsigned int cs2_3b8; unsigned int cs2_3bc;

    unsigned int cs2_3c0; unsigned int cs2_3c4; unsigned int cs2_3c8; unsigned int cs2_3cc; unsigned int cs2_3d0; unsigned int cs2_3d4; unsigned int cs2_3d8; unsigned int cs2_3dc;

    unsigned int cs2_3e0; unsigned int cs2_3e4; unsigned int cs2_3e8; unsigned int cs2_3ec; unsigned int cs2_3f0; unsigned int cs2_3f4; unsigned int cs2_3f8; unsigned int cs2_3fc;

    unsigned int cs2_400; unsigned int cs2_404; unsigned int cs2_408; unsigned int cs2_40c; unsigned int cs2_410; unsigned int cs2_414; unsigned int cs2_418; unsigned int cs2_41c;

    unsigned int cs2_420; unsigned int cs2_424; unsigned int cs2_428; unsigned int cs2_42c; unsigned int cs2_430; unsigned int cs2_434; unsigned int cs2_438; unsigned int cs2_43c;

    unsigned int cs2_440; unsigned int cs2_444; unsigned int cs2_448; unsigned int cs2_44c; unsigned int cs2_450; unsigned int cs2_454; unsigned int cs2_458; unsigned int cs2_45c;

    unsigned int cs2_460; unsigned int cs2_464; unsigned int cs2_468; unsigned int cs2_46c; unsigned int cs2_470; unsigned int cs2_474; unsigned int cs2_478; unsigned int cs2_47c;

    unsigned int cs2_480; unsigned int cs2_484; unsigned int cs2_488; unsigned int cs2_48c; unsigned int cs2_490; unsigned int cs2_494; unsigned int cs2_498; unsigned int cs2_49c;

    unsigned int cs2_4a0; unsigned int cs2_4a4; unsigned int cs2_4a8; unsigned int cs2_4ac; unsigned int cs2_4b0; unsigned int cs2_4b4; unsigned int cs2_4b8; unsigned int cs2_4bc;

    unsigned int cs2_4c0; unsigned int cs2_4c4; unsigned int cs2_4c8; unsigned int cs2_4cc; unsigned int cs2_4d0; unsigned int cs2_4d4; unsigned int cs2_4d8; unsigned int cs2_4dc;

    unsigned int cs2_4e0; unsigned int cs2_4e4; unsigned int cs2_4e8; unsigned int cs2_4ec; unsigned int cs2_4f0; unsigned int cs2_4f4; unsigned int cs2_4f8; unsigned int cs2_4fc;

    unsigned int cs2_500; unsigned int cs2_504; unsigned int cs2_508; unsigned int cs2_50c; unsigned int cs2_510; unsigned int cs2_514; unsigned int cs2_518; unsigned int cs2_51c;

    unsigned int cs2_520; unsigned int cs2_524; unsigned int cs2_528; unsigned int cs2_52c; unsigned int cs2_530; unsigned int cs2_534; unsigned int cs2_538; unsigned int cs2_53c;

    unsigned int cs2_540; unsigned int cs2_544; unsigned int cs2_548; unsigned int cs2_54c; unsigned int cs2_550; unsigned int cs2_554; unsigned int cs2_558; unsigned int cs2_55c;

    unsigned int cs2_560; unsigned int cs2_564; unsigned int cs2_568; unsigned int cs2_56c; unsigned int cs2_570; unsigned int cs2_574; unsigned int cs2_578; unsigned int cs2_57c;

    unsigned int cs2_580; unsigned int cs2_584; unsigned int cs2_588; unsigned int cs2_58c; unsigned int cs2_590; unsigned int cs2_594; unsigned int cs2_598; unsigned int cs2_59c;

    unsigned int cs2_5a0; unsigned int cs2_5a4; unsigned int cs2_5a8; unsigned int cs2_5ac; unsigned int cs2_5b0; unsigned int cs2_5b4; unsigned int cs2_5b8; unsigned int cs2_5bc;

    unsigned int cs2_5c0; unsigned int cs2_5c4; unsigned int cs2_5c8; unsigned int cs2_5cc; unsigned int cs2_5d0; unsigned int cs2_5d4; unsigned int cs2_5d8; unsigned int cs2_5dc;

    unsigned int cs2_5e0; unsigned int cs2_5e4; unsigned int cs2_5e8; unsigned int cs2_5ec; unsigned int cs2_5f0; unsigned int cs2_5f4; unsigned int cs2_5f8; unsigned int cs2_5fc;

    unsigned int cs2_600; unsigned int cs2_604; unsigned int cs2_608; unsigned int cs2_60c;

    Map m_map;

    unsigned int after_map_614; unsigned int after_map_618; unsigned int after_map_61c; unsigned int after_map_620; unsigned int after_map_624; unsigned int after_map_628; unsigned int after_map_62c; unsigned int after_map_630;

    unsigned int after_map_634; unsigned int after_map_638; unsigned int after_map_63c; unsigned int after_map_640; unsigned int after_map_644; unsigned int after_map_648; unsigned int after_map_64c; unsigned int after_map_650;

    unsigned int after_map_654; unsigned int after_map_658; unsigned int after_map_65c; unsigned int after_map_660; unsigned int after_map_664; unsigned int after_map_668; unsigned int after_map_66c; unsigned int after_map_670;

    unsigned int after_map_674; unsigned int after_map_678; unsigned int after_map_67c; unsigned int after_map_680; unsigned int after_map_684; unsigned int after_map_688; unsigned int after_map_68c; unsigned int after_map_690;

    unsigned int after_map_694; unsigned int after_map_698; unsigned int after_map_69c; unsigned int after_map_6a0; unsigned int after_map_6a4; unsigned int after_map_6a8; unsigned int after_map_6ac; unsigned int after_map_6b0;

    unsigned int after_map_6b4; unsigned int after_map_6b8; unsigned int after_map_6bc; unsigned int after_map_6c0; unsigned int after_map_6c4; unsigned int after_map_6c8; unsigned int after_map_6cc; unsigned int after_map_6d0;

    unsigned int after_map_6d4; unsigned int after_map_6d8; unsigned int after_map_6dc; unsigned int after_map_6e0; unsigned int after_map_6e4; unsigned int after_map_6e8; unsigned int after_map_6ec; unsigned int after_map_6f0;

    unsigned int after_map_6f4; unsigned int after_map_6f8; unsigned int after_map_6fc; unsigned int after_map_700; unsigned int after_map_704; unsigned int after_map_708; unsigned int after_map_70c; unsigned int after_map_710;

    unsigned int after_map_714; unsigned int after_map_718; unsigned int after_map_71c; unsigned int after_map_720; unsigned int after_map_724; unsigned int after_map_728; unsigned int after_map_72c; unsigned int after_map_730;

    unsigned int after_map_734; unsigned int after_map_738; unsigned int after_map_73c; unsigned int after_map_740; unsigned int after_map_744; unsigned int after_map_748; unsigned int after_map_74c; unsigned int after_map_750;

    unsigned int after_map_754; unsigned int after_map_758; unsigned int after_map_75c; unsigned int after_map_760; unsigned int after_map_764; unsigned int after_map_768; unsigned int after_map_76c; unsigned int after_map_770;

    unsigned int after_map_774; unsigned int after_map_778; unsigned int after_map_77c; unsigned int after_map_780; unsigned int after_map_784; unsigned int after_map_788; unsigned int after_map_78c; unsigned int after_map_790;

    unsigned int after_map_794; unsigned int after_map_798; unsigned int after_map_79c; unsigned int after_map_7a0; unsigned int after_map_7a4; unsigned int after_map_7a8; unsigned int after_map_7ac; unsigned int after_map_7b0;

    unsigned int after_map_7b4; unsigned int after_map_7b8; unsigned int after_map_7bc; unsigned int after_map_7c0; unsigned int after_map_7c4; unsigned int after_map_7c8; unsigned int after_map_7cc; unsigned int after_map_7d0;

    unsigned int after_map_7d4; unsigned int after_map_7d8; unsigned int after_map_7dc; unsigned int after_map_7e0; unsigned int after_map_7e4; unsigned int after_map_7e8; unsigned int after_map_7ec; unsigned int after_map_7f0;

    unsigned int after_map_7f4; unsigned int after_map_7f8; unsigned int after_map_7fc; unsigned int after_map_800; unsigned int after_map_804; unsigned int after_map_808; unsigned int after_map_80c; unsigned int after_map_810;

    unsigned int after_map_814; unsigned int after_map_818; unsigned int after_map_81c; unsigned int after_map_820; unsigned int after_map_824; unsigned int after_map_828; unsigned int after_map_82c; unsigned int after_map_830;

    unsigned int after_map_834; unsigned int after_map_838; unsigned int after_map_83c; unsigned int after_map_840; unsigned int after_map_844; unsigned int after_map_848; unsigned int after_map_84c; unsigned int after_map_850;

    unsigned int after_map_854; unsigned int after_map_858; unsigned int after_map_85c; unsigned int after_map_860; unsigned int after_map_864; unsigned int after_map_868; unsigned int after_map_86c; unsigned int after_map_870;

    unsigned int after_map_874; unsigned int after_map_878; unsigned int after_map_87c; unsigned int after_map_880; unsigned int after_map_884; unsigned int after_map_888; unsigned int after_map_88c; unsigned int after_map_890;

    unsigned int after_map_894; unsigned int after_map_898; unsigned int after_map_89c; unsigned int after_map_8a0; unsigned int after_map_8a4; unsigned int after_map_8a8;

    TargetObj* m_target;



    void FUN_00e71e40(FUN_00e744b0_Src* p);

};



struct ArrayEntry {

    unsigned int unk00;

    void* m_key;

};



struct ArrayObj {

    unsigned int arr_unk_000; unsigned int arr_unk_004; unsigned int arr_unk_008; unsigned int arr_unk_00c; unsigned int arr_unk_010; unsigned int arr_unk_014; unsigned int arr_unk_018; unsigned int arr_unk_01c;

    unsigned int m_size;

    unsigned int arr_unk_24;

    ArrayEntry** m_pBase;



    ArrayEntry* GetAt(unsigned int i) const {

        if (i < m_size)

            return m_pBase[i];

        return 0;

    }

};



struct Item {

    unsigned int item_unk_000; unsigned int item_unk_004; unsigned int item_unk_008; unsigned int item_unk_00c; unsigned int item_unk_010; unsigned int item_unk_014; unsigned int item_unk_018; unsigned int item_unk_01c;

    unsigned int item_unk_020; unsigned int item_unk_024;

    ArrayObj* m_array;

};



struct Node {

    unsigned int node_unk_000; unsigned int node_unk_004;

    Item* m_item;

    unsigned int node_mid_00c; unsigned int node_mid_010; unsigned int node_mid_014; unsigned int node_mid_018; unsigned int node_mid_01c;

    Node* m_next;



    static void operator delete(void* pvMem, unsigned int uiSize) {

        operator_delete_sized(pvMem, uiSize);

    }

};



void E71E40::FUN_00e71e40(FUN_00e744b0_Src* p) {

    if (!p) return;

    Item* items = (Item*)p->unk0c;

    if (!items || !items->m_array) return;

    if (p->unk08 > 0) {

        Item* item = items;

        unsigned int count = p->unk08;

        do {

            ArrayObj* arr = item->m_array;

            if (arr->m_size <= 0 || arr->m_pBase[0] == 0) {

            } else {

                fnv_EnterCriticalSection(&cs1_080);

                fnv_EnterCriticalSection(&cs2_100);



                for (unsigned int i = 0; i < arr->m_size; ++i) {

                    void* key = arr->GetAt(i)->m_key;

                    Node* outNode = 0;

                    if (m_map.Get(key, outNode)) {

                        Node* curr = outNode;

                        Node* prev = 0;

                        while (curr) {

                            if (curr->m_item == item) {

                                Node* next = 0;

                                if (prev) {

                                    prev->m_next = curr->m_next;

                                    next = curr->m_next;

                                } else if (curr->m_next) {

                                    m_map.Set(key, static_cast<Node* const volatile&>(curr->m_next));

                                    next = curr->m_next;

                                } else {

                                    m_map.Remove(key);

                                }

                                curr->m_next = 0;

                                delete curr;

                                curr = next;

                            } else {

                                prev = curr;

                                curr = curr->m_next;

                            }

                        }

                    }

                }



                fnv_LeaveCriticalSection(&cs2_100);

                fnv_LeaveCriticalSection(&cs1_080);

            }

            item++;

        } while (--count);

    }



    m_target->Invoke(p);

}





