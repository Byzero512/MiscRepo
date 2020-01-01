disable pie
> 1. pip install pefile

```python
def NOPIE(fpath="",new_fpath=""):
    import pefile
    pe_fp=pefile.PE(fpath)
    pe_fp.OPTIONAL_HEADER.DllCharacteristics &= \
        ~pefile.DLL_CHARACTERISTICS["IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE"]
    if not new_fpath:
        new_fpath=fpath
    pe_fp.OPTIONAL_HEADER.CheckSum = pe_fp.generate_checksum()
    # pe_fp.flush()
    # print(new_fpath)
    pe_fp.write(new_fpath)
def PIE(fpath="",new_fpath=""):
    import pefile
    pe_fp=pefile.PE(fpath)
    print(pe_fp.OPTIONAL_HEADER.DllCharacteristics)
    print(pefile.DLL_CHARACTERISTICS["IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE"])
    pe_fp.OPTIONAL_HEADER.DllCharacteristics |= \
        pefile.DLL_CHARACTERISTICS["IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE"]
    if not new_fpath:
        new_fpath=fpath
    pe_fp.OPTIONAL_HEADER.CheckSum = pe_fp.generate_checksum()
    pe_fp.write(new_fpath)
```
