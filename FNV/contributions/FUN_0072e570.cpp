class TESBoundObject { public:
virtual void method0();
virtual void method1();
virtual void method2();
virtual void method3();
virtual void method4();
virtual void method5();
virtual void method6();
virtual void method7();
virtual void method8();
virtual void method9();
virtual void method10();
virtual void method11();
virtual void method12();
virtual void method13();
virtual void method14();
virtual void method15();
virtual void method16();
virtual void method17();
virtual void method18();
virtual void method19();
virtual void method20();
virtual void method21();
virtual void method22();
virtual void method23();
virtual void method24();
virtual void method25();
virtual void method26();
virtual void method27();
virtual void method28();
virtual void method29();
virtual void method30();
virtual void method31();
virtual void method32();
virtual void method33();
virtual void method34();
virtual void method35();
virtual void method36();
virtual bool CannotSell();
int FUN_00401170();
};
class TESFullName { public: virtual void method0(); unsigned int GetModelLength() const; };
class TESObjectARMO : public TESBoundObject { public: bool FUN_0047bcf0(); };
class TESObjectWEAP : public TESBoundObject { public: bool FUN_004c94d0(); };
class TESBipedModelForm { public: static TESBipedModelForm* GetFormAsBipedModel(TESBoundObject*); bool FUN_00480d90(); };
class InventoryEntry { public: TESBoundObject* FUN_0044ddc0(); };
bool FUN_00481f10(TESBoundObject*);
bool FUN_0072e570(InventoryEntry* entry)
{
    bool unavailable=false;
    { TESBoundObject* form;
      { TESFullName* name;
        { TESObjectWEAP* weapon;
          { TESBipedModelForm* biped;
            { TESObjectARMO* armor;

    form=entry ? entry->FUN_0044ddc0() : 0;
    biped=TESBipedModelForm::GetFormAsBipedModel(form);
    name=dynamic_cast<TESFullName*>(form);
    armor=entry->FUN_0044ddc0()->FUN_00401170()==0x28 ? static_cast<TESObjectARMO*>(entry->FUN_0044ddc0()) : 0;
    weapon=entry->FUN_0044ddc0()->FUN_00401170()==0x29 ? static_cast<TESObjectWEAP*>(entry->FUN_0044ddc0()) : 0;
    if(!form || (biped && !biped->FUN_00480d90()) || form->CannotSell() || FUN_00481f10(form) || !name || !name->GetModelLength() || (armor && !armor->FUN_0047bcf0()) || (weapon && !weapon->FUN_004c94d0()) || form->FUN_00401170()==0x2e)
        unavailable=true;
            }
          }
        }
      }
    }
    return unavailable;
}
