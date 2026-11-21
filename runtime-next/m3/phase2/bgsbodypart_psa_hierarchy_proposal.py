"""Stage a private, uncompiled TESModel/BFC hierarchy hypothesis."""
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M/'out/phase2-bgsbodypart-psa-native-proposal';O=M/'out/phase2-bgsbodypart-psa-hierarchy-proposal'

def main():
    data=(P/'bgsbodypart_decls.h').read_bytes(); src=(P/'bgsbodypart.cpp').read_bytes()
    manifest=json.loads((P/'manifest.json').read_text())
    if hashlib.sha256(data).hexdigest()!=manifest['output_sha256']['header'] or hashlib.sha256(src).hexdigest()!=manifest['output_sha256']['source']:raise ValueError('input changed')
    text=data.decode('ascii').replace('\r\n','\n');start=text.index('class TESModel\n{');end=text.index('\nclass ModelLoader',start)
    tstart=text.index('template <class T> class BSStringT');tend=text.index('\nclass TESModelPSA',tstart)
    template=text[tstart:tend]
    replacement=template+'''
class BaseFormComponent
{
  public:
    virtual void Init();
    virtual void Free();
    virtual void CopyFromBase(BaseFormComponent*);
    virtual bool CompareWithBase(BaseFormComponent*);
};
class FileEntryList
{
  public:
    unsigned char count, padding[3];
    void** entries;
};
class TESModel : public BaseFormComponent
{
  public:
    BSStringT<char> m_kModelFilePath;
    FileEntryList m_pTextureSwapData;
    unsigned char cFlags, layoutPadding15[3];
    virtual void Init();
    virtual void Free();
    virtual void CopyFromBase(BaseFormComponent*);
    virtual bool CompareWithBase(BaseFormComponent*);
    virtual ~TESModel();
    virtual const char* vfn_14();
    virtual void vfn_18(const char*);
    static void LoadModelData(TESModel*, TESFile*);
    static void LoadTextureSwapData(TESModel*, TESFile*);
    TESModel();
    unsigned int GetModelLength() const;
};
typedef char psa_model_size_check[sizeof(TESModel)==24 ? 1 : -1];
'''
    # Remove old template first so replacement defines it exactly once.
    text=text[:tstart]+text[tend:]
    start=text.index('class TESModel\n{');end=text.index('\nclass ModelLoader',start)
    text=text[:start]+replacement+text[end:]
    text=text.replace('    ~TESModelPSA();','    virtual ~TESModelPSA();',1)
    O.mkdir(exist_ok=False);(O/'bgsbodypart.cpp').write_bytes(src);(O/'bgsbodypart_decls.h').write_text(text,encoding='ascii',newline='')
    out={'status':'private uncompiled hypothesis; not canonical','input_header_sha256':hashlib.sha256(data).hexdigest(),
      'output_header_sha256':hashlib.sha256((O/'bgsbodypart_decls.h').read_bytes()).hexdigest(),
      'limits':['local BaseFormComponent mirrors declarations to avoid layout_support BSStringT collision; reconcile before merge',
                'getter and setter names/signatures are hypotheses','eighth reference pointer ownership unresolved',
                'PSA destructor declared but not defined; native deleting-destructor body must be explicitly tested',
                'private layout assertion is not compiler evidence']}
    (O/'manifest.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out))
if __name__=='__main__':main()
