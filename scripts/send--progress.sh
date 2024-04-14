
PATH__FILE__PROGRESS__DIR=/mnt/hdd10tb/Users/laptq/laptq-prj-46/outputs/progress
ADDRESS__REMOTE=rack:/home/laptq/progress/laptq-prj-46

[[ -d "$PATH__FILE__PROGRESS__DIR" ]] && rm -r "$PATH__FILE__PROGRESS__DIR"
mkdir -p "$PATH__FILE__PROGRESS__DIR"

while true; do
    tree /mnt/hdd10tb/Users/laptq/laptq-prj-46/runs/20241122--phase-2--annotation-ver2/ > "${PATH__FILE__PROGRESS__DIR}/tree.txt"

    LIST__PATH__DIR=(
        "/mnt/hdd10tb/Users/laptq/laptq-prj-46/runs/20241122--phase-2--annotation-ver2/yolo11s--1280--crop-20"
        "/mnt/hdd10tb/Users/laptq/laptq-prj-46/runs/20241122--phase-2--annotation-ver2/yolo11m-p2--960--crop-20"
    )
    for path__dir in ${LIST__PATH__DIR[@]}; do
        if [[ -d $path__dir ]]; then
            rsync -av $path__dir "${PATH__FILE__PROGRESS__DIR}/"
            find "$PATH__FILE__PROGRESS__DIR" -type d -name *"weights"* -exec rm -rf {} \;
            find "$PATH__FILE__PROGRESS__DIR" -type d -name *"predict"* -exec rm -rf {} \;
            find "$PATH__FILE__PROGRESS__DIR" -type d -name *"val"* -exec rm -rf {} \;
        fi
    done

    rsync -avz "${PATH__FILE__PROGRESS__DIR}/" "${ADDRESS__REMOTE}/"
    sleep 60
done
