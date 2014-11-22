/*  2   - fork
    3   - read
    4   - write
    5   - open
    6   - close
    11  - execve
    41  - dup
    42  - pipe
    162 - nanosleep */

/*
IPC example, sends image to /usr/bin/display via pipe
	by Adam Balawender, Nov 20 2014

    compile with: gcc -gstabs display.s -o display -g -m32 */

.globl main
main:
    movl $4, %eax   
    movl $1, %ebx   
    movl $msg, %ecx 
    movl $13, %edx  
    int $0x80

    push $0
    push $0
    movl $42, %eax
    leal (%esp), %ebx
    int $0x80

    movl $2, %eax
    int $0x80
    or %eax, %eax
    jne _par

// under 18 area!

    movl $6, %eax
    movl $0, %ebx
    int $0x80

    movl $41, %eax
    pop %ebx
    int $0x80 

    movl $6, %eax
    int $0x80

    movl $6, %eax
    pop %ebx
    int $0x80

    pushl %ebp
    movl %esp, %ebp
    subl $0x8, %esp
    movl $display, %edi
    movl %edi, -0x8(%ebp)
    movl $0, -0x4(%ebp)

    movl $11, %eax   
    movl $display, %ebx
    leal -8(%ebp), %ecx
    
    pushl %ebp
    movl %esp, %ebp
    subl $0x8, %esp
    movl $env, %edi
    movl %edi, -0x8(%ebp)
    movl $0, -0x4(%ebp)

    leal -8(%ebp), %edx
    int $0x80

    // error happened, f*ck
    jmp _end

_par:
    movl $6, %eax
    pop %ebx
    int $0x80

    subl $0x50, %esp            /* allocate 80B for filename */

    movl $3, %eax
    movl $0, %ebx
    leal (%esp), %ecx
    movl $0x50, %edx
    int $0x80

    movb $0, -1(%esp, %eax, 1)  /* change last character (\n) to null */

    movl $5, %eax               /* open */
    leal (%esp), %ebx
    movl $0, %ecx
    int $0x80

    addl $0x50, %esp            /* free 80B - filename */
    push %eax                   /* save file descriptor */
    cmp $0, %eax
    jb _end

_copy:
    movl $3, %eax
    movl (%esp), %ebx
    leal -0xFF(%esp), %ecx      /* use 256B on stack */
    movl $0xFF, %edx
    int $0x80

    movl %eax, %edx             /* store length */
    movl $4, %eax               /* write to pipe */
    movl 4(%esp), %ebx
    //ecx & edx are ok
    int $0x80
    cmp $0, %eax
    jg _copy

    movl $6, %eax
    movl $4, %ebx
    int $0x80
    
_end:
    push $0
    push $30
    movl $162, %eax
    leal (%esp), %ebx
    movl $0, %ecx
    int $0x80
    pop %ebx
    pop %ebx

    movl $4, %eax   
    movl $1, %ebx   
    movl $msg2, %ecx 
    movl $11, %edx  
    int $0x80

    movl $1, %eax
    movl $0, %ebx   
    int $0x80 
msg:
.string "Hello world!\n"
msg2:
.string "Bye world!\n"
display:
.string "/usr/bin/display"
env:
.string "DISPLAY=:0.0"

