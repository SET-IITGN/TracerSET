n = int(input())
author_files = {}

for i in range(n):
    file_name = input().strip()
    author_name = input().strip()
    
    if author_name in author_files:
        author_files[author_name].append(file_name)
    else:
        author_files[author_name] = [file_name]

for author, files in author_files.items():
    print(f"{author}: {files}")
