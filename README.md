## Installaion
    ### For memcache docker container
    1. Install memcached server on Debian/Ubuntu
        sudo apt-get install memcached
    2. Built an image
        docker build -t local/memcached:0.1 .
    3. Run the docker container
        docker run -itd --name memcached -p 11311:11211 -e MEMCACHED_MEMUSAGE=32 local/memcached:0.1