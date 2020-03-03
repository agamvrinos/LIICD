from datasketch import MinHash, MinHashLSH

set1 = {
    'import java.lang.*;',
    'import java.io.*;',
    'import java.net.*;',
    'class A {',
    'public static void main(String args[]) {',
    'sout("hello world");',
    '}',
    '}'
}
set2 = {
    'import java.lang.*;',
    'import java.io.*;',
    'import java.net.*;',
    'class B {',
    'public static void main(String args[]) {',
    'sout("hello world");',
    '}',
    '}'
}

m1 = MinHash(num_perm=500)
m2 = MinHash(num_perm=500)
m3 = MinHash(num_perm=500)
for d in set1:
    m1.update(d.encode('utf8'))
for d in set2:
    m2.update(d.encode('utf8'))
# for d in set3:
#     m3.update(d.encode('utf8'))


# Create LSH index
lsh = MinHashLSH(threshold=0.5, num_perm=500)
lsh.insert("m2", m2)
lsh.insert("m3", m3)
result = lsh.query(m1)
print("Approximate neighbours with Jaccard similarity > 0.5", result)