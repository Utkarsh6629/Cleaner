import os
import filecmp
import shutil
from pathlib import Path

folder1 = Path(r"E:\laptop old\backup\utkarsh\desktop\family\daddy\daddy\pixel\untitled")
folder2 = Path(r"E:\laptop old\backup\utkarsh\desktop\family\daddy\daddy\pixel\Photos from 2017")

def compare_and_remove_duplicates(folder1_path: Path, folder2_path: Path, dry_run: bool = True) -> tuple[list, list]:
   
    if not folder1_path.exists() or not folder2_path.exists():
        raise ValueError("One or both folders do not exist")
    
    removed_files = []
    errors = []
    
    files1 = list(folder1_path.rglob("*"))
    files2 = list(folder2_path.rglob("*"))
    
    files1 = [f for f in files1 if f.is_file()]
    files2 = [f for f in files2 if f.is_file()]
    
    for file1 in files1:
        rel_path = file1.relative_to(folder1_path)
        
        file2 = folder2_path / rel_path
        
        if file2.exists():
            try:
                if filecmp.cmp(file1, file2, shallow=False):
                    if dry_run:
                        print(f"Would remove: {file1}")
                    else:
                        file1.unlink()
                        print(f"Removed: {file1}")
                    removed_files.append(str(file1))
            except Exception as e:
                errors.append(f"Error processing {file1}: {str(e)}")
    
    return removed_files, errors

if __name__ == "__main__":
    print("Performing dry run first...")
    removed, errors = compare_and_remove_duplicates(folder1, folder2, dry_run=True)
    
    if errors:
        print("\nErrors encountered:")
        for error in errors:
            print(f"- {error}")
    
    if removed:
        print(f"\nFound {len(removed)} duplicate files.")
        proceed = input("Do you want to proceed with removal? (yes/no): ")
        
        if proceed.lower() == "yes":
            removed, errors = compare_and_remove_duplicates(folder1, folder2, dry_run=False)
            print(f"\nRemoved {len(removed)} files.")
    else:
        print("\nNo duplicate files found.")