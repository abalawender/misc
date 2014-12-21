/*
 Converting char[32] with hex values to long long[2] for easy comparison - example
 Compilation:   gcc conv.c -o conv -lcrypto
 Usage:         ./conv hello 5d41402abc4b2a76b9719d911017c592
 Returns:       0 if word matches the hash, 1 otherwise
	by Adam Balawender, Dec 21 2014
*/
#include <openssl/md5.h>
void decode(char *hash, long long out[2]) {
    int i = 0;
    for( i = 0; i ^ 32; ++i )
        out[i>>4] |= (long long)(hash[i] > '9' ? hash[i]-'W' : hash[i]-'0') << ((i^1)<<2 & 0x3f);
}

int _strlen( const char * str) {
    int i = 0;
    if(str) while( str[i] ) ++i;
    return i;
}

int main(int argc, char **argv) {
    if(argc < 2 || 32 != _strlen(argv[2]) ) return 2;
    long long o1[2] = {0};
    char *hash = argv[2];
    decode(hash, o1);
    char md[16];

    long long o2[2] = {0};
    MD5(argv[1], _strlen(argv[1]), (char*)o2);

    return (o1[0] != o2[0] || o1[1] != o2[1]);
}
