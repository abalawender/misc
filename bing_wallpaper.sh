sh -c "wget -qO /tmp/bg `wget -qO - bing.com/HPImageArchive.aspx?format=xml\\&n=1\\&idx=0 |sed -e 's/.*<urlBase>\\(.*\\)<\\/url.*/bing.com\\1_1920x1080.jpg/'` && feh /tmp/bg --bg-scale"
