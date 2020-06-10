THRESHOLD = 0.2
PERMUTATIONS = 68
CHUNK_SIZE = 6
COMMITS = 2

SKIP_DIRS = [
    "node_modules", "assets", "build", "classes", "gradle", "licenses", "icu", "dcn21", "fixtures", "docs", "test",
    "tests", "examples", "changelogs"
]

SKIP_FILES = [
    ".3dm", ".3ds", ".3g2", ".3gp", ".7z", ".a", ".aac", ".adp", ".ai", ".aif", ".aiff", ".alz", ".ape", ".apk",
    ".ar", ".arj", ".asf", ".au", ".avi", ".bak", ".baml", ".bh", ".bin", ".bk", ".bmp", ".btif", ".bz2", ".bzip2",
    ".cab", ".caf", ".cgm", ".class", ".cmx", ".cpio", ".cr2", ".cur", ".dat", ".dcm", ".deb", ".dex", ".djvu",
    ".dll", ".dmg", ".dng", ".doc", ".docm", ".docx", ".dot", ".dotm", ".dra", ".DS_Store", ".dsk", ".dts",
    ".dtshd", ".dvb", ".dwg", ".dxf", ".ecelp4800", ".ecelp7470", ".ecelp9600", ".egg", ".eol", ".eot", ".epub",
    ".exe", ".f4v", ".fbs", ".fh", ".fla", ".flac", ".fli", ".flv", ".fpx", ".fst", ".fvt", ".g3", ".gh", ".gif",
    ".graffle", ".gz", ".gzip", ".h261", ".h263", ".h264", ".icns", ".ico", ".ief", ".img", ".ipa", ".iso", ".jar",
    ".jpeg", ".jpg", ".jpgv", ".jpm", ".jxr", ".key", ".ktx", ".lha", ".lib", ".lvp", ".lz", ".lzh", ".lzma",
    ".lzo", ".m3u", ".m4a", ".m4v", ".mar", ".mdi", ".mht", ".mid", ".midi", ".mj2", ".mka", ".mkv", ".mmr", ".mng",
    ".mobi", ".mov", ".movie", ".mp3", ".mp4", ".mp4a", ".mpeg", ".mpg", ".mpga", ".mxu", ".nef", ".npx",
    ".numbers", ".nupkg", ".o", ".oga", ".ogg", ".ogv", ".otf", ".pages", ".pbm", ".pcx", ".pdb", ".pdf", ".pea",
    ".pgm", ".pic", ".png", ".pnm", ".pot", ".potm", ".potx", ".ppa", ".ppam", ".ppm", ".pps", ".ppsm", ".ppsx",
    ".ppt", ".pptm", ".pptx", ".psd", ".pya", ".pyc", ".pyo", ".pyv", ".qt", ".rar", ".ras", ".raw", ".resources",
    ".rgb", ".rip", ".rlc", ".rmf", ".rmvb", ".rtf", ".rz", ".s3m", ".s7z", ".scpt", ".sgi", ".shar", ".sil",
    ".sketch", ".slk", ".smv", ".snk", ".so", ".stl", ".suo", ".sub", ".swf", ".tar", ".tbz", ".tbz2", ".tga",
    ".tgz", ".thmx", ".tif", ".tiff", ".tlz", ".ttc", ".ttf", ".txz", ".udf", ".uvh", ".uvi", ".uvm", ".uvp",
    ".uvs", ".uvu", ".viv", ".vob", ".war", ".wav", ".wax", ".wbmp", ".wdp", ".weba", ".webm", ".webp", ".whl",
    ".wim", ".wm", ".wma", ".wmv", ".wmx", ".woff", ".woff2", ".wrm", ".wvx", ".xbm", ".xif", ".xla", ".xlam",
    ".xls", ".xlsb", ".xlsm", ".xlsx", ".xlt", ".xltm", ".xltx", ".xm", ".xmind", ".xpi", ".xpm", ".xwd", ".xz",
    ".z", ".zip", "zipx", ".txt", ".md", ".bat", ".jks", ".sh", ".prpt", ".ini", ".db", ".plist", ".ver", ".pb",
    ".data-00000-of-00001", ".index", ".golden", ".pbtxt.gz", ".mdb", ".meta", ".bytes", ".lite", ".h5",
    ".data-00000-of-00002", ".data-00001-of-00002", ".map", ".elf", ".skb", ".skp", ".dtbo", ".mat", ".fig", ".pfx",
    ".dll", ".Rascal", ".exr", ".blend", ".pfb", ".xcf", ".odg", ".out", ".sgml", ".mo", '.install'
]
