# Spider JIT

[![Join the chat at https://gitter.im/ssarangi/spiderjit](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/ssarangi/spiderjit?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Spider JIT is a project inspired by llvmlite & SpiderMonkey. While working with llvmlite I wanted to write a small jitter which could jit python programs. Currently, the tasks
I am doing are these

* Develop the intermediate IR.
* Develop a frontend which can translate to this IR
* Write optimizations
* Register allocation
* Code Generation to x86
* A jitter which is interfaced through C since python mmap support doesn't allow PROT_EXEC to marking memory pages as executable.

Here is a sample of the code Spider JIT can generate currently.

```python
Module: MyModule
Target Datalayout: []
Target Arch: 
define i32 test_fn(float %myarg, float %myarg1) {
entry:
	%0 = call i32 @foo(i32 5, i32 3)
	%call = call i32 @foo(i32 7, i32 2)
	%call1 = call i32 @foo(i32 9, i32 1)
	%1 = fadd(i32 4, i32 7)
	%mymul = mul(i32 3, i32 9)
	br exit
exit:
	return void
}

define i32 foo(i32 %a, i32 %b) {
}
```