import os, re, shutil, nbformat, subprocess

# === CONFIG ===
USERNAME = "abigit240"   # <-- replace this before run
REPO = "deep-learning-tutorials"    # your repo name on GitHub
base = os.getcwd()

# folder mapping (source filename keywords → folder names)
folder_map = {
    "tutorial01": "Tutorial_01_Perceptron",
    "tutorial02": "Tutorial_02_MLP",
    "tutorial03": "Tutorial_03_ANN",
    "tutorial04": "Tutorial_04_Data_Augmentation",
    "tutorial05": "Tutorial_05_CNN",
    "tutorial06": "Tutorial_06_Transfer_Learning_Pretrained_Models",
    "tutorial07": "Tutorial_07_Transfer_Learning",
    "tutorial08": "Tutorial_08_Object_Detection_CustomModel"
}

# 1️⃣  Clean notebooks: remove outputs, execution counts, name tags
def clean_notebook(path):
    nb = nbformat.read(path, as_version=4)
    changed = False
    for cell in nb.cells:
        if cell.cell_type == 'code':
            if cell.get('outputs'):
                cell['outputs'] = []
                changed = True
            cell['execution_count'] = None
        if cell.cell_type == 'markdown':
            txt = re.sub(r'(?i)name\s*[:\-]\s*[\w ]+', '', cell['source'])
            if txt != cell['source']:
                cell['source'] = txt
                changed = True
    if changed:
        nbformat.write(nb, path)
        print(f"Cleaned: {os.path.basename(path)}")

# 2️⃣  Move notebooks into proper tutorial folders
def move_notebooks():
    for fname in os.listdir(base):
        if fname.endswith(".ipynb") and fname.lower().startswith("tutorial"):
            lower = fname.lower()
            for key, folder in folder_map.items():
                if key in lower:
                    dest_folder = os.path.join(base, folder)
                    os.makedirs(dest_folder, exist_ok=True)
                    src = os.path.join(base, fname)
                    dst = os.path.join(dest_folder, fname)
                    shutil.move(src, dst)
                    print(f"Moved {fname} → {folder}")
                    break

# 3️⃣  Generate nbviewer links in README (append / update)
def update_readme():
    readme = os.path.join(base, "README.md")
    lines = ["\n\n## 🌐 View Online (nbviewer links)\n",
             "| Tutorial | Notebook | View Online |\n",
             "|-----------|-----------|-------------|\n"]
    for folder in sorted(folder_map.values()):
        if not os.path.isdir(folder): 
            continue
        nbs = [f for f in os.listdir(folder) if f.endswith(".ipynb")]
        for nb in nbs:
            path = f"{folder}/{nb}"
            link = f"https://nbviewer.org/github/{USERNAME}/{REPO}/blob/main/{path}"
            lines.append(f"| {folder} | [{nb}]({path}) | [View Online]({link}) |\n")
    with open(readme, "a", encoding="utf8") as f:
        f.writelines(lines)
    print("Updated README.md with nbviewer links ✅")

# === MAIN ===
for f in os.listdir(base):
    if f.endswith(".ipynb"):
        clean_notebook(f)

move_notebooks()
update_readme()

print("\nAll notebooks cleaned and organized. Now commit & push to GitHub:\n")
print("git init")
print("git add .")
print('git commit -m "Clean notebooks and add nbviewer links"')
print(f"git remote add origin https://github.com/{USERNAME}/{REPO}.git")
print("git branch -M main")
print("git push -u origin main")
