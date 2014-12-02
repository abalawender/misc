/*
IPC SHM example, changing wallpaper every minute 
	by Adam Balawender, Nov 26 2014
*/
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <dirent.h>
#include <string.h>
#include <stdlib.h>

int main() {
    struct stat fst;
    struct dirent *ent;
    DIR *dir;
    int fd = -1;
    void *mem = NULL;
    int out = open("/tmp/bg", O_RDWR|O_CREAT|O_TRUNC, S_IRWXU);
    const char* path = "/home/phaezah7/.config/awesome/";
    char *filename = malloc( 128 );
    
    if ( !filename || !( dir = opendir( path ) ) )
        return 1;

    while ( ( ent = readdir(dir) ) != NULL ) {
        (void) strcpy(filename, path);
        (void) strcat(filename, ent->d_name);

        if( !strstr(filename, ".jpg") && !strstr(filename, ".png") ) continue;
        printf("setting %s\n", filename);

        if( 0 > (fd = open(filename, O_RDONLY) ) ) continue;

        (void) fstat(fd, &fst);
        (void) ftruncate(out, fst.st_size);
        mem = mmap(0, fst.st_size, PROT_READ|PROT_WRITE, MAP_SHARED, out, 0);
        (void) read(fd, mem, fst.st_size);
        (void) close(fd);
        (void) msync(mem, fst.st_size, 0);
        (void) munmap(mem, fst.st_size);
        if( !fork() ) execlp("feh", "feh", "--bg-fill", "/tmp/bg", 0);
        (void) sleep(60);
    }

    (void) close(out);
    (void) closedir(dir);
    (void) free(filename);
    (void) wait();

    return 0;
}
