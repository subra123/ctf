# Broadcast - Crypto Challenge Writeup

## Challenge Overview
The challenge provided an `output.txt` file containing three sets of RSA public keys (moduli $n_1, n_2, n_3$ and a common exponent $e = 3$) and three identical ciphertexts $c_1, c_2, c_3$.

## Analysis
The challenge title and the presence of three transmissions with $e=3$ strongly suggested **Håstad's Broadcast Attack**. 

In a standard RSA broadcast attack, if the same message $m$ is sent to $e$ recipients with different moduli $n_i$ but the same small exponent $e$, we can use the Chinese Remainder Theorem (CRT) to find $m^e \pmod{n_1 n_2 \dots n_e}$. Since $m < n_i$, it follows that $m^e < n_1 n_2 \dots n_e$, allowing us to recover $m$ by taking the $e$-th root.

In this specific case, observing the data:
- $e = 3$
- $c_1 = c_2 = c_3$
- $c_1 < n_1$

Because $c_1$ is already smaller than the modulus, it implies that $m^e$ never wrapped around the modulus ($m^3 = c_1$). Thus, a simple cube root of the ciphertext is sufficient to recover the message.

## Solution
The following Python script was used to calculate the cube root and decode the flag:

```python
import gmpy2
from Crypto.Util.number import long_to_bytes

# Ciphertext from output.txt
c = 475436441896018898725156479190091126537849994697426945980826369000641892902004477923335055269088235139492237640527487698088281484953901383579636883543216552932099156009006828723690550706326538736801225046068870773990108130474408522838234755277972911893744937243892927414355347438993698991261629557719442242861719577879055371620865465785392597257968132649494474946507819896785671106833645551504301840437212737125
e = 3

# Compute the cube root
m, exact = gmpy2.iroot(c, e)

if exact:
    print(f"Flag: {long_to_bytes(int(m)).decode()}")
```

## Flag
`kashiCTF{h4st4d_s4ys_sm4ll_3xp0n3nts_k1ll_RSA_br04dc4sts}`
