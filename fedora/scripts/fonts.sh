#!/usr/bin/env bash

fonts_dir="${HOME}/.local/share/fonts"
if [ ! -d "${fonts_dir}" ]; then
    echo "mkdir -p $fonts_dir"
    mkdir -p "${fonts_dir}"
else
    echo "Found fonts dir $fonts_dir"
fi

#fira
fcversion=6.2
zip=Fira_Code_v${fcversion}.zip
curl --fail --location --show-error https://github.com/tonsky/FiraCode/releases/download/${fcversion}/${zip} --output ${zip}
unzip -o -q -d ${fonts_dir} ${zip}
rm ${zip}

#iosevka
curl -s 'https://api.github.com/repos/be5invis/Iosevka/releases/latest' | jq -r ".assets[] | .browser_download_url" | grep PkgTTC-Iosevka | xargs -n 1 curl -L -O --fail --silent --show-error
for i in PkgTTC-Iosevka*; do 
    unzip -o -q -d ${fonts_dir} $i;
done

echo "fc-cache -rvf"
fc-cache -rvf
