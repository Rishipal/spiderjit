#include <Python.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>

// Allocates RW memory of given size and returns a pointer to it. On failure,
// prints out the error and returns NULL. mmap is used to allocate, so
// deallocation has to be done with munmap, and the memory is allocated
// on a page boundary so it's suitable for calling mprotect.
void* alloc_writable_memory(size_t size) {
  void* ptr = mmap(0, size,
                   PROT_READ | PROT_WRITE,
                   MAP_PRIVATE | MAP_ANON, -1, 0);
  if (ptr == (void*)-1) {
    perror("mmap");
    return NULL;
  }
  return ptr;
}

// Sets a RX permission on the given memory, which must be page-aligned. Returns
// 0 on success. On failure, prints out the error and returns -1.
int make_memory_executable(void* m, size_t size) {
  if (mprotect(m, size, PROT_READ | PROT_EXEC) == -1) {
    perror("mprotect");
    return -1;
  }
  return 0;
}

void emit_code_into_memory(unsigned char* m, unsigned char *code) {
  /*
  unsigned char code[] = {
    0x48, 0x89, 0xf8,                   // mov %rdi, %rax
    0x48, 0x83, 0xc0, 0x04,             // add $4, %rax
    0xc3                                // ret
  };
  */
  memcpy(m, code, sizeof(code));
}

const size_t SIZE = 1024;
typedef long (*JittedFunc)(long);

// Allocates RW memory, emits the code into it and sets it to RX before
// executing.
void emit_to_rw_run_from_rx(unsigned char *code) {
  void* m = alloc_writable_memory(SIZE);
  emit_code_into_memory(m, code);
  make_memory_executable(m, SIZE);

  JittedFunc func = m;
  int result = func(4);
  printf("result = %d\n", result);
}

static PyObject *JitterError;

static PyObject* jitter_jit(PyObject *self, PyObject *args, PyObject *keywrds) {
    const char* str;
    char * buf;
    Py_ssize_t count;
    PyObject * result;
    PyObject *sig;
    int i;

    static char *kwlist[] = {"code", "signature", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, keywrds, "|z#O", kwlist,
                                     &str, &count, &sig))
        return NULL;



    int buffer_size = (int)count;

    printf("Initiailzed Jitter with code size: %d bytes\n", buffer_size);
    
    // Check the types for the function signature
    PyObject *sig_seq = PySequence_Fast(sig, "expected a sequence");
    int signature_len = PySequence_Size(sig_seq);

    printf("Signature Size: %d\n", signature_len);

    for (i = 0; i < signature_len; i++) {
        item = PySequence_Fast_GET_ITEM(seq, i);
    }
    Py_DECREF(seq);


    // PyObject *ret_type_seq = PySequence_Fast(retTys, "expected a sequence");
    //int ret_type_len = PySequence_Size(ret_type_len);

    // printf("Num Return Tys: %d\n", ret_type_seq);
    // printf("Num Arg Tys: %d\n", arg_types_len);

    emit_to_rw_run_from_rx(str);

    result = PyLong_FromLong(1.0);

    return result;
}

static PyMethodDef JitterMethods[] = {
  {"jit", (PyCFunction)jitter_jit, METH_VARARGS | METH_KEYWORDS, "Jit a method at runtime"},
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef jittermodule = {
  PyModuleDef_HEAD_INIT,
  "jitter",
  NULL,
  -1,
  JitterMethods
};

PyMODINIT_FUNC PyInit_jitter(void) {
  PyObject *m;
  m = PyModule_Create(&jittermodule);
  if (m == NULL)
    return NULL;

  JitterError = PyErr_NewException("jitter.error", NULL, NULL);
  Py_INCREF(JitterError);
  PyModule_AddObject(m, "error", JitterError);
  return m;
}

int main(int argc, char *argv[]) {
  PyImport_AppendInittab("jitter", PyInit_jitter);

  Py_SetProgramName(argv[0]);

  Py_Initialize();

  PyImport_ImportModule("jitter");
}