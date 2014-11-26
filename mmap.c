/*
IPC SHM example, ver alpha 
	by Adam Balawender, Nov 26 2014
*/
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>

int main() {
    if( !fork() ) execlp("feh", "feh", "-R", "1", "out", 0); 
    int out = open("out", O_RDWR|O_CREAT|O_TRUNC, S_IRWXU);
    struct stat fst;
    
    int fd = open("pic1", O_RDONLY);
    (void) fstat(fd, &fst);
    (void) ftruncate(out, fst.st_size);
    void* mem = mmap(0, fst.st_size, PROT_READ|PROT_WRITE, MAP_SHARED, out, 0);
    (void) read(fd, mem, fst.st_size);
    (void) close(fd);
    (void) msync(mem, fst.st_size, 0);

    sleep(10);

    fd = open("pic3", O_RDONLY);
    (void) fstat(fd, &fst);
    (void) ftruncate(out, fst.st_size);
    mem = mmap(0, fst.st_size, PROT_READ|PROT_WRITE, MAP_SHARED, out, 0);
    (void) read(fd, mem, fst.st_size);
    (void) close(fd);
    (void) msync(mem, fst.st_size, 0);

    (void) munmap(mem, fst.st_size);

    (void) close(out);

    wait();
    return 0;
}
