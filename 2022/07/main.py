class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = {}
        self.files = {}
        self.deep_size = None

    def get_deep_size(self):
        if self.deep_size is None:
            self.deep_size = sum(self.files.values()) + sum(child.get_deep_size() for child in self.children.values())
        return self.deep_size

    def get_all_dirs(self):
        dirs = [self]
        for child in self.children.values():
            dirs.extend(child.get_all_dirs())
        return dirs

    def __repr__(self):
        return f"Directory({self.name}, {self.shallow_size}, {self.parent}, {self.children})"

    def __str__(self):
        return f"{self.name} ({self.shallow_size})"


def get_root(data):
    lines = data.splitlines()
    parent_dir = None
    current_dir = None
    for line in lines:
        if line[:4] == '$ cd':
            cwd  = line[5:]
            if cwd != '..':
                parent_dir = current_dir
                current_dir = Directory(name=cwd, parent=parent_dir)
                if parent_dir:
                    parent_dir.children[cwd] = current_dir
            else:
                current_dir = parent_dir
                parent_dir = parent_dir.parent
        elif line[:4] == '$ ls':
            pass
        elif line[:3] == 'dir':
            pass
        else:
            size, name = line.split()
            current_dir.files[name] = int(size)

    while current_dir.name != '/':
        current_dir = current_dir.parent
    return current_dir


root = get_root(open('input.txt').read())

dirs = root.get_all_dirs()

print('part1', sum(d.get_deep_size() for d in dirs if d.get_deep_size() < 100000))

print('Need to free:', 30000000 - 70000000 + root.get_deep_size())
print('part2', min(d.get_deep_size() for d in dirs if d.get_deep_size() >= (30000000 - 70000000 + root.get_deep_size())))

