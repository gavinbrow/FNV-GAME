extern "C" void FUN_0044f570();
class __declspec(novtable) Setting {
public:
    virtual void touch();
    void FUN_00404950();
    ~Setting(){ FUN_00404950(); }
};
class Collection {public: virtual void fn0(); virtual void fn1(); virtual void remove(Setting *);};
extern "C" Collection * DAT_011f96a0;
class Setting_01017720_011f96a0 : public Setting {
public:
    Setting_01017720_011f96a0(){}
    __forceinline ~Setting_01017720_011f96a0(){
      FUN_0044f570();
      {Collection* p=DAT_011f96a0; p->remove(this);}
      char unused[12];
    }
};
Setting_01017720_011f96a0 g_011f345c;