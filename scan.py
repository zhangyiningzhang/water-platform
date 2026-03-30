import os
import sys

# 不需要显示的文件夹（太大或不重要）
SKIP_DIRS = {
    '__pycache__', 'venv', 'env', '.venv', '.git',
    'node_modules', '.idea', '.vscode', 'dist', 'build',
    'migrations', '.mypy_cache', '.pytest_cache'
}

# 不需要显示的文件扩展名
SKIP_EXTS = {
    '.pyc', '.pyo', '.pyd', '.so', '.dll',
    '.mat',  # Matlab 数据文件（可能很大）
    '.db', '.sqlite3',
    '.jpg', '.jpeg', '.png', '.gif', '.bmp',
    '.zip', '.rar', '.tar', '.gz',
    '.pdf', '.docx', '.xlsx',
}

def scan(root, prefix='', depth=0, max_depth=5):
    if depth > max_depth:
        return
    try:
        entries = sorted(os.listdir(root))
    except PermissionError:
        return

    dirs = [e for e in entries if os.path.isdir(os.path.join(root, e))]
    files = [e for e in entries if os.path.isfile(os.path.join(root, e))]

    for i, d in enumerate(dirs):
        if d in SKIP_DIRS:
            connector = '└── ' if (i == len(dirs)-1 and not files) else '├── '
            print(f"{prefix}{connector}[{d}/]  ← 已跳过")
            continue
        connector = '└── ' if (i == len(dirs)-1 and not files) else '├── '
        print(f"{prefix}{connector}{d}/")
        extension = '    ' if connector.startswith('└') else '│   '
        scan(os.path.join(root, d), prefix + extension, depth + 1, max_depth)

    for i, f in enumerate(files):
        ext = os.path.splitext(f)[1].lower()
        if ext in SKIP_EXTS:
            continue
        size = os.path.getsize(os.path.join(root, f))
        size_str = f"{size/1024:.1f}KB" if size > 1024 else f"{size}B"
        connector = '└── ' if i == len(files)-1 else '├── '
        print(f"{prefix}{connector}{f}  ({size_str})")

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    target = os.path.abspath(target)
    print(f"项目根目录: {target}")
    print("=" * 60)
    scan(target)
    print("=" * 60)
    print("扫描完成！请把以上内容复制给 Claude。")