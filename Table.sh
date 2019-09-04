
#!/bin/bash


{
  eval "dirs=($(ls -v --quoting-style=shell-always))"
  headers_done=false
  for dir in "${dirs[@]}"; do
    (
      cd -- "$dir" || exit
      eval "files=($(
        ls -vd --quoting-style=shell-always LABEL_*.txt))"
      if ! "$headers_done"; then
        printf DIR
        printf ',%s' "${files[@]}"
        printf '\n'
        headers_done=true
      fi
      printf %s, "$dir"
      tail -q -n 1 -- "${files[@]}" | paste -sd , -
    )
  done
} > data.csv
