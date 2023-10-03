import sys

# Config
mode = sys.argv[1]
path = "test.conf"

start_keyword = "timelapse-block-start"
end_keyword = "timelapse-block-end"
comment_prefix = "# "

# Check mode
isCommenting = False
if mode == "ap":
    isCommenting = False
elif mode == "normal":
    isCommenting = True
else:
    print("Invalid mode " + mode + ": Please choose 'ap' or 'normal'")
    sys.exit(1)

# Read All Lines
with open(path, 'r') as file:
    lines = file.readlines()

# Open For Writing
with open(path, 'w') as file:
    found_start = False

    for line in lines:
        if start_keyword in line:
            found_start = True
            file.write(line)
            continue
        elif end_keyword in line:
            found_start = False
            file.write(line)
            continue

        if found_start:
            if isCommenting and not line.startswith(comment_prefix):
                file.write(comment_prefix + line)  # Add prefix
                continue
            elif not isCommenting and line.startswith(comment_prefix):
                file.write(line[len(comment_prefix):])  # Remove prefix
                continue
        
        file.write(line)