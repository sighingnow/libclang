#ifndef __FORCE_GLIBC_2_17_H__
#define __FORCE_GLIBC_2_17_H__

#if defined(__x86_64__) && __x86_64__
__asm__(".symver exp,exp@GLIBC_2.2.5");
__asm__(".symver pow,pow@GLIBC_2.2.5");
__asm__(".symver log,log@GLIBC_2.2.5");
__asm__(".symver log2,log2@GLIBC_2.2.5");
#endif

#if defined(__aarch64__) && __aarch64__
__asm__(".symver exp,exp@GLIBC_2.17");
__asm__(".symver pow,pow@GLIBC_2.17");
__asm__(".symver log,log@GLIBC_2.17");
__asm__(".symver log2,log2@GLIBC_2.17");
#endif

#if defined(__arm__) && __arm__
__asm__(".symver exp,exp@GLIBC_2.4");
__asm__(".symver pow,pow@GLIBC_2.4");
__asm__(".symver log,log@GLIBC_2.4");
__asm__(".symver log2,log2@GLIBC_2.4");
#endif

#endif  // __FORCE_GLIBC_2_17_H__
