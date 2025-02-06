#!/bin/bash

# apt update
# apt install default-jdk
# apt install graphviz

cd /app/laptq-prj-21

# wget -c https://github.com/plantuml/plantuml/releases/download/v1.2025.0/plantuml-1.2025.0.jar

uml_dir=./docs/uml
assets_dir=./assets/uml

[ -d $assets_dir ] || mkdir -p $assets_dir

for diagram_dir in $( ls $uml_dir ); do
    # [ -d $assets_dir/$diagram_dir ] && rm -r  $assets_dir/$diagram_dir
    for pu_file in $( ls $uml_dir/$diagram_dir ); do
        java -jar plantuml-1.2025.0.jar $uml_dir/$diagram_dir/$pu_file -o ../../../$assets_dir/$diagram_dir
    done
done

chmod -R 777 $assets_dir