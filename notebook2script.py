
import json,fire,re
from pathlib import Path
import io


def isExport(cell):
    "Checks wheather a cell contains #export or not"
    if cell['cell_type']!='code':
        return False
    src = cell['source']
    if len(src)==0 or len(src[0])<7:
        return False
    return re.match(r'^\s*#\s*export\s*$',src[0],re.IGNORECASE) is not None


def notebook2Script(fname):
    
    fname = Path(fname)
    fname_out = f'{fname.stem.split(".")[0]}.py'
    main_dic = json.load(open(fname,'r',encoding='utf-8'))
    code_cells = [c for c in main_dic['cells'] if isExport(c)]
    module = f'''# file to edit: dev_nb/{fname.name} 
'''
    
    for cell in code_cells:
        module+="".join(cell['source'][1:])+'\n\n'
    # remove trailing spaces
    module = re.sub(r' +$', '', module, flags=re.MULTILINE)
    if not (fname.parent/'expoMode').exists():
        (fname.parent/'expoMode').mkdir()
    output_path = fname.parent/'expoMode'/fname_out
    with io.open(output_path, "w", encoding="utf-8") as f:
        f.write(module[:-2])
    print(f"Converted {fname} to {output_path}")
        
        
if __name__=='__main__':
    fire.Fire(notebook2Script)