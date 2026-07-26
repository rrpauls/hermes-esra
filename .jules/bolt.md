## 2026-07-18 - Optimize skill validator dependency sorting
**Learning:** Found an O(V³) worst-case bottleneck in `tools/skill_validator.py` due to nested loops and inefficient queue sorting on graph algorithms. Using `heapq` and adjacency lists optimizes Kahn's topological sort to O(V log V + E) for alphabetical node processing.
**Action:** When implementing topological sort or graph processing with alphabetical tie breaking requirements, avoid standard list sorts inside while loops and use a min-heap structure (`heapq`) along with proper dependency mappings.
## 2026-07-19 - Duplicate File I/O Optimization in Skill Validator
**Learning:** In codebases where files are repeatedly parsed (like Markdown frontmatter and full-text searches), redundant `file.read_text()` operations can significantly slow down execution when processing many files.
**Action:** When a file parsing function successfully reads the raw content of a file, refactor it to return that raw content alongside its parsed structures, so downstream steps can reuse the text rather than reading from disk again.
## 2026-07-25 - Optimize redundant file system stat() calls during directory iteration
**Learning:** In operations iterating over many files and checking their attributes (like `st_mtime`), using `Path.glob()` combined with `Path.stat()` causes redundant `stat()` syscalls. `os.scandir()` retrieves file attributes simultaneously with directory entries, significantly reducing file system overhead for large directories.
**Action:** When filtering or processing directory contents based on file attributes, replace `Path.glob()` and `Path.stat()` with `os.scandir()` to improve performance.
## 2026-07-26 - Optimize JSON Loading Memory Usage
**Learning:** `json.loads(file.read_text())` buffers the entire file content into a memory string before parsing, causing a spike in peak memory usage. Using `with open(filepath, 'r') as f: json.load(f)` streams the file content directly to the JSON parser, significantly reducing memory consumption and slightly improving performance for large files.
**Action:** When reading JSON files from disk, prefer the `with open(...) as f: json.load(f)` pattern over loading the file content as a string first. Ensure performance optimizations are accompanied by explanatory comments like `# ⚡ BOLT OPTIMIZATION: ...`. Always clean up benchmarking scripts.
