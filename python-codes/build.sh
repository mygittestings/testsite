#!/bin/bash 
set -e

ALLOWEDFILES=("ybysource" "ybystream" "ybygongyanquanchang") 

generate() # need 1 argument
{
    if [[ $# -eq 0 ]]; then
        printf "generate() expects 1 and only 1 input"
        exit 1
    elif [[ $# -eq 1 ]]; then
        target=$1
    else
        printf "generate() expects 1 and only 1 input"
        exit 1
    fi

    if [[ "$target" == "ybygongyanquanchang" ]]; then
        python3 addurlblock2line.py -i ${target}.txt
        cat sources/${target}.head hexo.txt sources/ybygongyanwiki.md > rendered/${target}-hexo.md
        cat sources/${target}.head jekyll.txt sources/ybygongyanwiki.md > rendered/${target}-jekyll.md
    else
        python3 addurlblock.py -i ${target}.txt
        cat sources/${target}.head hexo.txt > rendered/${target}-hexo.md
        cat sources/${target}.head jekyll.txt > rendered/${target}-jekyll.md
    fi

    rm jekyll.txt hexo.txt
}

deploylocal() # need 1 argument: this is not generating, just copy files
{
    if [[ $# -eq 0 ]]; then
        printf "deploylocal() expects 1 and only 1 input"
        exit 1
    elif [[ $# -eq 1 ]]; then
        target=$1
    else
        printf "deploylocal() expects 1 and only 1 input"
        exit 1
    fi
 
    workfile="../source/_posts/$target.md"

    cp "rendered/${target}-hexo.md" "$workfile" 
}

main(){	

    FILES=("${ALLOWEDFILES[@]}"); 

    for target in "${FILES[@]}"; do 
        cp ../articles/"${target}.txt" .
        generate "$target" > /dev/null
        deploylocal "$target"
    done
}

main "$@"
