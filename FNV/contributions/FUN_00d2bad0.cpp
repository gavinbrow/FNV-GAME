struct Reader {virtual void v0();virtual void v1();virtual void v2();virtual unsigned char* v3(unsigned char*);};
struct hkBool { unsigned char m_bool; hkBool(bool v):m_bool(v){} };
struct Stream {int a,b;Reader* reader;int c,pos,end;hkBool FUN_00d2bad0();};
hkBool Stream::FUN_00d2bad0(){unsigned char byte; return hkBool(pos != end || *reader->v3(&byte) != 0);}