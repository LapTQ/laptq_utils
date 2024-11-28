
PATH__FILE__PROGRESS__DIR=/mnt/hdd10tb/Users/laptq/laptq-prj-46/outputs/progress
ADDRESS__REMOTE=rack:/home/laptq/progress/laptq-prj-46

[[ -d "$PATH__FILE__PROGRESS__DIR" ]] && rm -r "$PATH__FILE__PROGRESS__DIR"
mkdir -p "$PATH__FILE__PROGRESS__DIR"

while true; do
    tree /mnt/hdd10tb/Users/laptq/laptq-prj-46/runs/20241122--phase-2--annotation-ver2/ > "${PATH__FILE__PROGRESS__DIR}/tree.txt"

    path__dir=/mnt/hdd10tb/Users/laptq/laptq-prj-46/runs/20241122--phase-2--annotation-ver2/yolo11m--960--full
    if [[ -d $path__dir ]]; then
        rsync $path__dir "${PATH__FILE__PROGRESS__DIR}/"
        find "$PATH__FILE__PROGRESS__DIR" -type d -name *"weights"* -exec rm -rf {} \;
    fi

    path__dir=/mnt/hdd10tb/Users/laptq/laptq-prj-46/runs/20241122--phase-2--annotation-ver2/yolo11m--640--crop
    if [[ -d $path__dir ]]; then
        rsync $path__dir "${PATH__FILE__PROGRESS__DIR}/"
        find "$PATH__FILE__PROGRESS__DIR" -type d -name *"weights"* -exec rm -rf {} \;
    fi

    path__dir=/mnt/hdd10tb/Users/laptq/laptq-prj-46/runs/20241122--phase-2--annotation-ver2/yolo11s--960--crop
    if [[ -d $path__dir ]]; then
        rsync $path__dir "${PATH__FILE__PROGRESS__DIR}/"
        find "$PATH__FILE__PROGRESS__DIR" -type d -name *"weights"* -exec rm -rf {} \;
    fi

    rsync -avz "${PATH__FILE__PROGRESS__DIR}/" "${ADDRESS__REMOTE}/"
    sleep 60
done
