sh -c "wget -qO /tmp/bg.jpg `wget -qO - bing.com/HPImageArchive.aspx?format=xml\\&n=1\\&idx=$1 |sed -e 's/.*<urlBase>\\(.*\\)<\\/url.*/bing.com\\1_1920x1080.jpg/'` && feh /tmp/bg.jpg --bg-scale"
