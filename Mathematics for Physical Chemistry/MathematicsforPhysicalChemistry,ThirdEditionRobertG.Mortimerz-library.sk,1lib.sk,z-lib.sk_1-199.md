## Preface

This book provides a survey of the mathematics needed for chemistry courses at the undergraduate level. In four decades of teaching general chemistry and physical chemistry, I have found that some students have not been introduced to all the mathematical topics needed in these courses and that most need some practice in applying their mathematical knowledge to chemical problems. The emphasis is on the mathematics that is useful in a physical chemistry course, but the first several chapters provide a survey of mathematics that is useful in a general chemistry course.

I have tried to write all parts of this book so that they can be used for self-study by someone not familiar with the material, although any book such as this cannot be a substitute for the traditional training offered in mathematics courses. Exercises and solved example are interspersed throughout the chapters, and these form an important part of the presentations. As you study any topic in the book, you should follow the solution to each example and work each exercise as you come to it.

The first ten chapters of the book are constructed around a sequence of mathematical topics, with a gradual progression into more advanced material. Chapter 11 is a discussion of mathematical topics needed in the analysis of experimental data. Most of the material in at least the first five chapters should be a review for nearly all readers of the book. I have tried to write all of the chapters so that they can be studied in any sequence, or piecemeal as the need arises.

This edition is a revision of a second edition published by Academic Press in 1999. I have reviewed every paragraph and have made those changes that were necessary to improve the clarity and correctness of the presentations. Chapter 9 of the second edition discussed the solution of algebraic equations. It has been divided into two chapters: a new Chapter 3, which contains the parts of the old chapter that apply to general chemistry, and a new Chapter 10, which deals with sets of three or more simultaneous equations. Chapter 5 of the second edition introduced functions of several independent variables, and Chapter 6 of the second edition discussed mathematical series and transforms. These two chapters have been interchanged, since the discussion of series and transforms involves only a single independent variable. Chapter 11 of the second edition involved computer usage. It contained material on word processors, spreadsheets, programming in the BASIC language, graphics packages, and the use of the Mathematica program. The material on word processors, graphics packages, and BASIC programming has been omitted, since most students are now familiar with word processors and tend to use spreadsheets and packaged programs instead of writing their own programs. The material on the use of spreadsheets and the use of Mathematica has been divided up and distributed among various chapters so that the topics are placed with the discussion of the mathematics that is involved. I have continued the use of chapter summaries, chapter previews, lists of important facts and ideas at the beginning of each chapter, and chapter objectives.

This book serves three functions:

1. A review of topics already studied and an introduction to new topics for those preparing for a course in physical chemistry

2. A supplementary text to be used during a physical chemistry course

3. A reference book for graduate students and practicing chemists

I am pleased to acknowledge the cooperation and help of Jeremy Hayhurst and his collaborators at Academic Press. It is also a pleasure to acknowledge the assistance of all those who helped with the first and second editions of this book, and especially to thank my wife, Ann, for her patience, love, and forbearance.

# Numbers, Measurements, and Numerical Mathematics

## Preview

The first application of mathematics to chemistry deals with various physical quantities that have numerical values. In this chapter, we introduce the correct use of numerical values to represent measured physical quantities and the use of numerical mathematics to calculate values of other quantities. Such values generally consist of a number and a unit of measurement, and both parts of the value must be manipulated correctly. We introduce the use of significant digits to communicate the probable accuracy of the measured value. We also review the factor-label method, which is a routine method of expressing a measured quantity in terms of a different unit of measurement.

## Principal Facts and Ideas

1. Specification of a measured quantity consists of a number and a unit.

2. A unit of measurement is an arbitrarily defined quantity that people have agreed to use.

3. The SI units have been officially adopted by international organizations of physicists and chemists.

4. Consistent units must be used in any calculation.

5. The factor-label method can be used to convert from one unit of measurement to another.

6. Reported values of all quantities should be rounded so that insignificant digits are not reported.

## Objectives

After you have studied the chapter, you should be able to:

1. use numbers and units correctly to express measured quantities;

2. understand the relationship of uncertainties in measurements to the use of significant digits;

3. use consistent units, especially the SI units, in equations and formulas; and

4. use the factor-label method to convert from one unit of measurement to another.

## 1.1 Numbers and Measurements

The most common use that chemists make of numbers is to report values for measured quantities. Specification of a measured quantity generally includes a number and a unit of measurement. For example, a length might be given as 12.00 inches (12.00 in) or 30.48 centimeters (30.48 cm), or 0.3048 meters (0.3048 m), and so on. Specification of the quantity is not complete until the unit of measurement is specified. For example, 30.48 cm is definitely not the same as 30.48 in. We discuss numbers in this section of the chapter, and will use some common units of measurement. We discuss units in the next section.

## Numbers

There are several sets into which we can classify numbers. The numbers that can represent physical quantities are called real numbers. These are the numbers with which we ordinarily deal, and they consist of a magnitude and a sign, which can be positive or negative. Real numbers can range from positive numbers of indefinitely large magnitude to negative numbers of indefinitely large magnitude. Among the real numbers are the integers 0, ±1, ±2, ±3, and so on, which are part of the rational numbers. Other rational numbers are quotients of two integers, such as $\frac{2}{3}$ , $\frac{7}{9}$ , $\frac{37}{53}$ . Fractions can be represented as decimal numbers. For example, $\frac{1}{16}$ is the same as 0.0625. Some fractions cannot be represented exactly by a decimal number with a finite number of nonzero digits. For example, $\frac{1}{3}$ is represented by 0.333333···. The three dots (an ellipsis) that follow the given digits indicate that more digits follow. In this case, infinitely many digits are required for an exact representation. However, the decimal representation of a rational number either has a finite number of nonzero digits or contains a repeating pattern of digits.

EXERCISE 1.1 ▶ Take a few simple fractions, such as $\frac{2}{3}$ , $\frac{4}{9}$ , or $\frac{3}{7}$ and express them as decimal numbers, finding either all of the nonzero digits or the repeating pattern of digits.

The numbers that are not rational numbers are called irrational numbers. Algebraic irrational number include square roots of rational numbers, cube roots of rational numbers, and so on, which are not themselves rational numbers. All of the rest of the real numbers are called transcendental irrational numbers. Two commonly encountered transcendental irrational numbers are the ratio of the circumference of a circle to its diameter, called $\pi$ and given by 3.141592653 $\cdots$ , and the base of natural logarithms, called e and given by 2.718281828···. Irrational numbers have the property that if you have some means of finding what the correct digits are, you will never reach a point beyond which all of the remaining digits are zero, or beyond which the digits form some other repeating pattern. $^{1}$

In addition to real numbers, mathematicians have defined imaginary numbers into existence. The imaginary unit, i, is defined to equal $\sqrt{-1}$ . An imaginary number is equal to a real number times i, and a complex number is equal to a real number plus an imaginary number. If x and y are real numbers, then the quantity $z = x + iy$ is a complex number. x is called the real part of z, and the real number y is called the imaginary part of z. Imaginary and complex numbers cannot represent physically measurable quantities, but turn out to have important applications in quantum mechanics. We will discuss complex numbers in the next chapter.

The numbers that we have been discussing are called scalars, to distinguish them from vectors. A scalar number has magnitude and sign, and a vector has both magnitude and direction. We will discuss vectors later, and will see that a vector can be represented by several scalars.

## Measurements, Accuracy, and Significant Digits

A measured quantity can almost never be known with complete exactness. It is therefore a good idea to communicate the probable accuracy of a reported measurement. For example, assume that you measured the length of a piece of glass tubing with a meter stick and that your measured value was 387.8 millimeters (387.8 mm). You decide that your experimental error was probably no greater than 0.6 mm. The best way to specify the length of the glass tubing is

$$
l e n g t h = 387.8 \mathrm{mm} \pm 0.6 \mathrm{mm}
$$

If for some reason you cannot include a statement of the probable error, you should at least avoid including digits that are probably wrong. In this case, your estimated error is somewhat less than 1 mm, so the correct number is probably closer to 388 mm than to either 387 mm or 389 mm. If we do not want to report the expected experimental error, we report the length as 388 mm and assert that the three digits given are significant digits. This means that the given digits are correctly stated. If we had reported the length as 387.8 mm, the last digit is insignificant. That is, if we knew the exact length, the digit 8 after the decimal point is probably not the correct digit, since we believe that the correct length lies between 387.2 mm and 388.4 mm.

You should always avoid reporting digits that are not significant. When you carry out calculations involving measured quantities, you should always determine how many significant digits your answer can have and round off your result to that number of digits. When values of physical quantities are given in a physical chemistry textbook or in this book, you can assume that all digits specified are significant. If you are given a number that you believe to be correctly stated, you can count the number of significant digits. If there are no zeros in the number, the number of significant digits is just the number of digits. If the number contains one or more zeros, any zero that occurs between nonzero digits does count as a significant digit. Any zeros that are present only to specify the location of a decimal point do not represent significant digits. For example, the number 0.0000345 contains three significant digits, and the number 0.003045 contains four significant digits. The number 76,000 contains only two significant digits. However, the number 0.000034500 contains five significant digits. The zeros at the left are present only to locate the decimal point, but the final two zeros are not needed to locate a decimal point, and therefore must have been included because the number is known with sufficient accuracy that these digits are significant.

A problem arises when zeros that appear to occur only to locate the decimal point are actually significant. For example, if a mass is known to be closer to 3500 grams (3500 g) than to 3499 g or to 3501 g, there are four significant digits. If one simply wrote 3500 g, persons with training in significant digits would assume that the zeros are not significant and that there are two significant digits. Some people communicate the fact that there are four significant digits by writing 3500. grams. The explicit decimal point communicates the fact that the zeros are significant digits. Others put a bar over any zeros that are significant, writing 3500 to indicate that there are four significant digits.

## Scientific Notation

The communication difficulty involving significant zeros can be avoided by the use of scientific notation, in which a number is expressed as the product of two factors, one of which is a number lying between 1 and 10 and the other is 10 raised to some integer power. The mass mentioned above would thus be written as $3.500 \times 10^{3}$ g. There are clearly four significant digits indicated, since the trailing zeros are not required to locate a decimal point. If the mass were known to only two significant digits, it would be written as $3.5 \times 10^{3}$ g.

Scientific notation is also convenient for extremely small or extremely large numbers. For example, Avogadro's constant, the number of molecules or other formula units per mole, is easier to write as $6.02214 \times 10^{23}$ mol $^{-1}$ than as 602,214,000,000,000,000,000,000,000 mol $^{-1}$ , and the charge on an electron is easier to write and read as $1.60217 \times 10^{-19}$ coulomb ( $1.60217 \times 10^{-19}$ C) than as 0.000000000000000000160217 C.

EXERCISE 1.2 ▶ Convert the following numbers to scientific notation, using the correct number of significant digits:

(a) 0.000598

(b) 67,342,000

(c) 0.000002

(d) 6432.150

![[2960802b1779f158cc4e48abcbdcc3a04d589bdb9bba9343b3f6dd60b0d6410d.jpg]]

## Rounding

The process of rounding is straightforward in most cases. The calculated number is simply replaced by that number containing the proper number of digits that is closer to the calculated value than any other number containing this many digits. Thus, if there are three significant digits, 4.567 is rounded to 4.57, and 4.564 is rounded to 4.56. However, if your only insignificant digit is a 5, your calculated number is midway between two rounded numbers, and you must decide whether to round up or to round down. It is best to have a rule that will round down half of the time and round up half of the time. One widely used rule is to round to the even digit, since there is a 50% chance that any digit will be even. For example, 2.5 would be rounded to 2, and 3.5 would be rounded to 4. An equally valid procedure that is apparently not generally used would be to toss a coin and round up if the coin comes up “heads” and to round down if it comes up “tails.”

EXERCISE 1.3 ▶

(a) 0.2468985

Round the following numbers to four significant digits

(c) 123456789

(b) 78955

(d) 46.4535


## 1.2 Numerical Mathematical Operations

We are frequently required to carry out numerical operations on numbers. The first such operations involve pairs of numbers.

## Elementary Arithmetic Operations

The elementary mathematical operations are addition, subtraction, multiplication, and division. Some rules for operating on numbers with sign can be simply stated:

1. The product of two factors of the same sign is positive, and the product of two factors of different signs is negative.

2. The quotient of two factors of the same sign is positive, and the quotient of two factors of different signs is negative.

3. The difference of two numbers is the same as the sum of the first number and the negative of the second.

4. Multiplication is commutative, which means that $^{2}$ if a and b stand for numbers

$$
\boxed {a \times b = b \times a.}\tag{1.1}
$$

5. Multiplication is associative, which means that

$$
\boxed {a \times (b \times c) = (a \times b) \times c.}\tag{1.2}
$$

6. Multiplication and addition are distributive, which means that

$$
\boxed {a \times (b + c) = a \times b + a \times c.}\tag{1.3}
$$

## Additional Mathematical Operations

In addition to the four elementary arithmetic operations, there are some other important mathematical operations, many of which involve only one number. The magnitude, or absolute value, of a scalar quantity is a number that gives the size of the number irrespective of its sign. It is denoted by placing vertical bars before and after the symbol for the quantity. This operation means

$$
| x | = \left\{ \begin{array}{r l} x & \text { if } x \geq 0 \\ - x & \text { if } x <   0 \end{array} \right.\tag{1.4}
$$

For example,

$$
\begin{array}{l} {| 4.5 | = 4.5} \\ {| - 3 | = 3} \end{array}
$$

The magnitude of a number is always nonnegative (positive or zero).

Another important set of numerical operations is the taking of powers and roots. If x represents some number that is multiplied by itself n - 1 times so that there are n factors, we represent this by the symbol $x^{n}$ , representing x to the nth power. For example,

$$
x ^ {2} = x \times x, \quad x ^ {3} = x \times x \times x, \quad x ^ {n} = x \times x \times x \times \dots \times x \quad (n \text {factors}).\tag{1.5}
$$

The number n in the expression $x^{n}$ is called the exponent of x. If the exponent is not an integer, we can still define $x^{n}$ . We will discuss this when we discuss logarithms. An exponent that is a negative number indicates the reciprocal of the quantity with a positive exponent:

$$
\boxed {x ^ {- 1} = \frac {1}{x}, \quad x ^ {- 3} = \frac {1}{x ^ {3}}}\tag{1.6}
$$

There are some important facts about exponents. The first is

$$
\boxed {x ^ {a} x ^ {b} = x ^ {a + b}}\tag{1.7}
$$

where x, a, and b represent numbers. We call such an equation an identity, which means that it is correct for all values of the variables in the equation. The next identity is

$$
\boxed {(x ^ {a}) ^ {b} = x ^ {a b}}\tag{1.8}
$$

Roots of real numbers are defined in an inverse way from powers. For example, the square root of x is denoted by $\sqrt{x}$ and is defined as the number that yields x when squared:

$$
(\sqrt {x}) ^ {2} = x\tag{1.9}
$$

The cube root of $x$ is denoted by $\sqrt[3]{x}$ , and is defined as the number that when cubed (raised to the third power) yields $x$ :

$$
\left(\sqrt [ 3 ]{x}\right) ^ {3} = x\tag{1.10}
$$

Fourth roots, fifth roots, and so on, are defined in similar ways. The operation of taking a root is the same as raising a number to a fractional exponent. For example,

$$
\sqrt [ 3 ]{x} = x ^ {1 / 3}\tag{1.11}
$$

This equation means that

$$
\left(\sqrt [ 3 ]{x}\right) ^ {3} = \left(x ^ {1 / 3}\right) ^ {3} = x = \left(x ^ {3}\right) ^ {1 / 3} = \sqrt [ 3 ]{x ^ {3}}.
$$

This equation illustrates the fact that the order of taking a root and raising to a power can be reversed without changing the result. We say that these operations commute with each other.

There are two numbers that when squared will yield a given positive real number. For example, $2^{2} = 4$ and $(-2)^{2} = 4$ . When the symbol $\sqrt{\frac{1}{4}}$ is used, only the positive square root, 2, is meant. To specify the negative square root of x, we write $-\sqrt{x}$ . If we confine ourselves to real numbers, there is no square root, fourth root, sixth root, and so on, of a negative number. In Section 2.6, we define imaginary numbers, which are defined be square roots of negative quantities. Both positive and negative numbers can have real cube roots, fifth roots, and so on, since an odd number of negative factors yields a negative product.

The square roots, cube roots, and so forth, of integers and other rational numbers are either rational numbers or algebraic irrational numbers. The square root of 2 is an example of an algebraic irrational number. An algebraic irrational number produces a rational number when raised to the proper integral power. When written as a decimal number, an algebraic irrational number does not have a finite number of nonzero digits or exhibit any pattern of repeating digits. An irrational number that does not produce a rational number when raised to any integral power is a transcendental irrational number. Examples are e, the base of natural logarithms, and $\pi$ , the ratio of a circle's circumference to its diameter.

## Logarithms

We have discussed the operation of raising a number to an integral power. The expression $a^{2}$ means $a \times a$ , $a^{-2}$ means $1/a^{2}$ , $a^{3}$ means $a \times a \times a$ , and so on. In addition, you can have exponents that are not integers. If we write

$$
y = a ^ {x}\tag{1.12}
$$

the exponent $x$ is called the logarithm of $y$ to the base $a$ and is denoted by

$$
x = \log_ {a} (y)\tag{1.13}
$$

If $a$ is positive, only positive numbers possess real logarithms.

## Common Logarithms

If the base of logarithms equals 10, the logarithms are called common logarithms: If $10^{x} = y$ , then x is the common logarithm of y, denoted by $\log_{10}(y)$ . The subscript 10 is sometimes omitted, but this can cause confusion.

For integral values of x, it is easy to generate the following short table of common logarithms:

<table><tr><td>y</td><td> $x = \log_{10}(y)$ </td><td>y</td><td> $x = \log_{10}(y)$ </td></tr><tr><td>1</td><td>0</td><td>0.1</td><td>-1</td></tr><tr><td>10</td><td>1</td><td>0.01</td><td>-2</td></tr><tr><td>100</td><td>2</td><td>0.001</td><td>-3</td></tr><tr><td>1000</td><td>3</td><td>etc.</td><td></td></tr></table>

In order to understand logarithms that are not integers, we need to understand exponents that are not integers.

EXAMPLE 1.1 Find the common logarithm of $\sqrt{10}$ .

SOLUTION ▶ The square root of 10 is the number that yields 10 when multiplied by itself:

$$
\left(\sqrt {10}\right) ^ {2} = 10.
$$

We use the fact about exponents

$$
\left(a ^ {x}\right) ^ {z} = a ^ {x z}.\tag{1.14}
$$

Since 10 is the same thing as $10^{1}$ ,

$$
\sqrt {10} = 10 ^ {1 / 2}.\tag{1.15}
$$

Therefore

$$
\log_ {10} \left(\sqrt {10}\right) = \log_ {10} (3.162277 \dots) = \frac {1}{2} = 0.5000
$$

Equation (1.14) and some other relations governing exponents can be used to generate other logarithms, as in the following problem.

EXERCISE 1.4 ▶ Use Eq. (1.14) and the fact that $10^{-n} = 1/(10^{n})$ to generate the negative logarithms in the short table of logarithms.

We will not discuss further how the logarithms of various numbers are computed. Extensive tables of logarithms with up to seven or eight significant digits were once in common use. Most electronic calculators provide values of logarithms with as many as 10 or 11 significant digits. Before the invention of electronic calculators, tables of logarithms were used when a calculation required more significant digits than a slide rule could provide. For example, to multiply two numbers together, one would look up the logarithms of the two numbers, add the logarithms and then look up the antilogarithm of the sum (the number possessing the sum as its logarithm).

## Natural Logarithms

Besides 10, there is another commonly used base of logarithms. This is a transcendental irrational number called e and equal to 2.7182818 ...

$$
\boxed {\text {   If   } e ^ {y} = x \quad \text {   then   } y = \log_ {e} (x) = \ln (x).}\tag{1.16}
$$

Logarithms to this base are called natural logarithms. The definition of e is $^{3}$

$$
e = \lim _ {n \rightarrow \infty} \left(1 + \frac {1}{n}\right) ^ {n} = 2.7182818 \dots\tag{1.17}
$$

The “lim” notation means that larger and larger values of n are taken.

EXERCISE 1.5 ▶ Evaluate the quantity $(1 + \frac{1}{n})^{n}$ for several integral values of n ranging from 1 to 1,000,000. Notice how the value approaches the value of e as n increases.

The notation $\ln(x)$ is more common than $\log_{e}(x)$ . Natural logarithms are also occasionally called Napierian logarithms. $^{4}$ Unfortunately, some mathematicians use the symbol $\log(y)$ without a subscript for natural logarithms. Chemists frequently use the symbol $\log(y)$ without a subscript for common logarithms and the symbol $\ln(y)$ for natural logarithms. Chemists use both common and natural logarithms, so the best practice is to use $\log_{10}(x)$ for the common logarithm of x and $\ln(x)$ for the natural logarithm of x.

If the common logarithm of a number is known, its natural logarithm can be computed as

$$
e ^ {\ln (y)} = 10 ^ {\log_ {10} (y)} = \left(e ^ {\ln (10)}\right) ^ {\log_ {10} (y)} = e ^ {\ln (10) \log_ {10} (y)}.\tag{1.18}
$$

The natural logarithm of 10 is equal to 2.302585 . . . , so we can write

$$
\boxed {\ln (y) = \ln (10) \log_ {10} (y) = (2.302585 \dots) \log_ {10} (y).}\tag{1.19}
$$

In order to remember Eq. (1.19) correctly, keep the fact in mind that since e is smaller than 10, the natural logarithm is larger than the common logarithm.

EXERCISE 1.6 ▶
the following:

Without using a calculator or a table of logarithms, find

(a) $\ln (100.000)$

$$
\ln (0.0010000) \tag {b}
$$

(c) $\log_{10}(e)$


## Logarithm Identities

There are a number of identities involving logarithms, some of which come from the exponent identities in Eqs. (1.6)-(1.8). Table 1.1 lists some identities involving exponents and logarithms. These identities hold for common logarithms and natural logarithms as well for logarithms to any other base.

## TABLE 1.1 ▶ Properties of Exponents and Logarithms

Exponent fact Logarithm fact

$$
a ^ {0} = 1 \quad \log_ {a} (1) = 0
$$

$$
a ^ {1 / 2} = \sqrt {a} \qquad \log_ {a} (\sqrt {a}) = \frac {1}{2}
$$

$$
a ^ {1} = a \qquad \log_ {a} (a) = 1
$$

$$
a ^ {x _ {1}} a ^ {x _ {2}} = a ^ {x _ {1} + x _ {2}} \log_ {a} (y _ {1} y _ {2}) = \log_ {a} (y _ {1}) + \log_ {a} (y _ {2})
$$

$$
a ^ {- x} = \frac {1}{a ^ {x}} \log_ {a} \left(\frac {1}{y}\right) = - \log_ {a} (y)
$$

$$
\frac {a ^ {x _ {1}}}{a ^ {x _ {2}}} = a ^ {x _ {1} - x _ {2}} \log_ {a} \left(\frac {y _ {1}}{y _ {2}}\right) = \log_ {a} (y _ {1}) - \log_ {a} (y _ {2})
$$

$$
(a ^ {x}) ^ {z} = a ^ {x _ {z}} \qquad \log_ {a} {(y ^ {z})} = z \log_ {a} {(y)}
$$

$$
a ^ {\infty} = \infty \quad \log_ {a} (\infty) = \infty
$$

$$
a ^ {- \infty} = 0 \quad \log_ {a} (0) = - \infty
$$

![[610169e1f0168363993087de551f081e041f2541ba04a3388e2f56a42e270fa1.jpg]]  
Figure 1.1 ▶ The exponential function.

## The Exponential

The exponential is the same as raising e (the base of natural logarithms, equal to 2.7182818284 $\cdots$ ) to a given power and is denoted either by the usual notation for a power, or by the notation exp( $\cdots$ ).

$$
y = a e ^ {b x} \equiv a \exp (b x),\tag{1.20}
$$

Figure 1.1 shows a graph of this function for $b > 0$ .

The graph in Fig. 1.1 exhibits an important behavior of the exponential $e^{bx}$ . For b > 0, it doubles each time the independent variable increases by a fixed amount whose value depends on the value of b. For large values of b the exponential function becomes large very rapidly. If b < 0, the function decreases to half its value each time the independent variable increases by a fixed amount. For large negative values of b the exponential function becomes small very rapidly.

EXERCISE 1.7 For a positive value of b find an expression for the change in x required for the function $e^{bx}$ to double in size.

An example of the exponential function is in the decay of radioactive isotopes. If $N_{0}$ is the number of atoms of the isotope at time t = 0, the number at any other time, t, is given by

$$
N (t) = N _ {0} e ^ {- t / \tau},\tag{1.21}
$$

where $\tau$ is called the relaxation time. It is the time for the number of atoms of the isotope to drop to 1/e = 0.367879 of its original value. The time that is required for the number of atoms to drop to half its original value is called the half-time or half-life, denoted by $t_{1/2}$ .

EXAMPLE 1.2 Show that $t_{1/2}$ is equal to $\tau \ln(2)$ .

SOLUTION ▶ If $t_{1/2}$ is the half-life, then

$$
e ^ {- t _ {1 / 2} / \tau} = \frac {1}{2}.
$$

Thus

$$
\frac {t _ {1 / 2}}{\tau} = - \ln \left(\frac {1}{2}\right) = \ln (2).\tag{1.22}
$$

EXERCISE 1.8 ▶ A certain population is growing exponentially and doubles in size each 30 years.

(a) If the population includes $4.00 \times 10^{6}$ individuals at $t = 0$ , write the formula giving the population after a number of years equal to $t$ .

(b) Find the size of the population at $t = 150$ years.

EXERCISE 1.9 ▶ A reactant in a first-order chemical reaction without back reaction has a concentration governed by the same formula as radioactive decay,

$$
[ \mathbf {A} ] _ {t} = [ \mathbf {A} ] _ {0} e ^ {- k t},
$$

where $[A]_{0}$ is the concentration at time t = 0, $[A]_{t}$ is the concentration at time t, and k is a function of temperature called the rate constant. If $k = 0.123 s^{-1}$ , find the time required for the concentration to drop to 21.0% of its initial value.

## 1.3 Units of Measurement

The measurement of a length or other variable would be impossible without a standard definition of the unit of measurement. For many years science and commerce were hampered by the lack of accurately defined units of measurement. This problem has been largely overcome by precise measurements and international agreements. The internationally accepted system of units of measurements is called the Système International d'Unités, abbreviated SI. This is an MKS system, which means that length is measured in meters, mass in kilograms, and time in seconds. In 1960 the international chemical community agreed to use SI units, which had been in use by physicists for some time. $^{5}$ The seven base units given in Table 1.2 form the heart of the system. The table also includes some derived units, which owe their definitions to the definitions of the seven base units.

TABLE 1.2 ▶ SI Units  
SI base units (units with independent definitions)

<table><tr><td>Physical quantity</td><td>Name of unit</td><td>Symbol</td><td>Definition</td></tr><tr><td>Length</td><td>meter</td><td>m</td><td>Length such that the speed of light is exactly  $299,792,458 \text{ m s}^{-1}$ .</td></tr><tr><td>Mass</td><td>kilogram</td><td>kg</td><td>The mass of a platinum-iridium cylinder kept at the International Bureau of Weights and Measures in France.</td></tr><tr><td>Time</td><td>second</td><td>s</td><td>The duration of 9,192,631,770 cycles of the radiation of a certain emission of the cesium atom.</td></tr><tr><td>Electric current</td><td>ampere</td><td>A</td><td>The magnitude of current which, when flowing in each of two long parallel wires 1 m apart in free space, results in a force of  $2 \times 10^{7} \text{ N per meter of length}$ .</td></tr><tr><td>Temperature</td><td>kelvin</td><td>K</td><td>Absolute zero is 0 K; triple point of water is 273.16 K.</td></tr><tr><td>Luminous intensity</td><td>candela</td><td>cd</td><td>The luminous intensity, in the perpendicular intensity direction, of a surface of 1/600,  $000 \text{ m}^{2}$  of a black body at temperature of freezing platinum at a pressure of  $101,325 \text{ N m}^{-2}$ .</td></tr><tr><td>Amount of substance</td><td>mole.</td><td>mol</td><td>Amount of substance that contains as many elementary units as there are carbon atoms in exactly 0.012 kg of the carbon- $12 (^{12}\text{C})$  isotope.</td></tr></table>

Other SI units (derived units)

<table><tr><td>Physical quantity</td><td>Name of unit</td><td>Physical dimensions</td><td>Symbol</td><td>Definition</td></tr><tr><td>Force</td><td>newton</td><td> $\text{kg m s}^{-2}$ </td><td>N</td><td> $1\text{ N} = 1\text{ kg m s}^{-2}$ </td></tr><tr><td>Energy</td><td>joule</td><td> $\text{kg m}^{2}\text{ s}^{-2}$ </td><td>J</td><td> $1\text{ J} = 1\text{ kg m}^{2}\text{ s}^{-2}$ </td></tr><tr><td>Electrical charge</td><td>coulomb</td><td>A s</td><td>C</td><td> $1\text{ C} = 1\text{ A s}$ </td></tr><tr><td>Pressure</td><td>pascal</td><td> $\text{N m}^{-2}$ </td><td>Pa</td><td> $1\text{ Pa} = 1\text{ N m}^{-2}$ </td></tr><tr><td>Magnetic field</td><td>tesla</td><td> $\text{kg s}^{-2}\text{ A}^{-1}$ </td><td>T</td><td> $1\text{ T} = 1\text{ kg s}^{-2}\text{ A}^{-1}$  $= 1\text{ Wb m}^{-2}$ </td></tr><tr><td>Luminous flux</td><td>lumen</td><td>cd sr</td><td>lm</td><td> $1\text{ lm} = 1\text{ cd sr}$ (sr = steradian)</td></tr></table>

Multiples and submultiples of SI units are commonly used. $^{6}$ Examples are the millimeter and kilometer. These multiples and submultiples are denoted by standard prefixes attached to the name of the unit, as listed in Table 1.3. The abbreviation for a multiple or submultiple is obtained by attaching the prefix abbreviation to the unit abbreviation, as in Gm (gigameter) or ns (nanosecond). Note that since the base unit of length is the kilogram, the table would imply the use of things such as the mega kilogram. Double prefixes are not used. We use gigagram instead of megakilogram. The use of the prefixes for $10^{-1}$ and $10^{-2}$ is discouraged, but centimeters will probably not be abandoned for many years to come. The Celsius temperature scale also remains in common use among chemists.

TABLE 1.3 ▶ Prefixes for Multiple and Submultiple Units

<table><tr><td>Multiple</td><td>Prefix</td><td>Abbreviation</td><td>Multiple</td><td>Prefix</td><td>Abbreviation</td></tr><tr><td> $10^{12}$ </td><td>tera-</td><td>T</td><td> $10^{-3}$ </td><td>milli-</td><td>m</td></tr><tr><td> $10^9$ </td><td>giga-</td><td>G</td><td> $10^{-6}$ </td><td>micro-</td><td> $\mu$ </td></tr><tr><td> $10^6$ </td><td>mega-</td><td>M</td><td> $10^{-9}$ </td><td>nano-</td><td>n</td></tr><tr><td> $10^3$ </td><td>kilo-</td><td>k</td><td> $10^{-12}$ </td><td>pico-</td><td>p</td></tr><tr><td>1</td><td>—</td><td>—</td><td> $10^{-15}$ </td><td>femto-</td><td>f</td></tr><tr><td> $10^{-1}$ </td><td>deci-</td><td>d</td><td> $10^{-18}$ </td><td>atto-</td><td>a</td></tr><tr><td> $10^{-2}$ </td><td>centi-</td><td>c</td><td></td><td></td><td></td></tr></table>

Some non-SI units continue to be used, such as the atmosphere (atm), which is a pressure defined to equal 101, 325 N m $^{-2}$ (101, 325 Pa), the liter (l), which is exactly 0.001 m $^{3}$ , and the torr, which is a pressure such that exactly 760 torr equals exactly 1 atm. The Celsius temperature scale is defined such that the degree Celsius (°C) is the same size as the kelvin, and 0 °C is equivalent to 273.15 K.

In the United States of America, English units of measurement are still in common use. The inch (in) has been redefined to equal exactly 0.0254 m. The foot (ft) is 12 inches and the mile (mi) is 5280 feet. The pound (lb) is equal to 0.4536 kg (not an exact definition; good to four significant digits).

Any measured quantity is not completely specified until its units are given. If a is a length equal to 10.345 m, one must write

$$
a = 10.345 \mathrm{m}\tag{1.23}
$$

not just

$$
a = 10.345 \quad (\text { not   correct }).
$$

It is permissible to write

$$
a / \mathrm{m} = 10.345
$$

which means that the length a divided by 1 m is 10.345, a dimensionless number. When constructing a table of values, it is convenient to label the columns or rows with such dimensionless quantities.

When you make numerical calculations, you should make certain that you use consistent units for all quantities. Otherwise, you will likely get the wrong answer. This means that (1) you must convert all multiple and submultiple units to the base unit, and (2) you cannot mix different systems of units. For example, you cannot correctly substitute a length in inches into a formula in which the other quantities are in SI units without converting. It is a good idea to write the unit as well as the number, as in Eq. (1.23), even for scratch calculations. This will help you avoid some kinds of mistakes by inspecting any equation and making sure that both sides are measured in the same units. In 1999 a U.S. space vehicle optimistically named the Mars Climate Orbiter crashed into the surface of Mars instead of orbiting the planet. The problem turned out to be that engineers working on the project had used English units such as feet and pounds, whereas physicists had used metric units such as meters and kilograms. A failure to convert units properly cost U.S. taxpayers several millions of dollars and the loss of a possibly useful mission. In another instance, when a Canadian airline switched from English units to metric units, a ground crew miscalculated the mass of fuel needed for a flight. The jet airplane ran out of fuel, but was able to glide to an unused military airfield and make a “deadstick” landing. Some people were having a picnic on the unused runway, but were able to get out of the way. There was even a movie made about the incident.

## 1.4 Numerical Calculations

The most common type of numerical calculation in a chemistry course is the calculation of one quantity from the numerical values of other quantities, guided by some formula. There can be familiar formulas that are used in everyday life and there can be formulas that are specific to chemistry. Some formulas require only the four basic arithmetic operations: addition, subtraction, multiplication, and division. Other formulas require the use of the exponential, logarithms, or trigonometric functions. The formula is a recipe for carrying out the specified numerical operations. Each quantity is represented by a symbol (a letter) and the operations are specified by symbols such as $\times$ , /, +, -, ln, and so on. A simple example is the familiar formula for calculating the volume of a rectangular object as the product of its height (h), width (w), and length (l):

$$
V = h \times w \times l
$$

The symbol for multiplication is often omitted so that the formula would be written v = hwl. If two symbols are written side by side, it is understood that the quantities represented by the symbols are to be multiplied together. Another example is the ideal gas equation

$$
P = \frac {n R T}{V}\tag{1.24}
$$

where P represents the pressure of the gas, n is the amount of gas in moles, T is the absolute temperature, V is the volume, and R is a constant known as the ideal gas constant.

## Significant Digits in a Calculated Quantity

When you calculate a numerical value that depends on a set of numerical values substituted into a formula, the accuracy of the result depends on the accuracy of the first set of values. The number of significant digits in the result depends on the numbers of significant digits in the first set of values. Any result containing insignificant digits must be rounded to the proper number of digits.

## Multiplication and Division

There are several useful rules of thumb that allow you to determine the proper number of significant digits in the result of a calculation. For multiplication of two or more factors, the rule is that the product will have the same number of significant digits as the factor with the fewest significant digits. The same rule holds for division. In the following example we use the fact that the volume of a rectangular object is the product of its length times its width times its height.

EXAMPLE 1.3 What is the volume of a rectangular object whose length is given as 7.78 m, whose width is given as 3.486 m, and whose height is 1.367 m?

SOLUTION ▶ We denote the volume by V and obtain the volume by multiplication, using a calculator.

$$
V = (7.78 \mathrm{m}) (3.486 \mathrm{m}) (1.367 \mathrm{m}) = 37.07451636 \mathrm{m} ^ {3} = 37.1 \mathrm{m} ^ {3}.
$$

The calculator delivered 10 digits, but we round the volume to $37.1\mathrm{m}^3$ , since the factor with the fewest significant digits has three significant digits.

EXAMPLE 1.4 Compute the smallest and largest values that the volume in Example 1.1 might have and determine whether the answer given in Example 1.1 is correctly stated.

SOLUTION ▶ The smallest value that the length might have, assuming the given value to have only significant digits, is 7.775 m, and the largest value that it might have is 7.785 m. The smallest possible value for the width is 3.4855 m, and the largest value is 3.4865 m. The smallest possible value for the height is 1.3665 m, and the largest value is 1.3675 m. The minimum value for the volume is

$$
V _ {\min} = (7.775 \mathrm{m}) (3.4855 \mathrm{m}) (1.3665 \mathrm{m}) = 37.0318254562 \mathrm{m} ^ {3}.
$$

The maximum value is

$$
V _ {\max} = (7.785 \mathrm{m}) (3.4865 \mathrm{m}) (1.3675 \mathrm{m}) = 37.1172354188 \mathrm{m} ^ {3}.
$$

Obviously, all of the digits beyond the first three are insignificant. The rounded result of $37.1 \, m^{3}$ in Example 1.1 contains all of the digits that can justifiably be given. However, in this case there is some chance that $37.0 \, m^{3}$ might be closer to the actual volume than is $37.1 \, m^{3}$ . We will still consider a digit to be significant if it might be incorrect by $\pm1$ .

## Addition and Subtraction

The rule of thumb for significant digits in addition or subtraction is that for a digit to be significant, it must arise from a significant digit in every term of the sum or difference. You cannot simply count the number of significant digits in every term.

EXAMPLE 1.5 Determine the combined length of two objects, one of length 0.783 m and one of length 17.3184 m.

SOLUTION ▶ We make the addition:

$$
\begin{array}{r l} & \frac {0 .783 \mathrm{m}}{17 .3184 \mathrm{m}} \\ & \overline {{18 .1014 \mathrm{m}}} \approx 18.101 \mathrm{m} \end{array}
$$

The fourth digit after the decimal point in the sum could be significant only if that digit were significant in every term of the sum. The first number has only three significant digits after the decimal point. We must round the answer to 18.101 m. Even after this rounding, we have obtained a number with five significant digits, while one of our terms has only three significant digits.

In a calculation with several steps, it is not a good idea to round off the insignificant digits at each step. This procedure can lead to accumulation of round-off error. A reasonable policy is to carry along at least one insignificant digit during the calculation, and then to round off the insignificant digits at the final answer. When using an electronic calculator, it is easy to use all of the digits carried by the calculator and then to round off at the end of the calculation.

## Significant Digits in Trigonometric Functions, Logarithms, and Exponentials

If you are carrying out operations other than additions, subtractions, multiplications, and divisions, determining which digits are significant is not so easy. In many cases the number of significant digits in the result is roughly the same as the number of significant digits in the argument of the function, but more accurate rules of thumb can be found. $^{7}$ If you need an accurate determination of the number of significant digits when applying these functions, it might be necessary to do the operation with the smallest and the largest values that the number on which you must operate can have (incrementing and decrementing the number).

EXAMPLE 1.6 Calculate the following. Determine the correct number of significant digits by incrementing or decrementing.

(a) $\sin (372.15^{\circ})$

(b) $\ln (567.812)$

SOLUTION ▶ (a) Using a calculator, we obtain

$$
\begin{array}{l l} \sin (372.155 ^ {\circ}) & = 0.210557 \\ \sin (372.145 ^ {\circ}) & = 0.210386. \end{array}
$$

Therefore,

$$
\sin (372.15 ^ {\circ}) = 0.2105.
$$

The value could be as small as 0.2104, but we write 0.2105, since we routinely declare a digit to be significant if it might be wrong by just $\pm1$ . Even though the argument of the sine had five significant digits, the sine has only four significant digits.

(b) By use of a calculator, we obtain

$$
\begin{array}{l l} \ln (567.8125) = & 6.341791259 \\ \ln (567.8115) = & 6.341789497. \end{array}
$$

Therefore,

$$
\ln (567.812) = 6.34179.
$$

In this case, the logarithm has the same number of significant digits as its argument. If the argument of a logarithm is very large, the logarithm can have many more significant digits than its argument, since the logarithm of a large number is a slowly varying function of its argument.

(c) Using a calculator, we obtain

$$
\begin{array}{l l} e ^ {- 9.8135} = & 0.00005470803 \\ e ^ {- 9.8125} = & 0.00005476277. \end{array}
$$

Therefore, when we round off the insignificant digits,

$$
e ^ {- 9.8125} = 0.000547.
$$

Although the argument of the exponential had four significant digits, the exponential has only three significant digits. The exponential function of fairly large arguments is a rapidly varying function, so fewer significant digits can be expected for large arguments.

EXERCISE 1.10 ▶ Calculate the following to the proper numbers of signif-

icant digits.

$$
(37.815 + 0.00435) (17.01 + 3.713)
$$

(b) $625[e^{12.1} + \sin(60.0^{\circ})]$

(c) $65.718 \times 12.3$

(d) $17.13 + 14.6751 + 3.123 + 7.654 - 8.123$ .


## The Factor-Label Method

This is an elementary method for the routine conversion of a quantity measured in one unit to the same quantity measured in another unit. The method consists of multiplying the quantity by a conversion factor, which is a fraction that is equal to unity in a physical sense, with the numerator and denominator equal to the same quantity expressed in different units. This does not change the quantity physically, but numerically expresses it in another unit, and so changes the number expressing the value of the quantity. For example, to express 3.00 km in terms of meters, one writes

$$
(3.00 \mathrm{km}) \left(\frac {1000 \mathrm{m}}{1 \mathrm{km}}\right) = 3000 \mathrm{m} = 3.00 \times 10 ^ {3} \mathrm{m}.\tag{1.25}
$$

You can check the units by considering a given unit to “cancel” if it occurs in both the numerator and denominator. Thus, both sides of Eq. (1.25) have units of meters, because the km on the top cancels the km on the bottom of the left-hand side. In applying the method, you should write out the factors explicitly, including the units. You should carefully check that the unwanted units cancel. Only then should you proceed to the numerical calculation.

EXAMPLE 1.7 Express the speed of light, $2.9979 \times 10^{8}$ m s $^{-1}$ , in miles per hour. Use the definition of the inch, 1 in = 0.0254 m (exactly).

## SOLUTION ▶

$$
\begin{array}{r l} \left(2.9979 \times 10 ^ {8} \mathrm{ms} ^ {- 1}\right) & \left(\frac {1 \text {in}}{0 .0254 \mathrm{m}}\right) \left(\frac {1 \mathrm{ft}}{12 \text {in}}\right) \left(\frac {1 \mathrm{mi}}{5280 \mathrm{ft}}\right) \left(\frac {60 \mathrm{s}}{1 \min}\right) \left(\frac {60 \min}{1 \mathrm{h}}\right) \\ & = 6.7061 \times 10 ^ {8} \mathrm{mi} \mathrm{h} ^ {- 1}. \end{array}
$$

The conversion factors that correspond to exact definitions do not limit the number of significant digits. In this example, all of the conversion factors are exact definitions, so our answer has five significant digits because the stated speed has five significant digits.

EXERCISE 1.11 ▶ Express the following in terms of SI base units. The electron volt (eV), a unit of energy, equals $1.6022 \times 10^{-19}$ J.
(a) 24.17 mi (b) $75 \, mi h^{-1}$ (c) $7.5 \, nm ps^{-1}$ (d) 13.6 eV


## SUMMARY

In this chapter, we introduced the use of numerical values and operations in chemistry. In order to use such values correctly, one must handle the units of measurement in which they are expressed. Techniques for doing this, including the factor-label method, were introduced. One must also recognize the uncertainties in experimentally measured quantities. In order to avoid implying a greater accuracy than actually exists, one must express calculated quantities with the proper number of significant digits. Basic rules for significant digits were presented.

## PROBLEMS

1. Find the number of inches in a meter. How many significant digits could be given?

2. Find the number of meters in 1 mile and the number of miles in 1 kilometer, using the definition of the inch. How many significant digits could be given?

3. A furlong is one-eighth of a mile and a fortnight is 2 weeks. Find the speed of light in furlongs per fortnight, using the correct number of significant digits.

4. The distance by road from Memphis, Tennessee, to Nashville, Tennessee, is 206 miles. Express this distance in meters and in kilometers.

5. A U.S. gallon is defined as 231.00 cubic inches.

a) Find the number of liters in one gallon.

b) The volume of a mole of an ideal gas at $0.00^{\circ}$ C (273.15 K) and 1.000 atm is 22.414 liters. Express this volume in gallons and in cubic feet.

6. In the USA, footraces were once measured in yards and at one time, a time of 10.00 seconds for this distance was thought to be unattainable. The best runners now run 100 m in 10 seconds. Express 100 m in yards, assuming three significant digits. If a runner runs 100 m in 10.00 s, find his time for 100 yards, assuming a constant speed.

7. Find the average length of a century in seconds and in minutes, finding all possible significant digits. Use the fact that a year ending in 00 is not a leap year unless the year is divisible by 400, in which case it is a leap year. Find the number of minutes in a microcentury.

8. A light year is the distance traveled by light in one year.

a) Express this distance in meters and in kilometers. Use the average length of a year as described in the previous problem. How many significant digits can be given?

b) Express a light year in miles.

9. The Rankine temperature scale is defined so that the Rankine degree is the same size as the Fahrenheit degree, and $0^{\circ}$ R is the same as 0 K.

a) Find the Rankine temperature at $0.00^{\circ}$ C.

b) Find the Rankine temperature at $0.00^{\circ}$ F.

10. Calculate the mass of AgCl that can be precipitated from 10.00 ml of a solution of NaCl containing $0.345 \, mol l^{-1}$ . Report your answer to the correct number of digits.

11. The volume of a sphere is given by

$$
V = \frac {4}{3} \pi r ^ {3}\tag{1.26}
$$

where V is the volume and r is the radius. If a certain sphere has a radius given as 0.005250 m, find its volume, specifying it with the correct number of digits. Calculate the smallest and largest volumes that the sphere might have with the given information and check your first answer for the volume.

12. The volume of a right circular cylinder is given by

$$
V = \pi r ^ {2} h,
$$

where V is the volume, r is the radius, and h is the height. If a certain right circular cylinder has a radius given as 0.134 m and a height given as 0.318 m, find its volume, specifying it with the correct number of digits. Calculate the smallest and largest volumes that the cylinder might have with the given information and check your first answer for the volume.

13. The value of a certain angle is given as $31^{\circ}$ . Find the measure of the angle in radians. Using a table of trigonometric functions or a calculator, find the smallest and largest values that its sine and cosine might have and specify the sine and cosine to the appropriate number of digits.

a) Some elementary chemistry textbooks give the value of R, the ideal gas constant, as 0.08211 atm K $^{-1}$ mol $^{-1}$ . Using the SI value, 8.3145 J K $^{-1}$ mol $^{-1}$ , obtain the value in 1 atm K $^{-1}$ mol $^{-1}$ to five significant digits.

b) Calculate the pressure in atmospheres and in N m $^{-2}$ (Pa) of a sample of an ideal gas with n = 0.13678 mol, V = 1.0001 and T = 298.15 K, using the value of the ideal gas constant in SI units.

c) Calculate the pressure in part b in atmospheres and in $N m^{-2}$ (Pa) using the value of the ideal gas constant in $1 atm K^{-1} mol^{-1}$ .

15. The van der Waals equation of state gives better accuracy than the ideal gas equation of state. It is

$$
\left(P + \frac {a}{V _ {m} ^ {2}}\right) (V _ {m} - b) = R T
$$

where a and b are parameters that have different values for different gases and where $V_{m} = V/n$ , the molar volume. For carbon dioxide, $a = 0.3640 \, Pa \, m^{6} \, mol^{-2}$ , $b = 4.267 \times 10^{-5} \, m^{3} \, mol^{-1}$ . Calculate the pressure of carbon dioxide in pascals, assuming that n = 0.13678 mol, V = 1.0001, and T = 298.15 K. Convert your answer to atmospheres and torr.

16. The specific heat capacity (specific heat) of a substance is crudely defined as the amount of heat required to raise the temperature of unit mass of the substance by 1 degree Celsius (1 °C). The specific heat capacity of water is $4.18 \, J^{\circ}C^{-1} \, g^{-1}$ . Find the rise in temperature if 100.0 J of heat is transferred to 1.000 kg of water.

# Symbolic Mathematics and Mathematical Functions

## Preview

In this chapter, we discuss symbolic mathematical operations, including algebraic operations on real scalar variables, algebraic operations on real vector variables, and algebraic operations on complex scalar variables. We introduce the concept of a mathematical function and discuss trigonometric functions, logarithms and the exponential function.

## Principal Facts and Ideas

1. Algebra is a branch of mathematics in which operations are performed symbolically instead of numerically, according to a well-defined set of rules.

2. Trigonometric functions are examples of mathematical functions: To a given value of an angle there corresponds a value of the sine function, and so on.

3. There is a set of useful trigonometric identities.

4. A vector is a quantity with magnitude and direction.

5. Vector algebra is an extension of ordinary algebra with its own rules and defined operations.

6. A complex number has a real part and an imaginary part that is proportional to i, defined to equal $\sqrt{-1}$ .

7. The algebra of complex numbers is an extension of ordinary algebra with its own rules and defined operations.

8. Problem solving in chemistry involves organizing the given information, understanding the objective, planning the approach, carrying out the procedures, and checking the answer.

## Objectives

After you have studied the chapter, you should be able to:

1. manipulate variables algebraically to simplify complicated algebraic expressions;

2. manipulate trigonometric functions correctly;

3. work correctly with logarithms and exponentials;

4. calculate correctly the sum, difference, scalar product, and vector product of any two vectors, whether constant or variable;

5. perform elementary algebraic operations on complex numbers; form the complex conjugate of any complex number and separate the real and imaginary parts of any complex expression; and

6. plan and carry out the solution of typical chemistry problems.

## 2.1 Algebraic Operations on Real Scalar Variables

Algebra is a branch of mathematics that was invented by Greek mathematicians and developed by Hindu, Arab, and European mathematicians. It was apparently the first branch of symbolic mathematics. Its great utility comes from the fact that letters are used to represent constants and variables and that operations are indicated by symbols such as +, -, ×, /, √, and so on. Operations can be carried out symbolically instead of numerically so that formulas and equations can be modified and simplified before numerical calculations are carried out. This ability allows calculations to be carried out that arithmetic cannot handle.

The numbers and variables on which we operate in this section are called real numbers and real variables, They do not include imaginary numbers such as the square root of -1, which we discuss later. They are also called scalars, to distinguish them from vectors, which have direction as well as magnitude. Real scalar numbers have magnitude, a specification of the size of the number, and sign, which can be positive or negative.

## Algebraic Manipulations

Algebra involves symbolic operations. You manipulate symbols instead of carrying out numerical operations. For example, you can symbolically divide an expression by some quantity by writing its symbol in a denominator. You can then cancel the symbol in the denominator against the same symbol in the numerator of the same fraction or carry out other operations. You can factor a polynomial expression and possibly cancel one or more of the factors against the same factors in a denominator. You can solve an equation by symbolically carrying out some set of operations on both sides of an equation, eventually isolating one of the symbols on one side of the equation. Remember that if one side of an equation is operated on by anything that changes its value, the same operation must be applied to the other side of the equation to keep a valid equation. Operations that do not change the value of an expression, such as factoring an expression, multiplying out factors, multiplying the numerator and denominator of a fraction by the same factor, and so on, can be done to one side of an equation without destroying its validity.

EXAMPLE 2.1 Write the following expression in a simpler form:

$$
A = \frac {(2 x + 5) (x + 3) - 2 x (x + 5) - 14}{x ^ {2} + 2 x + 1}.
$$

SOLUTION ▶ We multiply out the factors in the numerator and combine terms, factor the denominator, and cancel a common factor:

$$
A = \frac {2 x ^ {2} + 11 x + 15 - 2 x ^ {2} - 10 x - 14}{(x + 1) (x + 1)} = \frac {x + 1}{(x + 1) (x + 1)} = \frac {1}{x + 1}
$$

EXERCISE 2.1 ▶

Write the following expression in a simpler form:

$$
B = \frac {(x ^ {2} + 2 x) ^ {2} - x ^ {2} (x - 2) ^ {2} + 12 x ^ {4}}{6 x ^ {3} + 12 x ^ {4}}.
$$


The van der Waals equation of state provides a more nearly exact description of real gases than does the ideal gas equation. It is

$$
\left(P + \frac {n ^ {2} a}{V ^ {2}}\right) (V - n b) = n R T
$$

where P is the pressure, V is the volume, n is the amount of gas in moles, T is the absolute temperature, and R is the ideal gas constant (the same constant as in the ideal gas equation, equal to $8.3145 \, J K^{-1} \, mol^{-1}$ or $0.082061 \, atm \, K^{-1} \, mol^{-1}$ ). The symbols a and b represent parameters, which means that they are constants for a particular gas, but have different values for different gases.

EXERCISE 2.2 ▶ (a) Manipulate the van der Waals equation so that $V_{m}$ , defined as $V / n$ , occurs instead of $V$ and $n$ occurring separately.

(b) Manipulate the equation into an expression for $P$ in terms of $T$ and $V_{m}$ .

(c) Manipulate the equation into a cubic equation in $V_{m}$ . That is, make an expression with terms proportional to powers of $V_{m}$ up to $V_{m}^{3}$ .

Find the value of the expression

$$
\frac {3 (2 + 4) ^ {2} - 6 (7 + | - 17 |) ^ {3} + (\sqrt {37 - | - 1 |}) ^ {3}}{(1 + 2 ^ {2}) ^ {4} - (| - 7 | + 6 ^ {3}) ^ {2} + \sqrt {12 + | - 4 |}}.
$$

## 2.2 Trigonometric Functions

The ordinary trigonometric functions include the sine, the cosine, the tangent, the cotangent, the secant, and the cosecant. These are sometimes called the circular trigonometric functions to distinguish them from the hyperbolic trigonometric functions discussed briefly in the next section of this chapter.

The trigonometric functions can be defined geometrically as in Fig. 2.1, which shows two angles, $\alpha_{1}$ and $\alpha_{2}$ . Along the horizontal reference line drawn from the point E to the point D, the points $C_{1}$ and $C_{2}$ are chosen so that the triangles are right triangles (triangles with one right angle). In the right triangle $AB_{1}C_{1}$ , the radius r is called the hypotenuse, the vertical side of length $y_{1}$ is called the opposite side, and the horizontal side of length $x_{1}$ is called the adjacent side. We define the trigonometric functions sine, cosine, and tangent of $\alpha_{1}$ as follows:

$$
\sin \left(\alpha_ {1}\right) = \frac {y _ {1}}{r} \quad (\text { opposite   side   over   hypotenuse })\tag{2.1}
$$

$$
\boxed {\cos (\alpha_ {1}) = \frac {x _ {1}}{r} \quad (\text { adjacent   side   over   hypotenuse })}\tag{2.2}
$$

$$
\tan \left(\alpha_ {1}\right) = \frac {y _ {1}}{x _ {1}} \quad (\text { opposite   side   over   adjacent   side })\tag{2.3}
$$

$$
\cot \left(\alpha_ {1}\right) = \frac {x _ {1}}{y _ {1}} \quad (\text { adjacent   side   over   opposite   side })\tag{2.4}
$$

$$
\sec \left(\alpha_ {1}\right) = \frac {r}{x _ {1}} \quad (\text { hypotenuse   over   adjacent   side })\tag{2.5}
$$

$$
\csc \left(\alpha_ {1}\right) = \frac {r}{y _ {1}} \quad (\text { hypotenuse   over   opposite   side })\tag{2.6}
$$

![[213ebb36708129d95f3b365f9040d6951691febfcdcc639348921444b928f76d.jpg]]  
Figure 2.1 ▶ The figure used in defining trigonometric functions.

The trigonometric functions of the angle $\alpha_{2}$ are defined in the same way, except that as drawn in Fig. 2.1, the distance $x_{2}$ must be counted as negative, because the point $B_{2}$ is to the left of A. If the point $B_{2}$ were below A, then $y_{2}$ would also be counted as negative.

There are three common ways to specify the size of an angle (the “measure” of an angle). Degrees are defined so that a right angle corresponds to $90^{\circ}$ (90 degrees), and a full circle contains $360^{\circ}$ . The grad is defined so that 100 grad corresponds to a right angle and a full circle contains 400 grad. For most mathematical purposes, the best way to specify the size of an angle is with radians. The measure of an angle in radians is defined to be the length of the arc subtending the angle divided by the radius of the circle. In Fig. 2.1, the arc $DB_{1}$ subtends the angle $\alpha_{1}$ , so that in radians

$$
\alpha_ {1} = \frac {d _ {1}}{r},\tag{2.7}
$$

where $d_{1}$ is the length of the arc $DB_{1}$ . The full circle contains $2\pi$ radians ( $2\pi$ rad), and 1 radian corresponds to $360^{\circ}/(2\pi)=57.2957795\cdots^{\circ}$ . The right angle, $90^{\circ}$ , is $\pi/2$ radians = $1.5707963\cdots$ radians. We can express the angle $\alpha$ in terms of radians, degrees, or grad, but must understand which measure is being used. For example, we could write

$$
\sin (90 ^ {\circ}) = \sin (\pi / 2)\tag{2.8}
$$

This does not look like a correct equation until we understand that on the left-hand side the angle is measured in degrees and on the right-hand side the angle is measured in radians. If you use degrees, you should always include the degree sign (°).

The trigonometric functions are examples of mathematical functions. A mathematical function is a rule that provides a unique connection between the value of one variable, called the independent variable or the argument of the function, and another variable, which we call the dependent variable. When we choose a value for the independent variable, the function provides a corresponding value for the dependent variable. For example, if we write

$$
f (x) = \sin (x),\tag{2.9}
$$

then f is the dependent variable and x the independent variable. The trigonometric functions illustrate a general property of the functions that we deal with. They are single-valued: for each value of the angle $\alpha$ , there is one and only one value of the sine, one and only one value of the cosine, and so on. Mathematicians usually use the name “function” to apply only to single-valued functions. We will discuss mathematical functions in more detail in Chapter 4.

## Trigonometric Identities

There are a number of relations between trigonometric functions that are valid for all values of the given angles. Such relations are said to be identically true, or to be identities. We first present some identities involving an angle and its negative. A negative angle is measured in the clockwise direction while positive angles are measured in the counter-clockwise direction. A figure analogous to Fig. 2.1 with

a negative angle can be used to show that

$$
\sin (\alpha) = - \sin (- \alpha)\tag{2.10}
$$

$$
\cos (\alpha) = \cos (- \alpha)\tag{2.11}
$$

$$
\tan (\alpha) = - \tan (- \alpha)\tag{2.12}
$$

Equations (2.10) and (2.12) express the fact that the sine and the tangent are odd functions, and Eq. (2.11) expresses the fact that the cosine is an even function. If $f(x)$ is an odd function, then

$$
f (- x) = - f (x) \quad (\text { odd   function })\tag{2.13}
$$

If $f(x)$ is an even function, then

$$
f (- x) = f (x) \quad (\text { even   function })\tag{2.14}
$$

From Eqs. (2.1) through (2.6), we can deduce the additional identities:

$$
\cot (\alpha) = \frac {1}{\tan (\alpha)}\tag{2.15}
$$

$$
\boxed {\sec (\alpha) = \frac {1}{\cos (\alpha)}}\tag{2.16}
$$

$$
\csc (\alpha) = \frac {1}{\sin (\alpha)}\tag{2.17}
$$

Figure 2.1 also shows a third angle $\alpha_{3}$ , which is counted as negative. This angle has the same triangle, and therefore the same trigonometric functions as the positive angle $\alpha_{2}$ . Since $\alpha_{3}$ is equal to $-(2\pi - \alpha_{2})$ if the angles are measured in radians, we can write an identity

$$
\sin (\alpha_ {3}) = \sin [ - (2 \pi - \alpha_ {2}) ] = \sin (\alpha_ {2} - 2 \pi) = \sin (\alpha_ {2})\tag{2.18}
$$

with similar equations for the other trigonometric functions. This equation is related to the periodic behavior of trigonometric functions. If an angle is increased by $2\pi$ radians ( $360^{\circ}$ ), the new angle corresponds to the same triangle as does the old angle, and we can write

$$
\sin (\alpha) = \sin (\alpha + 2 \pi) = \sin (\alpha + 4 \pi) = \dots\tag{2.19}
$$

$$
\cos (\alpha) = \cos (\alpha + 2 \pi) = \cos (\alpha + 4 \pi) = \dots\tag{2.20}
$$

with similar equations for the other trigonometric functions. The trigonometric functions are periodic functions with period $2\pi$ . That is, if any integral multiple of $2\pi$ is added to the argument, the value of the function is unchanged.

EXERCISE 2.4 ▶ Using a calculator, find the value of the cosine of $15.5^{\circ}$ and the value of the cosine of $375.5^{\circ}$ . Display as many digits as your calculator is able to display. Check to see if there is any round-off error in the last digit. Choose another pair of angles that differ by $360^{\circ}$ and repeat the calculation. Set your calculator to use angles measured in radians. Find the value of $\sin(0.3000)$ . Find the value of $\sin(0.3000 + 2\pi)$ . See if there is any round-off error in the last digit.

A useful trigonometric identity corresponds to the famous theorem of Pythagoras. Pythagoras drew a figure with three squares such that one side of each square formed a side of the same right triangle. He then proved by geometry that the area of the square on the hypotenuse was equal to the sum of the areas of the squares on the other two sides. In terms of the quantities in Fig. 2.1

$$
\boxed {x ^ {2} + y ^ {2} = r ^ {2}}\tag{2.21}
$$

We divide both sides of this equation by $r^{2}$ and use Eqs. (2.1) and (2.2) to obtain the identity:

$$
[ \sin (\alpha) ] ^ {2} + [ \cos (\alpha) ] ^ {2} = \sin^ {2} (\alpha) + \cos^ {2} (\alpha) = 1.\tag{2.22}
$$

Notice the common notation for a power of a trigonometric function: the exponent is written after the symbol for the trigonometric function and before the parentheses enclosing the argument.

EXERCISE 2.5 ▶ Using a calculator, find the values of the sine and cosine of $49.5^{\circ}$ . Square the two values and add the results. See if there is any round-off error in your calculator. Choose another angle and repeat the calculation.

## Mathematical Limits and a Useful Approximation

Comparison of Eqs. (2.1) and (2.7) shows that for a fairly small angle, the sine of an angle and the measure of the angle in radians are approximately equal, since the sine differs from the measure of the angle only by having the opposite side in place of the arc length, which is approximately the same size. In fact,

$$
\lim _ {\alpha \rightarrow 0} \frac {\sin (\alpha)}{\alpha} = 1 \quad (\alpha \text { must   be   measured   in   radians }).\tag{2.23}
$$

The symbol on the left stands for a mathematical limit. In this case, the equation means that if we let the value of $\alpha$ become smaller and smaller until it becomes more and more nearly equal to zero, the ratio of $\sin(\alpha)$ to $\alpha$ becomes more and more nearly equal to unity. In some cases (but not in this case), there is a distinction between letting the variable draw closer in value to a constant value from the positive side or from the negative side. To indicate that $\alpha$ approaches zero from the positive side (takes on positive values closer and closer to zero), we would write

$$
\lim _ {\alpha \to 0 ^ {+}} \frac {\sin (\alpha)}{\alpha} = 1\tag{2.24}
$$

To indicate that $\alpha$ approaches zero from the negative side, we would write

$$
\lim _ {\alpha \to 0 ^ {-}} \frac {\sin (\alpha)}{\alpha} = 1\tag{2.25}
$$

In the present case, the limits in Eq. (2.24) and (2.25) are the same, and there is no need to specify which one is meant.

For fairly small angles, we write as an approximation

$$
\alpha \approx \sin (\alpha) \quad (\alpha \text {   must   be   measured   in   radians })\tag{2.26}
$$

where the angle $\alpha$ must be measured in radians. Since the adjacent side of a right triangle is nearly equal to the hypotenuse for small angles, we can also write

$$
\alpha \approx \tan (\alpha) \approx \sin (\alpha) \quad (\alpha \text { must   be   measured   in   radians })\tag{2.27}
$$

Equations (2.26) and (2.27) are valid for both positive and negative values of $\alpha$ . If you are satisfied with an accuracy of about 1%, you can use Eq. (2.27) for angles with magnitude up to about 0.2 radians (approximately 11°).

EXERCISE 2.6 For an angle that is nearly as large as $\pi/2$ , find an approximate equality similar to Eq. (2.27) involving $(\pi/2) - \alpha$ , $\cos(\alpha)$ , and $\cot(\alpha)$ .

## General Properties of Trigonometric Functions

To use trigonometric functions easily, you must have a clear mental picture of the way in which the sine, cosine, and tangent depend on their arguments. Figures 2.2, 2.3, and 2.4 show these functions.

The tangent has a complicated behavior, becoming larger without bound as its argument approaches $\pi/2$ from the left, and becoming more negative without bound as its argument approaches the same value from the right. We can write

$$
\begin{array}{r l} \lim _ {\alpha \to \frac {\pi}{2} ^ {+}} [ \tan (\alpha) ] & = - \infty \\ \lim _ {\alpha \to \frac {\pi}{2} ^ {-}} [ \tan (\alpha) ] & = \infty . \end{array}
$$

![[45f67aeca1899fd62a0f5bee5b17246cd30764d4a1ebf202d16a010c83e5eed2.jpg]]  
Figure 2.2 ▶ The sine of an angle α.

![[a206ef50645fe2ae8b4d96effb13cb9894b4ac9af7fecb1e9dd94267b66425ba.jpg]]  
Figure 2.3 ▶ The cosine of an angle α.

![[4b9d8da01a7d3a97d92272d541d8df2f8dc869dae79dbda5930d5011c78073b6.jpg]]  
Figure 2.4 ▶ The tangent of an angle α.

In these equations, the superscript + on the $\pi/2$ in the limit means that the value of $\alpha$ approaches $\pi/2$ from the right. That is, $\alpha$ is greater than $\pi/2$ as it becomes more and more nearly equal to $\pi/2$ . The – superscript in the limit means that $\alpha$ approaches $\pi/2$ from the left. The symbol $\infty$ stands for infinity, which is larger than any number that you or anyone else can name. This quantity is sometimes called “undefined.”

## 2.3 Inverse Trigonometric Functions

It is possible to think of trigonometric functions as defining a mathematical function in an inverse way. For example, if

$$
y = \sin (x)\tag{2.28}
$$

we can define a function to give a value for x as a function of y. We write

$$
x = \arcsin (y).\tag{2.29}
$$

This can be read as “x is the angle whose sine is y.” The arcsine function is also called the inverse sine function, and another notation is also common:

$$
x = \sin^ {- 1} (y).\tag{2.30}
$$

The -1 superscript indicates an inverse function. It is not an exponent, even though exponents are written in the same position. If you need to write the reciprocal of $\sin(y)$ , you should write $[\sin(y)]^{-1}$ to avoid confusion. It is probably better to use the notation of Eq. (2.29) rather than that of Eq. (2.30) to avoid confusion.

From Fig. 2.2, you can see that there are many angles that have the same value of the sine function. In order to make the arcsine in Eq. (2.29) or Eq. (2.30) into a single-valued function, we must restrict the values of x that we consider. With the arcsine function, these values are taken from $-\pi/2$ to $+\pi/2$ and are called the principal values of the arcsine function. The other inverse trigonometric functions such as the inverse cosine and inverse tangent are defined in the same way as the arcsine function, and must also have principal values defined. The principal values of the arctangent and arccosecant functions range from $-\pi/2$ to $+\pi/2$ , the same as with the arcsine. The principal values of the arccosine, arccotangent, and arcsecant are taken from 0 to $\pi$ .

EXERCISE 2.7 ▶ Sketch graphs of the arcsine function, the arccosine function, and the arctangent function. Include only the principal values.

## Hyperbolic Trigonometric Functions

These functions are closely related to the exponential function. The hyperbolic sine of $x$ is denoted by $\sinh(x)$ , and defined by

$$
\sinh (x) = \frac {1}{2} \left(e ^ {x} - e ^ {- x}\right).\tag{2.31}
$$

The hyperbolic cosine is denoted by $\cosh(x)$ , and defined by

$$
\cosh (x) = \frac {1}{2} \left(e ^ {x} + e ^ {- x}\right).\tag{2.32}
$$

The other hyperbolic trigonometric functions are the hyperbolic tangent, denoted by $\tanh(x)$ ; the hyperbolic cotangent, denoted by $\coth(x)$ ; the hyperbolic secant, denoted by $\operatorname{sech}(x)$ ; and the hyperbolic cosecant, denoted by $\operatorname{csch}(x)$ . These functions are given by the equations

$$
\tanh (x) = \frac {\sinh (x)}{\cosh (x)}\tag{2.33}
$$

$$
\coth (x) = \frac {1}{\tanh (x)}\tag{2.34}
$$

$$
\operatorname{sech} (x) = \frac {1}{\cosh (x)}\tag{2.35}
$$

$$
\operatorname{csch} (x) = \frac {1}{\sinh (x)}\tag{2.36}
$$

![[a4d19e6eb632a04ffbd23861fbaa93b6d074ee428f1fb29c43771e08678066bc.jpg]]  
Figure 2.5 ▶ The hyperbolic sine and cosine.

Figure 2.5 shows the hyperbolic sine and hyperbolic cosine for values of x from 0 to 3. Note that the values of the hyperbolic sin and the hyperbolic cosine do not necessarily lie between -1 and 1 as do the values of the circular sine and cosine functions and that both functions approach $e^{x}/2$ for large values of x.

EXERCISE 2.8 ▶ Make a graph of tanh(x) and coth(x) on the same graph for values of x ranging from 0 to 3.

EXERCISE 2.9 ▶ Find the value of each of the hyperbolic trigonometric functions for x = 0 and $x = \pi/2$ . Compare these values with the values of the ordinary (circular) trigonometric functions for the same values of the independent variable.

## 2.4 Vectors and Coordinate Systems

Quantities that have both magnitude and direction are called vectors. For example, the position of an object can be represented by a vector, since the position can be specified by giving the distance and the direction from a reference point (an origin). A force is also a vector, since it is not completely specified until its magnitude and direction are both given. Some other vectors that are important in physical chemistry are the dipole moments of molecules, magnetic and electric fields, angular momenta, and magnetic dipoles.

We will use a boldface letter to represent a vector. For example, the force on an object is denoted by F. When you are writing by hand, there is no easy way to write boldface letters, so you can use a letter with an arrow over it (e.g., $\vec{F}$ ) or you can use a wavy underscore (e.g., $\widetilde{F}$ ), which is the typesetter's symbol for boldface type.

![[9c3c92c858082537d11bf9ea0bf42d067a78ff33c4bb378ad8872eb1110e3f5a.jpg]]  
Figure 2.6 ▶ A position vector, $\rho$ , in a plane, with plane polar coordinates and Cartesian coordinates.

## Vectors in Two Dimensions

Two-dimensional vectors include position vectors of objects that remain on a flat surface. We represent this physical surface by a mathematical plane, which is a map of the surface so that each location in the physical surface corresponds to a point of the mathematical plane. We choose some point as an origin and pick some line passing through the origin as our x axis. One end of this axis is designated as the positive end. The line passing through the origin perpendicular to the x axis is our y axis, and the end that is counterclockwise $90^{\circ}$ from the positive end of the y axis is its positive end. These axes are shown in Fig. 2.6. In this figure, the origin is labeled as point O, and the location of some object is labeled as point P.

The directed line segment beginning at O and ending at P is the position vector of the object. We denote the position vector in two dimensions by the boldface Greek letter $\rho$ . In the figure, we draw an arrowhead on the directed line segment to make its direction clear.

The negative of a given vector is a vector of the same length directed in the opposite direction. A vector and its negative have the same magnitude, as do all the vectors of the same length pointing in any other directions. The magnitude of $\rho$ is denoted $|\rho|$ or by $\rho$ . It is a nonnegative quantity equal to the length of the vector $\rho$ . One way to specify the location of the point P is to give the magnitude of $\rho$ and the value of the angle $\phi$ between the positive end of the x axis and $\rho$ , measured counterclockwise from the axis. The variables $\rho$ and $\phi$ are called the plane polar coordinates of the point P. If we allow $\rho$ to range from zero to $\infty$ and allow $\phi$ to range from 0 to $2\pi$ radians, we can specify the location of any point in the plane.

There is another common way to specify the location of P. We draw two line segments from P perpendicular to the axes, as shown in Fig. 2.6. The distance from the origin to the intersection on the x axis is called x and is considered to be positive if the intersection is on the positive half of the axis, and negative if the intersection is on the negative half of the axis. The distance from the origin to the intersection on the y axis is called y, and its sign is assigned in a similar way. The variables x and y are the Cartesian coordinates of $P^{1}$ . The point P can be designated by its Cartesian coordinates within parentheses, as $(x, y)$ . The values of x and y are also called the Cartesian components of the position vector.

Changing from plane polar coordinates to Cartesian coordinates is an example of transformation of coordinates, and can be done by using the equations

$$
x = \rho \cos (\phi)
$$

$$
y = \rho \sin (\phi)\tag{2.37}
$$

(2.38)

EXERCISE 2.10 ▶ Show that Eqs. (2.37) and (2.38) are correct.

The coordinate transformation in the other direction is also possible. From the theorem of Pythagorus, Eq. (2.21),

$$
\rho = \sqrt {x ^ {2} + y ^ {2}}.\tag{2.39}
$$

From the definition of the tangent function, Eq. (2.3),

$$
\phi = \arctan \left(\frac {y}{x}\right).\tag{2.40}
$$

However, since we want $\phi$ to range from 0 to $2\pi$ radians, we must specify this range for the inverse tangent function, instead of using the principal value. If we are using a calculator that is programmed to deliver the principal value, we must decide in advance which quadrant $\phi$ lies in and be prepared to add $\pi$ or $2\pi$ to the calculator result if it lies in the wrong quadrant.

$$
\begin{array}{l} \text { EXERCISE   2.11 } \\ \text {(a) Find x and y if \rho = 6 and \phi = \pi / 6 radians.} \\ \text {(b) Find \rho and \phi if x = 5 and y = 10.} \end{array}
$$

A position vector is only one example of a vector. Anything, such as a force, a velocity, or an acceleration, which has magnitude and direction, is a vector. Figure 2.6 is a map of physical space, and a distance in such a diagram is measured in units of length, such as meters. Other kinds of vectors can also be represented on vector diagrams by directed line segments. However, such a diagram is not a map of physical space, and the length of a line segment representing a vector will represent the magnitude of a force, or the magnitude of a velocity, or something else. Position vectors ordinarily remain with their tails at the origin, but since other vector diagrams do not necessarily represent a physical (geographical) space, we will consider a vector to be unchanged if it is moved from one place in a vector diagram to another, as long as its length and its direction do not change.

## Vector Algebra in Two Dimensions

Figure 2.7 is a vector diagram in which two vectors, A and B, are shown. The sum of the two vectors is obtained as follows: (1) Move the second vector so that its tail coincides with the head of the first. (2) Draw the sum vector from the tail of the first vector to the head of the second. The addition of vectors is commutative: $A + B$ is the same as $B + A$ .

![[120290bdff4428775e3919e5a549f5160ce18799ae7a4b1f157e59a0bb82998a.jpg]]  
Figure 2.7 ▶ Two vectors and their sum.

The components of A and B are defined in the same way as the components of the position vector in Fig. 2.6. The x components are called $A_{x}$ and $B_{x}$ , and the y components are called $A_{y}$ and $B_{y}$ . We can denote the vector A by its component in x, y order inside parentheses, as $(A_{x}, A_{y})$ Vector addition can be performed using the components of the vectors. If the sum of A and B is called C,

$$
\mathbf {C} = \mathbf {A} + \mathbf {B}\tag{2.41}
$$

$$
C _ {x} = A _ {x} + B _ {x}
$$

$$
C _ {y} = A _ {y} + B _ {y}.\tag{2.42}
$$

(2.43)

EXAMPLE 2.2 Find the sum of the two vectors (2.5, 3) and (3.1, 4).

SOLUTION ▶ A + B = (5, 6, 7)

The difference of two vectors is the sum of the first vector and the negative of the second. The negative of B is denoted by -B and is the vector with components $-B_{x}$ and $-B_{y}$ . If the vector A - B is called D,

$$
\mathbf {D} = \mathbf {A} - \mathbf {B}\tag{2.44}
$$

$$
D _ {x} = A _ {x} - B _ {x}\tag{2.45}
$$

$$
D _ {y} = A _ {y} - B _ {y}.\tag{2.46}
$$

If the tail of the vector -B is placed at the head of the vector A, the vector D = A - B has its tail at the tail of A and its head at the head of -B. The difference D = A - B can also be represented by placing the tails of both A and B at the same place and drawing the vector D with its tail at the head of B and its head at the head of A.

EXERCISE 2.12 ▶ Draw vector diagrams and convince yourself that the two schemes presented for the construction of D = A - B give the same result.

![[e54e50d4ac04a20e18f7a6a55a2bb422abb9e19107d1d3ec51dd7bb84bdef6fc.jpg]]

If A is a vector and a is a scalar, the product of the scalar and the vector aA has the components

$$
(a A) _ {x} = a A _ {x}\tag{2.47}
$$

$$
(a A) _ {y} = a A _ {y}\tag{2.48}
$$

If a is a positive scalar, the vector aA points in the same direction as A, and if a is a negative scalar, the vector aA points in the opposite direction. The magnitude of aA is equal to $|a|$ $|A| = |a|A$ .

The magnitude of a vector A in two dimensions is denoted by A or by $|A|$ . It is obtained in the same manner as the magnitude of a position vector:

$$
A = | \mathbf {A} | = \sqrt {A _ {x} ^ {2} + A _ {y} ^ {2}}\tag{2.49}
$$

EXERCISE 2.13 ▶ The vector A has the components $A_{x}=2$ , $A_{y}=3$ . The vector B has the components $B_{x}=3$ , $B_{y}=4$ . (a) Find $|A|$ and $|B|$ . (b) Find the components and the magnitude of $A+B$ . (c) Find the components and the magnitude of A-B. (d) Find the components and the magnitude of 2A-B.

We next define the scalar product of two vectors, which is also called the dot product because of the use of a dot to represent the operation. If A and B are two vectors, and $\alpha$ is the angle between them, their scalar product is denoted by $A \cdot B$ and given by

$$
\mathbf {A} \cdot \mathbf {B} = | \mathbf {A} | | \mathbf {B} | \cos (\alpha).\tag{2.50}
$$

The result is a scalar, as the name implies.

## EXERCISE 2.14 ▶

(a) Let $|\mathbf{A}| = 4.5$ , $|\mathbf{B}| = 6.0$ , and let the angle between them equal $30.0^\circ$ . Find $\mathbf{A} \cdot \mathbf{B}$ .

(b) Let $|\mathbf{A}| = 4.0$ , $|\mathbf{B}| = 2.0$ , and let the angle between them equal $45.0^\circ$ . Find $\mathbf{A} \cdot \mathbf{B}$ .

The following are properties of the scalar product:

1. If $\mathbf{A}$ and $\mathbf{B}$ are parallel, $\mathbf{A} \cdot \mathbf{B}$ is the product of the magnitudes of $\mathbf{A}$ and $\mathbf{B}$ .

2. The scalar product of A with itself is the square of the magnitude of A:

$$
\mathbf {A} \cdot \mathbf {A} = \left| \mathbf {A} ^ {2} \right| = \left| A ^ {2} \right| = A ^ {2} = A _ {x} ^ {2} + A _ {y} ^ {2}.
$$

3. If A and B are perpendicular to each other, $A \cdot B = 0$ . Such vectors are said to be orthogonal to each other.

4. If A and B point in opposite directions (are antiparallel), $A \cdot B$ is the negative of the product of the magnitudes of A and B.

A convenient way to represent vectors is by using unit vectors. We define i to be a vector of unit length pointing in the direction of the positive end of the x axis, and j to be a vector of unit length pointing in the direction of the positive end of the y axis. These are shown in Fig. 2.8.

![[baa64fb3dae8b7fc497a3488aacee85a5e8a056a282f9bbea973d7f559917bc4.jpg]]  
Figure 2.8 ▶ A vector in terms of the unit vectors i and j.

A vector $\mathbf{A}$ is represented as

$$
\mathbf {A} = \mathrm{i} A _ {x} + \mathrm{j} A _ {y}.\tag{2.51}
$$

The first term on the right-hand side of this equation is a product of the component $A_{x}$ and a vector i, so it is a vector of length $A_{x}$ pointing along the x axis, as shown in Fig. 2.8. The other term is similarly a vector of length $A_{y}$ pointing along the y axis. The vector A is the vector sum shown in Fig. 2.8. A similar equation can be written for another vector, B:

$$
\mathbf {B} = \mathbf {i} B _ {x} + \mathbf {j} B _ {y}.\tag{2.52}
$$

The scalar product $\mathbf{A} \cdot \mathbf{B}$ can be written

$$
\begin{array}{r l} \mathbf {A} \cdot \mathbf {B} & = (\mathbf {i} A _ {x} + \mathbf {j} A _ {y}) \cdot (\mathbf {i} B _ {x} + \mathbf {j} B _ {y}) \\ & = \mathbf {i} \cdot \mathbf {i} A _ {x} B _ {x} + \mathbf {i} \cdot \mathbf {j} A _ {x} B _ {y} + \mathbf {j} \cdot \mathbf {i} A _ {y} B _ {x} + \mathbf {j} \cdot \mathbf {j} A _ {y} B _ {y}. \end{array}
$$

From the definitions of i and j and the definition of the scalar product,

$$
\mathbf {i} \cdot \mathbf {i} = \mathbf {j} \cdot \mathbf {j} = 1\tag{2.53}
$$

$$
\mathbf {i} \cdot \mathbf {j} = \mathbf {j} \cdot \mathbf {i} = 0\tag{2.54}
$$

so that

$$
\mathbf {A} \cdot \mathbf {B} = A _ {x} B _ {x} + A _ {y} B _ {y}\tag{2.55}
$$

EXAMPLE 2.3 Consider the following vectors: A = 2.5i + 4j and B = 3i - 5j.

(a) Find $\mathbf{A} \cdot \mathbf{B}$ .

(b) Find $|A|$ and $|B|$ and use them to find the angle between A and B.

SOLUTION ▶ A·B = (2.5)(3) + (4)(-5) = 7.5 - 20 = -12.5.

$$
| \mathbf {A} | = (6.25 + 16) ^ {1 / 2} = (22.25) ^ {1 / 2} = 4.717 \dots
$$

$$
| \mathbf {B} | = (9 + 25) ^ {1 / 2} = (34) ^ {1 / 2} = 5.8309 \dots
$$

$$
\begin{array}{r l} \cos (\alpha) & = \frac {\mathbf {A} \cdot \mathbf {B}}{| \mathbf {A} | | \mathbf {B} |} = \frac {- 12 .5}{(4 .717) (5 .831)} = - 0.4545 \\ \alpha & = \arccos (- 0.4545) = 2.043 \mathrm{rad} = 117.0 ^ {\circ} \end{array}
$$

EXERCISE 2.15 ▶ Consider two vectors A = (3.00)i - (4.00)j and B = (1.00)i + (2.00)j.

(a) Draw a vector diagram of the two vectors.

(b) Find $\mathbf{A} \cdot \mathbf{B}$ and (2A) $\cdot$ (3B).

(c) Find the magnitude of $\mathbf{A} \cdot \mathbf{B}$ .

(d) Find the angle between A and B. Use the principal value of the arccosine,

so that an angle of less than $\pi$ radians (180°) results.

## Vectors and Coordinate Systems in Three Dimensions

Figure 2.9 depicts the three-dimensional version of Cartesian coordinates. We define the x and y axes as before, and erect the z axis through the origin and perpendicular to the x and y axes.

The axes are viewed from the first octant, lying between the positive ends of the x, y, and z axes. The octants are numbered from 1 to 8, beginning with the first octant in the upper front right part of the coordinate system and moving counterclockwise around the upper part, and then moving to the lower front right part (octant 5) and moving counterclockwise around the bottom part. A coordinate system such as that shown is called a right-handed coordinate system. For such a system, the thumb, index finger, and middle finger of the right hand can be aligned with the positive ends of the x, y, and z axes, respectively. If the left hand must be used for such an alignment, the coordinate system is called a left-handed coordinate system.

The location of the point P is specified by x, y, and z, which are the Cartesian coordinates of the point. These are the distances from the origin to the points on the axes reached by moving perpendicularly from P to each axis. These coordinates can be positive or negative. In the first octant, x, y, and z are all positive. In the second octant, x is negative, but y and z are positive. The point P can be denoted by its coordinates, as $(x, y, z)$ . The directed line segment from the origin to P is the position vector of P, and is denoted by r. The Cartesian coordinates x, y, and z are also called the Cartesian components of r. A vector can be represented by the list of its components inside parentheses so that the position vector is denoted by $(x, y, z)$ and the vector A can be denoted by $(A_{x}, A_{y}, A_{z})$ .

![[5a691bec9f71930b71c8b414b02fb15e9a980f8845bca32aacad081a1c54e1a9.jpg]]  
Figure 2.9 ▶ Cartesian coordinates in three dimensions.

![[a53d72779c4a3c5a60f095989550a675654288105a16538235f9c5a8a1aadee0.jpg]]  
Figure 2.10 ▶ A position vector in terms of the unit vectors i, j, and k.

We can represent a three-dimensional vector by the use of unit vectors as we did in two dimensions. In addition to the unit vectors i and j in the x and y directions, we define k, a vector of unit length pointing in the direction of the positive end of the z axis. Figure 2.10 shows these unit vectors and the position vector written as

$$
\mathbf {r} = \mathbf {i} x + \mathbf {j} y + \mathbf {k} z.\tag{2.56}
$$

The magnitude of r of the vector r can be obtained from the theorem of Pythagoras. In Fig. 2.10 you can see that r is the hypotenuse of a right triangle with sides $\rho$ and z, where $\rho = \sqrt{x^{2} + y^{2}}$ so that the square of the magnitude of r is given by a three-dimensional version of the theorem of Pythagoras:

$$
\boxed {r ^ {2} = \rho^ {2} + z ^ {2} = x ^ {2} + y ^ {2} + z ^ {2}}\tag{2.57}
$$

or

$$
\boxed {r = | \mathbf {r} | = \sqrt {x ^ {2} + y ^ {2} + z ^ {2}}}.\tag{2.58}
$$

The magnitude of any vector is analogous to the magnitude of the position vector. If $\mathbf{A}$ is a vector with Cartesian components $A_{x}, A_{y}$ , and $A_{z}$ , the magnitude of $\mathbf{A}$ is given by

$$
\left| \mathbf {A} \right| = A = \left(A _ {x} ^ {2} + A _ {y} ^ {2} + A _ {z} ^ {2}\right) ^ {1 / 2} = \sqrt {A _ {x} ^ {2} + A _ {y} ^ {2} + A _ {z} ^ {2}}.\tag{2.59}
$$

EXAMPLE 2.4 Find the magnitude of the vector A = (3.00, 4.00, 5.00).

![[e3d5ac29137a900751443a8c0106337650d562263ece6e0c57992b1905f98797.jpg]]  
Figure 2.11 ▶ Spherical polar coordinates.

$$
\text { SOLUTION } \blacktriangleright A = \sqrt {3 .00 ^ {2} + 4 .00 ^ {2} + 5 .00 ^ {2}} = \sqrt {50 .00} = 7.07
$$

Figure 2.11 shows the way in which spherical polar coordinates are used to specify the location of the point P and the vector r from the origin to P. The vector $\rho$ in the x-y plane is also shown. The vector $\rho$ is called the projection of r into the x-y plane. Its head is reached from the head of r by moving to the x-y plane in a direction perpendicular to the plane. The three spherical polar coordinates are r, $\theta$ , and $\phi$ . The coordinate r is the magnitude of the vector r as in Eq. (2.58), $\theta$ is the angle between the positive z axis and the position vector r, and $\phi$ is the angle between the positive x axis and the vector $\rho$ , as in two-dimensional polar coordinates. The angle $\theta$ is allowed to range from 0 to $\pi$ and the angle $\phi$ is allowed to range from 0 to $2\pi$ . The distance r is allowed to range from 0 to $\infty$ , and these ranges allow the location of every point in the three-dimensional space to be given.

The following equations and Eq. (2.58) can be used to transform from Cartesian coordinates to spherical polar coordinates:

$$
\boxed {\theta = \arccos \left(\frac {z}{r}\right)}\tag{2.60}
$$

and

$$
\boxed {\phi = \arctan \left(\frac {y}{x}\right).}\tag{2.61}
$$

Equation (2.61) is the same as Eq. (2.40).

The following equations can be used to transform from spherical polar coordinates to Cartesian coordinates:

$$
x = r \sin (\theta) \cos (\phi)\tag{2.62}
$$

$$
y = r \sin (\theta) \sin (\phi)\tag{2.63}
$$

$$
\boxed {z = r \cos (\theta)}\tag{2.64}
$$

EXAMPLE 2.5 Find the spherical polar coordinates of the point whose Cartesian coordinates are (1.000, 1.000, 1.000).

## SOLUTION ▶

$$
r = \sqrt {(1 .000) ^ {2} - (1 .000) ^ {2} - (1 .000) ^ {2}} = \sqrt {3 .000} = 1.732
$$

$$
\phi = \arctan \left(\frac {1 .000}{1 .000}\right) = \frac {\pi}{4} \mathrm{rad} = 45 ^ {\circ}
$$

$$
\theta = \arccos \left(\frac {1 .000}{1 .732}\right) = 0.955 \mathrm{rad} = 54.7 ^ {\circ}
$$

EXERCISE 2.16 ▶ Find the spherical polar coordinates of the point whose Cartesian coordinates are (2, 3, 4).

The cylindrical polar coordinate system is another three-dimensional coordinate system. It uses the variables $\rho$ , $\phi$ , and z, already defined and shown in Fig. 2.11. The equations needed to transform from Cartesian coordinates to cylindrical polar coordinates are Eqs. (2.39) and (2.40). The third coordinate, z, is the same in both Cartesian and cylindrical polar coordinates. Equations (2.37) and (2.38) are used for the reverse transformation.

EXAMPLE 2.6 Find the cylindrical polar coordinates of the point whose Cartesian coordinates are (1.000, -4.000, -2.000).

## SOLUTION ▶

$$
\begin{array}{l l} \rho & = \sqrt {(1 .000) ^ {2} + (4 .000) ^ {2}} = \sqrt {17 .000} = 4.123 \\ \phi & = \arctan \left(\frac {- 4 .000}{1 .000}\right) = 4.957 \text { radians } = 284 ^ {\circ} \\ z & = - 2.000. \end{array}
$$

EXERCISE 2.17 ▶ (a) Find the Cartesian coordinates of the point whose cylindrical polar coordinates are $\rho = 25.00$ , $\phi = 60.0^{\circ}$ , $z = 17.50$

(b) Find the cylindrical polar coordinates of the point whose Cartesian coordinates are $(-2.000, -2.000, 3.000)$ .

The magnitude of the position vector in cylindrical polar coordinates is given by

$$
r = \left(\rho^ {2} + z ^ {2}\right) ^ {1 / 2}\tag{2.65}
$$

EXAMPLE 2.7 Find the spherical polar coordinates of the points whose cylindrical polar coordinates are ( $\rho = 10.00, \phi = 45.00^{\circ}, z = 15.00$ )

SOLUTION ▶ $r = \sqrt{10.00^{2} + 15.00^{2}} = \sqrt{325.00} = 18.03, \theta = \arccos(\frac{15.00}{18.03}) = \arccos(0.83205) = 33.69^{\circ}, \phi = 45.00^{\circ}$

## Vector Algebra in Three Dimensions

The sum of two vectors are similar to the sum in two dimensions. Let A and B be two vectors, represented in terms of their components and the unit vectors i, j, and k by

$$
\mathbf {A} = \mathbf {i} A _ {x} + \mathbf {j} A _ {y} + \mathbf {k} A _ {z}\tag{2.66a}
$$

$$
\mathbf {B} = \mathbf {i} B _ {x} + \mathbf {j} B _ {y} + \mathbf {k} B _ {z}.\tag{2.66b}
$$

The sum is still obtained by placing the tail of the second vector at the head of the first and drawing the sum vector from the tail of the first to the head of the second. If C is the sum of A and B, then

$$
\boxed { \begin{array}{c} \mathbf {C} = \mathbf {A} + \mathbf {B} \\ C _ {x} = A _ {x} + B _ {x} \\ C _ {y} = A _ {y} + B _ {y} \\ C _ {z} = A _ {z} + B _ {z} \end{array} }.\tag{2.67}
$$

There are three kinds of products involving vectors. The product of a vector $\mathbf{A}$ and a scalar $a$ is

$$
\boxed {\mathbf {C} = a \mathbf {A} = \mathbf {i} a A _ {x} + \mathbf {j} a A _ {y} + \mathbf {k} a A _ {z}.}\tag{2.68}
$$

The scalar product of two vectors is still given by

$$
\mathbf {A} \cdot \mathbf {B} = | \mathbf {A} | | \mathbf {B} | \cos (\alpha)\tag{2.69}
$$

where $\alpha$ is the angle between the vectors.

Analogous to Eq. (2.55), we have

$$
\boxed {\mathbf {A} \cdot \mathbf {B} = A _ {x} B _ {x} + A _ {y} B _ {y} + A _ {z} B _ {z}}.\tag{2.70}
$$

EXAMPLE 2.8 Let $A = 2i + 3j + 7k$ and $B = 7i + 2j + 3k$ . Find $A \cdot B$ and the angle between A and B. Find (3A) $\cdot$ B.

SOLUTION ▶

$$
\mathbf {A} \cdot \mathbf {B} = 14 + 6 + 21 = 41
$$

The magnitude of $\mathbf{A}$ is

$$
| \mathbf {A} | = A = (2 ^ {2} + 3 ^ {2} + 7 ^ {2}) ^ {1 / 2} = \sqrt {62}\tag{2.71}
$$

The magnitude of B happens to be the same. Let $\alpha$ be the angle between the vectors A and B.

$$
\begin{array}{r l} \alpha & = \arccos \left(\frac {\mathbf {A} \cdot \mathbf {B}}{| \mathbf {A} | | \mathbf {B} |}\right) \\ & = \arccos \left(\frac {41}{\sqrt {62} \sqrt {62}}\right) = \arccos (0.6613) = 0.848 \mathrm{rad} = 48.6 ^ {\circ} \end{array}
$$

$$
(3 \mathbf {A}) \cdot \mathbf {B} = 3 \times 14 + 3 \times 6 + 3 \times 21 = \mathbf {A} \cdot \mathbf {B} = 4 \times 41 = 123.
$$

Notice that $(3\mathbf{A})\cdot \mathbf{B} = 3(\mathbf{A}\cdot \mathbf{B})$

EXERCISE 2.18 ▶ Find the cartesian components of the position vector of the point whose spherical polar coordinates are $r=2, \theta=90^{\circ}, \phi=0^{\circ}$ . Call this vector A.

(a) Find the scalar product of the vector $\mathbf{A}$ from part a and the vector $\mathbf{B}$ whose cartesian components are (1, 2, 3).

(b) Find the angle between these two vectors.


We now introduce another kind of a product between two vectors, called the vector product or cross product, and denoted by $A \times B$ . If

$$
\mathbf {C} = \mathbf {A} \times \mathbf {B}
$$

then $\mathbf{C}$ is defined to be perpendicular to the plane containing $\mathbf{A}$ and $\mathbf{B}$ and to have the magnitude

$$
C = | \mathbf {C} | = | \mathbf {A} | | \mathbf {B} | \sin (\alpha),\tag{2.72}
$$

where $\alpha$ is the angle between A and B, measured so that it lies between 0 and 180°. The direction of the cross product $A \times B$ is defined as follows: If the first vector listed is rotated through the angle $\alpha$ so that its direction coincides with that of B, then C points in the direction that an ordinary (right-handed) screw thread would move with this rotation. Another rule to obtain the direction is a right-hand rule. If the thumb of the right hand points in the direction of the first vector and the index finger points in the direction of the second vector, the middle finger can point in the direction of their cross product.

EXERCISE 2.19 ▶

From the geometrical definition just given, show that

$$
\boxed {\mathbf {A} \times \mathbf {B} = - \mathbf {B} \times \mathbf {A}.}\tag{2.73}
$$

In this exercise you have shown that the vector product of two vectors is not commutative, which means that you get a different result if you switch the order of the two factors.

From Eq. (2.72),

$$
\boxed {\mathbf {A} \times \mathbf {A} = \mathbf {0}}.\tag{2.74}
$$

where 0 is the null vector. The null vector has zero magnitude and no particular direction. To express the cross product in terms of components, we can use the

definition of the vector product to write

$$
\mathbf {i} \times \mathbf {i} = \mathbf {j} \times \mathbf {j} = \mathbf {k} \times \mathbf {k} = 0\tag{2.75a}
$$

and

$$
\mathbf {i} \times \mathbf {j} = \mathbf {k}\tag{2.75b}
$$

$$
\mathbf {j} \times \mathbf {i} = - \mathbf {k}\tag{2.75c}
$$

$$
\mathbf {i} \times \mathbf {k} = - \mathbf {j}\tag{2.75d}
$$

$$
\mathbf {k} \times \mathbf {i} = \mathbf {j}\tag{2.75e}
$$

$$
\mathbf {j} \times \mathbf {k} = \mathbf {i}\tag{2.75f}
$$

$$
\mathbf {k} \times \mathbf {j} = - \mathbf {i}.\tag{2.75g}
$$

By use of these relations, we obtain

$$
\mathbf {C} = \mathbf {A} \times \mathbf {B}
$$

$$
\begin{array}{r l} \mathbf {C} & = \mathbf {i} C _ {x} + \mathbf {j} C _ {y} + \mathbf {k} C _ {z} \\ & = \mathbf {i} (A _ {y} B _ {z} - A _ {z} B _ {y}) + \mathbf {j} (A _ {z} B _ {x} - A _ {x} B _ {z}) + \mathbf {k} (A _ {x} B _ {y} - A _ {y} B _ {x}) \end{array}\tag{2.76}
$$

EXERCISE 2.20 ▶

Show that Eq. (2.76) follows from Eq. (2.75).

EXAMPLE 2.9 Find the cross product $\mathbf{A} \times \mathbf{B}$ , where $\mathbf{A} = (1, 2, 3)$ and $\mathbf{B} = (1, 1, 1)$ .

SOLUTION ▶ Let C = A × B.

$$
\mathbf {C} = \mathbf {i} (2 - 3) + \mathbf {j} (3 - 1) + \mathbf {k} (1 - 2) = - \mathbf {i} + 2 \mathbf {j} - \mathbf {k}.
$$

EXAMPLE 2.10 Show that the vector C obtained in the previous example is perpendicular to A.

SOLUTION ▶ We do this by showing that $A \cdot C = 0$ .

$$
\begin{array}{r l} \mathbf {A} \cdot \mathbf {C} & = A _ {x} C _ {x} + A _ {y} C _ {y} + A _ {z} C _ {z} \\ & = - 1 + 4 + 3 = 0. \end{array}
$$

EXERCISE 2.21 ▶ Show that the vector C is perpendicular to B, and that Eq. (2.72) is satisfied. Do this by finding the angle between A and B through calculation of A · B.

An example of a vector product is the force on a moving charged particle due to a magnetic field. If q is the charge on the particle measured in coulombs (C), v is the velocity of the particle in meters per second, and B is the magnetic induction (often called the “magnetic field”) measured in tesla (T), $^{2}$ the force in newtons is given by

$$
\mathbf {F} = q \mathbf {v} \times \mathbf {B}.\tag{2.77}
$$

Since this force is perpendicular to the velocity, it causes the trajectory of the particle to curve, rather than changing the speed of the particle.

EXAMPLE 2.11 Find the force on an electron in a magnetic field if $\mathbf{v} = \mathbf{i}(1.000 \times 10^{5} \mathrm{~ms}^{-1})$ and $\mathbf{B} = \mathbf{j}(1.000 \times 10^{-4} \mathrm{T})$ .

SOLUTION ▶ The value of q is $-1.602 \times 10^{-19}$ C (note the negative sign).

$$
\begin{array}{r l} \mathbf {F} & = (\mathbf {i} \times \mathbf {j}) (- 1.602 \times 10 ^ {- 19} \mathrm{C}) (1.000 \times 10 ^ {5} \mathrm{ms} ^ {- 1}) (1.000 \times 10 ^ {- 4} \mathrm{T}) \\ & = - \mathbf {k} (1.602 \times 10 ^ {- 18} \mathrm{Asms} ^ {- 1} \mathrm{kgs} ^ {- 2} \mathrm{A} ^ {- 1}) \\ & = - \mathbf {k} (1.602 \times 10 ^ {- 18} \mathrm{kgms} ^ {- 2}) = - \mathbf {k} (1.602 \times 10 ^ {- 18} \mathrm{N}). \end{array}
$$

The force on a charged particle due to an electric field is

$$
\mathbf {F} = q \mathbf {E},\tag{2.78}
$$

where E is the electric field and q is the charge on the particle. If the charge is measured in coulombs and the field in volts per meter, the force is in newtons.

EXERCISE 2.22 ▶ Find the direction and the magnitude of the electric field necessary to provide a force on the electron in the previous example that is equal in magnitude to the force due to the magnetic field but opposite in direction. If both these forces act on the particle, what will be their effect?

## 2.5 Imaginary and Complex Numbers

Imaginary numbers have been defined into existence by mathematicians. They cannot be used to represent any physically measured quantity, but turn out to be useful in quantum mechanics. The imaginary unit is called i (not to be confused with the unit vector i) and is defined to be the square root of -1:

$$
\boxed {i = \sqrt {- 1}}\tag{2.79}
$$

If $b$ is a real number, the quantity $ib$ is said to be pure imaginary, and if $a$ is also real, the quantity

$$
c = a + i b\tag{2.80}
$$

is said to be a complex number. The real number $a$ is called the real part of $c$ and is denoted by

$$
a = R (c).\tag{2.81}
$$

The real number b is called the imaginary part of c and is denoted by

$$
b = I (c).\tag{2.82}
$$

All of the rules of ordinary arithmetic apply with complex numbers. The sum of two complex numbers is obtained by adding the two real parts together and adding the two imaginary parts together. If $c_{1}=a_{1}+ib_{1}$ and $c_{2}=a_{2}+ib_{2}$ , then

$$
c _ {1} + c _ {2} = a _ {1} + a _ {2} + i (b _ {1} + b _ {2})
$$

The product of two complex numbers is obtained by the same procedure as multiplying two real binomials.

$$
\begin{array}{r l} c _ {1} c _ {2} & = a _ {1} a _ {2} + i (a _ {1} b _ {2} + b _ {1} a _ {2}) + \left(i ^ {2}\right) b _ {1} b _ {2} \\ & = a _ {1} a _ {2} + i (a _ {1} b _ {2} + b _ {1} a _ {2}) - b _ {1} b _ {2} \end{array}
$$

Addition and multiplication are associative. That is, if A, B, and C are complex numbers,

$$
A + (B + C) = (A + B) + C\tag{2.83}
$$

$$
A (B C) = (A B) C.\tag{2.84}
$$

Addition and multiplication are distributive. That is,

$$
A (B + C) = A B + A C.\tag{2.85}
$$

Addition and multiplication are commutative. That is, addition or multiplication of two complex numbers yields the same result in either order:

$$
A + B = B + A\tag{2.86}
$$

$$
A B = B A.\tag{2.87}
$$

Subtraction is the addition of a number whose real and imaginary parts are the negatives of the number to be subtracted, and division is multiplication by the reciprocal of a number. If

$$
z = x + i y\tag{2.88}
$$

then the reciprocal of $z$ , called $z^{-1}$ , is given by

$$
\boxed {z ^ {- 1} = \frac {x}{x ^ {2} + y ^ {2}} - i \frac {y}{x ^ {2} + y ^ {2}}}.\tag{2.89}
$$

EXAMPLE 2.12 Show that $z(z^{-1}) = 1$ .

SOLUTION ▶

$$
\begin{array}{r c l} z (z ^ {- 1}) & = & (x + i y) \left(\frac {x}{x ^ {2} + y ^ {2}} - i \frac {y}{x ^ {2} + y ^ {2}}\right) \\ & = & \frac {1}{x ^ {2} + y ^ {2}} \left(x ^ {2} + i x y - i x y - i ^ {2} y ^ {2}\right) \\ & = & \frac {1}{x ^ {2} + y ^ {2}} \left(x ^ {2} - i ^ {2} y ^ {2}\right) = 1. \end{array}
$$

EXERCISE 2.23 ▶

Show that

$$
(a + i b) (c + i d) = a c - b d + i (b c + a d).\tag{2.90}
$$

EXERCISE 2.24 ▶

Show that

$$
\frac {a + i b}{c + i d} = \frac {(a c + b d - i a d + i b c)}{c ^ {2} + d ^ {2}}.\tag{2.91}
$$

EXERCISE 2.25 ▶

Find the value of

$$
(4 + 6 i) (3 + 2 i) + 4 i - \frac {1 + i}{3 - 2 i}.\tag{2.92}
$$

[NO TEXT]

Specifying a complex number is equivalent to specifying two real numbers, one for the real part and one for the imaginary part. A complex number is therefore similar to a vector in two dimensions. We can therefore represent a complex number by the location of a point in a plane, as shown in Fig. 2.12.

This kind of a figure is called an Argand diagram, and the plane of the figure is called the Argand plane or the complex plane. The horizontal coordinate represents the real part of the number and the vertical coordinate represents the imaginary part. The horizontal axis, labeled R, is called the real axis, and the vertical axis, labeled I, is called the imaginary axis.

![[d422e693804d3f98d8adc6ac3312279248f129f8e1c777a8735485b3160e5058.jpg]]  
Figure 2.12 ▶ Representation of the complex number $z = x + iy$ in the Argand diagram.

The location of the point in the Argand plane can be given by polar coordinates. We use the symbol r for the distance from the origin to the point, and the symbol $\phi$ for the angle in radians between the positive real axis and the line segment joining the origin and the point. The quantity r is the magnitude of the complex number. It is also called the absolute value or the modulus of the complex number. The angle $\phi$ is called the argument or phase of the complex number. From Eq. (2.37) and (2.38),

$$
z = x + i y = r \cos (\phi) + i r \sin (\phi).
$$

There is a theorem, known as Euler's formula, that allows a complex number to be written as an exponential with an imaginary exponent,

$$
\boxed {z = r e ^ {i \phi} = r \cos (\phi) + i r \sin (\phi) = x + i y,}\tag{2.93}
$$

where e is the base of natural logarithms, $e = 2.7182818 \ldots$ , and where r and $\phi$ are the magnitude and phase of the complex number. This form is called the polar representation of the complex number. In this formula, $\phi$ must be measured in radians.

In the polar representation, the product of two complex numbers, say $z_{1} = r_{1}e^{i\phi_{1}}$ and $z_{2} = r_{2}e^{i\phi_{2}}$ , is given in a convenient form:

$$
\boxed {z _ {1} z _ {2} = r _ {1} r _ {2} e ^ {i (\phi_ {1} + \phi_ {2})}}.\tag{2.94}
$$

The quotient $z_{1}z_{2}$ is given by

$$
\boxed {\frac {z _ {1}}{z _ {2}} = \left(\frac {r _ {1}}{r _ {2}}\right) e ^ {i (\phi_ {1} - \phi_ {2})}}\tag{2.95}
$$

DeMoivre's formula gives the result of raising a complex number to a given power:

$$
\left(r e ^ {i \phi}\right) ^ {n} = r ^ {n} e ^ {i n \phi} = r ^ {n} [ \cos (n \phi) + i \sin (n \phi) ]
$$

EXAMPLE 2.13 Evaluate the following.

(a) $\left(4e^{i\pi}\right)\left(3e^{2i\pi}\right)$

$$
\mathrm{(b)} \left(8 e ^ {2 i \pi}\right) \left(2 e ^ {i \pi / 2}\right)
$$

(c) $\left(8e^{4i}\right)^2$

SOLUTION ▶

$$
\mathrm{(a)} \left(4 e ^ {i \pi}\right) \left(3 e ^ {2 i \pi}\right) = 12 e ^ {3 i \pi} = 12 e ^ {i \pi}
$$

$$
\mathrm{(b)} \left(8 e ^ {2 i \pi}\right) \left(2 e ^ {i \pi / 2}\right) = 4 e ^ {5 i \pi / 2}
$$

$$
\left(\mathrm{c}\right) \left(8 e ^ {4 i}\right) ^ {2} = 64 e ^ {8 i}.
$$

In part (a) of the preceding example we have used the fact that an angle of $2\pi$ radians gives the same point in the complex plane as an angle of 0, so that

$$
\boxed {e ^ {2 \pi i} = 1}\tag{2.96}
$$

Similarly,

$$
\boxed {e ^ {\pi i} = - 1}\tag{2.97}
$$

Since an angle is unchanged if any multiple of $2\pi$ is added or subtracted from it, we can write

$$
e ^ {i (\phi + 2 n \pi)} = e ^ {i \phi}\tag{2.98}
$$

where n is an integer. If a number is given in the form $z = x + iy$ , we can find the magnitude and the phase as

$$
r = \sqrt {x ^ {2} + y ^ {2}}\tag{2.99}
$$

$$
\phi = \arctan \left(\frac {y}{x}\right)\tag{2.100}
$$

Just as with a transformation from cartesian coordinates to polar coordinates, we do not necessarily use the principal value of the arctangent function, but must obtain an angle in the proper quadrant, with $\phi$ ranging from 0 to $2\pi$ .

$$
\begin{array}{l} \boxed {\text {EXERCISE 2.26}} \blacktriangleright \\ r e ^ {i \phi}: \\ \text {(a) 4 + 4 i} \\ \text {(c) 1} \end{array}
$$

Express the following complex numbers in the form

$$
\begin{array}{l} \text {(b)} - 1 \\ \text {(d)} 1 - i. \end{array}
$$

![[7c8b9b3c872df08144f87d09d345308c57e39d99cf291e830c366cdaddd5a786.jpg]]

$$
\begin{array}{l} \text {EXERCISE 2.27} \\ i y: \\ \text {(a)} e ^ {i \pi} \\ \text {(c)} e ^ {3 \pi i / 2} \end{array}
$$

Express the following complex numbers in the form $x +$

$$
(b) 3 e ^ {\pi i / 2}
$$

![[0c62074ab2f9b43403247f3bce4e565fa6bdb5e8095dc929dbf83ed8de62725c.jpg]]

The complex conjugate of a number is defined as the number that has the same real part and an imaginary part that is the negative of that of the original number. We will denote the complex conjugate by an asterisk (\*). It is also denoted by a bar over the letter for the number.

If $z = x + iy$ , then

$$
\boxed {\bar {z} = z ^ {*} = (x + i y) ^ {*} = x - i y.}\tag{2.101}
$$

Figure 2.13 shows the location of a complex number and of its complex conjugate in the Argand plane.

The phase of the complex conjugate is $-\phi$ if the phase of the original number is $\phi$ . The magnitude is the same, so

$$
\boxed {\left(r e ^ {i \phi}\right) ^ {*} = r e ^ {- i \phi}}.\tag{2.102}
$$

![[42fa2b3f2dba5d473f7d7838bac6499e0f58543ff419d22f8268fafdb38b049f.jpg]]

![[f9a09ef7be1283647b606dbce56b1092798bb14792e38b31de6a6d0ff8158098.jpg]]  
Figure 2.13 ▶ A complex number, $z = x + iy$ , and its complex conjugate, $z^{*} = x - iy$ , in the Argand plane.

Although we do not prove it, the following fact is useful in obtaining the complex conjugate of a complex quantity: The complex conjugate of any expression is obtained by changing the sign in front of every i that occurs in the expression.

EXAMPLE 2.14 Find the complex conjugates of the following, where $a, b, c$ , and $d$ are real quantities:

(a) $A = (1 + 2i)^{3 / 2} - \exp (3 + 4i)$

(b) $B = a(b + ci)^{2} + 4(c - id)^{-1}.$

SOLUTION ▶ (a) $A^{*} = (1 - 2i)^{3/2} - \exp(3 - 4i)$ (b) $B^{*} = a(b - ci)^{2} + 4(c + id)^{-1}$ .

EXERCISE 2.28 ▶ Find the complex conjugates of

(a) $A = (x + iy)^{2} - 4e^{ixy}$

$$
B = (3 + 7 i) ^ {3} - (7 i) ^ {2}.
$$

Once we have an expression for the complex conjugate of a quantity, we can use it to express the real and imaginary parts separately:

$$
R (z) = \frac {z + z ^ {*}}{2}\tag{2.103}
$$

$$
I (z) = \frac {z - z ^ {*}}{2 i}\tag{2.104}
$$

Use Eq. (2.101) to show that Eqs. (2.103) and (2.104)

EXERCISE 2.30 ▶

Obtain the famous formulas

$$
\boxed {\cos (\phi) = \frac {e ^ {i \phi} + e ^ {- i \phi}}{2} = R (e ^ {i \phi})}\tag{2.105}
$$

$$
\boxed {\sin (\phi) = \frac {e ^ {i \phi} - e ^ {- i \phi}}{2 i} = I (e ^ {i \phi})}\tag{2.106}
$$

The magnitude of an expression can also be obtained by using the complex conjugate. We find that

$$
\boxed {z z ^ {*} = \left(r e ^ {i \phi}\right) \left(r e ^ {- i \phi}\right) = r ^ {2}}\tag{2.107}
$$

so that

$$
\boxed {r = \sqrt {z z ^ {*}}},\tag{2.108}
$$

where the positive square root is to be taken. The product of any complex number and its complex conjugate is always real and nonnegative.

EXERCISE 2.31 ▶ Write a complex number in the form $x + iy$ and show that the product of the number with its complex conjugate is real and nonnegative.

EXAMPLE 2.15 If $z = 4e^{3i} + 6i$ , find $R(z), I(z), r$ , and $\phi$ .

## SOLUTION ▶

$$
\begin{array}{r l} R (z) & = \frac {z + z ^ {*}}{2} = \frac {4 e ^ {3 i} + 6 i + 4 e ^ {- 3 i} - 6 i}{2} \\ & = 2 (e ^ {3 i} + e ^ {- 3 i}) = 4 \cos (3) = - 3.960 \\ I (z) & = \frac {z - z ^ {*}}{2 i} = \frac {4 e ^ {3 i} + 6 i - 4 e ^ {- 3 i} + 6 i}{2 i} \\ & = \frac {4 (e ^ {3 i} - e ^ {- 3 i})}{2 i} + 6 = 4 \sin (3) + 6 \\ & = 4 \sin (171.89 ^ {\circ}) + 6 = 6.5645 \\ r & = (z z ^ {*}) ^ {1 / 2} = (x ^ {2} + y ^ {2}) ^ {1 / 2} \\ & = [ (- 3.960) ^ {2} + (6.5645) ^ {2} ] ^ {1 / 2} = 7.666 \\ \phi & = \arctan \left(\frac {I}{R}\right) = \arctan \left(\frac {- 6 .5645}{3 .960}\right) \\ & = \arctan (- 1.6577) \end{array}
$$

The principal value of this arctangent is $-58.90^{\circ}$ . However, since $R(z)$ is negative and $I(z)$ is positive, we require an angle in the second quadrant.

$$
\phi = 180 ^ {\circ} - 58.90 ^ {\circ} = 121.10 ^ {\circ} = 2.114 \mathrm{rad}.
$$

EXERCISE 2.32 ▶

$$
\text { If } z = \left(\frac {3 + 2 i}{4 + 5 i}\right) ^ {2}, \text { find } R (z), I (z), r, \text { and } \phi .
$$

The square root of a complex number is a number that will yield the first number when multiplied by itself. Just as with real numbers, there are two square roots of a complex number. If $z = r e^{i\phi}$ , one of the square roots is given by

$$
\sqrt {r e ^ {i \phi}} = \sqrt {r} e ^ {i \phi / 2}.\tag{2.109}
$$

The other square root is obtained by realizing that if $\phi$ is increased by $2\pi$ , the same point in the Argand plane is represented. Therefore, the square root of $re^{i(2\pi+\phi)}$ is the same as the other square root of $re^{i\phi}$ .

$$
\sqrt {r e ^ {i \phi}} = \sqrt {r e ^ {i (2 \pi + \phi)}} = \sqrt {r} e ^ {i (\pi + \phi / 2)}.\tag{2.110}
$$

EXAMPLE 2.16 Find the square roots of $3e^{i\pi/2}$ .

SOLUTION ▶ One square root is, from Eq. (2.109),

$$
\sqrt {3 e ^ {i \pi / 2}} = \sqrt {3} e ^ {i \pi / 4}.
$$

The other square root is, from Eq. (2.110),

$$
\sqrt {3} e ^ {i (\pi + \pi / 4)} = \sqrt {3} e ^ {i 5 \pi / 4}.
$$

If a complex number is represented as $x + iy$ , it is usually best to transform to polar coordinates before taking the square root of the number.

EXERCISE 2.33 ▶ Find the square roots of $4 + 4i$ . Sketch an Argand diagram and locate the roots on it.

There are three cube roots of a complex number. These can be found by looking for the numbers that when cubed yield $re^{i\phi}$ , $re^{i(2\pi+\phi)}$ , and $re^{i(4\pi+\phi)}$ . These numbers are

$$
\sqrt [ 3 ]{r e ^ {i \phi}} = \sqrt [ 3 ]{r} e ^ {i \phi / 3}, \sqrt [ 3 ]{r} e ^ {i (2 \pi + \phi) / 3}, \sqrt [ 3 ]{r} e ^ {i (4 \pi + \phi) / 3}.
$$

Higher roots are obtained similarly.

EXAMPLE 2.17 Find the three cube roots of -1.

SOLUTION ▶ In the polar representation, $-1 = e^{i\pi}$ . The three cube roots are

$$
\sqrt [ 3 ]{e ^ {i \pi}} = e ^ {i \pi / 3}, e ^ {i \pi}, e ^ {5 i \pi / 3}\tag{2.111}
$$

Higher roots are defined similarly.

EXERCISE 2.34 ▶

Find the four fourth roots of $-1$ .

## 2.6 Problem Solving and Symbolic Mathematics

We have already seen a number of relatively simple exercises, examples, and problems in this and the previous chapter. In most cases, these involved carrying out operations that we either specified or that were fairly obvious. We now make some general comments on solving chemistry problems, which are usually a little more complicated. A typical chemistry problem is similar to what was once called a story problem or a word problem in elementary school. You are given some factual information (or asked to find some), together with a verbal statement of what answer is required, but you must find your own method of obtaining the answer from the given information. In a simple problem, this may consist only of substituting numerical values into a formula, but in a more complicated problem you might have to derive your own mathematical formula or carry out other procedures. The method, or algorithm, must be developed for each problem. Sometimes the algorithm is the use of a single formula. The principal tool for obtaining a useful formula from another formula is algebra, In algebra we manipulate the symbols standing for variables without actually carrying out numerical operations. An algebraic equation has a set of symbols for variables and operations on each side of the equation, with the assertion that if we replace the variable symbols by their numerical values and carry out the indicated operations, we obtain the same numerical value for each side of the equation. If we have a valid algebraic equation, we can symbolically carry out the same operation on both sides of the equation and obtain a valid new equation. For example, we can symbolically divide both sides of the equation by some variable by writing the symbol for the variable as a denominator in a fraction and canceling symbols on both the top and bottom of the fraction.

EXAMPLE 2.18 Under ordinary conditions, ordinary gases nearly obey the ideal gas equation is

$$
P V = n R T\tag{2.112}
$$

where V is the volume, n is the amount of gas in moles, T is the temperature, P is the pressure, and R is the ideal gas constant, equal to $8.3145 \, J \, K^{-1} \, mol^{-1} = 0.082061 \, atm \, K^{-1} \, mol^{-1}$ . Calculate the volume occupied by 1.278 mol of an ideal gas if the pressure is 2.341 atm and the temperature is 298.15 K.

SOLUTION ▶ Since there are four variables, we can calculate the value of one of them if the values of the other three are given. We solve the ideal gas equation for V by symbolically dividing both sides of the equation by P, obtaining

$$
V = \frac {n R T}{P}.\tag{2.113}
$$

We substitute the numerical values into Eq. (2.113), convert the pressure from atmospheres to pascals by use of the factor label method, and carry out the numerical operations:

$$
\begin{array}{r l} V & = \frac {(1 .278 \mathrm{mol}) (8 .3145 \mathrm{JK} ^ {- 1} \mathrm{mol} ^ {- 1}) (298 .15 \mathrm{K})}{2 .314 \mathrm{atm}} \left(\frac {1 \mathrm{atm}}{101325 \mathrm{Pa}}\right) \\ & = 1.351 \times 10 ^ {- 2} \mathrm{JPa} ^ {- 1} \\ & = 1.351 \times 10 ^ {- 2} \mathrm{JPa} ^ {- 1} \left(\frac {1 \mathrm{Pa}}{1 \mathrm{Nm} ^ {- 2}}\right) \left(\frac {1 \mathrm{Nm}}{1 \mathrm{J}}\right) \\ & = 1.351 \times 10 ^ {- 2} \mathrm{m} ^ {3}. \end{array}
$$

We give the answer to four significant digits, because both the pressure and the amount of gas are specified to four significant digits. We can now make an additional conversion to express the volume in liters:

$$
\left(1.351 \times 10 ^ {- 2} \mathrm{m} ^ {3}\right) \left(\frac {11}{10 ^ {- 3} \mathrm{m} ^ {3}}\right) = 13.511
$$

We know that this solution is in the correct range of values, since a mole of gas at room temperature and one atmosphere pressure occupies about 25 liters.

The preceding example was a simple one, but it illustrates some of the principles of problem solving. Let's summarize the procedure that was used. We first determined that the ideal gas equation of state was sufficient to work the problem and that enough information was given. This equation was solved algebraically for the volume to give a working formula. The given values of quantities were substituted into the formula, and the necessary unit conversion was made. After all factors were written out and the units checked, the multiplications and divisions were carried out and it was determined that the answer was about the right size.

The general problem-solving procedure can be summarized as follows:

1. Analyze the given information and the desired answer.

2. Decide what kind of a procedure is needed to process the given information and obtain the desired answer. Determine whether enough information is contained in the given information. If one or more formulas are needed, find the formulas. In working a complicated problem, it might be useful to map out on a piece of paper how you are going to get from the given information to the desired answer. $^{3}$

3. Find any addition information that is needed.

4. Carry our any necessary symbolic manipulations to obtain a working formula from the formula or formulas that you found. In some problems you might be asked to obtain a formula, and if so this is the end of the procedure.

5. Carry out any numerical operations to obtain the desired answer.

6. Look at your answer to see it if is reasonable. Simple numerical mistakes will usually cause your answer to be much too large or too small, and you can usually see if this is the case. For example, if your answer is a molecular diameter and you obtain a value of roughly 1000 m, you know that there is a mistake somewhere. You should also check your answer by substituting it into the original formula.

In order to judge whether an answer is reasonable, it is useful to be able to estimate approximate sizes of things. You need to start with reasonable estimates and work out an estimate of the desired quantity. For example, a professor asked a class to estimate the number of piano tuners in New York City. One would start with an estimate of the population—say, 10 million people—which might amount to 5 million households. Perhaps one household in 10 might have a piano, for 500,000 pianos. A professional pianist might have a piano tuned every month, but most people might let it go for several years. We assume that on the average, each piano is tuned once in two years, for 250,000 tunings per year. A professional piano tuner might be able to tune 6 pianos in a day, or about 1200 pianos in a year. The result is that there might be about 200 full-time piano tuners in New York City. This number is surely wrong, but must be in the right order of magnitude.

EXERCISE 2.35 ▶

Estimate the number of house painters in Chicago.

In the remaining chapters of this book, you will see a number of examples worked out, and you will see a number of exercises and problems that you can solve. In most of these, a method must be found and applied that will lead from the given information to the desired answer. In some problems there will be a choice of methods. Perhaps you must choose between a graphical procedure and a numerical procedure, or between an approximate formula and an exact formula. In some of these cases, it would be foolish to carry out a more difficult solution, because an approximate solution will give you an answer that will be sufficient for the purpose at hand. In other cases, you will need to carry out a more nearly exact solution. You will need to learn how to distinguish between these two cases.

## SUMMARY

In this chapter we have introduced symbolic mathematics, which involves the manipulation of symbols instead of performing numerical operations. We have presented the algebraic tools needed to manipulate expressions containing real scalar variables, real vector variables, and complex scalar variables. We have also introduced ordinary and hyperbolic trigonometric functions, exponentials, and logarithms. A brief introduction to the techniques of problem solving was included.

## PROBLEMS

1. A Boy Scout finds a tall tree while hiking and wants to estimate its height. He walks away from the tree and finds that when he is 98 m from the tree, he must look upward at an angle of $35^{\circ}$ to look at the top of the tree. His eye is 1.50 m from the ground, which is perfectly level. How tall is the tree?

2. The equation $x^{2} + y^{2} + z^{2} = c^{2}$ , where c is a constant, represents a surface in three dimensions. Express the equation in spherical polar coordinates. What is the shape of the surface?

3. Express the equation $y = b$ , where $b$ is a constant, in plane polar coordinates.

4. Express the equation $y = mx + b$ , where m and b are constants, in plane polar coordinates.

5. Find the values of the plane polar coordinates that correspond to x = 2, y = 4.

6. Find the values of the cartesian coordinates that correspond to $r = 10, \theta = 45^{\circ}, \phi = 135^{\circ}$ .

7. Find the values of the spherical polar coordinates that correspond to $x = 2$ , $y = 2$ , $z = 4$ .

8. A surface is represented in cylindrical polar coordinates by the equation $z = \rho^{2}$ . Describe the shape of the surface.

9. Find A - B if $A = 2i + 3j$ and $B = i + 3j - k$ .

10. Find $\mathbf{A} \cdot \mathbf{B}$ if $\mathbf{A} = (0, 2)$ and $\mathbf{B} = (2, 0)$ .

11. Find $|\mathbf{A}|$ if $\mathbf{A} = 3\mathbf{i} + 4\mathbf{j} - \mathbf{k}$ .

12. Find $\mathbf{A} \cdot \mathbf{B}$ if $\mathbf{A} = \mathbf{i} + \mathbf{j} + \mathbf{k}$ and $\mathbf{B} = \mathbf{i} + 3\mathbf{j} - 2\mathbf{k}$ .

13. Find $\mathbf{A} \cdot \mathbf{B}$ if $\mathbf{A} = (1, 1, 1)$ and $\mathbf{B} = (2, 2, 2)$ .

14. Find $\mathbf{A} \times \mathbf{B}$ if $\mathbf{A} = (0, 1, 2)$ and $\mathbf{B} = (2, 1, 0)$ .

15. Find $\mathbf{A} \times \mathbf{B}$ if $\mathbf{A} = (1, 1, 1)$ and $\mathbf{B} = (2, 2, 2)$ .

16. Find the angle between A and B if $A = i + 2j + k$ and $B = i + j + k$ .

17. Find the angle between A and B if $A = 3i + 2j + k$ and $B = i + 2j + 3k$ .

18. A spherical object falling in a fluid has three forces acting upon it: (1) The gravitational force, whose magnitude is $F_{g} = mg$ , where m is the mass of the object and g is the acceleration due to gravity, equal to $9.8 \, m s^{-2}$ ; (2) The buoyant force, whose magnitude is $F_{b} = m_{f} g$ , where $m_{f}$ is the mass of the displaced fluid, and whose direction is upward; (3) The frictional force, which is given by $F_{f} = -6\pi \eta r v$ , where r is the radius of the object, v its velocity, and $\eta$ the coefficient of viscosity of the fluid. This formula for the frictional forces applies only if the flow around the object is laminar (flow in layers). The object is falling at a constant speed in glycerol, which has a viscosity of $1490 \, kg m^{-1} s^{-1}$ . The object has a mass of 0.00381 kg, has a radius of 0.00432 m, a mass of 0.00381 kg, and displaces a mass of fluid equal to 0.000337 kg. Find the speed of the object.

19. The solutions to the Schrödinger equation for the electron in a hydrogen atom have three quantum numbers associated with them, called n, l, and m, and these solutions are often denoted by $\psi_{nlm}$ . One of the solutions is

$$
\psi_ {211} = \frac {1}{8 \sqrt {\pi}} \left(\frac {1}{a _ {0}}\right) ^ {3 / 2} \frac {r}{a _ {0}} e ^ {- r / 2 a _ {0}} \sin (\theta) e ^ {i \phi},
$$

where $a_{0}$ is a distance equal to $0.529 \times 10^{-10}$ m, called the Bohr radius.

a) Write this function in terms of cartesian coordinates.

b) Write an expression for the magnitude of this complex function.

c) This function is sometimes called $\psi_{2p1}$ . Write expressions for the real and imaginary parts of the function, which are proportional to the related functions called $\psi_{2px}$ and $\psi_{2py}$ .

20. Find the sum of $4e^{3i}$ and $5e^{2i}$ .

21. Find the difference $3e^{\pi i} - 2e^{2i}$ .

22. Find the three cube roots of 3 - 2i.

23. Find the four fourth roots of 3i.

24.

a) Find the real and imaginary parts of

$$
\sqrt {3 + i} + (6 + 5 i) ^ {2}
$$

Obtain a separate answer for each of the two square roots of the first term.

b) Write the complex conjugate of each answer.

25. An object has a force on it given by $(4.75\mathrm{N})\mathbf{i} + (7.00\mathrm{N})\mathbf{j} + (3.50\mathrm{N})\mathbf{k}$ .

a) Find the magnitude of the force.

b) Find the projection of the force in the x-y plane. That is, find the vector in the x-y plane whose head is reached from the head of the force vector by moving in a direction perpendicular to the x-y plane.

26. An object of mass 12.000 kg is moving in the x direction. It has a gravitational force acting on it equal to -mgk, where m is the mass of the object and g is the acceleration due to gravity, equal to 9.80 m s $^{-1}$ . There is a frictional force equal to (0.240 N)i. What is the magnitude and direction of the resultant force (the vector sum of the forces on the object)?

27. The potential energy of a magnetic dipole in a magnetic field is given by the scalar product

$$
\mathcal {V} = - \mu \cdot \mathbf {B},
$$

where B is the magnetic induction (magnetic field) and $\mu$ is the magnetic dipole. Make a graph of $\mathcal{V}/(|\mu||\mathbf{B}|)$ as a function of the angle between $\mu$ and B.

28. Estimate the number of grains of sand on the beaches of the major continents of the earth. Exclude islands and inland bodies of water. You should come up with a number somewhere near Avogadro's number.

29. Assume that a gas has a molar volume of 20 liters. Estimate the average distance between nearest-neighbor molecules.

30. Estimate the number of blades of grass in a lawn with an area of 1000 square meters.

# The Solution of Algebraic Equations

## Preview

If an equation is written in the form $f(x) = 0$ , where f is some function and x is a variable, solving the equation means to find those constant values of x such that the equation is satisfied. These values are called solutions or roots of the equation. We discuss both algebraic and numerical methods for finding roots to algebraic equations. If there are two variables in the equation, such as $F(x, y) = 0$ , then the equation can be solved for y as a function of x or x as a function of y, but in order to solve for constant values of both variables, a second equation, such as $G(x, y) = 0$ , is required, and the two equations must be solved simultaneously. In general, if there are n variables, n independent and consistent equations are required.

## Principal Facts and Ideas

1. The solution to an algebraic equation is generally a value or a set of values of the independent variable such that substitution of such a value into the equation produces an numerically correct equation such as 0 = 0.

2. For a single independent variable, one equation is required.

3. An algebraic equation in one variable can be solved algebraically, graphically, or numerically.

4. Polynomial equations through the fourth degree can be solved algebraically, but some equations of fifth and higher degree cannot be solved algebraically.

5. For n variables, n equations are required, but these equations must be independent and consistent.

6. Linear homogeneous simultaneous equations have a nontrivial solution only when a certain dependence condition is met.

## Objectives

After studying this chapter, you should be able to:

1. solve any quadratic equation and determine which root is physically meaningful;

2. obtain an accurate numerical approximation to the roots of any single equation in one unknown, using graphical and numerical techniques;

3. solve any fairly simple set of two simultaneous linear equations.

## 3.1 Algebraic Methods for Solving One Equation with One Unknown

If you have one algebraic equation containing one variable, there will generally be a set of one or more constant values of that variable which make the equation valid. They are said to satisfy the equation, and the values in the set are called the roots or solutions of the equation. Other values of the variable do not produce a valid equation and are said not to satisfy the equation.

## Polynomial Equations

A polynomial equation in the variable x is written in the form

$$
f (x) = a _ {0} + a _ {1} x + a _ {2} x ^ {2} + \dots + a _ {n} x ^ {n} = 0,\tag{3.1}
$$

where n, the largest exponent in the equation, is some positive integer. The integer n is called the degree of the equation. If n = 1, the equation is a linear equation. If n = 2, the equation is a quadratic equation. If n = 3, the equation is a cubic equation. If n = 4, it is a quartic equation, and so on.

Generally, there are n roots to an nth-degree polynomial equation, but two or more of the roots can be equal to each other. It is also possible for some of the roots to be imaginary or complex numbers. If complex roots occur, there is always an even number of them. For most equations arising from physical and chemical problems, there will be only one root that is physically reasonable, and the others must be disregarded. For example, a concentration cannot be negative, and if a quadratic equation for a concentration produces a positive root and a negative root, the negative root disregarded. Complex roots cannot represent physically measurable quantities and must be disregarded if we are solving for a physically meaningful quantity.

## Linear Equations

If an equation is of the form

$$
a _ {0} + a _ {1} x = 0\tag{3.2}
$$

then the single root of the equation is

$$
x = - \frac {a _ {0}}{a _ {1}}.\tag{3.3}
$$

## Quadratic Equations

A quadratic equation is written in a standard form as

$$
a x ^ {2} + b x + c = 0.\tag{3.4}
$$

Some quadratic expressions can be factored, which means that the equation can be written

$$
a (x - x _ {1}) (x - x _ {2}) = 0,\tag{3.5}
$$

where $x_{1}$ and $x_{2}$ are constants. In this case, $x_{1}$ and $x_{2}$ are the two roots of the equation. If a quadratic equation cannot easily be factored, you can apply the quadratic formula

$$
\boxed {x = \frac {- b \pm \sqrt {b ^ {2} - 4 a c}}{2 a}.}\tag{3.6}
$$

This equation provides two roots, one when the positive sign in front of the square root is chosen and one when the negative sign is chosen. There are three cases: (1) if the discriminant $b^{2} - 4ac$ is positive, the roots will be real and unequal; (2) if the discriminant is equal to zero, the two roots will be real and equal to each other; (3) if the discriminant is negative, the roots will be unequal and complex, since the square root of a negative quantity is imaginary. Each imaginary root will be the complex conjugate of the other root.

EXERCISE 3.1 ▶ Show by substituting Eq. (3.6) into Eq. (3.4) that the quadratic formula provides the roots to a quadratic equation.

A common application of a quadratic equation in elementary chemistry is the calculation of the hydrogen ion concentration in a solution of a weak acid. If activity coefficients are assumed to equal unity, the equilibrium expression in terms of molar concentrations is

$$
K _ {a} = \frac {\left([ \mathrm{H} ^ {+} ] / \mathrm{c} ^ {\circ}\right) \left([ \mathrm{A} ^ {-} ] / \mathrm{c} ^ {\circ}\right)}{\left([ \mathrm{HA} ] / \mathrm{c} ^ {\circ}\right)},\tag{3.7}
$$

where $[H^{+}]$ is the hydrogen-ion concentration expressed in moles per liter, $[A^{-}]$ the acid-anion concentration, $[HA]$ is the concentration of the undissociated acid, $c^{\circ}$ is defined to equal 1 mol $l^{-1}$ , and $K_{a}$ is the acid ionization constant. The expression in terms of molalities can also be used and has the same appearance. It is true that the hydrogen ions are nearly all attached to water molecules or water molecule dimers, and so forth, so that we could write $[H_{3}O^{+}]$ instead of $[H^{+}]$ , but this makes no difference in the calculation.

EXAMPLE 3.1 For acetic acid, $K_{a} = 1.754 \times 10^{-5}$ at $25^{\circ}\mathrm{C}$ . Find $[\mathrm{H}^{+}]$ if $0.1000\mathrm{mol}$ of acetic acid is dissolved in enough water to make $1.0001$ . We say that the stoichiometric concentration (the concentration that would occur if no ionization occurred) is equal to $0.100\mathrm{mol}1^{-1}$ .

SOLUTION ▶ Assuming that no other sources of hydrogen ions or acetate ions are present, $[H^{+}]/c^{\circ} = [A^{-}]/c^{\circ}$ , which we denote by x,

$$
K _ {a} = \frac {x ^ {2}}{0 .1000 - x}
$$

or

$$
x ^ {2} + K _ {a} x - 0.1000 K _ {a} = 0.
$$

From Eq. (3.6), our solution is

$$
\begin{array}{r l} x & = \frac {- K _ {a} \pm \sqrt {K _ {a} ^ {2} - 0 .4000 K _ {a}}}{2} \\ & = 1.316 \times 10 ^ {- 3} \quad \text {or} \quad - 1.333 \times 10 ^ {- 3} \\ [ \mathrm{H} ^ {+} ] & = [ \mathrm{A} ^ {-} ] = 1.316 \times 10 ^ {- 3} \mathrm{mol} \mathrm{l} ^ {- 1}. \end{array}
$$

We have disregarded the negative root because a concentration cannot be negative.

EXERCISE 3.2 ▶ Express the answer to the previous example in terms of pH, defined for our present purposes as

$$
p H = - \log_ {10} ([ \mathrm{H} ^ {+} ] / \mathrm{c} ^ {\circ})\tag{3.8}
$$

EXERCISE 3.3 ▶ Find the pH of a solution formed from 0.075mol of $NH_{3}$ and enough water to make 1.00 l of solution. The ionization that occurs is

$$
\mathrm{NH} _ {3} + \mathrm{H} _ {2} \mathrm{O} \leftrightarrows \mathrm{NH} _ {4} ^ {+} + \mathrm{OH} ^ {-}
$$

The equilibrium expression in terms of molar concentrations is

$$
K _ {\mathrm{b}} = \frac {([ \mathrm{NH} _ {4} ^ {+} ] / \mathrm{c} ^ {\circ}) ([ \mathrm{OH} ^ {-} ] / \mathrm{c} ^ {\circ})}{([ \mathrm{NH} _ {3} ] / \mathrm{c} ^ {\circ})}
$$

where the water concentration is replaced by its mole fraction, which is very nearly equal to unity. $K_{b}$ equals $1.80 \times 10^{-5}$ for $NH_{3}$ .

## Approximate Solutions to Equations

It is usually necessary to seek approximate roots to equations other than linear or quadratic equations, especially with equations containing sines, cosines, logarithms, exponentials, and so on. These equations are called transcendental equations. Cubic and quartic polynomial equations can be solved algebraically, but it is probably best to apply approximation techniques rather than attempting an algebraic solution. $^{1}$ There are two approaches: one is to modify the equation by making simplifying assumptions, and the other is to seek a numerical approximation that can be made to approximate the correct solution to any desired degree of accuracy.

## Approximation by Use of Simplifying Assumptions

The first method for finding approximate roots to an equation is to modify the equation by making simplifying assumptions. As an example, let us consider an equation for the hydrogen-ion concentration in a solution of a weak acid in which the hydrogen ions from the ionization of water cannot be ignored. We must solve simultaneous equations for the ionization of the weak acid and ionization of water. Later in this chapter, we will derive the equation

$$
K _ {a} = \frac {x (x - K _ {w} / x)}{c / c ^ {\circ} - x + K _ {w} / x},\tag{3.9}
$$

where c is the stoichiometric concentration of the acid, where $c^{\circ}$ is defined to equal $1\ mol\ l^{-1}$ , where $K_{w}$ is the ionization constant of water, equal to $1.00 \times 10^{-14}$ near $25^{\circ}C$ , and where $x = [H^{+}]/c^{\circ}$ . If we multiply this equation out, we obtain the cubic equation

$$
x ^ {3} + K _ {a} x ^ {2} - \left(\frac {c K _ {a}}{c ^ {\circ}} + K _ {w}\right) x - K _ {a} K _ {w} = 0.\tag{3.10}
$$

This equation can be solved numerically for any specific case, but in some cases, it is possible to simplify this equation by making approximations.

EXERCISE 3.4 ▶ Carry out the algebraic manipulations to obtain the cubic equation version of Eq. (3.9).

EXAMPLE 3.2 For the case of acetic acid with a stoichiometric concentration of 0.100 mol l $^{-1}$ , convert Eq. (3.9) to a simpler approximate equation by discarding any negligibly small terms.

SOLUTION ▶ Equation (3.9) contains two terms in the numerator and three in the denominator. If one term in a polynomial is much smaller than the other terms, it might be possible to neglect this term. In the numerator, we know that $x = [H^{+}]/c^{\circ}$ will lie somewhere between 0.1 and $10^{-7}$ , the value for pure water. In fact, we know from our approximate solution in the previous example that $[H^{+}]$ is near $10^{-3}$ mol l $^{-1}$ . Since $K_{w}$ equals $1.00 \times 10^{-14}$ , the second term must be near $10^{-11}$ mol l $^{-1}$ , which is smaller than the first term by a factor of $10^{8}$ . We therefore drop the term $K_{w}/x$ . We also drop the same term in the denominator, and obtain the equation

$$
K _ {a} = \frac {x ^ {2}}{c / c ^ {\circ} - x}\tag{3.11}
$$

which is the same as Eq. (3.7), which was obtained with the assumption that $[H^{+}]=[A^{-}]$ .

It is possible in some cases to make a further approximation on Eq. (3.11). If only a small fraction of the weak acid ionizes, $[H^{+}]$ will be small compared with c, so that x can be neglected in the denominator. In the case of acetic acid and a gross acid concentration of $0.100\ mol\ l^{-1}$ , $[H^{+}]$ is approximately equal to $10^{-3}\ mol\ l^{-1}$ , only about 1% as large as c. If we can tolerate an error of about 1%, we can neglect x compared with $c/c^{\circ}$ . We obtain

$$
K _ {a} = \frac {x ^ {2}}{c / c ^ {\circ}}\tag{3.12}
$$

TABLE 3.1 ▶ Results for the Hydrogen-Ion Concentration in Acetic Acid Solutions at 25°C from Different Equations at Different Concentrations

<table><tr><td> $c$  (mol  $liter^{-1}$ )</td><td>by Eq. (3.10)</td><td> $[H^{+}]$  (mol  $liter^{-1}$ ) by Eq. (3.11)</td><td>by Eq. (3.13)</td></tr><tr><td>0.1000</td><td> $1.31565 \times 10^{-3}$ </td><td> $1.31565 \times 10^{-3}$ </td><td> $1.324 \times 10^{-3}$ </td></tr><tr><td> $1.000 \times 10^{-3}$ </td><td> $1.23959 \times 10^{-4}$ </td><td> $1.23959 \times 10^{-4}$ </td><td> $1.324 \times 10^{-4}$ </td></tr><tr><td> $1.000 \times 10^{-5}$ </td><td> $0.711545 \times 10^{-5}$ </td><td> $0.711436 \times 10^{-5}$ </td><td> $1.324 \times 10^{-5}$ </td></tr><tr><td> $1.000 \times 10^{-7}$ </td><td> $0.161145 \times 10^{-6}$ </td><td> $0.099435 \times 10^{-6}$ </td><td> $1.324 \times 10^{-6}$ </td></tr></table>

which has the solution

$$
x = \sqrt {(c / c ^ {\circ}) K _ {a}}.\tag{3.13}
$$

However, as c is made smaller, Eq. (3.13) quickly becomes a poor approximation, and for very small acid concentrations, Eq. (3.11) also becomes inaccurate. Table 3.1 shows the results from the three equations at different acid concentrations. Equation (3.11), the quadratic equation, remains fairly accurate down to $c = 10^{-5} \, mol l^{-1}$ , but Eq. (3.13) is wrong by about 7% at $10^{-3} \, mol l^{-1}$ , and much worse than that at lower concentrations.

In the case that approximations such as that of Eq. (3.13) are inaccurate, we can apply the method of successive approximations. In this method, one begins by solving an equation such as Eq. (3.13). The result of this approximation is used to approximate the term which was neglected in the first approximation and the solution is repeated. If needed, the result of this second approximation is used to replace the term that was originally neglected and the solution is repeated. This procedure is repeated (iterated) as many times as is necessary.

EXAMPLE 3.3 Solve the problem of Example 3.1 by successive approximation.

SOLUTION ▶ We write the equilibrium expression in the form

$$
x ^ {2} = K _ {a} (0.1000 - x)
$$

Since $x$ is presumably much smaller than 0.1000, we neglect it compared with 0.1000. We obtain

$$
x ^ {2} \approx (1.754 \times 10 ^ {- 5}) (0.1000) = (1.754 \times 10 ^ {- 6})
$$

This is the result that would be obtained from Eq. (3.13). The next approximation is obtained by replacing the $x$ in the right-hand side of the first equation by this value,

$$
x ^ {2} \approx (1.754 \times 10 ^ {- 5}) (0.1000 - 0.00132) = 1.731 \times 10 ^ {- 6}
$$

$$
x \approx \sqrt {1 .731 \times 10 ^ {- 6}} = 0.001316 \approx 0.00132.
$$

This result shows that the first approximation is acceptable. Further iterations would make even smaller changes, so we stop at this point.

EXERCISE 3.5 ▶ Solve for the hydrogen ion concentration in solutions of acetic acid with gross molarities equal to

$$
(a) 0.00100 \mathrm{mol} l ^ {- 1}
$$

$$
(b) 0.0000100 \mathrm{mol} l ^ {- 1}.
$$

Use the method of successive approximations on Eq. (3.9) and on Eq. (3.11).

## Approximation by linearization

In the next example, we see another way in which an equation can be made into a tractable approximate equation, by linearizing a function. We illustrate this technique in the following example:

EXAMPLE 3.4 The Dieterici equation of state is

$$
P e ^ {a / V _ {m} R T} (V _ {m} - b) = R T,\tag{3.14}
$$

where P is the pressure, T is the temperature, $V_{m}$ is the molar volume, and R is the ideal gas constant. The constant parameters a and b have different values for different gases. For carbon dioxide, $a = 0.468 \, Pa \, m^{6} \, mol^{-2}$ , $b = 4.63 \times 10^{-5} \, m^{3} \, mol^{-1}$ . Find the molar volume of carbon dioxide if $T = 298.15 \, K$ and $P = 10.000 \, atm = 1.01325 \times 10^{6} \, Pa$ .

SOLUTION ▶ The exponential function can be represented by the power series

$$
e ^ {x} = 1 + \frac {1}{1 !} x + \frac {1}{2 !} x ^ {2} + \frac {1}{3 !} x ^ {3} + \dots
$$

where $n!$ stands for n factorial, defined as $n(n-1)(n-2)(n-3)\cdots(3)(2)(1)$ . We write

$$
e ^ {a / V _ {m} R T} = 1 + a / V _ {m} R T + \frac {1}{2 !} (a / V _ {m} R T) ^ {2} + \dots .\tag{3.15}
$$

Rough calculation shows that $a/V_{m}RT \approx 0.09$ so that $(a/V_{m}RT)^{2} \approx 0.008$ . We therefore discard all of the terms past the $a/V_{m}RT$ term and write to a fairly good approximation:

$$
e ^ {a / V _ {m} R T} \approx 1 + a / V _ {m} R T.
$$

We say that we have linearized the exponential function. We substitute this approximation into the original equation of state, obtaining

$$
P (1 + a / V _ {m} R T) (V _ {m} - b) = R T
$$

which can be written in the standard form for a quadratic equation:

$$
P V _ {m} ^ {2} + \left(\frac {P a}{R T} - P b - R T\right) V _ {m} - \frac {P a b}{R T} = 0.
$$

We divide by P and substitute the numerical values. We temporarily let $x = V_{m}/(1 \, \text{m}^{3} \, \text{mol}^{-1})$ and obtain after some manipulation

$$
x ^ {2} - (2.304 \times 10 ^ {- 3}) x + 8.741 \times 10 ^ {- 9} = 0.
$$

Applying the quadratic formula,

$$
x = \frac {2 .304 \times 10 ^ {- 3} \pm \sqrt {(0 .002304) ^ {2} - 4 (8 .741 \times 10 ^ {- 9})}}{2} = \left\{ \begin{array}{l} 2.3 \times 10 ^ {- 3} \\ 4.000 \times 10 ^ {- 6}. \end{array} \right.
$$

We disregard the second value as too small to correspond to the physical situation, and obtain

$$
V _ {m} = 2.30 \times 10 ^ {- 3} \mathrm{m} ^ {3} \mathrm{mol} ^ {- 1}.
$$

The ideal gas equation of state gives $V_{m} = 2.447 \times 10^{-3} \, \mathrm{m}^{3} \, \mathrm{mol}^{-1}$ , for a difference of about $6\%$ .

EXERCISE 3.6 ▶ (a) Verify the prediction of the ideal gas equation of state given in the previous example.

(b) Substitute the value of the molar volume obtained in the previous example and the given temperature into the Dieterici equation of state to calculate the pressure. Compare the calculated pressure with 10.00 atm, to check the validity of the linearization approximation used in the example.

## 3.2 Graphical Solution of Equations

Instead of approximating an equation and then solving the approximate equation algebraically, we can apply the graphical method to obtain a numerical approximation to the correct root. This method is sometimes very useful because you can see what you are doing and you can usually be sure that you do not obtain a different root than the one you want to find. The equation to be solved is written in the form

$$
f (x) = 0
$$

where we denote the independent variable by x. If a graph of the function f is drawn, any real roots to the equation correspond to the places where the curve crosses the x axis.

EXAMPLE 3.5 By graphing, find a root of the equation

$$
2 \sin (x) - x = 0.
$$

in the interval 1.8 < x < 2.0.

SOLUTION ▶ A graph of the function for the interval 1.8 < x < 2.0 is shown in Fig. 3.1. From the graph, it appears that the root is near x = 1.895.

EXERCISE 3.7 ▶
equation

Find approximately the smallest positive root of the

$$
\tan (x) - x = 0.
$$

## Graphing with a Spreadsheet

Drawing a graph by hand is tedious, and almost no one actually makes graphs by hand, since it is possible to make graphs more easily with a spreadsheet program on a computer. A spreadsheet can perform various mathematical and other operations on sets of items that are entered by the user and displayed in the form of a table. A common spreadsheet is Microsoft Excel $^{®}$ . Another spreadsheet is Lotus 1-2-3 $^{®}$ . Microsoft Works $^{®}$ contains a spreadsheet that is a simplified version of Excel, and Claris Works $^{®}$ contains a similar spreadsheet program. At the time of this writing, the latest version of Excel is called Excel 2003. Previous versions were called Excel 2000, 1998, 4.0, 3.0, and so on. We describe briefly how to make a graph on the Excel spreadsheet. The instructions are written for a computer using the Windows operating system, but the procedure is similar on a Macintosh computer.

![[be7377c62a72a2650c5223b2bc8821cab99a2380f1c9968f3857921eceaf5bf7.jpg]]  
Figure 3.1 ▶ Graph of Example 3.5.

## Creating and Editing a Worksheet in Excel

When one first opens Excel a window is displayed on the screen with a number of rectangular areas called cells arranged in rows and columns. This window is called a worksheet. The rows are labeled by numbers and the columns are labeled by letters. Any cell can be specified by giving its column and its row (its address). For example, the address of the cell in the third row of the second column is B3. A list of menu headings appears across the top of the screen and a double strip of small icons called a “toolbar” appears under the menu headings.

Any cell can be selected by using the arrow buttons on the keyboard or by moving the mouse until its cursor is in the desired cell and clicking the left mouse button. One can then type one of three kinds of information into the cell: a number, some text, or a formula. For example, one might want to use the top cell in each column for a label for that column. One would first select the cell and then type the label. As the label is typed, it appears in a line above the cells. It is then entered into the cell by moving the cursor away from that cell or by pressing the “Return” key. A number is entered into another cell in the same way. To enter a number but treat it as text, precede the number with a single quotation mark (').

The use of formulas in cells is a useful features of Excel. A formula is entered by typing an equal sign followed by the formula, using the symbol \* (asterisk) for multiplication, / (slash) for division, + (plus) for addition, and – (minus) for subtraction. The caret symbol ^ is used for powers. For example, $3.26^{3/2}$ would be represented by $3.26^{1.5}$ . Don’t use $3.26^{3/2}$ to represent $3.26^{3/2}$ , since the computer carries out operations in a predetermined sequence. Powers are carried out before multiplications and divisions, so the computer would interpret this entry as $3.26^{3/2}$ . Since the formula must be typed on a single line, parentheses are used as necessary to make sure that the operations are carried out correctly, using the rule that all operations inside a pair of parentheses are carried out before being combined with anything else. Other operations are carried out from left to right, with multiplications and divisions carried out before additions and subtractions. If there is any doubt about which operations are carried out first, use parentheses to make the formula unambiguous. If a number or a variable stored in another cell is needed in a formula, one types the address of that cell into the formula in place of the number. A number of common functions can be included in formulas. The following abbreviations must be used. The argument of a function is enclosed in parentheses in place of the ellipsis ( $\cdots$ ), as indicated:

<table><tr><td>Abbreviation</td><td>Function</td></tr><tr><td>SIN(···)</td><td>sine</td></tr><tr><td>COS(···)</td><td>cosine</td></tr><tr><td>EXP(···)</td><td>exponential (e raised to the argument)</td></tr><tr><td>LOG(···)</td><td>common logarithm (base 10)</td></tr><tr><td>LN(···)</td><td>natural logarithm (base e)</td></tr></table>

For example, if you want the cell to contain the natural logarithm of the number presently contained in cell B2, you would type =LN(B2) in the cell. Lowercase letters can also be used and LOG10( $\cdots$ ) can also be used for the common logarithm. The argument of the sine and cosine must be expressed in radians. An arithmetic expression can be used as the argument and will automatically be evaluated when the function is evaluated. These rules are similar to those used in the BASIC and FORTRAN programming languages and in Mathematica, a comprehensive mathematical computer package. After the formula is typed one enters it into a cell by pressing the “return” key. When a formula is entered into a cell, the computer will automatically calculate the appropriate number from whatever constants and cell contents are specified and will display the numerical result in the cell. If the value of the number in a cell is changed, any formulas in other cells containing the first cell’s address will automatically recalculate the numbers in those cells.

EXAMPLE 3.6 Enter a formula into cell C1 to compute the sum of the number in cell A1 and the number in cell B2, divide by 2, and take the common logarithm of the result.

SOLUTION ▶ With the cursor in cell C1 we type the following:

$$
= L O G ((A 1 + B 2) / 2)
$$

We then press the “return” key to enter the formula into that cell. If numbers are stored in cells A1 and B2, the numerical answer will appear in cell C1.

EXERCISE 3.8 ▶ Enter a formula into cell D2 that will compute the mean of the numbers in cells A2, B2, and C2.

If you move a formula from one cell to another, any addresses entered as in the above example will change. Such addresses are called relative addresses or relative references. For example, say that the address A1 and the address B2 were typed into a formula placed in cell C1. If this formula is copied and placed into another cell, the address A1 is replaced by the address of whatever cell is two columns to the left of the new location of the formula. The address B2 is replaced by the address of whatever cell is one column to the left and one row below the new location of the formula. This feature is very useful, but you must get used to it. If you want to move a formula to a new cell but still want to refer to the contents of a particular cell, put a dollar sign (\$) in front of the column letter and another dollar sign in front of the row number. For example, \$A\$1 would refer to cell A1 no matter what cell the formula is placed in. Such an address is called a absolute address or an absolute reference.

There is a convenient way to put the same formula or the same number in an entire column or an entire row of a table. Type a formula with the cursor in the topmost cell of a given portion of a column, and then press the “return” key to enter the formula in the first cell. Then select a portion of the column by dragging the cursor down the column (while holding down the mouse button) from the cell containing the formula as far as desired. Then choose the “Fill” command in the “Edit” menu and choose “Down” from a small window that appears. You can also hold down the “Ctrl” key and then type a “d.” When you do this, the cells are all “filled” with the formula. The formulas in different cells will refer to different cells according to the relative addressing explained above. Selecting a given cell will show the formula for that cell, with the addresses that will actually be used. A similar procedure is used to fill a portion of a row by entering the formula in the leftmost cell of a portion of a row, selecting the portion of the row, and using the “Fill” command in the “Edit” menu and choosing “Right” in the next window. The same procedures can be used to fill a column or a row with the same number in every cell.

A block of cells can be selected by moving the cursor to the upper left cell of the block and then moving it to the opposite corner of the block while holding down the mouse button (“dragging” the cursor). You can also drag the cursor in the opposite direction. The contents of the cell or block of cells can then be cut or copied into the clipboard, using the “Cut” command or the “Copy” command in the “Edit” menu. The contents of the clipboard can be pasted into a new location. One selects the upper left cell of the new block of cells and then uses the “Paste” command in the “Edit” menu to paste the clipboard contents into the workbook. If you put something into a set of cells and want to change it, you can select the cells and then choose “Clear” in the “Edit” menu. To clear the cells completely, choose “All” in the window that appears.

Excel has the capability of using routines called “Macros” that can be called inside the spreadsheet. These routines can be programs written in a version of the BASIC programming language called “Visual Basic for Applications.” Macros can be obtained from other sources, such as internet websites, and placed in any spreadsheet.

## Creating Graphs with Excel

Excel can be used to produce graphs of various kinds (Excel refers to graphs as “charts”). We present a procedure to construct a two-dimensional graph using the “Chart Wizard.” The graph is constructed from values of an independent variable in one column values of a dependent variable in another column. These values must first be loaded into the columns. After the values have been loaded into the spreadsheet, you follow the procedure:

1. Save the spreadsheet, and if you want a printed copy of it without the graph, print it now by using the "Print" command in the "File" menu.

2. Select the two columns by dragging the mouse cursor over them. If the two columns are not adjacent, drag the cursor over the first column, and then hold down the "Ctrl" key while dragging the cursor over the second column. The values of the independent variable must be in the column to the left of the other column. Copy and paste a column of values if necessary.

3. Click on the icon for the Chart Wizard in the toolbar at the top of the spreadsheet. It looks like a small bar graph with three bars.

4. A window labeled “Step 1” appears showing different types of graphs to choose from. Most of the graph types plot categories, not values of a variable, on the horizontal axis. That is, the row number is used as the variable on this axis. To put values of a variable on the horizontal axis, choose the type of graph called “XY(Scatter)” by putting the cursor on this icon and clicking. Several types of graphs can now be chosen by clicking on one of five areas on the screen. The topmost area produces a graph with only the data points showing. The one below that produces a graph with the data points and a smooth curve passing nearly through the data points. The one to its right produces a graph with the smooth curve but no data points. The bottom two produce graphs with line segments connecting the data points. Make your choice and click on the “Next” button.

5. Another window labeled “step 2” appears. The range of data is exhibited. You can verify or change the range of cells from which the graph will be made. Click on the “Next” button.

6. A window labeled “step 3” appears. There are several areas on which you can click. These are self-explanatory. For example, you can click on the “Titles” area and then type in a title for the graph and labels for the axes. You can click on the “Axes” area and choose whether you want numeric labels on the axes. You can click on the “Grid lines” area and choose whether you want horizontal and vertical grid lines. You can click on the “Legend” area and decide whether you want a labeled symbol to the right of the graph (the “legend”). For a graph with a single curve, this is superfluous. Click on the “Next” button.

7. A window labeled "Step 4" appears that allows you to choose whether to place the graph in your worksheet or on a separate sheet. If you want to print the graph, choose a separate sheet. After you do this, click on the "Finish" button and the finished graph appears.

Printing a graph in Excel is done by using the “Print” command in the “File” menu in the usual way. You can use the “Print Preview” command in the “File” menu to see on the screen how the printed version will be arranged. You can change this by choosing “Page Setup.”

We illustrate this procedure in the following example

## EXAMPLE 3.7 Find the positive root of the cubic equation

$$
x ^ {3} - 0.6000 x = 0
$$

This cubic equation has three real roots, one of which is obviously at x = 0.

SOLUTION ▶ We open a blank spreadsheet in Excel. We start by making a table of values of the function

$$
f (x) = x ^ {3} - 0.6000 x
$$

in the range $-2 < x < 2$ . We first type the value $-2$ in the cell A1. In cell A2 we type $= A1 + 0.2$ and press "enter." or "return." We then select 20 cells in the first column by dragging the cursor over the cells, starting with the A2 cell and ending with the A21 cell. We press the “d” key while holding down the “Ctrl” key. This fills the first column with 21 values of x ranging from -2 to 2 in increments of 0.2. We then type the formula in cell B1 that will evaluate the polynomial. We type = A1^3 - 0.6 \* A1 and press the “enter” key or the “return” key. This inserts the formula into cell B1 and the places the value of the function (-6.8) in that cell. We then drag the cursor down the B column to B21, and then fill the cells with the formula by pressing the “d” key while holding down the “Ctrl” key. The values of the function appear in column B. Inspection of the values shows that the function changes sign three times in the interval, so all three of the roots lie in this region. We now construct a graph of the function, following the above procedure. Inspection of the graph indicates that there are roots near x = -0.77, at x = 0, and near x = 0.77. To locate the positive root more accurately, we construct a graph with a smaller range of x. We enter 0.77 in cell C1 and enter the formula = C1 + 0.0005 in cell C2. We then fill the formula down to cell C11. We then copy the formula in cell B1 and paste it into cell D1 and then fill the formula down to cell D21. We select columns C and D and make a second graph. This graph is shown in Figure 3.2. The root appears to lie near x = 0.7745.

![[d039c019aa3df9a4f8647b23553e31feb34010083cdf0b85a63b0a6cd78a9aec.jpg]]  
Figure 3.2 ▶ Graph of Example 3.7.

Using a graphical procedure, find the most positive real root of the quar-

tic equation:

$$
x ^ {4} - 4.500 x ^ {3} - 3.800 x ^ {2} - 17.100 x + 20.000 = 0
$$

You will note that the curve in the graph crosses the x axis in only two places. This indicates that two of the four roots are imaginary or complex numbers. Chemists are not usually interested in complex roots to equations.

A spreadsheet such as Excel is a large and powerful program, and can perform many different tasks, most of which are not needed by a physical chemistry student. You can consult the manual provided by the software manufacturer to learn more about Excel. There are also several textbooks listed at the end of the book that are more easily used than the manufacturer's manual.

EXERCISE 3.10 ▶ Using a graphical method, find the two positive roots of the following equation.

$$
e ^ {x} - 3 x = 0.
$$

## 3.3 Numerical Solution of Algebraic Equations

Strictly speaking, one does not solve an equation numerically. One obtains an approximation to a root. However, with a computer or with a hand calculator, it is easy to obtain enough significant digits for almost any purpose.

## Trial and Error

If the equation is written in the form

$$
f (x) = 0
$$

one repeatedly evaluates the function f, choosing different values of x, until f nearly vanishes. When using this method with a hand calculator or a spreadsheet, it is usually possible to adopt a strategy of finding two values of x such that f has different signs for the two values of x, and then to choose values of x within this interval until $f \approx 0$ . If the equation has more than one root, you must either find all of the roots, or must make sure that you have found the one that you want. If the equation has complex roots and if you care about them, you must vary both the real and imaginary parts of x, which can be done by using a computer program that will carry out arithmetic with complex quantities.

EXAMPLE 3.8 Use the method of trial and error to find the positive root of the equation

$$
2 \sin (x) - x = 0
$$

SOLUTION ▶ We let $f(x) = 2 \sin(x) - x$ , which vanishes at the root. It is convenient to use a spreadsheet to carry out the evaluation of the function $f(x)$ . We put the formula in the B column, filling it down to enough rows for the number of times we think we will have to evaluate the function. We then put trial values into column A and inspect the value of the function in column B. We find quickly that $f(1) = 0.68294$ , and that $f(2) = -0.1814$ , so that there must be a root between x = 1 and x = 2. We find that $f(1.5) = 0.49499$ , so the root lies between 1.5 and 2. We find that $f(1.75) = 0.21798$ , so the root is larger than 1.75. However, $f(1.9) = -0.00740$ , so the root is smaller than 1.9. We find that $f(1.89) = 0.00897$ , so the root is between 1.89 and 1.90. We find that $f(1.895) = 0.000809$ and that $f(1.896) = -0.000829$ . To five significant digits, the root is x = 1.8955.

EXERCISE 3.11 ▶ Use the method of trial and error to find the two positive roots of the equation

$$
e ^ {x} - 3 x = 0
$$

to five significant digits. Make a graph of the function to find the approximate locations of the roots.

## The Method of Bisection

This is a systematic variation of the method of trial and error. You start with two values of x for which the function $f(x)$ has opposite signs, and then evaluate the function for the midpoint of the interval and determine which half of the interval contains the root. If the function has the same sign at the midpoint as at the left end of the interval, the root is in the right half of the interval. The midpoint of the half of the original interval containing the root is taken, and it is determined which half of this new interval contains the root. The method is continued, repeating the process until the interval known to contain the root is as small as twice the error you are willing to tolerate. The middle of the last interval is then taken as the approximation to the root.

## Solution of Equations Using Mathematica

Mathematica is a complete mathematics package that can carry out both numerical and symbolic mathematics. Before we discuss the solution of equations using Mathematica, we provide an elementary introduction to the program. When you open Mathematica, a blank “untitled” window appears on the video screen. This window is called a notebook. Mathematica is now ready to accept instructions.

## Numerical Calculations with Mathematica

You can use Mathematica to make numerical calculations much as you would a calculator. In an open notebook, you can type in numbers and symbols for arithmetic operations:

addition: +

subtraction: -

negation: -

division: /

multiplication: blank space or asterisk (\*)

exponentiation: ^

factorial: !

Parentheses are used in the same way as in writing ordinary formulas.

Numbers in scientific notation are entered in a fairly obvious way. To enter $1.234 \times 10^{4}$ , you would type $1.234 \times 10^{4}$ with the space standing for multiplication, or $1.234 \times 10^{4}$ . In the output lines, Mathematica always uses the space for multiplication.

Most of the Mathematica symbols are the same as those used in Excel or various computer programming languages such as BASIC except for the use of a blank space for multiplication. Excel and BASIC use only the asterisk for multiplication. In ordinary formulas, placing two symbols together without a space between them can stand for multiplication. In Mathematica, if you write xy, the software will think you mean a variable called xy, and not the product of x and y. However, you can write either 2x or 2x for 2 times x, but not x2. It is probably best to use the asterisk (\*) for multiplication rather than a space in input statements. Watch for the use of the blank space in output statements. Complex arithmetic is done automatically, using the capital letter I for $\sqrt{-1}$ . Several constants are available by using symbols: Pi, E, I, Infinity, and Degree stand for $\pi$ , e, $i = \sqrt{-1}$ , $\infty$ , and $\pi/180$ (conversion from degrees to radians). The first letter of each symbol must be capitalized.

For example, to obtain $(4.67841 + 3.58731)^{56.3}$ , you type in an open notebook the following expression:

$$
(4.67841 + 3.58731) ^ {56.3}
$$

using the caret (^) to stand for exponentiation. Parentheses are used to determine the sequence of operations. The rule is that all operations inside a pair of parentheses will be carried out before the result is combined with anything else. After finishing your input statement you then press the “Enter” key (the “Enter” key at the far right of the keyboard in the number keypad, not the “Return” key in the main part of the keyboard, which is also labeled “Enter” on some keyboards). Instead of pressing the “Enter” key, you can press the “Return” key in the main part of the keyboard while holding down the “Shift” key (a “Shift-Return”). If you press the “Return” key without the “Shift” key, you are signaling Mathematica that you are continuing one statement onto a second line. When you press the “Enter” key, you are ending a unit called a “cell.”

Mathematica labels each input cell by a number. If you are at the beginning of a notebook, after you press the “Enter” key you will see

In[1]: $=(4.67841+3.58731)^{56.3}$

Mathematica prints input in boldface type. When you press the “Enter” key, it will immediately print out the result, labeling it as output number 1:

Out[1]=4.39443 10 $^{51}$

In this expression, the space before the 10 stands for multiplication, which is standard notation in Mathematica.

On the screen there is now a square bracket at the right of your input and another at the right of the output, as well as a larger square bracket to the right of both of these brackets and encompassing them. The smaller brackets identify the cells. Mathematica assumes that any new cell is an input cell. When you press the “Enter” key, you notify Mathematica that you are ending the input cell, and that you want any expression in the input cell to be evaluated. When Mathematica prints your output, it creates an output cell for the output, and also prints a larger bracket linking the input cell with its output cell. Any Mathematica notebook consists of a sequence of cells, which are numbered sequentially.

Pressing the “Return” key on the main part of a keyboard does not end a cell. If a piece of input requires more than one line, you can press the “Return” key at the end of each line, and then press the “Enter” key or the “Shift-Return” at the end of the cell. You can put several executable statements in the same cell. It is best to separate them by pressing the “Return” key after each statement.

Many functions are available in Mathematica. The names of the functions must be entered with the first letter capitalized and sometimes a letter in the middle capitalized. The other letters must be in lower case and the argument of the function must be enclosed in square brackets, not parentheses. You will have to get used to this. No deviation from the capitalization rule is allowed, and Mathematica will not recognize parentheses instead of brackets. Some common functions are given in Table 3.2. Other functions are described in the book by Wolfram listed at the end of the chapter.

EXERCISE 3.12 ▶

Write Mathematica expressions for the following:

(a) The complex conjugate of (10) $e^{2.657i}$

(b) $\ln (100!) - (100\ln (100) - 100)$

(c) The complex conjugate of $(1 + 2i)^{2.5}$


Mathematica will print out numerical values with any specified number of digits. You enter the letter N followed by the expression, then a comma, and then the number of digits desired. For example, if you want to have the value of $(3.58731)^{56.3}$ to 15 digits, you use the input statement

TABLE 3.2 ▶ Mathematical Functions in Mathematica

<table><tr><td>Symbol</td><td>Function</td><td>Result</td></tr><tr><td>Abs[x]</td><td>absolute value (magnitude) of x</td><td>nonzero constant</td></tr><tr><td>Arg[z]</td><td>argument  $\phi$  of complex expression  $|z|e^{i\phi}$ </td><td>nonzero constant</td></tr><tr><td>ArcCos[x]</td><td>inverse cosine in radians</td><td>constant, 0 &lt; c &lt; π</td></tr><tr><td>ArcSin[x]</td><td>inverse sine in radians</td><td>constant,  $-\frac{\pi}{2} < c < \frac{\pi}{2}$ </td></tr><tr><td>ArcTan[x]</td><td>inverse tangent in radians</td><td>constant,  $-\frac{\pi}{2} < c < \frac{\pi}{2}$ </td></tr><tr><td>Conjugate[z]</td><td>complex conjugate of z = x + iy</td><td>x - iy</td></tr><tr><td>Cos[x]</td><td>cosine of an angle in radians</td><td>constant, -1 &lt; c &lt; 1</td></tr><tr><td>Exp[x]</td><td>exponential function,  $e^x$ </td><td>positive constant</td></tr><tr><td>Im[z]</td><td>imaginary part of complex expression z</td><td>constant</td></tr><tr><td>Log[x]</td><td>natural logarithm (base e)</td><td>constant</td></tr><tr><td>Log[b,x]</td><td>logarithm to the base b</td><td>constant</td></tr><tr><td>n!</td><td>n factorial</td><td>constant</td></tr><tr><td>Random[ ]</td><td>random number generator</td><td>constant, 0 &lt; c &lt; 1</td></tr><tr><td>Re[z]</td><td>real part of complex expression z</td><td>constant</td></tr><tr><td>Round[x]</td><td>closest integer to x</td><td>constant</td></tr><tr><td>Sin[x]</td><td>sine of an angle in radians</td><td>constant, -1 &lt; c &lt; 1</td></tr><tr><td>Sqrt[x]</td><td>square root of x</td><td>constant</td></tr><tr><td>Tan[x]</td><td>tangent of an angle in radians</td><td>constant</td></tr></table>

$$
\mathrm{N} [ 3.58731 ^ {56.3}, 15 ]
$$

and press the "Enter" key. Mathematica will print

$$
\operatorname{In} [ 1 ] := \mathbf {N} [ 3.58731 ^ {\wedge} 56.3, 15 ]
$$

$$
\operatorname{Out} [ 1 ] = 1.7119439046197910 ^ {31}
$$

The entire expression and the number of digits are enclosed in the square brackets following the N. If you do not specify the number of digits, Mathematica will give you a standard number of digits (usually six) for an expression that contains a decimal point. It will give all of the digits if possible for an expression that does not contain a decimal point. If you enter 30!, it will give you the entire value, with 33 digits. If you enter 30., it will give you a value with six digits. However, if you enter Sqrt[3], it will not give you a value, since an exact value of 3 cannot be written with a finite number of digits. It will print Sqrt[3] as output. If you enter

Sqrt[3.], it will give you a value with six digits, and you can also get a six-digit answer by entering N[Sqrt[3]] or Sqrt[3]//N. If you want 20 digits, you can enter N[Sqrt[3],20].

You can refer to the last output cell with a percent sign (\%) or to any other output cell by its number following a percent sign. If you want to refer to output cell number 3, you would type \%3. If you had entered Sqrt[3] and had obtained Sqrt[3] as your output, you could type N[%] and press the enter key to obtain a numerical value with six digits, or could type N[%,15] to obtain a numerical value with 15 digits.

Mathematica statements can contain symbols for stored variables as well as constants. A variable stands for a location in the computer memory in which a numerical value can be stored. Variable names can contain any number of letters and/or digits. However, they cannot begin with a digit. Begin your variable names with a lowercase letter to avoid confusion with Mathematica functions and other Mathematica objects, which always begin with a capital letter. Also remember that xy would represent a variable called xy while x y (with a space between the letters) stands for the product of the two variables x and y.

Values are assigned to variables by using an ordinary equal sign, which stands for an assignment operator. For example, a value of 75.68 would be assigned to the variable x by entering the statement:

$$
\mathrm{x} = 75.68
$$

and pressing the “Enter” key. The variable x will be replaced by the value 75.68 whenever it occurs in a Mathematica expression until a new value is assigned. To remove a value from the variable x, type the statement

$$
\text { Clear } [ x ].
$$

If you are not sure whether a given variable already has a value, use the Clear statement before using the variable.

You can also define one variable in terms of other variables. Assuming that x already has a value, the statement

$$
\mathbf {y} = \mathbf {x} ^ {\wedge} 3
$$

will assign the cube of the value of x to the variable y. The variable y will keep that numerical value until it is explicitly assigned a new value, even if the value of x is changed. You can also define y as a function of x such that the value of y will change if a new value of x is assigned. To do this, you use the second type of equal sign that is used in Mathematica, denoted by the symbol := (a colon followed by an equal sign). The statement

$$
\mathrm{y} := \mathrm{x} ^ {\wedge} 3
$$

will cause y to be evaluated as the cube of whatever value x has at the time of execution. You can see what the value of any variable is at the moment by typing the name of the variable and pressing the Enter key. If you type a question mark followed by the name of the variable and press the Enter key, you can see whether it is defined as a function of other variables.

You can also define a function. For example, if you want to define the function

$$
f = a b c e ^ {- x / y}\tag{3.16}
$$

you can type

where we have used the space to stand for multiplication. You can also type

$$
f [ x _ {-} ] := a ^ {*} b ^ {*} c ^ {*} \text { Exp } [ - x / y ]
$$

The underscore following the symbol for the independent variable in the function expression on the left-hand side of the statement is part of the function definition and must be typed in. Mathematica's second type of equal sign, := (a colon followed by an equal sign), must be used. After defining a function, you can use it in a Mathematica expression, as in the statement

$$
\mathrm{g} = \mathrm{x} ^ {*} \mathrm{f} [ \mathrm{x} ] ^ {*} \mathrm{Cos} [ \mathrm{x} / \mathrm{y} ]
$$

The underline is used only in the definition of the function. It is not used after the symbol for the function's argument in an expression. Note that Mathematica uses square brackets for the argument of a function, not parentheses. The rules of Mathematica must be followed exactly. There is no provision for alternative symbols.

A cell can also be designated as a text cell, allowing Mathematica to be used like a word processor. You can convert any cell to a text cell as follows: first “select” the cell by placing the mouse cursor on the bracket to the right of the cell and pressing on the mouse button (clicking on the bracket). Then type the numeral 7 while depressing the “Alt” key. Mathematica will store text in a text cell, but will not perform any mathematical operations on anything in a text cell. You can delete the contents of any cell by selecting the cell and then choosing “Clear” from the “Edit” menu or typing the letter x while depressing the “Ctrl” key.

## Symbolic Algebra with Mathematica

Mathematica has a powerful capability to carry out symbolic mathematics on algebraic expressions and can solve equations symbolically. In addition to the arithmetic operations, the principal Mathematica statements for manipulating algebraic expressions are Expand[ ], Factor[ ], Simplify[ ], Together[ ], and Apart[ ]. The Expand statement multiplies factors and powers out to give an expanded form of the expression. The following input and output illustrate this action:

In[1]:=Clear[a,x]

$$
\text { Expand } [ (a + x) ^ {3} ]
$$

$$
\operatorname{Out} [ 1 ] = \mathrm{a} ^ {3} + 3 \mathrm{a} ^ {2} \mathrm{x} + 3 \mathrm{a} \mathrm{x} ^ {2} + \mathrm{x} ^ {3}
$$

The Clear statement is included in case a and x had been previously defined as variables with specific values, which would cause Mathematica to return a numerical result instead of a symbolic result.

The Factor statement manipulates the expression into a product of factors. The following input and output illustrate this action:

In[2]:=Clear[y]

$$
\text { Factor } [ 1 + 5 y + 6 y ^ {2} ]
$$

$$
\operatorname{Out} [ 2 ] = (1 + 2 \mathrm{y}) (1 + 3 \mathrm{y})
$$

Note the use of the blank space for multiplication. Note also that the Factor statement does not have its own input line number, because the “Return” key was pressed after the Clear statement, not the “Enter” key. The Simplify statement manipulates an expression into the form that is considered by the rules built into Mathematica to be the simplest form (with the fewest parts). This form might be the factored form or the expanded form, depending on the expression.

The Together statement collects all terms of an expression together over a common denominator, while the Apart statement breaks the expression apart into terms with simple denominators, as in the method of partial fractions. The theorem of partial fractions states that if $Q(x)$ can be factored in the form

$$
Q (x) = \left(a _ {1} x + b _ {1}\right) \left(a _ {2} x + b _ {2}\right) \left(a _ {3} x + b _ {3}\right) \dots \left(a _ {n} x + b _ {n}\right),\tag{3.17}
$$

where all the $a$ 's and $b$ 's are constants and if $P(x)$ is of lower degree than $Q(x)$ , then

$$
\boxed {\frac {P (x)}{Q (x)} = \frac {A _ {1}}{a _ {1} x + b _ {1}} + \frac {A _ {2}}{a _ {2} x + b _ {2}} + \dots + \frac {A _ {n}}{a _ {n} x + b _ {n}},}\tag{3.18}
$$

where $A_{1}, A_{2}, \ldots, A_{n}$ , are all constants.

EXAMPLE 3.9 Write a Mathematica entry that will carry out the decomposition into partial fractions of the expression

$$
\frac {6 x - 30}{x ^ {2} + 3 x + 2}
$$

SOLUTION ▶ The input and output lines are:

In[1]: =Clear[x]

$$
\begin{array}{r l} & \text { Apart } [ (6 x - 30) / (x ^ {2} + 3 x + 2) ] \\ & \text { Out } [ 1 ] = - \frac {36}{1 + x} + \frac {42}{2 + x} \end{array}
$$

EXERCISE 3.13 ▶

stances A and B:

In the study of the rate of the chemical reaction of sub-

$$
a \mathrm{A} + b \mathrm{B} \rightarrow p r o d u c t s
$$

the quotient occurs.

$$
\frac {1}{([ \mathrm{A} ] _ {0} - a x) ([ \mathrm{B} ] _ {0} - b x)}
$$

where $[A]_{0}$ and $[B]_{0}$ are the initial concentrations of A and B, a and b are the stoichiometric coefficients of these reactants, and x is a variable specifying the extent to which the reaction has occurred. Write a Mathematica statement to decompose the denominator into partial fractions.

## Solving Equations with Mathematica

Mathematica can carry out both symbolic and numerical solutions of equations, including single algebraic equations, simultaneous algebraic equations, and differential equations, which we discuss later. Mathematica contains the rules needed for the symbolic solution of polynomial equations up to the fourth degree, and can solve some fifth-degree equations. The principal statements used to solve equations are Solve, FindRoot, Eliminate, and Reduce.

The Solve statement returns symbolic formulas for solutions, if they exist. For example, the input line to solve the equation $ax^2 + bx + c = 0$ is

In[1]: =Solve[a\*x^2+b\*x+c==0,x]

The name of the variable to be solved for must be included at the end of the equation and separated from it by a comma. Mathematica's third kind of equal sign, a double equal sign, must be used in equations to be solved. Another use of this equal sign is in asking Mathematica to test whether an equality if true or false. The resulting output is the standard quadratic formula:

$$
\operatorname{Out} [ 1 ] = \{\{\mathrm{x} \rightarrow \frac {- b - \operatorname{Sqrt} [ b ^ {2} - 4 a c ]}{2 a} \}, \{\mathrm{x} \rightarrow \frac {- b + \operatorname{Sqrt} [ b ^ {2} - 4 a c ]}{2 a} \} \}
$$

Note the use of the arrow symbol ( $\rightarrow$ ).

If no formula can be found for a solution, you can use the FindRoot statement to obtain a numerical value for the root. You must provide a first estimate of the root (a). For example, to find a root for the equation

$$
e ^ {- x} - 0.5 x = 0
$$

with a trial root of $x = 1$ , you type the input statement:

In[1]:=FindRoot[Exp[-x] - 0.5\*x == 0,{x,1}]

and get the output

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
$\operatorname{Out}[1] = \{\mathrm{x}\rightarrow 0.852606\}$
</div>

The trial value of the root is here represented by the 1 following the x in braces (curly parentheses, $\{\cdots\}$ ). If your equation is a polynomial equation, the NSolve statement can be used instead of FindRoot. The NSolve statement does not require a trial root, and will find all roots, while the FindRoot statement will generally cause Mathematica to converge to one root and then stop. If your equation has more than one root, you need to determine whether you have found the desired root and not one of the others.

EXAMPLE 3.10 Using the NSolve statement find the roots of the equation

$$
x ^ {4} - 5 x ^ {3} + 4 x ^ {2} - 3 x + 2 = 0\tag{3.19}
$$

## SOLUTION ▶ We enter the input statement

```python
NSolve[x^4-5 x^3+4 x^2-3 x+2==0,x]
```

```txt
We press the "Enter" key and receive the output
```

```txt
Out[1] = { { x → 0.00442308 - 0.771419ii, }
```

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
$\{\mathrm{x}\to 0.00442308 + 0.771419\mathrm{ii},$
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
$\{\mathrm{x}\to 0.802307\} ,\{\mathrm{x}\rightarrow 4.18885\}\}$
</div>

where Mathematica uses the a symbol that looks like double i (ii with a single dot) to represent the imaginary unit in its output statement. Use a capital I in an input statement containing the square root of -1.

EXERCISE 3.14 ▶ Verify the real solutions in the preceding example by substituting them into the equation.

EXERCISE 3.15 ▶ (a) Use the NSolve statement in Mathematica to find the numerical values of the roots of the equation

$$
x ^ {3} + 5 x - 42 = 0
$$

(b) Use the FindRoot statement to find the real root of the same equation.

## Graphing with Mathematica

Mathematica can produce sophisticated graphs, including two-dimensional graphs and perspective views of three-dimensional graphs. Graphing a function is easier than with Excel, since you do not have to fill columns with values of the variable.

EXAMPLE 3.11 Make a graph of $\sin(x)$ from $x = 0$ to $x = 2\pi$ ,

SOLUTION ▶ One enters the input

Plot[Sin[x],{x,0,2Pi}]

and presses the “Enter” key. The graph appears on the computer screen in an output statement.

The graphic capabilities of Mathematica are very extensive. For example, it makes perspective views of three-dimensional graphs. You can read more about this in the book by Wolfram and in the manual that is supplied with Mathematica.

## Solving Equations Numerically with Excel

Excel is a large and versatile program, and we do not have the space to discuss all of its capabilities. It has the capability to solve equations numerically, using a command called Goal Seek. This command causes the software to change a variable until a defined function of that variable attains a specified value. It uses a method called the Newton-Raphson method, which we will discuss in a later chapter. To find a root of an equation, one must begin with a trial root that is not too far from the desired root. You must find this by graphing or by looking for places where a table of value of the function changes sign, as we did earlier. You type in a trial root in one cell and type in the function of that variable that needs to equal zero (or some other numerical value).

EXAMPLE 3.12 Find the real roots of the equation

$$
x ^ {4} - 5 x ^ {3} + 4 x ^ {2} - 3 x + 2 = 0\tag{3.20}
$$

SOLUTION ▶ This is the same equation that we solved with Mathematica in a previous example, so we know where the real roots are. We pretend that we know only that there is a real root near 1 and a real root near 4. We type in the value 1 in cell A1 and the value 4 in cell A2. We type the following formula in cell B1: =A1^4-5\*A1^3+4\*A1^2-3\*A1+2 and press the "Return" key. We then drag the cursor over cells B1 and B2 and "fill down" by holding down the "Ctrl" key and typing a letter d. We could also select the two cells and choose "Fill Down" in the "Edit" menu. We then select the B1 cell and choose "Goal Seek" from the "Tools" menu. A window appears with three blanks. The first says "Set cell:" and should have B1 in the blank. The second blank says “To value:” and we type in a zero, since we want the function to attain the value zero. The third blank says “By changing cell:” We type in A1, since that is the cell containing our trial root. We click on “OK” and the software quickly finds the root and places it in cell A1. We then select cell B2 and repeat the process, specifying that we want to vary the contents of cell A2.

EXERCISE 3.16 ▶

Use Excel to find the real root of the equation

$$
x ^ {3} + 5 x - 42 = 0\tag{3.21}
$$

![[944c8d253804439b215c55ae227a6d01c7f12e12e2ff87aa2874d348e7835196.jpg]]

## 3.4 Simultaneous Equations: Two Equations with Two Unknowns

The simplest type of simultaneous equations is the set of two equations:

$$
a _ {11} x + a _ {12} y = c _ {1}\tag{3.22}
$$

$$
a _ {21} x + a _ {22} y = c _ {2},\tag{3.23}
$$

where the $a$ 's and the $c$ 's are constants. This set of equations is called linear because the unknowns $x$ and $y$ enter only to the first power, and is called inhomogeneous, because there are constant terms that do not contain $x$ or $y$ . If certain conditions are met, such a set of equations can be solved for a solution set consisting of a single value of $x$ and a single value of $y$ .

## The Method of Substitution

The first step of this method is to manipulate one equation to give one variable as a function of the other. This function then is substituted into the other equation to give an equation in one unknown which can be solved. The result is then substituted into either of the original equations, which is then solved for the second variable.

EXAMPLE 3.13 Use the method of substitution on Eqs. (3.22) and (3.23).

SOLUTION ▶ We solve the first equation for y in terms of x:

$$
y = \frac {c _ {1}}{a _ {12}} - \frac {a _ {11} x}{a _ {12}}\tag{3.24}
$$

We substitute this into the second equation to obtain the linear equation in x:

$$
a _ {21} x + a _ {22} \left(\frac {c _ {1}}{a _ {12}} - \frac {a _ {11} x}{a _ {12}}\right) = c _ {2}\tag{3.25}
$$

$$
a _ {21} x - a _ {22} \frac {a _ {11} x}{a _ {12}} = c _ {2} - a _ {22} \frac {c _ {1}}{a _ {12}}.\tag{3.26}
$$

This contains only $x$ and not $y$ , so it can be solved for $x$ to give the root

$$
x = \frac {c _ {1} a _ {22} - c _ {2} a _ {12}}{a _ {11} a _ {22} - a _ {12} a _ {21}}.\tag{3.27}
$$

This expression can be substituted into one of our original equations and solved for $y$ to yield

$$
y = \frac {c _ {2} a _ {11} - c _ {1} a _ {21}}{a _ {11} a _ {22} - a _ {12} a _ {21}}.\tag{3.28}
$$

EXERCISE 3.17 ▶ Do the algebraic manipulations to obtain the expression for y.

The method of substitution is not limited to two equations and is not limited to linear equations. In the following example, we treat a nonlinear system of two equations:

EXAMPLE 3.14 In the study of the equilibrium of a weak acid in water, the ionization of the water is generally neglected. If we cannot do this, we have the equilibrium equation for the autoionization of water

$$
K _ {w} = \frac {[ \mathrm{H} ^ {+} ]}{c ^ {\circ}} \frac {[ \mathrm{OH} ^ {-} ]}{c ^ {\circ}}
$$

where $\left[H^{+}\right]$ is the molar concentration of hydrogen ions, where $\left[OH^{-}\right]$ is the molar concentration of hydroxide ions and where $K_{w}$ is the equilibrium constant, equal to $1.00 \times 10^{-14}$ at $25^{\circ}C$ . We also have the equilibrium relation for the weak acid

$$
K _ {a} = \frac {\left(\left[ \mathrm{H} ^ {+} \right] / c ^ {\circ}\right) \left(\left[ \mathrm{A} ^ {-} \right] / c ^ {\circ}\right)}{\left[ \mathrm{HA} \right] / c ^ {\circ}}
$$

where [HA] is the molar concentration of the unionized acid and $[A^{-}]$ is the molar concentration of the acid anion. We let c equal the stoichiometric molar concentration of the acid (the concentration that would occur if no ionization occurred). Use the method substitution to obtain a single equation in $[H^{+}]$ .

SOLUTION ▶ We let $x = [H^{+}] / c^{\circ}$ and $y = [OH^{-}] / c^{\circ}$ . We have the relations

$$
\begin{array}{r c l} x & = & y + [ \mathrm{A} ^ {-} ] / c ^ {\circ} \\ {[ \mathrm{HA} ] / c ^ {\circ}} & = & c / c ^ {\circ} - [ \mathrm{A} ^ {-} ] / c ^ {\circ} = c / c ^ {\circ} - x + y \end{array}
$$

so that we have the simultaneous equations

$$
\begin{array}{l} K _ {w} = x y \\ K _ {a} = \frac {x (x - y)}{c / c ^ {\circ} - x + y}, \end{array}
$$

Solving the first equation for $y$ in terms of $x$ and substituting the result into the second equation yields the equation:

$$
K _ {a} = \frac {x (x - K _ {w} / x)}{c / c ^ {\circ} - x + K _ {w} / x},\tag{3.29}
$$

This equation can be multiplied out to yield the cubic equation that we discussed earlier in the chapter.

EXERCISE 3.18 ▶ Solve the pair of simultaneous equations by the method of substitution:

$$
x ^ {2} - 2 x y - x = 0\tag{3.30}
$$

$$
\frac {1}{x} + \frac {1}{y} = 2.\tag{3.31}
$$

Hint. Multiply the second equation by xy before proceeding.


In the preceding exercise there are two solution sets, since the first equation is quadratic in x. When it is solved after substituting to eliminate y, two values of x are found to satisfy the equation, and there is a root in y for each of these. Nonlinear equations are more complicated than linear equations, so we consider only linear equations for the rest of this section.

## The Method of Elimination

This method is used with linear equations. It applies the process of subtracting one equation from another to obtain a simpler equation. That is, the left-hand side of the first equation is subtracted from the left-hand side of the second equation and the right-hand side of the first equation is subtracted from the right-hand side of the second to yield a new equation that is simpler.

EXAMPLE 3.15 Solve the following pair of equations:

$$
\begin{array}{r l} {x + y} & {= 3} \\ {2 x + y} & {= 0.} \end{array}
$$

SOLUTION ▶ We subtract the first equation from the second to obtain

$$
x = - 3.
$$

This is substituted into either of the original equations to obtain

$$
y = 6.
$$

If necessary to get a simpler equation, you can multiply one or both of the equations by constants before taking the difference, and it is possible to add the equations instead of subtracting.

EXERCISE 3.19 ▶

Solve the set of equations

$$
\begin{array}{r l} 3 x + 2 y & = 40 \\ 2 x - y & = 10. \end{array}
$$


## Consistency and Independence in Simultaneous Equations

There are two common difficulties that can arise with pairs of simultaneous equations. These are (1) that the equations might be inconsistent, and (2) that the equations might not be independent. If two equations are inconsistent, there is no solution that can satisfy both of them, and if the equations are not independent, they express the same information, so that there is really only one equation, which can be solved for one variable in terms of the other but cannot be solved to give numerical values for both variables.

EXAMPLE 3.16 Show that the pair of equations is inconsistent:

$$
2 x + 3 y = 15
$$

$$
4 x + 6 y = 45
$$

SOLUTION ▶ We attempt a solution by elimination. We multiply the first equation by 2 and subtract the second from the first, obtaining

$$
0 = - 15
$$

which is obviously not correct. The equations are inconsistent.

EXAMPLE 3.17 Show that the equations are not independent:

$$
3 x + 4 y = 7
$$

$$
6 x + 8 y = 14
$$

SOLUTION ▶ We attempt a solution by elimination, multiplying the first equation by 2. However, this makes the two equations identical, so that if we subtract one from the other, we obtain

$$
0 = 0
$$

which is correct but not useful. We have just one independent equation instead of two, so that we could solve for x in terms of y or for y in terms of x, but not for numerical values of either x or y. If one equation becomes identical to the other when it is multiplied by any constant or function, the two equations are not independent.

We can understand consistency and independence in simultaneous equations by looking at the graphs of the equations. Each of the equations represents y as a function of x. With linear equations, these functions are represented by straight lines. Figure 3.3 shows the two lines representing the two equations of Example 3.15. The two equations are consistent and independent, and the lines cross at the point whose coordinates represent the solution set, consisting of a value of x and a value of y. Figure 3.4 shows the lines representing the two equations of Example 3.16. Since the lines do not cross, there is no solution to this pair of inconsistent equations. A single line represents both of the equations of Example 3.17. Any point on the line satisfies both equations, which are linearly dependent. Consistency and independence are more complicated when we have more than two equations, and we discuss this in a later chapter.

![[06525b1e9ed7caa1f41d04acbc126c7932ddfd19adfb90d65e9c8682af0dbfcf.jpg]]  
Figure 3.3 ▶ Graphical representation of the two consistent and linearly independent equations of Example 3.15.

![[51a5063ab38a9cf4eafd4accc9d52af117e2b83f8631fab7b3815b1d9069e234.jpg]]  
Figure 3.4 ▶ Graphical representation of two inconsistent equations of Example 3.16.

## Homogeneous Linear Equations

The concept of linear dependence is important in the study of homogeneous linear equations. A pair of homogeneous linear equations is similar to those of Eq. (3.22) except that both $c_{1}$ and $c_{2}$ vanish. Consider the set of homogeneous linear equations:

$$
a _ {11} x + a _ {12} y = 0\tag{3.32a}
$$

$$
a _ {21} x + a _ {22} y = 0\tag{3.32b}
$$

We solve both of these equations for $y$ in terms of $x$ :

$$
\begin{array}{l} y = \frac {- a _ {11} x}{a _ {12}} \\ y = \frac {- a _ {21} x}{a _ {22}} \end{array}\tag{3.32c}
$$

(3.32d)

Both of these functions are represented by straight lines with zero intercept. There are two possibilities: Either the lines cross at the origin or they coincide everywhere. In other words, either x = 0, y = 0 is the solution, or else the equations are linearly dependent (are the same equation). The solution x = 0, y = 0 is called a trivial solution. The two equations must be linearly dependent in order for a nontrivial solution to exist. A nontrivial solution consists of specifying y as a function of x, not in finding constant values for both x and y, since there is really only one independent equation.

EXERCISE 3.20 ▶ Determine whether the set of equations has a nontrivial solution, and find the solution if it exists:

$$
\begin{array}{r l} 7 x + 15 y & = 0 \\ 101 x + 195 y & = 0 \end{array}
$$

![[67f1a9e22dddf0441cf3d896865c3c72b9252c50471cc32f8e6e0aba7909d31c.jpg]]

We will return to the discussion of simultaneous equations in Chapter 10.

## Using Mathematica to Solve Simultaneous Equations

The Solve statement can also be used to solve simultaneous equations as well as single equations. The equations are typed inside curly brackets with commas between them, and the variables are listed inside curly brackets. To solve the equations

$$
a x + b y = c\tag{3.33}
$$

$$
g x + h y = k\tag{3.34}
$$

we type the input entry

$$
\text { In } [ 1 ] := \text { Solve } [ \{\mathbf {a} * \mathbf {x} + \mathbf {b} * \mathbf {y} = = \mathbf {c}, \mathbf {g} * \mathbf {x} + \mathbf {h} * \mathbf {y} = = \mathbf {k} \}, \{\mathbf {x}, \mathbf {y} \} ]
$$

Blank spaces could be used instead of the asterisks to denote multiplication. Notice the use of braces to notify Mathematica that we have a list of two equations to be solved. The two variables to be solved for must be included inside curly brackets (braces). The output is

$$
\operatorname{Out} [ 1 ] = \{\{x \rightarrow - \frac {- c h + b k}{- b g + a h}, y \rightarrow - \frac {- c g + a k}{b g - a h} \} \}
$$

which is the expression obtained from Cramer's rule. If numerical values for the coefficients are specified, Mathematica will give the numerical solution set.

EXERCISE 3.21 ▶

Use Mathematica to solve the simultaneous equations

$$
\begin{array}{r l} 2 x + 3 y & = 13 \\ x - 4 y & = - 10 \end{array}\tag{3.35}
$$

![[dd33d5920e4fa9f6107ff5c063abca0b5059bef0458eb30a491a2f8256bb2f72.jpg]]

The Eliminate statement is used to eliminate one or more of the variables in a set of simultaneous equations. For example, to obtain a single equation in x from the set of equations above, you would type the input entry (note the double equal signs):

$$
\text { Eliminate } [ \{a x + b y = = c, g x + h y = = k \}, y ]
$$

and would receive the output:

Out[1]=b k - b g x + a h x == c h we solve this equation for x by typing

Solve[%,x]

and receive the output

$$
\operatorname{Out} [ 2 ] = \{\{x \rightarrow \frac {- c h + b k}{b g - a h} \} \}
$$

## SUMMARY

This chapter has dealt with solving algebraic equations. For a single equation in a single unknown, x, this means finding a value of x or a set of values of x that makes the equation into a correct numerical equation. We have discussed algebraic procedures for finding a solution, as well schemes for finding approximate solutions. If an equation cannot easily be solved, the equation itself can be approximated by neglecting terms that are small compared with other terms or by linearization. Graphical methods and numerical methods can be used to find numerical approximations to solutions. Simultaneous equations in two variables were discussed. If two equations in two unknowns are consistent and are independent, they can be solved for numerical values of the two unknowns. Linear dependence and inconsistency were discussed. The use of Excel and Mathematica to solve equations was introduced.

## PROBLEMS

1. Solve the quadratic equations:

a) $x^{2} - 3x + 2 = 0$

b) $x^{2} - 1 = 0$

c) $x^{2} + 2x + 2 = 0$

2. Solve the following equations by factoring:

$$
\begin{array}{l l} \text {a)} & 4 x ^ {4} - 4 x ^ {2} - x - 1 = 0 \\ \text {b)} & x ^ {3} + x ^ {2} - x - 1 = 0 \\ \text {c)} & x ^ {4} - 1 = 0 \end{array}
$$

3. Find the real roots of the following equations by graphing:

$$
\mathbf {a}) x ^ {3} - x ^ {2} + x - 1 = 0
$$

b) $e^{-x} - 0.5x = 0$

c) $\sin (x) / x - 0.75 = 0$

a) Using Excel, make a properly labeled graph of the function $y(x) = \ln(x) + \cos(x)$ for values of x from 0 to $2\pi$ , at intervals of $\pi/100$ .

b) Repeat part a using Mathematica.

4. When expressed in terms of “reduced variables” the van der Waals equation of state is

$$
\left(P _ {r} + \frac {3}{V _ {r} ^ {2}}\right) \left(V _ {r} - \frac {1}{3}\right) = \frac {8 T _ {r}}{3}\tag{3.36}
$$

a) Using Excel, construct a graph containing three curves of $P_{r}$ as a function of $V_{r}$ : one for $T_{r}=0.8$ , one for $T_{r}=1$ , and one for $T_{r}=1.2$ . Specify the range $0.4 < V_{r} < 2$ .

b) Repeat part a using Mathematica.

5. The following data were taken for the thermal decomposition of $N_{2}O_{3}$ :

$$
\begin{array}{l l l l l l} t / \mathrm{s} & 0 & 184 & 426 & 867 & 1877 \\ [ \mathrm {N_ {2} O_ {3}} ] / \mathrm{mol}   \mathrm{l} ^ {- 1} & 2.33 & 2.08 & 1.67 & 1.36 & 0.72 \end{array}
$$

Using Excel, make three graphs: one with $\ln([N_{2}O_{3}])$ as a function of t, one with $1/[N_{2}O_{3}]$ as a function of t, and one with $1/[N_{2}O_{3}]^{2}$ as a function of t. Determine which graph is most nearly linear. If the first graph is most nearly linear, the reaction is first order; if the second graph is most nearly linear, the reaction is second order, and if the third graph is most nearly linear, the reaction is third order.

6. Write an Excel worksheet that will convert a list of distance measurements in meters to miles, feet, and inches. If the length in meters is typed into a cell in column A, let the corresponding length in miles appear on the same line in column B, the length in feet in column C, and the length in inches in column C.

7. The van der Waals equation of state is

$$
\left(P + \frac {n ^ {2} a}{V ^ {2}}\right) (V - n b) = n R T\tag{3.37}
$$

where a and b are temperature-independent parameters that have different values for each gas. For carbon dioxide, $a = 0.3640 \, Pa m^{6} mol^{-2}$ and $b = 4.267 \times 10^{-5} \, m^{3} mol^{-1}$ .

a) Write this equation as a cubic equation in $V$ .

b) Use the Solve statement in Mathematica to obtain a symbolic solution to the cubic equation. How would you decide which root is the one you want?

c) Use the NSolve statement in Mathematica to find the volume of 1.000 mol of carbon dioxide at P = 1.000 bar (100000 Pa) and T = 298.15 K. Notice that two of the three roots are complex, and must be ignored. Compare your result with the prediction of the ideal gas equation of state.

d) Use the FindRoot statement in Mathematica to find the real root in part c.

e) Repeat part c for $P = 10.000$ bar ( $1.0000 \times 10^{6}$ Pa) and $T = 298.15$ K. Compare your result with the prediction of the ideal gas equation of state.

f) Repeat part c for P = 100.000 bar ( $1.0000 \times 10^{7}$ Pa) and T = 298.15 K. Compare your result with the prediction of the ideal gas equation of state.

g) Make graphs showing the pressure of 1.000 mol of carbon dioxide as a function of the volume for several different temperatures. You can use the statement

$$
\text { PlotRange } - > \{\text { ymin }, \text { ymax } \}
$$

as part of your Plot statement (separate it by commas) to adjust the vertical axis. Note that the symbol -> is typed with two strokes, with - and > separately typed.

h) Change variables to measure volumes in liters and pressures in atmospheres. Repeat parts a–e. Remember to change the value of R to 0.082061 atm K $^{-1}$ mol $^{-1}$ .

8. An approximate equation for the ionization of a weak acid, including consideration of the hydrogen ions from water is $^{2}$

$$
[ \mathrm{H} ^ {+} ] / c ^ {\mathrm{o}} = \sqrt {K _ {a} c / c ^ {\mathrm{o}} + K _ {w}},
$$

where c is stoichiometric acid concentration. This equation is based on the assumption that the concentration of unionized acid is approximately equal to stoichiometric acid concentration. Consider a solution of HCN (hydrocyanic acid) with stoichiometric acid concentration equal to $1.00 \times 10^{-5}$ mol l $^{-1}$ . $K_{a} = 4 \times 10^{-10}$ for HC $_{1}$ N.

a) Calculate $[H^{+}]$ using this equation.

b) Calculate $[H^{+}]$ using Eq. (3.9) and the method of bisection.

c) Calculate $[H^{+}]$ using Eq. (3.11). Comment on your answers.

9. Find the smallest positive root of the equation.

$$
\sinh (x) - x ^ {2} - x = 0.
$$

10. Solve the cubic equation by trial and error, factoring, or by using Mathematica or Excel:

$$
x ^ {3} + x ^ {2} - 4 x - 4 = 0\tag{3.38}
$$

11. Find the real root of the equation

$$
x ^ {2} = e ^ {- x}\tag{3.39}
$$

12. Find the root of the equation

$$
x = 2 \sin (x)\tag{3.40}
$$

13. Find two positive roots of the equation

$$
\ln (x) - 0.200 x = 0\tag{3.41}
$$

14. Find the real roots of the equation

$$
10 x ^ {2} - 2 = \tan (x)\tag{3.42}
$$

15. In the theory of blackbody radiation, the following equation

$$
x = 5 (1 - e ^ {- x})\tag{3.43}
$$

needs to be solved to find the wavelength of maximum spectral radiant emittance. The variable x is

$$
x = \frac {h c}{\lambda_ {\max} k _ {B} T}\tag{3.44}
$$

where $\lambda_{max}$ is the wavelength of maximum spectral radiant emittance, h is Planck's constant, c is the speed of light, $k_{B}$ is Boltzmann's constant, and T is the absolute temperature. Solve the equation numerically for a value of x. Find the value of $\lambda_{max}$ for $T = 6600 K$ . In what region of the electromagnetic spectrum does this value lie?

16. Solve the simultaneous equations by hand, using the method of substitution:

$$
x ^ {2} + x + 3 y = 15\tag{3.45}
$$

$$
3 x + 4 y = 18\tag{3.46}
$$

Use Mathematica to check your result. Since the first equation is a quadratic equation, there will be two solution sets.

17. Stirling's approximation for $\ln (N!)$ is

$$
\ln (N!) \approx \frac {1}{2} \ln (2 \pi N) + N \ln (N) - N\tag{3.47}
$$

a) Determine the validity of this approximation and of the less accurate version

$$
\ln (N!) \approx N \ln (N) - N\tag{3.48}
$$

for several values of $N$ up to $N = 100$ . Use a calculator, Excel, or Mathematica.

b) Use Mathematica for values of N up to 2000.

18. The Dieterici equation of state is

$$
P e ^ {a / V _ {m} R T} (V _ {m} - b) = R T,\tag{3.49}
$$

where P is the pressure, T is the temperature, $V_{m}$ is the molar volume, and R is the ideal gas constant. The constant parameters a and b have different values for different gases. For carbon dioxide, $a = 0.468 \, Pa \, m^{6} \, mol^{-2}$ , $b = 4.63 \times 10^{-5} \, m^{3} \, mol^{-1}$ . Without linearization, find the molar volume of carbon dioxide if $T = 298.15 \, K$ and $P = 10.000 \, atm = 1.01325 \times 10^{6} \, Pa$ . Use the FindRoot statement in Mathematica, Excel, or trial and error.

19. Determine which, if any, of the following sets of equations are inconsistent or linearly dependent. Draw a graph for each set of equations, showing both equations. Find the solution for any set that has a unique solution.

$$
\begin{array}{l l} \mathbf {a}) & x + 3 y = 4 \\ & 2 x + 6 y = 8 \\ \mathbf {b}) & 2 x + 4 y = 24 \\ & x + 2 y = 8 \\ \mathbf {c}) & 3 x _ {1} + 4 x _ {2} = 10 \\ & 4 x _ {1} - 2 x _ {2} = 6 \end{array}
$$

20. Solve the set of equations using Mathematica or by hand with the method of substitution:

$$
\begin{array}{r l} {x ^ {2} - 2 x y + y ^ {2}} & {= 0} \\ {2 x + 3 y} & {= 5} \end{array}
$$

# Mathematical Functions and Differential Calculus

## Preview

In this chapter we discuss the concept of a mathematical function and its relationship to the behavior of physical variables. We define the derivative of a function of one independent variable and discuss its geometric interpretation. We discuss the use of derivatives in approximate calculations of changes in dependent variables and describe their use in finding minimum and maximum values of functions.

## Principal Facts and Ideas

1. A mathematical function of one variable is a rule for obtaining a value of a dependent variable that corresponds to any value of an independent variable.

2. The derivative of a function is a measure of how rapidly the dependent variable changes with changes in the value of the independent variable. If $\Delta y$ is the change in the dependent variable produced by a change $\Delta x$ in the independent variable, then the derivative dy/dx is defined by

$$
\frac {d y}{d x} = \lim _ {\Delta x \rightarrow 0} \frac {\Delta y}{\Delta x}.
$$

3. The derivatives of many simple functions can be obtained by applying a few simple rules, either separately or in combination.

4. A finite increment in a dependent variable, $\Delta y$ , can sometimes be calculated approximately by use of the formula

$$
\Delta y \approx \frac {d y}{d x} \Delta x.
$$

5. Differential calculus can be used to find maximum and minimum values of a function. A relative minimum or maximum value of a variable y which depends on x is found at a point where dy/dx = 0.

## Objectives

After studying this chapter, you should:

1. understand the concept of a mathematical function;

2. be able to obtain a formula for the derivative of any fairly simple function without consulting a table;

3. be able to draw a rough graph of any fairly simple function and locate important features on the graph;

4. be able to find maximum and minimum values of a function of one variable.

## 4.1 Mathematical Functions

In Chapter 2 we introduced trigonometric functions, the logarithm function and the exponential function. We now revisit the concept of a function. Mathematical functions are useful in thermodynamics because thermodynamic variables behave exactly like mathematical functions, with some variables acting as independent variables and others as dependent variables. They are useful in quantum mechanics because all information about the state of a system is contained in a mathematical function called a wave function or state function.

One definition of a mathematical function of one variable is that it is a rule for generating a set of ordered pairs of numbers. This means, for example, that if you have a table with two columns of numbers in it, each number in the first column is associated with the number on the same line the other column. The choice of a number in the first column delivers a unique value from the second column. For example, thermodynamics implies that the temperature is a function of the pressure or that the pressure is a function of the temperature in a system with a single substance and two phases. A physical chemistry student might measure the vapor pressure of liquid ethanol (the pressure of a system containing only liquid ethanol and gaseous ethanol) at ten different temperatures. The student could present the results in a table. In the first column, the student puts the values of the temperature, and on the same line in the second column he or she puts the observed vapor pressure for that temperature.

Let us choose the temperature to be the independent variable. The vapor pressure is then the dependent variable. This means that if we choose a value of the temperature, the function provides the corresponding value of the vapor pressure. This is the important property of a function. It is as though the function says, "You give me a value for the independent variable, and I'll give you the corresponding value of the dependent variable." In this case, we could have chosen the temperature as the dependent variable and the pressure as the independent variable. There are also functions with more than one independent variable. In this case, a value must be specified for each of the independent variables in order for the function to deliver a value of the dependent variable. We discuss this kind of function in Chapter 7.

A two-column table of numerical values is of course not the only way to represent a mathematical function of a single independent variable. Any rule that delivers a value of a dependent variable when a value of an independent variable is specified is a representation of a mathematical function. Two common representations of functions are mathematical formulas and graphs.

## Properties of Functions Representing Physical Variables

We make the following assumptions about the behavior of physical systems:

1. Of the macroscopic variables such as temperature, pressure, volume, density, entropy, energy, and so on, only a certain number (depending on circumstances) can be independent variables. The others are dependent variables, governed by mathematical functions.

2. These mathematical functions are single-valued, except possibly at isolated points. This means that only one value of the dependent variable occurs for a given value of the independent variable.

3. These mathematical functions are continuous and differentiable, except possibly at isolated points. We will discuss later what this statement means.

Although a list of several temperatures and the corresponding several values of the vapor pressure qualifies as a mathematical function, such a function is not useful for other temperatures. We need a representation of the function that will provide a value of the vapor pressure for other temperatures. Although mathematicians frequently have exact representations of their functions, approximate representations of a function must generally be used in physical chemistry. These representations include interpolation between values in a table, use of an approximate curve in a graph, and approximate mathematical formulas. In all these approximate representations of a function we hope to make our rule for generating new values give nearly the same values as the correct function.

We assume that the exact representation of a function describing a property of a physical system is nearly always single-valued. A single-valued function delivers one and only one value of the dependent variable for any given value of the dependent variable. In discussing real functions of real variables, mathematicians will usually not call something a function unless it is single-valued. We also assume that a function describing a property of a physical system is nearly always continuous. If a function is continuous, the dependent variable does not change abruptly if the independent variable changes gradually. If you are drawing a graph of a continuous function, you will not have to draw a vertical step in your curve or take your pencil away from the paper. We define continuity in terms of mathematical limits. We say that a function $f(x)$ is continuous at x = a if

$$
\lim _ {x \rightarrow a ^ {+}} f (x) = \lim _ {x \rightarrow a ^ {-}} f (x) = f (a).\tag{4.1}
$$

If the function is continuous at x = a, as x draws close to a from either direction, $f(x)$ smoothly draws close to $f(a)$ , the value that the function has at x = a. If $f(x)$ approaches a different value if x approaches a from the positive side than it does if it approaches from the negative side, the function is discontinuous at x = a. If $f(x)$ approaches one finite value when x approaches a from the positive side and a different finite value when x approaches a from the negative side, we say that the function has a finite jump discontinuity. Finite jump discontinuities are sometimes called ordinary discontinuities. In some cases, a function that is discontinuous at x = a becomes larger and larger in magnitude without bound (diverges) as x approaches a. For example, consider the tangent function, which becomes larger and larger in the positive direction if its argument (measured in radians) approaches $\pi/2$ from the negative side. It becomes larger and larger in magnitude in the negative direction if its argument approaches $\pi/2$ from the positive direction. Some other functions can diverge in the same direction when the argument of the function approaches some value from either direction. For example, the function $1/x^{2}$ diverges in the positive direction as x approaches zero from either direction.

Some functions that represent physical variables are continuous over the entire range of values of the independent variable. In other cases, they are piecewise continuous. That is, they are continuous except at a number of isolated points, at which discontinuities in the function occur. Figure 4.1 shows schematically the density of a pure substance as a function of temperature at fixed pressure. The density is piecewise continuous. There is a large finite step discontinuity in the density at the boiling temperature, $T_{b}$ , and a smaller finite step discontinuity at the freezing temperature, $T_{f}$ . If T is made to approach $T_{f}$ from the positive side the density smoothly approaches the density of the liquid at $T_{f}$ . If T is made to approach $T_{f}$ from the negative side the density smoothly approaches the density of the solid at this temperature. The system can exist either as a solid or as a liquid at the freezing temperature $T_{f}$ , or the two phases can coexist, each having a different value of the density. The function representing the density is not single-valued at the freezing temperature. A similar situation occurs at the boiling temperature $T_{b}$ . At this temperature the liquid and gas phases can coexist.

If a mathematician wants to discuss a function of a variable x, he or she would write

$$
y = f (x),\tag{4.2}
$$

![[7f2799fb9d19e9cc9304cb5cb79d51334ff6f2574655ba4bc8bb2be187dbeb3a.jpg]]  
Figure 4.1 ▶ The density of a pure substance as a function of temperature (schematic).

![[bfbe51a8eba0b6382e9b0dd79e3fa142c4ee5d3a4d3f4b019d34ec8f8c7cdace.jpg]]

using the letter y to represent the dependent variable and the letter f to represent the function that provides values of y. We will follow a different policy, writing for example for the density as a function of temperature

$$
\rho = \rho (T),\tag{4.3}
$$

where the letter $\rho$ stands both for the density and for the function that provides values of the density. The main reason for this policy is that we have a lot of variables to discuss and only a limited supply of letters.

## Graphical Representations of Functions

One way to communicate quickly the general behavior of a function is with a graph. A rough graph can quickly show the general behavior of a dependent variable. An accurate graph can be read to provide good approximate values of the dependent variable for specific values of the independent variable. A graph containing data points and a curve drawn through or near the points can also reveal the presence of an inaccurate data point.

EXERCISE 4.1 ▶ The following is a set of data for the vapor pressure of ethanol. Plot these points by hand on graph paper, with the temperature on the horizontal axis (the abscissa) and the vapor pressure on the vertical axis (the ordinate). Decide if there are any bad data points. Draw a smooth curve nearly through the points, disregarding any bad points. Use Excel to construct another graph and notice how much work the spreadsheet saves you.

<table><tr><td>Temperature/°C</td><td>Vapor pressure/torr</td></tr><tr><td>25.00</td><td>55.9</td></tr><tr><td>30.00</td><td>70.0</td></tr><tr><td>35.00</td><td>97.0</td></tr><tr><td>40.00</td><td>117.5</td></tr><tr><td>45.00</td><td>154.1</td></tr><tr><td>50.00</td><td>190.7</td></tr><tr><td>55.00</td><td>241.9</td></tr></table>

## Important Families of Functions

There are a number of important families of functions that occur frequently in physical chemistry. A family of functions is a set of related functions. A family of functions is frequently represented by a single formula that contains other symbols besides the one for the independent variable. These quantities are sometimes called parameters. The choice of a set of values for these quantities specifies which member of the family of functions is meant.

## Linear Functions

The following formula represents the family of linear functions:

$$
y = m x + b\tag{4.4}
$$

This is a family of linear functions or first-degree polynomials. In this family, we have a different function for each set of values of the parameters m and b. The graph of each such function is a straight line, so Eq. (4.4) represents a family of different straight lines. The constant b is called the intercept. It equals the value of the function for x = 0. The constant m is called the slope. It gives the steepness of the line, or the relative rate at which the dependent variable changes as the independent variable varies.

Figure 4.2 shows two particular values of x, called $x_{1}$ and $x_{2}$ , and their corresponding values of y, called $y_{1}$ and $y_{2}$ . A line is drawn through the two points. If m > 0, then $y_{2} > y_{1}$ and the line slopes upward to the right. If m < 0, then $y_{2} < y_{1}$ and the line slopes downward to the right.

EXAMPLE 4.1 For a linear function let $y_{1}$ be the value of $y$ corresponding to $x_{1}$ and $y_{2}$ be the value of $y$ corresponding to $x_{2}$ . Show that the slope is given by

$$
m = \frac {y _ {2} - y _ {1}}{x _ {2} - x _ {1}} = \frac {\Delta y}{\Delta x}.\tag{4.5}
$$

where we introduce the common notation for a difference:

$$
\Delta x = x _ {2} - x _ {1}\tag{4.6}
$$

$$
\Delta y = y _ {2} - y _ {1}\tag{4.7}
$$

SOLUTION ▶

$$
y _ {2} - y _ {1} = m x _ {2} + b - (m x _ {1} + b) = m (x _ {2} - x _ {1})
$$

or

$$
m = \frac {y _ {2} - y _ {1}}{x _ {2} - x _ {1}}.
$$

![[232b0be062a209eca9c61c27df48ce2f48c873ad63206578a0d028feb7b396d3.jpg]]  
Figure 4.2 ▶ The graph of the linear function $y = mx + b$ .

![[3af0b6faf98cc7a2546bb154e66f6e84ca43fff15b7400fc26ef4e68d40a7044.jpg]]  
Figure 4.3 ▶ Graph of the quadratic function $y = x^{2} - 3x - 4$ .

Another important property of the slope is that the slope is the tangent of the angle between the horizontal axis and the straight line representing the function

$$
m = \tan (\alpha).\tag{4.8}
$$

The angle $\alpha$ is taken to lie between $-90^{\circ}$ and $90^{\circ}$ and the slope can range from $-\infty$ to $\infty$ .

## Quadratic Functions

Another important family of functions is the quadratic function or second-degree polynomial:

$$
y = a x ^ {2} + b x + c.\tag{4.9}
$$

The graph of a function from this family is a parabola. Figure 4.3 depicts the parabola representing the function

$$
y (x) = x ^ {2} - 3 x - 4\tag{4.10}
$$

Notice that the parabola rapidly rises on both sides of the minimum.

## Trigonometric Functions

There are several families of trigonometric functions. We have already discussed them in Chapter 2. You should be familiar with the graphs of the trigonometric functions that are shown in Figs. 2.2 through 2.4.

## Exponential and Logarithmic Functions

We have also discussed these two families of functions in Chapter 2. You should be familiar with their properties. An important property of the exponential function is that it increases very rapidly for large values of its independent variable. An important property of the logarithm function is that is increases only very slowly for large values of its independent variable.

## Gaussian Functions

Another important family of functions is the family of Gaussian functions, named for Karl Friedrich Gauss (1777–1855), a great German mathematician. A Gaussian function is represented by the formula

$$
y = c e ^ {- (x - \mu) ^ {2} / 2 \sigma^ {2}}.\tag{4.11}
$$

The constant c can be given a specific value to achieve normalization, which we discuss later. The constant $\mu$ is called the mean, and the constant $\sigma$ is called the standard deviation and is a measure of the width of the “hump” in the curve. The graph of this function shown in Fig. 4.4 corresponds to $\mu = 0$ . The curve in this graph is sometimes called a bell-curve.

This function is proportional to the probability that a value of x will occur in a number of statistical applications and is discussed in Chapter 11.

## Generating Approximate Graphs

A graph that represents a function is useful in helping us to visualize the behavior of the function, even if it is only a rough graph. Sketching a rough graph of a function is often useful in understanding the function. The families of functions that we have listed form a repertoire of functions that you can use to generate approximate graphs of functions that are products of other functions. To do this, you need to recognize the factors as members of the families that we have studied and to figure out what a graph of the product of the factors will be like from graphs of the factors. The two most important facts are that if any of the factors vanishes, the product vanishes and that if either factor diverges (becomes infinite) the product diverges.

![[77e8907aecf841fcdfe4f57569d345f149291e7c834c2f4d70c687ced687e4fe.jpg]]  
Figure 4.4 ▶ The graph of the Gaussian function.

EXAMPLE 4.2 Sketch a rough graph of the function

$y = x\cos (\pi x)$

SOLUTION ▶ This function is a product of the function x, which is shown in Fig. 4.5a, and the function $\cos(\pi x)$ , which is shown in Fig. 4.5b. The desired rough graph can be constructed by inspection of the graphs of the two factors. The first thing to do is to find where the function vanishes, using that fact that if either factor vanishes, the product vanishes. The factor x vanishes at the origin and the factor $\cos(x)$ vanishes when $x = \frac{\pi}{2}$ , $\frac{3\pi}{2}$ , and so on. Since the cosine oscillates between -1 and +1, the product oscillates between x and +x. A rough graph of the product is shown in Fig. 4.4c.

![[8d17f402a6aeab575fdb912a4f292e642896213b5061445a089bdcc997bd46e7.jpg]]  
Figure 4.5 ▶ (a) The first factor in the function of Example 4.2. (b) The second factor in the function of Example 4.2. (c) The function of Example 4.2.

EXERCISE 4.2 ▶ Sketch rough graphs of the following functions. Verify your graphs using Excel or Mathematica if possible.

(a) $e^{-x}\sin (x)$

(c) $x^{2}e^{-x / 2}$

(b) $\sin^2 (x) = \sin (x)^2$

(d) $1 / x^{2}$

(e) $(1 - x)e^{-x}$

(f) $xe^{-x^2}$

## 4.2 The Tangent Line and the Derivative of a Function

A function other than a linear function has a graph with a curve other than a straight line. Such a curve has a different direction (different steepness) at different points on the curve.

## The Line Tangent to a Curve

Consider the graph of some nonlinear function of x, as is shown in Fig. 4.6. The figure also shows the line that is tangent to the curve representing the function at $x = x_{1}$ . At most points on such a curve, the tangent to the curve at that point is the line that has the point in common with the curve but does not cross it at that point, as shown in Fig. 4.6. There are points called inflection points at which the tangent line does cross the curve, and we will discuss them later. We can say that the curve at $x = x_{1}$ has the same direction as the tangent line at that point.

If the tangent line is represented by the formula

$$
y = m x + b,
$$

then the slope of the tangent line is equal to m. In the figure, we have labeled another point at $x = x_{2}$ . In addition to the tangent line, the figure includes a horizontal line intersecting the curve at $x = x_{1}$ . At $x = x_{2}$ , the vertical distance from the horizontal line to the tangent line is given by $m(x_{2}-x_{1})=m\Delta x$ , where

![[e9e3d5c63d7a1c6f532956890f08ffb17845ca38566025557d7b0c56d91e1672.jpg]]  
Figure 4.6 ▶ The curve representing the function $y = y(x)$ and its tangent line.

$$
\Delta x = x _ {2} - x _ {1}
$$

The distance $m\Delta x$ is not necessarily equal to the distance from the horizontal line to the curve, which is given by

$$
y \left(x _ {2}\right) - y \left(x _ {1}\right) = y _ {2} - y _ {1} = \Delta y.
$$

EXERCISE 4.3 ▶ Using graph paper plot the curve representing $y = \sin(x)$ for values of x lying between 0 and $\pi/2$ radians. Using a ruler, draw the tangent line at $x = \pi/4$ . By drawing a right triangle on your graph and measuring its sides, find the slope of the tangent line.

There is a case in which the definition of the tangent line to a curve at a point $x_{1}$ is more complicated than in the case shown in Fig. 4.6. In this case, the point $x_{1}$ lies between a region in which the curve is concave downward and a region in which the curve is concave upward. Such a point is called an inflection point. For such a point, we must consider tangent lines at points that are taken closer and closer to $x_{1}$ . As we approach closer and closer to $x_{1}$ from either direction, the tangent line will approach more and more closely to a line that is the tangent line at $x_{1}$ . This line does cross the curve at the point that it shares with the curve.

## The Derivative of a Function

The derivative of a function is a quantity that represents the rate of change of a function and the steepness of the curve in a graph representing the function. Consider a nonlinear function $y = y(x)$ . We have already asserted that $\Delta y$ is not necessarily equal to m $\Delta x$ , where m is the slope of the tangent to the curve. However, if $\Delta x$ is not too large, we can write as an approximation

$$
\Delta y \approx m \Delta x.\tag{4.12}
$$

We divide both sides of Eq. (4.12) by $\Delta x$ and write

$$
m \approx \frac {\Delta y}{\Delta x} = \frac {y (x _ {2}) - y (x _ {1})}{x _ {2} - x _ {1}} = \frac {y _ {2} - y _ {1}}{x _ {2} - x _ {1}}.\tag{4.13}
$$

If the curve is smooth, this equation becomes a better and better approximation as $\Delta x$ becomes smaller, and if we take the mathematical limit as $\Delta x \to 0$ , it becomes exact:

$$
\boxed {m = \lim _ {x _ {2} \rightarrow x _ {1}} \frac {y (x _ {2}) - y (x _ {1})}{x _ {2} - x _ {1}}}.\tag{4.14}
$$

DEFINITION ◆ If the limit in Eq. (4.14) exists and has the same value when $x_{2}$ approaches $x_{1}$ from either side, it is called the derivative of the function at $x = x_{1}$ . If the derivative exists, it is equal to the slope of the tangent line at the given point. The derivative is denoted by the symbol dy/dx. The symbol $y'$ is also used.

![[82f9a0426aa565079d426a79a76060ccb7f70e9af1b67838a6f6dee9360e9545.jpg]]  
Figure 4.7 ▶ A function that is not differentiable at x = a and at y = b.

The symbol $y'$ has the advantage that the value of x at which the derivative is evaluated can easily be specified. If the derivative is to be evaluated at $x_{1}$ , we would write $y'(x_{1})$ . The value of x at which dy/dx is to be evaluated can be denoted by a subscript, as in $(dy/dx)_{x_{1}}$ . The symbol $(dy/dx)$ resembles a fraction, but you should remember that a derivative is not a fraction. It is a limit that a fraction approaches. It is not permissible to cancel what looks like a numerator or a denominator against another factor.

If the limit in Eq. 4.14 does not exist, the function is not differentiable and its derivative does not exist at $x = x_{1}$ . If $y(x)$ has a discontinuity at $x = x_{1}$ , the limit does not exist at that point and a function is not differentiable at that point. A function is also not differentiable at a cusp, which corresponds to a “corner” or abrupt change in direction of a curve representing a function. At a cusp the function is continuous, but the tangent to the curve has different values on the two sides of the cusp. If the function has a cusp at $x = x_{1}$ , the limit has a different value if $x_{2} > x_{1}$ than it does if $x_{2} < x_{1}$ .

Figure 4.7 shows the graph of a function that is discontinuous at x = b and has a cusp at x = a and is not differentiable at these points, although it is differentiable elsewhere in the region shown in the graph.

EXAMPLE 4.3 Decide where the following functions are differentiable and where they are not differentiable:

(a) $y = |x|$

$$
\mathrm{(b)} y = \sqrt {x}.
$$

## SOLUTION ▶

(a) Differentiable everywhere except at $x = 0$ , where there is a cusp. The limit has different values when $x = 0$ is approached from the two different directions.

(b) This function has real values for $x \geq 0$ . It is differentiable for all positive values of $x$ , but the limit does not exist at $x = 0$ , so it is not differentiable at $x = 0$ . The tangent to the curve at $x = 0$ is vertical.

## EXERCISE 4.4 ▶

Decide where the following functions are differentiable.

(a) $y = \frac{1}{1 - x}$

$$
y = x + 2 \sqrt {x} \tag {b}
$$

(c) $y = \tan (x)$

## Derivatives of Specific Functions

Now that we have defined the derivative, we can see how derivatives of particular functions are found by using the definition of the derivative.

EXAMPLE 4.4 Find the derivative of the function

$$
y = y (x) = a x ^ {2}.
$$

## SOLUTION ▶

$$
\begin{array}{r c l} \Delta y & = & y (x _ {2}) - y (x _ {1}) = y _ {2} - y _ {1} = a x _ {2} ^ {2} - a x _ {1} ^ {2} = a (x _ {1} + \Delta x) ^ {2} - a x _ {1} ^ {2} \\ & = & a [ x _ {1} ^ {2} + 2 x _ {1} \Delta x + (\Delta x) ^ {2} ] - a x _ {1} ^ {2} \\ & = & 2 a x _ {1} \Delta x + (\Delta x) ^ {2} \\ \frac {\Delta y}{\Delta x} & = & 2 a x _ {1} + \Delta x. \end{array}
$$

We now take the limit as $x_{2} \rightarrow x_{1} (\Delta x \rightarrow 0)$ . The first term, $2ax_{1}$ is not affected. The second term, $\Delta x$ , vanishes. Thus, if we use the symbol x instead of $x_{1}$

$$
{\frac {d \left(a x ^ {2}\right)}{d x}} = \lim _ {\Delta x \to 0} {\frac {\Delta y}{\Delta x}} = 2 a x.\tag{4.15}
$$

Figure 4.8 shows a graph of the function $y = ax^2$ and a graph of its derivative, $dy / dx = 2ax$ .

This graph exhibits some important general characteristics of derivatives:

1. Where the function has a horizontal tangent line, the derivative is equal to zero.

2. The derivative is positive in regions where the function increases as x increases.

3. A positive derivative is larger when the tangent line is steeper.

4. The derivative is negative where the function decreases as x increases, as it does in this example for negative values of x.

![[e9bd4e9461c3bb04943db5473e0048dfb19fc4b44e4ad75ec86b6c50e4291e82.jpg]]

![[e576e22b2a389988355e1d1794cd70ad3b84efb17b1bb7026fc5a280d9eff64b.jpg]]  
Figure 4.8 ▶ A graph of a function and its derivative.

5. A negative derivative is more negative (has a larger magnitude) when the tangent line is steeper.

The derivative of any differentiable function can be obtained by using the definition of the derivative.

EXERCISE 4.5 ▶ Show that the derivative of $ay(x)$ is equal to $ady/dx$ where $y(x)$ is a differentiable function of $x$ and where $a$ is a constant.

EXERCISE 4.6 ▶ The exponential function can be represented by the following power series

$$
e ^ {b x} = 1 + b x + \frac {1}{2 !} b ^ {2} x ^ {2} + \frac {1}{3 !} b ^ {3} x ^ {3} + \dots + \frac {1}{n !} b ^ {n} x ^ {n} \dots ,
$$

where the ellipsis ( $\cdots$ ) indicates that additional terms follow. The notation $n!$ stands for n factorial, which is defined to equal $n(n-1)(n-2)\ldots(3)(2)(1)$ . Use this representation to derive the expression for the derivative of $e^{bx}$ .

Table 4.1 gives the derivatives of some simple functions, derived in much the same way as Eq. (4.15). Additional derivatives are given in Appendix D.

TABLE 4.1 ▶ Some Elementary Functions and Their Derivatives.\*

<table><tr><td>Function, y = y(x)</td><td>Derivative, dy/dx = y&#x27;(x)</td></tr><tr><td> $ax^n$ </td><td> $nax^{n-1}$ </td></tr><tr><td> $ae^{bx}$ </td><td> $abe^{bx}$ </td></tr><tr><td>a</td><td>0</td></tr><tr><td>a sin (bx)</td><td>ab cos (x)</td></tr><tr><td>a cos (bx)</td><td>-ab sin (bx)</td></tr><tr><td>a ln (x)</td><td>a/x</td></tr></table>

\*In these formulas, $a, b$ , and $n$ are constants. not necessarily integers.

The derivative of a function is the rate of change of the dependent variable with respect to the independent variable. Because it is the slope of the tangent line, it has a large magnitude when the curve is steep and a small magnitude when the curve is nearly horizontal.

EXERCISE 4.7 ▶ Make rough graphs of several functions from Table 4.1. Below each graph, on the same sheet of paper, make a rough graph of the derivative of the same function.

## 4.3 Differentials

In Section 4.2, we talked about a change in a dependent variable produced by a change in an independent variable. If y is a function of x, we wrote in Eq. (4.12)

$$
\Delta y \approx m \Delta x,\tag{4.16}
$$

where $\Delta x = y(x_{2}) - y(x_{1}),\Delta x = x_{2} - x_{1}$ , and $m$ was the slope of the tangent line at $x = x_{1}$ . Using Eq. (4.14) this becomes

$$
\Delta y \approx \left(\frac {d y}{d x}\right) \Delta x.\tag{4.17}
$$

This approximate equality will generally be more nearly correct when $\Delta x$ is made smaller.

EXAMPLE 4.5 Using Eq. (4.17), estimate the change in the pressure of 1.000 mol of an ideal gas at 0°C when its volume is changed from 22.4141 to 21.4141.

SOLUTION ▶ An ideal gas obeys the equation

$$
P = \frac {n R T}{V}\tag{4.18}
$$

so that if n and T are kept fixed, we can differentiate with respect to V:

$$
\begin{array}{r l} \frac {d P}{d V} & = \frac {- n R T}{V ^ {2}} \\ & = \frac {- (1 .000 \mathrm{mol}) (0 .08206 \mathrm{l} \mathrm{atm} \mathrm{mol} ^ {- 1} \mathrm{K} ^ {- 1}) (273 .15 \mathrm{K})}{(22 .414 \mathrm{l}) ^ {2}} \\ & = - 0.0446 \mathrm{atm} \mathrm{l} ^ {- 1}. \end{array}\tag{4.19}
$$

We can approximate an increment in $P$ :

$$
\begin{array}{r l} \Delta P & \approx \left(\frac {d P}{d V}\right) \Delta V = \left(- 0.0446 \mathrm{atm} 1 ^ {- 1}\right) (- 1.0001) \\ & \approx 0.0446 \mathrm{atm}. \end{array}
$$

EXAMPLE 4.6 Determine the accuracy of the result of Example 4.5.

## SOLUTION ▶

$$
\begin{array}{r c l} \Delta P & = & P (21.414 \mathrm{l}) - P (22.414 \mathrm{l}) = 1.0468 \mathrm{atm} - 1.0000 \mathrm{atm} \\ & = & 0.0468 \mathrm{atm}. \end{array}
$$

Our estimate in Example 4.5 was wrong by about 5%. If the change in volume had been 0.1 l, the error would have been about 0.5%.

Since Eq. (4.17) becomes more nearly exact as $\Delta x$ is made smaller, we make it into an exact equation by making $\Delta x$ become smaller than any finite quantity that anyone can name. We do not make $\Delta x$ strictly vanish, but we say that we make it become infinitesimal. That is, we make it smaller in magnitude than any nonzero quantity one might specify. In this limit, $\Delta x$ is called the differential dx and we write

$$
\boxed {d y = \left(\frac {d y}{d x}\right) d x}\tag{4.20}
$$

The infinitesimal quantity dy is the differential of the dependent variable y. It is the change in y that results from the infinitesimal increment dx in x. It is proportional to dx and to the slope of the tangent line, which is equal to dy/dx. Since x is an independent variable, dx is arbitrary, or subject to our control. Since y is a dependent variable, its differential dy is determined by dx, as specified by Eq. (4.20) and is not under our control once we have chosen a value for dx. Note that Eq. (4.20) has the appearance of an equation in which the dx in the denominator is canceled by the dx in the numerator. This cancellation cannot occur, although the equation is valid. The symbol dy/dx is not a fraction or a ratio. It is the limit that a ratio approaches, which is not the same thing.

In numerical calculations, differentials are not of direct use, since they are smaller than any finite quantities that you can specify. Their use lies in the construction of formulas, especially through the process of integration, in which infinitely many infinitesimal quantities are added up to produce something finite. We discuss integration in the next chapter.

EXERCISE 4.8 ▶
t is given by

The number of atoms of a radioactive substance at time

$$
N (t) = N _ {o} e ^ {- t / \tau},
$$

where $N_{o}$ is the initial number of atoms and $\tau$ is the relaxation time. For ${}^{14}C$ , $\tau = 8320y$ . Calculate the fraction of an initial sample of ${}^{14}C$ that remains after 10.0 years, using Eq. (4.17). Calculate the correct fraction and compare it with your first answer.

EXERCISE 4.9 ▶ Assume that $y = 3x^{2} - 4x + 10$ . If x = 4 and $\Delta x = 0.5$ , Find the value of $\Delta y$ using Eq. (4.17). Find the correct value of $\Delta y$ .

## 4.4 Some Useful Facts About Derivatives

In this section we present some useful identities involving derivatives, which, together with the formulas for the derivatives of simple functions presented in Table 4.1, will enable you to obtain the derivative of almost any function that you will encounter in physical chemistry.

## The Derivative of a Product of Two Functions

If $y$ and $z$ are both functions of $x$ ,

$$
\boxed {\frac {d (y z)}{d x} = y \frac {d z}{d x} + z \frac {d y}{d x}.}\tag{4.21}
$$

## The Derivative of the Sum of Two Functions

If $y$ and $z$ are both functions of $x$ ,

$$
\boxed {\frac {d (y + z)}{d x} = \frac {d y}{d x} + \frac {d z}{d x}.}\tag{4.22}
$$

## The Derivative of the Difference of Two Functions

If $y$ and $z$ are both functions of $x$ ,

$$
\boxed {\frac {d (y - z)}{d x} = \frac {d y}{d x} - \frac {d z}{d x}}.\tag{4.23}
$$

## The Derivative of the Quotient of Two Functions

If y and z are both functions of x, and z is not zero.

$$
\boxed {\frac {d (y / z)}{d x} = \frac {x \left(\frac {d y}{d x}\right) - y \left(\frac {d z}{d x}\right)}{z ^ {2}}.}\tag{4.24}
$$

An equivalent result can be obtained by considering y/z to be a product of 1/z and y and using Eq. (4.21),

$$
\boxed {\frac {d}{d x} \left(y \frac {1}{z}\right) = \frac {1}{z} \frac {d y}{d x} - y \frac {1}{z ^ {2}} \frac {d z}{d x}.}\tag{4.25}
$$

Many people think that Eq. (4.25) is more convenient to use than Eq. (4.24).

## The Derivative of a Constant

If $c$ is a constant,

$$
\boxed {\frac {d c}{d x} = 0.}\tag{4.26}
$$

From this follows the simple but important fact:

$$
\boxed {\frac {d (y + c)}{d x} = \frac {d y}{d x}}.\tag{4.27}
$$

If we add any constant to a function, we do not change its derivative.

## The Derivative of a Function Times a Constant

If $y$ is a function of $x$ and $c$ is a constant,

$$
\boxed {\frac {d (c y)}{d x} = c \frac {d y}{d x}}.\tag{4.28}
$$

This can be deduced by substituting into the definition of the derivative, or by using Eqs. (4.21) and (4.26).

## The Derivative of a Function of a Function (the Chain Rule)

If $u$ is a differentiable function of $x$ , and $f$ is a differentiable function of $u$ ,

$$
\boxed {\frac {d f}{d x} = \frac {d f}{d u} \frac {d u}{d x}.}\tag{4.29}
$$

The function f is sometimes referred to as a composite function. It is a function of x, because x is a function of u. Specifying a value of x specifies a value of u, which specifies a value of f. This can be communicated by the notation

$$
f (x) = f [ u (x) ].\tag{4.30}
$$

Here we have used the same letter for the function $f$ whether it is expressed as a function of $u$ or of $x$ .

We now illustrate how these facts about derivatives can be used to obtain formulas for the derivatives of various functions.

EXAMPLE 4.7 Find the derivative of tan(ax) by using the formulas for the derivatives of the sine and cosine.

SOLUTION ▶

$$
\begin{array}{r l} \frac {d}{d x} \tan (a x) & = \frac {d}{d x} \left[ \frac {\sin (a x)}{\cos (a x)} \right] \\ & = \frac {\cos (a x) a \cos (a x) + \sin (a x) a \sin (a x)}{\cos^ {2} (a x)} \\ & = a \left[ \frac {\cos^ {2} (a x) + \sin^ {2} (a x)}{\cos^ {2} (a x)} \right] = \frac {a}{\cos^ {2} (a x)} \\ & = a \sec^ {2} (a x) \end{array}
$$

We have used several trigonometric identities in the solution.

EXAMPLE 4.8 Find dP/dT if $P(T) = ke^{-Q/T}$ .

SOLUTION ▶ Let $u = -Q / T$ . From the chain rule,

$$
\begin{array}{r c l} \frac {d P}{d T} & = & \frac {d P}{d u} \frac {d u}{d T} = k e ^ {u} \frac {Q}{T ^ {2}} \\ & = & k e ^ {- Q / T} \left(\frac {Q}{T}\right). \end{array}
$$

EXERCISE 4.10 ▶ Find the following derivatives. All letters stand for constants except for the dependent and independent variables indicated.

(a) $\frac{dy}{dx}$ , where $y = (ax^2 + bx + c)^{-3/2}$ (b) $\frac{d\ln(P)}{dT}$ , where $P = ke^{-Q/T}$

(c) $\frac{dy}{dx}$ , where $y = a\cos (bx^3)$

## Newton's Method

This method, which is also called the Newton–Raphson method, is an iterative procedure for obtaining a numerical solution to an algebraic equation. An iterative procedure is one that is repeated until the desired degree of accuracy is attained. The procedure is illustrated in Fig. 4.9. We assume that we have an equation written in the form

$$
f (x) = 0
$$

![[e16d27e93e705f58237d13f215344a14cc396c2d2084ab208ea765b20999ab75.jpg]]  
Figure 4.9 ▶ Graph to illustrate Newton's method.

The process is as follows:

Step 1. Guess at a value, $x_{0}$ , which is “not too far” from the actual root. A rough graph of the function $f(x)$ can help you to choose a good value for $x_{0}$ .

Step 2. Find the value of $f(x)$ and the value of $df / dx$ at $x = x_0$ .

Step 3. Using the value of $f(x)$ and $df / dx$ , find the value of $x$ at which the tangent line to the curve at $x = x_0$ crosses the axis. This value of $x$ , which we call $x_1$ , is our next approximation to the root. It is given by

$$
x _ {1} = x _ {0} - \frac {f (x _ {0})}{f ^ {\prime} (x _ {0})},\tag{4.31}
$$

where we use the notation

$$
f ^ {\prime} (x _ {0}) = \left. \frac {d f}{d x} \right| _ {x = x _ {0}}.
$$

for the derivative evaluated at $x = x_0$ .

Step 4. Repeat the process until you are satisfied with the accuracy obtained. The nth approximation is given by

$$
\boxed {x _ {n} = x _ {n - 1} - \frac {f (x _ {n - 1})}{f ^ {\prime} (x _ {n - 1})}}\tag{4.32}
$$

EXERCISE 4.11 ▶ Using the definition of the derivative, show that Eqs. (4.31) and (4.32) are correct.

You must decide when to stop your iteration. If the graph of the function $f(x)$ crosses the x axis at the root, you can probably stop when the difference between $x_{n}$ and $x_{n+1}$ is smaller than the error you can tolerate. However, if the curve becomes tangent to the x axis at the root, the method may converge very slowly near the root. It may be necessary to pick another trial root on the other side of the root and to compare the results from the two iterations. Another possibility is to take the derivative of the function, set that equal to zero, and solve for that root, since the first derivative changes sign if the function is tangent to the x axis.

You should not demand too much of Newton's method. A poor choice of $x_0$ can make the method converge to the wrong root, especially if the function is oscillatory. If your choice of $x_0$ is near a local maximum or a local minimum, the first application of the procedure might give a value of $x_1$ that is nowhere near the desired root. These kinds of problems can be especially troublesome when you are using a computer to do the iterations, because you might not see the values of $x_1$ , $x_2$ , and so on, until the program has finished execution. Remember the first maxim of computing: "Garbage in, garbage out." Carrying out an approximate graphical solution before you start is a good idea so that you can make a good choice for your first approximation to the root and so that you can know if you found the desired root instead of some other root.

EXERCISE 4.12 ▶ Carry out the Newton–Raphson method to find the smallest positive root of the equation

$$
5 x - e ^ {x} = 0\tag{4.33}
$$

Do the calculation by hand or use a spreadsheet. The Goal Seek command in Excel carries out the Newton-Raphson method automatically. See Chapter 3.

## 4.5 Higher-Order Derivatives

Since the derivative of a function is itself a function, a derivative of a differentiable function is usually differentiable. The derivative of a derivative is called a second derivative, and the derivative of a second derivative is called a third derivative, and so on. We use the notation

$$
{\frac {d ^ {2} y}{d x ^ {2}}} = {\frac {d}{d x}} \left({\frac {d y}{d x}}\right)\tag{4.34}
$$

and

$$
\frac {d ^ {3} y}{d x ^ {3}} = \frac {d}{d x} \left(\frac {d ^ {2} y}{d x ^ {2}}\right),\tag{4.35}
$$

and so on. The $n$ th-order derivative is

$$
\frac {d ^ {n} y}{d x ^ {n}} = \frac {d}{d x} \left(\frac {d ^ {n - 1} y}{d x ^ {n - 1}}\right).\tag{4.36}
$$

The notation $y''(x)$ is sometimes used for the second derivative. The third and higher order derivatives are sometimes denoted by a lowercase roman numeral superscript in parentheses, as $y^{(iii)}$ , $y^{(iv)}$ , and so on.

EXAMPLE 4.9 Find $d^{2}y/dx^{2}$ if $y = a \sin(bx)$ .

SOLUTION ▶

$$
\frac {d ^ {2} y}{d x ^ {2}} = \frac {d}{d x} [ a b \cos (b x) ] = - a b ^ {2} \sin (b x).
$$

The result of this example is sometimes useful: the sine is proportional to the negative of its second derivative. The cosine has the same behavior. The exponential function is proportional to all of its derivatives.

EXERCISE 4.13 ▶ Find the second and third derivatives of the following functions. All letters stand for constants except for the indicated dependent and independent variables. Treat all symbols except for the specified independent variable as constants.

(a)

$$
y = y (x) = a x ^ {n}\tag{b}
$$

$$
y = y (x) = a e ^ {b x}
$$

(c) $v_{\mathrm{rms}} = v_{\mathrm{rms}}(T) = \sqrt{\frac{3RT}{M}}$

$$
P = P (V) = \frac {n R T}{(V - n b)} - \frac {a n ^ {2}}{V ^ {2}}\tag{d}
$$

(e) $\eta = \eta (\lambda) = \frac{2\pi hc^2}{\lambda^5(e^{hc / \lambda kT} - 1)}.$


## The Curvature of a Function

Figure 4.10 shows a rough graph of a function in the interval $a < x < g$ .

A rough graph of the first derivative of the function and a rough graph of the second derivative of the function in the interval are also included. Where the function is concave downward, the second derivative is negative, and where the function is concave upward, the second derivative is positive. Where the graph of the function is more sharply curved, the magnitude of the second derivative is larger. The second derivative therefore provides a measure of the curvature of the function curve.

![[4ab11e283f0a5f32278806517ddb13b4809e65c794297eaa8e03399c6bb5278e.jpg]]  
Figure 4.10 ▶ A function and its first and second derivative.

For any function that possesses a second derivative, the curvature $K$ is defined by

$$
K = \frac {d ^ {2} y / d x ^ {2}}{\left[ 1 + \left(\frac {d y}{d x}\right) ^ {2} \right] ^ {3 / 2}}.\tag{4.37}
$$

The curvature is positive if the curve representing the function is concave upward, and is negative if the curve is concave downward. The magnitude of the curvature is equal to the reciprocal of the radius of the circle that fits the curve at that point. If the curvature is larger the circle is smaller. At a point where the first derivative is zero, the curvature is equal to the second derivative. Since the denominator in Eq. (4.37) is always positive, the curvature has the same sign as the second derivative.

EXAMPLE 4.10 Find the curvature of the function $y = x^2$ at $x = 0$ and at $x = 2$ .

SOLUTION ▶

$$
\frac {d ^ {2} y}{d x ^ {2}} = \frac {d}{d x} (2 x) = 2
$$

$$
K = \frac {2}{(1 + 4 x ^ {2}) ^ {3 / 2}} = \left\{ \begin{array}{c l} 2 & \text {at} x = 0 \\ 0.0285 & \text {at} x = 2 \end{array} . \right.
$$

EXERCISE 4.14 ▶

(a) Find the curvature of the function $\cos (x)$ at $x = 0$ and at $x = \pi /2$ .

(b) Find a formula for the curvature of the function

$$
P (V) = \frac {n R T}{V - n b} - \frac {a n ^ {2}}{V ^ {2}},
$$

where n, R, a, b, and T are treated as constants.

## 4.6 Maximum-Minimum Problems

Sometimes you want to find the largest or smallest value that a function attains or approaches in a certain interval, or to find the value of the independent variable at which this happens. The minimum value of a function means the most negative value of the function, not necessarily the smallest magnitude. The maximum value means the most positive value of the function, not necessarily the largest magnitude. Both a maximum and a minimum are called an extremum. If a function happens to be negative in all parts of some interval, the maximum value in that interval will correspond to the smallest magnitude and the minimum value will correspond to the largest magnitude. We now state the fact that enables us to find maximum and minimum values of a differentiable function in a given interval: The minimum or maximum value of a differentiable function in an interval will either occur at an end of the interval or at a point where the first derivative of the function vanishes.

We illustrate the process of finding the maximum and minimum values of a function in an interval in Fig. 4.10. In the interval shown there are three points at which the curve has a horizontal tangent, labeled b, d, and f. The first derivative vanishes at these points. The points at which we might have the maximum value of the function include these three points and the ends of the interval, labeled a and g. At x = f we have a relative minimum, also called a local minimum. At such a point the function has a smaller value than at any other point in the immediate vicinity. At point d we have a relative maximum or a local maximum, at which the function has a larger value than at any other point in the immediate vicinity. The first derivative also vanishes at point b, but this is an inflection point with a horizontal tangent line.

To find the maximum value we must compare the value of the function at point d and at the ends of the interval. Inspection of the graph indicates that the function has a greater value at point d than at the ends of the interval, and this point is the absolute maximum of the function in the interval shown. The possible points for the minimum value of the function are the ends of the interval and point f. Inspection of the graph indicates that the left end of the interval (point a) is the absolute minimum.

In our discussion of Fig. 4.10, we were guided by inspection of the graph. If you don't have a graph, you can distinguish relative minima, relative maxima, and inflection points from each other by finding the sign of the curvature, which is equal to the second derivative at a point with zero first derivative. At a relative minimum, the second derivative is positive. At a relative maximum, the second derivative is negative. At an inflection point with horizontal tangent line, the second derivative vanishes. To find the absolute maximum of a function in an interval, you evaluate the function at each relative maximum and at the ends of the interval and then choose the point with the largest value of the function. To find the absolute minimum of a function in an interval, you evaluate the function at each relative minimum and at the ends of the interval and then choose the point with the smallest (most negative) value.

If you don't want to go to the trouble of evaluating the second derivatives, you can use the following procedure for a differentiable function:

1. Find all the points in the interval at which the first derivative vanishes.

2. Evaluate the function at all of these points and at the ends of the interval. The largest value in the list is the maximum value and the smallest value is the minimum.

If a function is not differentiable at all points in an interval, you must add all points at which the function is not differentiable to your list of possible maxima or minima. For example, there might be a discontinuity or a cusp at which the function has a larger value than at any other point in the interval.

EXAMPLE 4.11 Find the maximum and minimum values of the function

$$
y = x ^ {2} - 4 x + 6
$$

in the interval 0 < x < 5.

SOLUTION ▶ The derivative is

$$
\frac {d y}{d x} = 2 x - 4.
$$

There is only one point at which $dy / dx = 0$ . Call it $x_{m}$ .

$$
2 x _ {m} - 4 = 0 \quad \text { or } \quad x _ {m} = 2.
$$

We evaluate the function at the ends of the interval and at $x = x_{m}$ :

$$
\begin{array}{r c l} {y (0)} & = & 6 \\ {y (x _ {m})} & = & {y (2) = 2} \\ {y (5)} & = & 11. \end{array}
$$

The maximum value of the function is at $x = 5$ , the end of the interval. The minimum value is at $x = 2$ .

EXERCISE 4.15 For the interval $10 < x < 10$ , find the maximum and minimum values of

$$
y = - x ^ {3} + 3 x ^ {2} - 3 x + 8.
$$


EXERCISE 4.16 ▶ The probability that a molecule in a gas will have a speed v is proportional to the function

$$
f _ {v} (v) = 4 \pi \left(\frac {m}{2 \pi k _ {B} T}\right) ^ {3 / 2} v ^ {2} \exp \left(\frac {- v ^ {2}}{2 m k _ {B} T}\right),
$$

where m is the mass of the molecule, $k_{B}$ is Boltzmann's constant, and T is the temperature on the Kelvin scale. The most probable speed is the speed for which this function is at a maximum. Find the expression for the most probable speed and find its value for nitrogen molecules at T = 298 K. Remember to use the mass of a molecule, not the mass of a mole.

EXERCISE 4.17 ▶ According to the Planck theory of black-body radiation, the radiant spectral emittance is given by the formula

$$
\eta = \eta (\lambda) = \frac {2 \pi h c ^ {2}}{\lambda^ {5} (e ^ {h c / \lambda k T} - 1)},
$$

where h is Planck's constant, $k_{B}$ is Boltzmann's constant, c is the speed of light, and T is the temperature on the Kelvin scale. Treat T as a constant and find an equation that will give the wavelength of maximum emittance.

Find the maximum and minimum values of the function

$$
y = x ^ {3} + 4 x ^ {2} - 10 x + 25 \left| x ^ {3} \right|
$$

in the interval -5 < x < 5. Note the cusp at x = 0.


## 4.7 Limiting Values of Functions: L'Hôpital's Rule

We have already defined mathematical limits. The limit of $y$ as $x$ approaches $a$ is denoted by

$$
\lim _ {x \rightarrow a} [ y (x) ]
$$

and is defined as the value that y approaches ever more closely as x approaches ever more closely to a, if such a number exists. The value a is not required to be finite, and a limit such as

$$
\lim _ {x \rightarrow \infty} [ y (x) ]
$$

exists if $y(x)$ approaches more closely to some value as x is made larger and larger without bound. In some cases it matters whether the limit is approached from the right or from the left. This occurs when there is a discontinuity or a cusp at the limiting point. An example of a limit that does not exist is

$$
\lim _ {x \to a} \left(\frac {1}{x - a}\right).\tag{4.38}
$$

As x approaches closer to a, $1/(x - a)$ becomes larger without bound if x approaches a from the right (from values larger than a) and $1/(x - a)$ becomes more negative without bound if x approaches a from the left.

Another limit that does not exist is

$$
\lim _ {x \to \infty} [ \sin (x) ].\tag{4.39}
$$

The sine function continues to oscillate between -1 and 1 as x becomes larger and larger. An example of a limit that does exist as x approaches infinity is

$$
\lim _ {x \rightarrow \infty} (1 - e ^ {- x}) = 1.\tag{4.40}
$$

EXERCISE 4.19 ▶ Decide which of the following limits exist and find the values of those that do exist.

$$
\text { (a) } \lim _ {x \to 0} \left(1 - e ^ {- x}\right)
$$

(c) $\lim_{x\to \pi /2}[x\tan (x)]$

$$
\begin{array}{l} \text {(b)} \lim _ {x \to \infty} \left(e ^ {- x ^ {2}}\right) \\ \text {(d)} \lim _ {x \to 0} \left[ \ln (x) \right]. \end{array}
$$

Sometimes a limit exists but cannot be evaluated in a straightforward way by substituting into the expression the limiting value of the independent variable. For example, if we try to determine the limit

$$
\lim _ {x \rightarrow 0} \left[ \frac {\sin (x)}{x} \right]\tag{4.41}
$$

we find that for x = 0 both the numerator and denominator of the expression vanish. If an expression appears to approach 0/0, it might approach 0, it might approach a finite constant of either sign, or it might diverge in either direction (approach $-\infty$ or $+\infty$ ). The same is true if it appears to approach $\infty/\infty$ or $0 \times \infty$ .

The rule of l'Hôpital provides a way to determine the limit in such cases. This rule can be stated: If the numerator and denominator of a quotient both approach zero or both approach infinity in some limit, the limit of the quotient is equal to the limit of the quotient of the derivatives of the numerator and denominator if this limit exists. That is, if the limits exist, then

$$
\lim _ {x \rightarrow a} \left[ \frac {f (x)}{g (x)} \right] = \lim _ {x \rightarrow a} \left[ \frac {d f / d x}{d g / d x} \right] = \lim _ {x \rightarrow a} \left[ \frac {f ^ {\prime} (x)}{g ^ {\prime} (x)} \right]\tag{4.42}
$$

EXAMPLE 4.12 Find the value of the limit in Eq. (4.41) by use of l'Hôpital's rule.

SOLUTION ▶

$$
\lim _ {x \rightarrow 0} \left[ \frac {\sin (x)}{x} \right] = \lim _ {x \rightarrow 0} \left[ \frac {d \sin (x) / d x}{d x / d x} \right] = \lim _ {x \rightarrow 0} \left[ \frac {\cos (x)}{1} \right] = 1.\tag{4.43}
$$

l'Hôpital's rule does not necessarily give the correct limit if it is applied to a case in which the limit does not appear to approach 0/0 or $\infty/\infty$ or $0 \times \infty$ . One author put it: "As a rule of thumb, l'Hôpital's rule applies when you need it, and not when you do not need it."

If the expression appears to approach $0 \times \infty$ , it can be put into a form that appears to approach 0/0 or $\infty/\infty$ by using the expression for the reciprocal of one factor. In the following example, we use this technique, as well as illustrating the fact that sometimes the rule must be applied more than once in order to find the value of the limit.

EXAMPLE 4.13 Find the limit

$$
\lim _ {x \rightarrow \infty} \left(x ^ {3} e ^ {- x}\right).
$$

SOLUTION ▶

$$
\begin{array}{r l} \lim _ {x \to \infty} \left(x ^ {3} e ^ {- x}\right) & = \lim _ {x \to \infty} \left(\frac {x ^ {3}}{e ^ {x}}\right) = \lim _ {x \to \infty} \left(\frac {3 x ^ {2}}{e ^ {x}}\right) \\ & = \lim _ {x \to \infty} \left(\frac {6 x}{e ^ {x}}\right) = \lim _ {x \to \infty} \left(\frac {6}{e ^ {x}}\right) = 0. \end{array}\tag{4.44}
$$

By applying l'Hôpital's rule n times, we can show

$$
\boxed {\lim _ {x \to \infty} \left(x ^ {n} e ^ {- x}\right) = 0}\tag{4.45}
$$

for any finite value of n. The exponential function $e^{-x}$ approaches zero so rapidly that it overwhelms any finite power of x in the limit that x becomes large.

![[fbcfd75af4a888180450ccd95b9be40022be20c8bc61f902ef03a6dafcc375d2.jpg]]

EXERCISE 4.20 ▶

Investigate the limit

$$
\lim _ {x \to \infty} \left(x ^ {- n} e ^ {x}\right)
$$

for any finite value of $n$ .

![[691f275b1b87e67fc33f78fb0993967025bea5360fa473d4b3694074c6c60e91.jpg]]

Another interesting limit is that of the next example.

EXAMPLE 4.14 Find the limit

$$
\lim _ {x \rightarrow \infty} \left(\frac {\ln (x)}{x}\right).
$$

SOLUTION ▶

$$
\lim _ {x \rightarrow \infty} \left(\frac {\ln (x)}{x}\right) = \lim _ {x \rightarrow \infty} \left(\frac {1 / x}{1}\right) = 0.\tag{4.46}
$$

EXERCISE 4.21

Find the limit

$$
\lim _ {x \rightarrow \infty} \left[ \frac {\ln (x)}{\sqrt {x}} \right].
$$

![[8a0438e0d8bd72c4c7716d72bf613e447212f5780ff30acf5e2aecbf10614f55.jpg]]

EXERCISE 4.22 A collection of N harmonic oscillators at thermal equilibrium at absolute temperature T is shown by statistical mechanics to have the thermodynamic energy

$$
U = \frac {N h \nu}{e ^ {h \nu / k _ {B} T} - 1}\tag{4.47}
$$

where $k_{B}$ is Boltzmann's constant, h is Planck's constant, T is the absolute temperature, and $\nu$ is the vibrational frequency.

(a) Find the limit of $U$ as $\nu \to 0$ .

(b) Find the limit of $U$ as $T \to 0$ .

There are a number of applications of limits in physical chemistry, and l'Hôpital's rule is useful in some of them. $^{1}$

EXERCISE 4.23 ▶ Draw a rough graph of the function

$$
y = \frac {\tan (x)}{x}
$$

in the interval $-\pi < x < \pi$ . Use l'Hôpital's rule to evaluate the function at $x = 0$ .

## SUMMARY

A function is a rule that provides a value for a dependent variable for any given value of a dependent variable. The derivative of a function is another function of the same independent variable, which specifies the rate of change of the first function with respect to the independent variable. The first derivative of the function $y(x)$ is defined by

$$
\frac {d y}{d x} = y ^ {\prime} = \lim _ {x _ {2} \rightarrow x _ {1}} \frac {y (x _ {2}) - y (x _ {1})}{x _ {2} - x _ {1}}
$$

if this limit exists. The derivative is equal to the slope of the tangent line to a curve representing the function. The first derivative vanishes at a relative maximum or minimum and can be used to locate these points. The second derivative is the derivative of the first derivative

$$
\frac {d ^ {2} y}{d x ^ {2}} = \frac {d}{d x} \left(\frac {d y}{d x}\right)
$$

The second derivative determines the curvature of a function. Higher derivatives were defined. Derivatives are useful in applying the rule of l'Hôpital:

$$
\lim _ {x \rightarrow a} \left[ \frac {f (x)}{g (x)} \right] = \lim _ {x \rightarrow a} \left[ \frac {d f / d x}{d g / d x} \right] = \lim _ {x \rightarrow a} \left[ \frac {f ^ {\prime} (x)}{g ^ {\prime} (x)} \right]
$$

## PROBLEMS

1. The sine and cosine functions are represented by the two series

$$
\begin{array}{l} \sin (x) = x - \frac {x ^ {3}}{3 !} + \frac {x ^ {5}}{5 !} - \frac {x ^ {7}}{7 !} + \dots . \\ \cos (x) = 1 - \frac {x ^ {2}}{2 !} + \frac {x ^ {4}}{4 !} - \frac {4 ^ {6}}{6 !} + \dots . \end{array}\tag{4.48}
$$

Differentiate each series to show that

$$
\frac {d \sin (x)}{d x} = \cos (x)
$$

and

$$
\frac {d \cos (x)}{d x} = - \sin (x)
$$

2. The natural logarithm of $1 + x$ is represented by the series

$$
\ln (1 + x) = x - \frac {x ^ {2}}{2} + \frac {x ^ {3}}{3} - \frac {x ^ {4}}{4} \dots (x ^ {2} <   1 \text {   and   } x = 1).
$$

Use the identity

$$
\frac {d \ln (x)}{d x} = \frac {1}{x}.
$$

to find a series to represent $1 / (1 + x)$ .

3. Use the definition of the derivative to derive the formula

$$
\frac {d (y z)}{d x} = y \frac {d z}{d x} + z \frac {d y}{d x}
$$

where $y$ and $z$ are both functions of $x$ .

4. Find the first and second derivatives of the following functions

a) $P = P(V_m) = RT(1 / V_m + B / V_m^2 + C / V_m^3)$ where $R, B,$ and $C$ are constants

b) $G = G(x) = G^{\circ} + RTx\ln (x) + RT(1 - x)\ln (1 - x)$ , where $G^{\circ}, R$ , and $T$ are constants

c) $y = y(x) = a \ln (x^{1/3})$ , where $a$ is a constant

$$
\mathbf {a}) y = y (x) = 3 x ^ {3} \ln (x)
$$

b) $y = y(x) = 1 / (c - x^2)$ , where $c$ is a constant

c) $y = y(x) = ce^{-a\cos (bx)}$ , where $a, b$ , and $c$ are constants

5. Find the first and second derivatives of the following functions.

a) $y = \ln [\tan (2x)]$

$$
\mathbf {b}) y = (1 / x) (1 / (1 + x))
$$

c) $f = f(v) = ce^{-mv^2 / (2kT)}$ where $m, c, k,$ and $T$ are constants

6. Find the first and second derivatives of the following functions.

$$
\mathbf {a}) y = 3 \sin^ {2} (2 x) = 3 \sin (2 x) ^ {2}
$$

b) $y = a_{0} + a_{1}x + a_{2}x^{2} + a_{3}x^{3} + a_{4}x^{4} + a_{5}x^{5}$ , where $a_{0}, a_{1}$ , and so on, are constants

c) $y = a \cos(e^{-bx})$ , where a and b are constants

7. Find the following derivatives and evaluate them at the points indicated.

a) $(dy / dx)_{x = 0}$ if $y = \sin (bx)$ , where $b$ is a constant

b) $(df / dt)_{t = 0}$ if $f = Ae^{-kt}$ , where $A$ and $k$ are constants

8. Find the following derivatives and evaluate them at the points indicated.

a) $(dy / dx)_{x = 1}$ , if $y = (ax^3 + bx^2 + cx + 1)^{-1/2}$ , where $a, b$ , and $c$ are constants

b) $\left(d^2 y / dx^2\right)_{x = 0}$ , if $y = ae^{-bx}$ , where $a$ and $b$ are constants

9. Find the following derivatives

a) $\frac{d(yz)}{dx}$ , where $y = ax^2, z = \sin(bx)$

b) $\frac{dP}{dV}$ , where $P = \frac{nRT}{(V - nb)} - \frac{an^2}{V^2}$

c) $\frac{d\eta}{d\lambda}$ , where $\eta = \frac{2\pi hc^2}{\lambda^5(e^{hc / \lambda kT} - 1)}$

10. The volume of a cube is given by

$$
V = V (a) = a ^ {3},
$$

where a is the length of a side. Estimate the percent error in the volume if a 1% error is made in measuring the length, using the formula

$$
\Delta V \approx \left(\frac {d V}{d a}\right) \Delta a.
$$

Check the accuracy of this estimate by comparing $V(a)$ and $V(1.01a)$ .

11. Draw a rough graph of the function

$$
y = y (x) = e ^ {- | x |}
$$

Is the function differentiable at x = 0? Draw a rough graph of the derivative of the function.

12. Draw a rough graph of the function

$$
y = y (x) = \sin (| x |)
$$

Is the function differentiable at x = 0? Draw a rough graph of the derivative of the function.

13. Draw a rough graph of the function

$$
y = y (x) = \cos (| x |)
$$

Is the function differentiable at x = 0? Draw a rough graph of the derivative of the function.

14. Show that the function $\psi = \psi(x) = A \sin(kx)$ satisfies the equation

$$
\frac {d ^ {2} \psi}{d x ^ {2}} = - k ^ {2} \psi
$$

if $A$ and $k$ are constants.

15. Show that the function $\psi = \psi(x) = \cos(kx)$ satisfies the equation

$$
\frac {d ^ {2} \psi}{d x ^ {2}} = - k ^ {2} \psi
$$

if $A$ and $k$ are constants.

16. Draw rough graphs of the third and fourth derivatives of the function whose graph is given in Fig. 4.10.

17. The Gibbs energy of a mixture of two enantiomorphs (optical isomers of the same substance) is given by

$$
G = G (x) = G ^ {\circ} + R T x \ln (x) + R T \left(x _ {0} - x\right) \ln \left(x _ {0} - x\right)
$$

where $x_{0}$ is the sum of the concentrations of the enantiomorphs and x is the concentration of one of them. $G^{\circ}$ is a constant, R is the gas constant, and T is the temperature. If the temperature is maintained constant, what is the concentration of each enantiomorph when G has its minimum value? What is the maximum value of G in the interval $0 < x < x_{0}$ ?

a) A rancher wants to enclose a rectangular part of a large pasture so that $1.000 km^{2}$ is enclosed with the minimum amount of fence. Find the dimensions of the rectangle that he should choose. The area is

$$
A = x y
$$

but $A$ is fixed at $1.000\mathrm{km}^2$ , so that $y = A / x$ .

b) The rancher now decides that the fenced area must lie along a road and finds that the fence costs \$20 per meter along the road and \$10 per meter along the other edges. Find the dimensions of the rectangle that would minimize the cost of the fence.

18. Using

$$
\Delta y \approx \left(\frac {d y}{d x}\right) \Delta x
$$

show that

$$
e ^ {\Delta x} - 1 \approx \Delta x \quad \mathrm{if} \Delta x \ll 1.
$$

19. The sum of two nonnegative numbers is 100. Find their values if their product plus twice the square of the first is to be a maximum.

20. A cylindrical tank in a chemical factory is to contain $2.000 \, m^{3}$ of a corrosive liquid. Because of the cost of the material, it is desirable to minimize the area of the tank. Find the optimum radius and height and find the resulting area.

21. Find the following limits.

a) $\lim_{x\to \infty}[\ln (x) / x^2 ]$

b) $\lim_{x\to 3}\left[(x^3 -27) / (x^2 -9)\right]$

c) $\lim_{x\to \infty}[x\ln (\frac{1}{1 + x})]$

22. Find the following limits.

a) $\lim_{x\to 0^{+}}\left[\frac{\ln(1 + x)}{\sin(x)}\right]$

b) $\lim_{x\to 0^{+}}[\sin (x)\ln (x)]$

23. Find the following limits

a) $\lim_{x\to \infty}\left(e^{-x^2} / e^{-x}\right)$

b) $\lim_{x\to 0}\left[x^2 /(1 - \cos (2x))\right]$

c) $\lim_{x\to \pi}\left[\sin (x) / \sin (3x / 2)\right].$

24. If a hydrogen atom is in a 2s state, the probability of finding the electron at a distance r from the nucleus is proportional to $4\pi r^{2}\psi_{2s}^{2}$ , where $\psi$ represents the orbital (wave function):

$$
\psi_ {2 s} = \frac {1}{4 \sqrt {2 \pi}} \left(\frac {1}{a _ {0}}\right) ^ {3 / 2} \left(2 - \frac {r}{a _ {0}}\right) e ^ {- r / a _ {0}},
$$

where $a_{0}$ is a constant known as the Bohr radius, equal to $0.529 \times 10^{-10}$ m.

a) Locate the maxima and minima of $\psi_{2s}$ .

b) Draw a rough graph of $\psi_{2s}$ .

c) Locate the maxima and minima of $\psi_{2s}^2$ .

d) Draw a rough graph of $\psi_{2s}^2$ .

e) Locate the maxima and minima of $4\pi r^2\psi_{2s}^2$ .

f) Draw a rough graph of $4\pi r^2\psi_{2s}^2$

25. The thermodynamic energy of a collection of N harmonic oscillators (approximate representations of molecular vibrations) is given by

$$
U = \frac {N h \nu}{e ^ {h \nu / k _ {B} T} - 1}\tag{4.49}
$$

a) Draw a rough sketch of the thermodynamic energy as a function of T.

b) The heat capacity of this system is given by

$$
C = \frac {d U}{d T}.
$$

c) Show that the heat capacity is given by

$$
C = N k _ {B} \left(\frac {h \nu}{k _ {B} T}\right) ^ {2} \frac {e ^ {h \nu / k _ {B} T}}{\left(e ^ {h \nu / k _ {B} T} - 1\right) ^ {2}}.
$$

d) Find the limit of the heat capacity as $T \to 0$ and as $T \to \infty$ . Note that the limit as $T \to \infty$ is the same as the limit $\nu \to 0$ .

e) Draw a graph of $C$ as a function of $T$ .

26. Find the relative maxima and minima of the function $f(x) = x^{3} + 3x^{2} - 2x$ for all real values of x.

27. The van der Waals equation of state is

$$
\left(P + \frac {n ^ {2} a}{V ^ {2}}\right) (V - n b) = n R T
$$

When the temperature of a given gas is equal to its critical temperature, the gas has a state at which the pressure as a function of V at constant T and n exhibits an inflection point at which dP/dV = 0 and $d^{2}P/dV^{2} = 0$ . This inflection point corresponds to the critical point of the gas. Write P as a function of T, V, and n and write expressions for dP/dV and $d^{2}P/dV^{2}$ , treating T and n as constants. Set these two expressions equal to zero and solve the simultaneous equations to find an expression for the pressure at the critical point.

28. Solve the following equations by hand, using the Newton-Raphson method. Verify your results using Excel or Mathematica:

a) $x^{3} - x^{2} + x - 1 = 0$

b) $e^{-x} - 0.5x = 0$

c) $\sin (x) / x - 0.75 = 0$

29. Use the Newton-Raphson method to calculate the pH of a 0.01 molar solution of lactic acid, $C_{3}H_{6}O_{3}$ at $25^{\circ}C$ . The acid dissociation constant, $K_{a}$ , is equal to $1.38 \times 10^{-4}$ at this temperature. Use Eqs. (3.10) and (3.11) to calculate the pH and comment on the accuracy of these two approximations.

# Integral Calculus

## Preview

In this chapter we first discuss the antiderivative, a function that possesses a given derivative. We then define integration as the limit of a summation process and discuss the process of constructing a finite increment in a function from knowledge of its derivative. We discuss the role of the antiderivative as an indefinite integral and the use of tables of indefinite and definite integrals. We discuss several methods of working out integrals without the use of a table. Finally, we discuss the use of integration to find mean values with a probability distribution.

## Principal Facts and Ideas

1. The antiderivative $F(x)$ of a function $f(x)$ is the function such that $dF / dx = f(x)$ .

2. An indefinite integral is the same thing as the antiderivative function.

3. A definite integral is the limit of a sum of terms $f(x)\Delta x$ in the limit that $\Delta x$ approaches zero, where $f(x)$ is the integrand function.

4. A definite integral equals the indefinite integral evaluated at the upper limit minus the indefinite integral evaluated at the lower limit:

$$
\int_ {a} ^ {b} f (x) d x = F (b) - F (a).
$$

5. An improper integral has at least one infinite limit or has an integrand function that is infinite somewhere in the interval of integration. If an improper integral has a finite value it is said to converge. Otherwise it is said to diverge.

6. Analytical methods can be used to transform an integral into a more easily computed form.

7. Numerical methods exist to compute accurate approximations to integrals that cannot be analytically performed.

8. A mean value of a continuously distributed variable can be computed as an integral using a probability distribution.

## Objectives

After studying this chapter, you should be able to:

1. obtain the indefinite integral of an integrand function using a table;

2. calculate a definite integral using the indefinite integral and understand its role as an increment in the antiderivative function;

3. understand the relationship of a definite integral to an area in a graph of the integrand function;

4. obtain an approximate value for a definite integral using numerical analysis;

5. manipulate integrals into tractable forms by use of partial integration, the method of substitution, and the method of partial fractions;

6. calculate mean values of quantities using a probability distribution with one random variable.

## 5.1 The Antiderivative of a Function

In Chapter 4, we discussed the derivative of a function. We consider the inverse problem, finding a function that possesses a specific function as its derivative. We begin with a particular example.

## Position, Velocity, and Acceleration

The position of a particle is represented by its position vector, which we denote by r. If a particle moves only in the vertical direction, we can express its position as a function of time by the z component of this vector, which is a function of time.

$$
z = z (t),\tag{5.1}
$$

The velocity is the derivative of the position vector with respect to time. The velocity is a vector which we denote by v. The z component of the velocity is

$$
v _ {z} = v _ {z} (t) = \frac {d z}{d t}\tag{5.2}
$$

The acceleration is the derivative of the velocity with respect to time, or the second derivative of the position vector. The z component of the acceleration is

$$
a _ {z} = \frac {d v _ {z}}{d t} = \frac {d ^ {2} z}{d t ^ {2}}.\tag{5.3}
$$

The x and y components are defined in the same way if the particle moves in three dimensions.

EXAMPLE 5.1 According to classical mechanics (Newtonian mechanics) particle falling vertically in a vacuum near the surface of the earth has a position given by

$$
z = z (t) = z (0) + v _ {z} (0) t - \frac {g t ^ {2}}{2},
$$

where $z(0)$ is the position at t = 0, $v_{z}(0)$ is the velocity at t = 0, and g is the acceleration due to gravity, $^{a}$ equal to 9.80 m s $^{-2}$ . Find the velocity and the acceleration.

(5.4)

(5.5)

(5.6)

(5.7)

(5.8)

EXAMPLE 5.3 Find the expression for the velocity of a particle falling near the surface of the earth in a vacuum, given that the velocity at t = 1.000 s is $10.00 \, m s^{-1}$ .

SOLUTION ▶ The necessary family of functions is given by Eq. (5.6), with $v_{z}(0) = 19.80 \, \text{m s}^{-1}$ :

$$
v _ {z} (t) = 19.80 \mathrm{ms} ^ {- 1} - (9.80 \mathrm{ms} ^ {- 2}) t.\tag{5.9}
$$

In order to find the position as a function of time, we would need to know the initial position.

EXAMPLE 5.4 Find the antiderivative of

$$
f (x) = a \sin (b x),
$$

where a and b are constants.

SOLUTION ▶ The antiderivative function is, from Table 4.1,

$$
F (x) = - \frac {a}{b} \cos (b x) + c,\tag{5.10}
$$

where $c$ is an arbitrary constant. You can differentiate to verify that

$$
{\frac {d F}{d x}} = f (x).\tag{5.11}
$$

EXERCISE 5.1 ▶

Find the family of functions whose derivative is $ae^{bx}$ .

EXERCISE 5.2 ▶ Find the function whose derivative is $-10e^{-5x}$ and whose value at x = 0 is 10.

## 5.2 The Process of Integration

In the previous examples we have identified an antiderivative function by inspection of the well-known formulas for derivatives. We now consider the general problem of constructing a function that possesses a certain derivative. Say that we have a function $f = f(x)$ , and we want to find its antiderivative function, which we call $F(x)$ . That is,

$$
\frac {d F}{d x} = f (x).\tag{5.12}
$$

We first describe a process of finding the value of $F(x_{1}) - F(x_{0})$ where $x_{0}$ and $x_{1}$ are two values of x and where the value of F at $x = x_{0}$ is known. In Section 4.4, we discussed the approximate calculation of an increment in a function, using the slope of the tangent line, which is equal to the derivative of the function. Equation (4.17) is

$$
\Delta F = F (x _ {1}) - F (x _ {0}) \approx \left(\frac {d F}{d x}\right) _ {x = x _ {0}} \Delta x,\tag{5.13}
$$

![[2c88451a3826f5e1aa133ed24c01b154fd92725dd7f2b59325e178da4339e2f2.jpg]]  
Figure 5.1 ▶ Figure to illustrate Eq. (5.14).

where $\Delta x = x_{1} - x_{0}$ . This approximation becomes more and more nearly exact as $\Delta x$ is made smaller.

If we want the value of F at some point that is not close to $x = x_{0}$ , we can get a better approximation by using Eq. (5.13) several times for smaller values of $\Delta x$ . Say that we want the value of F at $x = x'$ . We divide the interval $(x_{0}, x')$ into n equal subintervals. This is shown in Fig. 5.1, with n equal to 3. We now write

$$
\begin{array}{l} F \left(x ^ {\prime}\right) - F \left(x _ {0}\right) \approx \left(\frac {d F}{d x}\right) _ {x = x _ {0}} \Delta x \\ \qquad + \left(\frac {d F}{d x}\right) _ {x = x _ {1}} \Delta x + \left(\frac {d F}{d x}\right) _ {x = x _ {2}} \Delta x + \dots \\ \qquad + \left(\frac {d F}{d x}\right) _ {x = x _ {n - 1}} \Delta x, \end{array}\tag{5.14}
$$

where $\Delta x$ is the length of each subinterval:

$$
\Delta x = x _ {1} - x _ {0} = x _ {2} - x _ {1} = x _ {3} - x _ {2} = \dots = x ^ {\prime} - x _ {n - 1}.\tag{5.15}
$$

This approximation to $F(x') - F(x_{0})$ is generally a better approximation than the one obtained by multiplying the slope at the beginning of the interval by the length of the whole interval, as you can see in Fig. 5.1. In fact, if we make n fairly large, we can make the approximation nearly exact.

Let us now rewrite Eq. (5.14), using the symbol $f = f(x)$ instead of $dF / dx$ ,

$$
\begin{array}{c} F (x ^ {\prime}) - F (x _ {0}) \approx f (x _ {0}) \Delta x + f (x _ {1}) \Delta x + f (x _ {2}) \Delta x \\ + \dots + f (x _ {n - 1}) \Delta x \end{array}\tag{5.16}
$$

$$
\approx \sum_ {k = 0} ^ {n - 1} f (x _ {k}) \Delta x.\tag{5.17}
$$

In Eq. (5.17), we have introduced the standard notation for a sum, a capital Greek sigma $(\Sigma)$ . The letter k is called the summation index. Its initial value is given under the capital sigma and its final value is given above it. Unless otherwise stated, k is incremented by unity for each term. There are n terms indicated in this sum.

We can use Eq. (5.15) to write

$$
x _ {k} = x _ {0} + k \Delta x\tag{5.18}
$$

and use this in Eq. (5.17):

$$
F (x ^ {\prime}) - F (x _ {0}) \approx \sum_ {k = 0} ^ {n - 1} f (x _ {0} + k \Delta x) \Delta x.\tag{5.19}
$$

We now make Eq. (5.19) into an exact equation by taking the limit as n becomes larger and larger without bound, meanwhile making $\Delta x$ smaller and smaller so that $n \Delta x$ remains fixed and equal to $x' - x_{0}$ .

$$
F (x ^ {\prime}) - F (x _ {0}) = \lim_ {\substack {\Delta x \to 0, n \to \infty , \\ n \Delta x = x ^ {\prime} - x _ {0}}} \left[ \sum_ {k = 0} ^ {n - 1} f (x _ {0} + k \Delta x) \Delta x \right].\tag{5.20}
$$

The limiting value of the right-hand side of Eq. (5.20) is called a definite integral. The function $f(x)$ is called the integrand function. The notation in this equation is cumbersome, so another symbol is used:

$$
\lim_{\substack{\Delta x\to 0, n\to \infty ,\\ n\Delta x = x^{\prime} - x_{0}}}\left[\sum_{k = 0}^{n - 1}f\left(x_{0} + k\Delta x\right) \Delta x\right] = \int_{x_{0}}^{x^{\prime}}f\left(x\right) dx.\tag{5.21}
$$

The integral sign on the right-hand side of Eq. (5.21) is a stretched-out letter “S,” for sum. However, an integral is not just a sum. It is the limit that a sum approaches as the number of terms in the sum becomes infinite in a particular way. The value $x_{0}$ at the bottom of the integral sign is called the lower limit of integration, and the value x at the top is called the upper limit of integration. Equation (5.20) is now

$$
\boxed {F (x ^ {\prime}) - F (x _ {0}) = \int_ {x _ {0}} ^ {x ^ {\prime}} f (x) d x.}\tag{5.22}
$$

The finite increment $F(x') - F(x_0)$ is equal to the sum of infinitely many infinitesimal increments, each given by the differential $dF = (dF/dx)dx = f(x)dx$ evaluated at the appropriate value of x. The integral on the right-hand side of Eq. (5.22) is called a definite integral, because the limits of integration are definite values. Equation (5.22) is often called the fundamental theorem of integral calculus. It is equivalent to saying that a finite increment in F is constructed by adding up infinitely many infinitesimal increments. The antiderivative function F is called the indefinite integral of the integrand function f.

Equation (5.22) is an important equation. In many applications of calculus to physical chemistry, we will be faced with an integral equivalent to the right-hand side of this equation. If we can by inspection or by use of a table find the function F that possesses the function f as its derivative, we can evaluate the function F at the two limits of integration and take the difference to obtain the value of the integral. In other cases, we might not be able to identify the antiderivative function, but can numerically construct a change in its value using this equation.

EXAMPLE 5.5 Find the value of the definite integral

$$
\int_ {0} ^ {\pi} \sin (x) d x.
$$

SOLUTION ▶ From our table of derivatives we find that the antiderivative of $\sin(x)$ is

$$
- \cos (x) + C = F (x),
$$

where C is an arbitrary constant. The integral is the difference between the value of the antiderivative function at the upper limit and at the lower limit:

$$
\begin{array}{r c l} I & = & F (\pi) - F (0) = - \cos (\pi) + C - [ - \cos (0) + C ] \\ & = & - \cos (\pi) + \cos (0) = - (- 1) + 1 = 2. \end{array}
$$

The constant C cancels because it occurs with the same value in both occurrences of the antiderivative function.

This example illustrates an important fact: A definite integral is not a function of its integration variable, called x in this case. Its value depends only on what values are chosen for the limits and on what function occurs under the integral sign. It is called a functional, or a function of a function, because its value depends on what function is chosen for the integrand function.

EXERCISE 5.3 ▶

Find the numerical value of the definite integral

$$
\int_ {0} ^ {1} e ^ {x} d x.
$$


## The Definite Integral as an Area

We will now show that a definite integral is equal in value to an area between the x axis and the curve representing the integrand function in a graph. We return to Eq. (5.17), which gives an approximation to a definite integral. Figure 5.2 shows the situation with n = 3.

The curve in the figure is the curve representing the integrand function $f(x)$ . Each term in the sum is equal to the area of a rectangle with height $f(x_{k})$ and width $\Delta x$ , so that the sum is equal to the shaded area under the bar graph in the figure. As the limit of Eq. (5.20) is taken, the number of bars between $x = x_{0}$ and $x = x'$ becomes larger and larger, while the width $\Delta x$ becomes smaller and smaller. The roughly triangular areas between the bar graph and the curve become smaller and smaller, and although there are more and more of them their total area shrinks to zero as the limit is taken. The integral thus becomes equal to the area bounded by the x axis, the curve of the integrand function, and the vertical lines at the limits $x = x_{0}$ and $x = x'$ .

Figure 5.2 shows a case in which all values of the integrand function are positive. If $x_{0} < x'$ , the increment $\Delta x$ is always taken as positive. If the integrand function is negative in some region, we must take the area in that region as negative.

![[84e9f9463d03694ecd41ade7f8b1c8d2fbb3ca32fb9558046897820ff9c518af.jpg]]  
Figure 5.2 ▶ The area under a bar graph and the area under a curve.

![[842c0273f8e0e908bf50e3afc46400725b06e21ea22fbc2214477c101d976911.jpg]]  
Figure 5.3 ▶ A graph of $f = \sin (x)$ for Example 5.6

EXAMPLE 5.6 Find the area bounded by the x axis and the curve representing

$$
f (x) = \sin (x),
$$

(a) between x = 0 and $x = 2\pi$ .

(b) between $x = 0$ and $x = \pi$

SOLUTION ▶ The graph of the function is shown in Fig. 5.3.

(a)

$$
\begin{array}{r l} \text { area } & = \int_ {0} ^ {\pi} \sin (x) d x = - \cos (\pi) - [ - \cos (0) ] \\ & = 2. \end{array}\tag{b}
$$

$$
\begin{array}{r c l} a r e a & = & \int_ {0} ^ {2 \pi} \sin (x) d x = - \cos (2 \pi) - [ - \cos (0) ] \\ & = & - (1) - [ - (- 1) ] = 0. \end{array}
$$

When we found the value of the integral from the antiderivative function, we omitted the constant term that generally must be present in the antiderivative function. This constant would have canceled out, so we left it out from the beginning.

EXERCISE 5.4 ▶ Find the following areas by computing the values of definite integrals:

(a) The area bounded by the curve representing $y = x^3$ , the positive $x$ axis, and the line $x = 3$ .

(b) The area bounded by the straight line $y = 2x + 3$ , the $x$ axis, the line $x = 1$ , and the line $x = 4$ .

(c) The area bounded by the parabola $y = 4 - x^2$ and the $x$ axis. You will have to find the limits of integration.

![[6efcf961c6dd6906901a437528bf9af946eb3bcd75975a9d635e59b6c30c6891.jpg]]

Before the advent of programmable computers and electronic calculators, numerical approximations to integrals were sometimes made by drawing an accurate graph of the integrand function and directly measuring the appropriate area in the graph. There were three practical ways to do this. One was by simply counting squares on the graph paper. Another was by cutting out the area to be determined and weighing this piece of graph paper and also weighing another piece of known area from the same sheet. A third was by using a mechanical device called a planimeter, which registers an area on a dial after a stylus is moved around the boundary of the area.

Such procedures are now seldom used, since numerical approximations can be done quickly and easily with computer software.

EXERCISE 5.5 ▶ Find the approximate value of the integral

$$
\int_ {0} ^ {1} e ^ {- x ^ {2}} d x
$$

by making a graph of the integrand function and measuring an area.

## Rules about Integrals

The following rules can be understood by considering the relation between integrals and areas in graphs of integrand functions:

1. A definite integral over the interval $(a, c)$ is the sum of the definite integrals over the intervals $(a, b)$ and $(b, c)$ :

$$
\int_ {a} ^ {c} f (x) d x = \int_ {a} ^ {b} f (x) d x + \int_ {b} ^ {c} f (x) d x.\tag{5.23}
$$

This fact is illustrated in Fig. 5.4. The integral on the left-hand side of Eq. (5.23) is equal to the entire area shown, and each of the two terms on the right-hand side is equal to one of the two differently shaded areas that combine to make the entire area.

2. If the two limits of integration are interchanged, the resulting integral is the negative of the original integral. In Eq. (5.22), we assumed that $x_{0} < x'$ , so that $\Delta x$ would be positive. If the lower limit $x_{0}$ is larger than the upper limit of integration $x'$ , $\Delta x$ must be taken as negative, reversing the sign of the area

![[d188a64eee5a2d5203ab033383238812445d5d2c77f7ddccd1ebae9820b8351d.jpg]]  
Figure 5.4 ▶ Figure to illustrate Eq. (5.23).

![[1b2612112cd420ffa5a9c61f37e43f9effce951ebe64c1a17366fd214b7f0425.jpg]]  
Figure 5.5 ▶ An integrand function that is discontinuous at x = b.

in the graph. Therefore,

$$
\int_ {a} ^ {b} f (x) d x = - \int_ {b} ^ {a} f (x) d x.\tag{5.24}
$$

Use of this fact makes Eq. (5.23) usable for any real values of a, b, and c. It is not necessary for b to lie between a and c.

3. The presence of a finite step discontinuity in an integrand function does not prevent us from carrying out the process of integration. In this regard, integration differs from differentiation. Figure 5.5 illustrates the situation. If the discontinuity is at x = b, we simply apply Eq. (5.23) and find that the integral is given by the integral up to x = b plus the integral from x = b to the end of the interval.

4. If an integrand function consists of a constant times some other function, the constant can be factored out of the integral:

$$
\int_ {a} ^ {b} c f (x) d x = c \int_ {a} ^ {b} f (x) d x.\tag{5.25}
$$

5. An odd function is one that obeys the relation

$$
f (- x) = - f (x).\tag{5.26}
$$

The integral of an odd function from $-c$ to $c$ vanishes, where $c$ is a constant. In this case, the area above the axis exactly cancels the area below the axis, so that

$$
\int_ {- c} ^ {c} f (x) d x = 0 \quad (f (x) \mathrm{odd}),\tag{5.27}
$$

The sine function and the tangent function are examples of odd functions, as defined in Eqs. (2.10) and (2.12).

EXERCISE 5.6 ▶ Draw a rough graph of $f(x) = xe^{-x^{2}}$ and satisfy yourself that this is an odd function. Identify the area in this graph that is equal to the following integral and satisfy yourself that the integral vanishes:

$$
\int_ {- 2} ^ {2} x e ^ {- x ^ {2}} d x = 0.
$$

6. An even function is one that obeys the relation

$$
f (- x) = f (x).\tag{5.28}
$$

The integral of an even function from -c to c is twice the integral from 0 to c. In this case the area between c and 0 is equal to the area between 0 and c, so that

$$
\int_ {- c} ^ {c} f (x) d x = 2 \int_ {0} ^ {c} f (x) d x \quad (f (x) \text {even}),\tag{5.29}
$$

where c is any real constant. The cosine function is an example of an even function.

EXERCISE 5.7 ▶ Draw a rough graph of $f(x) = e^{-x^{2}}$ . Satisfy yourself that this is an even function. Identify the area in the graph that is equal to the definite integral

$$
I _ {1} = \int_ {- 1} ^ {1} e ^ {- x ^ {2}} d x
$$

and satisfy yourself that this integral is equal to twice the integral

$$
I _ {2} = \int_ {0} ^ {1} e ^ {- x ^ {2}} d x.
$$

If you have an integrand that is a product of several factors, you can use the following facts:

a. The product of two even functions is an even function.

b. The product of two odd functions is an even function.

c. The product of an odd function and an even function is an odd function.

The rules about odd and even functions are valid if the function is either even or odd about the center of the integration interval, even if the center of the interval is not at the origin.

EXERCISE 5.8 ▶ The quantum-mechanical wave functions of a particle in a box of length a are either even or odd functions. For example, if the box extends from x = 0 to x = a, the two lowest-energy wave functions are

$$
\psi_ {1} = \sqrt {\frac {2}{a}} \sin \left(\frac {\pi x}{a}\right)
$$

$$
\psi_ {2} = \sqrt {\frac {2}{a}} \sin \left(\frac {2 \pi x}{a}\right)
$$

(a) By drawing rough graphs, satisfy yourself that $\psi_{1}$ is even about the center of the box—that is, $\psi_{1}(x) = \psi_{1}(a - x)$ . Satisfy yourself that $\psi_{2}$ is odd about the center of box.

(b) Draw a rough graph of the product $\psi_1\psi_2$ and satisfy yourself that the integral of this product from $x = 0$ to $x = a$ vanishes.


If the upper limit of a definite integral is considered to be a variable, we can write

$$
{\frac {d}{d b}} \left[ \int_ {a} ^ {b} f (x) d x \right] = f (b),\tag{5.30}
$$

where a is considered to be a constant. If the lower limit is considered to be a variable, we can write

$$
\frac {d}{d a} \left[ \int_ {a} ^ {b} f (x) d x \right] = - f (a),\tag{5.31}
$$

where b is considered to be a constant. If a and b are functions of some variable c (not the variable of integration, x), then

$$
\boxed {\frac {d}{d c} \left[ \int_ {a} ^ {b} f (x) d x \right] = f (b) \frac {d b}{d c} - f (a) \frac {d a}{d c}.}\tag{5.32}
$$

These equations follow from Eq. (5.22). Equation (5.32) also comes from the chain rule, Eq. (4.29), p. 105.

## 5.3 Indefinite Integrals: Tables of Integrals

Let us consider the upper limit $x'$ in Eq. (5.22) to be variable and the lower limit to be fixed and equal to a:

$$
\int_ {a} ^ {x ^ {\prime}} f (x) d x = F (x ^ {\prime}) + C.
$$

The quantity C is a constant that is equal to $-f(a)$ . It is called the constant of integration. Its value is arbitrary if a is arbitrary. We omit mention of a and write

$$
\int^ {x ^ {\prime}} f (x) d x = F \left(x ^ {\prime}\right) + C.\tag{5.33}
$$

This integral is called an indefinite integral, since the lower limit is unspecified and the upper limit is variable. The indefinite integral is the same as the antiderivative function. Large tables of indefinite integrals have been compiled. Appendix E is a brief version of such a table. In most such tables, the notation of Eq. (5.33) is not maintained. The entries are written in the form

$$
\int f (x) d x = F (x).\tag{5.34}
$$

This equation is an abbreviation for Eq. (5.33). The upper limit and the constant of integration are usually omitted from table entries, and the same symbol is usually used for the variable of integration and for the argument of the integral function F. However, you should remember that an arbitrary constant C can be added to the right-hand side of Eq. (5.34).

The same information is contained in a table of indefinite integrals as is contained in a table of derivatives. However, we can get by with a fairly short table of derivatives, since we have the chain rule and other facts listed in Section 4.4. Antiderivatives are harder to find, so it is good to have a separate table of indefinite integrals, arranged so that similar integrand functions occur together.

EXAMPLE 5.7 Using a table, find the indefinite integrals:

$$
\int {\frac {d x}{a ^ {2} + x ^ {2}}}\tag{a}
$$

$$
\int x \sin^ {2} (x) d x \tag {b}\tag{c}
$$

$$
\int x e ^ {a x} d x
$$

SOLUTION ▶ From Appendix E or any published table of indefinite integrals,

$$
\int^ {x ^ {\prime}} \frac {d x}{a ^ {2} + x ^ {2}} = \frac {1}{a} \arctan \left(\frac {x ^ {\prime}}{a}\right) + C\tag{a}
$$

(b)

$$
\begin{array}{l} \int^ {x ^ {\prime}} x \sin^ {2} (x) d x = \frac {x ^ {\prime 2}}{4} - \frac {x ^ {\prime} \sin (2 x ^ {\prime})}{4} \\ - \frac {\cos (2 x ^ {\prime})}{8} + C \end{array}
$$

$$
\int^ {x ^ {\prime}} x e ^ {a x} d x = \frac {e ^ {a x ^ {\prime}}}{a ^ {2}} (a x ^ {\prime} - 1) + C. \tag {c}
$$

EXERCISE 5.9 ▶ Show by differentiation that the functions on the right-hand sides of the equations in Example 5.7 yield the integrand functions when differentiated.

Since the indefinite integral is the antiderivative function, it is used to find a definite integral in the same way as in Section 5.2. If $x_{1}$ and $x_{2}$ are the limits of the definite integral,

$$
\begin{array}{r l} \int_ {x _ {1}} ^ {x _ {2}} f (x) d x & = \int_ {x _ {1}} ^ {a} f (x) d x + \int_ {a} ^ {x _ {2}} f (x) d x = \int_ {a} ^ {x _ {2}} f (x) d x - \int_ {a} ^ {x _ {1}} f (x) d x \\ & = F (x _ {2}) - C - [ F (x _ {1}) - C ] = F (x _ {2}) - F (x _ {1}). \end{array} \tag {5.35}
$$

Equation (5.35) is the same as Eq. (5.22).

EXAMPLE 5.8 Using a table of indefinite integrals, find the definite integral

$$
\int_ {0} ^ {\pi / 2} \sin (x) \cos (x) d x.
$$

SOLUTION ▶ From Appendix C we find that the indefinite integral is $\sin^{2}(x)/2$ ,

$$
\begin{array}{r l} \int_ {0} ^ {\pi / 2} \sin (x) \cos (x) d x & = \left. \frac {\sin^ {2} (x)}{2} \right| _ {0} ^ {\pi / 2} = \frac {1}{2} \left[ \sin^ {2} \left(\frac {\pi}{2}\right) - \sin^ {2} (0) \right] \\ & = \frac {1}{2} (1 - 0) = \frac {1}{2}. \end{array}
$$

We have used the common notation

$$
F (x) | _ {a} ^ {b} = F (b) - F (a).\tag{5.36}
$$

EXERCISE 5.10 ▶
tegrals.

Using a table of indefinite integrals, find the definite in-

$$
\begin{array}{l} \text {(a)} \int_ {0} ^ {3} \cosh (2 x) d x \\ \text {(c)} \int_ {0} ^ {5} 4 ^ {x} d x. \end{array}
$$

$$
\int_ {1} ^ {2} \frac {\ln (3 x)}{x} d x \tag {b}
$$

In addition to tables of indefinite integrals, there are tables of definite integrals. Some tables are listed at the end of the book, and Appendix F is a short version of such a table. Some of the entries in these tables are integrals that could be worked out by using a table of indefinite integrals, but others are integrals that cannot be obtained as indefinite integrals, but by some particular method can be worked out for one set of limits. An example of such an integral is worked out in Appendix G. Tables of definite integrals usually include only sets of limits such as $(0, 1)$ , $(0, \pi)$ , $(0, \frac{\pi}{2})$ , and $(0, \infty)$ . The last set of limits corresponds to an improper integral, which is discussed in the next section.

## 5.4 Improper Integrals

So far we have assumed that both limits of a definite integral are finite and that the integrand function does not become infinite inside the interval of integration. If either of these conditions is not met, an integral is said to be an improper integral. For example,

$$
I = \int_ {0} ^ {\infty} f (x) d x\tag{5.37}
$$

is an improper integral because its upper limit is infinite. We must decide what is meant by the infinite upper limit in Eq. (5.37), because Eq. (5.20) cannot always be modified by inserting $\infty$ into the equation instead of $x'$ . We define

$$
\int_ {0} ^ {\infty} f (x) d x = \lim _ {b \rightarrow \infty} \int_ {0} ^ {b} f (x) d x.\tag{5.38}
$$

In this mathematical limit, the upper limit of integration becomes larger and larger without bound. Notice that the word “limit” has several definitions, and two of them unfortunately occur here in the same sentence.

If the integral approaches more and more closely to some finite value as the upper limit is made larger and larger, we say that the limit exists and that the improper integral is equal to this finite value. The improper integral is said to converge to the value that is approached. Some improper integrals do not converge. The magnitude of the integral can become larger and larger without bound as the limit of integration is made larger and larger. In other cases, the integral oscillates repeatedly in value as the limit of integration is made larger and larger. We say in both of these cases that the integral diverges.

In addition to the type of improper integral shown in Eq. (5.37), some improper integrals have a lower limit of integration that is made to approach $-\infty$ , while the upper limit is finite. Other improper integrals have a lower limit that is made to approach $-\infty$ , while the upper limit is made to approach $+\infty$ . Just as in the case of Eq. (5.38), if the integral approaches a finite value more and more closely as the limit or limits approach infinite magnitude, the improper integral is said to converge to that value.

Another kind of improper integral has an integrand function that becomes infinite somewhere in the interval of integration. For example,

$$
I = \int_ {0} ^ {1} \frac {1}{x ^ {2}} d x\tag{5.39}
$$

is an improper integral because the integrand function becomes infinite at x = 0. This improper integral is defined by

$$
\int_ {0} ^ {1} \frac {1}{x ^ {2}} d x = \lim _ {a \rightarrow 0 ^ {+}} \int_ {a} ^ {1} \frac {1}{x ^ {2}} d x.\tag{5.40}
$$

Just as in the other cases, if the integral grows larger and larger in magnitude as the limit is taken, we say that it diverges. If the limit exists, we say that the improper integral converges to that limit. The situation is similar if the point at which the integrand becomes infinite is at the upper limit of integration. If it is within the interval of integration, break the interval into two subintervals so that the point at which the integrand function diverges is at the lower limit of one subinterval and at the upper end of the other subinterval.

The two principal questions that we need to ask about an improper integral are:

1. Does it converge?

2. If so, what is its value?

EXAMPLE 5.9 Determine whether the following improper integral converges, and if so, find its value:

$$
\int_ {0} ^ {\infty} e ^ {- x} d x.
$$

SOLUTION ▶

$$
\begin{array}{r l} \int_ {0} ^ {\infty} e ^ {- x} d x & = \lim _ {b \to \infty} \int_ {0} ^ {b} e ^ {- x} d x = \lim _ {b \to \infty} \left[ - e ^ {- x} \right] \bigg | _ {0} ^ {b} \\ & = \lim _ {b \to \infty} - (e ^ {- b} - 1) = 0 + 1 = 1. \end{array}
$$

The integral converges to the value 1.

EXERCISE 5.11 ▶ Determine whether each of the following improper integrals converges, and if so, determine its value:

(a) $\int_0^1\left(\frac{1}{x}\right)dx$

(b) $\int_0^\infty \sin (x)dx$

(c) $\int_0^\infty \left(\frac{1}{1 + x}\right)dx$

(d) $\int_0^\infty \frac{1}{x^3} dx$

(e) $\int_{-\infty}^{0} e^x dx$

## 5.5 Methods of Integration

In this section, we discuss three methods that can be used to transform an integral that is not exactly like any integral you can find in a table into one that is.

## The Method of Substitution

In this method a change of variables is performed in order to obtain a simpler integral. The integrand function is expressed in terms of the new independent variable, which then becomes the variable of integration.

EXAMPLE 5.10 Find the integral

$$
\int_ {0} ^ {\infty} x e ^ {- x ^ {2}} d x
$$

without using a table of integrals.

SOLUTION ▶ We have $x^{2}$ in the exponent, which suggests using $y = x^{2}$ as a new variable. If $y = x^{2}$ , then dy = 2x dx, or $x dx = \frac{1}{2}dy$ ,

$$
\begin{array}{r l} \int_ {0} ^ {\infty} x e ^ {- x ^ {2}} d x & = \frac {1}{2} \int_ {x = 0} ^ {x = \infty} e ^ {- y} d y = \frac {1}{2} \int_ {0} ^ {\infty} e ^ {- y} d y \\ & = - \frac {1}{2} e ^ {- y} \Big | _ {0} ^ {\infty} = - \frac {1}{2} (0 - 1) = \frac {1}{2}. \end{array}
$$

To review the solution of this example: First a new variable was chosen that looked as though it would give a simpler integrand function. Next, the integrand function was expressed in terms of this variable. The differential of the integration variable was also reexpressed. The limits of integration were then expressed in terms of the new variable, making the limits equal to the values of the new variable that correspond to the values of the old variable at the old limits. The final step was to compute the new integral, which is equal to the old integral.

EXAMPLE 5.11 Find the integral

$$
\int_ {0} ^ {1 / 2} \frac {d x}{2 - 2 x}
$$

without using a table of integrals.

SOLUTION ▶ We let y = 2 - 2x, in order to get a simple denominator. With this, dy = -2dx, or dx = -dy/2. When x = 0, y = 2, and when $x = \frac{1}{2}$ , y = 1,

$$
\begin{array}{r c l} \int_ {0} ^ {1 / 2} \frac {1}{2 - 2 x} d x & = & - \frac {1}{2} \int_ {2} ^ {1} \frac {1}{y} d y = \frac {1}{2} \int_ {1} ^ {2} \frac {1}{y} d y \\ & = & \left. \frac {1}{2} \ln (y) \right| _ {1} ^ {2} = \frac {1}{2} [ \ln (2) - \ln (1) ] \\ & = & \frac {1}{2} \ln (2). \end{array}
$$

EXERCISE 5.12 ▶

Find the integral

$$
\int_ {0} ^ {\pi} e ^ {\sin (\theta)} \cos (\theta) d \theta
$$

without using a table of integrals.


## Integration by Parts

This method, which is also called partial integration, consists of application of the formula

$$
\boxed {\int u \frac {d v}{d x} d x = u v - \int v \frac {d u}{d x} + C}\tag{5.41}
$$

or the corresponding formula for definite integrals

$$
\boxed {\int_ {a} ^ {b} u \frac {d v}{d x} d x = u (x) v (x) | _ {a} ^ {b} - \int_ {a} ^ {b} v \frac {d u}{d x}.}\tag{5.42}
$$

In these formulas, u and v must be functions of x that are differentiable everywhere in the interval of integration.

We can derive Eq. (5.41) by use of Eq. (4.21), which gives the derivative of the product of two functions:

$$
{\frac {d}{d x}} (u v) = u {\frac {d v}{d x}} + v {\frac {d u}{d x}}.
$$

The antiderivative of either side of this equation is just $uv + C$ , where C is an arbitrary constant. We can write the indefinite integral

$$
\int \frac {d (u v)}{d x} d x = \int u \frac {d v}{d x} d x + \int v \frac {d u}{d x} d x = u (x) v (x) + C.
$$

This is the same as Eq. (5.41).

EXAMPLE 5.12 Find the indefinite integral

$$
\int x \sin (x) d x
$$

without using a table.

SOLUTION ▶ There are two choices. We could let $u(x) = x$ and $\sin(x) = dv/dx$ , or we could let $u(x) = \sin(x)$ and x = dv/dx. We make the first choice because the antiderivative of x is $x^{2}/2$ , which will lead to a more complicated integral than the one containing x. With this choice

$$
\frac {d u}{d x} = 1 \quad \text { and } \quad v = - \cos (x)
$$

$$
\begin{array}{r c l} \int x \sin (x) d x & = & - x \cos (x) + \int \cos (x) d x \\ & = & - x \cos (x) + \sin (x) + C. \end{array}
$$

EXERCISE 5.13 ▶

Find the integral

$$
\int_ {0} ^ {\pi} x ^ {2} \sin (x) d x
$$

without using a table. You will have to apply partial integration twice.

The fundamental equation of partial integration, Eq. (5.41), is sometimes written with differentials instead of derivatives:

$$
\boxed {\int u d v = u v - \int v d u + C}\tag{5.43}
$$

## The Method of Partial Fractions

This method uses an algebraic procedure for turning a difficult integrand into a sum of two or more easier functions. It works with an integral of the type

$$
I = \int \frac {P (x)}{Q (x)} d x,\tag{5.44}
$$

where $P(x)$ and $Q(x)$ are polynomials in x. The highest power of x in P must be lower than the highest power of x in Q. However, if this is not the case, you can proceed by performing a long division, obtaining a polynomial plus a remainder, which will be a quotient of polynomials that does obey the condition. The polynomial can be integrated easily, and the remainder quotient can be handled with the method of partial fractions.

The first step in the procedure is to factor the denominator, $Q(x)$ , into a product of polynomials of degree 1 and 2. A polynomial of degree 1 is an expression of the form $ax + b$ , and a polynomial of degree 2 is $ax^{2} + bx + c$ . We first assume that all of the factors are of degree 1, so that

$$
Q (x) = \left(a _ {1} x + b _ {1}\right) \left(a _ {2} x + b _ {2}\right) \left(a _ {3} x + b _ {3}\right) \dots \left(a _ {n} x + b _ {n}\right),\tag{5.45}
$$

where all the $a$ 's and $b$ 's are constants.

The fundamental formula of the method of partial fractions is a theorem of algebra that says that if $Q(x)$ is given by Eq. (5.45) and $P(x)$ is of lower degree than $Q(x)$ , then

$$
\boxed {\frac {P (x)}{Q (x)} = \frac {A _ {1}}{a _ {1} x + b _ {1}} + \frac {A _ {2}}{a _ {2} x + b _ {2}} + \dots + \frac {A _ {n}}{a _ {n} x + b _ {n}},}\tag{5.46}
$$

where $A_{1}, A_{2}, \ldots, A_{n}$ , are all constants.

Equation (5.46) is applicable only if all the factors in $Q(x)$ are distinct from each other. If the same factor occurs more than once, Eq. (5.46) must be modified. If the factor $a_{1}x + b_{1}$ occurs m times in the denominator, we write

$$
\frac {P (x)}{(a _ {1} x + b _ {1}) ^ {m}} = \frac {A _ {1}}{a _ {1} x + b _ {1}} + \frac {A _ {2}}{(a _ {1} x + b _ {1}) ^ {2}} + \dots + \frac {A _ {m}}{(a _ {1} x + b _ {1}) ^ {m}}\tag{5.47}
$$

If other factors occur in the denominator, we must add other terms as in Eq. (5.46). Sometimes a factor of degree 2 occurs that cannot easily be factored. If $Q = a_{1}x^{2} + b_{1}x + c_{1}$ , we must write

$$
\frac {P (x)}{Q (x)} = \frac {A _ {1} x + B _ {1}}{a _ {1} x ^ {2} + b _ {1} x + c _ {1}} + \text { other   terms   as   in   Eqs. } \tag {5.46}\tag{5.48}
$$

If Q contains other factors we must add other terms as in Eqs. (5.46) and (5.47).

EXAMPLE 5.13 Apply Eq. (5.46) to

$$
\int \frac {6 x - 30}{x ^ {2} + 3 x + 2} d x.
$$

SOLUTION ▶ The denominator can be factored, so we write

$$
\frac {6 x - 30}{x ^ {2} + 3 x + 2} = \frac {A _ {1}}{x + 2} + \frac {A _ {2}}{x + 1}.
$$

We need to solve for $A_{1}$ and $A_{2}$ so that this equation will be satisfied for all values of $x$ . We multiply both sides of the equation by $(x + 2)(x - 1)$ :

$$
6 x - 30 = A _ {1} (x + 1) + A _ {2} (x + 2).
$$

Since this equation must be valid for all values of $x$ , we can get a different equation for each value of $x$ . If we let $x = 0$ , we get

$$
- 30 = A _ {1} + 2 A _ {2}.\tag{5.49}
$$

If we let $x$ become very large, so that the constant terms can be neglected, we obtain

$$
6 x = A _ {1} x + A _ {2} x
$$

or

$$
6 = A _ {1} + A _ {2}.\tag{5.50}
$$

Equations (5.49) and (5.50) can be solved simultaneously to obtain

$$
A _ {1} = 42, \quad A _ {2} = - 36.\tag{5.51}
$$

Our result is

$$
\int \frac {6 x - 30}{x ^ {2} + 3 x + 2} = \int \frac {42}{x + 2} d x - \int \frac {36}{x + 1} d x.\tag{5.52}
$$

Solve Eq. (5.49) and (5.50) simultaneously to obtain

EXERCISE 5.15 ▶ Find the indefinite integrals on the right-hand side of Eq. (5.52).

The Apart statement in Mathematica carries out the decomposition into partial fractions automatically. See Chapter 3.

EXERCISE 5.16 ▶ Use Mathematica to verify the partial fractions in the above example.

The following example shows a case in the study of chemical reaction rates that requires the use of partial fractions.

EXAMPLE 5.14 Consider a chemical reaction

$$
a \mathrm{A} + b \mathrm{B} \longrightarrow c \mathrm{C},
$$

where the capital letters are abbreviations for some chemical formulas and the lowercase letters are abbreviations for the stoichiometric coefficients that balance the equation. Assume that the rate of the reaction is given by the rate law

$$
- \frac {1}{a} \frac {d [ \mathrm{A} ]}{d t} = k _ {f} [ \mathrm{A} ] [ \mathrm{B} ],
$$

where $k_{f}$ is a function of temperature called the rate constant and where [A] represents the molar concentration of A and [B] represents the molar concentration of B. This rate law is said to be second order overall, first order in A, and first order in B. Carry out the integration of this rate law using the method of partial fractions.

SOLUTION ▶ In order to proceed, we express [A] and [B] in terms of a single variable:

$$
[ \mathrm{A} ] = [ \mathrm{A} ] _ {0} - a x
$$

and

$$
[ \mathbf {B} ] = [ \mathbf {B} ] _ {0} - b x,
$$

where the initial values of the concentrations are labeled with a subscript 0. We have

$$
- \frac {1}{a} \frac {d [ \mathrm{A} ]}{d t} = \frac {d x}{d t}.
$$

In the case that the reactants are not mixed in the stoichiometric ratio, we manipulate the rate expression into the form, where we have multiplied by dt and recognized that $(dx/dt)dt = dx$ ,

$$
\frac {1}{([ \mathrm{A} ] _ {0} - a x) ([ \mathrm{B} ] _ {0} - b x)} d x = k _ {f} d t.
$$

We write

$$
\frac {1}{([ \mathrm{A} ] _ {0} - a x) ([ \mathrm{B} ] _ {0} - b x)} = \frac {G}{[ \mathrm{A} ] _ {0} - a x} + \frac {H}{[ \mathrm{B} ] _ {0} - b x}.
$$

The constants $G$ and $H$ are found to be

$$
G = \frac {1}{[ \mathrm{B} ] _ {0} - b [ \mathrm{A} ] _ {0} / a} \quad \text { and } \quad H = \frac {1}{[ \mathrm{A} ] _ {0} - a [ \mathrm{B} ] _ {0} / b}.
$$

When these expressions are substituted into the rate expression, a definite integration gives

$$
\frac {1}{a [ \mathrm{B} ] _ {0} - b [ \mathrm{A} ] _ {0}} \ln \left(\frac {[ \mathrm{B} ] _ {t} [ \mathrm{A} ] _ {0}}{[ \mathrm{A} ] _ {t} [ \mathrm{B} ] _ {0}}\right) = k _ {f} t.
$$

EXERCISE 5.17 ▶ Show that the expressions for G and H are correct. Verify your result using Mathematica if it is available.

The methods presented thus far in this chapter provide an adequate set of tools for the calculation of most integrals that will be found in a physical chemistry course. In applying these methods, it is probably best to proceed as follows:

1. If the limits are 0 and $\infty$ or 0 and $\pi$ , or something else quite simple, look first in a table of definite integrals.

2. If this does not work, or if the limits were not suitable, look in a table of indefinite integrals.

3. If you do not find the integral in a table, try the method of substitution.

4. If you still have not obtained the integral, see if the method of partial fractions is applicable and use it if you can.

5. If this did not work, manipulate the integrand into a product of two factors and try the method of partial integration.

6. If all these things have failed, or if they could not be attempted, do a numerical approximation to the integral. This is discussed in the next section.

## Integration with Mathematica

Mathematica can carry out indefinite integrals symbolically. For example, the input and output statements for the indefinite integral of $\sin(x)$ are

In[1]: =Clear[x]

Integrate[Sin[x],x]

Out[1] = -Cos[x]

Mathematica appears to contain just about every indefinite integral that exists in tables. However, if you specify an integrand for which no indefinite integral exists or one that is not in Mathematica's tables, Mathematica will print out what you gave it.

Mathematica can also carry out definite integrals. Definite integrals are obtained by adding the limits to the input entry. To obtain the definite integral of $\sin(x)$ from x = 0 to $x = \pi$ , the input and output statements are

In[1]: =Clear[x]

Integrate[Sin[x],{x,0,Pi}]

Out[1] = 2

## 5.6 Numerical Integration

There are two cases for which a numerical approximation to a definite integral must be used. In one case the integrand function does not possess an antiderivative function that you can find in a table or can work out. For example, one integrand function for which no antiderivative functions exists is $e^{-x^{2}}$ (see Appendix G). In the other case the integrand function is represented approximately by a set of data points instead of by a formula. In ether case, there are several approximation methods that we can use to obtain a definite integral.

## The Bar-Graph Approximation

We begin with Eq. (5.21):

$$
\int_{a}^{b}f(x)  dx = \lim_{\substack{\Delta x\to 0, n\to \infty ,\\ (n\Delta x = x^{\prime} - x_{0})}}\sum_{k = 0}^{n - 1}f(a + j\Delta x)   \Delta x.\tag{5.53}
$$

If we do not take the limit but allow n to be some convenient finite number, the resulting equation will be approximately correct. Let us consider an example the integral of $e^{-x^{2}}$ from x = 1 to x = 2. We apply an approximate version of Eq. (5.53) with n = 10. The result is

$$
\int_ {1} ^ {2} e ^ {- x ^ {2}} d x \approx \sum_ {j = 0} ^ {9} \exp \left[ - (1 + 0.1 j) ^ {2} \right] (0.1) = 0.15329.\tag{5.54}
$$

This result is represented by the area under a bar graph with bars of unit width such as in Fig. 5.2. We call this approximation the bar-graph approximation. The integral is equal to the area under the graph of the integrand function, so the bar-graph approximation is in error by the area of the roughly triangular areas between the bar graph and the curve representing the integrand function. The error in Eq. (5.54) is about 15%, since the correct value of this integral is 0.13525726 to eight significant digits.

Each bar in Fig. 5.2 is called a panel. The bar-graph approximation can be made more nearly accurate by increasing the number of panels and decreasing their width, but the rate of improvement can be quite slow. For example, if we take n = 20 and $\Delta x = 0.05$ , we get 0.14413 for the bar-graph approximation to the integral in Eq. (5.54), which is still in error by about 6%. If we take n = 100 and $\Delta x = 0.01$ , we get 0.13701, which is still wrong by about 1%.

## The Trapezoidal Approximation

One way to improve on the bar-graph approximation is to take the height of the rectangles as equal to the value of the integrand function near the middle of the panel. In the trapezoidal approximation the height of the bar is taken as the average of the values of the function at the two sides of the panel. This gives an area for the panel that is the same as that of a trapezoid whose upper corners match the integrand function at the sides of the panel, as shown in Fig. 5.6.

$$
\int_ {a} ^ {b} f (x) d x \approx \frac {f (a) \Delta x}{2} + \sum_ {k = 1} ^ {n - 1} f (a + k \Delta x) \Delta x + \frac {f (b) \Delta x}{2}.\tag{5.55}
$$

As expected, the trapezoidal approximation gives more nearly correct values than does the bar-graph approximation, for the same number of panels. For 10 panels, the trapezoidal approximation gives a result of 0.135810 for the integral in Eq. (5.54). For 100 panels, the trapezoidal approximation is correct to five significant digits.

![[587674b7e82be971a5d534fcb8872e579fa86404d263bab6d2ef6f43c979ccbe.jpg]]  
Figure 5.6 ▶ Figure to illustrate the trapezoidal approximation (enlarged view of one panel shown).

EXERCISE 5.18 ▶ Using the trapezoidal approximation with five panels, calculate the value of the integral

$$
\int_ {10} ^ {20} 2 x ^ {2} d x.
$$

Calculate the exact value of the integral for comparison.


## Simpson's Rule

In the bar-graph approximation, we used only one value of the integrand for each panel. In the trapezoidal approximation, we used two values for each panel, corresponding to a line segment fitting the integrand curve at the edges of the panel. If three points in a plane are given, there is one and only one parabola that can be drawn through all three. In Simpson's rule, we take the panels two at a time, construct a parabola through the three points, find the area under the parabola, and sum these areas to approximate the integral. A parabolic curve is likely to fall closer to the integrand curve than a straight line, so we expect this to give a better approximation than the trapezoidal approximation, and it usually does. We must have an even number of panels to use this method.

We let $f_{0} = f(a)$ , $f_{1} = f(a + \Delta x)$ , $f_{2} = f(a + 2\Delta x)$ , and so on, and use the formula for the area under a parabola to obtain as our final result

$$
\int_ {a} ^ {b} f (x) d x \approx \frac {\left(f _ {0} + 4 f _ {1} + 2 f _ {2} + 4 f _ {3} + \cdots + 4 f _ {n - 1} + f _ {n}\right) \Delta x}{3}.\tag{5.56}
$$

Notice the pattern, with alternating coefficients of 2 and 4, except for the first and last values of the integrand.

This version of Simpson's rule is sometimes called Simpson's one-third rule because of the 3 in the denominator. There is another version, called Simpson's five-eighths rule, which corresponds to fitting third-degree polynomials to four points at a time.

EXERCISE 5.19 Apply Simpson's rule to the integral of Exercise 5.18, using two panels. Since the integrand curve is a parabola, your result should be exactly correct.

There is another widely used way to obtain a numerical approximation to a definite integral, known as Gauss quadrature. In this method, the integrand function must be evaluated at particular unequally spaced points on the interval of integration. We will not discuss this method, but you can read about it in books on numerical analysis.

So far, we have assumed that the integrand function was known so that it could be evaluated at the required points. Most of the applications of numerical integration in physical chemistry are to integrals where the integrand function is not known exactly, but is known only approximately from experimental measurements at a few points on the interval of integration. If there are an odd number of data points that are equally spaced, we can apply Simpson's rule.

EXERCISE 5.20 In thermodynamics, it is shown that the entropy change of a system that is heated at constant pressure from temperature $T_{1}$ to temperature $T_{2}$ is given by

$$
\Delta S = S \left(T _ {2}\right) - S \left(T _ {1}\right) = \int_ {T _ {1}} ^ {T _ {2}} \frac {C _ {p}}{T} d T,\tag{5.57}
$$

where $C_{p}$ is the constant-pressure heat capacity and T is the temperature on the Kelvin scale. Calculate $\Delta S$ for the heating of 1.00 mol of solid zinc from 20.0 K to 100.0 K, using the following data:

<table><tr><td>T/K</td><td> $C_{\text{p}}/\text{J K}^{-1}\text{mol}^{-1}$ </td><td>T/K</td><td> $C_{\text{p}}/\text{J K}^{-1}\text{mol}^{-1}$ </td></tr><tr><td>20</td><td>1.70</td><td>70</td><td>15.43</td></tr><tr><td>30</td><td>4.966</td><td>80</td><td>16.87</td></tr><tr><td>40</td><td>8.171</td><td>90</td><td>18.11</td></tr><tr><td>50</td><td>11.18</td><td>100</td><td>19.15</td></tr><tr><td>60</td><td>13.60</td><td></td><td></td></tr></table>

## Numerical Integration with Mathematica

If you give Mathematica a definite integral with an integrand that has no indefinite integral in Mathematica's tables, Mathematica will simply return your input statement. To carry out a numerical approximation to the integral and obtain a numerical value, use the NIntegrate statement, which has the form:

NIntegrate[integrand function, {x, lower limit, upper limit}].

EXAMPLE 5.15 Use Mathematica to obtain the integral

$$
{\frac {2}{\sqrt {\pi}}} \int_ {0} ^ {1} e ^ {- x ^ {2}} d x\tag{5.58}
$$

SOLUTION ▶ We type the input statements:

Clear[x]

NIntegrate[(2/Sqrt[Pi])Exp[-x^2],{x,0,1}]

and press the "Enter" key. We obtain the output

Out[1]=0.842701

which is the value of $\operatorname{erf}(1)$ .

EXERCISE 5.21 ▶ Write Mathematica entries to obtain the following integrals:

(a)

$$
\int \cos^ {3} (x) d x\tag{b}
$$

$$
\int_ {1} ^ {2} e ^ {5 x ^ {2}} d x
$$

(c) $\int_0^\pi \sin [\cos (x)]dx$


## 5.7 Probability Distributions and Mean Values

In this section, we discuss how to obtain certain average values using integration. There are several kinds of averages in common use. One type is the median, which is the value such that half of the set of values is greater than the median and half of the set is smaller than the median. The mode is the value that occurs most frequently in the set. We now discuss the calculation of a mean value by integration. The mean of a set of N values is defined as

$$
\boxed {\bar {x} = \frac {1}{N} \left(x _ {1} + x _ {2} + x _ {3} + x _ {4} + \dots + x _ {N}\right),}\tag{5.59}
$$

where $x_{1}$ , $x_{2}$ , $x_{3}$ , and so on, are the values to be averaged. The notation $\langle x\rangle$ is also used for the mean value.

EXERCISE 5.22 ▶ Calculate the mean of the integers beginning with 10 and ending with 20.

There is another way to write the mean of a set of values if several of the members of the list are equal to each other. Let us arrange the members of our list so that the first M members of the list are all different from each other, and each of the other N - M members is equal to some member of the first subset. Let $N_{i}$ be the total number of members of the entire list that are equal to $x_{i}$ , where $x_{i}$ is one of the distinct values in the first subset. Equation (5.59) can be rewritten

$$
\bar {x} = \frac {1}{N} (N _ {1} x _ {1} + N _ {2} x _ {2} + N _ {3} x _ {3} + N _ {4} x _ {4} + \dots + N _ {M} x _ {M})\tag{5.60}
$$

$$
\bar {x} = \frac {1}{N} \sum_ {i = 1} ^ {M} N _ {i} x _ {i} = \sum_ {i = 1} ^ {M} p _ {i} x _ {i}.\tag{5.61}
$$

We again use the standard notation of a capital Greek sigma ( $\Sigma$ ) for a sum, introduced in Eq. (5.17). The quantity $p_{i}$ is equal to $N_{i}/N$ and is the fraction of the members of the entire list that are equal to $x_{i}$ . If we were to sample the entire list by choosing a member at random, the probability that this member would equal $x_{i}$ is given by $p_{i}$ . The set of probabilities that we have defined adds up to unity:

$$
\sum_ {i = 1} ^ {M} p _ {i} = \sum_ {i = 1} ^ {M} \frac {N _ {i}}{N} = \frac {1}{N} \sum_ {i = 1} ^ {M} N _ {i} = 1.\tag{5.62}
$$

A set of probabilities that adds up to unity is said to be normalized.

EXAMPLE 5.16 A quiz was given in a class with 100 members. The scores were as follows:

<table><tr><td>Score</td><td># of students</td><td>Score</td><td># of students</td></tr><tr><td>100</td><td>8</td><td>70</td><td>23</td></tr><tr><td>90</td><td>11</td><td>60</td><td>14</td></tr><tr><td>80</td><td>35</td><td>50</td><td>9</td></tr></table>

Find the mean score.

SOLUTION ▶

$$
\bar {s} = (0.08) (100) + (0.11) (90) + (0.35) (80) + (0.23) (70) + (0.14) (60) + (0.09) (50) = 74.9.
$$

If you have a set of values with considerable duplication, Eq. (5.61) is quicker and easier to use than Eq. (5.59).

It is also possible to take the mean of a function of the values in our set. For example, to form the mean of the squares of the values, we have

$$
\begin{array}{r l} \overline {{x ^ {2}}} & = \frac {1}{N} \left(x _ {1} ^ {2} + x _ {2} ^ {2} + x _ {3} ^ {2} + x _ {4} ^ {2} + \dots + x _ {N} ^ {2}\right) \\ & = \frac {1}{N} \sum_ {i = 1} ^ {M} N _ {i} x _ {i} ^ {2} = \sum_ {i = 1} ^ {M} p _ {i} x _ {i} ^ {2}. \end{array}\tag{5.63}
$$

(5.64)

Similarly, if $g = g(x)$ is any function defined for all values of x that occur in our list, the mean value of this function is given by

$$
\boxed {\overline {{g (x)}} = \sum_ {i = 1} ^ {M} p _ {i} g (x _ {i})}.\tag{5.65}
$$

EXERCISE 5.23 ▶ Find the mean of the squares of the scores given in Example 5.16. Find also the square root of this mean, which is called the root-mean-square score. The root-mean-square (rms) value is another type of average.

## Probability Distributions

One of the important quantities in gas kinetic theory is the mean speed of molecules in a gas. The calculation of such a mean is a little more complicated than the case of Eq. (5.61). The reasons for this are: (1) the speed of a molecule can take on any real nonnegative value, and (2) there are many molecules in almost any sample of a gas. Let's develop formulas to handle cases like this. Consider a variable $x$ , which can take on any real values between $x = a$ and $x = b$ . We divide the interval $(a, b)$ into $n$ subintervals. Look at the subinterval $(x_i, x_{i+1})$ , which is the same as saying $x_i < x < x_{i+1}$ . The interval can also be written $(x_i, x_i + \Delta x_i)$ , where

$$
\Delta x = x _ {i + 1} - x _ {i}.\tag{5.66}
$$

Let the fraction of all members of our sample that have values of x lying between $x_{i}$ and $x_{i+1}$ be called $p_{i}$ . If $\Delta x$ is quite small, $p_{i}$ will be very nearly proportional to $\Delta x$ . We write

$$
p _ {i} = f _ {i} \Delta x.\tag{5.67}
$$

The quantity $f_{i}$ will not depend strongly on $\Delta x$ . The mean value of x is given by Eq. (5.61):

$$
\bar {x} \approx \sum_ {i = 0} ^ {n - 1} p _ {i} x _ {i} = \sum_ {i = 0} ^ {n - 1} x _ {i} f _ {i} \Delta x.\tag{5.68}
$$

This equation is only approximately true, because we have multiplied the probability that x is in the subinterval $(x_{i}, x_{i} + \Delta x)$ by $x_{i}$ , which is only one of the values of x in the subinterval. However, Eq. (5.68) can be made more and more nearly exact by making n larger and larger and $\Delta x$ smaller and smaller in such a way that $n\Delta x$ is constant. In this limit, $f_{i}$ becomes independent of $\Delta x$ . We replace the symbol $f_{i}$ by $f(x_{i})$ and assume that $f(x_{i})$ is an integrable function of $x_{i}$ . It must be at least piecewise continuous. Our formula for the mean value of x now becomes an integral as defined in Eq. (5.21):

$$
\bar {x} = \lim _ {\stackrel {\Delta x \to 0, n \to \infty ,} {n \Delta x = b - a}} \sum_ {i = 0} ^ {n - 1} x _ {i} f (x _ {i}) \Delta x = \int_ {a} ^ {b} x f (x) d x.\tag{5.69}
$$

The function $f(x)$ is called the probability density, or probability distribution, or sometimes the distribution function.

If we desire the mean value of a function of $x$ — say, $g(x)$ — the formula is analogous to Eq. (5.65),

$$
\boxed {\overline {{g (x)}} = \int_ {a} ^ {b} g (x) f (x) d x.}\tag{5.70}
$$

For example, the mean of $x^{2}$ is given by

$$
\overline {{{{x ^ {2}}}}} = \int_ {a} ^ {b} x ^ {2} f (x) d x.\tag{5.71}
$$

As defined above, the probability density is normalized, which now means that

$$
\int_ {a} ^ {b} f (x) d x = 1.\tag{5.72}
$$

It is possible to use a probability density that is not normalized, but if you do this, you must modify Eq. (5.70). For an unnormalized probability distribution

$$
\boxed { \begin{array}{l l} \overline {{g (x)}} = \frac {\int_ {a} ^ {b} g (x) f (x) d x}{\int_ {a} ^ {b} f (x) d x} & \text {(unnormalized} \\ & \text {probability distribution)} \end{array} }\tag{5.73}
$$

For a normalized probability distribution, the probability that x lies in the infinitesimal interval $(x, x + dx)$ is $f(x) \, dx$ , which is the probability per unit length times the length of the infinitesimal interval. The fact that $f(x)$ is a probability per unit length is the reason for using the name “probability density” for it. Since all continuously variable values of x in some range are possible, a continuous probability distribution must apply to a set of infinitely many members. Such a set is called the population to which the distribution applies. The probability $f(x') \, dx$ is the fraction of the population that has its value of x lying in the region between x and $x' + dx$ .

The most commonly used measure of the “spread” of a probability distribution is the standard deviation, $\sigma_{x}$ , defined by

$$
\boxed {\sigma_ {x} = \left[ \overline {{x ^ {2}}} - (\bar {x}) ^ {2} \right] ^ {1 / 2}.}\tag{5.74}
$$

We label the standard deviation with a subscript to indicate what variable is being considered. Generally, about two-thirds of a population will have their values of x within one standard deviation of the mean—that is, within the interval $(\bar{x} - \sigma_{x}, \bar{x} + \sigma_{x})$ .

EXAMPLE 5.17 If all values of x between a and b are equally probable, find the mean value of x, the root-mean-square value of x, and the standard deviation of x.

SOLUTION ▶ In order to be normalized, the probability density is

$$
f (x) = \frac {1}{b - a}
$$

so that

$$
\bar {x} = \int_ {a} ^ {b} x \frac {1}{b - a} d x = \frac {1}{2 (b - a)} \left(b ^ {2} - a ^ {2}\right) = \frac {1}{2} (b + a)
$$

$$
\overline {{x ^ {2}}} = \int_ {a} ^ {b} x ^ {2} \frac {1}{b - a} d x = \frac {1}{3 (b - a)} \left(b ^ {3} - a ^ {3}\right) = \frac {1}{3} \left(b ^ {2} + a b + a ^ {2}\right).
$$

The root-mean-square value of $x$ is

$$
\left(\overline {{{{x ^ {2}}}}}\right) ^ {1 / 2} = \left[ \frac {1}{3} (b ^ {2} + a b + a ^ {2}) \right] ^ {1 / 2}.
$$

The standard deviation is found as

$$
\begin{array}{r l} \sigma_ {x} ^ {2} & = \overline {{x ^ {2}}} - \bar {x} ^ {2} = \frac {1}{3} (b ^ {2} + a b + a ^ {2}) - \frac {1}{4} (b ^ {2} + 2 a b + a ^ {2}) \\ & = \frac {1}{12} (a - b) ^ {2} \\ \sigma_ {x} & = \sqrt {\frac {1}{12}} (a - b). \end{array}
$$

EXERCISE 5.24 ▶ From the results of the preceding example, find the numerical values of $\bar{x}$ , $\left(\overline{x^{2}}\right)^{1/2}$ , and $\sigma_{x}$ for a = 0 and b = 10. Comment on your values. What fraction of the total probability is found between $\bar{x} - \sigma_{x}$ and $\bar{x} + \sigma_{x}$ ?

EXERCISE 5.25 ▶ If x ranges from 0 to 10 and if $f(x) = cx^{2}$ , find the value of c so that $f(x)$ is normalized. Find the mean value of x and the root-mean-square value of x.

## The Gaussian Distribution

The most important probability distribution is the Gaussian distribution, which is represented by the formula

$$
\boxed {f (x) = \frac {1}{\sqrt {2 \pi} \sigma} \exp \left[ - \frac {(x - \mu) ^ {2}}{2 \sigma^ {2}} \right],}\tag{5.75}
$$

where $\mu$ is the mean value of x and where $\sigma$ is the standard deviation. This distribution is also called the normal distribution. If $\sigma = 1$ , then the distribution is called the standard normal distribution. The Gaussian distribution is assumed to describe populations of various kinds, including the IQ scores of people and velocities of molecules in a gas. $^{1}$

EXAMPLE 5.18 Show that the distribution in Eq. (5.75) satisfies the normalization condition of Eq. (5.72) with the limits of integration equal to $-\infty$ and $+\infty$ .

SOLUTION ▶ We have the following integral, which we modify by the method of substitution, and then look up in Appendix G:

$$
\int_ {- \infty} ^ {\infty} \frac {1}{\sqrt {2 \pi} \sigma} e ^ {- (x - \mu) ^ {2} / 2 \sigma^ {2}} d x = \frac {1}{\sqrt {\pi}} \int_ {- \infty} ^ {\infty} e ^ {- t ^ {2}} d t = 1.
$$

EXERCISE 5.26 ▶ Calculate the mean and standard deviation of the Gaussian distribution, showing that $\mu$ is the mean and that $\sigma$ is the standard deviation.

![[1acc97ae85b5c7d4503ea23e56a7db9564366dd21949cdbc49ef9fb77d1ad484.jpg]]  
Figure 5.7 ▶ The Gaussian probability distribution.

Figure 5.7 shows a graph of the Gaussian distribution. Five values of x have been marked on the x axis: $x = \mu - 1.96\sigma$ , $x = \mu - \sigma$ , $x = \mu$ , $x = \mu + \sigma$ , and $x = \mu + 1.96\sigma$ .

EXAMPLE 5.19 Assuming the Gaussian distribution, calculate the fraction of the population with x lying between $x = \mu - \sigma$ and $x = \mu + \sigma$ .

SOLUTION ▶ By integration of Eq. (5.75), we obtain

$$
\begin{array}{r l} (\text {fraction between} \mu - \sigma \text {and} \mu + \sigma) & = \int_ {\mu - \sigma} ^ {\mu + \sigma} \frac {1}{\sqrt {2 \pi} \sigma} e ^ {- (x - \mu) ^ {2} / 2 \sigma^ {2}} d x \\ & = \int_ {- \sigma} ^ {+ \sigma} \frac {1}{\sqrt {2 \pi} \sigma} e ^ {- y ^ {2} / 2 \sigma^ {2}} d y \\ & = \frac {2}{\sqrt {\pi}} \int_ {0} ^ {1 / \sqrt {2}} e ^ {- t ^ {2}} d t. \end{array}
$$

The last integral in this example is the error function with argument $1/\sqrt{2}$ . The integrand function $e^{-t^{2}}$ does not possess an indefinite integral that can be written with a single formula, so the error function must be approximated numerically unless the upper limit is infinite, in which case the error function is equal to 1. The error function is described in Appendix G. From the table of values in that appendix,

$$
\begin{array}{r l} \text {(fraction between} \mu - \sigma \text {and} \mu + \sigma) & = \operatorname{erf} \left(\frac {1}{\sqrt {2}}\right) \\ & = \operatorname{erf} (0.707 \dots) = 0.683 \dots \end{array}
$$

in agreement with our assertion that roughly two-thirds of the members of a population lie within one standard deviation of the mean.

EXERCISE 5.27 ▶ Show that the fraction of a population lying between $\mu - 1.96\sigma$ and $\mu + 1.96\sigma$ is equal to 0.95 if the population is described by the Gaussian distribution.

![[66fa609e5957f35628e40e2b23567f8f5202de3146035345b97522e61448ef22.jpg]]

You should remember the following facts: With a Gaussian distribution, 68% of the population lies within one standard deviation of the mean, 95% of the population lies within 1.96 standard deviations of the mean, and 99% of the population lies within 2.67 standard deviations of the mean. For other intervals, we can write

$$
\text {(fraction between} \mu - x _ {i} \text { and } \mu + x _ {i}) = \operatorname{erf} \left(\frac {x _ {i}}{\sqrt {2} \sigma}\right).\tag{5.76}
$$

There are a number of other common probability distributions in addition to the Gaussian distribution, including the binomial distribution, the Poisson distribution, and the Lorentzian distribution. $^{2}$ However, the Gaussian distribution is generally used in discussing experimental errors, and we return to this topic in Chapter 11.

## Probability Distributions in Gas Kinetic Theory

In gas kinetic theory, the probability density for a component of the molecular velocity is a Gaussian distribution. The normalized probability distribution for $v_{x}$ , the x component of the velocity, is given by

$$
f \left(v _ {x}\right) = \left(\frac {m}{2 \pi k _ {B} T}\right) ^ {3 / 2} \exp \left(- \frac {m v _ {x} ^ {2}}{2 k _ {B} T}\right),\tag{5.77}
$$

where $m$ is the molecular mass, $T$ the temperature on the Kelvin scale, and $k_{B}$ is Boltzmann's constant.

EXERCISE 5.28

(a) Show that the mean value of $v_{x}$ is equal to zero. Explain this fact in physical terms.

(b) Find the expression for $\left(\overline{v_x^2}\right)^{1 / 2}$ , the root-mean-square value of $v_{x}$ .

(c) Find the expression for the standard deviation of $v_{x}$ .

The speed v is the magnitude of the velocity. Since velocities with the same magnitude but different directions are included in the same speed, the distribution of speeds is different from the velocity distribution of Eq. (5.77). We denote the speed distribution by $f_{v}(v)$ . It is given by $^{3}$

$$
f _ {v} (v) = 4 \pi \left(\frac {m}{2 \pi k _ {B} T}\right) ^ {3 / 2} v ^ {2} \exp \left(- \frac {m v ^ {2}}{2 k _ {B} T}\right).\tag{5.78}
$$

A graph of this function is shown in Fig. 5.8. The speed is never negative, so that the graph does not extend to the left of the origin. In ordinary gas kinetic theory, the requirements of special relativity are ignored, and speeds approaching infinity are included. The error due to this inclusion is insignificant at ordinary temperatures, because of the low probability ascribed to high speeds.

![[7feceb39b2ab274c523bb5d6275085b65c828436fd005110d098cd55ce1ff4fd.jpg]]  
Figure 5.8 ▶ A graph of the probability density for speeds of molecules in a gas.

The mean speed is given by

$$
\bar {v} = \int_ {0} ^ {\infty} v f _ {v} (v) d v.\tag{5.79}
$$

EXAMPLE 5.20 Obtain a formula for the mean speed of molecules in a gas.

## SOLUTION ▶

$$
\bar {v} = 4 \pi \left(\frac {m}{2 \pi k _ {B} T}\right) ^ {3 / 2} \int_ {0} ^ {\infty} v ^ {3} \exp \left(- \frac {m v ^ {2}}{2 k _ {B} T}\right) d v.\tag{5.80}
$$

This integral can be obtained from Eq. (A.6) of Appendix G:

$$
\bar {v} = 4 \pi \left(\frac {m}{2 \pi k _ {B} T}\right) ^ {3 / 2} \frac {(2 k _ {B} T) ^ {2}}{2 m ^ {2}} = \left(\frac {8 k _ {B} T}{\pi m}\right) ^ {1 / 2}.\tag{5.81}
$$

EXERCISE 5.29 ▶

Find the value of $\bar{v}$ for $\mathbf{N}_2$ gas at $298\mathrm{K}$ .

EXAMPLE 5.21 Find a formula for the mean of the square of the speed of molecules in a gas and for the root-mean-square speed.

## SOLUTION ▶

$$
\begin{array}{r l} \overline {{v ^ {2}}} & = 4 \pi \left(\frac {m}{2 \pi k _ {B} T}\right) ^ {3 / 2} \int_ {0} ^ {\infty} v ^ {4} \exp \left(- \frac {m v ^ {2}}{2 k _ {B} T}\right) d v \\ & = \frac {3 k _ {B} T}{m} \\ v _ {r m s} & = \left(\overline {{v ^ {2}}}\right) ^ {1 / 2} = \left(\frac {3 k _ {B} T}{m}\right) ^ {1 / 2}. \end{array}
$$

EXERCISE 5.30 For molecules in a gas, find the formula for $\sigma_{v}$ and find its value for $\mathrm{N}_{2}$ gas at $298\mathrm{K}$ .

## Time Averages

If $g = g(t)$ , the time average of $g$ is defined as

$$
\overline {{{{g (t)}}}} = \int_ {t _ {1}} ^ {t _ {2}} g (t) f (t) d t,\tag{5.82}
$$

where we call $f(t)$ the weighting function. It plays the same role as a probability density, specifying the importance of different times. Most time averages are unweighted, which means that $f(t)$ is a constant equal to $1/(t_{2}-t_{1})$ :

$$
\overline {{{{g (t)}}}} = \frac {1}{t _ {2} - t _ {1}} \int_ {t _ {1}} ^ {t _ {2}} g (t) d t.\tag{5.83}
$$

Equation (5.83) is a version of the mean value theorem of integral calculus, which states that the mean value of a function is equal to the integral of the function divided by the length of the interval over which the mean is taken.

EXAMPLE 5.22 A particle falls in a vacuum near the surface of the earth. Find the average z component of the velocity during the first 10.00 s of fall if the initial speed is zero.

SOLUTION ▶ From Eq. (5.6),

$$
v _ {z} = - g t,
$$

where g is the acceleration due to gravity, $9.80 \, m s^{-2}$ ,

$$
\begin{array}{r l} \overline {{{v}}} _ {z} & = - \frac {1}{10} \int_ {0} ^ {10} g t d t = - \frac {g}{10} \left. \frac {t ^ {2}}{2} \right| _ {0} ^ {10} = - 5 g \\ & = - 5 (9.80 \mathrm{ms} ^ {- 2}) = - 49.0 \mathrm{ms} ^ {- 1}. \end{array}
$$

EXERCISE 5.31 ▶

EXERCISE 5.31 Find the time-average value of the z coordinate of the particle in the previous example for the first 10.00 s of fall if the initial position is z = 0.00 m.

## SUMMARY

Integration is one of the two fundamental processes of calculus. It is essentially the reverse of differentiation, the other important process. The first kind of an integral is the indefinite integral, which is the antiderivative of the integrand function. The second kind of an integral is the definite integral, which is constructed as the sum of very many small increments of the antiderivative function F, constructed from the integrand function f according to the formula from Chapter 4,

$$
d F = f (x) d x = \frac {d F}{d x} d x
$$

The definite integral has a lower limit of integration, at which the summation process starts, and an upper limit, at which the process ends. The definite integral is therefore equal to the value of the antiderivative function (indefinite integral) at the upper limit minus its value at the lower limit

$$
\int_ {a} ^ {b} f (x) d x = F (b) - F (a).
$$

Extensive tables of indefinite integrals exist, as well as tables of definite integrals. Some integrals have infinite limits or have integrands that attain infinite values, and such integrals are called improper integrals. Many such integrals diverge (have undefined values), but some improper integrals have finite values and are said to converge.

There are several techniques for manipulating integrals into a form that you can recognize or which you can look up in a table, and we presented a few of these. Some integrals cannot be worked out mathematically, but must be approximated numerically. We discussed some elementary techniques for carrying out this approximation, including Simpson's rule, the most commonly used technique, and finally presented a simple computer program for implementing Simpson's rule.

Mean values of variables that take on all real values in a certain interval are calculated as integrals of the form

$$
g = \int_ {a} ^ {b} g (x) f (x) d x,
$$

where $g(x)$ is the function to be averaged and $f(x)$ is the probability distribution, or probability density, or distribution function.

## PROBLEMS

1. Find the indefinite integrals without using a table:

a) $\int x\ln (x)dx$

b) $\int x\sin^2 (x)dx$

c) $\int \frac{1}{x(x - a)} dx$

d) $\int x^{3}\ln (x^{2})dx$

2. Find the definite integrals:

a) $\int_0^{2\pi}\sin (x)dx$

b) $\int_1^2 x\ln (x)dx$

c) $\int_0^{\pi /2}\sin^2 (x)\cos (x)dx$

3. Find the definite integrals:

a) $\int_0^{2\pi}\sin^2 (x)dx$

b) $\int_2^{10}x\ln (x)dx$

c) $\int_0^{\pi /2}\sin (x)\cos^2 (x)dx$

4. Find the definite integrals:

a) $\int_0^{\pi /2}x\sin (x^2)dx$ b) $\int_0^{\pi /2}x\sin (x^2)\cos (x^2)dx$ c) $\int_0^{2\pi}x\cos (x)dx$

5. Determine whether the following improper integrals converge. Evaluate the convergent integrals.
a) $\int_{1}^{\infty}\left(\frac{1}{x^{2}}\right)dx$ b) $\int_{1}^{\pi/2}\tan(x)dx$ c) $\int_{0}^{1}\frac{1}{x\ln(x)}dx$

6. Determine whether the following improper integrals converge. Evaluate the convergent integrals.
a) $\int_{1}^{\infty}\left(\frac{1}{x}\right)dx$ b) $\int_{0}^{\pi}\tan(x)dx$ c) $\int_{0}^{\pi/2}\tan(x)dx$

7. Determine whether the following improper integrals converge. Evaluate the convergent integrals.
a) $\int_{0}^{1}\left(\frac{1}{x}\right)dx$ b) $\int_{0}^{\infty}\sin(x)dx$ c) $\int_{-\pi/2}^{\pi/2}\tan(x)dx$

8. At 298 K, what fraction of nitrogen molecules has speeds lying between 0 and the mean speed? Do a numerical approximation to the integral or use the identity

$$
\int_ {0} ^ {\infty} t ^ {2} e ^ {- a t ^ {2}} d t = \frac {\sqrt {x}}{4 a ^ {3 / 2}} \operatorname{erf} (\sqrt {a} x) - \frac {x}{2 a} e ^ {- a x ^ {2}}.
$$

9. Approximate the integral

$$
\int_ {0} ^ {\infty} e ^ {- x ^ {2}} d x
$$

using Simpson's rule. You will have to take a finite upper limit, choosing a value large enough so that the error caused by using the wrong limit is negligible. The correct answer is $\sqrt{\pi}/2 = 0.886226926\cdots$ .

10. Using Simpson's rule, evaluate erf(2).

$$
\operatorname{erf} (2) = \frac {2}{\sqrt {\pi}} \int_ {0} ^ {2} e ^ {- t ^ {2}} d t
$$

Compare your answer with the correct value from the table in Appendix G.

11. Find the integrals.

a) $\int \sin [x(x + 1)](2x + 1)dx$

b) $\int_0^\pi \sin [\cos (x)]\sin (x)dx$

12. When a gas expands reversibly, the work that it does on its surroundings is given by the integral

$$
w _ {s u r r} = \int_ {V _ {1}} ^ {V _ {2}} P d V,
$$

where $V_{1}$ is the initial volume, $V_{2}$ the final volume, and P the pressure of the gas. Certain nonideal gases are described quite well by the van der Waals equation of state,

$$
\left(P + \frac {n ^ {2} a}{V ^ {2}}\right) (V - n b) = n R T
$$

where V is the volume, n is the amount of gas in moles, T is the temperature on the Kelvin scale, and a and b are constants. R is usually taken to be the ideal gas constant, $8.3145 \, J K^{-1} \, mol^{-1}$ .

a) Obtain a formula for the work done if 1.000 mol of such a gas expands reversibly at constant temperature from a volume $V_{1}$ to a volume $V_{2}$ .

b) If $T = 298 \, K$ , $V_{1} = 1.001 (1.000 \times 10^{-3} \, \text{m}^{3})$ , and $V_{2} = 100.01 = 0.100 \, m^{3}$ , find the value of the work done for 1.000 mol of $CO_{2}$ , which has $a = 0.3640 \, Pa \, m^{6} \, mol^{-2}$ , and $b = 4.267 \times 10^{-5} \, m^{3} \, mol^{-1}$ . The ideal gas constant, $R = 8.3145 \, J \, K^{-1} \, mol^{-1}$ .

c) Calculate the work done in the process of part b if the gas is assumed to be ideal.

13. The entropy change to bring a sample from 0 K (absolute zero) to a given state is called the absolute entropy of the sample in that state. Using Simpson's rule, calculate the absolute entropy of 1.000 mol of solid silver at 270 K. For the region 0 K to 30 K, use the approximate relation

$$
C _ {P} = a T ^ {3},
$$

where a is a constant that you can evaluate from the value of $C_{P}$ at 30 K. For the region 30 K to 270 K, use the following data: $^{4}$

<table><tr><td>T/K</td><td> $C_P/JK^{-1}mol^{-1}$ </td><td>T/K</td><td> $C_P/JK^{-1}mol^{-1}$ </td></tr><tr><td>30</td><td>4.77</td><td>170</td><td>23.61</td></tr><tr><td>50</td><td>11.65</td><td>190</td><td>24.09</td></tr><tr><td>70</td><td>16.33</td><td>210</td><td>24.42</td></tr><tr><td>90</td><td>19.13</td><td>230</td><td>24.73</td></tr><tr><td>110</td><td>20.96</td><td>250</td><td>25.03</td></tr><tr><td>130</td><td>22.13</td><td>270</td><td>25.31</td></tr><tr><td>150</td><td>22.97</td><td></td><td></td></tr></table>

$^{4}$ P.F. Meads, W.R. Forsythe, and W.F. Giaque, J. Am. Chem. Soc. 63, 1902 (1941).

14. Use Simpson's rule with at least 10 panels to evaluate the following definite integrals. Use Mathematica to check your results.

a) $\int_0^2 e^{3x^3}dx$

b) $\int_1^3 e^{x^2}dx$

# Mathematical Series and Transforms

## Preview

A mathematical series is a sum of terms. A series can have a finite number of terms or can have an infinite number of terms. If a series has an infinite number of terms, an important question is whether it approaches a finite limit as more and more terms of the series are included (in which case we say that it converges) or whether it becomes infinite in magnitude or oscillates endlessly (in which case we say that it diverges). A constant series has terms that are constants, so that it equals a constant if it converges. A functional series has terms that are functions of one or more independent variables, so that the series is a function of the same independent variables if it converges. Each term of a functional series contains a constant coefficient that multiplies a function from a set of basis functions. The process of constructing a functional series to represent a specific function is the process of determining the coefficients. We discuss two common types of functional series, power series and Fourier series.

An integral transform is similar to a functional series, except that it contains an integration instead of a summation, which corresponds to an integration variable instead of a summation index. The integrand contains two factors, as does a term of a functional series. The first factor is the transform, which plays the same role as the coefficients of a power series. The second factor is the basis function, which plays the same role as the set of basis functions in a functional series. We discuss two types of transforms, Fourier transforms and Laplace transforms.

## Principal Facts and Ideas

1. A mathematical series is a sum of terms, either with a finite number of terms or an infinite number of terms.

2. A constant series has terms that are constants, and a functional series has terms that are functions.
158

3. An infinite series converges if the sum approaches a finite limit ever more closely as ever more terms are summed, or diverges if the series does not approach such a limit.

4. An infinite functional series represents a function if it converges.

5. A Taylor series is a sum of terms that consist of coefficients times powers of x - h, where x is a variable and h is a constant. The coefficients can be determined to represent any analytic function within a region of convergence.

6. A Fourier series is an infinite series of terms that consist of coefficients times sine and cosine functions. It can represent almost any periodic function.

7. A Fourier transform is a representation of a function as an integral instead of a sum. Many modern instruments use Fourier transforms to produce spectra from raw data in another form.

8. A Laplace transform is a representation of a function that is similar to a Fourier transform.

## Objectives

After studying this chapter, you should be able to:

1. determine whether an infinite constant series converges,

2. determine how large a partial sum must be taken to approximate a series to a specified accuracy,

3. compute the coefficients for a power series to represent a given function,

4. determine the region of convergence of a power series,

5. determine the coefficients of a Fourier series to represent some elementary functions,

6. determine the Fourier transform of some elementary functions,

7. determine the Laplace transform of some elementary functions,

8. manipulate Laplace transforms using various theorems.

## 6.1 Constant Series

A sequence is a set of numerical quantities with a rule for generating one member of the set from the previous one. If the members of a sequence are added together, the result is a series. A finite series has a finite number of terms, and an infinite series has a infinite number of terms. If a series has terms that are constants, it is a constant series. Such a series can be written

$$
s = a _ {0} + a _ {1} + a _ {2} + a _ {3} + a _ {4} + \dots + a _ {n} + \dots\tag{6.1}
$$

For an infinite series, we define the nth partial sum as the sum of the first n terms:

$$
S _ {n} = a _ {0} + a _ {1} + a _ {2} + a _ {3} + \dots + a _ {n - 1}.\tag{6.2}
$$

The entire infinite series is the limit

$$
s = \lim _ {n \rightarrow \infty} S _ {n}.\tag{6.3}
$$

If this limit exists and is finite, we say that the series converges. If the magnitude of $S_{n}$ becomes larger and larger without bound as n becomes large, or if $S_{n}$ continues to oscillate without approaching a fixed value as n becomes large, we say that the series diverges.

The two questions that we generally ask about an infinite constant series are: (1) Does the series converge? (2) What is the value of the series if it does converge? Sometimes it is difficult to find the value of a convergent infinite series, and we then might ask how well we can approximate the series with a partial sum.

## Some Convergent Series

Let us consider a well-known convergent constant series:

$$
s = 1 + \frac {1}{2} + \frac {1}{4} + \frac {1}{8} + \dots + \frac {1}{2 ^ {n}} + \dots = \sum_ {n = 0} ^ {\infty} \frac {1}{2 ^ {n}}.\tag{6.4}
$$

There is no general method that is capable of finding the value of every series. $^{1}$ However, the value of this series is calculated in the following example.

EXAMPLE 6.1 Find the value of the series in Eq. (6.4).

SOLUTION ▶ We write the sum as the first term plus the other terms, with a factor of $\frac{1}{2}$ factored out of all the other terms:

$$
s = 1 + \frac {1}{2} \left(1 + \frac {1}{2} + \frac {1}{4} + \frac {1}{8} + \dots\right).
$$

The series in the parentheses is just the same as the original series. There is no problem due to the apparent difference that the series in the parentheses seems to have one less term than the original series, because both series have an infinite number of terms. We now write

$$
s = 1 + \frac {1}{2} s
$$

which can be solved to give

$$
s = 2.\tag{6.5}
$$

EXERCISE 6.1 ▶ Show that in the series of Eq. (6.4) any term of the series is equal to the sum of all the terms following it. (Hint: Factor a factor out of all of the following terms so that they will equal this factor times the original series, whose value is now known.)

The result of this exercise is of interest in seeing how a series can be approximated by a partial sum. For the series of Eq. (6.4), we can write

$$
s = S _ {n} + a _ {n - 1}.\tag{6.6}
$$

In some cases it is necessary to approximate a series with a partial sum, and sometimes Eq. (6.6) can be applied to other series as a rough measure of the error in approximating s by $S_{n}$ .

EXAMPLE 6.2 Determine which partial sum approximates the series of Eq. (6.4) to (a) 1% and (b) 0.001%.

SOLUTION ▶ Since 1% of 2 is equal to 0.02, we find the first term of the series that is equal to or smaller than 0.02, and take the partial sum that ends with that term. We have

$$
\frac {1}{2 ^ {6}} = \frac {1}{64} = 0.015625,
$$

so that the partial sum required is the one ending with $\frac{1}{64}$ , or $S_7$ . Its value is

$$
S _ {7} = 1.984375.
$$

Since $0.001\%$ of 2 is $2 \times 10^{-5}$ , and $1/2^n$ has the value $1.5259 \times 10^{-5}$ when $n = 16$ , we need the partial sum $S_{17}$ , which has the value $S_{17} = 1.999984741$ .

EXERCISE 6.2 ▶

Consider the series

$$
s = 1 + \frac {1}{2 ^ {2}} + \frac {1}{3 ^ {2}} + \frac {1}{4 ^ {2}} + \dots + \frac {1}{n ^ {2}} + \dots
$$

which is known to be convergent. Using Eq. (6.6) as an approximation, determine which partial sum approximates the series to (a) 1% and (b) 0.001%.

## The Geometric Series

The series of Eq. (6.4) is an example of a geometric series, which is defined to be

$$
s = a + a r + a r ^ {2} + a r ^ {3} + a r ^ {4} + \dots + a r ^ {n} + \dots\tag{6.7a}
$$

$$
= a r \left(1 + r + r ^ {2} + r ^ {3} + \dots + r ^ {n} + \dots\right),\tag{6.7b}
$$

where a and r are constants. In order for the infinite series of Eq. (6.7a) to converge, the magnitude of r must be less than unity. Otherwise, each term would be equal to or larger than the previous term, causing the sum to grow without bound (diverge) as more and more terms are added. However, r can be positive or negative. If r is negative, the sum has terms of alternating sign, but still converges only if $|r| < 1$ .

The value of a geometric series can be obtained in the same way as was the value of the series in Eq. (6.4),

$$
\begin{array}{r l} s & = a + r \left(a + a r + a r ^ {2} + a r ^ {3} + \dots\right) \\ & = a + r s \end{array}
$$

or

$$
\boxed {s = \frac {a}{1 - r}} \quad (| r | <   1).\tag{6.8}
$$

The partial sums of the geometric series are given by

$$
\boxed {S _ {n} = a + a r + a r ^ {2} + \dots + a r ^ {n - 1} = a \frac {1 - r ^ {n}}{1 - r}.}\tag{6.9}
$$

Equation (6.9) is valid for any value of $r$ , since a finite series always converges.

Instead of writing a series in the form used up to now, in which various terms are exhibited, we can use a standard symbol for a sum, a capital Greek sigma, which we introduced in Chapter 5. For example, the geometric series can be written as

$$
s = \sum_ {n = 0} ^ {\infty} a ^ {n}
$$

where the summation index n ranges from 0 to $\infty$ . The nth partial sum is written as

$$
S _ {n} = \sum_ {n = 0} ^ {n - 1} a ^ {n}
$$

EXAMPLE 6.3 The molecular partition function z is defined in the statistical mechanics of noninteracting molecules as the sum over all the states of one molecule

$$
z = \sum_ {i = 0} ^ {\infty} \exp \left(\frac {- E _ {i}}{k _ {B} T}\right),\tag{6.10}
$$

where i is an index specifying the state, $E_{i}$ is the energy that the molecule has when in state number i, $k_{B}$ is Boltzmann's constant, and T is the absolute temperature. If we consider only the vibration of a diatomic molecule, to a good approximation

$$
E _ {i} = E _ {v} = h \nu \left(v + \frac {1}{2}\right),\tag{6.11}
$$

where v is the vibrational frequency; v is the vibrational quantum number, which can take on the integral values 0, 1, 2, 3, etc.; and h is Planck's constant. Use Eq. (6.8) to find the value of the partition function for vibration.

SOLUTION ▶

$$
\begin{array}{r l} z _ {v i b} & = \sum_ {v = 0} ^ {\infty} \exp \left[ \frac {- h \nu \left(v + \frac {1}{2}\right)}{k _ {B} T} \right] \\ & = \exp \left(\frac {- h \nu}{2 k _ {B} T}\right) \sum_ {v = 0} ^ {\infty} \left[ \exp \left(\frac {h \nu}{k _ {B} T}\right) \right] ^ {v} \\ & = e ^ {- x / 2} \sum_ {v = 0} ^ {\infty} (e ^ {- x}) ^ {v}, \end{array}
$$

where $h\nu / k_B T = x$ , a positive quantity. The sum is a geometric series, so

$$
z _ {v i b} = \frac {e ^ {- x / 2}}{1 - e ^ {- x}}\tag{6.12}
$$

The series is convergent, because $e^{-x}$ is smaller than unity for all positive values of $x$ and is never negative.

EXERCISE 6.3 ▶

Find the value of the infinite series

$$
\sum_ {n = 0} ^ {\infty} [ \ln (2) ] ^ {n}
$$

Determine how well this series is approximated by $S_{2}$ , $S_{5}$ , and $S_{10}$ .

## A Divergent Series

The harmonic series is defined to be

$$
s = 1 + \frac {1}{2} + \frac {1}{3} + \frac {1}{4} + \dots + \frac {1}{n} + \dots .\tag{6.13}
$$

Here are a few partial sums of this series:

$$
\begin{array}{r l} S _ {1} & = 1 \\ S _ {2} & = 1.5 \\ S _ {200} & = 6.87803 \\ S _ {1000} & = 8.48547 \\ S _ {100, 000} & = 13.0902. \end{array}
$$

However, the harmonic series diverges.

$$
s = \lim _ {n \to \infty} S _ {n} = \infty .
$$

Many people are surprised when they first learn that this series diverges, because the terms keep on getting smaller as you go further into the series. This is a necessary condition for a series to converge, but it is not sufficient. We will show that the harmonic series is divergent when we introduce tests for convergence.

EXERCISE 6.4 ▶ Use a spreadsheet or a computer program to evaluate partial sums of the harmonic series and use it to verify the foregoing values.

There are a number of constant series listed in Appendix C, and additional series can be found in the references listed at the end of the chapter.

## Tests for Convergence of a Series

There are several tests that will usually tell us whether an infinite series converges or not.

1. The Comparison Test. If a series has terms that are each smaller in magnitude than the corresponding term of a series known to converge, it is convergent. If a series has terms that are each larger in magnitude than the corresponding term of a series known to diverge, it is divergent.

2. The Alternating Series Test. If a series has terms that alternate in sign, it is convergent if the terms approach zero as you go further and further into the series and if each term is smaller in magnitude than the previous term.

3. The nth-Term Test. If the terms of a series approach some limit other than zero or do not approach any limit as you go further into the series, the series diverges.

4. The Integral Test. If a formula can be written to deliver the terms of a series

$$
a _ {n} = f (n),\tag{6.14}
$$

then the series will converge if the improper integral

$$
\int_ {1} ^ {\infty} f (x) d x\tag{6.15}
$$

converges and will diverge if the improper integral diverges.

5. The Ratio Test. For a series of positive terms or a series of negative terms, we define the limit

$$
r = \lim _ {n \rightarrow \infty} \frac {a _ {n + 1}}{a _ {n}}.\tag{6.16}
$$

If r < 1, the series converges. If r > 1, the series diverges. If r = 1, the test fails, and the series might either converge or diverge. If the ratio does not approach any limit but does not increase without bound, the test also fails.

EXAMPLE 6.4 Apply the ratio test and the integral test to the harmonic series, Eq. (6.13).

SOLUTION ▶ Apply the ratio test:

$$
r = \lim _ {n \rightarrow \infty} \left[ \frac {1 / n}{1 / (n - 1)} \right] = \lim _ {n \rightarrow \infty} \frac {n - 1}{n} = 1.
$$

The ratio test fails. Apply the integral test:

$$
\int_ {1} ^ {0} \frac {1}{x} d x = \ln (x) \bigg | _ {1} ^ {\infty} = \lim _ {b \to \infty} [ \ln (b) - \ln (1) ] = \infty .
$$

The series diverges by the integral test.

EXAMPLE 6.5 Determine whether the series converges:

$$
s = 1 - \frac {1}{2} + \frac {1}{3} - \frac {1}{4} + \frac {1}{5} - \dots = \sum_ {n = 1} ^ {\infty} \frac {(- 1) ^ {n - 1}}{n}.
$$

SOLUTION ▶ This is an alternating series, so the alternating series test applies. Since every term approaches more closely to zero than the previous term, the series is convergent.

EXAMPLE 6.6 Determine whether the series converges:

$$
s = 1 - \frac {1}{2} + \frac {2}{2} - \frac {1}{3} + \frac {2}{3} - \frac {1}{4} + \frac {2}{4} - \frac {1}{5} + \frac {2}{5} - \dots .
$$

SOLUTION ▶ This is a tricky series, because it is an alternating series, and the nth term approaches zero as n becomes large. However, the series diverges. The alternating series test does not apply, because it requires that each term be closer to zero than the previous term. Half the time as you go from one term to the next in this series, the magnitude increases instead of decreasing. Let us manipulate the series by subtracting each negative term from the following positive term to obtain

$$
s = 1 + \frac {1}{2} + \frac {1}{3} + \frac {1}{4} + \frac {1}{5} + \dots .
$$

This is the harmonic series, which we already found to diverge.

EXERCISE 6.5 ▶

Show that the geometric series converges if $r^2 < 1$ .

## EXERCISE 6.6 ▶

Test the following series for convergence.

(a) $\sum_{n=0}^{\infty}\left(1/n^{2}\right)$ .

(b) $\sum_{n=0}^{\infty}(1/n!)$ .

(c) $\sum_{n=0}^{\infty}((-1)^{n}(n-1)/n^{2})$ .

(d) $\sum_{n=0}^{\infty}((-1)^{n} n / n!)$ .

![[3a284e568caa095d2f9bab2b2cba913ddad4906432c96743bf90cfa2a84a2d0d.jpg]]

Note. $n!$ ( $n$ factorial) is defined for positive integral values of $n$ to be $n(n - 1)(n - 2) \ldots (2)(1)$ , and is defined to equal 1 if $n = 0$ .

## 6.2 Functional Series

A functional series has terms that are constants times functions. If a single independent variable is called x,

$$
s (x) = a _ {0} g _ {0} (x) + a _ {1} g _ {1} (x) + a _ {2} g _ {2} (x) + a _ {3} g _ {3} (x) + \dots .\tag{6.17}
$$

We call the set of constant quantities $a_{0}$ , $a_{1}$ , $a_{2}$ , and so on, the coefficients of the series and the set of functions $g_{0}$ , $g_{1}$ , $g_{2}$ , $g_{3}$ , … the basis functions. Just as with constant series, a functional series such as that of Eq. (6.17) might converge or it might diverge. However, it might converge for some values of x and diverge for others. If there is an interval of values of x such that the series converges for all values of x in that interval, we say that the series is convergent in that interval.

There is an important mathematical concept called uniform convergence. If a functional series converges in some interval, it is uniformly convergent in that interval if it converges with at least a certain fixed rate of convergence in the entire interval. We do not discuss the details of this concept. $^{2}$ If a functional series is uniformly convergent in some interval, it has been shown to have some useful mathematical properties, which we discuss later.

There are two problems to be faced in constructing a series to represent a given function. The first is finding the values of the coefficients so that the function will be correctly represented. The second is finding the interval in which the series is convergent and in which it represents the given function.

## Power Series

A common type of functional series is the power series, in which the basis functions are powers of x - h, where x is the independent variable and h is a constant (it can equal zero).

$$
s (x) = a _ {0} + a _ {1} (x - h) + a _ {2} (x - h) ^ {2} + a _ {3} (x - h) ^ {3} + \dots ,\tag{6.18}
$$

where $a_{0}$ , $a_{1}$ , and so on, are constant coefficients. An infinite series of this form is called a Taylor series, and if h = 0 it is called a Maclaurin series. If we represent a function by a power series, we say that we expand the function in terms of the power series. Several methods of theoretical chemistry, such as the perturbation method in quantum mechanics, use power series.

## Maclaurin Series

A Maclaurin series to represent a function $f(x)$ is written

$$
f (x) = a _ {0} + a _ {1} x + a _ {2} x ^ {2} + \dots = s (x),\tag{6.19}
$$

where $f(x)$ is the function and $s(x)$ is the series. We now show how to determine the a coefficients. In order for the function and the series to be equal at all values of x, they must be equal at x = 0, which means that

$$
\boxed {f (0) = s (0) = a _ {0}}.\tag{6.20}
$$

This determines $a_0$ .

We also require that all derivatives of the function and of the series be equal at x = 0. This is sufficient for the series to represent the function in some interval around x = 0. Only a function that possesses derivatives of all orders at x = 0 can be represented by a Maclaurin series. Such a function is said to be analytic at x = 0. The nth derivative of the series at x = 0 is

$$
\left(\frac {d ^ {n} s}{d x ^ {n}}\right) _ {x = 0} = n! a _ {n},\tag{6.21}
$$

where $n!$ ( $n$ factorial) is defined for $n \geq 1$ by

$$
n! = n (n - 1) (n - 2) \dots (2) (1).
$$

This gives us a general formula for the coefficients in a Maclaurin series to represent the function $f(x)$ :

$$
\boxed {a _ {n} = \frac {1}{n !} \left(\frac {d ^ {n} f}{d x ^ {n}}\right) _ {0} \quad (n = 1, 2, 3 \dots).}\tag{6.22}
$$

A power series that is obtained by using Eq. (6.22) to obtain the coefficients faithfully represents the appropriate function in the vicinity of x = 0 if it converges and if infinitely many terms are taken. However, we must discuss how far from x = 0 we can go and still represent the function by the series.

EXAMPLE 6.7 Find all the coefficients for the Maclaurin series representing $\sin (x)$ .

SOLUTION ▶ Since sin (θ) = 0,

$$
\begin{array}{l} a _ {0} = 0 \\ a _ {1} = \left[ \frac {d}{d x} \sin (x) \right] _ {x = 0} = \cos (0) = 1, \end{array}\tag{6.23}
$$

where the subscript indicates that the derivative is evaluated at x = 0. The second partial sum of the series is therefore

$$
S _ {2} = 0 + x = x
$$

giving the same approximation as in Eq. (2.26). Figure 6.1 shows the function $\sin(x)$ and the approximation, $S_{2}=x$ . The derivatives of $\sin(x)$ follow a repeating pattern:

$$
\begin{array}{r c l} f (x) & = & \sin (x) \\ \frac {d f}{d x} & = & \cos (x) \\ \frac {d ^ {2} f}{d x ^ {2}} & = & - \sin (x) \\ \frac {d ^ {3} f}{d x ^ {3}} & = & - \cos (x) \\ \frac {d ^ {4} f}{d x ^ {4}} & = & \sin (x), \end{array}
$$

When these are evaluated at x = 0, all of the even-numbered derivatives vanish, and the odd-numbered derivatives are alternately equal to 1 and -1:

$$
\boxed {\sin (x) = x - \frac {1}{3 !} x ^ {3} + \frac {1}{5 !} x ^ {5} - \frac {1}{7 !} x ^ {7} + \dots .}\tag{6.24}
$$

![[39083777805a90dfe1a75feb35c5cff31f6e80e64fe4dc004291665a63256109.jpg]]  
Figure 6.1 ▶ The function $\sin(x)$ and the approximation $S_{2}=x$ .

EXERCISE 6.8 ▶

(a) Show that the Maclaurin series for $e^x$ is

$$
\boxed {e ^ {x} = 1 + \frac {1}{1 !} x + \frac {1}{2 !} x ^ {2} + \frac {1}{3 !} x ^ {3} + \frac {1}{4 !} x ^ {4} \dots .}\tag{6.25}
$$

(b) Find the Maclaurin series for $\cos (x)$ .


## Taylor Series

A Taylor series has the form

$$
s (x) = a _ {0} + a _ {1} (x - h) + a _ {2} (x - h) ^ {2} + a _ {3} (x - h) ^ {3} + \dots ,
$$

where h is not equal to zero. We say that a Taylor series is expanded around x = h. There are a number of important functions that are not analytic at x = 0, and these cannot be represented by a Maclaurin series, for which h = 0. One such function is $\ln(x)$ . The first derivative of this function is 1/x, which becomes infinite as $x \to 0$ , as do the other derivatives. Although there is no Maclaurin series for $\ln(x)$ , you can find a Taylor series for a positive value of h.

In order to find the coefficients for a Taylor series, we require the function and the series to be equal at x = h and to have the same derivatives of all orders at x = h. This gives

$$
\boxed {a _ {0} = f (h); \quad a _ {n} = \frac {1}{n !} \left(\frac {d ^ {n} f}{d x ^ {n}}\right) _ {x = h},}\tag{6.26}
$$

where $f(x)$ is the function to be represented and the subscript h indicates that the derivative is to be evaluated at x = h.

EXAMPLE 6.8 Find the Taylor series for $\ln(x)$ , expanding about x = 1.

SOLUTION ▶ The first derivative of $\ln(x)$ is 1/x, which equals 1 at x = 1. The second derivative is $-1/x^{2}$ , which equals 1 at x = 1. The derivatives follow a regular pattern,

$$
\left(\frac {d ^ {n} f}{d x ^ {n}}\right) _ {x = 1} = (- 1) ^ {n - 1} (n - 1)!
$$

so that

$$
\boxed {\ln (x) = (x - 1) - \frac {1}{2} (x - 1) ^ {2} + \frac {1}{3} (x - 1) ^ {3} - \frac {1}{4} (x - 1) ^ {4} + \dots .}\tag{6.27}
$$

EXERCISE 6.9 ▶ Find the Maclaurin series for $\ln(1 + x)$ . You can save some work by using the result of Example 6.8.

$$
x = \pi / 2.
$$

Find the Taylor series for $\cos (x)$ , expanding about

## The Convergence of Power Series

If a series is to represent a function $f(x)$ in some interval, it must be convergent in the entire interval and must converge to the value of the function for every value of x in the interval. For a fixed value of x, the series $s(x)$ is no different from a constant series, and all the tests for convergence of Section 6.1 can be applied. We can then consider different fixed values of x and determine the interval of convergence, that interval in which the series is convergent.

EXAMPLE 6.9 Investigate the convergence of the series for $\ln (x)$ in Eq. (6.27).

SOLUTION ▶ Let us consider three cases: x = 1, x > 1, and x < 1. If x = 1, the entire series vanishes, as does the function, so the series converges to the value of the function for x = 1. For x > 1, the series is an alternating series, and we can apply the alternating series test. The nth term of the series is

$$
t _ {n} = a _ {n} (x - 1) ^ {n} = \frac {(x - 1) ^ {n} (- 1) ^ {n - 1}}{n}.
$$

Look at the limit of this as $n$ becomes large:

$$
\lim _ {n \to \infty} t _ {n} = \left\{ \begin{array}{l l} 0 & \text {if} | x - 1 | \leq 1 \text {or} 0 \leq x \leq 2 \\ \infty & \text {if} | x - 1 | > 1 \text {or} x > 2. \end{array} \right.
$$

The interval of convergence for x > 1 extends up to and including x = 2. For x < 1, the series is not alternating. We apply the ratio test.

$$
r = \lim _ {n \rightarrow \infty} \frac {t _ {n}}{t _ {n - 1}} = \lim _ {n \rightarrow \infty} \left[ - \frac {(x - 1) ^ {n} / n}{(x - 1) ^ {n - 1} / (n - 1)} \right] = - (x - 1) = 1 - x.
$$

This will be less than unity if x lies between 0 and 1, but if x = 0, the text fails. However, if x = 0, the series is the same as the harmonic series except for the sign, and thus diverges. The interval of convergence is $0 < x \leq 2$ .

We summarize the behavior of the Taylor series representation of the previous example: There is a point at which the logarithm function is not analytic, at x = 0. The function is analytic to the right of this point, and the series equals the function for positive values arbitrarily close to x = 0. Beyond x = 2, the series diverges. The interval of convergence is centered on the point about which the function is expanded, which is x = 1 in this case. That is, the distance from x = 1 to the left end of the interval of convergence is 1 unit, and the distance from x = 1 to the right end of the interval of convergence is also 1 unit. This distance is called the radius of convergence. Even though the function is defined for values of x beyond x = 2, the series does not converge and cannot represent the function for values of x beyond x = 2. Another Taylor series expanded about a value of x larger than x = 1 can represent the logarithm function beyond x = 2.

EXERCISE 6.11 ▶ Find the Taylor series for $\ln(x)$ , expanding about x = 2, and show that the radius of convergence for this series is equal to 2, so that the series can represent the function up to and including x = 4.

The behavior of the Taylor series representation of the logarithm function is typical. In general, the interval of convergence is centered on the point about which we are expanding. The radius of convergence is the distance from the point about which we are expanding to the closest point at which the function is not analytic, and the interval of convergence extends by this distance in either direction. If a function is defined on both sides of a point at which the function is not analytic, it is represented on the two sides by different series.

EXAMPLE 6.10 Find the interval of convergence for the series representing the exponential function in Eq. (6.25).

SOLUTION ▶ We apply the ratio test,

$$
r = \lim _ {n \to \infty} \frac {t _ {n}}{t _ {n - 1}} = \lim _ {n \to \infty} \frac {x ^ {n} / n !}{x ^ {n - 1} / (n - 1) !} = \lim _ {n \to \infty} \frac {x}{n}.
$$

This limit vanishes for any real finite value of $x$ , so the series converges for any real finite value of $x$ , and the radius of convergence is infinite.

EXERCISE 6.12 ▶ Find the series for $1/(1-x)$ , expanding about $x=0$ . What is the interval of convergence?

EXERCISE 6.13 ▶ Find the interval of convergence for the series for sin (x) and for cos (x).

Unfortunately, the situation is not always so simple as in the examples we have been discussing. A power series can represent a function for complex values of the independent variable, and points in the complex plane at which the function is not analytic can determine the radius of convergence. A Taylor series converges to the function in a circle in the complex plane with radius equal to the radius of convergence. The radius of convergence is the distance from the point about which we expand to the closest point in the complex plane at which the function is not analytic.

For example, if we wanted to construct a Maclaurin series for the function

$$
f (x) = \frac {1}{1 + x ^ {2}}
$$

the radius of convergence would be determined by discontinuities at x = i and x = -i even though there are no discontinuities for real values of x. The radius of convergence equals unity, the distance from the origin to $x = \pm i$ in the Argand plane. We do not discuss the behavior of power series in the complex plane, but you can read more about this topic in the book by Kreyszig listed at the end of the book.

In physical chemistry there are a number of applications of power series, but in most applications, a partial sum is actually used to approximate the series. For example, the behavior of a nonideal gas is often described by use of the virial series or virial equation of state,

$$
\frac {P V _ {m}}{R T} = 1 + \frac {B _ {2}}{V _ {m}} + \frac {B _ {3}}{V _ {m} ^ {2}} + \frac {B _ {4}}{V _ {m} ^ {3}} + \dots ,\tag{6.28}
$$

where P is the pressure, $V_{m}$ is the molar volume of the gas, T is the Kelvin temperature, and R is the ideal gas constant. The coefficients $B_{2}$ , $B_{3}$ , and so on, are called virial coefficients and are functions of T but not functions of $V_{m}$ . If all the virial coefficients were known for a particular gas, the virial series would represent exactly the volumetric behavior of that gas at all values of $1/V_{m}$ . However, only the first few virial coefficients can be determined experimentally or theoretically, so a partial sum must be used. For many purposes, the two-term truncated equation is adequate:

$$
\frac {P V _ {m}}{R T} \approx 1 + \frac {B _ {2}}{V _ {m}}.\tag{6.29}
$$

There is another commonly used series equation of state, sometimes called the pressure virial equation of state:

$$
P V _ {m} = R T + A _ {2} P + A _ {3} P ^ {2} + A _ {4} P ^ {3} + \dots ,\tag{6.30}
$$

This is a Maclaurin series in P. It is also truncated for practical use.

EXAMPLE 6.11 Show that the coefficient $A_{2}$ in Eq. (6.30) is equal to the coefficient $B_{2}$ in Eq. (6.28).

SOLUTION ▶ We multiply Eq. (6.28) on both sides by $RT/V_{m}$ to obtain

$$
P = \frac {R T}{V _ {m}} + \frac {R T B _ {2}}{V _ {m} ^ {2}} + \frac {R T B _ {3}}{V _ {m} ^ {3}} + \dots ,\tag{6.31}
$$

This must be equal to

$$
P = \frac {R T}{V _ {m}} + \frac {A _ {2} P}{V _ {m}} + \frac {A _ {3} P ^ {2}}{V _ {m}} + \dots .\tag{6.32}
$$

We convert the second series into a series in $1/V_{m}$ by substituting the first series into the right-hand side wherever a P occurs. When the entire series on the right-hand side of Eq. (6.31) is squared, every term will have a least a $V_{m}^{2}$ in the denominator [see Eq. (11) of Appendix C for the square of a series]. Therefore, Eq. (6.32) becomes

$$
P = \frac {R T}{V _ {m}} + \frac {A _ {2}}{V _ {m}} \left(\frac {R T}{V _ {m}} + \frac {R T B _ {2}}{V _ {m} ^ {2}} + \dots\right) + O \left(\frac {1}{V _ {m}}\right) ^ {3},\tag{6.33}
$$

where the symbol $O(1/V_{m})^{3}$ stands for terms of degree $1/V_{m}^{3}$ or higher (containing no powers of $1/V_{m}$ lower than the third power).

Equation (6.33) is thus

$$
P = \frac {R T}{V _ {m}} + \frac {R T A _ {2}}{V _ {m} ^ {2}} + 0 \left(\frac {1}{V _ {m}}\right) ^ {3}.\tag{6.34}
$$

We now use a fact about series [Eq. (9) of Appendix C]: If two power series in the same independent variable are equal to each other for all values of the independent variable, then any coefficient in one series is equal to the corresponding coefficient of the other series.

Comparison of Eq. (6.34) with Eq. (6.31) shows that

$$
B _ {2} = A _ {2}.
$$

Another application of a power series in physical chemistry is in the discussion of colligative properties (freezing-point depression, boiling-point elevation, and osmotic pressure). If $X_{1}$ is the mole fraction of solvent, $\Delta_{vap}H_{m}$ is the molar heat of vaporization of the solvent, $T_{0}$ is the pure solvent's boiling temperature, and $T$ is the solution's boiling temperature, it is shown in physical chemistry textbooks that

$$
- \ln (X _ {1}) = \frac {\triangle_ {v a p} H _ {m}}{R} \left(\frac {1}{T _ {0}} - \frac {1}{T}\right).\tag{6.35}
$$

If there is only one solute (component other than the solvent), then its mole fraction, $X_{2}$ , is given by

$$
X _ {2} = 1 - X _ {1}.\tag{6.36}
$$

The logarithm on the left-hand side of Eq. (6.35) is represented by the power series

$$
- \ln (X _ {1}) = - \ln (1 - X _ {2}) = X _ {2} + \frac {1}{2} X _ {2} ^ {2} + \dots .\tag{6.37}
$$

If $X_{2}$ is not too large, we can truncate this series after one term and write

$$
X _ {2} \approx \frac {\Delta_ {v a p} H _ {m}}{R} \left(\frac {1}{T _ {0}} - \frac {1}{T}\right).\tag{6.38}
$$

EXERCISE 6.14 ▶ Determine how large $X_{2}$ can be before the truncation of Eq. (6.37) that was used in Eq. (6.38) is inaccurate by more than 1%.

## 6.3 Fourier Series

If we want to produce a series that will converge rapidly, so that we can approximate it fairly well with a partial sum containing only a few terms, it is good to choose basis functions that have as much as possible in common with the function to be represented. The basis functions in Fourier series $^{3}$ are sine and cosine functions, which are periodic functions. Fourier series are used to represent periodic functions. A Fourier series that represents a periodic function of period 2L is

$$
f (x) = a _ {0} + \sum_ {n = 1} ^ {\infty} a _ {n} \cos \left(\frac {n \pi x}{L}\right) + \sum_ {n = 1} ^ {\infty} b _ {n} \sin \left(\frac {n \pi x}{L}\right).\tag{6.39}
$$

EXERCISE 6.15 ▶ Using trigonometric identities show that the basis functions in the series in Eq. (6.39) are periodic with period 2L. That is, show for arbitrary n that

$$
\sin \left[ \frac {n \pi (x + 2 L)}{L} \right] = \sin \left(\frac {n \pi x}{L}\right)
$$

and

$$
\cos \left[ \frac {n \pi (x + 2 L)}{L} \right] = \cos \left(\frac {n \pi x}{L}\right).
$$

![[878946a2ae8ff85f2243db9d529b9befe74ec6f26b6f8d15b1a848cf4865c958.jpg]]

Fourier series occur in various physical theories involving waves, because waves often behave sinusoidally. For example, Fourier series can represent the constructive and destructive interference of standing waves in a vibrating string. $^{4}$ This fact provides a useful way of thinking about Fourier series. A periodic function of arbitrary shape is represented by adding up sine and cosine functions with shorter and shorter wavelengths, having different amplitudes adjusted to represent the function correctly. This is analogous to the constructive and destructive interference of waves resulting from the addition of their displacements.

There are some important mathematical questions about Fourier series, including the convergence of a Fourier series and the completeness of the basis functions. A set of basis functions is said to be complete for representation of a set of functions if a series in these functions can accurately represent any function from the set. We do not discuss the mathematics, but state the facts that were proved by Fourier: (1) any Fourier series in x is uniformly convergent for all real values of x; (2) the set of sine and cosine basis functions in Eq. (6.39) is a complete set for the representation of periodic functions of period 2L. In many cases of functional series, the completeness of the set of basis functions has not been proved, but most people assume completeness and proceed.

## Finding the Coefficients of a Fourier Series—Orthogonality

In a power series, we found the coefficients by demanding that the function and the series have equal derivatives at the point about which we were expanding. In a Fourier series, we use a different procedure, utilizing a property of the basis functions that is called orthogonality. This property is expressed by the three equations:

$$
\int_ {- L} ^ {L} \cos \left(\frac {m \pi x}{L}\right) \cos \left(\frac {n \pi x}{L}\right) d x = L \delta_ {m n} = \left\{ \begin{array}{l l} L & \mathrm{if} m = n \\ 0 & \mathrm{if} m \neq n \end{array} \right.\tag{6.40}
$$

$$
\int_ {- L} ^ {L} \cos \left(\frac {m \pi x}{L}\right) \sin \left(\frac {n \pi x}{L}\right) d x = 0\tag{6.41}
$$

$$
\int_ {- L} ^ {L} \sin \left(\frac {m \pi x}{L}\right) \sin \left(\frac {n \pi x}{L}\right) d x = L \delta_ {m n}.\tag{6.42}
$$

The quantity $\delta_{mn}$ is called the Kronecker delta. It is equal to unity if its two indices are equal and is equal to zero otherwise. Equations (6.40) and (6.42) do not apply if m and n are both equal to zero. The integral in Eq. (6.40) is equal to 2L if m = n = 0, and the integral in Eq. (6.42) is equal to zero if m = n = 0.

Two different functions that yield zero when multiplied together and integrated are said to be orthogonal to each other. Equations (6.40), (6.41), and (6.42) indicate that all the basis functions for the Fourier series of period 2L are orthogonal to each other. An integral of the product of two functions is sometimes called a scalar product of the two functions. This terminology is analogous to that used with vectors. If two vectors are at right angles to each other, they are said to be orthogonal to each other, and their scalar product is zero (see Chapter 2). Since each of the basis functions is orthogonal to the others, its scalar product with a different basis function vanishes, just as the scalar product of any two of the unit vectors i, j, and k vanishes.

To find $a_{m}$ , where $m \neq 0$ we multiply both sides of Eq. (6.39) by $\cos(m\pi x/L)$ and integrate from -L to L.

$$
\begin{array}{r l} \int_ {- L} ^ {L} f (x) \cos \left(\frac {m \pi x}{L}\right) d x & = \sum_ {n = 0} ^ {\infty} a _ {n} \int_ {- L} ^ {L} \cos \left(\frac {n \pi x}{L}\right) \cos \left(\frac {m \pi x}{L}\right) d x \\ & + \sum_ {n = 0} ^ {\infty} b _ {n} \int_ {- L} ^ {L} \sin \left(\frac {n \pi x}{L}\right) \cos \left(\frac {m \pi x}{L}\right) d x \end{array} \tag {6.43}
$$

We have incorporated the $a_{0}$ term into the first sum, using the fact that $\cos(0)=1$ . We have also used the fact that the integral of a sum is equal to the sum of the integrals of the terms if the series is uniformly convergent.

We now apply the orthogonality facts, Eqs. (6.40)-(6.42), to find that all of the integrals on the right-hand side of Eq. (6.43) vanish except for the term with two cosines in which $n = m$ . The result is

$$
\int_ {- L} ^ {L} f (x) \cos \left(\frac {m \pi x}{L}\right) d x = a _ {m} L.\tag{6.45}
$$

This is a formula for finding all of the a coefficients except for $a_0$ . To find $a_0$ , we use the fact that

$$
\int_ {- L} ^ {L} \cos (0) \cos (0) d x = \int_ {- L} ^ {L} d x = 2 L\tag{6.46}
$$

which leads to our working equations for the a coefficients:

$$
\boxed {a _ {0} = \frac {1}{2 L} \int_ {- L} ^ {L} f (x) d x}\tag{6.47}
$$

$$
\boxed {a _ {n} = \frac {1}{L} \int_ {- L} ^ {L} f (x) \cos \left(\frac {n \pi x}{L}\right) d x}\tag{6.48}
$$

A similar procedure consisting of multiplication by $\sin(m\pi x/L)$ and integration from -L to L yields

$$
\boxed {b _ {n} = \frac {1}{L} \int_ {- L} ^ {L} f (x) \sin \left(\frac {n \pi x}{L}\right) d x.}\tag{6.49}
$$

EXERCISE 6.16 ▶

Show that Eq. (6.49) is correct.

![[86428f3f34defbc4a4d1be69c61abeb4738e2882cdf97ce5171c935ea167652a.jpg]]

A function does not have to be analytic, or even continuous, in order to be represented by a Fourier series. It is only necessary that the function be integrable. As mentioned in Chapter 5, an integrable function can have step discontinuities, as long as the step in the function is finite. At a step discontinuity, a Fourier series will converge to a value halfway between the value just to the right of the discontinuity and the value just to the left of the discontinuity.

We can represent a function that is not necessarily periodic by a Fourier series if we are only interested in representing the function in the interval -L < x < L. The Fourier series will be periodic with period 2L, and the series will be equal to the function inside the interval, but not necessarily equal to the function outside the interval.

![[ad49f159dc3c7b2ca0d12a31c823343e3856222972b38287bf5b8ed09f45dbad.jpg]]

If the function $f(x)$ is an even function, all of the $b_{n}$ coefficients will vanish, and only the cosine terms will appear in the series. Such a series is called a Fourier cosine series. If $f(x)$ is an odd function, only the sine terms will appear, and the series is called a Fourier sine series. If we want to represent a function only in the interval 0 < x < L we can regard it as the right half of an odd function or the right half of an even function, and can therefore represent it either with a sine series or a cosine series. These two series would have the same value in the interval 0 < x < L but would be the negatives of each other in the interval -L < x < 0.

EXAMPLE 6.12 Find the Fourier series to represent the function $f(x) = x$ for the interval $-L < x < L$ .

SOLUTION ▶ The function is odd in the interval $(-L, L)$ , so the series will be a sine series. Although our function is defined only for the interval $(-L, L)$ , the series will be periodic, and will be the “sawtooth” function that is shown in Fig. 6.2.

The coefficients are obtained from Eq. (6.49). Since the integrand is the product of two odd functions, it is an even function and the integral is equal to twice the integral from 0 to L:

$$
b _ {n} = \frac {2}{L} x \sin \left(\frac {n \pi x}{L}\right) d x = \frac {2}{L} \left(\frac {L}{n \pi}\right) ^ {2} \int_ {0} ^ {n \pi} y \sin (y) d y = \frac {2 L}{n \pi} (- 1) ^ {n - 1}.
$$

The series is

$$
f (x) = \sum_ {n - 1} ^ {\infty} \frac {2 L}{n \pi} (- 1) ^ {n - 1} \sin \left(\frac {n \pi x}{L}\right).
$$

## EXERCISE 6.17 ▶

(a) Show that the $a_{n}$ coefficients for the series representing the function in Example 6.12 all vanish.

(b) Show that the series equals zero at $x = -L$ , $x = L$ , $x = 3L$ , etc., rather than equaling the function at this point.

![[764926fe1a0bc84fbd472a3188bb25abf873f2bedbb33c3d337b6aabb1dc5760.jpg]]  
Figure 6.2 ▶ The sawtooth function of Example 6.12.

![[c8f11f908aefc2faf7365bce00b38135b885d573e91e45d8dd32f152bf79185f.jpg]]  
Figure 6.3 ▶ The square wave function approximated by $S_{1}$ , $S_{2}$ , and $S_{10}$ .

EXERCISE 6.18 ▶

Find the Fourier cosine series for the even function

$$
f (x) = | x | \quad \text { for } - L <   x <   L.
$$

Draw a graph of the periodic function represented by the series.

![[ea4ea0cb4ee0c21ad998432954e29d9e457461142e1ed16f1f7940ecc232c0cc.jpg]]

It is a necessary condition for the convergence of Fourier series that the coefficients become smaller and smaller and approach zero as n becomes larger and larger. If a Fourier series is convergent, it will be uniformly convergent for all values of x. If convergence is fairly rapid, it might be possible to approximate a Fourier series by one of its partial sums. Figure 6.3 shows three different partial sums of the series that represent the “square-wave” function

$$
f (x) = \begin{array}{l} + 1 \text {for} 0 <   x <   L \\ - 1 \text {for} - L <   x <   0. \end{array}
$$

Only the right half of one period is shown. The first partial sum only vaguely resembles the function, but $S_{10}$ is a better approximation. Notice the little spike or overshoot near the discontinuity. This is a typical behavior and is known as the Gibbs phenomenon. $^{5}$ The partial sum $S_{100}$ fits the function more closely away from the discontinuity, but it has a spike near the discontinuity that is just as high as that of $S_{10}$ , although much narrower.

## Fourier Series with Complex Exponential Basis Functions

The sine and cosine basis functions are closely related to complex exponential functions, as shown in Eqs. (2.105) and (2.106). One can write

$$
b _ {n} \sin \left(\frac {n \pi x}{L}\right) + a _ {n} \cos \left(\frac {n \pi x}{L}\right) = \frac {1}{2} \left(a _ {n} - i b _ {n}\right) e ^ {i n \pi x / L} + \frac {1}{2} \left(a _ {n} + i b _ {n}\right) e ^ {i n \pi x / L}. \tag {6.50}\tag{6.50}
$$

It is therefore possible to rewrite Eq. (6.39) as an exponential Fourier series:

$$
\boxed {f (x) = \sum_ {n = - \infty} ^ {\infty} c _ {n} e ^ {i n \pi x / L}.}\tag{6.51}
$$

We have incorporated the terms with negative exponents into the same sum with the other terms by allowing the summation index to take on negative as well as positive values. The function being represented by a Fourier series does not have to be a real function. If it is a real function, the coefficients $a_{n}$ and $b_{n}$ will be real and the coefficients $c_{n}$ will be complex.

## Other Functional Series with Orthogonal Basis Sets

Fourier series are just one example of series using orthogonal sets of basis functions. For example, in quantum mechanics it is found that the eigenfunctions of quantum mechanical operators form orthogonal sets of functions, and these can be used as basis functions for series. It is generally assumed that such a set of functions is complete for representation of functions that obey the same boundary conditions as the basis functions. Boundary conditions are discussed in Chapter 8 in connection with differential equations.

Assume that we have a complete set of orthogonal functions, called $\psi_{1}$ , $\psi_{2}$ , $\psi_{3}$ , and so on, and that these functions have been normalized and that they are orthogonal to each other. This means that the functions have been multiplied by appropriate constants so that the scalar product of any one of the functions with itself is unity and that the scalar product of two of the functions vanishes:

$$
\int \psi_ {n} ^ {*} \psi_ {m} d x = \delta_ {n m} = \left\{ \begin{array}{l l} 1 & \text { if } n = m \\ 0 & \text { if } n \neq m \end{array} \right.\tag{6.52}
$$

In case the basis functions are complex, the scalar product is defined as the integral of the complex conjugate of the first function times the second function, as in Eq. (6.52).

Since the set of functions is assumed to be complete, we can expand an arbitrary function, f, in terms of the $\psi$ functions so long as f obeys the same boundary conditions as the $\psi$ functions.

$$
f = \sum_ {n} c _ {n} \psi_ {n}\tag{6.53}
$$

The sum in this equation will include one term for each function in the complete set and can have infinitely many terms.

In order to find the coefficients $c_{1}$ , $c_{2}$ , $c_{3}$ , and so on, we multiply by the complex conjugate of $\psi_{m}$ and integrate. With Eq. (6.52), our result is

$$
\boxed {\int \psi_ {m} ^ {*} f d x = \sum_ {n} c _ {n} \int \psi_ {m} ^ {*} \psi_ {n} d x = \sum_ {n} c _ {n} \delta_ {n m} = c _ {m}}\tag{6.54}
$$

When the final sum over n is carried, only the n = m term survives because of the Kronecker delta. Equations (6.47), (6.48), and (6.49) are special cases of this equation.

EXAMPLE 6.13 The normalized quantum-mechanical wave functions for the particle in a one-dimensional box of length a are

$$
\psi_ {n} = \left(\frac {2}{a}\right) ^ {1 / 2} \sin (n \pi x / a)
$$

These functions are a complete set for expansion of functions that are defined only in the region 0 < x < a and vanish at x = 0 and at x = a. That is, a linear combination of these functions can be an exact representation of the function in the region 0 < x < a. Find the coefficient $c_{1}$ if $f = x^{2} - ax$ .

## SOLUTION ▶

$$
\begin{array}{r l} c _ {1} & = \left(\frac {2}{a}\right) ^ {1 / 2} \left(\int_ {0} ^ {a} x ^ {2} \sin (\pi x / a) d x + a \int_ {0} ^ {a} x \sin (\pi x / a) d x\right) \\ & = \left(\frac {2}{a}\right) ^ {1 / 2} \left(\frac {a}{\pi}\right) ^ {3} \int_ {0} ^ {\pi} y ^ {2} \sin (y) d y - a \left(\frac {2}{a}\right) ^ {1 / 2} \left(\frac {a}{\pi}\right) ^ {2} \int_ {0} ^ {\pi} y \sin (y) d y \\ & = \left(\frac {2}{a}\right) ^ {1 / 2} \left(\frac {a}{\pi}\right) ^ {3} [ 2 y \sin (y) - (y ^ {2} - 2) \cos (y) ] \Big | _ {0} ^ {\pi} \\ & - a \left(\frac {2}{a}\right) ^ {1 / 2} \left(\frac {a}{\pi}\right) ^ {2} [ \sin (y) - y \cos (y) ] | _ {0} ^ {\pi} \\ & = \left(\frac {2}{a}\right) ^ {1 / 2} \left(\frac {a}{\pi}\right) ^ {3} [ (\pi^ {2} - 2) - 2 ] - a \left(\frac {2}{a}\right) ^ {1 / 2} (\frac {a}{\pi}) ^ {2} [ \pi^ {2} ] \\ & = - \frac {4 \sqrt {2} a ^ {5 / 2}}{\pi^ {3}} = - 0.182442 a ^ {5 / 2} \end{array}\tag{6.55}
$$

(6.56)

(6.57)

EXERCISE 6.19 ▶ Using Excel, construct a graph of the function f from the previous example in the region 0 < x < a and another graph of $c_{1}\psi_{1}$ . Compare the graphs and comment on how well the partial sum with one term approximates the function. Let a = 1 for your graphs.

EXERCISE 6.20 ▶ Write the formula for finding the coefficients for an exponential Fourier series. Is there any difference in the formulas for odd functions, even functions, or functions that are neither odd nor even? What conditions must the function obey to be represented by an exponential Fourier series?

## 6.4 Mathematical Operations on Series

Carrying out mathematical operations such as integration or differentiation on a functional series with a finite number of terms is straightforward, since no questions of convergence arise. However, carrying out such operations on an infinite series presents a few difficulties. The question arises whether differentiating each term and then summing the result gives the same result as first summing the series and then differentiating. Although we do not prove it, the principal fact is: If a series is uniformly convergent the result of operating on the series is the same as the result of operating on the individual terms and then summing the resulting series. For example, if

$$
f (x) = \sum_ {n = 0} ^ {\infty} a _ {n} g _ {n} (x)\tag{6.58}
$$

and if the series is uniformly convergent, then

$$
{\frac {d f}{d x}} = {\frac {d}{d x}} \left[ \sum_ {n = 0} ^ {\infty} a _ {n} g _ {n} (x) \right] = \sum_ {n = 0} ^ {\infty} a _ {n} {\frac {d g _ {n}}{d x}}.\tag{6.59}
$$

This amounts to interchange of the operations of summing and differentiating. Similarly, for a uniformly convergent series,

$$
\int_ {a} ^ {b} f (x) d x = \int_ {a} ^ {b} \left[ \sum_ {n = 0} ^ {\infty} a _ {n} g _ {n} (x) \right] d x = \sum_ {n = 0} ^ {\infty} a _ {n} \int_ {a} ^ {b} g _ {n} (x) d x.\tag{6.60}
$$

This amounts to interchange of the operations of summing and integrating.

We have already used Eq. (6.60) in the previous section in deriving the formula for the coefficients in the Fourier series, without commenting on the fact that the series must be uniformly convergent to justify this procedure.

EXAMPLE 6.14 Find the Maclaurin series for $\cos(x)$ from the Maclaurin series for $\sin(x)$ , using the fact that $d[\sin(x)]/dx=\cos(x)$ .

SOLUTION ▶ The series happens to be uniformly convergent for all values of x. From Eq. (6.29), we have

$$
\sin (x) = x - \frac {x ^ {3}}{3 !} + \frac {x ^ {5}}{5 !} - \frac {x ^ {7}}{7 !} + \dots
$$

so that

$$
\frac {d [ \sin (x) ]}{d x} = 1 - \frac {x ^ {2}}{2 !} + \frac {x ^ {4}}{4 !} - \frac {x ^ {6}}{6 !} + \dots .
$$

EXERCISE 6.21 ▶ From the Taylor series for $\ln(x)$ expanded about $x = 1$ given in Eq. (6.27), find the Taylor series for $1/x$ about $x = 1$ , using the fact that

$$
\frac {d [ \ln (x) ]}{d x} = \frac {1}{x}
$$

and the fact that the series is uniformly convergent for all x > 0. Comment on the range of values of x for which your series is valid.

## 6.5 Integral Transforms

Integral transforms are closely related to functional series. However, instead of a sum with each term consisting of a coefficient multiplying a basis function, we have an integral in which the summation index is replaced by an integration variable. The basis functions are multiplied by a function of this integration variable, and integration over this variable yields a representation of the function. This function of the integration variable is called the integral transform of the given function. The transform is a function of the integration variable, in the same way as the coefficients in a functional series depend on the value of the summation index. You can think of a transform as encoding the same information as in the original representation of the function, but with a different independent variable. There are several kinds of integral transforms, including Mellin transforms, Hankel transforms, and so forth, $^{6}$ but the principal kinds of transforms encountered by physical chemists are Fourier transforms and Laplace transforms.

## Fourier Transforms (Fourier Integrals)

Although Fourier transforms were once important only to mathematicians and some theoretical scientists, they are now widely used in spectroscopy, because instruments have been designed that produce a superposition of wave-like signals such that the spectrum is the Fourier transform of the detected signal. $^{7}$ Let us see how Fourier transforms compare with Fourier series, which are designed to represent periodic functions with period 2L. If we allow L to become larger and larger without bound, the values of $n\pi x/L$ become closer and closer together. We let

$$
k = \frac {n \pi}{L}.\tag{6.61}
$$

As the limit $L \rightarrow \infty$ is taken, k becomes a continuously variable quantity. In this limit, an exponential Fourier series becomes an integral, which is called a Fourier integral or a Fourier transform,

$$
f (x) = \frac {1}{\sqrt {2 \pi}} \int_ {- \infty} ^ {\infty} F (k) e ^ {i k x} d k,\tag{6.62}
$$

where the coefficient $c_{n}$ in Eq. (6.51) is replaced by a function of k, denoted by $F(k)$ .

The equation for determining $F(k)$ is analogous to Eq. (6.47), (6.48), and (6.49)

$$
F (k) = \frac {1}{\sqrt {2 \pi}} \int_ {- \infty} ^ {\infty} f (x) e ^ {- i k x} d x.\tag{6.63}
$$

We have introduced a factor of $1/\sqrt{2\pi}$ in front of the integral in Eq. (6.62) in order to have the same factor in front of this integral and the integral in Eq. (6.63).

The function $F(k)$ is called the Fourier transform of $f(x)$ and the function $f(x)$ is also called the Fourier transform of $F(k)$ . The function $f(x)$ is no longer required to be periodic, because the period 2L has been allowed to become infinite. Since we now have improper integrals, the functions $f(x)$ and $F(k)$ must have properties such that the integrals converge. For the integral of Eq. (6.63) to converge, the following integral must converge:

$$
\int_ {- \infty} ^ {\infty} | f (x) | ^ {2} d x.
$$

We say that the function $f(x)$ must be square integrable. The function $f(x)$ must approach zero as $x \to -\infty$ and as $x \to \infty$ to be square integrable. If the Fourier transform $F(k)$ exists, it will also be square integrable.

EXAMPLE 6.15 Find the Fourier transform of the Gaussian function

$$
f (x) = e ^ {- a x ^ {2}}.
$$

SOLUTION ▶

$$
F (k) = \frac {1}{\sqrt {2 \pi}} \int_ {- \infty} ^ {\infty} e ^ {- a x ^ {2}} e ^ {- i k x} d x.
$$

From Eq. (2.93),

$$
F (k) = \frac {1}{\sqrt {2 \pi}} \int_ {- \infty} ^ {\infty} e ^ {- a x ^ {2}} \cos (k x) d x - \frac {i}{\sqrt {2 \pi}} \int_ {- \infty} ^ {\infty} e ^ {- a x ^ {2}} \sin (k x) d x.
$$

The second integral in this equation is equal to zero because its integrand is an odd function. The first integral is twice the integral of Eq. (47) of Appendix F,

$$
\begin{array}{r c l} {F (k)} & = & {\frac {2}{\sqrt {2 \pi}} \int_ {0} ^ {\infty} e ^ {- a x ^ {2}} \cos (k x) d x = \frac {2}{\sqrt {2 \pi}} \frac {1}{2} \sqrt {\frac {\pi}{a}} e ^ {- k ^ {2} / 4 a}} \\ & = & {\frac {1}{\sqrt {2 a}} e ^ {- k ^ {2} / 4 a}.} \end{array}
$$

This example illustrates that interesting fact that the Fourier transform of a Gaussian function of x is another Gaussian function of k.

In the previous example the transform integral was separated into one part containing a cosine function and one containing a sine function. If the function $f(x)$ is an even function, its Fourier transform is a Fourier cosine transform:

$$
F (k) = \sqrt {\frac {1}{2 \pi}} \int_ {- \infty} ^ {\infty} f (x) \cos (k x) d x = \sqrt {\frac {2}{\pi}} \int_ {0} ^ {\infty} f (x) \cos (k x) d x \quad (f \text {   even }).\tag{6.64}
$$

The second version of the transform is called a one-sided cosine transform.

If $f(x)$ is an odd function, its Fourier transform is a Fourier sine transform:

$$
F (k) = \sqrt {\frac {1}{2 \pi}} \int_ {- \infty} ^ {\infty} f (x) \sin (k x) d x = \sqrt {\frac {2}{\pi}} \int_ {0} ^ {\infty} f (x) \sin (k x) d x \quad (f \text { odd }).\tag{6.65}
$$

There is a useful theorem for the Fourier transform of a product of two functions, called the convolution theorem or the Faltung theorem (Faltung is German for “folding”). The convolution of two functions $f(x)$ and $g(x)$ is defined as the integral

$$
{\frac {1}{\sqrt {2 \pi}}} \int_ {- \infty} ^ {\infty} f (y) g (x - y) d y.\tag{6.66}
$$

This integral is a function of x, and its Fourier transform is equal to $F(k)G(k)$ where $F(k)$ is the Fourier transform of $f(x)$ and $G(k)$ is the Fourier transform of $g(x)$ .⁸ Since the Fourier transform is nearly the same going in both directions, the analogous convolution

$$
\frac {1}{\sqrt {2 \pi}} \int_ {- \infty} ^ {\infty} F (l) G (k - l) d l\tag{6.67}
$$

has as its Fourier transform the product $f(x)g(x)$ .

EXERCISE 6.22 ▶

Take the two Gaussian functions

$$
f (x) = e ^ {- a x ^ {2}} \quad \text { and } \quad g (x) = e ^ {- b x ^ {2}}.
$$

Find the Fourier transform of the product of the functions using the convolution theorem. Show that this transform is the same as that obtained by multiplying the functions together and computing the transform in the usual way.

The two principal applications of Fourier transformation for chemists are in infrared spectroscopy and nuclear magnetic resonance spectroscopy. In both cases, the instrument takes raw data as a function of time and a spectrum as a function of frequency is obtained. In a Fourier transform infrared instrument, an interferometer varies the intensities of radiation of various frequencies as a function of time, and a detector determines the intensity as a function of time, producing an interferogram, which is the Fourier transform of the desired spectrum. The Fourier transformation is carried out by a computer program for predetermined values of the frequency, so that the spectrum is obtained only for a discrete set of frequencies. Numerical Fourier transformation is usually a fairly slow process, demanding a lot of computer time, but a Fast Fourier Transform (FFT) algorithm has been developed that makes the process practical for routine usage. $^{9}$ In a Fourier transform NMR instrument, a signal called the free induction decay signal is obtained as a function of time, and the Fourier transform of this signal is the desired NMR spectrum. The FFT algorithm is used to carry out the transformation.

## Laplace Transforms

The Laplace transform $F(s)$ of the function $f(t)$ is defined by $^{10}$

$$
\boxed {F (s) = \int_ {0} ^ {\infty} f (t) e ^ {- s t} d t.}\tag{6.68}
$$

We use the same notation as with the Fourier transform, denoting a Laplace transform by a capital letter and the function by a lowercase letter. You will have to tell from the context whether we are discussing a Fourier transform or a Laplace transform. We use the letter t for the independent variable of the function, since Laplace transforms are commonly applied to functions of the time. The letter x could also have been used.

TABLE 6.1 ▶ Laplace Transforms

<table><tr><td>F(s)</td><td>f(t)</td></tr><tr><td>1/s</td><td>1</td></tr><tr><td> $1/s^{2}$ </td><td>t</td></tr><tr><td> $n!/s^{n+1}$ </td><td> $t^{n}$ </td></tr><tr><td> $\frac{1}{s-a}$ </td><td> $e^{at}$ </td></tr><tr><td> $\frac{s}{s^{2}+k^{2}}$ </td><td> $\cos (kt)$ </td></tr><tr><td> $\frac{k}{s^{2}+k^{2}}$ </td><td> $\sin (kt)$ </td></tr></table>

The Laplace transform is similar to a one-sided Fourier transform, except that it has a real exponential instead of the complex exponential of the Fourier transform. If we consider complex values of the variables, the two transforms become different versions of the same transform, and their properties are related. $^{11}$ The integral that is carried out to invert the Laplace transform is carried out in the complex plane, and we do not discuss it. Fortunately, it is often possible to apply Laplace transforms without carrying out such an integral. $^{12}$ We will discuss the use of Laplace transforms in solving differential equations in Chapter 8.

The Laplace transform and its inverse are often denoted in the following way:

$$
F (s) = \mathcal {L} \{f (t) \}\tag{6.69}
$$

$$
f (t) = \mathcal {L} ^ {- 1} \left\{F (s) \right\}.\tag{6.70}
$$

Table 6.1 gives a few common Laplace transforms.

EXAMPLE 6.16 Find the Laplace transform of the function $f(t) = t^2$ .

SOLUTION ▶

$$
F (s) = \int_ {0} ^ {\infty} t ^ {2} e ^ {- s t} d t = \frac {1}{s ^ {3}} \int_ {0} ^ {\infty} u ^ {2} e ^ {- u} d u = \frac {2 !}{s ^ {3}},
$$

where we have used Eq. (1) of Appendix F to obtain the value of the definite integral.

EXERCISE 6.23 ▶ Find the Laplace transform $F(s)$ of the function $f(t) = e^{at}$ where $a$ is a constant.

There are several theorems that are useful in obtaining Laplace transforms of various functions. $^{13}$ The first is the shifting theorem:

$$
\boxed {\mathcal {L} \left\{e ^ {a t} f (t) \right\} = F (s - a)}.\tag{6.71}
$$

EXAMPLE 6.17 Use the theorem of Eq. (6.71) to obtain the Laplace transform of the function

$$
f (t) = e ^ {a t} \cos (k t).
$$

SOLUTION ▶ We transcribe the entry for $\cos(kx)$ from Table 6.1, replacing s by s - a, obtaining

$$
F (s) = \frac {s - a}{(s - a) ^ {2} + k ^ {2}}.
$$

EXERCISE 6.24 ▶

Find the Laplace transform of the function

$$
f (t) = t ^ {n} e ^ {a t}.
$$


The next useful theorem is the derivative theorem

$$
\boxed {\mathcal {L} \left\{f ^ {\prime} \right\} = s \mathcal {L} \left\{f \right\} - f (0)}  ,\tag{6.72}
$$

where we use the notation $f'$ for the first derivative of f. This theorem can be applied to the solution of first-order differential equations and can be applied repeatedly to obtain the extended version,

$$
\boxed {\mathcal {L} \left\{f ^ {(n)} \right\} = s ^ {n} \mathcal {L} \left\{f \right\} - s ^ {n - 1} f (0) - s ^ {n - 2} f ^ {\prime \prime} (0) - \dots - f ^ {(n - 1)} (0),}\tag{6.73}
$$

where we use the notation $f^{(n)}$ for the nth derivative of f, and so on.

EXERCISE 6.25 ▶

Derive the version of Eq. (6.73) for $n = 2$ .

The next theorem is for the Laplace transform of an integral of a given function $f$ ,

$$
\boxed {\mathcal {L} \left\{\int_ {0} ^ {t} f (u) d u \right\} = \frac {1}{s} \mathcal {L} \{f (t) \}}.\tag{6.74}
$$

These theorems can be used to construct the Laplace transforms of various functions, and to find inverse transforms without carrying out an integral in the complex plane.

EXAMPLE 6.18 Find the inverse Laplace transform of

$$
\frac {1}{s (s - a)}.
$$

SOLUTION ▶ From Table 6.1, we recognize $1/(s - a)$ as the Laplace transform of $e^{at}$ . From the theorem of Eq. (6.74),

$$
\mathcal {L} \left\{\int_ {0} ^ {t} e ^ {a u} d u \right\} = \frac {1}{s} \mathcal {L} \left\{e ^ {a t} \right\} = \frac {1}{s} \frac {1}{s - a}.
$$

Therefore, the inverse transform is

$$
\mathcal {L} ^ {- 1} \left\{\frac {1}{s (s - a)} \right\} = \int_ {0} ^ {t} e ^ {a y} d y = \frac {1}{a} (e ^ {a t} - 1).
$$

EXERCISE 6.26 ▶

Find the inverse Laplace transform of

$$
\frac {1}{s (s ^ {2} + k ^ {2})}.
$$


## SUMMARY

In this chapter we introduced mathematical series and mathematical transforms. A finite series is a sum of a finite number of terms, and an infinite series is a sum of infinitely many terms. A constant series has terms that are constants, and a functional series has terms that are functions. The two important questions to ask about a constant series are whether the series converges and, if so, what value it converges to. We presented several tests that can be used to determine whether a series converges. Unfortunately, there appears to be no general method for finding the value to which a convergent series converges.

A functional series is one way of representing a function. Such a series consists of terms, each one of which is a basis function times a coefficient. A power series uses powers of the independent variable as basis functions and represents a function as a sum of the appropriate linear function, quadratic function, cubic function, etc. We discussed Taylor series, which contain powers of x - h, where h is a constant, and also Maclaurin series, which are Taylor series with h = 0. Taylor series can represent a function of x only in a region of convergence centered on h and reaching no further than the closest point at which the function is not analytic. We found the general formula for determining the coefficients of a power series.

The other functional series that we discussed was the Fourier series, in which the basis functions are sine and cosine functions. This type of series is best suited for representing periodic functions and represents the function as a sum of the sine and cosine functions with the appropriate coefficients. The method of determining the coefficients to represent any particular function was given.

Integral transforms were discussed, including Fourier and Laplace transforms. Fourier transforms are the result of allowing the period of the function to be represented by a Fourier series to become larger and larger, so that the series approaches an integral in the limit. Fourier transforms are usually written with complex exponential basis functions, but sine and cosine transforms also occur. Laplace transforms are related to Fourier transforms, with real exponential basis functions. We presented several theorems that allow the determination of some kinds of inverse Laplace transforms and that allow later applications to the solution of differential equations.

## PROBLEMS

1. By use of the Maclaurin series already obtained in this chapter, prove the identity $e^{ix} = \cos(x) + i \sin(x)$ .

2.

a) Show that no Maclaurin series

$$
f (x) = a _ {0} + a _ {1} x + a _ {2} x ^ {2} + \dots
$$

can be formed to represent the function $f(x) = \sqrt{x}$ . Why is this?

b) Find the first few coefficients for the Maclaurin series for the function

$$
f (x) = \sqrt {1 + x}.
$$

3. Find the coefficients of the first few terms of the Taylor series

$$
\tan (x) = a _ {0} + a _ {1} \left(x - \frac {\pi}{4}\right) + a _ {2} \left(x - \frac {\pi}{4}\right) ^ {2} + \dots ,
$$

where x is measured in radians. What is the radius of convergence of the series?

4. Find the coefficients of the first few terms of the Maclaurin series

$$
\cosh (x) = a _ {0} + a _ {1} x + a _ {2} x ^ {2} + \dots ,
$$

What is the radius of convergence of the series?

5. The sine of $\pi/4$ radians ( $45^{\circ}$ ) is $\sqrt{2}/2 = 0.70710678\cdots$ . How many terms in the series

$$
\sin (x) = x - \frac {x ^ {3}}{3 !} + \frac {x ^ {5}}{5 !} - \frac {x ^ {7}}{7 !} + \dots
$$

must be taken to achieve 1% accuracy at $x = \pi / 4$ ?

6. The cosine of $30^{\circ}$ ( $\pi/6$ radians) is equal to $\sqrt{3}/2 = 0.866025\cdots$ . How many terms in the series

$$
\cos (x) = 1 - \frac {x ^ {2}}{2 !} + \frac {x ^ {4}}{4 !} - \frac {x ^ {6}}{6 !} + \dots .
$$

must be taken to achieve 0.1% accuracy $x = \pi / 6$ ?

7. Estimate the largest value of x that allows $e^{x}$ to be approximated to 1% accuracy by the following partial sum

$$
e ^ {x} \approx 1 + x.
$$

8. Estimate the largest value of x that allows $e^{x}$ to be approximated to 0.01% accuracy by the following partial sum

$$
e ^ {x} \approx 1 + x + \frac {x ^ {2}}{2 !}.
$$

9. How many terms in the series

$$
e ^ {x} \approx 1 + x + \frac {x ^ {2}}{2 !} + \frac {x ^ {3}}{3 !} + \dots
$$

must be taken to approximate $e^{x}$ to 0.01% accuracy for x = 1? For x = 2?

10. Find two different Taylor series to represent the function

$$
f (x) = \frac {1}{x ^ {2}}
$$

such that one series is

$$
f (x) = a _ {0} + a _ {1} (x - 1) + a _ {2} (x - 1) ^ {2} + \dots
$$

and the other is

$$
f (x) = b _ {0} + b _ {1} (x - 2) + b _ {3} (x - 2) ^ {2} + \dots .
$$

Show that $b_{n} = a_{n}/2^{n}$ for any value of n. Find the interval of convergence for each series (the ratio test may be used). Which series must you use in the vicinity of x = 3? Why?

11. Find the Taylor series in powers of $(x - 10)$ that represents the function $\ln(x)$ .

12. Using the Maclaurin series for $e^x$ , show that the derivative of $e^x$ is equal to $e^x$ .

13. Find the Maclaurin series that represents $\tan(x)$ . What is its radius of convergence?

14. Find the Maclaurin series that represents $\cosh(x)$ . What is its radius of convergence?

15. A certain electronic circuit produces the following sawtooth wave,

$$
f (t) = \left\{ \begin{array}{c l} a (- T - t), & - T <   t <   - T / 2 \\ a t, & - T / 2 <   t <   T / 2 \\ a (T - t), & - T / 2 <   t <   T, \end{array} \right.
$$

where a and T are constants and t represents the time. Find the Fourier series that represents this function. The definition of the function given is for only an interval of length 2T, but the Fourier series will be periodic. Make a graph of the function and of the first two partial sums.

16. Find the Fourier series that represents the square wave

$$
A (t) = \left\{ \begin{array}{l l} 0, & - T / 2 <   t <   0 \\ A _ {0}, & 0 <   t <   T / 2, \end{array} \right.
$$

where $A_0$ is a constant and $T$ is the period.

17. Find the Fourier series to represent the function

$$
A (t) = \left\{ \begin{array}{l l} e ^ {t}, & 0 <   t <   \pi \\ 0, & \text { elsewhere } \end{array} \right.
$$

Your series will be periodic and will represent the function only in the region $0 < t < \pi$ .

a) Use a sine series.

b) Use a cosine series.

18. Find the Fourier transform of the function $a \exp(-(x - x_{0})^{2}/b)$ , where a and b are constants.

19. Find the Fourier transform of the function $ae^{-b|x|}$ .

20. Find the one-sided Fourier sine transform of the function $ae^{-bx}$

21.

a) Find the Laplace transform of the function $a/(b^{2}+t^{2})$ , where a and b are constants.

b) Find the Fourier transform of the same function.

22. Show that $\mathcal{L}\{t\cos (kt)\} = (s^2 -k^2) / (s^2 +k^2)^2$

# Calculus With Several Independent Variables

## Preview

In this chapter, we discuss functions of more than one independent variable. For example, if you have a function of three independent variables, the function will deliver a value of the dependent variable if three values are specified: one value of each of the three independent variables. Differential calculus of such functions begins with the differential of the function, which represents an infinitesimal change in the dependent variable resulting from infinitesimal changes in the independent variables and consists of a sum of terms. Each term consists of a partial derivative with respect to an independent variable multiplied by the differential of that variable (an infinitesimal change in that independent variable). Maximum and minimum values of functions can be found using partial derivatives. There are two principal kinds of integrals that have integrand functions depending on several independent variables: line integrals and multiple integrals.

## Principal Facts and Ideas

1. Functions of several independent variables occur frequently in physical chemistry, both in thermodynamics and in quantum mechanics.

2. A derivative of a function of several variables with respect to one independent variable is a partial derivative. The other variables are treated as constants during the differentiation.

3. There are some useful identities allowing manipulations of expressions containing partial derivatives.

4. The differential of a function of several variables (an exact differential) has one term for each variable, consisting of a partial derivative times the differential of the independent variable. This differential form delivers the value of an infinitesimal change in the function produced by infinitesimal changes in the independent variables.

5. Differential forms exist that are not the differentials of any function. Such a differential form delivers the value of an infinitesimal quantity, but it is not the differential of any function. Such a differential form is called an inexact differential.

6. An integral of a differential with several independent variables is a line integral, carried out on a specified path in the space of the independent variables.

7. The line integral of an exact differential depends only on the endpoints of the path, but the line integral of an inexact differential depends on the path.

8. A multiple integral has as its integrand function a function of several variables, all of which are integrated.

9. The gradient operator is a vector derivative operator that produces a vector when applied to a scalar function.

10. The divergence operator is a vector derivative operator that produces a scalar when applied to a vector function.

11. Relative maxima and minima of a function of several variables are found by solving simultaneously the equations obtained by setting all partial derivatives equal to zero.

12. Constrained maxima and minima of a function of several variables can be found by the method of Lagrange multipliers.

## Objectives

After studying this chapter, you should be able to:

1. write formulas for the partial derivatives and for the differential of a function if given a formula for the function and use these in applications such as the calculation of small changes in a dependent variable;

2. perform a change of independent variables and obtain formulas relating different partial derivatives;

3. use identities involving partial derivatives to eliminate undesirable quantities from thermodynamic formulas;

4. identify an exact differential and an integrating factor;

5. perform a line integral with two independent variables;

6. perform a multiple integral;

7. change independent variables in a multiple integral;

8. use vector derivative operators;

9. find constrained and unconstrained maximum and minimum values of functions of several variables.

## 7.1 Functions of Several Independent Variables

A function of several independent variables is similar to a function of a single independent variable except that you must specify a value for each of the independent variables in order for the function to provide a value for the dependent variable. For example, the equilibrium thermodynamic properties of a fluid (gas or liquid) system of one substance and one phase are functions of three independent variables. If we choose a set of values for the temperature, T, the volume, V, and n, the amount of the substance in moles, then the other thermodynamic properties, such as pressure, P, and thermodynamic energy, U, are functions of these variables. We can write

$$
P = P (T, V, n)\tag{7.1a}
$$

$$
U = U (T, V, n)\tag{7.1b}
$$

We can choose any three of the variables as independent variables so long as at least of them is proportional to the size of the system. For example, we could also write

$$
\begin{array}{l} V = V (T, P, n) \\ U = U (P, V, n) \end{array}\tag{7.2}
$$

and so on. We assume that the functions that represent the behavior of physical systems are piecewise continuous with respect to each variable. That is, if we temporarily keep all but one of the independent variables fixed, the function behaves as a piecewise continuous function of that variable. We also assume that the function is piecewise single-valued.

In physical chemistry, we sometimes work with mathematical formulas that represent various functions. For example, if the temperature of a gas is fairly high and its volume is large enough, the pressure of a gas is given to a good approximation by the ideal gas equation

$$
P = P (T, V, n) = \frac {n R T}{V} = \frac {R T}{V _ {m}},\tag{7.3}
$$

where T is the temperature on the Kelvin scale, n is the amount of gas in moles, V is the volume, and R is the ideal gas constant. The molar volume, $V_{m}$ , is equal to V/n.

In addition to formulas, functions can be represented by graphs, by tables of values, or by infinite series. However, graphs, tables, and series become more complicated when used for a function of several variables than for functions of a single variable.

Figure 7.1 shows the dependence of the pressure of a nearly ideal gas as a function of the molar volume, $V_{m}$ . With only two axes on our graph, a curve can show the dependence of P on $V_{m}$ only for a fixed value of T. The figure shows curves for several members of a family of functions of $V_{m}$ , each for a different value of T.

Figure 7.2 is a perspective view of a three-dimensional graph representing P as a function of $V_{m}$ and T. The value of P is given by the height from the horizontal plane to a surface, which plays the same role as the curve in a two-dimensional graph. It is fairly easy to read quantitative information from the two-dimensional graph in Figure 7.1, but the perspective view in Figure 7.2 is more difficult to read numbers from. If you have more than two independent variables, a graph cannot be constructed. Sometimes attempts are made to show roughly how functions of three variables depend on their independent variables by drawing a perspective view of three axes, one for each of the independent variables, and then trying to communicate the approximate value of the dependent variable by a density of dots placed in the diagram.

![[f3b4ea65d346b5aa518e8866bdd8cef67a5bb01fbfa70652902bdda7f0ec71dd.jpg]]  
Figure 7.1 ▶ The pressure of a nearly ideal gas as a function of the molar volume $V_{m}$ at various fixed temperatures.

![[a87d6f32d9c1782de80899d80b51d555b97f82161e9cacaaf9adb1fd411ecdda.jpg]]  
Figure 7.2 ▶ The pressure of a nearly ideal gas a function of $V_{m}$ and T.

Tables of values are also cumbersome with two or more independent variables, since a function is now not a set of ordered pairs of numbers but a set of ordered sets of three numbers or four numbers, and so forth. For two independent variables, we need a rectangular array, with values of one independent variable along the top and values of the other along one side, and values of the dependent variable in the body of the array. For a third independent variable, we would need a different sheet of paper for each value of the third variable. The most common way to represent a function of several variables is with a mathematical formula.

## Changes in a Function of Several Variables

Many times in physical chemistry we do not have an accurate representation of a function representing some physical variable. Generally we are more interested in changes in a function than in the entire function, and in some cases we can find changes in a function even if we do not know the entire function. We now discuss changes in a function. Consider a gas contained in a cylinder with a movable piston and a valve through which additional gas can be admitted or removed, and let the entire system be immersed in a constant-temperature bath. For the present, we keep the valve closed, so that n is fixed (the system is now a closed system). Let us now make an infinitesimal change dV in the volume of the gas, keeping n and T fixed. If n and T are both fixed, P will behave just like a function of the one variable V. The change in P is given in the same way as with a function of one variable:

$$
d P = \left(\frac {d P}{d V}\right) d V \quad (n \text {   and   } T \text {   fixed }),\tag{7.4}
$$

where $dP / dV$ is the derivative of $P$ with respect to $V$ .

## Partial Derivatives

We adopt a new notation, replacing the d symbols by symbols that are slightly distorted lowercase Greek deltas and adding subscripts to specify the variables that are being held fixed.

$$
d P = \left(\frac {\partial P}{\partial V}\right) _ {n, T} d V \quad (n \text {   and   } T \text {   fixed }).\tag{7.5}
$$

The quantity $(\partial P/\partial V)_{n,T}$ is called the partial derivative of P with respect to V at constant n and T. The partial derivative is obtained by the differentiation techniques of Chapter 4, treating n and T like ordinary constants. There are as many partial derivatives of a given function as there are independent variables on which it depends. For an ideal gas, P is a function of T, V, and n.

$$
\left(\frac {\partial P}{\partial V}\right) _ {n, T} = \left(\frac {\partial}{\partial V} \left[ \frac {n R T}{V} \right]\right) _ {n, T} = - \frac {n R T}{V ^ {2}} (n \text {   and   } T \text {   fixed })\tag{7.6a}
$$

$$
\left(\frac {\partial P}{\partial T}\right) _ {n, V} = \left(\frac {\partial}{\partial T} \left[ \frac {n R T}{V} \right]\right) _ {n, V} = \frac {n R}{V} (n \text { and } V \text { fixed })\tag{7.6b}
$$

$$
\left(\frac {\partial P}{\partial n}\right) _ {T, V} = \left(\frac {\partial}{\partial n} \left[ \frac {n R T}{V} \right]\right) _ {T, V} = \frac {R T}{V} (T \text {   and   } V \text {   fixed }).\tag{7.6c}
$$

Each of these partial derivatives is obtained by the usual differentiation technique, treating the other variables as constants.

## Differentials

If we make an infinitesimal change dV in the volume and a change dT in the temperature of the gas while keeping n fixed, the change in P is the sum of two expressions like that in Eq. (7.5).

$$
d P = \left(\frac {\partial P}{\partial V}\right) _ {n, T} d V + \left(\frac {\partial P}{\partial T}\right) _ {n, V} d T \quad (n \text {   fixed }).\tag{7.7}
$$

Each term of this equation is the change due to the change in one independent variable, and each partial derivative thus is taken with the other independent variables treated as constants. If we make the changes dV in V, dT in T, and dn in n these changes affect P separately, and we can write for the total infinitesimal change in P,

$$
d P = \left(\frac {\partial P}{\partial V}\right) _ {n, T} d V + \left(\frac {\partial P}{\partial T}\right) _ {n, V} d T + \left(\frac {\partial P}{\partial n}\right) _ {T, V} d n.\tag{7.8}
$$

The infinitesimal change dP given by this expression is called the differential of P, or sometimes the total differential of P. It is a sum of terms, one for each independent variable. Each term gives the effect of one variable with the other treated as constants.

If we have a function y that depends on n independent variables, $x_{1}, x_{2}, x_{3}, \ldots, x_{n}$ , its differential is

$$
\boxed {d y = \sum_ {i = 1} ^ {n} \left(\frac {\partial y}{\partial x _ {i}}\right) _ {x ^ {\prime}} d x _ {i}}\tag{7.9}
$$

where the subscript $x'$ stands for keeping all of the variables except for $x_{i}$ fixed in the differentiation. This equation is sometimes called the fundamental equation of differential calculus.

The expression for $dP$ for an ideal gas is

$$
d P = - \frac {n R T}{V ^ {2}} d V + \frac {n R}{V} d T + \frac {R T}{V} d n\tag{7.10}
$$

For small but finite changes, an approximate version of this can be written

$$
\Delta P \approx - \frac {n R T}{V ^ {2}} \Delta V + \frac {n R}{V} \Delta T + \frac {R T}{V} \Delta n.\tag{7.11}
$$

EXAMPLE 7.1 Use Eq. (7.11) to calculate approximately the change in pressure of an ideal gas if the volume is changed from 20.0001 to 19.8001, the temperature is changed from 298.15 K to 299.00 K, and the amount of gas in moles is changed from 1.0000 mol to 1.0015 mol.

## SOLUTION ▶

$$
\begin{array}{r l} \Delta P & \approx - \frac {(1 .0000 \mathrm{mol}) (8 .3145 \mathrm{JK} ^ {- 1} \mathrm{mol} ^ {- 1}) (298 .15 \mathrm{K})}{(0 .020000 \mathrm{m} ^ {3}) ^ {2}} \left(- 0.200 \times 10 ^ {- 3} \mathrm{m} ^ {3}\right) \\ & + \frac {(1 .0000 \mathrm{mol}) (8 .3145 \mathrm{JK} ^ {- 1} \mathrm{mol} ^ {- 1})}{0 .020000 \mathrm{m} ^ {3}} (0.85 \mathrm{K}) \\ & + \frac {(8 .3144 \mathrm{JK} ^ {- 1} \mathrm{mol} ^ {- 1}) (298 .15 \mathrm{K})}{0 .020000 \mathrm{m} ^ {3}} (0.0015 \mathrm{mol}) \\ & \approx 1.779 \times 10 ^ {3} \mathrm{Nm} ^ {- 2} = 1.779 \times 10 ^ {3} \mathrm{Pa}, \end{array}
$$

where we use the fact that 1 J = 1 N m.

EXAMPLE 7.2 Compare the result of the previous example with the correct value of the pressure change.

SOLUTION ▶ We can calculate the actual change as follows. Let the initial values of n, V, and T be called $n_{1}$ , $V_{1}$ , and $T_{1}$ , and the final values be called $n_{2}$ , $V_{2}$ , and $T_{2}$ ,

$$
\begin{array}{r c l} \Delta P & = & P (n _ {2}, V _ {2}, T _ {2}) - P (n _ {1}, V _ {1}, T _ {1}) \\ & = & \frac {n _ {2} R T _ {2}}{V _ {2}} - \frac {n _ {1} R T _ {1}}{V _ {1}}. \end{array}
$$

The result of this calculation is $1.797 \times 10^{3} \, N m^{-2} = 1.797 \times 10^{3} \, Pa$ , so that our approximate value is in error by about 1%.

In these examples the exact calculation could be made more easily than the approximation. However, in physical chemistry it is frequently the case that a formula for a function is not known, but values for the partial derivatives are available, so that approximation can be made while the exact calculation cannot. For example, there is usually no simple formula giving the thermodynamic energy as a function of its independent variables. However, the differential of the thermodynamic energy of a system containing only one substance as a function of T, P, and n can be written as

$$
d U = \left(\frac {\partial U}{\partial T}\right) _ {P, n} d T + \left(\frac {\partial U}{\partial P}\right) _ {T, n} d P + \left(\frac {\partial U}{\partial n}\right) _ {P, T} d n.\tag{7.12}
$$

Experimental values of these partial derivatives are frequently available.

EXERCISE 7.1 ▶ For a sample of 1.000 mol (0.15384 kg) of liquid carbon tetrachloride, CCl₄

$$
\begin{array}{r l} \left(\frac {\partial U}{\partial T}\right) _ {P, n} & = 129.4 \mathrm{JK} ^ {- 1} \\ \left(\frac {\partial U}{\partial P}\right) _ {T, n} & = 8.51 \times 10 ^ {- 4} \mathrm{Jatm} ^ {- 1} \end{array}
$$

where these values are for a temperature of $20^{\circ}$ C and a pressure of 1.000 atm. Estimate the change in the energy of 1.000 mol of $CCl_{4}$ if its temperature is changed from $20.0^{\circ}$ C to $40.0^{\circ}$ C and its pressure from 1.0 atm to 100.0 atm.

EXERCISE 7.2 ▶

The volume of a right circular cylinder is given by

$$
V = \pi r ^ {2} h,
$$

where r is the radius and h the height. Calculate the percentage error in the volume if the radius and the height are measured and a 1% error is made in each measurement in the same direction. Use the formula for the differential, and also direct substitution into the formula for the volume, and compare the two answers.

## 7.2 Change of Variables

In thermodynamics there is usually the possibility of choosing between different sets of independent variables. For example, we can consider the thermodynamic energy U of a one-component, one-phase system to be a function of T, V, and n,

$$
U = U (T, V, n)\tag{7.13}
$$

or a function of $T$ , $P$ , and $n$ ,

$$
U = U (T, P, n).\tag{7.14}
$$

The two choices lead to different expressions for dU,

$$
d U = \left(\frac {\partial U}{\partial T}\right) _ {V, n} d T + \left(\frac {\partial U}{\partial P}\right) _ {T, n} d V + \left(\frac {\partial U}{\partial n}\right) _ {T, V} d n\tag{7.15}
$$

and

$$
d U = \left(\frac {\partial U}{\partial T}\right) _ {P, n} d T + \left(\frac {\partial U}{\partial P}\right) _ {T, n} d P + \left(\frac {\partial U}{\partial n}\right) _ {T, P} d n.\tag{7.16}
$$

There are two different derivatives of U with respect to T: $(\partial U/\partial T)_{V,n}$ and $(\partial U/\partial T)_{P,n}$ . These derivatives have different values for most systems. If we did not use the subscripts, there would be no difference between the symbols for the two derivatives, which could lead to confusion.

EXAMPLE 7.3 Express the function $z = x(x, y) = ax^2 + bxy + cy^2$ in terms of $x$ and $u$ , where $u = xy$ . Find the two partial derivatives $(\partial z / \partial x)_y$ and $(\partial z / \partial x)_u$ .

SOLUTION ▶

$$
\begin{array}{r c l} z & = & z (x, u) = a x ^ {2} + b u + \frac {c u ^ {2}}{x ^ {2}} \\ \left(\frac {\partial z}{\partial x}\right) _ {y} & = & \left(\frac {\partial}{\partial x} \left(a x ^ {2} + b x y + y ^ {2}\right)\right) _ {y} = 2 a x + b y \\ \left(\frac {\partial z}{\partial x}\right) _ {u} & = & 2 a x - \frac {2 c u ^ {2}}{x ^ {2}} = \left(\frac {\partial z}{\partial x}\right) _ {y} - \frac {b u}{x} - \frac {2 c u ^ {2}}{x ^ {3}}. \end{array}
$$

In this example, there was no difficulty in obtaining an expression for the difference between $(\partial z/\partial x)_{y}$ and $(\partial z/\partial x)_{u}$ , because we had the formula to represent the mathematical function. In thermodynamics, it is unusual to have a functional form. More commonly we have measured values for partial derivatives and require a separate means for computing the difference between partial derivatives.

We will obtain a formula of the type

$$
\left(\frac {\partial U}{\partial T}\right) _ {V, n} = \left(\frac {\partial U}{\partial T}\right) _ {P, n} +?,\tag{7.17}
$$

where the question mark indicates an unknown term. The procedure that we use is not mathematically rigorous, but it does give the correct answer. To construct the partial derivative on the left-hand side of our equation, we begin with an expression for the differential dU that contains the derivative on the right-hand side. This is the same as Eq. (7.16). The first thing we do is to “divide” this differential expression by dT, because the derivative we want on the left-hand side is $(\partial U/\partial T)_{V,n}$ . This cannot be done legitimately, because dT is an infinitesimal quantity, but we do it anyway. We get

$$
\frac {d U}{d T} = \left(\frac {\partial U}{\partial T}\right) _ {P, n} \frac {d T}{d T} + \left(\frac {\partial U}{\partial P}\right) _ {T, n} \frac {d P}{d T} + \left(\frac {\partial U}{\partial n}\right) _ {P, T} \frac {d n}{d T}.\tag{7.18}
$$

This equation contains several things that look like ordinary derivatives. However, we must interpret them as partial derivatives, since we have specified that we want to have V and n constant. We change the symbols to the symbols for partial derivatives and add the appropriate subscripts to indicate the variables that are being held fixed. These variables must be the same in all four of the derivatives to keep a valid equation. We want V and n to be constant, so we write

$$
\left(\frac {\partial U}{\partial T}\right) _ {V, n} = \left(\frac {\partial U}{\partial T}\right) _ {P, n} \left(\frac {\partial T}{\partial T}\right) _ {V, n} + \left(\frac {\partial U}{\partial P}\right) _ {T, n} \left(\frac {\partial P}{\partial T}\right) _ {V, n} + \left(\frac {\partial U}{\partial n}\right) _ {P, T} \left(\frac {\partial n}{\partial T}\right) _ {V, n}.\tag{7.19}
$$

The partial derivative of T with respect to T is equal to unity, no matter what is held constant, and the partial derivative of n with respect to anything is zero if n is constant, so

$$
\boxed {\left(\frac {\partial U}{\partial T}\right) _ {V, n} = \left(\frac {\partial U}{\partial T}\right) _ {P, n} + \left(\frac {\partial U}{\partial P}\right) _ {T, n} \left(\frac {\partial P}{\partial T}\right) _ {V, n}}\tag{7.20}
$$