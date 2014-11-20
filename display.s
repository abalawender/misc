/*  2   - fork
    3   - read
    4   - write
    5   - open
    6   - close
    11  - execve
    41  - dup
    42  - pipe
    162 - nanosleep
    27  - alarm */


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
    //pop %ebx
    int $0x80

    movl $6, %eax
    pop %ebx
    int $0x80

/*    push $65
    movl $3, %eax
    movl $0, %ebx
    leal (%esp), %ecx
    movl $4, %edx
    int $0x80

    movl $4, %eax
    movl $1, %ebx
    leal (%esp), %ecx
    movl $4, %edx
    int $0x80
*/
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

    //addl $0x50, %esp
    push $0
    push $0
    push $0
    push $0
    push $0
    push $0
    push $0
    push $0
    push $0
    push $0
    push $0
    push $0
    push $0
    push $0
    push $0
    push $0
    push $0
    push $0
    push $0
    push $0
    movl $3, %eax
    movl $0, %ebx
    leal (%esp), %ecx
    movl $0x50, %edx
    int $0x80
    
    movl %eax, %edx

    leal (%esp), %ebx
    subl $0x4f, %ebx
    addl %edx, %ebx
    movl $0, (%ebx)

    movl $4, %eax
    movl $1, %ebx
    leal (%esp), %ecx
    //movl $edx, %edx - write as much as was read
    movl $0x50, %edx
    int $0x80

    movl $5, %eax
    leal (%esp), %ebx
    movl $0, %ecx
    int $0x80
    subl $0x50, %esp
    push %eax

_copy:
    //movl %eax, %ebx /* fd */
    movl $3, %eax
    //movl %esp, %ebx
    movl $3, %ebx
    addl $0x50, %esp
    leal (%esp), %ecx
    movl $0x50, %edx
    int $0x80

    movl %eax, %edx /*save */
    movl $4, %eax
    movl $4, %ebx
    //ecx ok
    //movl %edx
    int $0x80
    subl $0x50, %esp
    or %edx, %edx
    jne _copy


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
fmt:
.string "%d, %d\n"
parent:
.string "PA\n"
child:
.string "CH\n"
display:
.string "/usr/bin/display"
env:
.string "DISPLAY=:0.0"

