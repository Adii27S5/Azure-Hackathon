import os
import zipfile

def pack():
    zip_path = os.path.join("deploy", "app-deploy.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)
        
    items_to_add = [
        "service.js",
        "package.json",
        "package-lock.json",
        ".deployment",
        "src",
        "public"
    ]
    
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in items_to_add:
            if os.path.isfile(item):
                arcname = item.replace("\\", "/")
                zf.write(item, arcname)
                print(f"Added file: {arcname}")
            elif os.path.isdir(item):
                for root, dirs, files in os.walk(item):
                    for file in files:
                        full_path = os.path.join(root, file)
                        arcname = full_path.replace("\\", "/")
                        zf.write(full_path, arcname)
                        print(f"Added file: {arcname}")
                        
    print(f"Successfully created POSIX-compliant {zip_path}")

if __name__ == "__main__":
    pack()
