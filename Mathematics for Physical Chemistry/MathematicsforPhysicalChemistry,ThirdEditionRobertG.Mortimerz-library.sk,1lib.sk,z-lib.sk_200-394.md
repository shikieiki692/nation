Equation (7.20) is an example of a set of useful equations. If each symbol is consistently replaced by another symbol, we will have a useful equation for other variables besides the thermodynamic energy. We regard this as our first identity for partial derivatives, which we call the variable-change identity.

EXAMPLE 7.4 Apply the foregoing method to the function in Example 7.2 and find the relation between $(\partial z/\partial x)_{u}$ , and $(\partial z/\partial x)_{y}$ .

## SOLUTION ▶

$$
\left(\frac {\partial z}{\partial x}\right) _ {u} = \left(\frac {\partial z}{\partial x}\right) _ {y} + \left(\frac {\partial z}{\partial y}\right) _ {x} \left(\frac {\partial y}{\partial x}\right) _ {u}
$$

$$
\left(\frac {\partial z}{\partial y}\right) _ {x} = b x + 2 c y = b x + \frac {2 c u}{x}
$$

$$
\left(\frac {\partial y}{\partial x}\right) _ {u} = \left[ \frac {\partial}{\partial x} \left(\frac {u}{x}\right) \right] _ {u} = - \frac {u}{x ^ {2}}
$$

Thus

$$
\left(\frac {\partial z}{\partial x}\right) _ {u} = \left(\frac {\partial z}{\partial x}\right) _ {y} - \frac {b u}{x} - \frac {2 c u}{x ^ {3}}.
$$

This agrees with Example 7.2, as it must.

EXERCISE 7.3 ▶ Complete the following equations.

(a) $\left(\frac{\partial H}{\partial T}\right)_{P,n}=\left(\frac{\partial H}{\partial T}\right)_{V,n}+?$

(c) $\left(\frac{\partial z}{\partial u}\right)_{x,y} = \left(\frac{\partial z}{\partial u}\right)_{x,w} + ?$

(b) $\left(\frac{\partial S}{\partial T}\right)_{U,n} = \left(\frac{\partial S}{\partial T}\right)_{U,V} + ?$

(d) Apply the equation of part c if $z = \cos (x / u) + e^{-y^2 /u^2} + 4y / u$ and $w = y / u$ .

## 7.3 Additional Useful Relations Between Partial Derivatives

It is fairly common in thermodynamics to have measured values for some partial derivative such as $(\partial H/\partial T)_{P,n}$ , which is equal to the heat capacity at constant pressure. However, some other partial derivatives are difficult or impossible to measure. It is convenient to be able to express such partial derivatives in terms of measurable quantities. We now obtain some identities that can be used for this purpose.

The next identity is the reciprocal identity, which states that a derivative is equal to the reciprocal of the derivative with the roles of dependent and independent variables reversed:

$$
\boxed {\left(\frac {\partial y}{\partial x}\right) _ {z, u} = \frac {1}{(\partial x / \partial y) _ {z , u}}}\tag{7.21}
$$

The same variables must be held constant in the two derivatives.

EXAMPLE 7.5 Show that

$$
\left(\frac {\partial P}{\partial V}\right) _ {n, T} = \frac {1}{(\partial V / \partial P) _ {n , T}}
$$

for an ideal gas.

SOLUTION ▶

$$
\begin{array}{r c l} \left(\frac {\partial P}{\partial V}\right) _ {n, T} & = & - \frac {n R T}{V ^ {2}} \\ \frac {1}{(\partial V / \partial P) _ {n , T}} & = & \frac {1}{- n R T / P ^ {2}} = - \frac {P ^ {2}}{n R T} \\ & = & - \frac {(n R T / V) ^ {2}}{n R T} = - \frac {n R T}{V ^ {2}}. \end{array}
$$

EXERCISE 7.4 ▶ Show that the reciprocal identity is satisfied by $(\partial z/\partial x)$ and $(\partial z/\partial z)_{y}$ if

$$
z = \sin \left(\frac {x}{y}\right) \quad \text { and } \quad x = y \sin^ {- 1} (z).
$$


There are two kinds of second partial derivatives. If $z = z(x, y)$ we can differentiate twice with respect to $x$ :

$$
\left(\frac {\partial^ {2} z}{\partial x ^ {2}}\right) = \left[ \frac {\partial}{\partial x} \left(\frac {\partial z}{\partial x}\right) _ {y} \right] _ {y}.\tag{7.22}
$$

In this case, y is held fixed in both differentiations. In addition, there are mixed second partial derivatives, such as the derivative with respect to x and then with respect to y:

$$
\boxed {\frac {\partial^ {2} z}{\partial y \partial x} = \left[ \frac {\partial}{\partial y} \left(\frac {\partial z}{\partial x}\right) _ {y} \right] _ {x}.}\tag{7.23}
$$

Since both variables are shown in the symbol, the subscripts are usually omitted, as in the symbol on the left. However, if there is a third independent variable, it must be held constant and is listed as a subscript:

$$
\left(\frac {\partial^ {2} U}{\partial V \partial T}\right) _ {n} = \left[ \frac {\partial}{\partial V} \left(\frac {\partial U}{\partial T}\right) _ {V, n} \right] _ {T, n}.\tag{7.24}
$$

The Euler reciprocity relation is an identity relating the mixed second partial derivatives. If $z = z(x, y)$ is a differentiable function, then the two different mixed second partial derivatives must equal each other:

$$
\boxed {\frac {\partial^ {2} z}{\partial y \partial x} = \frac {\partial^ {2} z}{\partial x \partial y}.}\tag{7.25}
$$

![[336ad1fd2b018d3bd19d0469402be337aad2110386edc5f7dcccb63b969b7b68.jpg]]

EXAMPLE 7.6 Show that $\left(\partial^2 P / \partial V\partial T\right)_n = \left(\partial^2 P / \partial T\partial V\right)_n$ for an ideal gas.

SOLUTION ▶

$$
\left(\frac {\partial^ {2} P}{\partial V \partial T}\right) _ {n} = \left[ \frac {\partial}{\partial V} \left(\frac {n R}{V}\right) \right] _ {T, n} = - \frac {n R}{V ^ {2}}
$$

$$
\left(\frac {\partial^ {2} P}{\partial T \partial V}\right) _ {n} = \left[ \frac {\partial}{\partial T} \left(\frac {n R T}{V ^ {2}}\right) \right] _ {V, n} = - \frac {n R}{V ^ {2}}.
$$

EXERCISE 7.5 ▶
if

Show by differentiation that $(\partial^2 z / \partial y \partial x) = (\partial^2 z / \partial x \partial y)$

$$
z = e ^ {- x y ^ {2}} \sin (x) \cos (y).
$$

An important set of identities obtained from the Euler reciprocity relation and thermodynamic equations is the set of Maxwell relations. These relations allow you to replace a partial derivative that is difficult or impossible to measure with one that can be measured. One of the Maxwell relations is $^{1}$

$$
\left(\frac {\partial S}{\partial V}\right) _ {T, n} = \left(\frac {\partial P}{\partial T}\right) _ {V, n}
$$

This relation can be used to replace $\left(\frac{\partial S}{\partial V}\right)_{T,n}$ by $\left(\frac{\partial P}{\partial T}\right)_{V,n}$ , which is much more easily measured.

Another useful identity is the cycle rule

$$
\boxed {\left(\frac {\partial y}{\partial x}\right) _ {z} \left(\frac {\partial x}{\partial z}\right) _ {y} \left(\frac {\partial z}{\partial y}\right) _ {x} = - 1.}\tag{7.26}
$$

Many people are at first surprised by this identity, thinking at first that the right-hand side should equal +1 instead of -1. We will “derive” this in the same non-rigorous way as was used to obtain Eq. (7.20). We write the differential of y as a function of x and z:

$$
d y = \left(\frac {\partial y}{\partial x}\right) _ {z} d x + \left(\frac {\partial y}{\partial z}\right) _ {x} d z.\tag{7.27}
$$

This equation delivers the value of dy corresponding to arbitrary infinitesimal changes in x and z, so it is still correct if we choose values of dz and dx such that dy vanishes. We now “divide” nonrigorously by dx, and interpret the “quotients” of differentials as partial derivatives, remembering that y is held fixed by our choice that dy vanishes,

$$
0 = \left(\frac {\partial y}{\partial x}\right) _ {z} \left(\frac {\partial x}{\partial x}\right) _ {y} + \left(\frac {\partial y}{\partial z}\right) _ {x} \left(\frac {\partial z}{\partial x}\right) _ {y}.\tag{7.28}
$$

Since the partial derivative of x with respect to x is equal to unity, this equation becomes identical with Eq. (7.26) when the reciprocal identity is used. Our derivation is indefensible, but the result is correct.

EXAMPLE 7.7 For the particular function $y = z\ln (x)$ show that the cycle rule, Eq. (7.26) is correct.

$$
\begin{array}{r l} \text {SOLUTION} & \triangleright (\partial y / \partial x) _ {z} = z / x, (\partial x / \partial z) _ {y} = e ^ {y / z} (- \frac {y}{z ^ {2}}), (\partial z / \partial y) _ {x} = 1 / \ln (x) \\ & (\partial y / \partial x) _ {z} (\partial x / \partial z) _ {y} (\partial z / \partial y) _ {x} = (z / x) e ^ {y / z} (- \frac {y}{z ^ {2}}) (1 / \ln (x)) = - (\frac {1}{x}) e ^ {y / z} (\frac {y}{z}) (\frac {1}{\ln (x)}) \\ & = - (\frac {1}{x}) e ^ {y / z} = - \frac {x}{x} = - 1 \end{array}
$$

EXERCISE 7.6 ▶ For the particular function y = $x^{2}/z$ , show that Eq. (7.26) is correct.

The final identity that we present in this section is the partial derivative version of the chain rule. If $z = z(u, x, y)$ and if x can be expressed as a function of u, v, and y, then

$$
\boxed {\left(\frac {\partial z}{\partial y}\right) _ {u, v} = \left(\frac {\partial z}{\partial x}\right) _ {u, v} \left(\frac {\partial x}{\partial y}\right) _ {u, v}.}\tag{7.29}
$$

This is very similar to Eq. (4.29). Notice that the same variables must be held fixed in all three derivatives.

EXAMPLE 7.8 Show that if $z = ax^2 + bwx$ and $x = uy$ , then Eq. (7.29) is correct.

## SOLUTION ▶

$$
\begin{array}{r l} \left(\frac {\partial z}{\partial x}\right) _ {u, w} \left(\frac {\partial x}{\partial y}\right) _ {u, w} & = (2 a x + b w) (u) = 2 a u ^ {2} y + b u w \\ \left(\frac {\partial z}{\partial y}\right) _ {u, w} & = \left[ \frac {\partial}{\partial y} \left(a u ^ {2} y ^ {2} + b w u y\right) \right] _ {u, w} = 2 a u ^ {2} y + b u w. \end{array}
$$

The following are commonly measured quantities that are related to partial derivatives:

▶ heat capacity at constant pressure

$$
C _ {P} = \left(\frac {\partial H}{\partial T}\right) _ {P, n} = T \left(\frac {\partial S}{\partial T}\right) _ {P, n}
$$

▶ heat capacity at constant volume

$$
C _ {V} = \left(\frac {\partial U}{\partial T}\right) _ {V, n} = T \left(\frac {\partial S}{\partial T}\right) _ {V, n}
$$

▶ isothermal compressibility

$$
\kappa_ {T} = - \frac {1}{V} \left(\frac {\partial V}{\partial P}\right) _ {T, n}
$$

▶ adiabatic compressibility

$$
\kappa_ {S} = - \frac {1}{V} \left(\frac {\partial V}{\partial P}\right) _ {S, n}
$$

▶ coefficient of thermal expansion

$$
\alpha = \frac {1}{V} \left(\frac {\partial V}{\partial T}\right) _ {P, n}
$$

There are a number of useful relationships among these quantities.

EXAMPLE 7.9 Show that $C_P / C_V = \kappa_T / \kappa_S$ .

SOLUTION ▶

$$
\frac {C _ {P}}{C _ {V}} = \frac {\left(\frac {\partial S}{\partial T}\right) _ {P , n}}{\left(\frac {\partial S}{\partial T}\right) _ {V , n}} = \frac {- \left(\frac {\partial S}{\partial P}\right) _ {T , n} \left(\frac {\partial P}{\partial T}\right) _ {S , n}}{- \left(\frac {\partial S}{\partial V}\right) _ {T , n} \left(\frac {\partial V}{\partial T}\right) _ {S , n}},
$$

where we have used the cycle rule twice. We use the reciprocal identity to write

$$
\frac {C _ {P}}{C _ {V}} = \frac {\left(\frac {\partial S}{\partial P}\right) _ {T , n} \left(\frac {\partial P}{\partial T}\right) _ {S , n}}{\left(\frac {\partial S}{\partial V}\right) _ {T , n} \left(\frac {\partial V}{\partial T}\right) _ {S , n}}.
$$

By the chain rule

$$
\frac {C _ {P}}{C _ {V}} = \frac {\left(\frac {\partial V}{\partial P}\right) _ {T , n}}{\left(\frac {\partial V}{\partial P}\right) _ {S , n}} = \frac {- \frac {1}{V} \left(\frac {\partial V}{\partial P}\right) _ {T , n}}{- \frac {1}{V} \left(\frac {\partial V}{\partial P}\right) _ {S , n}} = \frac {\kappa_ {T}}{\kappa_ {S}}.
$$

## 7.4 Exact and Inexact Differentials

The differential of a function is called an exact differential. There can also be differential forms that are not differentials of any function. A general differential form or pfaffian form can be written

$$
d u = M (x, v) d x + N (x, v) d y.\tag{7.30}
$$

If this is the differential of a function, then M and N must be the appropriate derivatives of that function. Pfaffian forms exist in which M and N are not the appropriate partial derivatives of the same function. In this case du is called an inexact differential. It is an infinitesimal quantity that can be calculated from specified values of dx and dy, but it is not equal to the change in any function of x and y resulting from these changes.

In order to tell whether some differential form is an exact differential or not, we can use the Euler reciprocity relation. If there exists a function $u = u(x, y)$ such that

$$
M (x, y) = \left(\frac {\partial u}{\partial x}\right) _ {y} \quad \text { and } \quad N (x, y) = \left(\frac {\partial u}{\partial y}\right) _ {x},
$$

then from the Euler reciprocity relation,

$$
\frac {\partial^ {2} u}{\partial x \partial y} = \frac {\partial^ {2} u}{\partial y \partial x},
$$

which means that if the differential is exact

$$
\left(\frac {\partial N}{\partial x}\right) _ {y} = \left(\frac {\partial M}{\partial y}\right) _ {x} \quad (\text { exact   differential }),\tag{7.31}
$$

Equation (7.31) represents a necessary and sufficient condition for the differential of Eq. (7.30) to be exact. That is, if the differential is exact, Eq. (7.31) will be obeyed, and if Eq. (7.31) is obeyed, the differential is exact.

EXAMPLE 7.10 Show that the differential

$$
d u = \left(2 x y + \frac {9 x ^ {2}}{y}\right) d x + \left(x ^ {2} - \frac {3 x ^ {2}}{y ^ {2}}\right) d y
$$

is exact.

SOLUTION ▶

$$
\left[ \frac {\partial}{\partial y} \left(2 x y + \frac {9 x ^ {2}}{y}\right) \right] _ {x} = 2 x - \frac {9 x ^ {2}}{y ^ {2}}
$$

$$
\left[ \frac {\partial}{\partial x} \left(x ^ {2} - \frac {3 x ^ {3}}{y ^ {2}}\right) \right] _ {x} = 2 x - \frac {9 x ^ {2}}{y ^ {2}}.
$$

EXERCISE 7.7 ▶ Determine whether each of the following is an exact differential.

$$
\mathrm{(a)} d u = (2 a x + b y ^ {2}) d x + (b x y) d y. \mathrm{(b)} d u = (x + y) d x + (x + y) d y
$$

$$
\mathrm{(c)} d u = (x ^ {2} + 2 x + 1) d x + (y ^ {2} + 25 y + 24) d y.
$$

Differential forms with three or more terms can also either be exact or inexact. The Euler reciprocity relation provides a test for such differentials. For example, if

$$
d u = M (x, v, z) d x + N (x, y, z) d y + P (x, y, z) d z,\tag{7.32}
$$

then in order for this to be an exact differential, the three equations must be obeyed:

$$
\left(\frac {\partial M}{\partial y}\right) _ {x, z} = \left(\frac {\partial N}{\partial x}\right) _ {y, z}\tag{7.33}
$$

$$
\left(\frac {\partial N}{\partial z}\right) _ {x, y} = \left(\frac {\partial P}{\partial y}\right) _ {x, z}\tag{7.34}
$$

$$
\left(\frac {\partial M}{\partial z}\right) _ {x, y} = \left(\frac {\partial P}{\partial x}\right) _ {y, z}\tag{7.35}
$$

EXERCISE 7.8 ▶ Show that the following is not an exact differential du = (2y) dx + (x) dy + cos(z) dz.

There are two important inexact differentials in thermodynamics. If a system undergoes an infinitesimal process (one in which the independent variables specifying the state of the system change infinitesimally), dq denotes the amount of heat transferred to the system and dw denotes the amount of work done on the system. Both of these quantities are inexact differentials. For a fluid system undergoing a reversible process,

$$
d w _ {r e v} = - P d V,\tag{7.36}
$$

where P is the pressure of the system and V is its volume.

EXAMPLE 7.11 Show that for an ideal gas undergoing a reversible process with n fixed, $dw_{rev}$ is inexact.

SOLUTION ▶ We choose T and V as our independent variables and write the differential form

$$
d w = M d T + N d V \quad (n \text {   fixed }).\tag{7.37}
$$

Comparison with Eq. (7.36) shows that M = 0 and $N = P = -nRT/V$ . We apply the test for exactness, Eq. (7.31),

$$
\begin{array}{l} \left(\frac {\partial M}{\partial V}\right) _ {T, n} = 0 \\ \left(\frac {\partial N}{\partial T}\right) _ {V, n} = \left[ \frac {\partial}{\partial T} \left(- \frac {n R T}{V}\right) \right] _ {V, n} = - \frac {n R}{V} \neq 0. \end{array}
$$

EXERCISE 7.9 ▶ The thermodynamic energy of a monatomic ideal gas is given approximately by

$$
U = \frac {3 n R T}{2}.\tag{7.38}
$$

Find the partial derivatives and write the expression for dU using T, V, and n as independent variables. Show that the partial derivatives obey the Euler reciprocity relations in Eqs. (7.33–7.35).

In thermodynamics, quantities such as the thermodynamic energy, the volume, the pressure, the temperature, the amount of substances, and so forth, are functions of the variables that can be used to specify the state of the system. They are called state functions. The differentials of these quantities are exact differentials. Work and heat are not state functions. There is no such thing as an amount of work or an amount of heat in a system. We have already seen in Example 7.11 that $dw_{rev}$ is not an exact differential, and the same is true of dw for an irreversible process. An infinitesimal amount of heat is also not an exact differential. However, the first law of thermodynamics states that dU, which equals $dq + dw$ , is an exact differential.

## Integrating Factors

Some inexact differentials become exact differential if the inexact differential is multiplied by a function called an integrating factor for that differential.

EXAMPLE 7.12 Show that the differential

$$
d u = (2 a x ^ {2} + b x y) d x + (b x ^ {2} + 2 c x y) d y
$$

is inexact, but that 1/x is an integrating factor, so that du/x is exact.

SOLUTION ▶

$$
\left[ \frac {\partial}{\partial y} (2 a x ^ {2} + b x y) \right] _ {x} = b x
$$

$$
\left[ \frac {\partial}{\partial x} (b x ^ {2} + 2 c x y) \right] _ {y} = 2 b x + 2 c y \neq b x
$$

so du is inexact. After we divide by x we obtain the partial derivatives

$$
\left[ \frac {\partial}{\partial y} (2 a x + b y) \right] _ {x} = b
$$

$$
\left[ \frac {\partial}{\partial x} (b x + 2 c y) \right] _ {y} = b
$$

so $(1 / x)du$ is exact.

EXERCISE 7.10 ▶

Show that the differential

$$
(1 + x) d x + \left[ \frac {x \ln x}{y} + \frac {x ^ {2}}{y} \right] d y
$$

is inexact, and that y/x is an integrating factor.


There is no general method for finding an integrating factor, although we will discuss a method that will work for a particular class of differential forms in Chapter 8. However, it is true that if a differential possesses one integrating factor, there are infinitely many integrating factors for that differential.

## Line Integrals

In Chapter 5, we found that a finite increment in a function could be constructed by a definite integration. If $x_{1}$ and $x_{0}$ are values of the single independent variable $x$ , we can write

$$
F \left(x _ {1}\right) - F \left(x _ {0}\right) = \int_ {x _ {0}} ^ {x _ {1}} f (x) d x = \int_ {x _ {0}} ^ {x _ {1}} d F,\tag{7.39}
$$

where

$$
f (x) = \frac {d F}{d x}.\tag{7.40}
$$

We can think of the integral of Eq. (7.39) as being a sum of infinitesimal increments equal to $f(x) \, dx$ and can think of moving along the x axis from $x_{0}$ to $x_{1}$ as we add up these increments.

![[2b6bd0c369d3e088a3acbb1a98f5a301f6737f303ba33e8c258022e48035aea4.jpg]]  
Figure 7.3 ▶ Diagram illustrating the line integral of an exact differential.

We now consider the analogous process for a differential with two or more independent variables. For two independent variables, $x$ and $y$ , we might try to define

$$
\int_ {x _ {0}, y _ {0}} ^ {x _ {1}, y _ {1}} d F = \int_ {x _ {0}, y _ {0}} ^ {x _ {1}, y _ {1}} [ M (x, y) d x + N (x, y) d y ].\tag{7.41}
$$

However, this integral is not yet well defined. With a single integration variable, there is only one way to integrate along its axis. With a pair of integration variables the situation is different. This is shown schematically in Fig. 7.3. The pair of values $(x_{0}, y_{0})$ represents one point in the x-y plane, and $(x_{1}, y_{1})$ represents another point in the plane. Many different paths in the plane can join the two points. In order to complete the definition of the integral in Eq. (7.41), we must specify the path in the x-y plane along which we integrate (add up the increments) from the point $(x_{0}, y_{0})$ to the point $(x_{1}, y_{1})$ . We introduce the notation

$$
\int_ {C} d F = \int_ {C} \left[ M (x, y) d x + N (x, y) d y \right],\tag{7.42}
$$

where the letter $C$ stands for the curve joining the two points. The integral is called a line integral or a path integral.

We can think of Eq. (7.42) as representing a sum of many infinitesimal contributions, each one given by the appropriate infinitesimal value of dF resulting when x is changed by dx and y is changed by dy. However, these changes dx and dy are not independent. They must be related so that we remain on the chosen curve during the integration process. A curve in the x-y plane specifies y as a function of x or x as a function of y. For a given curve, we can write

$$
y = y (x)\tag{7.43}
$$

$$
x = x (y)\tag{7.44}
$$

In order to calculate a line integral such as that of Eq. (7.42), we replace y in $M(x, y)$ by the function of x given in Eq. (7.43), and we replace x in $N(x, y)$ by the function of y given in Eq. (7.44). With this replacement, M is a function of x only, and N is a function of y only, and each term becomes an ordinary one-variable integral:

$$
\int_ {C} d F = \int_ {x _ {0}} ^ {x _ {1}} M [ x, y (x) ] d x + \int_ {y _ {0}} ^ {y _ {1}} N [ y, x (y) ] d y.\tag{7.45}
$$

In these integrals, specification of the curve C determines not only what the beginning point $(x_{0}, y_{0})$ and the final point $(x_{1}, y_{1})$ are, but also what the functions are that replace y in the dx integral and x in the dy integral.

EXAMPLE 7.13 Find the value of the line integral

$$
\int_ {C} d F = \int_ {C} \left[ (2 x + 3 y) d x + (3 x + 4 y) \right] d y,
$$

where c is the straight-line segment given by $y = 2x + 3$ from (0, 3) to (2, 7).

SOLUTION ▶ In the first term, y must be replaced by $2x + 3$ , and in the second term x must be replaced by $(1/2)(y - 3)$ ,

$$
\begin{array}{r l} \int_ {C} d F & = \int_ {0} ^ {2} [ 2 x + 3 (2 x + 3) ] d x + \int_ {3} ^ {7} \left[ \frac {3}{2} (y - 3) + 4 y \right] d y \\ & = \left. \left(\frac {8 x ^ {2}}{2} + 9 x\right) \right| _ {0} ^ {2} + \left. \left(\frac {(11 / 2) y ^ {2}}{2} - \frac {9}{2} y\right) \right| _ {3} ^ {7} = 126. \end{array}
$$

EXERCISE 7.11 ▶
exact.

Show that the differential in the preceding example is

## Line Integrals of Exact Differentials

There is an important theorem, which we now state without proof:

Theorem 1 If dF is an exact differential, then the line integral $\int_{C} dF$ depends only on the initial and final points and not on the choice of curve joining these points. Further, the line integral equals the value of the function F at the final point minus the value of the function at the beginning point. We say that the line integral of an exact differential is path-independent.

For example, if $(x_{0}, y_{0})$ is the initial point of the line integration and $(x_{1}, y_{1})$ is the final point of the line integration, then

$$
\begin{array}{r l} \int_ {C} d F & = \int_ {C} \left[ \left(\frac {\partial F}{\partial x}\right) d x + \left(\frac {\partial F}{\partial y}\right) d y \right] \\ & = F (x _ {1}, y _ {1}) - F (x _ {0}, y _ {0}) \quad (d F \text {exact}) \end{array}\tag{7.46}
$$

We have written M and N as the partial derivatives which they must be equal to in order for dF to be exact (see Section 7.4). If du is not an exact differential, there is no such things as a function u, and the line integral will depend not only on the beginning and ending points, but also on the curve of integration joining these points.

EXAMPLE 7.14 Show that the line integral of Example 7.12 has the same value as the line integral of the same differential on the rectangular path from (0, 3) to (2, 3) and then to (2, 7).

SOLUTION ▶ The path of this integration is not a single curve but two line segments, so we must carry out the integration separately for each segment. This is actually a simplification, because on the first line segment, y is constant, so dy = 0 and the dy integral vanishes. On the second line segment, x is constant, so dx = 0 and the dx integral vanishes. Therefore,

$$
\int_ {C} d F = \int_ {0} ^ {2} (2 x + 9) d x + \int_ {3} ^ {7} (6 + 4 y) d y.
$$

This follows from the fact that $y = 3$ on the first line segment, and from the fact that $x = 2$ on the second line segment. Performing the integration yields

$$
\int_ {C} d F = \left. \left(\frac {2 x ^ {2}}{2} + 9 x\right) \right| _ {0} ^ {2} + \left. \left(6 y + \frac {4 y ^ {2}}{2}\right) \right| _ {3} ^ {7} = 126.
$$

EXERCISE 7.12 ▶

(a) (a) Show that the following differential is exact:

$$
d z = (y e ^ {x y}) d x + (x e ^ {e y}) d y
$$

(b) Calculate the line integral $\int_{c} dz$ on the line segment from (0, 0) to (2, 2). On this line segment, $y = x$ and $x = y$ .

(c) Calculate the line integral $\int_{c} dz$ on the path going from (0,0) to (0,2) and then to (2,2) (a rectangular path).

![[b73312cde8448f6dc4ff693f857beb0d2e489e90d00338b006e8332794d5b3ef.jpg]]

## Line Integrals of Inexact Differentials

If a differential is not exact, two line integrals beginning and ending at the same points will not necessarily yield the same result.

## EXAMPLE 7.15 Show that the differential

$$
d u = d x + x d y
$$

is inexact and carry out the line integral from $(0,0)$ to $(2,2)$ by two different paths: path 1, the straight-line segment from $(0,0)$ to $(2,2)$ ; and path 2, the rectangular path from $(0,0)$ to $(2,0)$ and then to $(2,2)$ .

SOLUTION ▶ Test for exactness:

$$
\left[ \frac {\partial}{\partial y} (1) \right] _ {x} = 0
$$

$$
\left[ \frac {\partial}{\partial x} (x) \right] _ {y} = 1 \neq 0.
$$

The differential is not exact.

Path 1:

$$
\int_ {C _ {1}} d u = \int_ {C _ {1}} d x + \int_ {C _ {1}} x d y = \int_ {0} ^ {2} d x + \int_ {0} ^ {2} y d y,
$$

where we obtained the second integral by using the fact that $y = x$ on the straight-line segment of path 1,

$$
\int_ {C _ {1}} d u = x \left| _ {0} ^ {2} + \frac {y ^ {2}}{2} \right| _ {0} ^ {2} = 4.
$$

Path 2,

$$
\begin{array}{r c l} \int_ {C _ {2}} d u & = & \int_ {C _ {2}} d x + \int_ {C _ {2}} x d y = \int_ {0} ^ {2} d x + \int_ {0} ^ {2} 2 d y \\ & = & x | _ {0} ^ {2} + 2 y | _ {0} ^ {2} = 2 + 4 = 6. \end{array}
$$

The two line integrals have the same beginning point and the same ending point, but are not equal, because the differential is not an exact differential.

EXERCISE 7.13 ▶

(a) Carry out the two line integrals of du from Example 7.15 from (0, 0) to $(x_{1}, y_{1})$ .

(b) Integrate on the rectangular path from $(0,0)$ to $(0,y_{1})$ and then to $(x_{1},y_{1})$ .

(c) Integrate on the rectangular path from $(0,0)$ to $(x_{1},0)$ and then to $(x_{1},y_{1})$ .


## Line Integrals with Three Integration Variables

There are also line integrals of functions of three independent variables. The line integral of the differential du is

$$
\int_ {C} d u = \int_ {C} [ M (x, y, z) d x + N (x, y, z) d y + P (x, y, z) d z ],\tag{7.47}
$$

where C specifies a curve that gives y and z as functions of x, or x and y as functions of z, or x and z as functions of y. If the beginning point of the curve C is $(x_{0}, y_{0}, z_{0})$ and the ending point is $(x_{1}, y_{1}, z_{1})$ , the line integral is

$$
\begin{array}{r l} \int_ {C} d u & = \int_ {x _ {0}} ^ {x _ {1}} M [ x, y (x), z (x) ] d x + \int_ {y _ {0}} ^ {y _ {1}} N [ x (y), y, z (y) ] d y \\ & + \int_ {z _ {0}} ^ {z _ {1}} P [ x (z), y (z), z ] d z. \end{array}\tag{7.48}
$$

If du is an exact differential, then u is a function, and

$$
\boxed {\int_ {C} d u = u \left(x _ {1}, y _ {1}, z _ {1}\right) - u \left(x _ {0}, y _ {0}, z _ {0}\right) \quad (\text {if} d u \text {is an exact differential})}\tag{7.49}
$$

## Line integrals in Thermodynamics

In thermodynamics, the equilibrium state of a system is represented by a point in a space whose axes represent the variables specifying the state of the system. A line integral in such a space represents a reversible process. A cyclic process is one that begins and ends at the same state of a system. A line integral that begins and ends at the same point is denoted by the symbol $\oint du$ . Since the beginning and final points are the same, such an integral must vanish if du is an exact differential:

$$
\boxed {\oint d u = 0 \quad (\text {   if   } d u \text {   is   exact   })}.\tag{7.50}
$$

If du is inexact, a line integral that begins and ends at the same point will not generally be equal to zero.

EXERCISE 7.14 ▶ Carry out the cyclic line integral of $dw_{rev}$ for 1.000 mol of an ideal gas, using the following reversible cycle: Starting with T = 500.0 K and V = 20.0 l, the system is expanded at constant temperature to a volume of 40.0 l. The system is cooled at constant volume to 300.0 K. The system is then compressed to a volume of 20.0 l at a constant temperature of 300.0 K. It is finally heated at constant volume to 600.0 K.

## 7.6 Multiple Integrals

While a line integral can be thought of as adding up infinitesimal contributions represented as a differential form, a multiple integral can be thought of as adding up contributions given by an integrand function times an infinitesimal element of area or of volume, etc. A double integral is the simplest kind of multiple integral. It is written in the form

$$
I = \int_ {a _ {1}} ^ {a _ {2}} \int_ {b _ {1}} ^ {b _ {2}} f (x, y) d y d x,\tag{7.51}
$$

where $f(x, y)$ is the integrand function, $a_{1}$ and $a_{2}$ are the limits of the x integration, and $b_{1}$ and $b_{2}$ are the limits of the y integration. You should think of the product dy dx as an infinitesimal element of area in the x-y plane.

The double integral is carried out as follows: The “inside” integration is done first. This is the integration over the values of the variable whose differential and limits are written closest to the integrand function. During this integration, the other independent variable is treated as a constant if it occurs in the integrand. The result of the first integration is the integrand for the remaining integration. The limits $b_{1}$ and $b_{2}$ can depend on x, but the limits $a_{1}$ and $a_{2}$ must be constants.

EXAMPLE 7.16 Evaluate the double integral

$$
I = \int_ {0} ^ {a} \int_ {0} ^ {b} (x ^ {2} + 4 x y) d y d x.
$$

SOLUTION ▶ The integration over y is carried out, treating x as a constant:

$$
\int_ {0} ^ {b} \left(x ^ {2} + 4 x y\right) d y = \left. \left(x ^ {2} y + \frac {4 x y ^ {2}}{2}\right) \right| _ {0} ^ {b} = b x ^ {2} + 2 b ^ {2} x.
$$

This becomes the integrand for the second integration, so that

$$
\begin{array}{r l} I & = \int_ {0} ^ {a} \left(b x ^ {2} + 2 b ^ {2} x\right) d x = \left(\frac {b x ^ {3}}{3} + \frac {2 b ^ {2} x ^ {2}}{2}\right) \Bigg | _ {0} ^ {a} \\ & = \frac {b a ^ {3}}{3} + b ^ {2} a ^ {2}. \end{array}
$$

EXAMPLE 7.17 Evaluate the double integral

$$
\int_ {0} ^ {a} \int_ {0} ^ {3 x} (x ^ {2} + 2 x y + y ^ {2}) d y d x.
$$

SOLUTION ▶ The result of the inside integration is

$$
\begin{array}{r l} \int_ {0} ^ {3 x} \left(x ^ {2} + 2 x y + y ^ {2}\right) d y & = \left. \left(x ^ {2} y + \frac {2 x y ^ {2}}{2} + \frac {y ^ {3}}{3}\right) \right| _ {0} ^ {3 x} \\ & = 3 x ^ {3} + 9 x ^ {3} + 9 x ^ {3} = 21 x ^ {3}. \end{array}
$$

The $x$ integration gives

$$
\int_ {0} ^ {a} 21 x ^ {3} d x = \left. \frac {21 x ^ {4}}{4} \right| _ {0} ^ {a} = \frac {21 a ^ {4}}{4}.
$$

EXERCISE 7.15 ▶

Evaluate the double integral

$$
\int_ {2} ^ {4} \int_ {0} ^ {\pi} x \sin (y) d y d x.
$$

## The Double Integral Represented as a Volume

In Section 5.2 we saw that a definite integral with one independent variable is equal to an area in a graph of the integrand function between the axis and the integrand curve. A double integral is equal to a volume in an analogous way. This is illustrated in Fig. 7.4, which is drawn to correspond to Example 7.18. In the x-y plane, we have an infinitesimal element of area dx dy, drawn in the figure as though it were finite in size. The vertical distance from the x-y plane to the surface representing the integrand function f is the value of the integrand function, so that the volume of the small box lying between the element of area and the surface is equal to $f(x) \, dx \, dy$ .

![[7546272887395d6bca8c4869d215d0c020a6c45361cda643f4cf8e1d52cc996f.jpg]]  
Figure 7.4 ▶ The diagram for Example 7.18.

The double integral is the sum of the volume of all such infinitesimal boxes, and thus equals the volume of the solid bounded by the x-y plane, the surface representing the integrand function, and surfaces representing the limits of integration. If the integrand function is negative in part of the region of integration, we must take the volume above the x-y plane minus the volume below the plane as equal to the integral.

EXAMPLE 7.18 Calculate the volume of the solid shown in Fig. 7.4. The bottom of the solid is the x-y plane. The flat surface corresponds to y = 0, the curved vertical surface corresponds to $y = x^{2} - 4$ , and the top of the solid corresponds to f = 2 - y.

SOLUTION ▶ We carry out a double integral with f = 2 - y as the integrand:

$$
V = \int_ {- 2} ^ {2} \int_ {x ^ {2} - 4} ^ {0} (2 - y) d y d x.
$$

The inside integral is

$$
\int_ {x ^ {2} - 4} ^ {0} (2 - y) d y = \left. \left(2 y - \frac {y ^ {2}}{2}\right) \right| _ {x ^ {2} - 4} ^ {0} = \frac {x ^ {4}}{2} - 6 x ^ {2} + 16
$$

so that

$$
V = \int_ {- 2} ^ {2} \left(\frac {x ^ {4}}{2} - 6 x ^ {2} + 16\right) d x = \left. \left(\frac {x ^ {5}}{10} - 2 x ^ {3} + 16 x\right) \right| _ {- 2} ^ {2} = 38.4.
$$

![[f0285e27b83e0a4688ca407903fe508458b881d34496e393e8e58ff3233a2b47.jpg]]  
Figure 7.5 ▶ The diagram for Exercise 7.16.

EXERCISE 7.16 ▶ Find the volume of the solid object shown in Fig. 7.5. The top of the object corresponds to f = 5 - x - y, the bottom of the object is the x-y plane, the trapezoidal face is the x-f plane, and the large triangular face is the y-f plane. The small triangular face corresponds to x = 3.

## Multiple Integrals in Quantum Mechanics

In quantum mechanics, the square of a wave function is the probability density for finding a particle or particles. Since ordinary space has three dimensions, multiple integrals with three independent variables (triple integrals) represent probabilities of finding a particle in the region of integration.. For example, if the integrand function f depends on x, y, and z, we could have the triple integral

$$
I = \int_ {a _ {1}} ^ {a _ {2}} \int_ {b _ {1}} ^ {b _ {2}} \int_ {c _ {1}} ^ {c _ {2}} f (x, y, z) d z d y d x.\tag{7.52}
$$

To evaluate the integral, we first integrate z from $c_{1}$ to $c_{2}$ and take the result as the integrand for the double integral over y and x. Then we integrate y from $b_{1}$ to $b_{2}$ , and take the result as the integrand for the integral over x from $a_{1}$ to $a_{2}$ . The limits $c_{1}$ and $c_{2}$ can depend on y and x, and the limits $b_{1}$ and $b_{2}$ can depend on x, but $a_{1}$ and $a_{2}$ must be constants. If the limits are all constants, and if the integrand function can be factored, the entire integral can be factored, as in the following example.

EXAMPLE 7.19 Find the triple integral

$$
I = A ^ {2} \int_ {0} ^ {a} \int_ {0} ^ {b} \int_ {0} ^ {c} \sin^ {2} \left(\frac {n \pi x}{a}\right) \sin^ {2} \left(\frac {m \pi y}{b}\right) \sin^ {2} \left(\frac {k \pi z}{c}\right) d z d y d x.
$$

This is a normalization integral from quantum mechanics, equal to the total probability for finding a particle in a three-dimensional box. The integrand is the square of the wave function for one of the states of a particle in a three-dimensional box. The quantities m, n, and k are integral quantum numbers specifying the state of the particle. The integral is equal to the total probability of finding a particle in the box. It is customary to choose the value of the constant A so that the total probability equals unity, in which case the wave function is said to be normalized.

SOLUTION ▶ The integrand function is a product of three factors, each of which depends on only one variable, and the limits of integration are constants. The entire integral can therefore be written in factored form:

$$
I = A ^ {2} \left[ \int_ {0} ^ {a} \sin^ {2} \left(\frac {n \pi x}{a}\right) d x \right] \left[ \int_ {0} ^ {b} \sin^ {2} \left(\frac {m \pi y}{b}\right) d y \right] \left[ \int_ {0} ^ {c} \sin^ {2} \left(\frac {k \pi z}{c}\right) d z \right].
$$

We first carry out the z integration, using the substitution $u = k\pi z/c$ ,

$$
\int_ {0} ^ {c} \sin^ {2} \left(\frac {k \pi z}{c}\right) d z = \frac {c}{k \pi} \int_ {0} ^ {k \pi} \sin^ {2} (u) d u.
$$

The integrand is a periodic function with period $\pi$ , so that the integral from 0 to $k\pi$ is just $k$ times the integral from 0 to $\pi$ , which is given as Eq. (8) of Appendix F:

$$
\int_ {0} ^ {c} \sin^ {2} \left(\frac {k \pi z}{c}\right) d z = \frac {c}{k \pi} k \frac {\pi}{2} = \frac {c}{2}.
$$

The other integrals are similar, except for having $a$ or $b$ instead of $c$ , so that

$$
I = A ^ {2} \frac {a b c}{8}.
$$

Many triple integrals in quantum mechanics are factored in the same way as in this example.

EXERCISE 7.17 ▶ Find the value of the constant A so that the following integral equals unity.

$$
A \int_ {- \infty} ^ {\infty} \int_ {- \infty} ^ {\infty} e ^ {- x ^ {2} - y ^ {2}} d y d x.
$$


## Changing Variables in Multiple Integrals

Sometimes it is convenient to take a multiple integral over an area or over a volume using polar coordinates or spherical polar coordinates, and so on, instead of Cartesian coordinates. Figure 7.6 shows how this is done in polar coordinates. We require an infinitesimal element of area given in terms of the coordinates $\rho$ and $\phi$ . One dimension of the element of area is $d\rho$ and the other dimension is $\rho d\phi$ , from the fact that an arc length is the radius of the circle times the angle subtended by the arc, measured in radians. The element of area is $\rho d\phi d\rho$ . If the element of area were finite, it would not quite be rectangular, and this formula would not be exact, but it is valid for an infinitesimal element of area.

![[5b0f5b28037fbd727573f7d60d89a0d5f9beffcc9ef268b964d6da30d4edef7e.jpg]]  
Figure 7.6 ▶ An infinitesimal element of area in plane polar coordinates.

We can think of the plane as being covered completely by infinitely many such elements of area, and a double integral over some region of the plane is just the sum of the value of the integrand function at each element of area in the region times the area of the element.

EXAMPLE 7.20 In Cartesian coordinates, the wave function for the ground state of a two dimensional harmonic oscillator is

$$
\psi = B \exp \left[ - a (x ^ {2} + y ^ {2}) \right].
$$

Transform this to plane polar coordinates and find the value of B such that the integral of $\psi^{2}$ over the entire x-y plane is equal to unity.

## SOLUTION ▶

$$
\psi = B e ^ {- a \rho^ {2}}.
$$

The integral that is to equal unity is

$$
B ^ {2} \int_ {0} ^ {\infty} \int_ {0} ^ {2 \pi} e ^ {- 2 a \rho^ {2}} \rho d \phi d \rho .
$$

The integral can be factored,

$$
I = B ^ {2} \int_ {0} ^ {\infty} e ^ {- 2 a \rho^ {2}} \rho d \rho \int_ {0} ^ {2 \pi} d \phi = 2 \pi B ^ {2} \int_ {0} ^ {\infty} e ^ {- 2 a \rho^ {2}} \rho d \rho .
$$

The $\rho$ integral is done by the method of substitution, letting $u = 2a\rho^2$ and $du = 4a\rho d\rho$ . We obtain

$$
I = 2 \pi B ^ {2} \left(\frac {1}{4 a}\right) \int_ {0} ^ {\infty} e ^ {- u} d u = \frac {B ^ {2} \pi}{2 a}
$$

$$
B = \sqrt {\frac {2 a}{\pi}}.
$$

EXERCISE 7.18 ▶ Use a double integral to find the volume of a cone of height h and radius a at the base. If the cone is standing with its point upward and with its base centered at the origin, the equation giving the surface of the cone is

$$
f = h \left(1 - \frac {\rho}{a}\right).
$$


In transforming from Cartesian to plane polar coordinates, the factor $\rho$ , which is used with the product of the differentials $d\phi \, d\rho$ is called a Jacobian. The symbol $\partial(x, y)/\partial(\rho, \phi)$ is used for this Jacobian:

$$
\iint f (x, y) d x d y = \iint f (\rho , \phi) d \phi d \rho = \iint f (\rho , \phi) \frac {\partial (x , y)}{\partial (\rho , \phi)} d \rho d \phi .\tag{7.53}
$$

We will not discuss the mathematical theory, but this Jacobian is given by the following determinant (determinants are discussed in Chapter 9):

$$
\frac {\partial (x , y)}{\partial (\rho , \phi)} = \left| \begin{array}{l l} \partial x / \partial \rho & \partial x / \partial \phi \\ \partial y / \partial \rho & \partial y / \partial \phi \end{array} \right|.\tag{7.54}
$$

Equation (9.59) gives the formula for a 2 by 2 determinant:

$$
\left| \begin{array}{c c} \partial x / \partial \rho & \partial x / \partial \phi \\ \partial y / \partial \rho & \partial y / \partial \phi \end{array} \right| = \left| \begin{array}{c c} \cos (\phi) & - \rho \sin (\phi) \\ \cos (\phi) & \rho \cos (\phi) \end{array} \right| = \rho \cos^ {2} (\phi) + \rho \sin^ {2} (\phi) = \rho .\tag{7.55}
$$

where we have also used Eq. (7) of Appendix B. This equation gives us the same result as we had before,

$$
d A = \text { element   of   area } = \rho d \phi d \rho .\tag{7.56}
$$

The Jacobian for transformation of coordinates in three dimensions is quite similar. If u, v, and w are some set of coordinates such that

$$
\begin{array}{l} x = x (u, v, w) \\ y = y (u, v, w) \\ z = z (u, v, w), \end{array}
$$

then the Jacobian for the transformation of a multiple integral from Cartesian coordinates to the coordinates u, v, and w is given by the determinant

$$
\boxed {\frac {\partial (x , y , z)}{\partial (u , v , w)} = \left| \begin{array}{c c c} \partial x / \partial u & \partial x / \partial v & \partial x / \partial w \\ \partial y / \partial u & \partial y / \partial v & \partial y / \partial w \\ \partial z / \partial u & \partial z / \partial v & \partial z / \partial w \end{array} \right|.}\tag{7.57}
$$

The rule for expanding a 3 by 3 determinant is discussed in Chapter 9.

EXAMPLE 7.21 Obtain the Jacobian for the transformation from Cartesian coordinates to spherical polar coordinates.

SOLUTION ▶ The equations relating the coordinates are Eqs. (2.62)–(2.64):

$$
\frac {\partial (x , y , z)}{\partial (r , \theta , \phi)} = \left| \begin{array}{c c c} \sin (\theta) \cos (\theta) & r \cos (\theta) \cos (\phi) & - r \sin (\theta) \sin (\phi) \\ \sin (\theta) \sin (\phi) & r \cos (\theta) \sin (\phi) & r \sin (\theta) \cos (\phi) \\ \cos (\phi) & - r \sin (\theta) & 0 \end{array} \right|
$$

From the expansion of a 3 by 3 determinant illustrated in Example 9.12,

$$
\begin{array}{r c l} \frac {\partial (x , y , z)}{\partial (r , \theta , \phi)} & = & \cos (\theta) \left[ r ^ {2} \cos (\theta) \sin (\theta) \cos^ {2} (\phi) + r ^ {2} \sin (\theta) \cos (\theta) \sin^ {2} (\theta) \right] \\ & & + r \sin (\theta) \left[ r \sin^ {2} (\theta) \cos^ {2} (\phi) + r ^ {2} \sin^ {2} (\theta) \sin^ {2} (\phi) \right] \\ & = & r ^ {2} \sin (\theta) \cos^ {2} (\theta) + r ^ {2} \sin^ {3} (\theta) = r ^ {2} \sin (\theta), \end{array}\tag{7.58}
$$

(7.59)

where we have used Eq. (7) of Appendix B several times.

EXERCISE 7.19 ▶ Find the Jacobian for the transformation from Cartesian to cylindrical polar coordinates.

A triple integral in Cartesian coordinates is transformed into a triple integral in spherical polar coordinates by

$$
\iiint (x, y, z) d x d y d z = \iiint f (r, \theta , \phi) r ^ {2} \sin (\theta) d \phi d \theta d r.\tag{7.60}
$$

An element of volume is given by

$$
\boxed {d V = d x d y d z = r ^ {2} \sin (\theta) d \phi d \theta d r}
$$

To complete the transformation, the limits on r, $\theta$ , and $\phi$ must be found so that they correspond to the limits on x, y, and z. Sometimes the purpose of transforming to spherical polar coordinates is to avoid the task of finding the limits in Cartesian coordinates when they can be expressed easily in spherical polar coordinates. For example, if the integration is over the interior of a sphere of radius a centered at the origin, $\phi$ ranges from 0 to $2\pi$ , $\theta$ ranges from 0 to $\pi$ , and r ranges from 0 to a. If all of space is to be integrated over, $\phi$ ranges from 0 to $2\pi$ , $\theta$ ranges from 0 to $\pi$ , and r ranges from 0 to $\infty$ .

## 7.7 Vector Derivative Operators

An operator is a symbol for carrying out a mathematical operation (see Chapter 9). There are several vector derivative operators. We first define them in Cartesian coordinates.

## Vector Derivatives in Cartesian Coordinates

The gradient operator is defined in Cartesian coordinates by

$$
\nabla = \mathbf {i} \frac {\partial}{\partial x} + \mathbf {j} \frac {\partial}{\partial y} + \mathbf {k} \frac {\partial}{\partial z}\tag{7.61}
$$

where i, j, and k are the unit vectors in the directions of the x, y, and z axes defined in Chapter 2. The gradient of a scalar function is a vector. The symbol $\nabla$ , which is an upside-down capital Greek delta, is called “del.” If f is some scalar function of x, y, and z, the gradient of f is given in Cartesian coordinates by

$$
\nabla f = \mathbf {i} \frac {\partial f}{\partial x} + \mathbf {j} \frac {\partial f}{\partial y} + \mathbf {k} \frac {\partial f}{\partial z}.\tag{7.62}
$$

The gradient of f is sometimes denoted by grad f instead of $\nabla f$ . The direction of the gradient of a scalar function is the direction in which the function is increasing most rapidly, and its magnitude is the rate of change of the function in that direction.

EXAMPLE 7.22 Find the gradient of the function

$$
f = x ^ {2} + 3 x y + z ^ {2} \sin \left(\frac {x}{y}\right).
$$

## SOLUTION ▶

$$
\begin{array}{r l} \nabla f & = \mathbf {i} \left(\frac {\partial f}{\partial y}\right) + \mathbf {j} \left(\frac {\partial f}{\partial y}\right) + \mathbf {k} \left(\frac {\partial f}{\partial z}\right) \\ & = \mathbf {i} \left[ 2 x + 3 y + \frac {z ^ {2}}{y} \cos \left(\frac {x}{y}\right) \right] + \mathbf {j} \left[ 3 x - \frac {x z ^ {2}}{y ^ {2}} \cos \left(\frac {x}{y}\right) \right] + \mathbf {k} 2 z \sin \left(\frac {x}{y}\right) \end{array}
$$

EXERCISE 7.20 ▶

Find the gradient of the function

$$
g = a x ^ {3} + y e ^ {b z},
$$

where $a$ and $b$ are constants.

A common example of a gradient is found in mechanics. In a conservative system, the force on a particle is given by

$$
\boxed {\mathbf {F} = - \nabla \mathcal {V}}\tag{7.63}
$$

where V is the potential energy of the entire system. The gradient is taken with respect to the coordinates of the particle being considered, and the coordinates of any other particles are treated as constants in the differentiations.

EXAMPLE 7.23 The potential energy of an object of mass m near the surface of the earth is

$$
\mathcal {V} = m g z,
$$

where g is the acceleration due to gravity. Find the gravitational force on the object.

## SOLUTION ▶

$$
\mathbf {F} = - \mathbf {k} m g.
$$

EXERCISE 7.21 ▶ Neglecting the attractions of all other celestial bodies, the gravitational potential energy of the earth and the sun is given by

$$
\mathcal {V} = - \frac {G m _ {s} m _ {e}}{r},
$$

where G is the universal gravitational constant, equal to $6.673 \times 10^{-11} \, m^{3} \, s^{-2} \, kg^{-1}$ , $m_{s}$ the mass of the sun, $m_{e}$ the mass of the earth, and r the distance from the center of the sun to the center of the earth,

$$
r = \left(x ^ {2} + y ^ {2} + z ^ {2}\right) ^ {1 / 2}
$$

Find the force on the earth in Cartesian coordinates. That is, find the force in terms of the unit vectors i, j, and k with the components expressed in terms of x, y, and z. Find the magnitude of the force.

The operator $\nabla$ can operate on vector functions as well as on scalar functions. An example of a vector function is the velocity of a compressible flowing fluid

$$
\mathbf {v} = \mathbf {v} (x, y, z)\tag{7.64}
$$

In terms of Cartesian components

$$
\mathbf {v} = \mathbf {i} v _ {x} (x, y, z) + \mathbf {j} v _ {y} (x, y, z) + \mathbf {k} v _ {z} (x, y, z).\tag{7.65}
$$

There are two principal vector derivatives of vector functions. The divergence of F is defined in Cartesian coordinates by

$$
\boxed {\nabla \cdot \mathbf {F} = \left(\frac {\partial F _ {x}}{\partial x}\right) + \left(\frac {\partial F _ {y}}{\partial y}\right) + \left(\frac {\partial F _ {z}}{\partial z}\right),}\tag{7.66}
$$

where F is a vector function with Cartesian components $F_{x}$ , $F_{y}$ , and $F_{z}$ . The divergence of a vector function F is a scalar and is somewhat analogous to a scalar product (dot product) of two vectors. The divergence of F is sometimes denoted by divF.

One way to visualize the divergence of a function is to consider the divergence of the velocity of a compressible fluid. Curves that are followed by small portions of the fluid are called stream lines. In a region where the stream lines diverge (become farther from each other) as the flow is followed, the fluid will become less dense, and in such a region the divergence of the velocity is positive. The divergence thus provides a measure of the spreading of the stream lines. The equation of continuity of a compressible fluid expresses the effect this spreading has on the density of the fluid,

$$
\nabla \cdot (\rho \mathbf {v}) = - \frac {\partial \rho}{\partial t},\tag{7.67}
$$

where $\rho$ is the density of the fluid, v is its velocity, and t is the time.

EXAMPLE 7.24 Find $\nabla \cdot \mathbf{F}$ if

$$
\mathbf {F} = \mathbf {i} x ^ {2} + \mathbf {j} y z + \mathbf {k} \frac {x z ^ {2}}{y}
$$

SOLUTION ▶

$$
\nabla \cdot \mathbf {F} = 2 x + z + \frac {2 x z}{y}.
$$

EXERCISE 7.22 ▶

$$
\text {   Find   } \nabla \cdot \mathbf {r} \text {   if   }
$$

$$
\mathbf {r} = \mathbf {i} x + \mathbf {j} y + \mathbf {k} z.
$$


The curl of the vector function $\mathbf{F}$ is defined in Cartesian coordinates by

$$
\nabla \times \mathbf {F} = \mathbf {i} \left(\frac {\partial F _ {z}}{\partial y} - \frac {\partial F _ {y}}{\partial z}\right) + \mathbf {j} \left(\frac {\partial F _ {x}}{\partial z} - \frac {\partial F _ {z}}{\partial x}\right) + \mathbf {k} \left(\frac {\partial F _ {y}}{\partial x} - \frac {\partial F _ {x}}{\partial y}\right).\tag{7.68}
$$

The curl is a vector and is somewhat analogous to the vector product (cross product) of two vectors. To remember which vector derivative is which, remember that "dot" and "divergence" both begin with the letter "d" and that "cross" and "curl" both begin with the letter "c." The symbol curlF is sometimes used for the curl of F.

The curl of a vector function is more difficult to visualize than is the divergence. In fluid flow, the curl of the velocity gives the vorticity of the flow, or the rate of turning of the velocity vector. Because of this, the symbol rotF is also sometimes used for the curl of F.

EXAMPLE 7.25 Find $\nabla \times \mathbf{F}$ if

$$
\mathbf {F} = \mathbf {i} y + \mathbf {j} z + \mathbf {k} x.
$$

SOLUTION ▶

$$
\nabla \times \mathbf {F} = \mathbf {i} (0 - 1) + \mathbf {j} (0 - 1) + \mathbf {k} (0 - 1) = - \mathbf {i} - \mathbf {j} - \mathbf {k}.
$$

EXERCISE 7.23 ▶

Find $\nabla \times \mathbf{r}$ if

$$
\mathbf {r} = \mathbf {i} x + \mathbf {j} y + \mathbf {k} z.
$$

We can define derivatives corresponding to successive application of the del operator. The first such operator is the divergence of the gradient. If f is a scalar function, the divergence of the gradient of f is given in Cartesian coordinates by

$$
\boxed {\nabla \cdot \nabla f = \nabla^ {2} f = \left(\frac {\partial^ {2} f}{\partial x ^ {2}}\right) + \left(\frac {\partial^ {2} f}{\partial y ^ {2}}\right) + \left(\frac {\partial^ {2} f}{\partial z ^ {2}}\right)}\tag{7.69}
$$

The operator $\nabla\cdot\nabla$ occurs so commonly that it has its own name, the Laplacian operator, $^{2}$ and its own symbol, $\nabla^{2}$ , sometimes called “del squared.” It is an operator that occurs in the Schrödinger equation of quantum mechanics and in electrostatics.

EXAMPLE 7.26 Find the Laplacian of the function

$$
f (x, y, z) = A \sin (a x) \sin (b y) \sin (c z).
$$

SOLUTION ▶

$$
\begin{array}{r c l} \nabla^ {2} f & = & - A a ^ {2} \sin (a x) \sin (b y) \sin (c z) - A b ^ {2} \sin (a x) \sin (b y) \sin (c z) \\ & = & - A c ^ {2} \sin (a x) \sin (b y) \sin (c z) \\ & = & - (a ^ {2} + b ^ {2} + c ^ {2}) f. \end{array}
$$

EXERCISE 7.24 ▶

$$
\text {   Find   } \nabla^ {2} f \text {   if   } f = \exp (x ^ {2} + y ^ {2} + z ^ {2}) = e ^ {x ^ {2}} e ^ {y ^ {2}} e ^ {z ^ {2}}. \tag {4}
$$

Two other possibilities for successive operation of the del operator are the curl of the gradient and the gradient of the divergence. The curl of the gradient of any differentiable scalar function always vanishes.

EXERCISE 7.25

(a) Show that $\nabla \times \nabla f = 0$ if $f$ is a differentiable scalar function.

(b) Write the expression for $\nabla(\nabla\times\mathbf{F})$ , the gradient of the divergence of a vector function F, in Cartesian coordinates.


## Vector Derivatives in Other Coordinate Systems

It is sometimes convenient to work in coordinate systems other than Cartesian coordinates. For example, in the Schrödinger equation for the quantum mechanical motion of the electron in a hydrogen atom, the potential energy is a simple function of r, the distance of the electron from the nucleus, but it is a more complicated function of x, y, and z. This Schrödinger equation can be solved only if spherical polar coordinates are used. The complications produced by expressing the Laplacian in spherical polar coordinates are more than outweighed by the simplifications produced by having a simple expression for the potential energy.

Coordinate systems such as spherical polar or cylindrical polar coordinates are called orthogonal coordinates, because an infinitesimal displacement produced by changing only one of the coordinates is perpendicular (orthogonal) to a displacement produced by an infinitesimal change in any one of the other coordinates.

1. Figure 7.7 shows displacements, drawn as though they were finite, produced by infinitesimal changes in $r$ , $\theta$ , and $\phi$ . These displacements are lengths

$$
d s _ {r} = \text { displacement   in } r \text { direction } = d r
$$

$$
d s _ {\theta} = \text { displacement   in } \theta \text { direction } = r d \theta
$$

$$
d s _ {\phi} = \text { displacement   in } \phi \text { direction } = r \sin (\phi) d \theta .
$$

We define three vectors of unit length, whose directions are those of the infinitesimal displacements in Fig. 7.7, called $e_{r}$ , $e_{\theta}$ , and $e_{\phi}$ .

![[3f1c169c88fbb4c3593a01d53e21df1844e5804126a7077ef81d2c651ec46e1e.jpg]]  
Figure 7.7 ▶ Infinitesimal displacements $ds_{r}$ , $ds_{\theta}$ , and $ds_{\phi}$ produced by infinitesimal increments dr, $d\theta$ , and $d\phi$ .

An infinitesimal vector displacement is the sum of displacements in the three orthogonal directions. In Cartesian coordinates,

$$
d \mathbf {r} = \mathbf {i} d x + \mathbf {j} d y + \mathbf {k} d z.\tag{7.70}
$$

In spherical polar coordinates,

$$
d \mathbf {r} = \mathbf {e} _ {r} d r + \mathbf {e} _ {\theta} r d \theta + \mathbf {e} _ {\phi} r \sin (\theta) d \theta .\tag{7.71}
$$

We can write an expression for an infinitesimal vector displacement dr in a form that will hold for any set of orthogonal coordinates. Let the three coordinates of an orthogonal system in three dimensions be called $q_{1}$ , $q_{2}$ , and $q_{3}$ . Let the displacements due to the infinitesimal increments he called $ds_{1}$ , $ds_{2}$ , and $ds_{3}$ . Let the unit vectors in the directions of the displacements be called $e_{1}$ , $e_{2}$ , and $e_{3}$ . The equation analogous to Eq. (7.71) is

$$
d \mathbf {r} = \mathbf {e} _ {1} d s _ {1} + \mathbf {e} _ {2} d s _ {2} + \mathbf {e} _ {3} d s _ {3} = \mathbf {e} _ {1} h _ {1} d q _ {1} + \mathbf {e} _ {2} h _ {2} d q _ {2} + \mathbf {e} _ {3} h _ {3} d q _ {3},
$$

where the h's are the factors needed to give the correct expression for each displacement. For Cartesian coordinates, all three of the h factors are equal to unity. For spherical polar coordinates, $h_{r} = 1$ , $h_{\theta} = r$ , and $h_{\phi} = r \sin(\theta)$ . For other systems, you can figure out what the h's are geometrically so that ds = hdq for each coordinate.

## Gradients in Orthogonal Coordinates

The gradient of a scalar function f is written in terms of components in the direction of $ds_{1}$ , $ds_{2}$ , and $ds_{3}$ as

$$
\nabla f = \mathbf {e} _ {1} \frac {\partial f}{\partial s _ {1}} + \mathbf {e} _ {2} \frac {\partial f}{\partial s _ {2}} + \mathbf {e} _ {3} \frac {\partial f}{\partial s _ {3}}
$$

or

$$
\boxed {\nabla f = \mathbf {e} _ {1} \frac {1}{h _ {1}} \frac {\partial f}{\partial q _ {1}} + \mathbf {e} _ {2} \frac {1}{h _ {2}} \frac {\partial f}{\partial q _ {2}} + \mathbf {e} _ {3} \frac {1}{h _ {3}} \frac {\partial f}{\partial q _ {3}}}.\tag{7.72}
$$

EXAMPLE 7.27 Find the expression for the gradient of a function of spherical polar coordinates $f = f(r, \theta, \phi)$ .

SOLUTION ▶

$$
\nabla f = \mathbf {e} _ {r} \frac {\partial f}{\partial r} + \mathbf {e} _ {\theta} \frac {1}{r} \frac {\partial f}{\partial \theta} + \mathbf {e} _ {\phi} \frac {1}{r \sin (\theta)} \frac {\partial f}{\partial \phi}.
$$

## EXERCISE 7.26 ▶

(a) Find the $h$ factors for cylindrical polar coordinates.

(b) Find the expression for the gradient of a function of cylindrical polar coordinates, $f = f(\rho, \phi, z)$ . Find the gradient of the function

$$
f = e ^ {- \left(\rho^ {2} + z ^ {2}\right) / a ^ {2}} \sin (\phi).
$$

![[e2f54334b46f8de8ddce6b01152d2fa15dd993e4ee5eed9f047a9bacc0e321f4.jpg]]

The diver, coordinates. vectors of the if a vector function can similarly be expressed in orthogonal a vector function, it must be expressed in terms of the unit nate system in which we are to differentiate,

$$
\mathbf {F} = \mathbf {e} _ {1} F _ {1} + \mathbf {e} _ {2} F _ {2} + \mathbf {e} _ {3} F _ {3}.\tag{7.73}
$$

The components $F_{1}, F_{2}$ , and $F_{3}$ are the components in the directions of $\mathbf{e}_1, \mathbf{e}_2$ , and $\mathbf{e}_3$ , not necessarily the Cartesian components.

The divergence of the vector function $\mathbf{F}$ is given by

$$
\boxed {\nabla \cdot \mathbf {F} = \frac {1}{h _ {1} h _ {2} h _ {3}} \left[ \frac {\partial}{\partial q _ {1}} (F _ {1} h _ {2} h _ {3}) + \frac {\partial}{\partial q _ {2}} (F _ {2} h _ {1} h _ {3}) + \frac {\partial}{\partial q _ {3}} (F _ {3} h _ {1} h _ {2}) \right].}\tag{7.74}
$$

EXAMPLE 7.28 (a) Write the expression for the divergence of a vector function F expressed in terms of spherical polar coordinates.

(b) Find the divergence of the position vector, which in spherical polar coordinates is

$$
\mathbf {r} = \mathbf {e} _ {r} r.
$$

SOLUTION ▶ (a)

$$
\begin{array}{r l} \nabla \cdot \mathbf {F} & = \frac {1}{r ^ {2} \sin (\theta)} \left[ \frac {\partial}{\partial r} \left[ F _ {r} r ^ {2} \sin (\theta) \right] + \frac {\partial}{\partial \theta} \left[ F _ {\theta} r \sin (\theta) \right] + \frac {\partial}{\partial \phi} (F _ {\phi} r) \right] \\ & = \frac {1}{r ^ {2}} \frac {\partial}{\partial r} \left(r ^ {2} F _ {r}\right) + \frac {1}{r \sin (\theta)} \frac {\partial}{\partial \theta} \left[ \sin (\theta) F _ {\theta} \right] \\ & + \frac {1}{r \sin (\theta)} \frac {\partial F _ {\phi}}{\partial \phi}. \end{array} \tag {7.75}
$$

(b) The divergence of $\mathbf{r}$ is

$$
\nabla \cdot \mathbf {r} = \frac {1}{r ^ {2}} 3 r ^ {2} + 0 + 0 = 3.
$$

EXERCISE 7.27 ▶ Write the formula for the divergence of a function in cylindrical polar coordinates.

The curl of a vector function $\mathbf{F}$ is

$$
\begin{array}{l} \nabla \times \mathbf {F} = \mathbf {e} _ {1} \frac {1}{h _ {2} h _ {3}} \left[ \frac {\partial}{\partial q _ {2}} (h _ {3} F _ {3}) - \frac {\partial}{\partial q _ {3}} (h _ {2} F _ {2}) \right] \\ \qquad + \mathbf {e} _ {2} \frac {1}{h _ {1} h _ {3}} \left[ \frac {\partial}{\partial q _ {3}} (h _ {1} F _ {1}) - \frac {\partial}{\partial q _ {1}} (h _ {3} F _ {3}) \right] \\ \qquad + \mathbf {e} _ {3} \frac {1}{h _ {1} h _ {2}} \left[ \frac {\partial}{\partial q _ {1}} (h _ {2} F _ {2}) - \frac {\partial}{\partial q _ {2}} (h _ {1} F _ {1}) \right]. \end{array}\tag{7.76}
$$

The expression for the Laplacian of a scalar function, $f$ , is

$$
\nabla^ {2} f = \frac {1}{h _ {1} h _ {2} h _ {3}} \left[ \frac {\partial}{\partial q _ {1}} \left(\frac {h _ {2} h _ {3}}{h _ {1}} \frac {\partial f}{\partial q _ {1}}\right) + \frac {\partial}{\partial q _ {2}} \left(\frac {h _ {1} h _ {3}}{h _ {2}} \frac {\partial f}{\partial q _ {2}}\right) + \frac {\partial}{\partial q _ {3}} \left(\frac {h _ {1} h _ {2}}{h _ {3}} \frac {\partial f}{\partial q _ {3}}\right) \right]\tag{7.77}
$$

EXAMPLE 7.29 Write the expression for the Laplacian in spherical polar coordinates.

SOLUTION ▶

$$
\nabla^ {2} f = \frac {1}{r ^ {2}} \frac {\partial}{\partial r} \left(r ^ {2} \frac {\partial f}{\partial r}\right) + \frac {1}{r ^ {2} \sin (\theta)} \frac {\partial}{\partial \theta} [ \sin (\theta) \frac {\partial f}{\partial \theta} ] + \frac {1}{r ^ {2} \sin^ {2} (\theta)} \frac {\partial f}{\partial \phi^ {2}}.\tag{7.78}
$$

EXERCISE 7.28 ▶

Write the expression for the Laplacian in cylindrical polar coordinates

## 7.8 Maximum and Minimum Values of Functions of Several Variables

A point at which either a maximum or a minimum value in a function occurs is sometimes called an extremum. For example, Fig. 7.8 shows a perspective view of a graph of the function $f = e^{-x^{2} - y^{2}}$ . The surface representing the function has a “peak” at the origin, where the function attains its maximum value. Shown also in the figure is a curve at which the surface intersects with a plane representing the equation y = 1 - x. On this curve there is also a maximum, which has a smaller value than the maximum at the peak. We call this value the maximum subject to the constraint that y = 1 - x. We discuss the constrained maximum later.

![[7daa1fb53e487ab9b0660030d00df396d19ec6ec3ec80cb605d6a911e185d83a.jpg]]  
Figure 7.8 ▶ The surface representing a function of x and y with the absolute maximum and a constrained maximum shown.

A maximum at a peak such as the maximum at the origin in Fig. 7.8 is called a local maximum or a relative maximum. The value of the function at such a peak is larger than at any other point in the immediate vicinity. However, a complicated function can have more than one local maximum. Also, if we consider a finite region, the function might have a larger value somewhere on the boundary of the region that is larger than the value at a local maximum. To find the absolute maximum of the function for a given region, we must consider all local maxima and any points on the boundary of the region that might have greater values. The peak at the origin is the absolute maximum of this function. Points of minimum value are completely analogous to points of maximum value. Local minima are located at the bottom of depressions or valleys in the surface representing the function. To find an absolute minimum for a given region, you must consider all local minima and any points on the boundary of the region that might have smaller values.

To find a local maximum or minimum, we use the fact that the plane that is tangent to the surface will be horizontal at any local maximum or minimum. Therefore, the curve representing the intersection of any vertical plane with the surface will have a local maximum or a minimum at the same place. The partial derivative with respect to one independent variable gives the slope of the curve in the plane corresponding to a constant value of the other independent variable, so we can find a local maximum or minimum by finding the places where all the partial derivatives of the function vanish simultaneously.

Our method for a differentiable function of two variables is therefore:

1. Solve the simultaneous equations

$$
\left(\frac {\partial f}{\partial x}\right) _ {y} = 0\tag{7.79}
$$

$$
\left(\frac {\partial f}{\partial y}\right) _ {x} = 0\tag{7.80}
$$

2. Calculate the value of the function at all points satisfying these equations, and also at the boundaries of the region being considered. The maximum or minimum value in the region being considered must be in this set of values.

3. If there are points at which the function is not differentiable, such as discontinuities or cusps, these points must also be included in the set of possible locations of the maximum or minimum.

EXAMPLE 7.30 Find the maximum value of the function shown in Fig. 7.8, $f = e^{-x^2 - y^2}$ .

SOLUTION ▶ At a local maximum or minimum

$$
\left(\frac {\partial f}{\partial x}\right) _ {y} = e ^ {- x ^ {2} - y ^ {2}} (- 2 x) = 0
$$

$$
\left(\frac {\partial f}{\partial y}\right) _ {x} = e ^ {- x ^ {2} - y ^ {2}} (- 2 y) = 0.
$$

The only solution for finite values of x and y is x = 0, y = 0. Since no restricted region was specified, we consider all values of x and y. For very large magnitudes of x or y, the function vanishes, so we have found the desired absolute maximum, at which f = 1.

In the case of one independent variable, a local maximum could be distinguished from a local minimum or an inflection point by determining the sign of the second derivative. With more than one variable, the situation is more complicated. In addition to inflection points, we can have points corresponding to a maximum with respect to one variable and a minimum with respect to another. Such a point is called a saddle point, and at such a point, the surface representing the function resembles a mountain pass or the surface of a saddle. Such points are important in the transition-state theory of chemical reaction rates.

For two independent variables, the following quantity is calculated:

$$
D = \left(\frac {\partial^ {2} f}{\partial x ^ {2}}\right) \left(\frac {\partial^ {2} f}{\partial y ^ {2}}\right) - \left(\frac {\partial^ {2} f}{\partial x \partial y}\right) ^ {2}.\tag{7.81}
$$

The different cases are as follows:

1. If D > 0 and $(\partial^{2}f/\partial x^{2}) > 0$ , then we have a local minimum.

2. If $D > 0$ and $(\partial^2 f / \partial x^2) < 0$ , then we have a local maximum.

3. If D < 0, then we have neither a local maximum nor a local minimum.

4. If $D = 0$ , the test fails, and we cannot tell what we have.

EXERCISE 7.29 ▶ Evaluate D at the point $(0, 0)$ for the function of Example 7.30 and establish that the point is a local maximum.

For more than two independent variables, the method is similar, except that there is one equation for each independent variable.

## Constrained Maximum/Minimum Problems

Sometimes we must find a maximum or a minimum value of a function subject to some condition, which is called a constraint. Such an extremum is called a constrained maximum or a constrained minimum. Generally, a constrained maximum is smaller than the unconstrained maximum of the function, and a constrained minimum is larger than the unconstrained minimum of the function. Consider the following example:

EXAMPLE 7.31 Find the maximum value of the function in Example 7.30 subject to the constraint $x + y = 1$ .

SOLUTION ▶ The situation is shown in Fig. 7.8. The constraint corresponds to the specification of y as a function of x by

$$
y = 1 - x.\tag{7.82}
$$

This function is given by the line in the x-y plane of the figure. We are now looking for the place along this curve at which the function has a larger value than at any other place on the curve. Unless the curve happens to pass through the unconstrained maximum, the constrained maximum will be smaller than the unconstrained maximum.

Since y is no longer an independent variable on the curve of the constraint, the direct way to proceed is to replace y by use of Eq. (7.82):

$$
f = (x, 1 - x) = f (x) = e ^ {- x ^ {2} - (1 - x) ^ {2}} = e ^ {- 2 x ^ {2} + 2 x - 1}.\tag{7.83}
$$

The local maximum is now at the point where df/dx vanishes:

$$
\frac {d f}{d x} = e ^ {- 2 x ^ {2} - (1 - x) ^ {2}} (- 4 x + 2) = 0.\tag{7.84}
$$

This equation is satisfied by $x = \frac{1}{2}$ and by $|x| \to \infty$ . The constrained maximum corresponds to $x = \frac{1}{2}$ and the minimum corresponds to $|x| \to \infty$ . At the constrained maximum $y = 1 - \frac{1}{2} = \frac{1}{2}$ and

$$
f \left(\frac {1}{2}, \frac {1}{2}\right) \exp \left[ - \left(\frac {1}{2} ^ {2}\right) - \left(\frac {1}{2}\right) ^ {2} \right] = e ^ {- 1 / 2} = 0.6065 \dots .
$$

As expected, this value is smaller than the unconstrained maximum, at which f = 1.

EXERCISE 7.30 ▶

(a) Find the minimum in the function

$$
f (x, y) = x ^ {2} + y ^ {2} + 2 x.
$$

(b) Find the constrained minimum subject to the constraint

$$
x + y = 0.
$$

## Lagrange's Method of Undetermined Multipliers $^{3}$

If we have a constrained maximum or minimum problem with more than two variables, the direct method of substituting the constraint relation into the function is usually not practical. Lagrange's method finds a constrained maximum or minimum without substituting the constraint relation into the function. If the constraint is written in the form $g(x, y) = 0$ , the method for finding the constrained maximum or minimum in $f(x, y)$ is as follows:

## 1. Form the new function

$$
u (x, y) = f (x, y) + \lambda g (x, y),\tag{7.85}
$$

where $\lambda$ is a constant called an undetermined multiplier. Its value is unknown at this point of the analysis.

2. Form the partial derivatives of u, and set them equal to zero,

$$
\left(\frac {\partial u}{\partial x}\right) _ {y} = \left(\frac {\partial f}{\partial x}\right) _ {y} + \lambda \left(\frac {\partial g}{\partial x}\right) _ {y} = 0\tag{7.86}
$$

$$
\left(\frac {\partial u}{\partial x}\right) _ {x} = \left(\frac {\partial f}{\partial x}\right) _ {x} + \lambda \left(\frac {\partial g}{\partial x}\right) _ {x} = 0.\tag{7.87}
$$

3. Solve the set of equations consisting of g = 0 and the two equations of Eqs. (7.86) and (7.87) as a set of simultaneous equations for the value of x, the value of y, and the value of $\lambda$ that correspond to the local maximum or minimum.

We will not present a proof of the validity of this method, but you can find a proof in calculus textbooks.

EXAMPLE 7.32 Find the constrained maximum of Example 7.31 by the method of Lagrange.

SOLUTION ▶ The constraining equation is written

$$
g (x, y) = x + y - 1 = 0.\tag{7.88}
$$

The function $u$ is

$$
u (x, y) = e ^ {- x ^ {2} - y ^ {2}} + \lambda (x + y - 1)
$$

so that the equations to be solved are Eq. (7.88) and

$$
\left(\frac {\partial u}{\partial x}\right) _ {y} = (- 2 x) e ^ {- x ^ {2} - y ^ {2}} + \lambda = 0\tag{7.89}
$$

$$
\left(\frac {\partial u}{\partial y}\right) _ {x} = (- 2 y) e ^ {- x ^ {2} - y ^ {2}} + \lambda = 0.\tag{7.90}
$$

Let us begin by solving for $\lambda$ in terms of x and y. Multiply Eq. (7.89) and Eq. (7.90) by x and add the two equations. The result can be solved to give

$$
\lambda = \frac {4 x y}{x + y} e ^ {- x ^ {2} - y ^ {2}}.\tag{7.91}
$$

Substitute this into Eq. (7.89) to obtain

$$
(- 2 x) e ^ {- x ^ {2} - y ^ {2}} + \frac {4 x y}{x + y} e ^ {- x ^ {2} - y ^ {2}} = 0.\tag{7.92}
$$

The exponential factor is not zero for any finite values of x and y, so

$$
- 2 x + \frac {4 x y}{x + y} = 0.\tag{7.93}
$$

When Eq. (7.91) is substituted into Eq. (7.90) in the same way, the result is

$$
- 2 y + \frac {4 x y}{x + y} = 0.\tag{7.94}
$$

When Eq. (7.94) is subtracted from Eq. (7.94), the result is

$$
- 2 x + 2 y = 0
$$

which is solved for $y$ in terms of $x$ to obtain

$$
y = x.
$$

This is substituted into Eq. (7.88) to obtain

$$
x + x - 1 = 0
$$

which gives

$$
x + \frac {1}{2}, \quad y = \frac {1}{2}.
$$

This is the same result as in Example 7.31. In this case, the method of Lagrange was more work than the direct method. In more complicated problems, the method of Lagrange will usually be easier.

The method of Lagrange also works if there is more than one constraint. If we desire the local maximum or minimum of the function

$$
f = f (x, y, z)
$$

subject to the two constraints

$$
g _ {1} (x, y, z) = 0\tag{7.95}
$$

and

$$
g _ {2} (x, y, z) = 0\tag{7.96}
$$

the procedure is similar, except that two undetermined multipliers are used. One forms the function

$$
u = u (x, y, z) = f (x, y, z) + \lambda_ {1} g _ {1} (x, y, z) + \lambda_ {2} g _ {2} (x, y, z)\tag{7.97}
$$

and solves the set of simultaneous equations consisting of Eqs. (7.95), (7.96), and

$$
\left(\frac {\partial u}{\partial x}\right) _ {y, z} = 0\tag{7.98}
$$

$$
\left(\frac {\partial u}{\partial y}\right) _ {x, z} = 0\tag{7.99}
$$

$$
\left(\frac {\partial u}{\partial z}\right) _ {x, y} = 0\tag{7.100}
$$

The result is a value for $\lambda_{1}$ , a value for $\lambda_{2}$ , and values for x, y, and z which locate the constrained local maximum or minimum.

EXERCISE 7.31 ▶ Find the constrained minimum of Exercise 7.30 using the method of Lagrange.

## SUMMARY

The calculus of functions of several independent variables is a natural extension of the calculus of functions of one independent variable. The partial derivative is the first important quantity. For example, a function of three independent variables has three partial derivatives. Each one is obtained by the same techniques as with ordinary derivatives, treating other independent variables temporarily as constants. The differential of a function of $x_{1}$ , $x_{2}$ , and $x_{3}$ is given by

$$
d f = \left(\frac {\partial f}{\partial x}\right) _ {x _ {3}, x _ {3}} d x _ {1} + \left(\frac {\partial f}{\partial x _ {2}}\right) _ {x _ {1}, x _ {3}} d x _ {2} + \left(\frac {\partial f}{\partial x _ {3}}\right) _ {x _ {1}, x _ {2}} d x _ {3},
$$

where df is an infinitesimal change in the function f produced by the changes $dx_{1}$ , $dx_{2}$ , and $dx_{3}$ imposed on the independent variables and where the coefficients are partial derivatives. This is called an exact differential, identifying df as in increment in a function. A similar expression such as

$$
d w = M d x _ {1} + N d x _ {2} + P d x _ {3}
$$

is an inexact differential if the coefficients M, N, and P are not the appropriate derivatives of the same function. If not, they do not obey the Euler reciprocity relation, which is one of several relations that partial derivatives obey.

One application of partial derivatives is in the search for minimum and maximum values of a function. An extremum (minimum or maximum) of a function in a region is found either at a boundary of the region or at a point where all of the partial derivatives vanish. A constrained maximum or minimum is found by the method of Lagrange, in which a particular augmented function is maximized or minimized.

A line integral is denoted by

$$
\int_ {c} d w = \int_ {c} (M d x _ {1} + N d x _ {2} + P d x _ {3}).
$$

In this integral, the variables $x_{2}$ and $x_{3}$ in M must be replaced by functions of $x_{1}$ corresponding to the curve on which the integral is performed, with similar replacements in N and P. The line integral of the differential of a function depends only on the end points of the curve, which the line integral of an inexact differential depends on the path of the curve as well as on the end points.

A multiple integral is an integral of the form

$$
\iiint f (x, y, z) d z d y d x
$$

in which the integrations are carried out one after another. As each integration is carried out, those integration variables not yet integrated are treated as constants.

## PROBLEMS

1. A certain nonideal gas has an equation of state

$$
\frac {P V _ {m}}{R T} = 1 + \frac {B _ {2}}{V _ {m}},
$$

where T is the temperature on the Kelvin scale, $V_{m}$ is the molar volume (volume of 1 mol), P is the pressure, and R is the gas constant. The second virial coefficient $B_{2}$ is given as a function of T by

$$
B _ {2} = \left[ - 1.00 \times 10 ^ {- 4} - (2.148 \times 10 ^ {- 6}) e ^ {(1956 \mathrm{K}) / T} \right] \mathrm{m} ^ {3} \mathrm{mol} ^ {- 1},
$$

Find $(\partial P / \partial V_m)_T$ and $(\partial P / \partial T)_{V_m}$ and an expression for $dP$ .

2. For a certain system, the thermodynamic energy $U$ is given as a function of $S$ , $V$ , and $n$ by

$$
U = U (S, V, n) = K n ^ {5 / 3} V ^ {- 2 / 3} e ^ {2 S / 3 n R},
$$

where S is the entropy, V is the volume, n is the number of moles, K is a constant, and R is the ideal gas constant.

a) Find $dU$ in terms of $dS, dV$ , and $dn$ .

b) Find an expression for $(\partial U / \partial S)_{V,n}$ .

c) Find an expression for $(\partial U / \partial V)_{S,n}$ .

d) Find an expression for $(\partial U / \partial n)_{S,V}$ .

3. Find $(\partial f / \partial x)_y$ , and $(\partial f / \partial y)_x$ for each of the following functions, where $a, b$ , and $c$ are constants.

a) $f = axy\ln (y) + bx\cos (x + y)$

b) $f = ae^{-b(x^2 + y^2)} + c\sin (x^2 y)$

c) $f = a(x + by) / (c + xy)$

4. Find $(\partial f / \partial x)_y$ , and $(\partial f / \partial y)_x$ for each of the following functions, where $a, b$ , and $c$ are constants.

a) $f = a(bx + cy)^{-3}$ .

b) $f = a\cos^2 (bx) - b\sin^3 (y)$

c) $f = a\exp \left(-b(x^{2} - y^{2})\right)$

5. Find $(\partial^{2}f/\partial x^{2})_{y}$ , $(\partial^{2}f/\partial x\partial y)$ , $(\partial^{2}f/\partial y\partial x)$ , and $(\partial^{2}f/\partial y^{2})$ , for each of the following functions, where a, b, and c are constants.

a) $f = (x + y)^{-1}$

b) $f = \cos (x / y)$

c) $f = e^{(ax^2 + by^2)}$ .

6. Find $(\partial^{2}f/\partial x^{2})_{y}, (\partial^{2}f/\partial x\partial y), (\partial^{2}f/\partial y\partial x)$ , and $(\partial^{2}f/\partial y^{2})$ , for each of the following functions, where a, b, and c are constants.

a) $f = a\ln (bx^{2} + cy^{2})$

b) $f = a(x^{2} + y^{2})^{-2}$

c) $f = a\cos (\sin (x))$

7.

a) Find the area of the semicircle of radius $a$ given by

$$
y = + (a ^ {2} - x ^ {2}) ^ {1 / 2}
$$

by doing the double integral

$$
\int_ {- a} ^ {a} \int_ {0} ^ {\left(a ^ {2} - x ^ {2}\right) ^ {1 / 2}} 1 d y d x.
$$

b) Change to polar coordinates and repeat the calculation.

8. Test each of the following differentials for exactness.

a) $du = by\cos (bx)dx + \sin (bx)dy$

b) $du = ay \sin(xy) dx + ax \sin(xy) dy$

c) $du = (y/(1 + x^{2})) dx - \tan^{-1}(x) dy$

9. Test each of the following differentials for exactness.

a) $du = x dy + y dx$

b) $du = y \ln(x) dx + x \ln(y) dy$

c) $du = 2xe^{axy}dx + 2ye^{axy}dy.$

10. If $G = -RT \ln(aT^{3/2}V/n)$ find dG in terms of dT, dV, and dn, where R and a are constants.

11.

a) Perform the line integral

$$
\int_ {C} d u = \int_ {C} (x ^ {2} y d x + x y ^ {2} d y),
$$

where c represents the line segment from $(0, 0)$ to $(2, 2)$ . Would another path with the same end points yield the same result?

b) Perform the line integral on the path from $(0,0)$ to $(2,0)$ and then from $(2,0)$ to $(2,2)$ .

12.

a) Perform the line integral

$$
\int_ {C} d u = \int_ {C} (x y ^ {2} d x + x ^ {2} y d y),
$$

where c represents the line segment from $(0, 0)$ to $(2, 2)$ . Would another path with the same end points yield the same result?

b) Perform the line integral on the path from $(0,0)$ to $(2,0)$ and then from $(2,0)$ to $(2,2)$ .

13. Find the function $f(x, y)$ whose differential is

$$
d f = (x + y) ^ {- 1} d x + (x + y) ^ {- 1} d y
$$

and which has the value $f(1,1)=0$ . Do this by performing a line integral on a rectangular path from $(1,1)$ to $(x_{1},y_{1})$ where $x_{1}>0$ and $y_{1}>0$ .

14. A wheel of radius R has a distribution of mass given by

$$
m (\rho) = a \rho^ {2} + b,
$$

where $\rho$ is the distance from the center, a and b are constants, and $m(\rho)$ is the mass per unit area as a function of $\rho$ . Assume that m depends only on $\rho$ . Find the moment of inertia, defined by

$$
I = \iint m (\rho) \rho^ {2} d A = \int_ {0} ^ {\infty} \int_ {0} ^ {2 \pi} m (\rho) \rho^ {2} \rho d \phi d \rho ,
$$

where dA represents the element of area and the integral is a double integral over the entire wheel. Transform to Cartesian coordinates and carry out the integral again. In order to simplify the limits of integration in Cartesian coordinate, integrate over half of the wheel and double your result.

## 15. Complete the formula

$$
\left(\frac {\partial S}{\partial V}\right) _ {P, n} = \left(\frac {\partial S}{\partial V}\right) _ {T, n} +?
$$

16. Find the location of the minimum in the function

$$
f = f (x, y) = x ^ {2} - 6 x + 8 y + y ^ {2}
$$

considering all real values of x and y. What is the value of the function at the minimum?

17. Find the minimum in the function of the previous problem subject to the constraint $x + y = 2$ . Do this by substitution and by the method of undetermined multipliers.

18. Find the location of the maximum in the function

$$
f = f (x, y) = x ^ {2} - 6 x + 8 y + y ^ {2}
$$

considering the region 0 < x < 2 and 0 < y < 2. What is the value of the function at the maximum?

19. Find the maximum in the function of the previous problem subject to the constraint $x + y = 2$ . Do this by substitution and by Lagrange's method of undetermined multipliers.

# Differential Equations

![[dc21ae2b9488f773aca4cbfc6c50964eba3673b83f5cf82a988b1088ed3a7c08.jpg]]

## Preview

A differential equation contains one or more derivatives of an unknown function, and solving a differential equation means finding what that function is. One important class of differential equations consists of classical equations of motion, which come from Newton's second law of motion. We will discuss the solution of several kinds of differential equations, including linear differential equations, in which the unknown function and its derivatives enter only to the first power, and exact differential equations, which can be solved by a line integration. We will also introduce partial differential equations, in which partial derivatives occur and in which there are two or more independent variables. We will also discuss the solution of differential equations by use of Laplace transformations. Some differential equations can be solved either symbolically or numerically using Mathematica.

## Principal Facts and Ideas

1. The solution of a differential equation is a function whose derivative or derivatives satisfy the differential equation.

2. An equation of motion is a differential equation obtained from Newton's second law of motion, $\mathbf{F} = m\mathbf{a}$ .

3. In principle, an equation of motion can be solved to give the position and velocity as a function of time for every particle in a system governed by Newton's laws of motion.

4. A homogeneous linear differential equation with constant coefficients can be solved by use of an exponential trial solution.

5. An inhomogeneous linear differential equation can be solved if a particular solution can be found.

6. An exact differential equation can be solved by a line integration.

7. Some inexact differential equations can be converted to exact differential equations by multiplication by an integrating factor.
234

8. Some partial differential equations can be solved by separation of variables.

9. A differential equation can be transformed into an algebraic equation by a Laplace transformation. Solution of this equation followed by inverse transformation provides a solution to the differential equation.

10. Differential equations can be solved numerically by a variety of methods, including the use of Mathematica.

## Objectives

After studying this chapter, you should be able to:

1. construct an equation of motion for a particle from Newton's second law;

2. solve a linear homogeneous differential equation with constant coefficients;

3. solve a differential equation whose variables can be separated;

4. solve an exact differential equation;

5. use an integrating factor to solve an inexact differential equation;

6. solve a simple partial differential equation by separation of variables;

7. solve a differential equation by use of Laplace transforms;

8. use Mathematica to solve differential equations symbolically and numerically.

## 8.1 Differential Equations and Newton's Laws of Motion

A differential equation is an equation that contains one or more derivations of an unknown function. The solution of a differential equation is the unknown function, not a set of constant values of an unknown variable as is the case with an algebraic equation. Our first examples of differential equations are equations of motion, obtained from Newton's second law of motion. These equations are used to determine the time dependence of the position and velocity of particles. The position of a particle is given by the position vector r with Cartesian components x, y, and z. The velocity v of a particle is the rate of change of its position vector,

$$
\mathbf {v} = \frac {d \mathbf {r}}{d t} = \mathbf {i} \frac {d x}{d t} + \mathbf {j} \frac {d y}{d t} + \mathbf {k} \frac {d z}{d t} = \mathbf {i} v _ {x} + \mathbf {j} v _ {y} + \mathbf {k} v _ {z},\tag{8.1}
$$

where i, j, and k are the unit vectors defined in Chapter 2. The acceleration a is the rate of change of the velocity:

$$
\mathbf {a} = \frac {d \mathbf {v}}{d t} = \frac {d ^ {2} \mathbf {r}}{d t ^ {2}} = \mathbf {i} \frac {d ^ {2} x}{d t ^ {2}} + \mathbf {j} \frac {d ^ {2} y}{d t ^ {2}} + \mathbf {k} \frac {d ^ {2} z}{d t ^ {2}} = \mathbf {i} a _ {x} + \mathbf {j} a _ {y} + \mathbf {k} a _ {z}.\tag{8.2}
$$

Consider a particle that moves in the z direction only, so that $v_{x}$ , $v_{y}$ , $a_{x}$ , and $a_{y}$ vanish. If $a_{z}$ is known as a function of time,

$$
a _ {z} = a _ {z} (t)\tag{8.3}
$$

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
EXAMPLE 8.1 At time t = 0, a certain particle has  $z(0) = 0$  and  $v_{z}(0) = 0$ . Its acceleration is given as a function of time by

 $a_{z}(t) = a_{0}e^{-t/b}$ ,

where  $a_{0}$  and b are constants.

(a) Find  $v_{z}$  as a function of time. (b) Find z as a function of time.

(c) Find the speed and the position of the particle at t = 30.0 s if  $a_{0} = 10.0 \, m \, s^{-2}$  and if  $b = 20.0 \, s$ .

(d) Find the limiting value of the speed as  $t \to \infty$ .
</div>

we can write an equation by equating the time derivative of the velocity to this known function:

$$
\frac {d v _ {z}}{d t} = a _ {z} (t).\tag{8.4}
$$

This is a differential equation for the velocity, since it contains the derivative of the velocity. Solving this equation means finding a function to represent the velocity as a function of time.

To solve Eq. (8.4), we multiply both sides by dt and perform a definite integration from t = 0 to $t = t_{1}$ .

$$
v _ {z} (t _ {1}) - v _ {z} (0) = \int_ {0} ^ {t _ {1}} \left(\frac {d v _ {z}}{d t}\right) d t = \int_ {0} ^ {t _ {1}} a _ {z} (t) d t.\tag{8.5}
$$

The result of this integration gives $v_{z}$ as a function of time, so that the position obeys a second differential equation

$$
\frac {d z}{d t} = v _ {z} (t).\tag{8.6}
$$

A second integration gives the position as a function of time:

$$
z _ {z} (t _ {2}) - z (0) = \int_ {0} ^ {t _ {2}} \left(\frac {d z}{d t _ {1}}\right) d t _ {1} = \int_ {0} ^ {t _ {2}} v _ {z} (t _ {1}) d t _ {1}.\tag{8.7}
$$

There are inertial navigation systems used on submarines and space vehicles that determine the acceleration as a function of time and perform two numerical integrations in order to determine the position of the vehicle.

## SOLUTION ▶

## (a) The antiderivative of the given acceleration

function plus a constant $v_{0}$ is the velocity:

$$
v _ {z} (t) = - a _ {0} b e ^ {- t / b} + v _ {0} = - a _ {0} b e ^ {- t / b} + a _ {0} b = a _ {0} b (1 - e ^ {- t / b})
$$

since it was specified that $v_{z}(0) = 0$ , the

constant $v_{0} = a_{0}b$ .

(b) The antiderivative of the velocity plus a

constant $z_0$ is the position:

$$
z (t) = a _ {0} b ^ {2} e ^ {- t / b} + a _ {0} b t + z _ {0} = a _ {0} b ^ {2} e ^ {- t / b} + a _ {0} b t - a _ {0} b ^ {2}
$$

Since it was specified that $z(0) = 0$ , the

constant $z_0 = -a_0b^2$

$$
\begin{array}{r l} \text {(c)} & \text {At} t = 30.0 \mathrm{s} \\ v _ {z} (30.0 \mathrm{s}) & = (10.0 \mathrm{ms} ^ {- 2}) (20.0 \mathrm{s}) (1 - e ^ {- 1.50}) = 155 \mathrm{ms} ^ {- 1} \\ z (30.0 \mathrm{s}) & = (10.0 \mathrm{ms} ^ {- 2}) (20.0 \mathrm{s}) ^ {2} e ^ {- 1.50} + (200.0 \mathrm{ms} ^ {- 1}) (30.0 \mathrm{s}) \\ & - (10.0 \mathrm{ms} ^ {- 2}) (20.0 \mathrm{s}) ^ {2} = 2890 \mathrm{m} \end{array}
$$

(d) As $t \to \infty$ , the speed approaches

$$
\lim _ {t \to \infty} v _ {z} (t) = a _ {0} b = 200. \mathrm{ms} ^ {- 1}
$$

Unfortunately, the acceleration is very seldom known as a function of time, so integration as in the previous example cannot usually be used to find how a particle moves. Instead, we must obtain the acceleration of the particle from knowledge of the force on it, using Newton's second law.

## Newton's Laws of Motion

These laws were deduced by Isaac Newton $^{1}$ from his analysis of observations of the motions of actual objects, including apples and celestial bodies. The laws can be stated:

1. A body on which no forces act does not accelerate.

2. A body acted on by a force F accelerates according to

$$
\mathbf {F} = m \mathbf {a},\tag{8.8}
$$

where m is the mass of the object and a is its acceleration.

3. Two bodies exert forces of equal magnitude and opposite direction on each other.

Classical mechanics is primarily the study of the consequences of these laws. It is sometimes called Newtonian mechanics. The first law is just a special case of the second, and the third law is primarily used to obtain forces for the second law, so Newton's second law is the most important equation of classical mechanics.

If the force on a particle can be written as a function of its position alone, we have an equation of motion. If the force on a particle depends on the positions of other particles, the equations of motion of the particles are coupled together and must be solved simultaneously. The equations of motion cannot be solved exactly for a system of more than two interacting particles.

The simplest equation of motion is for a single particle that can move in only one direction. From Newton's second law, we can write the following equation for a particle that moves in the $z$ direction:

$$
F _ {z} (z) = m \frac {d ^ {2} z}{d t ^ {2}}.\tag{8.9}
$$

A force that depends only on position can be derived from a potential energy function, as in Eq. (7.63). Equation (8.9) becomes

$$
- \frac {d \mathcal {V}}{d z} = m \frac {d ^ {2 z}}{d t ^ {2}},\tag{8.10}
$$

where V is the potential energy function. We now examine these equations for a particular example system.

## 8.2 The Harmonic Oscillator: Linear Differential Equations with Constant Coefficients

Consider an object of mass m attached to the end of a coil spring whose other end is rigidly fastened. Let the object move only in the z direction, the direction in which the spring is stretched or compressed. Define the z coordinate so that z = 0 when the spring has its equilibrium length. To a good approximation, the force on the object due to the spring is given by Hooke's law, $^{2}$

$$
F _ {z} = - k z,\tag{8.11}
$$

where k is a constant called the spring constant. The negative sign produces a negative force (downward) when z is positive and vice versa, so that the force pushes the mass toward its equilibrium position. The harmonic oscillator is a model system that represents the mass on a spring. That is, it is a hypothetical system (existing only in our minds) which has some properties in common with the real system, but it is enough simpler to allow exact mathematical analysis. Our model system is defined by saying that the spring has no mass and that Eq. (8.11) is exactly obeyed, even if z has a large magnitude.

Replacement of $F$ by $md^2 z / dt^2$ according to Newton's second law gives the equation of motion for our harmonic oscillator:

$$
\frac {d ^ {2} z}{d t ^ {2}} + \frac {k}{m} z = 0.\tag{8.12}
$$

This differential equation has the properties:

1. It is called an ordinary differential equation because it contains only ordinary derivatives as opposed to partial derivatives.

2. It is linear, which means that the dependent variable z and its derivatives enter only to the first power.

3. It is homogeneous, which means that there are no terms that do not contain z.

4. It is second order, which means that the highest order derivative in the equation is a second derivative.

5. It has constant coefficients, which means that the quantities which multiply z and its derivatives are constants.

There are two important facts about linear homogeneous differential equations:

1. If $z_{1}(t)$ and $z_{2}(t)$ are two functions that satisfy the equation, then the linear combination $z_{3}(t)$ is also a solution, where

$$
z _ {3} (t) = c _ {1} z _ {1} (t) + c _ {2} z _ {2} (t)\tag{8.13}
$$

and $c_{1}$ and $c_{2}$ are constants. A linear combination is a sum of functions multiplied by constant coefficients.

2. If $z(t)$ satisfies the equation, then $cz(t)$ is also a solution, where c is a constant.

A linear homogeneous differential equation with constant coefficients can be solved by the following routine method:

1. Assume the trial solution

$$
z (t) = e ^ {\lambda t},\tag{8.14}
$$

where $\lambda$ is a constant. A trial solution is what the name implies. We try it by substituting it into the equation and produce an algebraic equation in $\lambda$ called the characteristic equation.

2. Find the values of $\lambda$ that satisfy the characteristic equation. For an equation of order n, there will be n values of $\lambda$ . Call these values $\lambda_{1}, \lambda_{2}, \ldots, \lambda_{n}$ . These values produce n versions of the trial solution that satisfy the equation.

3. Use fact (1) to write a solution

$$
z (t) = c _ {1} e ^ {\lambda_ {1} t} + c _ {2} e ^ {\lambda_ {2} t} + \dots + c _ {n} e ^ {\lambda_ {n} t}.\tag{8.15}
$$

EXAMPLE 8.2 Show that the differential equation

$$
a _ {3} \left(\frac {d ^ {3} y}{d x ^ {3}}\right) + a _ {2} \left(\frac {d ^ {2} y}{d x ^ {2}}\right) + a _ {1} \left(\frac {d y}{d x}\right) + a _ {0} y = 0\tag{8.16}
$$

can be satisfied by a trial solution $y = e^{\lambda x}$ .

SOLUTION ▶ We substitute the trial solution $y = e^{\lambda x}$ into the differential equation:

$$
a _ {3} \lambda^ {3} e ^ {\lambda x} + a _ {2} \lambda^ {2} e ^ {\lambda x} + a _ {1} \lambda^ {2} e ^ {\lambda x} + a _ {1} \lambda e ^ {\lambda x} + a _ {0} e ^ {\lambda x} = 0.\tag{8.17}
$$

If $x$ remains finite, we can divide by $e^{\lambda x}$ to obtain the characteristic equation:

$$
a _ {3} \lambda^ {3} + a _ {2} \lambda^ {2} + a _ {1} \lambda + a _ {0} = 0.\tag{8.18}
$$

If the constants $a_0, a_1, a_2$ , and $a_3$ are known, this is an equation that can be solved for three values of $\lambda$ which cause the trial solution to satisfy Eq. (8.16).

EXAMPLE 8.3 Solve the differential equation

$$
\frac {d ^ {2} y}{d x ^ {2}} + \frac {d y}{d x} - 2 y = 0.\tag{8.19}
$$

SOLUTION ▶ Substitution of the trial solution $y = e^{\lambda x}$ gives the characteristic equation

$$
\lambda^ {2} + \lambda - 2 y = 0.
$$

The solutions to this equation are

$$
\lambda = 1, \quad \lambda = - 2.
$$

The solution to the differential equation is thus

$$
y (x) = c _ {1} e ^ {x} + c _ {2} e ^ {- 2 x}.\tag{8.20}
$$

The solution to this example satisfies the differential equation no matter what values $c_{1}$ and $c_{2}$ have. It is actually a family of functions, one function for each set of values for $c_{1}$ and $c_{2}$ . A solution to a linear differential equation of order n that contains n arbitrary constants is known to be a general solution. A general solution is a family of functions which includes almost every solution to the differential equation. The solution of Eq. (8.20) is a general solution, since it contains two arbitrary constants. There is only one general solution to a differential equation. If you find two general solutions for the same differential equation that appear to be different, there must be some mathematical manipulations that will reduce both to the same form. A solution to a differential equation that contains no arbitrary constants is called a particular solution. A particular solution is usually one of the members of the general solution, but it might possibly be another function.

We are not finished with a problem when we find a general solution to a differential equation. We usually have additional information that will enable us to pick a particular solution out of the family of solutions. Such information consists of knowledge of boundary conditions and initial conditions. Boundary conditions arise from physical requirements on the solution, such as necessary conditions that apply to the boundaries of the region in space where the solution applies, or the requirement that the value of a physically measurable quantity must be a real number. Initial conditions arise from knowledge of the state of the system at some initial time.

We now solve the equation of motion for the harmonic oscillator, Eq. (8.12). We begin by finding the characteristic equation.

EXERCISE 8.1 ▶ Show that the characteristic equation for Eq. (8.12) for the harmonic oscillator is

$$
\lambda^ {2} + \frac {k}{m} = 0.\tag{8.21}
$$


The solution of the characteristic equation for the harmonic oscillator is

$$
\lambda = \pm i \left(\frac {k}{m}\right) ^ {1 / 2},\tag{8.22}
$$

where $i = \sqrt{-1}$ , the imaginary unit.

The general solution to Eq. (8.12) is therefore

$$
z = z (t) = c _ {1} \exp \left[ + i \left(\frac {k}{m}\right) ^ {1 / 2} t \right] + c _ {2} \exp \left[ - i \left(\frac {k}{m}\right) ^ {1 / 2} t \right],\tag{8.23}
$$

where $c_{1}$ and $c_{2}$ are arbitrary constants.

Our principal boundary condition is that the solution be real, because imaginary and complex numbers cannot represent physically measurable quantities like the position of the oscillator. From the trigonometric identity in Eq. (2.93) we can write

$$
z = c _ {1} \left[ \cos (\omega t) + i \sin (\omega t) \right] + c _ {2} \left[ \cos (\omega t) - i \sin (\omega t) \right],\tag{8.24}
$$

where we let

$$
\omega = \left(\frac {k}{m}\right) ^ {1 / 2}.
$$

If we let $c_{1} + c_{2} = b_{1}$ and $i(c_{1} - c_{2}) = b_{2}$ , then

$$
z = b _ {1} \cos (\omega t) + b _ {2} \sin (\omega t).\tag{8.25}
$$

Although the solutions in Eq. (8.23) and Eq. (8.25) look different, they are equivalent to each other. Since the sine and cosine of a real variable are real we can eliminate complex solutions by requiring that $b_{1}$ and $b_{2}$ be real.

EXERCISE 8.2 ▶

Show that the function of Eq. (8.25) satisfies Eq. (8.12).


Our new general solution applies to a particular harmonic oscillator if we use that oscillator's values of k and m to calculate the value of $\omega$ . We now require some conditions to make it apply to a particular case of motion. These conditions are initial conditions that specify the oscillator's position and velocity at some initial time. Say that we have the initial conditions at t = 0:

$$
z (0) = 0\tag{8.26a}
$$

$$
v _ {z} (0) = v _ {0}\tag{8.26b}
$$

where $v_{0}$ is a constant.

We require one initial condition to evaluate each arbitrary constant, so these two initial conditions will enable us obtain a particular solution for the case at hand. Knowledge of the position at time t = 0 without knowledge of the velocity at that time would not suffice, nor would knowledge of the velocity without knowledge of the position. For our initial conditions, $b_{1}$ must vanish:

$$
z (0) = b _ {1} \cos (0) + b _ {2} \sin (0) = b _ {1} = 0.\tag{8.27}
$$

The position is therefore given by

$$
z (t) = b _ {2} \sin (\omega t).\tag{8.28}
$$

The expression for the velocity is obtained by differentiation,

$$
v _ {2} (t) = \frac {d z}{d t} = b _ {2} \omega \cos (\omega t)\tag{8.29}
$$

so that

$$
v _ {z} (0) = b _ {2} \omega \cos (0) = b _ {2} \omega
$$

which gives

$$
b _ {2} = \frac {v _ {0}}{\omega}\tag{8.30}
$$

and gives us our particular solution

$$
z (t) = \left(\frac {v _ {0}}{\omega}\right) \sin (\omega t).\tag{8.31}
$$

The motion given by this solution is called uniform harmonic motion. It is a sinusoidal oscillation in time with a fixed frequency of oscillation. Figure 8.1 shows the position and the velocity of the suspended mass as a function of time. The motion is periodic, repeating itself over and over. During one period, the argument of the sine changes by $2\pi$ , so that if $\tau$ is the period (the length of time required for one cycle of the motion),

![[283575ba34d5eaf132cf02807d79c08d2e51edcee3c21b29a2b06299da624ecb.jpg]]  
Figure 8.1 ▶ The position and velocity of a harmonic oscillator as functions of time.

$$
2 \pi = \omega \tau = \left(\frac {k}{m}\right) ^ {1 / 2} \tau .\tag{8.32}
$$

Thus,

$$
\tau = 2 \pi \left(\frac {m}{k}\right) ^ {1 / 2}.\tag{8.33}
$$

The reciprocal of the period is called the frequency, denoted by v. (This is the Greek letter nu. Try not to confuse it with the letter “vee”).

$$
\nu = \frac {1}{2 \pi} \sqrt {\frac {k}{m}} = \frac {\omega}{2 \pi}\tag{8.34}
$$

The frequency gives the number of oscillations per second. The quantity $\omega$ is called the circular frequency. It gives the rate of change of the argument of the sine or cosine function in radians per second.

EXERCISE 8.3 ▶ The vibration of a diatomic molecule resembles that of a harmonic oscillator. Since both nuclei move, the mass must be replaced by the reduced mass,

$$
\mu = \frac {m _ {1} m _ {2}}{m _ {1} + m _ {2}},
$$

where $m_{1}$ is the mass of one nucleus and $m_{2}$ the mass of the other nucleus. $^{a}$ Calculate the frequency of vibration of a hydrogen chloride molecule. The force constant k is equal to $481 N m^{-1} = 481 J m^{2}$ . Be sure to use the mass of the nuclei in kilograms, not the mass of a mole of atoms.

The kinetic energy of the harmonic oscillator is

$$
\mathcal {K} = \frac {1}{2} m v _ {z} ^ {2}.\tag{8.35}
$$

In order for the force to be the negative derivative of the potential energy as in Eq. (7.63), the potential energy of the harmonic oscillator must be

$$
\mathcal {V} (z) = \frac {1}{2} k z ^ {2}.\tag{8.36}
$$

The total energy is the sum of the kinetic energy and the potential energy

$$
\begin{array}{r l} E & = \mathcal {K} + \mathcal {V} = \frac {1}{2} m v _ {0} ^ {2} \cos^ {2} (\omega t) + \frac {1}{2} k \left(\frac {v _ {0}}{\omega}\right) ^ {2} \sin^ {2} (\omega t) \\ & = \frac {1}{2} m v _ {0} ^ {2}, \end{array}\tag{8.37}
$$

where we have used the identity of Eq. (7) of Appendix B. As a harmonic oscillator moves, the total energy remains constant. As the kinetic energy rises and falls, the potential energy changes so that the total energy remains constant. When the energy is constant we say that the energy is conserved, and that the system is conservative. There is an important theorem of classical mechanics: If the forces on the particles of a system can be obtained from a potential energy function, the system will be conservative.

## The Damped Harmonic Oscillator—A Nonconservative System

We now discuss a damped harmonic oscillator, which is a harmonic oscillator that is subject to an additional force that is proportional to the velocity, such as a frictional force due to fairly slow motion of an object through a fluid,

$$
\mathbf {F} _ {f} = - \zeta \mathbf {v} = - \zeta \frac {d \mathbf {r}}{d t},\tag{8.38}
$$

where $\zeta$ is called the friction constant. Since this force cannot be derived from a potential energy, the system is not conservative and its energy will change with time.

The equation of motion is, for motion in the z direction

$$
F _ {z} = - \zeta \frac {d z}{d t} - k z = m \left(\frac {d ^ {2} z}{d t ^ {2}}\right).\tag{8.39}
$$

This equation is a linear homogeneous equation with constant coefficients, so a trial solution of the form of Eq. (8.14) will work. The characteristic equation is

$$
\lambda^ {2} + \frac {\zeta \lambda}{m} + \frac {k}{m} = 0.\tag{8.40}
$$

From the quadratic equation, the solutions of this equation are

$$
\begin{array}{l} \lambda_ {1} = - \frac {\zeta}{2 m} + \frac {\sqrt {(\zeta / m) ^ {2} - 4 k / m}}{2} \\ \lambda_ {2} = - \frac {\zeta}{2 m} - \frac {\sqrt {(\zeta / m) ^ {2} - 4 k / m}}{2} \end{array}\tag{8.41a}
$$

(8.41b)

and the general solution to the differential equation is

$$
z (t) = c _ {1} e ^ {\lambda_ {1} t} + c _ {2} e ^ {\lambda_ {2} t}.\tag{8.42}
$$

EXERCISE 8.4 ▶ Show that Eq. (8.40) is the correct characteristic equation, that Eq. (8.41a) gives the correct solutions to the characteristic equation, and that the function of Eq. (8.42) does satisfy Eq. (8.39).

## Greater than Critical Damping

There are three cases. In the first case, the quantity inside the square root in Eq. (8.41a) is positive, so that $\lambda_{1}$ and $\lambda_{2}$ are both real. This corresponds to a relatively large value of the friction constant $\zeta$ , and the case is called greater than critical damping. In this case, the mass at the end of the spring does not oscillate, but returns smoothly to its equilibrium position of z = 0 if disturbed from this position.

Figure 8.2 shows the position of a greater than critically damped oscillator as a function of time for a particular set of initial conditions.

![[472922474e8eeb031a0160648b149ccf208643cdc10823e41f4898e97538943b.jpg]]  
Figure 8.2 ▶ The position of a greater than critically damped harmonic oscillator as a function of time.

EXERCISE 8.5 ▶ From the fact that $\zeta$ , k, and m are all positive, show that $\lambda_{1}$ and $\lambda_{2}$ are both negative in the case of greater than critical damping, and from this fact, show that

$$
\lim _ {t \to \infty} z (t) = 0.\tag{8.43}
$$

## Less than Critical Damping

The next case is that of small values of $\zeta$ , or less than critical damping. If

$$
\left(\frac {\zeta}{m}\right) ^ {2} <   \frac {4 k}{m},
$$

the quantity inside the square root in Eq. (8.41a) is negative, and $\lambda_{1}$ and $\lambda_{2}$ are complex quantities,

$$
\lambda_ {1} = - \frac {\zeta}{2 m} + i \omega\tag{8.44}
$$

$$
\lambda_ {2} = - \frac {\zeta}{2 m} - i \omega ,\tag{8.45}
$$

where

$$
\omega = \sqrt {\frac {k}{m} - \left(\frac {\zeta}{2 m}\right) ^ {2}}.\tag{8.46}
$$

The solution thus becomes

$$
z (t) = \left(c _ {1} e ^ {i \omega t} + c _ {2} e ^ {i \omega t}\right) e ^ {- \zeta t / 2 m}\tag{8.47}
$$

which can also be written in a form that is similar to Eq. (8.25),

$$
z (t) = \left[ b _ {1} \cos (\omega t) + b _ {2} \sin (\omega t) \right] e ^ {- \zeta t / 2 m}.\tag{8.48}
$$

This shows $z(t)$ to be an oscillatory function times an exponentially decreasing function, giving the “ringing” behavior shown in Fig. 8.3.

![[5f2d65ee52eef2dd2e8566eed48a5d661a4da7a548c96108e3fe20d79aad334b.jpg]]  
Figure 8.3 ▶ The position of a less than critically damped oscillator as a function of time for the initial conditions $z(0) = z_{0}$ , $v_{z}(0) = 0$ .

EXERCISE 8.6 ▶ If the position of the oscillator at time 0 is a particular value $z(0) = z_0$ and if the velocity at time zero is a particular value $v_z(0) = v_0$ , express the constants $b_1$ and $b_2$ in terms of these values.

## Critical Damping

The final case is that of critical damping, in which the quantity inside the square root in Eq. (8.41) exactly vanishes. This case is not likely to happen by chance, but it is possible to construct an oscillating object such as a galvanometer mirror or a two-pan balance beam that is critically damped by a magnetic field. The condition for critical damping is

$$
\left(\frac {\zeta}{2 m}\right) ^ {2} = \frac {k}{m}.\tag{8.49}
$$

An interesting thing happens to the solution of Eq. (8.42) in the case of critical damping. The values of $\lambda$ are equal to each other,

$$
\lambda_ {1} = \lambda_ {2} = - \frac {\zeta}{2 m}\tag{8.50}
$$

so that Eq. (8.42) becomes

$$
z (t) = (c _ {1} + c _ {2}) e ^ {\lambda t} = c e ^ {\lambda t},\tag{8.51}
$$

where c is the sum of the two constant $c_{1}$ and $c_{2}$ and where we drop the subscript on $\lambda$ . This is not a general solution, since a general solution for a second order linear equation must contain two arbitrary constants, and a sum of two constants does not constitute two separate constants. This is called linear dependence. With two functions, linear dependence means that the functions are proportional to each other, so that they are not distinct solutions. If we have several solutions, they are linearly dependent if one or more of the solutions equals a linear combination of the others.

Since we do not have a general solution, there must be another family of solutions that is not included in the solution of Eq. (8.51). One way to find it is by attempting additional trial functions until we find one that works. The one that works is

$$
z (t) = t e ^ {\lambda t}.\tag{8.52}
$$

EXERCISE 8.7 ▶ Substitute the trial solution of Eq. (8.52) into Eq. (8.39), using the condition of Eq. (8.49) to restrict the discussion to critical damping, and show that the equation is satisfied.

Our general solution is now

$$
z (t) = (c _ {1} + c _ {2} t) e ^ {\lambda t},\tag{8.53}
$$

where we drop the subscript on $\lambda$ . The velocity is given by

$$
v _ {z} (t) = \frac {d z}{d t} = c _ {1} \lambda e ^ {\lambda t} + c _ {2} e ^ {\lambda t} + c _ {2} t \lambda e ^ {\lambda t}
$$

For any particular set of initial conditions, we can find the appropriate values of $c_{1}$ and $c_{2}$ . The behavior of a critically damped oscillator is much the same as that of Fig. 8.2.

EXAMPLE 8.4 Consider a critically damped oscillator with $\lambda = -1.00\mathrm{s}^{-1}$ . Assume that its initial position is $z(0) = 0.00\mathrm{m}$ and that its initial velocity is $1.00\mathrm{ms}^{-1}$ . Find its position and velocity at $t = 1.00\mathrm{s}$ .

SOLUTION ▶ In order for $z(0)$ to equal 0.00 m, we must require that $c_{1} = 0.00$ m. The velocity is given by

$$
v _ {z} (t) = c _ {2} e ^ {\lambda t} + c _ {2} t \lambda e ^ {\lambda t}
$$

The velocity at $t = 0$ is

$$
v _ {z} (0) = c _ {2}
$$

so that

$$
c _ {2} = 1.00 \mathrm{ms} ^ {- 1}
$$

The position at $t = 1.00 \, \mathrm{s}$ is

$$
z (1.00 \mathrm{s}) = c _ {2} t e ^ {\lambda t} = (1.00 \mathrm{ms} ^ {- 1}) (1.00 \mathrm{s}) e ^ {- 1.00} = 0.368 \mathrm{m}
$$

![[d0adfa685d69f59de2ed261dd49696aec701bc421a9a3540b7892dcf9dd9acc3.jpg]]

(a) Construct an accurate graph of the position of the critically damped oscillator of the previous example.

(b) Locate the time at which z attains its maximum value and find the maximum value.

EXERCISE 8.9 ▶ Find a formula for the position of the critically damped oscillator of the previous example if the initial position is $z(0) = 0.500 \, \text{m}$ and $v_{z}(0) = 0.00 \, \text{s}$ . Find the velocity and the position of the oscillator at $t = 1.00 \, s$ .

## The Forced Harmonic Oscillator: Inhomogeneous Linear Differential Equations

An inhomogeneous differential equation contains a term that is not proportional to the unknown function or to any of its derivatives. An example of a linear inhomogeneous equation is

$$
f _ {3} (t) \frac {d ^ {3} z}{d t ^ {3}} + f _ {2} (t) \frac {d ^ {2} z}{d t ^ {2}} + f _ {1} (t) \frac {d z}{d t} = g (t),\tag{8.54}
$$

where $f_{3}$ $f_{2}$ , $f_{1}$ , and g are some functions of time but do not depend on z. The term $g(t)$ is the inhomogeneous term. If an external force exerted on a harmonic oscillator depends only on the time, the equation of motion is an inhomogeneous differential equation:

$$
\frac {d ^ {2} z}{d t ^ {2}} + \frac {k}{m} z = \frac {F (t)}{m},\tag{8.55}
$$

where $F(t)$ is the external time-dependent force and the term $F(t)/m$ is the inhomogeneous term.

A method for solving such an equation is:

Step 1. Solve the equation obtained by deleting the inhomogeneous term. This homogeneous equation is called the complementary equation, and the general solution to this equation is called the complementary function.

Step 2. Find a particular solution to the inhomogeneous equation by whatever means may be necessary.

Step 3. Take the sum of the complementary function and this particular solution. This is the general solution to the inhomogeneous equation.

EXERCISE 8.10 ▶ If $z_{c}(t)$ is a general solution to the complementary equation and $z_{p}(t)$ is a particular solution to the inhomogeneous equation, show that $z_{c} + z_{p}$ is a solution to the inhomogeneous equation of Eq. (8.54).

## Variation of Parameters Method

There is a method for finding a particular solution to a linear inhomogeneous equation, known as the variation of parameters. If the inhomogeneous term is a power of t, an exponential, a sine, a cosine, or a combination of these functions, this method can be used. One proceeds by taking a suitable trial function that contains parameters (constants whose values need to be determined). This is substituted into the inhomogeneous equation and the values of the parameters are found so that the inhomogeneous equation is satisfied. Table 8.1 gives a list of suitable trial functions for various inhomogeneous terms.

EXAMPLE 8.5 Let us assume that the external force on a forced harmonic oscillator is

$$
F (t) = F _ {0} \sin (\alpha t),\tag{8.56}
$$

where $F_{0}$ and $\alpha$ are constants. Find the general solution to the equation of motion.

SOLUTION ▶ Use of Table 8.1 and determination of the parameters gives the particular solution

$$
z _ {p} (t) = \frac {F _ {0}}{m (\omega^ {2} - \alpha^ {2})} \sin (\alpha t),\tag{8.57}
$$

where $\omega$ is the circular frequency in the solution of Eq. (8.25), which is the solution to the complementary equation. The general solution is

$$
z (t) = b _ {1} \cos (\omega t) + b _ {2} \sin (\omega t) + z _ {p} (t),\tag{8.58}
$$

where the constants $b_{1}$ and $b_{2}$ are to be determined by the initial conditions. Let us assume that $z(0) = 0$ , so that

$$
z (t) = b _ {2} \sin (\omega t) + \frac {F _ {0}}{m (\omega^ {2} - \alpha^ {2})} \sin (\alpha t).\tag{8.59}
$$

EXERCISE 8.11 ▶

Verify Eq. (8.57) and (8.58).


TABLE 8.1 ▶ Particular Trial Solutions for the Variation of Parameters Method\*

<table><tr><td>Inhomogeneous Term</td><td>Trial Solution</td><td>Forbidden Characteristic Root $^{\dagger}$ </td></tr><tr><td>1</td><td>A</td><td>0</td></tr><tr><td> $t^n$ </td><td> $A_0 + A_1t + A_2t^2 + \cdots + A_nt^n$ </td><td>0</td></tr><tr><td> $e^{\alpha t}$ </td><td> $Ae^{\alpha t}$ </td><td>α</td></tr><tr><td> $t^n e^{\alpha t}$ </td><td> $e^{\alpha t}(A_0 + A_1t + A_2t^2 + \cdots + A_nt^n)$ </td><td>α</td></tr><tr><td> $e^{\alpha t}\sin(\beta t)$ </td><td> $e^{\alpha t}[A\cos(\beta t) + B\sin(\beta t)]$ </td><td>α, β</td></tr><tr><td> $e^{\alpha t}\cos(\beta t)$ </td><td> $e^{\alpha t}[A\cos(\beta t) + B\sin(\beta t)]$ </td><td>α, β</td></tr></table>

\* Source: M. Morris and O. E. Brown, Differential Equations, 3rd ed., Prentice-Hall, Englewood Cliffs, N.J., 1952.

$A, B, A_{0}, A_{1}$ , etc., are parameters to be determined. $\alpha$ and $\beta$ are constants in the differential equation to be solved.

The motion of the forced harmonic oscillator shows some interesting features. The solution in the previous example is a linear combination of the natural motion and a motion proportional to the external force. If the frequencies of these are not very different, a motion such as shown in Fig. 8.4, known as beating, can result. There is a periodic variation of the amplitude of vibration with a circular frequency equal to $\omega - \alpha$ . You can hear this beating when a piano is being tuned. There are two or three string for each note, and they are tuned separately. Each string can excite a “sympathetic vibration” in the other, which acts as an external force. When the frequencies of two strings are slightly different you can hear a pulsation like that in Fig. 8.4.

![[e137d7d01dee2bed1a4c7369eb6d7b7f5eac13db0b0ae1bf18765a1100a0bf22.jpg]]  
Figure 8.4 ▶ The position of a forced harmonic oscillator as a function of time for the case $\alpha = 1.1\omega$ .

## 8.3 Differential Equations with Separable Variables

In this section, we discuss equations that can be manipulated algebraically into the form

$$
g (y) \frac {d y}{d x} = f (x),\tag{8.60}
$$

where $g(y)$ is some integrable function of y and $f(x)$ is some integrable function of x. To solve Eq. (8.60), we multiply both sides of the equation by dx and use Eq. (4.20):

$$
{\frac {d y}{d x}} d x = d y.\tag{8.61}
$$

We now have

$$
g (y) d y = f (x) d x.\tag{8.62}
$$

If we have manipulated the equation into the form of Eq. (8.62), we say that we have separated the variables, because we have no x dependence in the left-hand side of the equation and no y dependence in the right-hand side. We can perform an indefinite integration on both sides of this equation to obtain

$$
\int g (y) d y = \int f (x) d x + C,\tag{8.63}
$$

where C is a constant of integration. We can alternatively do a definite integration

$$
\int_ {y _ {1}} ^ {y _ {2}} g (y) d y = \int_ {x _ {1}} ^ {x _ {2}} f (x) d x,\tag{8.64}
$$

where

$$
\begin{array}{r l} & y _ {1} = y (x _ {1}) \\ & y _ {2} = y (x _ {2}). \end{array}
$$

EXAMPLE 8.6 In a first-order chemical reaction with no back reaction, the concentration of the reactant is governed by

$$
- \frac {d c}{d t} = k c,\tag{8.65}
$$

where c is the concentration of the single reactant, t is the time, and k is a function of temperature called the rate constant. Solve the equation to find c as a function of t.

SOLUTION ▶ We divide by c and multiply by dt to separate the variables:

$$
\frac {1}{c} \frac {d c}{d t} d t = \frac {1}{c} d c = - k d t.
$$

We perform an indefinite integration

$$
\int {\frac {1}{c}} d c = \ln (c) = - k \int d t + C = - k t + C,\tag{8.66}
$$

where C is a constant of integration. Although each indefinite integration would require a constant of integration, we include only one constant, since the second constant of integration could be moved to the other side of the equation, giving the difference of two constants, which equals a constant.

We take the exponential of each side of Eq. (8.66) to obtain

$$
e ^ {\ln (c)} = c = e ^ {\hat {C}} e ^ {- k t} = c (0) e ^ {- k t}.\tag{8.67}
$$

In the last step, we recognized that $e^{C}$ had to equal the concentration at time t = 0. A definite integration can be carried out instead of an indefinite integration:

$$
\int_ {c (0)} ^ {c (t _ {1})} \frac {1}{c} d c = \ln \left(\frac {c (t _ {1})}{c (0)}\right) = - k \int_ {0} ^ {t _ {1}} d t = - k t _ {1}.
$$

This equation is the same as Eq. (8.67) except that the time is now called $t_{1}$ instead of t. The limits on the two definite integrations must be done correctly. If the lower limit of the time integration is zero, the lower limit of the concentration integration must be the value of the concentration at zero time. The upper limit is similar.

EXERCISE 8.12 ▶ In a second-order chemical reaction involving one reactant and having no back reaction,

$$
- \frac {d c}{d t} = k c ^ {2}.
$$

Solve this differential equation by separation of variables. Do a definite integration from t = 0 to $t = t_{1}$ .

If you are faced with a differential equation and if you think that there is some chance that separation of variables will work, try the method. If it doesn't work you haven't lost very much time since the method is quite rapid.

## 8.4 Exact Differential Equations

Sometimes you might be faced with an equation that can be manipulated into the pfaffian form:

$$
M (x, y) d x + N (x, y,) d y = 0.\tag{8.68}
$$

Some such differential forms are exact, which means that they are differentials of functions. Other differentials are inexact, which means that they are not differentials of functions. If the differential is exact, the equation is called an exact differential equation.

The test for exactness is based on the Euler reciprocity relation, as in Eq. (7.31): If

$$
\left(\frac {\partial M}{\partial y}\right) _ {x} = \left(\frac {\partial N}{\partial x}\right) _ {y},\tag{8.69}
$$

then the differential is exact. If the differential equation is exact, there is a function $f(x, y)$ such that

$$
d f = M (x, y) d x + N (x, y) d y = 0,\tag{8.70}
$$

which implies that

$$
f (x, y) = C,\tag{8.71}
$$

where C is a constant, because a constant function has a differential that vanishes. This equation can be solved for y in terms of x, providing a solution to the differential equation.

In Chapter 7 we discussed the procedure for finding the function in Eq. (8.71) by using a line integral,

$$
f (x _ {1}, y _ {1}) = f (x _ {0}, y _ {0}) + \int_ {c} d f,\tag{8.72}
$$

where C is a curve beginning at $(x_{0}, y_{0})$ and ending at $(x_{1}, y_{1})$ . A convenient curve is the rectangular path from $(x_{0}, y_{0})$ to $(x_{1}, y_{0})$ and then to $(x_{1}, y_{1})$ . On the first part of this path, y is constant at $y_{0}$ , so the dy integral vanishes and y is replaced by $y_{0}$ in the dx integral. On the second part of the path, x is constant at $x_{1}$ , so the dx integral vanishes and x is replaced by $x_{1}$ in the dy integral:

$$
f (x _ {1}, y _ {1}) = f (x _ {0}, y _ {0}) + \int_ {x _ {0}} ^ {x _ {1}} M (x, y _ {0}) d x + \int_ {y _ {0}} ^ {y _ {1}} N (x _ {1}, y) d y.\tag{8.73}
$$

Both integrals are now ordinary integrals, so we have a solution if we can perform the integrals. The solution will contain an arbitrary constant, because different constants can be added to $f(x_{1}, y_{1})$ and $f(x_{0}, y_{0})$ in Eq. (8.73) without changing the equality.

EXAMPLE 8.7 Solve the differential equation

$$
2 x y d x + x ^ {2} d y = 0.
$$

SOLUTION ▶ The equation is exact, because

$$
\frac {\partial}{\partial_ {y}} (2 x y) = 2 x \quad \text { and } \quad \frac {\partial}{\partial_ {x}} (x ^ {2}) = 2 x.
$$

We do a line integral from $(x_0, y_0)$ to $(x_1, y_0)$ and then to $(x_0, y_1)$ , letting $f(x, y)$ be the function whose differential must vanish:

$$
\begin{array}{r c l} 0 & = & f (x _ {1}, y _ {1}) - f (x _ {0}, y _ {0}) = \int_ {x _ {0}} ^ {x _ {1}} 2 x y _ {0} d x + \int_ {y _ {0}} ^ {y _ {1}} x _ {1} ^ {2} d y \\ & = & y _ {0} x _ {1} ^ {2} - y _ {0} x _ {0} ^ {2} + x _ {1} ^ {2} y _ {1} - x _ {1} ^ {2} y _ {0} \\ & = & x _ {1} ^ {2} y _ {1} - x _ {0} ^ {2} y _ {0}. \end{array}
$$


We regard $x_0$ and $y_0$ as constants so that $x_0^2 y_0 = C$ , where $C$ is a constant. We drop the subscripts on $x_1$ and $y_1$ , and write

$$
f (x, y) = x ^ {2} y = C.
$$

Our general solution is $y = C/x^{2}$ . Some condition would have to be specified to obtain the value of the constant C.

EXERCISE 8.13 ▶
the equation.

Show that the solution in the previous example satisfies


EXERCISE 8.14 ▶

Solve the equation $(4x + y)dx + xdy = 0$ .


## 8.5 Solution of Inexact Differential Equations by the Use of Integrating Factors

If we have an inexact pfaffian differential equation

$$
M (x, y) d x + N (x, y) d y = 0\tag{8.74}
$$

we cannot use the method of the previous section. However, some inexact differentials yield an exact differential when multiplied by a function known as an integrating factor. If the function $g(x, y)$ is an integrating factor for the differential in Eq. (8.74),

$$
g (x, y) M (x, y) d x + g (x, y) N (x, y) d y = 0\tag{8.75}
$$

is an exact differential equation that can be solved by the method of the previous section. A solution for Eq. (8.75) will also be a solution for Eq. (8.74).

EXAMPLE 8.8 Solve the differential equation

$$
{\frac {d y}{d x}} = {\frac {y}{x}}.
$$

SOLUTION ▶ We convert the equation to the pfaffian form, y dx - x dy = 0. Test for exactness:

$$
\begin{array}{r l} \left(\frac {\partial_ {y}}{\partial_ {y}}\right) _ {x} & = 1 \\ \left[ \frac {\partial (- x)}{\partial x} \right] _ {y} & = - 1. \end{array}
$$

The equation is not exact. We show that $1 / x^2$ is an integrating factor. Multiplication by this factor gives

$$
\left(\frac {y}{x ^ {2}}\right) d x - \left(\frac {1}{x}\right) d y = 0.\tag{8.76}
$$

This is exact:

$$
\left[ \frac {\partial (y / x ^ {2})}{\partial y} \right] _ {x} = \frac {1}{x ^ {2}}
$$

$$
\left[ \frac {\partial (- 1 / x)}{\partial x} \right] _ {y} = \frac {1}{x ^ {2}}.
$$

We can solve Eq. (8.76) by the method of Section 8.4:

$$
\begin{array}{r l} 0 & = \int_ {x _ {0}} ^ {x _ {1}} \left(\frac {y _ {0}}{x ^ {2}}\right) d x - \int_ {y _ {0}} ^ {y _ {1}} \left(\frac {1}{x _ {1}}\right) d y \\ & = - y _ {0} \left(\frac {1}{x _ {1}} - \frac {1}{x _ {0}}\right) - \frac {1}{x _ {1}} (y _ {1} - y _ {0}) = \frac {y _ {0}}{x _ {0}} - \frac {y _ {1}}{x _ {1}}. \end{array}
$$

We regard $x_0$ and $y_0$ as constants, so that

$$
\frac {y}{x} = \frac {y _ {0}}{x _ {0}} = C,
$$

where C is a constant. We solve for y in terms of x to obtain the solution

$$
y = C x.
$$

This is a general solution, since the original equation was first order and the solution contains one arbitrary constant.

If an inexact differential has one integrating factor, it has an infinite number of integrating factors. Therefore, there can be other integrating factors for a differential such as the one in the preceding example. Unfortunately, there is no general procedure for finding an integrating factor except by trial and error.

EXERCISE 8.15 ▶ Show that $1/y^{2}$ and $1/(x^{2}+y^{2})$ are integrating factors for the equation in the previous example and show that they lead to the same solution.

## 8.6 Partial Differential Equations: Waves in a String

Differential equations that contain partial derivatives of several independent variables are called partial differential equations. The differential equations that we have been discussing contain ordinary derivatives and are called ordinary differential equations. Ordinary differential equations occur that contain more than one dependent variable, but you must have one equation for each dependent variable and must solve them simultaneously. We will not discuss simultaneous differential equations, but you can read about such equations in some of the books listed at the end of the book, and Mathematica is capable of solving simultaneous differential equations.

![[fbb744846a0654f2d38a8046dd5963d1262bdfbdbcf6f3df9be37e1c17d37a3c.jpg]]  
Figure 8.5 ▶ A flexible string.

We discuss only a rather simple method of solving a partial differential equation, devoting most of this section to an example, the classical equation of motion of a flexible string of length L. There are important similarities between this equation and the Schrödinger equation $^{3}$ of quantum mechanics. The flexible string that we discuss is a model system that is simpler than a real string. It is defined by the following: (1) It is completely flexible, so that no force is required to bend the string. (2) Its motion is restricted to small vibrations, so that the string is not appreciably stretched. (3) Both ends of the string are fixed in position. Figure 8.5 shows the string. We choose one end of the string as our origin of coordinates and use the equilibrium (straight) position of the string as our x axis. The displacement of the string from its equilibrium position in the y direction is denoted by y and the displacement in the z direction is denoted by z. Since the string moves, y and z are functions of time as well as of x:

$$
y = y (x, t)\tag{8.77}
$$

$$
z = z (x, t).\tag{8.78}
$$

The equation of motion of the string is derived by writing Newton's second law for a small segment of the string and taking a mathematical limit as the length of the segment becomes infinitesimal. We do not present the derivation. $^{4}$ The result is a partial differential equation

$$
\left(\frac {\partial^ {2} y}{\partial t ^ {2}}\right) = \frac {T}{\rho} \left(\frac {\partial^ {2} y}{\partial x ^ {2}}\right) = c ^ {2} \left(\frac {\partial^ {2} y}{\partial x ^ {2}}\right)\tag{8.79}
$$

and a similar equation for z. In this equation T is the magnitude of the tension force on the string and $\rho$ is the mass of the string per unit length. The quantity c turns out to be the speed of propagation of a wave along the string.

$$
c = \sqrt {\frac {T}{\rho}}
$$

Since the two equations are independent of each other, we can solve for y and z separately, and the two general solutions will be identical except for the symbol used for the dependent variable.

## Solution by Separation of Variables

We do not seek a general solution for Eq. (8.79). but seek only a family of solutions that can be written as a product of factors, each of which depends on only one variable:

$$
y (x, t) = \psi (x) \theta (t).\tag{8.80}
$$

This is called a solution with the variables separated. We regard it as a trial solution and substitute it into the differential equation to see if it works. This method of separation of variables is slightly different from the previous version, since we are now separating two independent variables instead of one independent variable and one dependent variable.

Since $\psi$ does not depend on t and $\theta$ does not depend on x, the result of substituting the trial solution into the Eq. (8.79) is

$$
\psi (x) \left(\frac {d ^ {2} \theta}{d t ^ {2}}\right) = c ^ {2} \theta (t) \left(\frac {d ^ {2} \psi}{d x ^ {2}}\right).\tag{8.81}
$$

We write ordinary derivatives since we now have functions of only one variable. We separate the variables by manipulating Eq. (8.81) into a form in which one term contains no $x$ dependence and the other term contains no $t$ dependence, just as we manipulated Eq. (8.59) into a form with only one variable in each term. We divide both sides of Eq. (8.81) by the product $\psi(x)\theta(t)$ . We also divide by $c^2$ , but this is not essential.

$$
{\frac {1}{c ^ {2} \theta (t)}} {\frac {d ^ {2} \theta}{d t ^ {2}}}. = {\frac {1}{\psi (x)}} {\frac {d ^ {2} \psi}{d x ^ {2}}}\tag{8.82}
$$

The variables are now separated, since each term contains only one independent variable.

We now use the fact that x and t are both independent variables. If we temporarily keep t fixed at some value, we can still allow x to vary. The function of x on the right-hand side of Eq. (8.82) must be a constant function of x, because it equals a quantity that we can keep fixed while allowing x to range:

$$
\frac {1}{\psi (x)} \frac {d ^ {2} \psi}{d x ^ {2}} = - \kappa^ {2} = \text { constant }.\tag{8.83}
$$

For the same reason, the left-hand side is a constant function of t,

$$
\frac {1}{c ^ {2} \theta (t)} \frac {d ^ {2} \theta}{d t ^ {2}} = - \kappa^ {2}.\tag{8.84}
$$

We denote the constant by the symbol $-\kappa^{2}$ because this will make $\kappa$ real. We now multiply Eq. (8.83) by $\psi(x)$ and multiply Eq. (8.84) by $c^{2}\theta(t)$ . We obtain

$$
\frac {d ^ {2} \psi}{d x ^ {2}} + \kappa^ {2} \psi = 0\tag{8.85}
$$

and

$$
\frac {d ^ {2} \theta}{d t ^ {2}} + \kappa^ {2} c ^ {2} \theta = 0.\tag{8.86}
$$

The separation of variables is complete, and we have two ordinary differential equations. Except for the symbols used, both of these equations are the same as

Eq. (8.12). We transcribe the solution to that equation with appropriate changes in symbols:

$$
\psi (x) = a _ {1} \cos (\kappa x) + a _ {2} \sin (\kappa x)\tag{8.87}
$$

$$
\theta (t) = b _ {1} \cos (\kappa c t) + b _ {2} \sin (\kappa c t).\tag{8.88}
$$

These are general solutions to the ordinary differential equations of Eq. (8.85) and (8.86), but we do not necessarily have a general solution to our partial differential equation, because there can be solutions that are not of the form of Eq. (8.80).

We are now ready to consider a specific case. We consider a string of length L with the ends fixed, as in Fig. 8.5. We have the condition that y = 0 at x = 0 and at x = L. These conditions are called boundary conditions, and literally arise from a condition at the boundaries of a region. If y must vanish at x = 0 and at x = L, then $\psi$ must vanish at these points, since the factor $\theta$ does not necessarily vanish:

$$
\psi (0) = 0\tag{8.89}
$$

and

$$
\psi (L) = 0.\tag{8.90}
$$

Equation (8.89) requires that

$$
a _ {1} = 0\tag{8.91}
$$

since $\cos(0)=1$ . Equation (8.90) requires that the argument of the sine function in Eq. (8.87) be equal to some integer times $\pi$ for x=L, because

$$
\sin (n \pi) = 0 \quad (n = 0, 1, 2, \dots).\tag{8.92}
$$

Therefore,

$$
\kappa = \frac {n \pi}{L} (n = 1, 2, 3, \dots).\tag{8.93}
$$

We are not interested in the case that n = 0, because this corresponds to a stationary string at its equilibrium position.

The coordinate factor $\psi$ in our solution is now

$$
\psi (x) = a _ {2} \sin \left(\frac {n \pi x}{L}\right).\tag{8.94}
$$

We return to the time-dependent factor $\theta$ . We apply initial conditions that make our solution apply to a particular case. Let us consider the case that at t = 0, the string is passing through its equilibrium position, which corresponds to y = 0 for all x. If so, then $b_{1} = 0$ since $\cos(0) = 1$ . We now have

$$
\theta = b _ {2} \sin \left(\frac {n \pi c t}{L}\right)
$$

and

$$
y (x, t) = A \sin \left(\frac {n \pi x}{L}\right) \sin \left(\frac {n \pi c t}{L}\right),\tag{8.95}
$$

where we write $A = a_{2}b_{2}$ since the product of two constants is really just one constant. The maximum amplitude is A, and another initial condition would be required to specify its value.

We have a set of solutions, one for each value of the integer n. Figure 8.6 shows the function $\psi(x)$ for several values of n. Each curve represents the shape of the string at an instant when $\theta = 1$ . At other times, the string is vibrating between such a position and a position given by $-\psi(x)$ . There are fixed points at which the string is stationary. These points are called nodes, and the number of nodes other than the two nodes at the ends of the string is n - 1. A wave with stationary nodes is called a standing wave.

![[79a4b41b61c612eb098ca216e838494857e2011c26b7eb81b0d6bdde1e45218f.jpg]]  
Figure 8.6 ▶ Standing waves in a flexible string.

If we let $\lambda$ be the wavelength, or the distance for the sine function in $\psi$ to go through a complete period, then

$$
n \lambda = 2 L.\tag{8.96}
$$

The period of oscillation is the time required for the sine function in the factor $\theta$ to go through a complete oscillation and return the string to its original position and velocity, which requires the argument of the sine function to range through $2\pi$ . If $\tau$ is the period,

$$
\frac {n \pi c \tau}{L} = 2 \pi ; \quad \tau = \frac {2 L}{n c}.\tag{8.97}
$$

The frequency $\nu$ is the reciprocal of the period:

$$
\nu = \frac {n c}{2 L} = \left(\frac {n}{2 L}\right) \left(\frac {T}{\rho}\right) ^ {1 / 2}.\tag{8.98}
$$

In musical acoustics, the oscillation corresponding to n = 1 is called the fundamental, that for n = 2 is the first overtone, etc. The fundamental is also called the first harmonic, the first overtone is called the second harmonic, and so on.

EXERCISE 8.16 ▶ A certain violin string has a mass per unit length of $20.00 \, mg cm^{-1}$ and a length of 55 cm. Find the tension force necessary to make it produce a fundamental tone of A above middle C (440 oscillations per second = 440 Hz).

When a string in a musical instrument is struck or bowed, it will usually not vibrate according to a single harmonic. The following Fourier series is a linear combination that satisfies Eq. (8.79) and can represent any possible motion of the string:

$$
y (x, t) = \sum_ {n = 1} ^ {\infty} \sin \left(\frac {n \pi x}{L}\right) \left[ a _ {n} \cos \left(\frac {n \pi c t}{L}\right) + b _ {n} \sin \left(\frac {n \pi c t}{L}\right) \right].\tag{8.99}
$$

The fact that a linear combination of solutions can be a solution to the equation is an example of the principle of superposition. We can regard the linear combination as a physical representation of constructive and destructive interference of the different harmonics. The strengths of the different harmonics are represented by the values of the coefficients $a_{n}$ and $b_{n}$ . Different musical instruments have different relative strengths of different harmonics.

EXERCISE 8.17 ▶

Show that the function in Eq. (8.99) satisfies Eq. (8.79).


EXERCISE 8.18 For a string of finite length with fixed ends, only standing waves can occur. For an infinitely long string, traveling waves can also occur. The following is a traveling wave:

$$
y (x, t) = A \sin [ k (x - c t) ].\tag{8.100}
$$

Show that the function of Eq. (8.100) satisfies Eq. (8.79).


We can show that the function of Eq. (8.100) is a traveling wave by showing that a node in the wave moves along the string. When t = 0, there is a node at x = 0. At a later time, this node is located at a value of x such that $k(x - ct)$ is still equal to zero. At a time t, x = ct at the node, so that the speed of the wave is equal to c. The traveling wave solution in Eq. (8.100) is not a solution in which the variables are separated. However, using Eq. (14) of Appendix B, we can show that

$$
A \sin [ k (x - c t) ] = A [ \sin (k x) \cos (k c t) - \cos (k x) \sin (k c t) ].\tag{8.101}
$$

This equation exhibits the fact that a traveling wave is equivalent to two standing waves interfering with each other.

EXERCISE 8.19 ▶ Find the speed of propagation of a traveling wave in an infinite string with the same mass per unit length and the same tension force as the violin string in Exercise 8.16.

## 8.7 Solution of Differential Equations with Laplace Transforms

Some differential equations can be solved by taking the Laplace transform of the equation, applying some of the theorems presented in Section 6.5 to obtain an expression for the Laplace transform of the unknown function, and then finding the inverse transform. We illustrate this procedure with the differential equation for the damped harmonic oscillator, $^{5}$ Eq. (8.39), which can be rewritten

![[663bf6b6f9d7b211d164c99a5b5d81927bbc48b212e95b252d00a810bc21e112.jpg]]

$$
\left(\frac {d ^ {2} z}{d t ^ {2}}\right) + \frac {\zeta}{m} \frac {d z}{d t} + \frac {k}{m} z = z ^ {\prime \prime} + \frac {\zeta}{m} z ^ {\prime} + \frac {k}{m} z = 0.\tag{8.102}
$$

We introduce the notation $z''$ for the second derivative $d^{2}z/dt^{2}$ and $z'$ for the first derivative dz/dt. We take the Laplace transform of this equation, applying Eq. (6.72) and the n = 2 version of Eq. (6.73), to express the Laplace transforms of the first and second derivatives. We let Z be the Laplace transform of z,

$$
s ^ {2} Z - s z (0) - z ^ {\prime} (0) + \frac {\zeta}{m} (s Z - z (0)) + \frac {k}{m} Z = 0.\tag{8.103}
$$

This algebraic equation is solved for $Z$ :

$$
Z = \frac {s z (0) + z ^ {\prime} (0) + (\zeta / m) z (0)}{s ^ {2} + (\zeta / m) s + k / m}.\tag{8.104}
$$

When we find the inverse transform of this function, we will have our answer. We must carry out some algebraic manipulations before we can find the inverse transforms in Table 6.1. In order to match an expression for a transform in Table 6.1, we complete the square in the denominator (that is, we add a term so that we have a perfect square plus another term):

$$
Z = \frac {z (0) (s + \zeta / 2 m) + \zeta / 2 m + z ^ {\prime} (0)}{(s ^ {2} + \zeta / 2 m) ^ {2} - \zeta^ {2} / 4 m ^ {2} + k / m}.\tag{8.105}
$$

We have also expressed the numerator in terms of the quantity that is squared in the denominator. We now make the substitutions,

$$
a = \frac {\zeta}{2 m} \quad \mathrm{and} \quad \omega^ {2} = \frac {k}{m} - \frac {\zeta^ {2}}{4 m ^ {2}}
$$

so that Eq. (8.105) can be written

$$
Z = \frac {z (0) (s + a)}{(s ^ {2} + a) ^ {2} + \omega^ {2}} + \frac {z (0) a + z ^ {\prime} (0)}{(s ^ {2} + a) ^ {2} + \omega^ {2}}.\tag{8.106}
$$

We assume the case of less than critical damping, so that $\omega^{2}$ is positive.

From Table 6.1, we have the inverse transforms,

$$
\begin{array}{l} \mathcal {L} ^ {- 1} \left\{\frac {s}{s ^ {2} + \omega^ {2}} \right\} = \cos (\omega t) \\ \mathcal {L} ^ {- 1} \left\{\frac {s}{s ^ {2} + \omega^ {2}} \right\} = \sin (\omega t) \end{array}
$$

and from the theorem of Eq. (6.71)

$$
\mathcal {L} ^ {- 1} \left\{e ^ {- a t} f (t) \right\} = F (s + a)\tag{8.107}
$$

so that

$$
z (t) = \left[ z (0) \cos (\omega t) + \frac {z (0) a + z ^ {\prime} (0)}{\omega} \sin (\omega t) \right] e ^ {- a t}.\tag{8.108}
$$

EXERCISE 8.20 ▶ Substitute the function of Eq. (8.108) into Eq. (8.102) to show that it satisfies the equation.

EXERCISE 8.21 ▶ Obtain the solution of Eq. (8.102) in the case of critical damping, using Laplace transforms.

Our discussion of the Laplace transform method for solving differential equations suffices only to introduce the method. The book by Kreyszig in the list at the end of the book is recommended for further study.

## 8.8 Numerical Solutions of Differential Equations

Many differential equations occur for which no solution can be obtained with pencil and paper. A lot of these occur in the study of chemical reaction rates. With the use of programmable computers, it is now possible to obtain numerical approximations to the solutions of these equations to any desired degree of accuracy.

## Euler's Method

This is a method that is extremely simple to understand and implement. However, it is not very accurate and is not used in actual applications. Consider a differential equation for a variable x as a function of time that can be schematically represented by

$$
{\frac {d x}{d t}} = f (x, t)\tag{8.109}
$$

with the initial condition that $x(0) = x_{0}$ , a known value. A formal solution can be written

$$
x (t ^ {\prime}) = x _ {0} + \int_ {0} ^ {t ^ {\prime}} f (x, t) d t.\tag{8.110}
$$

Like any other formal solution, this cannot be used in practice, since the variable $x$ in the integrand function depends on $t$ in some way that we don't yet know.

Euler's method assumes that if $t$ is small enough, the integrand function in Eq. (8.110) can be replaced by its value at the beginning of the integration. We replace $t'$ by the symbol $\Delta t$ and write

$$
x (\Delta t) \approx x _ {0} + \int_ {0} ^ {\Delta t} f (x _ {0}, 0) d t = x _ {0} + \Delta t f (x _ {0}, 0).\tag{8.111}
$$

A small value of $\Delta t$ is chosen, and this process is repeated until the desired value of $t'$ is reached. Let $x_{i}$ be the value of x obtained after carrying out the process i times, and let $t_{i}$ equal $i\Delta t$ , the value of t after carrying out the process i times. We write

$$
x _ {i + 1} \approx x _ {i} + \Delta t f (x _ {i}, t _ {i}).\tag{8.112}
$$

Euler's method is analogous to approximating an integral by the area under a bar graph, except that the height of each bar is obtained by starting with the approximate height of the previous bar and using the known slope of the tangent line.

EXERCISE 8.22 The differential equation for a first-order chemical reaction without back reaction is

$$
\frac {d c}{d t} = - k c,
$$

where c is the concentration of the single reactant and k is the rate constant.

(a) Set up an Excel spreadsheet to carry out Euler's method for this differential equation. $^{a}$

(b) Carry out the calculation for the initial concentration 1.000 mol l $^{-1}$ , k = 1.000 s $^{-1}$ for a time of 2.000 s and for $\Delta t = 0.100$ s.

(c) Compare your result with the correct answer.

## Solution of Differential Equations with Mathematica

Mathematica can solve differential equations both symbolically and numerically.

## Symbolic Solution

The statement DSolve is used to carry out a symbolic solution of a differential equation. We illustrate this with an example.

EXAMPLE 8.9 Use Mathematica to solve the differential equation

$$
{\frac {d y}{d x}} = a y (x)
$$

SOLUTION ▶ We enter the Mathematica statement

$$
\mathrm{DSolve} [ \mathrm{y} ^ {\prime} [ \mathrm{x} ] = = \text { a   y } [ \mathrm{x} ], \mathrm{y} [ \mathrm{x} ], \mathrm{x} ]
$$

and press the “Enter” key. Notice how the statement is written inside the brackets. First comes the equation, with the first derivative denoted by y'. The double equal sign must be used to let Mathematica know that an equation is to be solved. We have used a blank space between the a and the y[x] to indicate multiplication. After a comma comes the specification of the dependent variable, y[x]. Note the use of brackets, not parentheses. The independent variable must be included inside the brackets. After another comma comes the statement of the independent variable. Mathematica returns the output

$$
\operatorname{Out} 1 = \{\{\mathrm{y} [ \mathrm{x} ] \rightarrow \mathrm{e} ^ {\mathrm{a} \mathrm{x}} \mathrm{C} [ 1 ] \} \}
$$

Note the space between the a and the x and the space between the exponential and the constant C[1] in the output. The constant C[1] is to be determined by initial conditions. An initial condition can be included in the original input statement. For example, if $y(0) = 2$ , we would enter

$$
\text { DSolve } [ \{\mathrm{y} ^ {\prime} [ \mathrm{x} ] = = \text { a   y } [ \mathrm{x} ], \mathrm{y} [ 0 ] = = 2 \}, \mathrm{y} [ \mathrm{x} ], \mathrm{x} ]
$$

and press the “Enter” key or a “Shift-return.” The output would be

$$
\operatorname{Out} 1 = \{\{\mathrm{y} [ \mathrm{x} ] \rightarrow 2 \mathrm{e} ^ {\mathrm{a} \mathrm{x}} \} \}
$$

## Numerical Solution

Mathematica carries out numerical solutions of differential equation for which no exact solution can be written. The solution is given in terms of an interpolating function, which is a table of values of the unknown function for different values of the independent variable. The program finds a numerical value of the function for a specific value of the independent variable by interpolation in this table. The statement NDSolve is used to solve the differential equation, as in the next example:

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
EXAMPLE 8.10 Obtain the numerical solution to the differential equation
$\frac{dy}{dx} = 2\sin(x)$ (8.118)
for the interval $0 &lt; x &lt; \pi$ with the initial condition $y(0) = 1$.

SOLUTION ▶ We type the input
    NDSolve[{y'[x]==2 sin[x], y[0]==1}, y, {x, 0, Pi}]
and press the “Enter” key. The output appears
    Out[1]={{y→InterpolatingFunction[{0,3.141593}, &lt;&gt;]}
To obtain the value of the function at some value of $x$, say $x = 2$, we type the input
    y[2]/.%1
and press the “Enter” key or a “Shift-return.” The /. is the replacement operator in Mathematica, and is typed as two characters, a forward slash and a period. The %1 means that the output line number 1 is referred to. If the interpolating function had been in line 3, we would have typed %. The output result now appears
    Out[2]={3.83229}
To obtain a graph of the solution, we enter
    Plot[Evaluate[y[x]/. %1], {x, 0, Pi}]
and press the “Enter” key or a “Shift-Return”. The graph appears as the output.

EXERCISE 8.23 ▶ Obtain the numerical solution to the differential equation
$\frac{d^2y}{dx^2} = \sin(x)$ (8.119)
for the interval $0 &lt; x &lt; \pi$ and for the initial condition $x = 1$.
</div>

## SUMMARY

A differential equation contains one or more derivatives, and its solution is a function that satisfies the equation. Classical equations of motion are differential equations based on Newton's laws of motion that when solved give the positions of particles as a function of time. We have presented the solution to several of these. These differential equations are deterministic. That is, given the equation of motion for a given system and the initial conditions (position and velocity of every particle at some initial time), the positions and velocities are determined for all times.

Many homogeneous and inhomogeneous linear differential equations with constant coefficients can be solved by routine methods, which we discussed. An exact differential equation can also be solved in a routine way. Such an equation consists of an exact differential set equal to zero. Since a line integral of an exact differential (the differential of a function) is equal to the value of the function at the end of the integration minus the value of the function at the beginning of the integration, a line integration to a general ending point provides the formula for the function, solving the equation. Some inexact differential equations can be converted into exact equations by use of an integrating factor, and solution of the exact equation provides a solution to the inexact equation.

Many partial differential equations arising in physical problems can be solved by separation of variables. In this procedure, a trial solution consisting of factors depending on one variable each is introduced, and the resulting equation is manipulated until the variables occur only in separate terms. Setting these terms equal to constants gives one ordinary differential equation for each variable.

Some ordinary differential equations can be solved by using some theorems of Laplace transforms which transform a differential equation into an algebraic equation. If this equation can be solved for the transform of the unknown function, and if the inverse transform can be found, the equation is solved.

If a mathematical method for solving a differential equation cannot be found, numerical methods exist for generating numerical solutions to any desired degree of accuracy. Euler's method and the Runge-Kutta method were presented.

## PROBLEMS

1. An object moves through a fluid in the x direction. The only force acting on the object is a frictional force that is proportional to the negative of the velocity:

$$
F _ {x} = - \zeta v _ {x} = - \zeta \left(\frac {d x}{d t}\right).
$$

Write the equation of motion of the object. Find the general solution to this equation, and obtain the particular solution that applies if $x(0) = 0$ and $v_{x}(0) = v_{0} = \text{constant}$ . Draw a graph of the position as a function of time.

2. A particle moves along the z axis. It is acted upon by a constant gravitational force equal to -kmg, where k is the unit vector in the z direction. It is also acted on by a frictional force given by

$$
\mathbf {F} _ {f} = - \mathbf {k} \zeta \left(\frac {d z}{d t}\right),
$$

where $\zeta$ is a constant called a “friction constant.” Find the equation of motion and obtain a general solution. Find z as a function of time if $z(0) = 0$ and $v_{x}(0) = 0$ . Draw a graph of z as a function of time.

3. An object sliding on a solid surface experiences a frictional force that is constant and in the opposite direction to the velocity if the particle is moving, and is zero it is not moving. Find the position of the particle as a function of time if it moves only in the x direction and the initial position is $x(0) = 0$ and the initial velocity is $v_{x}(0) = v_{0} = \text{constant}$ . Proceed as though the constant force were present at all times and then cut the solution off at the point at which the velocity vanishes. That is, just say that the particle is fixed after this time.

4. A harmonic oscillator has a mass $m = 0.200 \, kg$ and a force constant $k = 98 \, N \, m^{-1}$ .

a) Find the period and the frequency of oscillation.

b) Find the value of the friction constant $\zeta$ necessary to produce critical damping with this oscillator. Find the value of the constant $\lambda_{1}$ .

c) Construct a graph of the position of the oscillator as a function of t for the initial conditions $z(0)=0$ , $v_{z}(0)=0.100\ m\ s^{-1}$ .

5. A less than critically damped harmonic oscillator has a mass $m = 0.200 \, kg$ , a force constant $k = 98 \, N \, m^{-1}$ and a friction constant $\zeta = 4.00 \, kg \, s^{-1}$ .

a) Find the frequency of oscillation $\omega$ and compare it with the frequency that would occur if there were no damping.

b) Find the time required for the real exponential factor in the solution to drop to one-half of its value at t = 0.

6. A forced harmonic oscillator with a circular frequency $\omega = 6.283 s^{-1}$ (frequency $\nu = 1.000 s^{-1}$ ) is exposed to an external force $F_{0} \sin(\alpha t)$ with circular frequency $\alpha = 7.540 s^{-1}$ such that in the solution of Eq. (8.59) becomes

$$
z (t) = \sin (\omega t) + 0.100 \sin (\alpha t).\tag{8.120}
$$

Using Excel or Mathematica, make a graph of $z(t)$ for a time period of at least 20 s.

7. A forced harmonic oscillator with mass $m = 0.200\mathrm{kg}$ and a circular frequency $\omega = 6.283\mathrm{s}^{-1}$ (frequency $\nu = 1.000\mathrm{s}^{-1}$ ) is exposed to an external force $F_0\exp (-\beta t)\sin (\alpha t)$ with $\alpha = 7.540\mathrm{s}^{-1}$ and $\beta = 0.500\mathrm{s}^{-1}$ . Find the solution to its equation of motion. Construct a graph of the motion for several values of $F_{0}$ .

8. A tank contains a solution that is rapidly stirred, so that it remains uniform at all times. A solution of the same solute is flowing into the tank at a fixed rate of flow, and an overflow pipe allows solution from the tank to flow out at the same rate. If the solution flowing in has a fixed concentration that is different from the initial concentration in the tank, write and solve the differential equation that governs the number of moles of solute in the tank. The inlet pipe allows A moles per hour to flow in and the overflow pipe allows Bn moles per hour to flow out, where A and B are constants and n is the number of moles of solute in the tank. Find the values of A and B that correspond to a volume in the tank of 100.0 l, an input of $1.0001 h^{-1}$ of a solution with $1.000 mol l^{-1}$ , and an output of $1.0001 h^{-1}$ of the solution in the tank. Find the concentration in the tank after 5.00 h, if the initial concentration is zero.

9. An nth-order chemical reaction with one reactant obeys the differential equation

$$
\frac {d c}{d t} = - k c ^ {n},
$$

where c is the concentration of the reactant and k is a constant. Solve this differential equation by separation of variables. If the initial concentration is $c_{0}$ moles per liter, find an expression for the time required for half of the reactant to react.

10. Find the solution to the differential equation

$$
\left(\frac {d ^ {3} y}{d x ^ {3}}\right) - 2 \left(\frac {d ^ {2} y}{d x ^ {2}}\right) - \left(\frac {d y}{d x}\right) + 2 y = - x e ^ {x}.
$$

11. Test the following equations for exactness, and solve the exact equations:

$$
\mathbf {a}) (x ^ {2} + x y + y ^ {2}) d x + \left(4 x ^ {2} - 2 x y + 3 y ^ {2}\right) d y = 0
$$

b) $ye^{x}dx + e^{x}dy = 0$

c) $\left[2xy - \cos (x)\right]dx + (x^2 -1)dy = 0$

12. Use Mathematica to solve the differential equation symbolically

$$
{\frac {d y}{d x}} + y \cos (x) = e ^ {- \sin (x)}.
$$

13. Use Mathematica to obtain a numerical solution to the differential equation in the previous problem for the range 0 < x < 10 and for the initial condition $y(0) = 1$ . Evaluate the interpolating function for several values of x and make a plot of the interpolating function for the range 0 < x < 10.

14. Find a particular solution of

$$
\frac {d ^ {2} y}{d x ^ {2}} - 4 y = 2 e ^ {3 x} + \sin (x).
$$

15. Radioactive nuclei decay according to the same differential equation that governs first-order chemical reactions, Eq. (8.65). In living matter, the isotope ${}^{14}C$ is continually replaced as it decays, but it decays without replacement beginning with the death of the organism. The half-life of the isotope (the time required for half of an initial sample to decay) is 5730 years. If a sample of charcoal from an archaeological specimen exhibits 0.97 disintegrations of ${}^{14}C$ per gram of carbon per minute and wood recently taken from a living tree exhibits 15.3 disintegrations of ${}^{14}C$ per gram of carbon per minute, estimate the age of the charcoal.

16. A pendulum of length L oscillates in a vertical plane. Assuming that the mass of the pendulum is all concentrated at the end of the pendulum, show that it obeys the differential equation

$$
L \left(\frac {d ^ {2} \phi}{d t ^ {2}}\right) = - g \sin (\phi),
$$

where g is the acceleration due to gravity and $\phi$ the angle between the pendulum and the vertical. This equation cannot be solved exactly. For small oscillations such that

$$
\sin (\phi) \approx \phi
$$

find the solution to the equation. What is the period of the motion? What is the frequency? Evaluate these quantities if L = 1.000 m and if L = 10.000 m.

17. Use Mathematica to obtain a numerical solution to the pendulum equation in the previous problem without approximation for the case that $L = 1.000\mathrm{m}$ with the initial conditions $\phi(0) = 0.350\mathrm{rad}$ (about $20^{\circ}$ ) and $d\phi/dt = 0$ . Evaluate the solution for $t = 0.500\mathrm{s}$ , $1.000\mathrm{s}$ , and $1.500\mathrm{s}$ . Make a graph of your solution for $0 < t < 4.00\mathrm{s}$ . Repeat your solution for $\phi(0) = 0.050\mathrm{rad}$ (about $2.9^{\circ}$ ) and $d\phi/dt = 0$ . Determine the period and the frequency from your graphs. How do they compare with the solution from the previous problem?

18. Obtain the solution for Eq. (8.55) and (8.56) for the forced harmonic oscillator using Laplace transforms.

19. An object of mass m is subjected to an oscillating force in the x direction given by $a \sin(bt)$ where a and b are constants. Find the solution to the equation of motion of the particle.

20. An object of mass m is subjected to a gradually increasing force given by $a(1 - e^{-bt})$ where a and b are constants. Solve the equation of motion of the particle. Find the particular solution for the case that $x(0) = 0$ and dx/dt = 0 at t = 0.

# Operators, Matrices, and Group Theory

## Preview

A mathematical operator is a symbol standing for carrying out a mathematical operation or a set of operations. Operators are important in quantum mechanics, since each mechanical variable has a mathematical operator corresponding to it. Operator symbols can be manipulated symbolically in a way similar to the algebra of ordinary variables, but according to a different set of rules. An important difference between ordinary algebra and operator algebra is that multiplication of two operators is not necessarily commutative, so that if $\hat{A}$ and $\hat{B}$ are two operators, $\hat{A}\hat{B} \neq \hat{B}\hat{A}$ can occur.

A matrix is a list of quantities, arranged in rows and columns. We will introduce matrix algebra, which is a branch of algebra that has rules that are different from the algebra of ordinary variables, and which has similarities with operator algebra.

A group is a set of elements with defined properties, including a single operation which is not necessarily commutative. The elements of a group can represent symmetry operators, and group theory can provide useful information about quantum-mechanical wave functions for symmetrical molecules, spectroscopic transitions, and so forth.

## Principal Facts and Ideas

1. An operator is a symbol that stands for a mathematical operation. If an operator $\hat{A}$ operates on a function f the result is a new function, $g: \hat{A}f = g$ .

2. Operator algebra manipulates operator symbols according to rules that are slightly different from those of ordinary algebra.

3. An eigenvalue equation has the form $\hat{A} f = af$ where $f$ is an eigenfunction and $a$ is an eigenvalue.

4. Symmetry operators move points in space relative to a symmetry element. A symmetry operator which belongs to the nuclear framework of a molecule moves each nucleus to the former position of a nucleus of the same kind.

5. Symmetry operators can operate on functions as well as on points and can have eigenfunctions with eigenvalues equal to 1 or to -1. An electronic wave function of a molecule can be an eigenfunction of the symmetry operators which belong to the nuclear framework of a molecule.

6. Matrices can be manipulated according to the rules of matrix algebra. which are similar to the rules of ordinary algebra. One exception is that matrix multiplication is not necessarily commutative: if A and B are matrices, $AB \neq BA$ can occur.

7. The inverse of a matrix obeys $A^{-1}A = AA^{-1} = E$ where E is the identity matrix. The inverse of a given matrix can be obtained by the Gauss–Jordan elimination procedure.

8. A group is a set of elements obeying certain conditions, with a single operation combining two elements to give a third element of the group. This operation is called multiplication and is noncommutative.

9. The symmetry operators belonging to a symmetrical object such as the equilibrium nuclear framework of a molecule form a group.

10. A set of matrices obeying the same multiplication table as a group is a representation of the group.

11. Various theorems of group theory make it useful in studying the symmetry properties of molecules in quantum chemistry.

## Objectives

After studying this chapter, you should be able to:

1. perform the elementary operations of operator algebra;

2. identify and use symmetry operators associated with a symmetrical molecule;

3. perform the elementary operations of matrix algebra, including matrix multiplication and finding the inverse of a matrix;

4. identify a group of symmetry operators and construct a multiplication table for the group.

## 9.1 Operators and Operator Algebra

A mathematical operator is a symbol that stands for carrying out a mathematical operation on some function. For example, we can use the symbol d/dx or the symbol $\hat{D}_{x}$ to stand for the operation of differentiating with respect to x. We will usually assign a symbol to an operator that consists of a letter with a caret ( $^{\wedge}$ ) over it. When an operator operates on a function, the result will generally be another function. We will discuss three principal types of operators: multiplication operators, derivative operators, and symmetry operators. Multiplication operators are operators that stand for multiplying a function either by a constant or by a specified function. Derivative operators stand for differentiating a function one or more times with respect to one or more independent variables. An operator can correspond to carrying out more than one operation, such as multiplication by a function followed by a differentiation or taking the sum of the results of operating with two operators. Symmetry operators are defined by the way they move a point in space but can also operate on functions.

EXAMPLE 9.1 Let the operator $\hat{A}$ be given by

$$
\hat {A} = x + \frac {d}{d x}.\tag{9.1}
$$

Find $\hat{A} f$ if $f = a\sin (bx)$ , where $a$ and $b$ are constants.

SOLUTION ▶

$$
\hat {A} a \sin (b x) = x a \sin (b x) + a b \cos (b x).\tag{9.2}
$$

If the result of operating on a function with an operator is a function that is proportional to the original function, the function is called an eigenfunction of that operator, and the proportionality constant is called an eigenvalue. $^{1}$ If

$$
\boxed {\hat {A} f = a f}\tag{9.3}
$$

then $f$ is an eigenfunction of $\hat{A}$ and $a$ is the eigenvalue corresponding to that eigenfunction. An equation like Eq. (9.3) is called an eigenvalue equation. The time-independent Schrödinger equation of quantum mechanics is an eigenvalue equation, and other eigenvalue equations are important in quantum mechanics.

EXAMPLE 9.2 Find the eigenfunctions and corresponding eigenvalues for the operator $d^{2}/dx^{2}$ .

SOLUTION ▶ We need to find a function $f(x)$ and a constant a such that

$$
\frac {d ^ {2} f}{d x ^ {2}} = a f.
$$

This is a differential equation that was solved as in Chapter 8. The general solution is

$$
f (x) = A \exp (\sqrt {a} x) + B \exp (- \sqrt {a} x),
$$

where $A$ and $B$ are constants. Since no boundary conditions were stated, the eigenvalue $a$ can take on any value, as can the constants $A$ and $B$ .

EXERCISE 9.1 ▶

Find the eigenfunctions of the operator $i\frac{d}{dx}$ , where $i =$

![[229854887e5fc3c88cca646fa39836a37b34256c2cd8f94ea0cdbd34e636693a.jpg]]

## Operator Algebra

Although a mathematical operator is a symbol that stands for the carrying out of an operation, we can define an operator algebra in which we manipulate these symbols much as we manipulate variables and numbers in ordinary algebra. We define the sum of two operators by

$$
\left(\hat {A} + \hat {B}\right) f = \hat {A} f + \hat {B} f,\tag{9.4}
$$

where $\hat{A}$ and $\hat{B}$ are two operators and where f is some function on which $\hat{A}$ and $\hat{B}$ can operate.

The product of two operators is defined as the successive operation of the operators, with the one on the right operating first. If

$$
\hat {C} = \hat {A} \hat {B}\tag{9.5}
$$

then

$$
\hat {C} f = \hat {A} (\hat {B} f).\tag{9.6}
$$

The result of $\hat{B}$ operating on f is in turn operated on by $\hat{A}$ and the result is said to equal the result of operating on f with the product $\hat{A}\hat{B}$ . It is important that an operator operates on everything to its right in the same term and that the rightmost operator in an operator product operates first. Equation (9.5) is an operator equation. The two sides of the equation are equal in the sense that if each is applied to an arbitrary function the two results are the same.

EXAMPLE 9.3 Find the operator equal to the operator product $\frac{d}{dx}\hat{x}$ .

SOLUTION ▶ We take an arbitrary differentiable function $f = f(x)$ and apply the operator product to it,

$$
\frac {d}{d x} \hat {x} f = x \frac {d f}{d x} + f \frac {d x}{d x} = \left(x \frac {d}{d x} + \hat {E}\right) f,
$$

where $\hat{E}$ is the identity operator, defined to be the operator for multiplication by unity (same as doing nothing). We can write the operator equation that is equivalent to this equation:

$$
{\frac {d}{d x}} \hat {x} = x {\frac {d}{d x}} + \hat {E}.
$$

EXERCISE 9.2 ▶

Find the operator equal to the operator product $\frac{d^{2}}{dx^{2}}x$ .

The difference of two operators is given by

$$
(\hat {A} - \hat {B}) = \hat {A} + (- \hat {E}) \hat {B}.\tag{9.7}
$$

We now have an operator algebra in which we carry out the operations of addition and multiplication on the operators themselves. These operations have the following properties: Operator multiplication is associative. This means that if $\hat{A}$ , $\hat{B}$ , and $\hat{C}$ are operators, then

$$
\boxed {(\hat {A} \hat {B}) \hat {C} = \hat {A} (\hat {B} \hat {C}).}\tag{9.8}
$$

Operator multiplication and addition are distributive. This means that if $\hat{A}$ , $\hat{B}$ , and $\hat{C}$ are operators.

$$
\boxed {\hat {A} (\hat {B} + \hat {C}) = \hat {A} \hat {B} + \hat {A} \hat {C}.}\tag{9.9}
$$

Operator multiplication is not necessarily commutative. This means that in some cases the same result is not obtained if the sequence of operation of two operators is reversed:

$$
\boxed {\hat {A} \hat {B} \neq \hat {B} \hat {A} \quad (\text { possible })}\tag{9.10}
$$

If the operator $\hat{A}\hat{B}$ is equal to the operator $\hat{B}\hat{A}$ then $\hat{A}$ and $\hat{B}$ are said to commute. The commutator of $\hat{A}$ and $\hat{B}$ is denoted by $\left[\hat{A},\hat{B}\right]$ and defined by

$$
\boxed {\left[ \hat {A}, \hat {B} \right] = \hat {A} \hat {B} - \hat {B} \hat {A} \quad (\text { definition   of   the   commutator })}\tag{9.11}
$$

If $\hat{A}$ and $\hat{B}$ commute, then $\left[\hat{A},\hat{B}\right] = \hat{0}$ , where $\hat{0}$ is the null operator, equivalent to multiplying by zero.

EXAMPLE 9.4 Find the commutator $\left[\frac{d}{dx}, x\right]$ .

SOLUTION ▶ We apply the commutator to an arbitrary function $f(x)$ :

$$
\left[ \frac {d}{d x}, x \right] f = \frac {d}{d x} (x f) - x \frac {d f}{d x} = x \frac {d f}{d x} + f - x \frac {d f}{d x} = f.\tag{9.12}
$$

Therefore,

$$
\left[ \frac {d}{d x}, x \right] = \hat {E} = \hat {1},\tag{9.13}
$$

where the symbol $\hat{1}$ stands for multiplication by unity and is the same thing as $\hat{E}$ . We will generally omit the caret symbol on multiplication operators.

## EXERCISE 9.3 ▶

$$
\text {   Find   the   commutator   } [ x ^ {2}, d ^ {2} / d x ^ {2} ].
$$

Here are a few facts that will predict in almost all cases whether two operators will commute:

1. An operator containing a multiplication by a function of x and one containing d/dx will not generally commute.

2. Two multiplication operators commute. If g and h are functions of the same or different independent variables or are constants, then

$$
[ \hat {g}, \hat {h} ] = 0.\tag{9.14}
$$

3. Operators acting on different independent variables commute. For example,

$$
\left[ x \frac {d}{d x}, \frac {d}{d y} \right] = 0.\tag{9.15}
$$

![[3bebd4d5475203e63111e73e3f317ab5b9ca2f5eb506629f4058c03b1ffc2c6c.jpg]]

4. An operator for multiplication by a constant commutes with any other operator.

EXERCISE 9.4 ▶ Show that Eq. (9.15) is correct, and that statement (4) is correct.

Since we have defined the product of two operators, we have a definition for the powers of an operator. An operator raised to the nth power is the operator for n successive applications of the original operator:

$$
\hat {A} ^ {n} = \hat {A} \hat {A} \hat {A} \dots \hat {A} (n \text {factors})\tag{9.16}
$$

EXAMPLE 9.5 If the operator $\hat{A}$ is $x + \frac{d}{dx}$ , find $\hat{A}^3$ .

## SOLUTION ▶

$$
\begin{array}{r l} \hat {A} ^ {3} & = \left(x + \frac {d}{d x}\right) \left(x + \frac {d}{d x}\right) \left(x + \frac {d}{d x}\right) \\ & = \left(x + \frac {d}{d x}\right) \left(x ^ {2} + \frac {d}{d x} x + x \frac {d}{d x} + \frac {d ^ {2}}{d x ^ {2}}\right) \\ & = x ^ {3} + x \frac {d}{d x} \hat {x} + x ^ {2} \frac {d}{d x} + x \frac {d ^ {2}}{d x ^ {2}} + \frac {d}{d x} x ^ {2} + \frac {d ^ {2}}{d x ^ {2}} x + \frac {d}{d x} x \frac {d}{d x} + \frac {d ^ {3}}{d x ^ {3}}. \end{array}
$$

The order of the factors in each term must be maintained because the two terms in the operator do not commute with each other.

EXERCISE 9.5 ▶

(a) For the operator $\hat{A} = x + \frac{d}{dx}$ , find $\hat{A}^3 f$ if $f(x) = \sin (ax)$ .

(b) Find an expression for $\hat{B}^2$ if $\hat{B} = x(d^2 /dx^2)$ and find $\hat{B}^2 f$ if $f = bx^4$ .

Division by an operator is not defined. However, we define the inverse of an operator as that operator which “undoes” what the first operator does. The inverse of $\hat{A}$ is denoted by $\hat{A}^{-1}$ , and

$$
\boxed {\hat {A} \hat {A} ^ {- 1} = \hat {A} ^ {- 1} \hat {A} = \hat {E}}\tag{9.17}
$$

$$
\boxed {\hat {A} ^ {- 1} \hat {A} f = \hat {E} f = f.}\tag{9.18}
$$

The inverse of a nonzero multiplication operator is the operator for multiplication by the reciprocal of the original quantity. Not all operators possess inverses. For example, there is no inverse for $\hat{0}$ (multiplication by zero).

Operator algebra can be used to solve some differential equations. $^{2}$ A linear differential equation with constant coefficients can be written in operator notation and solved by operator algebra. The equation

$$
\frac {d ^ {2} y}{d x ^ {2}} - 3 \frac {d y}{d x} + 2 y = 0\tag{9.19}
$$

can be written as

$$
(\hat {D} _ {x} ^ {2} - 3 \hat {D} _ {x} + 2) y = 0\tag{9.20}
$$

where we introduce the symbol $\hat{D}_x$ as an abbreviation for $d / dx$ . The equation can be written as an operator equation:

$$
(\hat {D} _ {x} ^ {2} - 3 \hat {D} _ {x} + 2) = 0.\tag{9.21}
$$

Using operator algebra, we manipulate this equation as though it were an ordinary equation. We factor it to obtain

$$
\left(\hat {D} _ {x} - 2\right) \left(\hat {D} _ {x} - 1\right) = 0.\tag{9.22}
$$

The two roots are obtained from

$$
\hat {D} _ {x} - 2 = 0\tag{9.23a}
$$

$$
\hat {D} _ {x} - 1 = 0.\tag{9.23b}
$$

These equations are the same as

$$
\frac {d y}{d x} - 2 y = 0\tag{9.24a}
$$

$$
\frac {d y}{d x} - y = 0.\tag{9.24b}
$$

The solutions to these equations are

$$
y = e ^ {2 x}
$$

$$
y = e ^ {\lambda}\tag{9.25a}
$$

(9.25b)

Since both of these must be solutions to the original equation, the general solution is

$$
y = c _ {1} e ^ {2 x} + c _ {2} e ^ {x},\tag{9.26}
$$

where $c_{1}$ and $c_{2}$ are arbitrary constants.

EXERCISE 9.6 ▶

Show that the function in Eq. (9.26) satisfies Eq. (9.19).

## Operators in Quantum Mechanics

One of the postulates of quantum mechanical theory is that for every mechanical quantity there is a mathematical operator. The theory of quantum mechanics defines how these operators are constructed, and they contain derivative operators and multiplication operators. The eigenfunctions and eigenvalues of these operators play a central role in the theory. For example, the operator that corresponds to the mechanical energy is the Hamiltonian operator, and the time-independent Schrodinger equation is the eigenvalue equation for this operator. For motion in the x direction of a single particle of mass m with a potential energy given by $\mathcal{V}(x)$ , the Hamiltonian operator is

$$
- \frac {\hbar^ {2}}{2 m} \frac {\partial^ {2}}{\partial x ^ {2}} + \mathcal {V} (x)\tag{9.27}
$$

where $\hbar$ is Planck's constant divided by $2\pi$ . The term $\mathcal{V}(x)$ stands for a multiplication operator. You will become familiar with these operators in any physical chemistry class.

## 9.2 Symmetry Operators

Many common objects are said to be symmetrical. The most symmetrical object is a sphere, which looks just the same no matter which way it is turned. A cube, although less symmetrical than a sphere, has 24 different orientations in which it looks the same. Many biological organisms have approximate bilateral symmetry, meaning that the left side looks like a mirror image of the right side. Symmetry properties are related to symmetry operators, which can operate on functions like other mathematical operators. We first define symmetry operators in terms of how they act on points in space and will later define how they operate on functions. We will consider only point symmetry operators, a class of symmetry operators that do not move a point if it is located at the origin of coordinates.

We denote the position of a point by its Cartesian coordinates, keeping the Cartesian coordinate axes fixed as the point moves. The action of a general symmetry operator denoted by $\hat{O}$ is specified by writing

$$
\hat {O} (x _ {1}, y _ {1}, z _ {1}) = (x _ {2}, y _ {2}, z _ {2}),\tag{9.28}
$$

where $x_{1}$ , $y_{1}$ , $z_{1}$ are the coordinates of the original location of a point and $x_{2}$ , $y_{2}$ , $z_{2}$ are the coordinates of the location to which the operator moves the point.

## Specific Symmetry Operators

Our first symmetry operator is the identity operator, which leaves any point in its original location. We denote it by $\hat{E}$ , the same symbol as for the multiplicative identity operator.

$$
\hat {E} (x _ {1}, y _ {1}, z _ {1}) = (x _ {1}, y _ {1}, z _ {1})\tag{9.29}
$$

If $\mathbf{r}_1$ is the vector with components $(x_{1},y_{1},z_{1})$ , this equation can be written

$$
\hat {E} \mathbf {r} _ {1} = \mathbf {r} _ {1}.\tag{9.30}
$$

The inversion operator is denoted by $\hat{i}$ . It moves a point on a line from its original position through the origin to a location at the same distance from the origin as the original position:

$$
\hat {\imath} (x _ {1}, y _ {1}, z _ {1}) = (- x _ {1}, - y _ {1}, - z _ {1})\tag{9.31}
$$

$$
\boxed {\hat {t} \mathbf {r} _ {1} = - \mathbf {r} _ {1}}
$$

For each symmetry operator, we define a symmetry element, which is a point, line, or plane relative to which the symmetry operation is performed. The symmetry element for a given symmetry operator is sometimes denoted by the same symbol as the operator, but without the caret (^). For example, the symmetry element for the inversion operator is the origin. The symmetry element of any point symmetry operator must include the origin. If a point is located on the symmetry element for a symmetry operator, that symmetry operator will not move that point.

A reflection operator moves a point on a line perpendicular to a specified plane, through the plane to a location on the other side of the plane at the same distance from the plane as the original point. This motion is called reflection through the plane. The specified plane is the symmetry element and must pass through the origin if the operator is a point symmetry operator. There is a different reflection operator for each of the infinitely many planes passing through the origin. The operator $\hat{\sigma}_{h}$ corresponds to reflection through the x-y plane (the h subscript stands for “horizontal”). Figure 9.1 shows the action of the $\hat{\sigma}_{h}$ operator. There is only one horizontal plane passing through the origin, so there is only one $\hat{\sigma}_{h}$ operator among the point symmetry operators. The action of $\hat{\sigma}_{h}$ corresponds to

$$
\boxed {\hat {\sigma} _ {h} (x _ {1}, y _ {1}, z _ {1}) = (x _ {1}, y _ {1}, - z _ {1})}.\tag{9.33}
$$

A reflection operator whose symmetry element is a vertical plane is denoted by $\hat{\sigma}_{v}$ . You must separately specify which vertical plane is the symmetry element.

EXERCISE 9.7 ▶ Write an equation similar to Eq. (9.33) for the $\hat{\sigma}_{v}$ operator whose symmetry element is the x-z plane, and one for the $\hat{\sigma}_{v}$ operator whose symmetry element is the y-z plane.

Next we have rotation operators. An ordinary rotation, in which a point moves as if it were part of a rigid object rotating about an axis, is called a proper rotation. The axis of rotation is the symmetry element, and the action of the rotation operator is to move the point along an arc, staying at a fixed perpendicular distance from a fixed point on the axis. The axis of rotation must pass through the origin if the rotation operator is a point symmetry operator. In addition to specifying the axis of rotation, one must specify the direction of rotation and the angle of rotation. By convention, the direction of rotation is taken as counterclockwise when viewed from the end of the axis that is designated as the positive end. We consider only angles of rotation such that n applications of the rotation operator will produce exactly one complete rotation, where n is a positive integer. Such a rotation operator is denoted by $\hat{C}_{n}$ . The axis of rotation must be specified separately. For example, the operator for a rotation of $90^{\circ}$ about the z axis can be called $\hat{C}_{4}(z)$ .

![[c5ee0d4b85e9bff64c820df9ae8ff3621d8cf06406c2101c0cd30ef892309bc4.jpg]]  
Figure 9.1 ▶ The action of the reflection operator, $\hat{\sigma}_h$ .

Figure 9.2 shows the action of the $\hat{C}_4(z)$ operator. For this operator,

$$
\hat {C} _ {4} (z) (x _ {1}, y _ {1}, z _ {1}) = (- y _ {1}, x _ {1}, z _ {1})\tag{9.34}
$$

so that

$$
x _ {2} = - y _ {1}, \quad y _ {2} = x _ {1}, \quad z _ {2} = z _ {1}.\tag{9.35}
$$

EXERCISE 9.8 ▶

Find the following:

$$
(a) \hat {C} _ {4} (z) (1, - 4, 6)
$$

$$
(b) C _ {2} (x) (1, 2, - 3).
$$

![[dff6e57e7e6c0edf0bf5f2dece74357f0975b3fb00df8a95c4c9fdce6762e245.jpg]]

An improper rotation is equivalent to a proper rotation followed by a reflection through a plane that is perpendicular to the rotation axis. For this to be a point symmetry operation, both the rotation axis and the reflection plane must pass through the origin. The symbol for an improper rotation operator is $\hat{S}_{n}$ , where the subscript n has the same meaning as with a proper rotation. The symmetry element for an improper rotation is the axis of rotation. The action of the operator for an improper rotation of $90^{\circ}$ about the z axis is given by

![[bcf65934fcf7608f817cdfe1cc2dbcf51a5491a2fee1547fb511649649ea363a.jpg]]  
Figure 9.2 ▶ The action of a rotation operator, $\hat{C}_{4}$ .

$$
\hat {S} _ {4} (z) (x _ {1}, y _ {1}, z _ {1}) = (- y _ {1}, x _ {1}, - z _ {1}).\tag{9.36}
$$

An improper rotation operator $\hat{S}_2$ is the same as the inversion operator $\hat{\imath}$ , and any $\hat{S}_1$ operator is the same as a reflection operator.

EXERCISE 9.9 ▶

Find the following:

(a) $\hat{S}_3(z)(1,2,3)$

$$
(b) \hat {S} _ {2} (y) (3, 4, 5).
$$

![[d4b41b8df33d16ca0e5290a2ff8140bcbd31dd5098795ef41bd939c9d40d881d.jpg]]

We have defined all of the point symmetry operators. In addition, there are other symmetry operators and symmetry elements, such as translations, glide planes, screw axes, etc., which are useful in describing crystal lattices but which are not useful for molecules. We do not discuss these operators.

Symmetry operators can operate on a set of points as well as on a single point. For example, they can operate simultaneously on all of the particles of a solid object or on all of the nuclei of a molecule, or on all of the electrons of a molecule. For example, a benzene molecule in its equilibrium conformation has the shape of a regular hexagon. If the center of mass is at the origin, the inversion operator moves each of the carbon nuclei to the original location of another carbon nucleus and each of the hydrogen nuclei to the original location of another hydrogen nucleus. If after a symmetry operation all of the particles in an object are in the same conformation as before except for the exchange of identical particles, we say that the symmetry operator belongs to the object. Any object has a set of symmetry operators (or symmetry elements) that belong to it. An unsymmetrical object possesses only the identity operator, but a symmetrical object possesses at least one additional symmetry operator. The symmetry properties of the object can be specified by listing all symmetry operators that belong to it or by listing their symmetry elements. It is found that the symmetry operators belonging to any rigid object form a mathematical group, which we discuss later in this chapter. The symmetry of the object can also be specified by giving the symbol assigned to the appropriate group.

A uniform spherical object is the most highly symmetrical object. If the center of the sphere is at the origin, every mirror plane, every rotation axis, every improper rotation axis, and the inversion center at the origin are symmetry elements of symmetry operators belonging to the sphere.

EXAMPLE 9.6 List the symmetry elements of a uniform cube centered at the origin with its faces parallel to the coordinate planes.

SOLUTION ▶ The symmetry elements are:
The inversion center at the origin.
Three $C_{4}$ axes coinciding with the coordinate axes.
Four $C_{3}$ axes passing through opposite corners of the cube.

![[b7eb705cc59dfea222a2f98b806e76d36303d048cf2c31e76b1ed1314d7100f2.jpg]]

Four $S_{6}$ axes. coinciding with the $C_{3}$ axes.

Six $C_{2}$ axes connecting the midpoints of opposite edges.

Three mirror planes in the coordinate planes.

Six mirror planes passing through opposite edges.

EXERCISE 9.10 ▶

(a) List the symmetry elements of a right circular cylinder. It is customary to place the highest-order rotation axis on the axis, so we place the axis of the cylinder on the z axis and place its center at the origin. Since even an infinitesimal rotation belongs to the object, the z axis is a $C_{\infty}$ axis.

(b) List the symmetry elements of a uniform regular tetrahedron. It is possible to arrange the object so that its center is at the origin and the four corners are at alternate corners of a cube oriented as in Example 9.6.

## EXAMPLE 9.7 List the symmetry elements of the benzene molecule.

SOLUTION ▶ Locate the molecule with its nuclei in their equilibrium conformation as shown in Fig. 9.3. The symmetry elements are:

The inversion center at the origin.

The $\sigma_{h}$ mirror plane containing the nuclei.

A $C_6$ axis and an $S_6$ axis on the $z$ axis.

Six vertical mirror planes, three through carbon nuclei and three that pass halfway between adjacent carbon nuclei.

Six $C_{2}$ axes located where the mirror planes intersect the x-y plane. These are also $S_{2}$ axes. Some of the symmetry elements are shown in Fig. 9.3. The symbols on the rotation axes identify them, with a hexagon labeling a sixfold axis, a square labeling a fourfold axis, and so on.

EXERCISE 9.11 ▶

List the symmetry elements for

(a) $H_{2}O$ (bent)

(b) $\mathrm{CH}_4$ (tetrahedral)

(c) $\mathrm{CO}_{2}$ (linear).

## The Operation of Symmetry Operators on Functions

We have described the action of symmetry operators on points. We now define how they act on functions. When a mathematical operator operates on a function, a new function is produced. We define this same action for a symmetry operator. If $\psi$ is some function of x, y, and z and $\hat{O}$ is some symmetry operator, then we define

![[2519ea4671de57b358390a61d943320af0a969605da28358c927511b94a3a69b.jpg]]  
Figure 9.3 ▶ The benzene molecule with symmetry elements shown.

$$
\hat {O} \psi = \phi ,\tag{9.37}
$$

where $\phi$ is a newly produced function. We now have to define this new function. If $\hat{O}$ is the operator that carries a point from $(x_{1}, y_{1}, z_{1})$ to $(x_{2}, y_{2}, z_{2})$ , we define $\phi$ to have the same value at $(x_{2}, y_{2}, z_{2})$ that $\psi$ has at $(x_{1}, y_{1}, z_{1})$ :

$$
\phi (x _ {2}, y _ {2}, z _ {2}) = \psi (x _ {1}, y _ {1}, z _ {1})\tag{9.38}
$$

This definition allows us to treat symmetry operators on an equal footing with other mathematical operators that operate on functions.

EXAMPLE 9.8 The unnormalized 2px wave function for the electron in a hydrogen atom is

$$
\psi_ {2 p x} = x \exp \left[ \frac {- (x ^ {2} + y ^ {2} + z ^ {2}) ^ {1 / 2}}{2 a _ {0}} \right],\tag{9.39}
$$

where $a_{0}$ is a constant called the Bohr radius. Find $\hat{C}_{4}(z)\psi_{2px}$ .

SOLUTION ▶ The effect of this operator is given by Eq. (9.34)

$$
\hat {C} _ {4} (z) (x _ {1}, y _ {1}, z _ {1}) = (x _ {2}, y _ {2}, z _ {2}) = (- y _ {1}, x _ {1}, z _ {1}).
$$

The new function is thus

$$
\phi (x _ {2}, y _ {2}, z _ {2}) = \psi_ {2 p x} (x _ {1}, y _ {1}, z _ {1}) = y _ {2} \exp \left[ \frac {- (y _ {2} ^ {2} + x _ {2} ^ {2} + z _ {2} ^ {2}) ^ {1 / 2}}{2 a _ {0}} \right].
$$

Thus

$$
\hat {C} _ {4} (z) \psi_ {2 p x} = \psi_ {2 p y}.\tag{9.40}
$$

The original function has a positive region in front of the x-z plane and a negative region behind the x-z plane. The symmetry operator has moved the positive region in the same way that it moves a rigid object, and similarly for the negative region.

Symmetry operators can have eigenfunctions, like any other operator. The result of operating on an eigenfunction of the operator is equal to a constant (the eigenvalue) times the original function. If a symmetry operator leaves a function unchanged, its eigenvalue is equal to unity. The only other possible eigenvalue for a symmetry operator is -1.

EXERCISE 9.12 ▶ Find $\hat{i}\psi_{2px}$ . Show that $\psi_{2px}$ is an eigenfunction of the inversion operator, and find its eigenvalue.

The importance of symmetry operators in the study of electronic wave functions arises from the fact that two commuting operators can have a set of common eigenfunctions. In quantum mechanical theory, there is an operator corresponding to each mechanical variable. The most important quantum mechanical operator is the Hamiltonian operator, which corresponds to the energy. In the Born–Oppenheimer approximation, the electronic Hamiltonian operator operates on the coordinates of the electrons, but treats the nuclear coordinates as constants. This operator has a term in it that is the operator for multiplication by the potential energy as a function of the positions of the nuclei and electrons. If a symmetry operator leaves the potential energy unchanged when applied to the electrons' positions, it will commute with the Hamiltonian operator, and the eigenfunctions of the Hamiltonian operator can also be eigenfunctions of the symmetry operator.

A symmetry operator leaves the potential energy unchanged if it moves each electron so that after the motion it is the same distance from each nucleus or the same distance from another nucleus of the same charge as it was prior to the motion. If this is the case, the symmetry operator commutes with the Born-Oppenheimer Hamiltonian. There is another way to see if the symmetry operator will commute with the electronic Hamiltonian. Apply it to the nuclei and not to the electrons. If the symmetry operator either leaves a nucleus in the same position or places it in the original position of a nucleus of the same type, it belongs to the nuclear framework. The symmetry operators that belong to the nuclear framework will commute with the electronic Hamiltonian when applied to the electrons.

EXERCISE 9.13 ▶
vacuum is

The potential energy of two charges $Q_{1}$ and $Q_{2}$ in a

$$
\mathcal {V} = \frac {Q _ {1} Q _ {2}}{4 \pi \epsilon_ {0} r _ {12}}
$$

where $r_{12}$ is the distance between the charges and $\varepsilon_{0}$ is a constant called the permittivity of a vacuum. If a hydrogen molecule is placed so that the origin is midway between the two nuclei and the nuclei are on the z axis, show that the inversion operator $\hat{i}$ and the reflection operator $\hat{\sigma}_{h}$ do not change the potential energy if applied to the electrons but not to the nuclei.

Full exploitation of the symmetry properties of electronic wave functions requires the use of group theory, which we briefly introduce in a later section of this chapter. However, we state some facts:

1. If a molecule has a permanent dipole moment, the dipole vector must lie along a proper rotation axis and in a plane of symmetry.

2. A molecule with an improper rotation axis cannot be optically active.

3. A given object, such as a nuclear framework of a molecule, cannot possess a completely arbitrary collection of symmetry elements. Group theory can tell us which ones can belong together.

## 9.3 Matrix Algebra

A matrix is an array or list of numbers arranged in rows, columns, and so forth. Most of the matrices that you will encounter are two-dimensional arrays. That is, they have rows and columns. If the matrix A has m rows and n columns, it is called an m by n matrix and is written

$$
\mathbf {A} = \left[ \begin{array}{l l l l l} a _ {11} & a _ {12} & a _ {13} & \dots & a _ {1 n} \\ a _ {21} & a _ {22} & a _ {23} & \dots & a _ {2 n} \\ \dots & & & & \\ \dots & & & & \\ a _ {m 1} & a _ {m 2} & a _ {m 3} & \dots & a _ {m n} \end{array} \right].\tag{9.41}
$$

The quantities that are entries in the two-dimensional list are called matrix elements. The brackets written on the left and right are included to show where the matrix starts and stops. If m = n, we say that the matrix is a square matrix. A vector in ordinary space can be represented as a list of three components. We consider a matrix with one row and n columns to be a row vector. We consider a matrix with m rows and one column to be a column vector. We now refer to ordinary numbers as scalars, to distinguish them from vectors and matrices.

Matrices and mathematical operators have some things in common. There is a well-defined matrix algebra in which matrices are operated on and this matrix algebra is similar to operator algebra. Two matrices are equal to each other if and only if both have the same number of rows and the same number of columns and if every element of one is equal to the corresponding element of the other. The sum of two matrices is defined by

$$
\mathbf {C} = \mathbf {A} + \mathbf {B} \quad \text { if   and   only   if } c _ {i j} = a _ {i j} + b _ {i j} \text { for   every } i \text { and } j.\tag{9.42}
$$

Two matrices can be added only if they have the same number of rows and the same number of columns. The product of a scalar and a matrix is defined by

$$
\mathbf {B} = c \mathbf {A} \quad \text { if   and   only   if } b _ {i j} = c a _ {i j} \text { for   every } i \text { and } j,\tag{9.43}
$$

where c is a scalar and A is a matrix. The product of two matrices is similar to the scalar product of two vectors. If we rename the components of two vectors $F_{1}$ , $F_{2}$ , $F_{3}$ , $G_{1}$ , $G_{2}$ , and $G_{3}$ instead of $Fx$ , $F_{y}$ , $F_{z}$ , $G_{x}$ , $G_{y}$ , and $G_{z}$ , we can write the scalar product of two vectors in Eq. (2.70) in the form

$$
\mathbf {F} \cdot \mathbf {G} = F _ {1} G _ {1} + F _ {2} G _ {2} + F _ {3} G _ {3} = \sum_ {k = 1} ^ {3} F _ {k} G _ {k}.\tag{9.44}
$$

We define matrix multiplication in a way that is similar to this. If A, B, and C are matrices such that C is the matrix product AB, we define

$$
c _ {i j} = \sum_ {k = 1} ^ {n} a _ {i k} b _ {k j}.\tag{9.45}
$$

In this equation, n is the number of columns in A, which must equal the number of rows in the matrix B. The matrix C will have as many rows as A and as many columns as B.

We can think of the vector $\mathbf{F}$ in Eq. (9.44) as a row vector with one row and three columns and the vector $\mathbf{G}$ as being a column vector with three rows and one column. Equation (9.44) is then a special case of Eq. (9.45):

$$
\mathbf {F} \cdot \mathbf {G} = [ F _ {1} F _ {2} F _ {3} ] \left[ \begin{array}{l} G _ {1} \\ G _ {2} \\ G _ {3} \end{array} \right].
$$

Row and column vectors can have a number of elements other than three, just as a matrix can have a number of rows and columns other than three.

The scalar product $F \cdot G$ is a scalar, which is equivalent to a matrix with one row and one column. If A is a 2 by 3 matrix and B is a 3 by 3 matrix, we can write their matrix product as

$$
\mathbf {A B} = \left[ \begin{array}{l l l} a _ {11} & a _ {12} & a _ {13} \\ a _ {21} & a _ {22} & a _ {23} \end{array} \right] \left[ \begin{array}{l l l} b _ {11} & b _ {12} & b _ {13} \\ b _ {21} & b _ {22} & b _ {23} \\ b _ {31} & b _ {32} & b _ {33} \end{array} \right] = \left[ \begin{array}{l l l} c _ {11} & c _ {12} & c _ {13} \\ c _ {21} & c _ {22} & c _ {23} \end{array} \right] = \mathbf {C}.\tag{9.46}
$$

Each element in C is obtained in the same way as taking a scalar product of a row from A and a column from B. For a particular element in C, we take the row in A which is in the same position as the row in C containing the desired element, and the column in B which is in the same position as the column in C containing the desired element and sum the products of the respective elements.

EXAMPLE 9.9 Find the matrix product

$$
\left[ \begin{array}{r r r} 1 & 0 & 2 \\ 0 & - 1 & 1 \\ 0 & 0 & 1 \end{array} \right] \left[ \begin{array}{r r r} 0 & 0 & 2 \\ 3 & 0 & 1 \\ 1 & 1 & - 1 \end{array} \right].
$$

SOLUTION

$$
\left[ \begin{array}{r r r} 1 & 0 & 2 \\ 0 & - 1 & 1 \\ 0 & 0 & 1 \end{array} \right] \left[ \begin{array}{r r r} 0 & 0 & 2 \\ 3 & 0 & 1 \\ 1 & 1 & - 1 \end{array} \right] = \left[ \begin{array}{r r r} 2 & 2 & 0 \\ - 2 & 1 & - 2 \\ 1 & 1 & - 1 \end{array} \right].
$$

EXERCISE 9.14 ▶ Find the two matrix products

$$
\left[ \begin{array}{r r r} 1 & 2 & 3 \\ 3 & 2 & 1 \\ 1 & - 1 & 2 \end{array} \right] \left[ \begin{array}{r r r} 1 & 3 & 2 \\ 2 & 2 & - 1 \\ - 2 & 1 & - 1 \end{array} \right] \quad \text {and} \quad \left[ \begin{array}{r r r} 1 & 3 & 2 \\ 2 & 2 & - 1 \\ - 2 & - 1 & - 1 \end{array} \right] \left[ \begin{array}{r r r} 1 & 2 & 3 \\ 3 & 2 & 1 \\ 1 & - 1 & 2 \end{array} \right].
$$

The left factor in one product is equal to the right factor in the other product, and vice versa. Are the two products equal?

![[e41132b43af9e25d3dfbb0c70c57be0bed266fe9f087f9e791d4aa662f9fd35f.jpg]]

As you can see, matrix multiplication with fairly large matrices can involve a lot of computation. Computer programs can be written to carry out the process, and such programs are built into Mathematica and also into computer languages such as BASIC so that a matrix multiplication can be carried out with a single statement.

Two square matrices can be multiplied together in either order. However, the multiplication is not always commutative. It is possible that

$$
\mathbf {A B} \neq \mathbf {B A} (\text { in   some   cases })\tag{9.47}
$$

However, matrix multiplication is associative,

$$
\mathbf {A} (\mathbf {B C}) = (\mathbf {A B}) \mathbf {C}\tag{9.48}
$$

Matrix multiplication and addition are distributive,

$$
\boxed {\mathbf {A} (\mathbf {B} + \mathbf {C}) = \mathbf {A B} + \mathbf {A C}}.\tag{9.49}
$$

Show that the properties of Eqs. (9.48) and (9.49) are obeyed by the particular matrices

$$
\mathbf {A} = \left[ \begin{array}{l l l} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{array} \right] \quad \mathbf {B} = \left[ \begin{array}{r r r} 0 & 2 & 2 \\ - 3 & 1 & 2 \\ 1 & - 2 & - 3 \end{array} \right] \quad \mathbf {C} = \left[ \begin{array}{l l l} 1 & 0 & 1 \\ 0 & 3 & - 2 \\ 2 & 7 & - 7 \end{array} \right].
$$

Matrix multiplication is similar to operator multiplication. Both are associative and distributive but not necessarily commutative. In Section 8.1 we defined an identity operator, and we now define an identity matrix E. We require

$$
\mathbf {E} \mathbf {A} = \mathbf {A} \mathbf {E} = \mathbf {A}.
$$

The fact that we require E to be the identity matrix when multiplied on either side of A requires both A and E to be square matrices. In fact, only with square matrices will we get a strict similarity between operator algebra and matrix algebra.

An identity matrix can have any number of rows and columns. It has the form

$$
\mathbf {E} = \left[ \begin{array}{c c c c c} 1 & 0 & 0 & \dots & 0 \\ 0 & 1 & 0 & \dots & 0 \\ 0 & 0 & 1 & \dots & 0 \\ \dots & \dots & \dots & \dots & \dots \\ 0 & 0 & 0 & \dots & 1 \end{array} \right].\tag{9.50}
$$

The diagonal elements of any square matrix are those with both indices equal. The diagonal elements of E are all equal to 1 and are the only nonzero elements. This can be represented by the equation

$$
e _ {i j} = \delta_ {i j} = \left\{ \begin{array}{l l} 1 & \text { if } i = j \\ 0 & \text { if } i \neq j. \end{array} \right.
$$

The quantity $\delta_{ij}$ is called the Kronecker delta.

EXERCISE 9.15 ▶

Show by explicit matrix multiplication that

$$
\left[ \begin{array}{c c c c} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{array} \right] \left[ \begin{array}{c c c c} a _ {11} & a _ {12} & a _ {13} & a _ {14} \\ a _ {21} & a _ {22} & a _ {31} & a _ {41} \\ a _ {31} & a _ {31} & a _ {31} & a _ {41} \\ a _ {41} & a _ {41} & a _ {31} & a _ {41} \end{array} \right] = \left[ \begin{array}{c c c c} a _ {11} & a _ {12} & a _ {13} & a _ {14} \\ a _ {21} & a _ {21} & a _ {31} & a _ {41} \\ a _ {31} & a _ {31} & a _ {31} & a _ {41} \\ a _ {41} & a _ {41} & a _ {31} & a _ {41} \end{array} \right].
$$


Just as in operator algebra, we do not define division by a matrix. In operator algebra we defined an inverse operator, which undoes the effect of a given operator. We define now the inverse of a matrix. Only square matrices have inverses. We denote the inverse of A by $A^{-1}$ , so that

$$
\boxed {\mathbf {A} \mathbf {A} ^ {- 1} = \mathbf {E}}.\tag{9.51}
$$

This multiplication of a matrix by its inverse is commutative, so that A is also the inverse of $A^{-1}$ .

From Eq. (9.45) we can write the second equality in Eq. (9.51) in terms of matrix elements:

$$
\sum_ {k = 1} ^ {n} a _ {i k} (A ^ {- 1}) _ {k j} = \delta_ {i j},\tag{9.52}
$$

where we write $(\mathbf{A}^{-1})_{kj}$ for the kj element of $A^{-1}$ . This equation represents a set of simultaneous linear algebraic equations, one for each value of i and each value of j, so that there are just enough equations to determine the elements of $A^{-1}$ .

One method for finding $A^{-1}$ is called Gauss–Jordan elimination, which is a method of solving simultaneous linear algebraic equations. It consists of a set of operations to be applied to Eq. (9.51). In order to maintain a valid equation, these operations must be applied to both sides of the equation. The first operation is applied to the matrix A and to the matrix E on the right-hand side of the equation, but not to the unknown matrix $A^{-1}$ . This is analogous to the fact that if you have an equation ax = c, you would multiply a and c by some factor, but not multiply both a and x by the factor to maintain a valid equation. The goal of the operations is to transform Eq. (9.51) into

$$
\mathbf {E} (\mathbf {A} ^ {- 1}) = \mathbf {D}\tag{9.53}
$$

so that $A^{-1}$ will be the same matrix as D.

In order to carry out the procedure conveniently, we write the matrix A and the matrix E explicitly side by side and carry out operations on each element of the same row in each matrix. For example, we might multiply every element in a given row of A by some constant and multiply every element in the same row of E by the same constant. This is an example of a row operation. If we carry it out we still have a valid equation. Another row operation that we can apply is to subtract one row of A from another row of A, element by element, while doing the same thing to E. This amounts to subtracting the left-hand sides of pairs of equations and subtracting at the same time the right-hand sides of the equations, which produces valid equations. We can then replace one of the row by the difference of two rows. Successive application of these two row operations is sufficient to transform the left factor of a matrix product into the identity matrix. If we apply them in the appropriate way to Eq. (9.51), we can transform it into Eq. (9.53). We illustrate the procedure in the following example.

EXAMPLE 9.10 Find the inverse of the matrix

$$
\mathbf {A} = \left[ \begin{array}{l l l} 2 & 1 & 0 \\ 1 & 2 & 2 \\ 0 & 1 & 1 \end{array} \right].
$$

SOLUTION ▶ Our version of Eq. (9.51) is

$$
\left[ \begin{array}{c c c} 2 & 1 & 0 \\ 1 & 2 & 1 \\ 0 & 1 & 2 \end{array} \right] \left[ \begin{array}{c c c} (A ^ {- 1}) _ {11} & (A ^ {- 1}) _ {12} & (A ^ {- 1}) _ {13} \\ (A ^ {- 1}) _ {21} & (A ^ {- 1}) _ {22} & (A ^ {- 1}) _ {23} \\ (A ^ {- 1}) _ {22} & (A ^ {- 1}) _ {32} & (A ^ {- 1}) _ {33} \end{array} \right] = \left[ \begin{array}{c c c} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{array} \right].
$$

In order to carry out the row operations we write the two matrices on which we operate side by side and perform the same operations on the same row of both matrices. The matrix that is not operated on, $\mathbf{A}^{-1}$ , is not written. We don't know what its elements are so we couldn't operate on it.

$$
\left[ \begin{array}{c c c c c c c} 2 & 1 & 0 & \vdots & 1 & 0 & 0 \\ 1 & 2 & 1 & \vdots & 0 & 1 & 0 \\ 0 & 1 & 2 & \vdots & 0 & 0 & 1 \end{array} \right]
$$

It is usual to clear out the columns from left to right. We first want to get a zero in the place of $a_{21}$ , which is now equal to 1. We multiply the first row by $\frac{1}{2}$ , obtaining

$$
\left[ \begin{array}{c c c c c c c} 1 & \frac {1}{2} & 0 & \vdots & \frac {1}{2} & 0 & 0 \\ 1 & 2 & 1 & \vdots & 0 & 1 & 0 \\ 0 & 1 & 2 & \vdots & 0 & 0 & 1 \end{array} \right].
$$

We subtract the first row from the second and replace the second row by this difference. The result is

$$
\left[ \begin{array}{c c c c c c c} 1 & \frac {1}{2} & 0 & \vdots & \frac {1}{2} & 0 & 0 \\ 0 & \frac {3}{2} & 1 & \vdots & - \frac {1}{2} & 1 & 0 \\ 0 & 1 & 2 & \vdots & 0 & 0 & 1 \end{array} \right].
$$

We say that we have used the element $a_{11}$ as the pivot element in this procedure. The left column is now as we want it to be. We now use the $a_{22}$ element as the pivot element to clear the second column. We multiply the second row by $\frac{1}{3}$ and replace the first row by the difference of the first row and the second to obtain

$$
\left[ \begin{array}{c c c c c c c} 1 & 0 & - \frac {1}{3} & \vdots & \frac {2}{3} & - \frac {1}{3} & 0 \\ 0 & \frac {1}{2} & \frac {1}{3} & \vdots & - \frac {1}{6} & \frac {1}{3} & 0 \\ 0 & 1 & 2 & \vdots & 0 & 0 & 1 \end{array} \right].
$$

We now multiply the second row by 2, subtract this row from the third row, and replace the third row by the difference. The result is

$$
\left[ \begin{array}{c c c c c c c} 1 & 0 & - \frac {1}{3} & \vdots & \frac {2}{3} & - \frac {1}{3} & 0 \\ 0 & 1 & \frac {2}{3} & \vdots & - \frac {1}{3} & \frac {2}{3} & 0 \\ 0 & 0 & \frac {4}{3} & \vdots & \frac {1}{3} & - \frac {2}{3} & 1 \end{array} \right].
$$

We now multiply the third row by $\frac{1}{2}$ in order to use the $a_{33}$ element as the pivot element. We subtract the third row from the second and replace the second row by the difference, obtaining

$$
\left[ \begin{array}{c c c c c c c} 1 & 0 & - \frac {1}{3} & \vdots & \frac {2}{3} & - \frac {1}{3} & 0 \\ 0 & 1 & 0 & \vdots & - \frac {1}{2} & 1 & - \frac {1}{2} \\ 0 & 0 & \frac {2}{3} & \vdots & \frac {1}{6} & - \frac {1}{3} & \frac {1}{2} \end{array} \right].
$$

We now multiply the third row by $\frac{1}{2}$ , add it to the first row, and replace the first row by the sum. The result is

$$
\left[ \begin{array}{c c c c c c c} 1 & 0 & 0 & \vdots & \frac {3}{4} & - \frac {1}{2} & \frac {1}{4} \\ 0 & 1 & 0 & \vdots & - \frac {1}{2} & 1 & - \frac {1}{2} \\ 0 & 0 & \frac {1}{3} & \vdots & \frac {1}{12} & - \frac {1}{6} & \frac {1}{4} \end{array} \right].
$$

The final row operation is multiplication of the third row by 3 to obtain

$$
\left[ \begin{array}{c c c c c c c} 1 & 0 & 0 & \vdots & \frac {3}{4} & - \frac {1}{2} & \frac {1}{4} \\ 0 & 1 & 0 & \vdots & - \frac {1}{2} & 1 & - \frac {1}{2} \\ 0 & 0 & 1 & \vdots & \frac {1}{4} & - \frac {1}{2} & \frac {3}{4} \end{array} \right].
$$

We now reconstitute the matrix equation by placing the identity matrix on the left to the left of the $A^{-1}$ matrix. This produces a matrix equation such that the left-hand side of the equation is $EA^{-1}$ and the right-hand side is the right half of the double matrix. Therefore, the right half of this double matrix is $A^{-1}$ :

$$
\mathbf {A} ^ {- 1} = \left[ \begin{array}{c c c} \frac {3}{4} & - \frac {1}{2} & \frac {1}{4} \\ - \frac {1}{2} & 1 & - \frac {1}{2} \\ \frac {1}{4} & - \frac {1}{2} & \frac {3}{4} \end{array} \right].
$$

EXERCISE 9.16 ▶ a. Show that $\mathbf{A}\mathbf{A}^{-1} = \mathbf{E}$ and that $\mathbf{A}^{-1}\mathbf{A} = \mathbf{E}$ for the matrices of the preceding example.

b. Find the inverse of the matrix

$$
\mathbf {A} = \left[ \begin{array}{l l} 1 & 2 \\ 3 & 4 \end{array} \right]
$$


Only square matrices have inverses, but not all square matrices have inverses. Associated with each square matrix is a determinant, which we define in the next section. If the determinant of a square matrix vanishes, the matrix is said to be singular. A singular matrix has no inverse.

We conclude this section with the definition of several terms that apply to square matrices. The trace of a matrix is the sum of the diagonal elements of the matrix:

$$
\operatorname{Tr} (\mathbf {A}) = \sum_ {i = 1} ^ {n} a _ {i i}.\tag{9.54}
$$

The trace is sometimes called the spur, from the German word Spur, which means track or trace. For example, the trace of the n by n identity matrix is equal to n. A matrix in which all the elements below the diagonal elements vanish is called an upper triangular matrix. A matrix in which all the elements above the diagonal elements vanish is called a lower triangular matrix, and a matrix in which all the elements except the diagonal elements vanish is called a diagonal matrix. The matrix in which all of the elements vanish is called the null matrix or the zero matrix. The transpose of a matrix is obtained by replacing the first column by the first row, the second column by the second row of the original matrix, and so on. The transpose of A is denoted by $\tilde{A}$ (pronounced “A tilde”),

$$
(\tilde {\mathbf {A}}) _ {i j} = \tilde {a} _ {i j} = a _ {j i}.\tag{9.55}
$$

If a matrix is equal to its transpose, it is a symmetric matrix. The matrix in Example 9.10 is symmetric, and its inverse is also symmetric.

The hermitian conjugate of a matrix is obtained by taking the complex conjugate of each element and then taking the transpose of the resulting matrix. If a matrix has only real elements, the hermitian conjugate is the same as the transpose. The hermitian conjugate is also called the adjoint (mostly by physicists) and the associate (mostly by mathematicians, who use the term “adjoint” for something else). The hermitian conjugate is denoted by $A^{\dagger}$ .

$$
(\mathbf {A} ^ {\dagger}) _ {i j} = a _ {j i} ^ {*}.\tag{9.56}
$$

A matrix that is equal to its hermitian conjugate is said to be a hermitian matrix.

An orthogonal matrix is one whose inverse is equal to its transpose. If A is orthogonal, then

$$
\mathbf {A} ^ {- 1} = \tilde {\mathbf {A}} \quad (\text { orthogonal   matrix }).\tag{9.57}
$$

A unitary matrix is one whose inverse is equal to its hermitian conjugate. If A is unitary, then

$$
\mathbf {A} ^ {- 1} = \mathbf {A} ^ {\dagger} = \tilde {\mathbf {A}} ^ {*} \quad (\text { unitary   matrix }).\tag{9.58}
$$

EXERCISE 9.17 ▶ Which of the following matrices are diagonal, symmetric, hermitian, orthogonal, or unitary?

$$
\text {a.} \left[ \begin{array}{c c} 1 & 0 \\ 0 & 1 \end{array} \right] \quad \text {b.} \left[ \begin{array}{c c} 1 & 0 \\ 1 & 1 \end{array} \right] \quad \text {c.} \left[ \begin{array}{c c} i & i \\ 0 & 1 \end{array} \right] \quad \text {d.} \left[ \begin{array}{c c} 0 & i \\ - i & 1 \end{array} \right].
$$


## Determinants

Associated with every square matrix is a quantity called a determinant. If the elements of the matrix are constants, the determinant is a single constant, defined as a certain sum of products of subsets of the elements. If the matrix has n rows and columns, each term in the sum making up the determinant will have n factors in it. The determinant of a 2 by 2 matrix is defined as the product of the diagonal elements minus the product of the off-diagonal elements:

$$
\boxed {\det (\mathbf {A}) = \left| \begin{array}{c c} a _ {11} & a _ {12} \\ a _ {21} & a _ {22} \end{array} \right| = a _ {11} a _ {22} - a _ {12} a _ {21}.}\tag{9.59}
$$

The determinant is written in much the same way as the matrix, except that straight vertical lines are used on the left and right instead of brackets.

EXAMPLE 9.11 Find the value of the determinant

$$
\left| \begin{array}{c c} 3 & - 17 \\ 1 & 5 \end{array} \right|.
$$

SOLUTION ▶ $\left|\begin{array}{cc}3 & -17 \\ 1 & 5\end{array}\right|=(3)(5)-(-17)(1)=15+17=32.$

Finding the value of a determinant larger than 2 by 2 requires a number of operations. One way to do it is by expanding by minors, as follows:

1. Pick a row or a column of the determinant. Any row or column will do, but one with zeros in it will minimize the work.

2. The determinant is equal to a sum of terms, one for each element in this row or column. Each term consists of an element of the chosen row or column times the minor of that element, with an assigned sign, either positive or negative. The minor of an element in a determinant is obtained by deleting the row and the column containing that element. It is a determinant with one less row and one less column than the original determinant.

3. Determine the sign assigned to a term as follows: Count the number of steps of one row or one column required to get from the upper left element to the element whose minor is desired. If the number of steps is odd, the sign is negative. If the number of steps is even (including zero), the sign is positive.

4. Repeat the entire process with each determinant in the expansion until you have a sum of 2 by 2 determinants, which can be evaluated by Eq. (9.59).

The cofactor of an element in a determinant is the minor multiplied by the appropriate factor of 1 or -1, determined as in step 3. In addition to the minor which we have defined, other minors of different order are defined, in which two or more rows and columns are deleted. We do not need to use these and will not discuss them.

EXAMPLE 9.12 Expand the 3 by 3 determinant of the matrix A by minors.

$$
\begin{array}{r l} \left| \begin{array}{c c c} a _ {11} & a _ {12} & a _ {13} \\ a _ {21} & a _ {22} & a _ {23} \\ a _ {31} & a _ {32} & a _ {33} \end{array} \right| & = a _ {11} \left| \begin{array}{c c} a _ {22} & a _ {23} \\ a _ {32} & a _ {33} \end{array} \right| - a _ {12} \left| \begin{array}{c c} a _ {21} & a _ {23} \\ a _ {31} & a _ {33} \end{array} \right| + a _ {13} \left| \begin{array}{c c} a _ {21} & a _ {22} \\ a _ {31} & a _ {32} \end{array} \right|. \\ & = a _ {11} a _ {22} a _ {33} - a _ {11} a _ {23} a _ {32} - a _ {12} a _ {21} a _ {33} + a _ {12} a _ {23} a _ {31} \\ & \quad + a _ {13} a _ {21} a _ {32} - a _ {13} a _ {22} a _ {31}. \end{array}
$$

EXERCISE 9.18 ▶

Expand the following determinant by minors:

$$
\left| \begin{array}{c c c} 3 & 2 & 0 \\ 7 & - 1 & 5 \\ 2 & 3 & 4 \end{array} \right|.
$$

![[8bb30045d2b9e7e34aab97fc012636b25e72300dae4162cff8787d5e6acfc523.jpg]]

EXERCISE 9.19 ▶

Expand the 4 by 4 determinant by minors

$$
\left| \begin{array}{c c c c} a _ {11} & a _ {12} & a _ {13} & a _ {14} \\ a _ {21} & a _ {22} & a _ {23} & a _ {24} \\ a _ {31} & a _ {32} & a _ {33} & a _ {34} \\ a _ {41} & a _ {42} & a _ {43} & a _ {44} \end{array} \right.
$$

![[b6d1867646c87b8158a1ca6ce1d5ebc7e1e1abf9736750570afd142e4d42496a.jpg]]

Determinants have a number of important properties:

1. If two rows of a determinant are interchanged, the result will be a determinant whose value is the negative of the original determinant. The same is true if two columns are interchanged.

2. If two rows or two columns of a determinant are identical, the determinant has value zero.

3. If each element in one row or one column of a determinant is multiplied by the same quantity c the value of the new determinant is c times the value of the original determinant. Therefore, if an n by n determinant has every element multiplied by c, the new determinant is $c^{n}$ times the original determinant.

4. If every element in any one row or in any one column of a determinant is zero, the value of the determinant is zero.

5. If any row is replaced, element by element, by that row plus a constant times another row, the value of the determinant is unchanged. The same is true for

two columns. For example,

$$
\left| \begin{array}{l l l} a _ {11} + c a _ {12} & a _ {12} & a _ {13} \\ a _ {21} + c a _ {22} & a _ {22} & a _ {13} \\ a _ {31} + c a _ {32} & a _ {32} & a _ {33} \end{array} \right| = \left| \begin{array}{l l l} a _ {11} & a _ {12} & a _ {13} \\ a _ {21} & a _ {22} & a _ {23} \\ a _ {31} & a _ {32} & a _ {33} \end{array} \right|.\tag{9.60}
$$

6. The determinant of a triangular matrix (a triangular determinant) is equal to the product of the diagonal elements. For example,

$$
\left| \begin{array}{c c c} a _ {11} & 0 & 0 \\ a _ {22} & a _ {22} & 0 \\ a _ {21} & a _ {32} & a _ {33} \end{array} \right| = a _ {11} a _ {22} a _ {33}.\tag{9.61}
$$

7. The determinant of a matrix is equal to the determinant of the transpose of that matrix.

$$
\det (\tilde {\mathbf {A}}) = \det (\mathbf {A}).\tag{9.62}
$$

These properties can be verified using the expansion of a determinant by minors.

EXERCISE 9.20 ▶

(a) Find the value of the determinant

$$
\left| \begin{array}{c c c} 3 & 4 & 5 \\ 2 & 1 & 6 \\ 3 & - 5 & 10 \end{array} \right|.
$$

(b) Interchange the first and second columns and find the value of the resulting determinant.

(c) Replace the second column by the sum of the first and second columns and find the value of the resulting determinant.

(d) Replace the second column by the first, thus making two identical columns, and find the value of the resulting determinant.

![[532cd54d3e9aa7708e890bd5b9ba9c309e982f7d36a64e0bfe31b67b38c7ab06.jpg]]

There is an application of determinants in quantum chemistry that comes from Property 1. The electronic wave function of a system containing two or more electrons must change sign but keep the same magnitude if the coordinates of two of the electrons are interchanged (the wave function must be antisymmetric). For example, if $r_{1}$ and $r_{2}$ are the position vectors of two electrons and $\Psi$ is a multi-electron wave function, then the wave function must obey

$$
\Psi (\mathbf {r} _ {1}, \mathbf {r} _ {2}, \mathbf {r} _ {3}, \mathbf {r} _ {4}, \ldots , \mathbf {r} _ {n}) = - \Psi (\mathbf {r} _ {2}, \mathbf {r} _ {1}, \mathbf {r} _ {3}, \mathbf {r} _ {4}, \ldots , \mathbf {r} _ {n})\tag{9.63}
$$

with similar equations for exchanging any other pair of electrons' coordinates. Many approximate multi-electron wave functions are constructed as a product of one-electron wave functions, or orbitals. If $\psi_{1}, \psi_{2}$ , and so on, are orbitals such a wave function for n electrons is written as

$$
\Psi = \psi_ {1} (\mathbf {r} _ {1}) \psi_ {2} (\mathbf {r} _ {2}) \psi_ {3} (\mathbf {r} _ {3}) \psi_ {4} (\mathbf {r} _ {4}) \cdot \cdot \cdot \psi_ {n} (\mathbf {r} _ {n}).\tag{9.64}
$$

where $r_{1}, r_{2}, \cdots$ represent the coordinates of electron 1, electron 2, and so on. This wave function does not obey the antisymmetry condition of Eq. (9.63). A wave function that does obey this equation can be constructed as a Slater determinant. $^{3}$ The elements of this determinant are the orbital functions, so the determinant is equal to a function of the coordinates of all electrons:

$$
\Psi (\mathbf {r} _ {1}, \mathbf {r} _ {2}, \ldots , \mathbf {r} _ {n}) = \frac {1}{\sqrt {n !}} \left| \begin{array}{c c c c c} \psi_ {1} (\mathbf {r} _ {1}) & \psi_ {1} (\mathbf {r} _ {2}) & \psi_ {1} (\mathbf {r} _ {3}) & \dots & \psi_ {1} (\mathbf {r} _ {n}) \\ \psi_ {2} (\mathbf {r} _ {1}) & \psi_ {2} (\mathbf {r} _ {2}) & \psi_ {2} (\mathbf {r} _ {3}) & \dots & \psi_ {2} (\mathbf {r} _ {n}) \\ \psi_ {3} (\mathbf {r} _ {1}) & \psi_ {3} (\mathbf {r} _ {2}) & \psi_ {3} (\mathbf {r} _ {3}) & \dots & \psi_ {3} (\mathbf {r} _ {n}) \\ \ldots & \ldots & \ldots & \ldots & \ldots \\ \psi_ {n} (\mathbf {r} _ {1}) & \psi_ {n} (\mathbf {r} _ {2}) & \psi_ {n} (\mathbf {r} _ {3}) & \dots & \psi_ {n} (\mathbf {r} _ {n}) \end{array} \right|.\tag{9.65}
$$

The factor $1/\sqrt{n!}$ is a normalizing factor, which is not important to us now. The Slater determinant obeys the antisymmetry property, since interchanging $r_{1}$ and $r_{2}$ , for example, is the same as interchanging two columns, which changes the sign of the determinant. If we attempt to write such a wave function with two electrons in the same orbital (two of the $\psi$ factors identical), then two rows of the determinant are identical, and the entire determinant vanishes by Property 2. This is the Pauli exclusion principle, which states that no two electrons in the same atom or molecule can occupy the same orbital. $^{4}$

## 9.4 Matrix Algebra with Mathematica

As you have seen, matrix algebra can be tedious. Mathematica has all of the matrix operations built into it, so that you can form matrix products and carry out matrix inversion automatically. Mathematica treats matrices as lists of lists, with the elements of each row entered as a list. A list is entered inside curly brackets ("braces") with the elements separated by commas. A list of lists requires braces around the set of lists with braces and commas. For example, to enter the following 3 by 3 matrix

$$
\mathbf {A} = \left[ \begin{array}{l l l} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{array} \right],\tag{9.66}
$$

you would type in the following:

$$
\begin{array}{l} \text { Clear } [ a ] \\ a = \{\{1, 2, 3 \}, \{4, 5, 6 \}, \{7, 8, 9 \} \} \end{array}
$$

and press the “Enter” key or a “Shift-Return.” Mathematica will type the following:
In[1]:= a={{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}

Note that the symbol that we chose for the matrix name is in lower case and requires no auxiliary labels. You should start the names of all Mathematica variables with lowercase letters to avoid possible confusion with Mathematica operators and functions. If you want to see the matrix A in standard form, type the statement MatrixForm[a] and press the “Enter” key or the “Shift-Return.”

Mathematica treats vectors as a single list. It does not distinguish between row vectors and column vectors. If you want to enter a vector $v = (2, 4, 6)$ , you enter the components inside curly brackets separated by commas as follows:

$$
\mathrm{v} = \{2, 4, 6 \}
$$

followed by pressing the “Enter” key or a “Shift-return.” A diagonal matrix is entered as a single list inside square brackets. To enter the diagonal matrix

$$
\left[ \begin{array}{c c c} 1 & 0 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 4 \end{array} \right],\tag{9.67}
$$

use the statement

DiagonalMatrix[ $\{1,2,4\}$ ]

When you press "Enter" or "Shift-Return" you get the output

After two matrices A and B have been entered, a matrix multiplication is carried out by the statement

a.b

where you type a period between the symbols for the matrices. The product of a row vector with a matrix is accomplished with the statement

and a product of a matrix and a column vector is accomplished with the statement a.v

The inverse of a matrix is obtained with the statement

Inverse[a]

If the matrix is singular and does not have an inverse, Mathematica will tell you so. To obtain the determine of a square matrix A, use the statement

Remember the capitalization. Mathematica does not allow alternate choices to its statements.

EXERCISE 9.21 ▶ Obtain the inverse of the following matrix by hand. Then use Mathematica to verify your answer.

$$
\left[ \begin{array}{l l l} 1 & 3 & 0 \\ 3 & 0 & 4 \\ 1 & 2 & 0 \end{array} \right]
$$

Mathematica is a large and powerful program, and you can refer to the book by Wolfram listed at the end of this book to learn more about its use.

## 9.5 An Elementary Introduction to Group Theory

A mathematical group is a collection of elements with a single method for combining two elements of the group. We call the method multiplication in order to exploit the similarities of this operation with matrix and operator multiplication. The following requirements must be met:

1. If A and B are members of the group, and F is the product AB, then F must be a member of the group.

2. The group must contain the identity element, E, such that

$$
\mathbf {A} \mathbf {E} = \mathbf {E} \mathbf {A} = \mathbf {A}.\tag{9.68}
$$

3. The inverse of every element of the group must be a member of the group.

4. The associative law must hold:

$$
\mathbf {A} (\mathbf {B C}) = (\mathbf {A B}) \mathbf {C}.\tag{9.69}
$$

It is not necessary that the elements of the group commute with each other. That is, it is possible that

$$
\mathbf {A B} \neq \mathbf {B A} \quad (\text { possible   but   not   required })\tag{9.70}
$$

If all the members of the group commute, the group is called abelian. $^{5}$

The set of symmetry operators which “belong” to a symmetrical object in the sense of Section 9.3 form a group if we define operator multiplication to be the method of combining two elements of the group.

We illustrate this fact for the ammonia molecule, $NH_{3}$ . In its equilibrium conformation, the molecule is a triangular pyramid. $^{6}$ Figure 9.4a shows the nuclear framework as viewed from the first octant of the coordinate system, and Fig. 9.4b shows the framework as viewed from the positive end of the z axis. The molecule is placed in the coordinate system in the conventional way, with the center of mass at the origin and the rotation axis of highest order (largest value of n) along the z axis.

The symmetry elements of the molecule are shown in the figure. The symmetry operators that belong to the nuclear framework are $\hat{E}$ , $\hat{C}_{3}$ , $\hat{C}_{3}^{2}$ and the three reflection operators corresponding to vertical mirror planes passing through each of the three hydrogen nuclei, which we call $\hat{\sigma}_{a}$ , $\hat{\sigma}_{b}$ , and $\hat{\sigma}_{c}$ . The square of the $\hat{C}_{3}$ operator is included because we must include the inverse of all operators in the group and $\hat{C}_{3}^{2}$ is the inverse of $\hat{C}_{3}$ .

We now satisfy ourselves that the four conditions to have a group are met:

Condition 1. The product of any two members of the group must be a member of the group. We show this by constructing a multiplication table, as shown in Table 9.1. The operators listed in the first column of the table are used as the left factor, and the operators listed in the first row of the table are used as the right factor in a product. We must specify which factor comes first because the operators do not necessarily commute. The entries in the table are obtained as in the example:

![[5e3b0660007ee5a5ee31e33320754a0d2fb301dc6c994530e877e6f3bd95fc6a.jpg]]  
Figure 9.4 ▶ (a) The $NH_{3}$ molecule in its coordinate axes, with symmetry elements shown (after Levine). (b) The $NH_{3}$ molecule viewed from the positive z axis (after Levine).

TABLE 9.1 ▶ Multiplication Table for the Symmetry Operators of the NH₃ Molecule

<table><tr><td></td><td> $\hat{E}$ </td><td> $\hat{C}_{3}$ </td><td> $\hat{C}_{3}^{2}$ </td><td> $\hat{\sigma}_{a}$ </td><td> $\hat{\sigma}_{b}$ </td><td> $\hat{\sigma}_{c}$ </td></tr><tr><td> $\hat{E}$ </td><td> $\hat{E}$ </td><td> $\hat{C}_{3}$ </td><td> $\hat{C}_{3}^{2}$ </td><td> $\hat{\sigma}_{a}$ </td><td> $\hat{\sigma}_{b}$ </td><td> $\hat{\sigma}_{c}$ </td></tr><tr><td> $\hat{C}_{3}$ </td><td> $\hat{C}_{3}$ </td><td> $\hat{C}_{3}^{2}$ </td><td> $\hat{E}$ </td><td> $\hat{\sigma}_{c}$ </td><td> $\hat{\sigma}_{a}$ </td><td> $\hat{\sigma}_{b}$ </td></tr><tr><td> $\hat{C}_{3}^{2}$ </td><td> $\hat{C}_{3}^{2}$ </td><td> $\hat{E}$ </td><td> $\hat{C}_{3}$ </td><td> $\hat{\sigma}_{b}$ </td><td> $\hat{\sigma}_{c}$ </td><td> $\hat{\sigma}_{a}$ </td></tr><tr><td> $\hat{\sigma}_{a}$ </td><td> $\hat{\sigma}_{a}$ </td><td> $\hat{\sigma}_{b}$ </td><td> $\hat{\sigma}_{c}$ </td><td> $\hat{E}$ </td><td> $\hat{C}_{3}$ </td><td> $\hat{C}_{3}^{2}$ </td></tr><tr><td> $\hat{\sigma}_{b}$ </td><td> $\hat{\sigma}_{b}$ </td><td> $\hat{\sigma}_{c}$ </td><td> $\hat{\sigma}_{a}$ </td><td> $\hat{C}_{3}^{2}$ </td><td> $\hat{E}$ </td><td> $\hat{C}_{3}$ </td></tr><tr><td> $\hat{\sigma}_{c}$ </td><td> $\hat{\sigma}_{c}$ </td><td> $\hat{\sigma}_{a}$ </td><td> $\hat{\sigma}_{b}$ </td><td> $\hat{C}_{3}$ </td><td> $\hat{C}_{3}^{2}$ </td><td> $\hat{E}$ </td></tr></table>

EXAMPLE 9.13 Find the product $\hat{\sigma}_c\hat{C}_3$ .

SOLUTION ▶ Both of these operators leave the nitrogen nucleus in its original location. The $\hat{C}_{3}$ operator moves the hydrogen nucleus originally at the $\sigma_{a}$ plane to the $\sigma_{b}$ plane, the nucleus originally at the $\sigma_{b}$ plane to the $\sigma_{c}$ plane, and the nucleus originally at the $\sigma_{c}$ plane to the $\sigma_{a}$ plane. The $\hat{\sigma}_{c}$ operator reflects in the $\sigma_{c}$ plane, so that it exchanges the nuclei at the $\sigma_{a}$ and $\sigma_{b}$ planes. It thus returns the nucleus originally at the $\sigma_{c}$ plane to its original position and moves the nucleus originally at the $\sigma_{c}$ plane to the $\sigma_{b}$ plane. This is the same as the effect that the $\hat{\sigma}_{a}$ operator would have, so

$$
\hat {\sigma} _ {c} \hat {C} _ {3} = \hat {\sigma} _ {a}.
$$

EXERCISE 9.22 ▶

Verify several of the entries in Table 9.1.

Some pairs of operators in this group commute, whereas others do not. For example, $\hat{C}_3\hat{\sigma}_c = \hat{\sigma}_b$ , whereas $\hat{\sigma}_c\hat{C}_3 = \hat{\sigma}_a$ .

Condition 2. The group does contain the identity operator, $\hat{E}$ .

Condition 3. The inverse of every operator is in the group. Each reflection operator is its own inverse, and the inverse of $\hat{C}_3$ is $\hat{C}_3^2$ .

Condition 4. The multiplication operation is associative, because operator multiplication is always associative.

A group that consists of point symmetry operators is called a point group. There is only a limited number of point groups that exist, and each is assigned a symbol, called a Schoenflies symbol. The point group of the $NH_{3}$ molecule is called the $C_{3v}$ group. This symbol is chosen because the principal rotation axis is a $C_{3}$ axis, and because there are vertical mirror planes. You can communicate what the symmetry properties of the $NH_{3}$ molecule are by saying that it has $C_{3v}$ symmetry. Flow charts have been constructed for the routine assignment of Schoenflies symbols. $^{7}$

The $H_{2}O$ molecule belongs to the $C_{2v}$ point group, which contains the operators $\hat{E}$ , $\hat{C}_{2}$ , and two reflection operators, one whose mirror plane is the plane of the nuclei and one whose mirror plane bisects the angle between the bonds and is perpendicular to the first.

EXERCISE 9.23 ▶ Obtain the multiplication table for the $C_{2v}$ point group and show that it satisfies the conditions to be a group.

## Symmetry Operators and Matrices

Operator algebra and matrix algebra are quite similar, and matrices can be used to represent symmetry operators. A set of matrices that represent all of the elements of a group is called a representation of that group. Equation (9.28) represents the action of a general symmetry operator, $\hat{A}$ , on the location of a point. Let the original location of the point be given by the Cartesian coordinates $(x, y, z)$ , and the final coordinates be given by $(x', y', z')$ :

$$
\hat {A} (x, y, z) = \left(x ^ {\prime}, y ^ {\prime}, z ^ {\prime}\right).\tag{9.71}
$$

If we represent the position vectors by 3 by 1 matrices (column vectors) this can be written as a matrix equation:

$$
{\left[ \begin{array}{l l l} a _ {11} & a _ {12} & a _ {13} \\ a _ {21} & a _ {22} & a _ {23} \\ a _ {31} & a _ {32} & a _ {33} \end{array} \right]} {\left[ \begin{array}{l} x \\ y \\ z \end{array} \right]} = {\left[ \begin{array}{l} x ^ {\prime} \\ y ^ {\prime} \\ z ^ {\prime} \end{array} \right]}\tag{9.72}
$$

Equation (9.72) is the same as three ordinary equations:

$$
a _ {11} x + a _ {12} y + a _ {13} z = x ^ {\prime}\tag{9.73a}
$$

$$
a _ {21} x + a _ {22} y + a _ {23} z = y ^ {\prime}\tag{9.73b}
$$

$$
a _ {31} x + a _ {32} y + a _ {33} z = z ^ {\prime}.\tag{9.73c}
$$

We can obtain the elements of the matrix that represents $\hat{A}$ by comparing these equations with the equations obtained in Section 9.2 for various symmetry operators. For example, in the case of the identity operator, $x = x'$ , $y = y'$ , and $z = z'$ , so that the matrix for the identity symmetry operator is the 3 by 3 identity matrix.

$$
\hat {E} \leftrightarrow \mathbf {E} = \left[ \begin{array}{l l l} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{array} \right].\tag{9.74}
$$

The double-headed arrow means that the symmetry operator $\hat{E}$ and the matrix E are equivalent. That is, the matrix product in Eq. (9.72) and the operator expression in Eq. (9.71) give the same result. We sometimes say that there is a one-to-one correspondence between this operator and this matrix.

EXAMPLE 9.14 Find the matrix that represents $\hat{C}_n(z)$ .

SOLUTION ▶ Let $\alpha = 2\pi/n$ radians, the angle through which the operator rotates a particle,

$$
\begin{array}{r c l} x ^ {\prime} & = & \cos (\alpha) x - \sin (\alpha) y \\ y ^ {\prime} & = & \sin (\alpha) x + \cos (\alpha) y \\ z ^ {\prime} & = & z. \end{array}
$$

Comparison of this with Eq. (9.73a) gives

$$
\hat {C} _ {n} (z) \leftrightarrow \left[ \begin{array}{c c c} \cos (\alpha) & - \sin (\alpha) & 0 \\ \sin (\alpha) & \cos (\alpha) & 0 \\ 0 & 0 & 1 \end{array} \right].\tag{9.75}
$$

EXERCISE 9.24 ▶

(a) Verify Eqs. (9.74) and (9.75) by matrix multiplication.

(b) Use Eq. (9.75) to find the matrix for $\hat{C}_2(z)$ .

(c) Find the matrices equivalent to $\hat{S}_3(z)$ and $\hat{\sigma}_h$ .

The matrices that represent a group of symmetry operators have the same effect as the symmetry operators, so they must multiply together in the same way. We can show this for our present representation by carrying out the matrix multiplications. The matrices for the $C_{3v}$ group are

$$
\hat {E} \leftrightarrow \left[ \begin{array}{l l l} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{array} \right] = \mathbf {E}, \hat {C} _ {3} \leftrightarrow \left[ \begin{array}{c c c} - 1 / 2 & - \sqrt {3} / 2 & 0 \\ \sqrt {3} / 2 & - 1 / 2 & 0 \\ 0 & 0 & 1 \end{array} \right] = \mathbf {A}\tag{9.76}
$$

$$
\hat {C} _ {3} ^ {2} \leftrightarrow \left[ \begin{array}{c c c} - 1 / 2 & \sqrt {3} / 2 & 0 \\ - \sqrt {3} / 2 & - 1 / 2 & 0 \\ 0 & 0 & 1 \end{array} \right] = \mathbf {B}, \hat {\sigma} _ {a} \leftrightarrow \left[ \begin{array}{c c c} 1 / 2 & \sqrt {3} / 2 & 0 \\ \sqrt {3} / 2 & - 1 / 2 & 0 \\ 0 & 0 & 1 \end{array} \right] = \mathbf {C}
$$

$$
\hat {\sigma} _ {b} \leftrightarrow \left[ \begin{array}{c c c} 1 / 2 & - \sqrt {3} / 2 & 0 \\ - \sqrt {3} / 2 & - 1 / 2 & 0 \\ 0 & 0 & 1 \end{array} \right] = \mathbf {D}, \hat {\sigma} _ {c} \leftrightarrow \left[ \begin{array}{c c c} - 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{array} \right] = \mathbf {F},
$$

where we have given each matrix an arbitrarily chosen letter symbol.

EXERCISE 9.25 ▶

(a) By transcribing Table 9.1 with appropriate changes in symbols, generate the multiplication table for the matrices in Eq. (9.76).

(b) Verify several of the entries in the multiplication table by matrix multiplication.


Each of the matrices in Eq. (9.76) is equivalent to one of the symmetry operators in the $C_{3v}$ group, but it is not exactly identical to it, being only one possible way to represent the symmetry operator. Any set of matrices that obeys the same multiplication table as a given group is called a representation of that group. Our set of matrices forms another group of the same order (same number of members) as the $C_{3v}$ point group. The fact that it obeys the same multiplication table is expressed by saying that it is isomorphic with the group of symmetry operators. A group of matrices that is isomorphic with a group of symmetry operators is called a faithful representation of the group. Our group of matrices consists of 3 by 3 matrices and is said to be of dimension 3.

The representation of the $C_{3v}$ group that we have presented is said to have the coordinates x, y, and z as its basis. Other representations can be obtained by using other functions as a basis and determining how the symmetry operators change these functions. The matrices in a representation do not have to have any physical interpretation, but they must multiply in the same way as do the symmetry operators, must be square, and all must have the same number of rows and columns. In some representations, called unfaithful or homomorphic, there are fewer matrices than there are symmetry operators, so that one matrix occurs in the places in the multiplication table where two or more symmetry operators occur.

Group representations are divided into two kinds, reducible and irreducible. In a reducible representation, the matrices are “block-diagonal” or can be put into block-diagonal form by a similarity transformation. A similarity transformation

means forming the matrix product

$$
\mathbf {P} = \mathbf {X} ^ {- 1} \mathbf {Q X}\tag{9.77}
$$

where P, X, and Q are square matrices. A block-diagonal matrix is one in which all elements are zero except those in square regions along the diagonal. The following matrix has two 2 by 2 blocks and a 1 by 1 block

$$
\left| \begin{array}{c c c c c} 1 & 2 & 0 & 0 & 0 \\ 3 & 2 & 0 & 0 & 0 \\ 0 & 0 & 4 & 3 & 0 \\ 0 & 0 & 3 & 3 & 0 \\ 0 & 0 & 0 & 0 & 2 \end{array} \right|.
$$

All the matrices in a reducible representation have the same size blocks in the same order. The representation of the group $C_{3v}$ given in Eq. (9.76) is reducible, since each matrix has a 2 by 2 block and a 1 by 1 block. When two block-diagonal matrices with the same size blocks are multiplied together, the result is a matrix that is block-diagonal with the same size blocks in the same order. This is apparent in the case of the matrices in Eq. (9.76), which produce only each other when multiplied together.

EXERCISE 9.26 ▶ Show by matrix multiplication that two matrices with a 2 by 2 block and two 1 by 1 blocks produce another such matrix when multiplied together.

Because of the way in which block-diagonal matrices multiply, the 2 by 2 blocks in the matrices in Eq. (9.76) if taken alone form another representation of the $C_{3v}$ group. When a reducible representation is written with its matrices in block-diagonal form, the block submatrices form irreducible representations, and the reducible representation is said to be the direct sum of the irreducible representations. Both the representations obtained from the submatrices are irreducible. The 1 by 1 blocks form an unfaithful or homomorphic representation, in which every operator is represented by the 1 by 1 identity matrix. This one-dimensional representation is called the totally symmetric representation. In this particular case we could not get three one-dimensional representations, because the $\hat{C}_{3}(z)$ operator mixes the x and y coordinates of a particle, preventing the matrices from being diagonal.

EXERCISE 9.27 ▶ Pick a few pairs of 2 by 2 submatrices from Eq. (9.76) and show that they multiply in the same way as the 3 by 3 matrices.

In any representation of a symmetry group, the trace of a matrix is called the character of the corresponding operator for that representation.

EXERCISE 9.28 ▶ Find the characters of the operators in the $C_{3v}$ group for the representation in Eq. (9.76).

The two irreducible representations of the $C_{3v}$ group that we have obtained thus far are said to be nonequivalent, since they have different dimensions. There are several theorems governing irreducible representations for a particular group. $^{8}$

These theorems can be used to determine that three irreducible representations of the $C_{3v}$ group occur, and that their dimensions are 2, 1, and 1. The other one-dimensional representation is

$$
\begin{array}{r l} \hat {E} \leftrightarrow 1 & \hat {C} _ {3} \leftrightarrow 1 \quad \hat {C} _ {3} ^ {2} \leftrightarrow 1 \\ \hat {\sigma} _ {a} \leftrightarrow - 1 & \hat {\sigma} _ {b} \leftrightarrow - 1 \quad \hat {\sigma} _ {c} \leftrightarrow - 1. \end{array}\tag{9.78}
$$

EXERCISE 9.29 ▶ Show that the 1 by 1 matrices (scalars) in Eq. (9.78) obey the same multiplication table as does the group of symmetry operators.

![[63f9849582fbf3ddb622a37956e93714656e15fa695abff975376d75edb1ccaf.jpg]]

Group theory can be applied to several different areas of molecular quantum mechanics, including the symmetry of electronic and vibrational wave functions and the study of transitions between energy levels. $^{9}$ There is also a theorem which says that there is a correspondence between an energy level and some one of the irreducible representations of the symmetry group of the molecule, and that the degeneracy (number of states in the level) is equal to the dimension of that irreducible representation.

## SUMMARY

We discussed three topics in this chapter: operator algebra, matrix algebra, and group theory. A mathematical operator is a symbol standing for the carrying out of a mathematical operation. Operating on a function with an operator produces a new function. Operator symbols can be manipulated in a way similar to the algebra of ordinary variables, without reference to any function that might be operated on. We defined the sum and the product of two operators. The product of two operators was defined as successive operation with the operators. The quotient of two operators was not defined, but we defined the inverse of an operator, which undoes the effect of that operator. The principal difference between operator algebra and ordinary algebra is that multiplication of two operators is not necessarily commutative. We discussed symmetry operators, a useful class of operators which move points in space relative to a symmetry element.

A matrix is a list of quantities, arranged in rows and columns. Matrix algebra is similar to operator algebra in that multiplication of two matrices is not necessarily commutative. The inverse of a matrix is similar to the inverse of an operator. If $A^{-1}$ is the inverse of A, then $A^{-1}A = AA^{-1} = E$ , where E is the identity matrix. We presented the Gauss-Jordan method for obtaining the inverse of a nonsingular square matrix.

Group theory is a branch of mathematics that involves elements with defined properties and a single method to combine two elements called multiplication. The symmetry operators belonging to any symmetrical object form a group. The theorems of group theory can provide useful information about electronic wave functions for symmetrical molecules, spectroscopic transitions, and so forth.

## PROBLEMS

1. Find the following commutators, where $D_{x} = d/dx$ :

a) $[\hat{D}_x, \sin(x)]$ ;

b) $[\hat{D}_x^3,x];$

2. Find the following commutators, where $D_{x} = d/dx$ :

a) $[\hat{D}_x^3, x^2]$ ;

b) $[\hat{D}_x^2, f(x)]$ .

3. Show that the x and z components of the angular momentum have quantum mechanical operators that do not commute and find their commutator:

$$
\hat {L} _ {x} = \frac {\hbar}{i} \left(\hat {y} \frac {d}{d z} - \hat {z} \frac {d}{d y}\right), \quad \hat {L} _ {z} = \frac {\hbar}{i} \left(\hat {x} \frac {d}{d y} - \hat {y} \frac {d}{d x}\right).
$$

4. The Hamiltonian operator for a one-dimensional harmonic oscillator moving in the $x$ direction is

$$
\hat {H} = - \frac {\hbar^ {2}}{2 m} \frac {d ^ {2}}{d x ^ {2}} + \frac {k x ^ {2}}{2}.
$$

Find the value of the constant $a$ such that the function $e^{-ax^2}$ is an eigenfunction of the Hamiltonian operator. The quantity $k$ is the force constant, $m$ is the mass of the oscillating particle, and $\hbar$ is Planck's constant divided by $2\pi$ .

5. In quantum mechanics, the expectation value of a mechanical quantity is given by

$$
\langle A \rangle = \frac {\int \psi^ {*} \hat {A} \psi d x}{\int \psi^ {*} \psi d x},
$$

where $\hat{A}$ is the operator for the mechanical quantity and $\psi$ is the wave function for the state of the system. The integrals are over all permitted values of the coordinates of the system. The expectation value is defined as the prediction of the mean of a large number of measurements of the mechanical quantity, given that the system is in the state corresponding to $\psi$ prior to each measurement.

For a particle moving in the $x$ direction only and confined to a region on the $x$ axis from $x = 0$ to $x = a$ , the integrals are single integrals from 0 to $a$ and $\hat{p}_x$ is given by $(\hbar / i)\partial/\partial x$ . Find the expectation value of $p_x$ and of $p_x^2$ if the wave function is

$$
\psi = C \sin \left(\frac {\pi x}{a}\right),
$$

where $C$ is a constant.

6. If $\hat{A}$ is the operator corresponding to the mechanical quantity $A$ and $\phi_n$ is an eigenfunction of $\hat{A}$ , such that

$$
\hat {A} \phi_ {n} = a _ {n} \phi_ {n}
$$

show that the expectation value of A is equal to $a_{n}$ if the state of the system corresponds to $\phi_{n}$ . See Problem 5 for the formula for the expectation value.

7. If x is an ordinary variable, the Maclaurin series for $1/(1 - x)$ is

$$
\frac {1}{1 - x} = 1 + x ^ {2} + x ^ {3} + x ^ {4} + \dots .
$$

If $\hat{X}$ is some operator, show that the series

$$
1 + \hat {X} + \hat {X} ^ {2} + \hat {X} ^ {3} + \hat {X} ^ {4} + \dots
$$

is the inverse of the operator $1 - \hat{X}$ .

8. Find the result of each operation on the given point (represented by Cartesian coordinates):
a) $\hat{i}(2,4,6)$ b) $\hat{C}_{2}(y)(1,1,1)$ c) $\hat{C}_{3}(z)(1,1,1)$

9. Find the result of each operation on the given point (represented by Cartesian coordinates):
a) $\hat{S}_{4}(z)(1,1,1)$ b) $\hat{C}_{2}(z)\hat{i}\hat{\sigma}_{h}(1,1,1)$ c) $\hat{S}_{2}(y)\hat{\sigma}_{h}(1,1,0)$ .

10. Find the 3 by 3 matrix that is equivalent in its action to each of the symmetry operators:
a) $\hat{S}_{2}(z)$ b) $\hat{C}_{2}(x)$

11. Find the 3 by 3 matrix that is equivalent in its action to each of the symmetry operators:
a) $\hat{C}_{8}(x)$ b) $\hat{S}_{6}(x)$

12. Give the function that results if the given symmetry operator operates on the given function for each of the following:
a) $\hat{C}_{4}(z)x^{2}$ b) $\hat{\sigma}_{h}x\cos(x/y)$

13. Give the function that results if the given symmetry operator operates on the given function for each of the following:
a) $\hat{i}(x + y + z^{2})$ b) $\hat{S}_{4}(x)(x + y + z)$

14. Find the matrix products. Use Mathematica to check your result.

a)

$$
\left[ \begin{array}{c c c} 0 & 1 & 2 \\ 4 & 3 & 2 \\ 7 & 6 & 1 \end{array} \right] \left[ \begin{array}{c c c} 1 & 2 & 3 \\ 6 & 8 & 1 \\ 7 & 4 & 3 \end{array} \right]
$$

b)

$$
\left[ \begin{array}{r r r r} 6 & 3 & 2 & - 1 \\ - 7 & 4 & 3 & 2 \\ 1 & 3 & 2 & - 2 \\ 6 & 7 & - 1 & - 3 \end{array} \right] \left[ \begin{array}{r r r r} 4 & 7 & - 6 & - 8 \\ 3 & - 6 & 8 & - 6 \\ 2 & 3 & - 3 & 4 \\ - 1 & 4 & 2 & 3 \end{array} \right]
$$

15. Find the matrix products. Use Mathematica to check your result.

$$
\mathbf {a}) \left[ \begin{array}{l l l l} 3 & 2 & 1 & 4 \end{array} \right] \left[ \begin{array}{r r r} 1 & 2 & 3 \\ 0 & 3 & - 4 \\ 1 & - 2 & 1 \\ 3 & 1 & 0 \end{array} \right]
$$

b)

$$
{\left[ \begin{array}{r r r} 1 & 2 & 3 \\ 0 & 3 & - 4 \\ 1 & - 2 & 1 \\ 3 & 1 & 0 \end{array} \right]} {\left[ \begin{array}{l} 3 \\ 2 \\ 1 \\ 4 \end{array} \right]}
$$

$$
\mathbf {c}) \left[ \begin{array}{l l l} 6 & 3 & - 1 \\ 7 & 4 & - 2 \end{array} \right] \left[ \begin{array}{l l l l} 1 & 4 & - 7 & 3 \\ 2 & 5 & 8 & - 2 \\ 3 & 6 & - 9 & 1 \end{array} \right]
$$

16. Show that (AB)C = A(BC) for the matrices:

$$
\mathbf {A} = \left[ \begin{array}{r r r} 0 & 1 & 2 \\ 3 & 1 & - 4 \\ 2 & 3 & 1 \end{array} \right] \mathbf {B} = \left[ \begin{array}{r r r} 3 & 1 & 4 \\ - 2 & 0 & 1 \\ 3 & 2 & 1 \end{array} \right] \mathbf {C} = \left[ \begin{array}{r r r} 0 & 3 & 1 \\ - 4 & 2 & 3 \\ 3 & 1 & - 2 \end{array} \right]
$$

17. Show that $\mathbf{A}(\mathbf{B} + \mathbf{C}) = \mathbf{A}\mathbf{B} + \mathbf{A}\mathbf{C}$ for the example matrices in the previous problem.

18. Test the following matrices for singularity. Find the inverses of any that are nonsingular. Multiply the original matrix by its inverse to check your work. Use Mathematica to check your work.

a)

$$
\left[ \begin{array}{l l l} 0 & 1 & 2 \\ 2 & 3 & 1 \\ 2 & 4 & 3 \end{array} \right]
$$

b)

$$
\left[ \begin{array}{l l l} 6 & 8 & 1 \\ 7 & 3 & 2 \\ 4 & 6 & - 9 \end{array} \right]
$$

19. Test the following matrices for singularity. Find the inverses of any that are nonsingular. Multiply the original matrix by its inverse to check your work. Use Mathematica to check your work.

a)

$$
\left[ \begin{array}{r r r} 3 & 2 & - 1 \\ - 4 & 6 & 3 \\ 7 & 2 & - 1 \end{array} \right]
$$

b)

$$
\left[ \begin{array}{c c c} 0 & 2 & 3 \\ 1 & 1 & 1 \\ 2 & 0 & 1 \end{array} \right]
$$

20. Find the matrix P that results from the similarity transformation

$$
\mathbf {P} = \mathbf {X} ^ {- 1} \mathbf {Q X},
$$

where

$$
\mathbf {Q} = \left[ \begin{array}{l l} 1 & 2 \\ 2 & 1 \end{array} \right], \mathbf {X} = \left[ \begin{array}{l l} 2 & 3 \\ 4 & 3 \end{array} \right].
$$

21. The $H_{2}O$ molecule belongs to the point group $C_{2v}$ , which contains the symmetry operators $\hat{E}$ , $\hat{C}_{2}$ , $\hat{\sigma}_{a}$ , and $\hat{\sigma}_{b}$ , where the $C_{2}$ axis passes through the oxygen nucleus and midway between the two hydrogen nuclei, and where the $\sigma_{a}$ mirror plane contains the three nuclei and the $\sigma_{b}$ mirror plane is perpendicular to the $\sigma_{a}$ mirror plane.

a) Find the 3 by 3 matrix that is equivalent to each symmetry operator.

b) Show that the matrices obtained in part (a) have the same multiplication table as the symmetry operators, and that they form a group. The multiplication table for the group was to be obtained in Exercise 9.23.

22. Permutation operators are operators that interchange objects. Three objects can be arranged in 3! = 6 different ways, or permutations. From a given arrangement, all six permutations can be attained by application of the six operators: $\hat{E}$ , the identity operator; $\hat{P}_{12}$ , which interchanges objects 1 and 2; $\hat{P}_{23}$ , which interchanges objects 2 and 3; $\hat{P}_{13}$ , which interchanges objects 1 and 3; $\hat{P}_{23}\hat{P}_{12}$ , which interchanges objects 1 and 2 and then interchanges objects 2 and 3, and $\hat{P}_{23}\hat{P}_{13}$ , which interchanges objects 1 and 3 and then interchanges objects 2 and 3. Satisfy yourself that each of these operators produces a different arrangement. Show that the six operators form a group. Construct a multiplication table for the group.

# The Solution of Simultaneous Algebraic Equations

## Preview

If there are two variables in an equation, such as $F(x, y) = 0$ , then the equation can be solved for y as a function of x or x as a function of y, but in order to solve for constant values of both variables, a second equation, such as $G(x, y) = 0$ , is required, and the two equations must be solved simultaneously. If there are n variables, n independent and consistent equations are required. In this chapter, we discuss various methods for finding the roots to sets of simultaneous equations.

## Principal Facts and Ideas

1. To solve for n variables, n equations are required, and these equations must be independent and consistent.

2. Simultaneous linear inhomogeneous equations can be solved with various techniques, including elimination, use of Cramer's formula, and by matrix inversion.

3. Linear homogeneous simultaneous equations have a nontrivial solution only when a certain dependence condition is met.

## Objectives

After studying this chapter, you should be able to:

1. solve any fairly simple set of several simultaneous linear equations by the method of elimination;

2. solve a set of linear inhomogeneous simultaneous equations by Cramer's method and by matrix inversion;

3. solve a set of linear homogeneous simultaneous equations using the dependence condition.

## 10.1 Simultaneous Equations with More than Two Unknowns

In Chapter 3, we discussed the use of the method of substitution and the method of elimination to solve the linear inhomogeneous set of two simultaneous equations:

$$
a _ {11} x + a _ {12} y = c _ {1}\tag{10.1a}
$$

$$
a _ {21} x + a _ {22} y = c _ {2},\tag{10.1b}
$$

where the a's and the c's are constants. Systems of several equations are similar to pairs of equations for two unknowns. For a unique solution, you must have n independent and consistent equations to solve for n unknowns. Sometimes in practical calculations you will have more equations than you have unknowns. If the equations are not all consistent, you have what is called an overdetermined system of equations, which has no solution. If the equations arise from experimental measurements, the source of inconsistency is likely experimental error. In this case, you can pick various sets of n equations and solve them separately, presumably getting slightly different answers for different sets because of experimental error. The variation between different answers can be used to get an idea of the effects of the errors.

## 10.2 Cramer's Rule

This method is a systematic method for solving linear inhomogeneous equations. We illustrate the method with the set of two linear inhomogeneous equations in Eq. (10.1). Written in matrix form these equations are

$$
\mathbf {A} \mathbf {X} = \mathbf {C},\tag{10.2}
$$

where $\mathbf{A}$ is a square matrix, and $\mathbf{X}$ and $\mathbf{C}$ are column vectors (matrices with only one column):

$$
\left[ \begin{array}{l l} a _ {11} & a _ {12} \\ a _ {21} & a _ {22} \end{array} \right] \left[ \begin{array}{l} x _ {1} \\ x _ {2} \end{array} \right] = \left[ \begin{array}{l} c _ {1} \\ c _ {2} \end{array} \right]\tag{10.3}
$$

EXERCISE 10.1 ▶ Use the rules of matrix multiplication to show that Eq. (10.2) is identical with Eq. (10.1).

Cramer's rule states that the solutions to this set of equations are written as quotients of determinants:

$$
x = \frac {\left| \begin{array}{c c} c _ {1} & a _ {12} \\ c _ {2} & a _ {22} \end{array} \right|}{\left| \begin{array}{c c} a _ {11} & a _ {12} \\ a _ {21} & a _ {22} \end{array} \right|}\tag{10.4}
$$

$$
y = \frac {\left| \begin{array}{c c} a _ {11} & c _ {1} \\ a _ {21} & c _ {2} \end{array} \right|}{\left| \begin{array}{c c} a _ {11} & a _ {12} \\ a _ {21} & a _ {22} \end{array} \right|}.\tag{10.5}
$$

The solutions are constructed as follows: The denominator in each expression is the determinant of the matrix A, and the numerator is the determinant of this matrix with one of the columns replaced by the column vector $\binom{c_{1}}{c_{2}}$ . In the expression for x, the column of coefficients for x is replaced, and in the expression for y, the column of coefficients for y is replaced.

EXERCISE 10.2 ▶

Use Cramer's rule to solve the simultaneous equations

$$
\begin{array}{r l} 4 x + y & = 14 \\ 2 x - 3 y & = 0. \end{array}
$$


If there are more than two variables and more than two linear inhomogeneous equations, Cramer's rule uses exactly the same pattern. If we have a set of three equations

$$
a _ {11} x _ {1} + a _ {12} x _ {2} + a _ {13} x _ {3} = c _ {3}\tag{10.6}
$$

$$
a _ {21} x _ {1} + a _ {22} x _ {2} + a _ {23} x _ {3} = c _ {2}\tag{10.7}
$$

$$
a _ {31} x _ {1} + a _ {32} x _ {2} + a _ {33} x _ {3} = c _ {3},\tag{10.8}
$$

where we call the unknown quantities $x_{1}$ , $x_{2}$ , and $x_{3}$ instead of x, y, and z. This equation can be written in matrix notation:

$$
{\left[ \begin{array}{l l l} a _ {11} & a _ {12} & a _ {13} \\ a _ {21} & a _ {22} & a _ {23} \\ a _ {31} & a _ {32} & a _ {33} \end{array} \right]} {\left[ \begin{array}{l} x _ {1} \\ x _ {2} \\ x _ {3} \end{array} \right]} = {\left[ \begin{array}{l} c _ {1} \\ c _ {2} \\ c _ {3} \end{array} \right]}\tag{10.9}
$$

or

$$
\mathbf {A} \mathbf {X} = \mathbf {C},
$$

where X and C are the column vectors shown.

According to Cramer's rule the value of $x_{1}$ is given by

$$
\boxed {x _ {1} = \frac {\left| \begin{array}{c c c} c _ {1} & a _ {12} & a _ {13} \\ c _ {2} & a _ {22} & a _ {23} \\ c _ {3} & a _ {32} & a _ {33} \end{array} \right|}{\det (\mathbf {A})},}\tag{10.10}
$$

where $\det(\mathbf{A})$ is the determinant of the 3 by 3 matrix of the a coefficients. The determinant in the numerator is obtained by replacing the first column by the constants $c_{1}$ , $c_{2}$ , and $c_{3}$ (the column vector C). The value of $x_{2}$ is given by a similar expression with the second column in the determinant in the numerator replaced by the constants $c_{1}$ , $c_{2}$ , and $c_{3}$ . The value of $x_{3}$ is given by an expression with the third column in the determinant replaced by the column vector C.

EXAMPLE 10.1 Use Cramer's rule to find the value of $x_{1}$ that satisfies

$$
\left[ \begin{array}{r r r} 2 & 4 & 1 \\ 1 & - 1 & 1 \\ 1 & 1 & 1 \end{array} \right] \left[ \begin{array}{l} x _ {1} \\ x _ {2} \\ x _ {3} \end{array} \right] = \left[ \begin{array}{l} 21 \\ 4 \\ 10 \end{array} \right].\tag{10.11}
$$

SOLUTION ▶

$$
\begin{array}{r l} x _ {1} & = \frac {\left[ \begin{array}{l l l} 21 & 4 & 1 \\ 4 & - 1 & 1 \\ 10 & 1 & 1 \end{array} \right]}{\left[ \begin{array}{l l l} 2 & 4 & 1 \\ 1 & - 1 & 1 \\ 1 & 1 & 1 \end{array} \right]} = \frac {21 \left[ \begin{array}{l l} - 1 & 1 \\ 1 & 1 \end{array} \right] - 4 \left[ \begin{array}{l l} 4 & 1 \\ 1 & 1 \end{array} \right] + 10 \left[ \begin{array}{l l} 4 & 1 \\ - 1 & 1 \end{array} \right]}{2 \left[ \begin{array}{l l} - 1 & 1 \\ 1 & 1 \end{array} \right] - 1 \left[ \begin{array}{l l} 4 & ] \\ 1 & 1 \end{array} \right] + 1 \left[ \begin{array}{l l} 4 & ] \\ - 1 & 1 \end{array} \right]} \\ & = \frac {21 (- 1 - 1) - 4 (4 - 1) + 10 (4 + 1)}{2 (- 1 - 1) - (4 - 1) + (4 + 1)} = \frac {- 4}{- 2} = 2. \end{array}
$$

EXERCISE 10.3 ▶

Find the values of $x_{2}$ and $x_{3}$ for the previous example.

Cramer's rule for more than three linear inhomogeneous equations is completely analogous to this. We write the equations in matrix form

$$
\mathbf {A} \mathbf {X} = \mathbf {C},
$$

where the matrices now have more than three rows and columns. In order to have a solution, the matrix A must be square and have the same number of rows and columns as the column vectors X and C have rows. Let $A_{n}$ be the matrix that is obtained from A by replacing the nth column by the column vector C. Cramer's rule is now written

$$
\boxed {x _ {n} = \frac {\det (\mathbf {A} _ {n})}{\det (\mathbf {A})}}.\tag{10.12}
$$

## Linear Dependence and Inconsistency

In Chapter 3 we discussed linear dependence and inconsistency in the case of two equations. We will not discuss completely the questions of consistency and independence for sets of more than two equations, but we will make the following comments, which apply to sets of linear inhomogeneous equations:

1. A set of n equations is said to be linearly dependent if a set of constants $b_{1}, b_{2}, \ldots, b_{n}$ , not all equal to zero, can be found such that if the first equation is multiplied by $b_{1}$ , the second equation by $b_{2}$ , the third equation by $b_{3}$ , and so on, the equations add to zero for all values of the variables. A simple example of linear dependence is for two of the equations to be identical. In this case, we could multiply one of these equations by +1 and the other by -1 and all of the remaining equations by 0 and have the equations sum to zero. If two equations are identical, one has only n - 1 usable equations and cannot solve for n variables. More complicated types of linear dependence also occur, and in any case one has only n - 1 usable equations or fewer.

2. In the case of two identical equations, the determinant of the matrix A vanishes, from property 2 of determinants, described in Chapter 9. The determinant of A will also vanish in more complicated types of linear dependence. If det(A) vanishes, either the equations are linearly dependent or they are inconsistent.

3. It is possible for a set of equations to appear to be overdetermined and not actually be overdetermined if some of the set of equations are linearly dependent.

EXERCISE 10.4 ▶ See if the set of four equations in three unknowns can be solved:

$$
\begin{array}{r l} {x _ {1} + x _ {2} + x _ {3}} & {= 6} \\ {x _ {1} + x _ {2} + x _ {3}} & {= 0} \\ {3 x _ {1} + 3 x _ {2} + x _ {3}} & {= 12} \\ {2 x _ {1} + x _ {2} + 4 x _ {3}} & {= 16} \end{array}
$$


## 10.3 Solution by Matrix Inversion

We write a set of linear inhomogeneous equations in matrix form:

$$
\boxed {\mathbf {A X} = \mathbf {C}},\tag{10.13}
$$

where A is now an n by n square matrix, X is an n by 1 column vector containing the unknowns, and C is another n by 1 column vector containing constants. If we possess the inverse of A, we can multiply both sides this equation on the left by $A^{-1}$ to get

$$
\boxed {\mathbf {A} ^ {- 1} \mathbf {A X} = \mathbf {X} = \mathbf {A} ^ {- 1} \mathbf {C}}.\tag{10.14}
$$

The solution is represented by a column vector that is equal to the matrix product $A^{-1}C$ . In order for a matrix to possess an inverse, it must be nonsingular, which means that its determinant does not vanish. If the matrix is singular, the system of equations cannot be solved because it is either linearly independent or inconsistent. We have already discussed the inversion of a matrix in Chapter 9. The difficulty with carrying out this procedure by hand is that it is probably more work to invert an n by n matrix than to solve the set of equations by other means. However, with access to Mathematica, BASIC, or another computer language that automatically inverts matrices, you can solve such a set of equations very quickly.

EXERCISE 10.5 ▶ Solve the following set of simultaneous equations by matrix inversion:

$$
\begin{array}{r l} 2 x _ {1} + x _ {2} & = 1 \\ x _ {1} + 2 x _ {2} + x _ {3} & = 2 \\ x _ {2} + 2 x _ {3} & = 3. \end{array}
$$

The inverse of the relevant matrix has already been obtained in Example 9.10.

## Gauss–Jordan Elimination

This is a systematic procedure for carrying out the method of elimination. It is very similar to the Gauss–Jordan method for finding the inverse of a matrix, described in Chapter 9. If the set of equations is written in the vector form

$$
\mathbf {A} \mathbf {X} = \mathbf {C},
$$

we write an augmented matrix consisting of the A matrix and the C column vector written side by side. For a set of four equations, the augmented matrix is

$$
\left[ \begin{array}{c c c c c c} a _ {11} & a _ {12} & a _ {13} & a _ {14} & \vdots & c _ {1} \\ a _ {21} & a _ {22} & a _ {23} & a _ {24} & \vdots & c _ {2} \\ a _ {31} & a _ {32} & a _ {33} & a _ {34} & \vdots & c _ {3} \\ a _ {41} & a _ {42} & a _ {42} & a _ {44} & \vdots & c _ {4} \end{array} \right].\tag{10.15}
$$

Row operations are carried out on this augmented matrix: a row can be multiplied by a constant, and one row can be subtracted from or added to another row. These operations will not change the roots to the set of equations, since such operations are equivalent to multiplying one of the equations by a constant or to taking the sum or difference of two equations. In Gauss–Jordan elimination, our aim is to transform the left part of the augmented matrix into the identity matrix, which will transform the right column into the four roots, since the set of equations will then be

$$
\mathbf {E X} = \mathbf {C} ^ {\prime}.\tag{10.16}
$$

The row operations are carried out exactly as in Section 9.4 except for having only one column in the right part of the augmented matrix.

EXERCISE 10.6 ▶ Use Gauss–Jordan elimination to solve the set of simultaneous equations in the previous exercise. The same row operations will be required that were used in Example 9.10.

There is a similar procedure known as Gauss elimination, in which row operations are carried out until the left part of the augmented matrix is in upper triangular form. The bottom row of the augmented matrix then provides the root for one variable. This is substituted into the equation represented by the next-to-bottom row, and it is solved to give the root for the second variable. The two values are substituted into the next equation, and so on.

## Linear Homogeneous Equations

In Chapter 3 we discussed pairs of linear homogeneous equations for two variables. We found that such a pair of equations needed to be linearly dependent in order to have a solution other than the trivial solution x = 0, y = 0. The same is true of sets with more than two variables.

A set of three homogeneous equations in three unknowns is written

$$
a _ {11} x _ {1} + a _ {12} x _ {2} + a _ {13} x _ {3} = 0\tag{10.17a}
$$

$$
a _ {21} x _ {1} + a _ {22} x _ {2} + a _ {23} x _ {3} = 0\tag{10.17b}
$$

$$
a _ {31} x _ {2} + a _ {32} x _ {2} + a _ {33} x _ {3} = 0.\tag{10.17c}
$$

If we attempt to apply Cramer's rule to this set of equations, without asking whether it is legitimate to do so, we find for example that

$$
x _ {1} = \frac {\left| \begin{array}{c c c} 0 & a _ {12} & a _ {13} \\ 0 & a _ {22} & a _ {23} \\ 0 & a _ {32} & a _ {33} \end{array} \right|}{\det (\mathbf {A})}.\tag{10.18}
$$

If $\det(\mathbf{A}) \neq 0$ , this yields $x_{1} = 0$ , and similar equations will also give $x_{2} = 0$ and $x_{3} = 0$ . This trivial solution is all that we can have if the determinant of A is nonzero (i.e., if the three equations are independent). To have a nontrivial solution, the equations must be linearly dependent. In order to find a possible nontrivial solution, we investigate the condition

$$
\det (\mathbf {A}) = 0,\tag{10.19}
$$

which in the 3 by 3 case is the same as

$$
a _ {11} a _ {22} a _ {33} - a _ {11} a _ {23} a _ {32} - a _ {12} a _ {21} a _ {33} - a _ {13} a _ {22} a _ {31} + a _ {12} a _ {23} a _ {31} - a _ {13} a _ {21} a _ {32} = 0\tag{10.20}
$$

This condition must be satisfied for a nontrivial solution to exist.

## Matrix Eigenvalues and Eigenvectors

One case in which a set of linear homogeneous equations arises is the matrix eigenvalue problem. This problem is very similar to an eigenvalue equation for an operator, as in Eq. (9.3). The problem is to find a column vector, X and a scalar eigenvalue b, such that

$$
\mathbf {B} \mathbf {X} = b \mathbf {X},\tag{10.21}
$$

where B is the square matrix for which we want to find an eigenvector and X is a column vector (the eigenvector). Since the right-hand side of Eq. (10.21) is the same as bEX where E is the identity matrix, we can rewrite Eq. (10.21) as

$$
(\mathbf {B} - b \mathbf {E}) \mathbf {X} = 0,\tag{10.22}
$$

which is a set of linear homogeneous equations written in the notation of Eq. (10.13). The equations must be linearly dependent in order to have a solution, so there are only n - 1 independent equations if this condition is satisfied.

EXAMPLE 10.2 Find the values of b and X that satisfy the eigenvalue equation

$$
\left[ \begin{array}{l l l} 1 & 1 & 0 \\ 1 & 1 & 1 \\ 0 & 1 & 1 \end{array} \right] \left[ \begin{array}{l} x _ {1} \\ x _ {2} \\ x _ {3} \end{array} \right] = b \left[ \begin{array}{l} x _ {1} \\ x _ {2} \\ x _ {3} \end{array} \right]\tag{10.23}
$$

and also satisfy a "normalization" condition:

$$
x _ {1} ^ {2} + x _ {2} ^ {2} + x _ {3} ^ {2} = 1.\tag{10.24}
$$

Since the equations must be linearly dependent, this additional equation will provide unique values for the three variables.

SOLUTION ▶ In the form of Eq. (10.22),

$$
\left[ \begin{array}{c c c} 1 - b & 1 & 0 \\ 1 & 1 - b & 1 \\ 0 & 1 & 1 - b \end{array} \right] \left[ \begin{array}{c} x _ {1} \\ x _ {2} \\ x _ {3} \end{array} \right] = 0.\tag{10.25}
$$

The condition that corresponds to Eq. (10.19) is

$$
\left| \begin{array}{c c c} y & 1 & 0 \\ 1 & y & 1 \\ 0 & 1 & y \end{array} \right| = y \left| \begin{array}{c c} y & 1 \\ 1 & y \end{array} \right| - 1 \left| \begin{array}{c c} 1 & 1 \\ 0 & y \end{array} \right| = y ^ {3} - 2 y = 0,\tag{10.26}
$$

where we temporarily let $y = 1 - b$ . Equation (10.26) is a cubic equation that can be solved by factoring. It has the three roots

$$
y = 0, \quad y = \sqrt {2}, \quad y = - \sqrt {2}
$$

or

$$
b = 1, \quad b = 1 - \sqrt {2}, \quad b = 1 + \sqrt {2}.\tag{10.27}
$$

The three roots in Eq. (10.27) are three different eigenvalues. It is only when b is equal to one of these three values that Eq. (10.23) has a nontrivial solution. Since we have three values of b, we have three different eigenvectors. We find the eigenvectors by substituting each value of b in turn into Eq. (10.25) and solving the set of equations. We begin with b = 1 and write

$$
0 + x _ {2} + 0 = 0\tag{10.28a}
$$

$$
x _ {1} + 0 + x _ {3} = 0\tag{10.28b}
$$

$$
0 + x _ {2} + 0 = 0.\tag{10.28c}
$$

It is now obvious that this set of equations is linearly dependent, as required, since the first and third equations are the same. Our solution is now

$$
x _ {2} = 0\tag{10.28d}
$$

$$
x _ {1} = - x _ {3}.\tag{10.28e}
$$

We have solved for two of the variables in terms of the third. Since we have only two independent equations, we do not have definite values for $x_{1}$ and $x_{3}$ until we apply the normalization condition of Eq. (10.24). Imposing it, we find for our first eigenvector

$$
\mathbf {X} = \left[ \begin{array}{c} 1 / \sqrt {2} \\ 0 \\ - 1 / \sqrt {2} \end{array} \right].\tag{10.29}
$$

The negative of this eigenvector could also have been taken.

We now seek the second eigenvector, for which $y = \sqrt{2}$ , or $b = 1 - \sqrt{2}$ . Equation (10.25)

![[ad774a40141d18585028ea2f1a7e710c00c03dd1b70b327dc7e71570863e861d.jpg]]

becomes

$$
\begin{array}{r c l} \sqrt {2} x _ {1} + x _ {2} + 0 & = & 0 \\ x _ {1} + \sqrt {2} x _ {2} + x _ {3} & = & 0 \\ 0 + x _ {2} + \sqrt {2} x _ {3} & = & 0. \end{array}\tag{10.30}
$$

With the normalization condition, the solution to this is

$$
\mathbf {X} = \left[ \begin{array}{c} 1 / 2 \\ - 1 / \sqrt {2} \\ 1 / 2 \end{array} \right].\tag{10.31}
$$

EXERCISE 10.7 ▶

(a) Verify Equation (10.31). Show that this is an eigenvector.

(b) Find the third eigenvector for the problem of the previous example.


In various methods in quantum chemistry orbital functions are represented as linear combinations of functions from a basis set containing several functions. A set of simultaneous equations very similar to Eq. (10.22) arises that is to be solved for the coefficients in the linear combinations. The condition analogous to Eq. (10.19) is called a secular equation, and the eigenvalue b in Eq. (10.22) is replaced by the orbital energy. The simplest theory using this representation for molecular orbitals is the Hückel method, $^{1}$ which is known as a semi-empirical method because it relies on experimental data to establish values for certain integrals that occur in the theory while assuming that certain other integrals vanish.

## 10.4 The Use of Mathematica to Solve Simultaneous Equations

In Chapter 3, we introduced the use of Mathematica to solve a single algebraic equation, using the Solve statement and the NSolve statement. The Solve statement can also be used to solve simultaneous equations. The equations are typed inside curly brackets with commas between them, and the variables are listed inside curly brackets. To solve the equations

$$
\begin{array}{l} {a x + b y = c} \\ {g x + h y = k} \end{array}
$$

we type the input entry

$$
\text { Solve } [ \{\mathrm{a} x + \mathrm{b} y = = c, \mathrm{g} x + \mathrm{h} y = = k \}, \{\mathrm{x}, \mathrm{y} \} ]
$$

and press the “Enter” key. Notice the use of braces to notify Mathematica that we have a list of two equations and a list of two variables and the use of a space to indicate multiplication. The output is

$$
\operatorname{Out} [ 1 ] = \{\{x \rightarrow c a + \frac {b (c g - a k)}{a (- (b g) + a h)}, y \rightarrow - \frac {(c g - a k)}{- (b g) + a h)} \} \}
$$

To simplify the expressions for x and y, we use the fact that the percent symbol represents the last line of output and type

Simplify[%]

```txt
We receive the output
Out[2]={ {x → - (c h) + b k / b g - a h, y → - -(c g) + a k / -(b g) + a h} }
which is the expression obtained from Cramer's rule.
```

The Eliminate statement is used to eliminate one or more of the variables in a set of simultaneous equations. For example, to obtain a single equation in x from the set of equations above, you would type the input entry (note the double equal signs):

```txt
Eliminate[{a x + b y == c, g x + h y == k},y] and would receive the output:
Out[1]=c h == b k - b g x + a h x
we solve this equation for x by typing
Solve[%,x]
We receive the output:
Out[2]={{x → (c h) + b k / b g - a h }}
```

## The Use of Mathematica to Find Matrix Eigenvalues and Eigenvectors

Mathematica finds matrix eigenvalues and eigenvectors by use of the statements Eigenvalues[m] and Eigenvectors[m], where m denotes a matrix that has already been typed into the program.

EXAMPLE 10.3 Use Mathematica to find the eigenvalues and eigenvectors of the matrix in the previous example.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
SOLUTION ▶ We open Mathematica and type the input statement
    m={{1,1,0},{1,1,1},{0,1,1}}
We press the “Enter” key and see the output
    Out[1]={{1,1,0},{1,1,1},{0,1,1}}
We then type the statement
    Eigenvalues[m]
We press the “Enter” key and see the output
    Out[2]={1 + $\sqrt{2}$, 1, 1 - $\sqrt{2}$}
We type the statement
    Eigenvectors[m]
and see the output
    Out[3]={{1, $\sqrt{2}$, 1}, {-1, 0, 1}, {1, $\sqrt{2}$, 1}}
</div>

## SUMMARY

To solve for numerical values of two variables, two equations are required, and they must be solved simultaneously, and similarly for more variables. We presented several methods for solving simultaneous equations. First was the method of substitution, which is not limited to linear equations, but which is not practical for more than two or three equations. We then presented several methods which can apply to sets of linear inhomogeneous equations. Cramer's method is a method which uses determinants to obtain the roots. A set of linear equations can be written in matrix form and can be solved by finding the inverse of the matrix of the coefficients. The methods of Gauss elimination and Gauss–Jordan elimination were presented.

Finally, we examined linear homogeneous equations. With such a set, the equations possess only a trivial solution if the equations are linearly independent. The condition of dependence that must occur in order to have a nontrivial solution is represented by an equation in which the determinant of the matrix of the coefficients is set equal to zero. Matrix eigenvalue equations fall into this category, and we discussed the determination of the eigenvalues and eigenvectors, including the use of Mathematica to find the eigenvalues and eigenvectors.

## PROBLEMS

1. Solve the set of simultaneous equations.

$$
\begin{array}{l} 3 x + 4 y + 5 z = 1 \\ 4 x - 3 y + 6 z = 3 \\ 7 x + 2 y - 6 z = 2 \end{array}
$$

2. Solve the set of simultaneous equations.

$$
\begin{array}{r l} {y + z} & {= 1} \\ {x + z} & {= 2} \\ {x + y} & {= 3} \end{array}
$$

3. Solve the set of equations, using Cramer's rule.

$$
\begin{array}{r l} 3 x _ {1} + x _ {2} + x _ {3} & = 19 \\ x _ {1} - 2 x _ {2} + 3 x _ {3} & = 13 \\ x _ {1} + 2 x _ {2} + 2 x _ {3} & = 23 \end{array}
$$

Verify your result using Mathematica.

4. Solve the set of equations, using Gauss or Gauss-Jordan elimination.

$$
\begin{array}{r l} x _ {1} + x _ {2} + x _ {3} & = 9 \\ 2 x _ {1} - x _ {2} - x _ {3} & = 9 \\ x _ {1} + 2 x _ {2} - x _ {3} & = 9 \end{array}
$$

Use Mathematica to confirm your solution.

5. Solve the sets of equations.

$$
\begin{array}{r l} \mathbf {a}) & 3 x _ {1} + 4 x _ {2} + 5 x _ {3} = 25 \\ & 4 x _ {1} + 3 x _ {2} - 6 x _ {3} = - 7 \\ & x _ {1} + x _ {2} + x _ {3} = 6 \end{array}
$$

b)

$$
\left[ \begin{array}{c c c c} 1 & 1 & 1 & 3 \\ 2 & 1 & 1 & 1 \\ 1 & 2 & 3 & 4 \\ 2 & 0 & 1 & 4 \end{array} \right] \left[ \begin{array}{c} x _ {1} \\ x _ {2} \\ x _ {3} \\ x _ {4} \end{array} \right] = \left[ \begin{array}{c} 6 \\ 5 \\ 10 \\ 7 \end{array} \right].
$$

6. Decide whether the following set of equations has a solution. Solve the equations if it does.

$$
\begin{array}{r l} 3 x + 4 y + z & = 13 \\ 4 x + 3 y + 2 z & = 10 \\ 7 x + 7 y + 3 z & = 23 \end{array}
$$

7. Solve the set of equations by matrix inversion. If available, use Mathematica to invert the matrix.

$$
\begin{array}{r l} 2 x _ {1} + 4 x _ {2} + x _ {3} & = 40 \\ x _ {1} + 6 x _ {2} + 2 x _ {3} & = 55 \\ 3 x _ {1} + x _ {2} + x _ {3} & = 23 \end{array}
$$

8. Find the eigenvalues and eigenvectors of the matrix

$$
\left[ \begin{array}{c c c} 1 & 1 & 1 \\ 1 & 1 & 1 \\ 1 & 1 & 1 \end{array} \right].
$$

9. Find the eigenvalues and eigenvectors of the matrix

$$
\left[ \begin{array}{c c c} 0 & 1 & 1 \\ 1 & 0 & 1 \\ 1 & 1 & 0 \end{array} \right].
$$

10. Find the eigenvalues and eigenvectors of the matrix

$$
\left[ \begin{array}{l l l} 1 & 0 & 1 \\ 1 & 0 & 1 \\ 1 & 0 & 1 \end{array} \right].
$$

Does this matrix have an inverse?

11. In the Hückel method for finding approximate orbitals for electrons in a conjugated system of pi bonds, each orbital is represented as a linear combination of several basis functions. In the treatment of the cyclopropenyl radical, the basis functions are the three 2pz atomic orbitals, which we denote by $f_{1}$ , $f_{2}$ , and $f_{3}$ .

$$
\psi = c _ {1} f _ {1} + c _ {2} f _ {2} + c _ {3} f _ {3}
$$

The orbital energy, denoted by W, is expressed as a certain quotient of integrals and the minimum value of W is sought as a function of the c coefficients by differentiating with respect to each c and setting The three simultaneous equations are

$$
\begin{array}{l} x c _ {1} + c _ {2} + c _ {3} = 0 \\ c _ {1} + x c _ {2} + c _ {3} = 0 \\ c _ {1} + c _ {2} + x c _ {3} = 0, \end{array}
$$

where $x = (\alpha - W)/\beta$ and where $\alpha$ and $\beta$ are certain integrals whose values are to be determined later.

a) The determinant of the c coefficients must be set equal to zero in order for a nontrivial solution to exist. This is the secular equation. Solve the secular equation, which will yield three different values of x.

b) Solve the three simultaneous equations, once for each value of $x$ . Since there are only two independent equations, express $c_{2}$ and $c_{3}$ in terms of $c_{1}$ .

c) Impose the normalization condition

$$
c _ {1} ^ {2} + c _ {2} ^ {2} + c _ {3} ^ {2} = 1
$$

$$
\left[ \begin{array}{c c c} 1 & 1 & 1 \\ 1 & 1 & 1 \\ 1 & 1 & 1 \end{array} \right].
$$

to find the values of the c coefficients for each value of W.

d) Check your work by using Mathematica to find the eigenvalues and eigenvectors of the matrix

# The Treatment of Experimental Data

![[8274260271d38a2bce2fcd97d4516a240c780a8065efb684b5be959696ae23b8.jpg]]

## Preview

Some quantities in which we are interested can be measured directly. More often, a quantity must be calculated from other quantities that can be measured. This calculation process is called data reduction. The simplest form of data reduction is the use of a formula into which measured values are substituted. Other forms of data reduction include analysis of a set of data that can be represented by data points on a graph. Construction of such a graph and analysis of features of the graph, such as slopes and intercepts of lines, can provide values of variables. Statistical analysis done numerically can replace graphical analysis, providing better accuracy with less effort. We discuss both of these approaches.

We also discuss the analysis of the accuracy of experimental data. In the case that we can directly measure some desired quantity, we need to estimate the accuracy of the measurement. If data reduction must be carried out, we must study the propagation of errors in measurements through the data reduction process. The two principal types of experimental errors, random errors and systematic errors, are discussed separately. Random errors are subject to statistical analysis, and we discuss this analysis.

## Principal Facts and Ideas

1. Every measured quantity is subject to experimental error.

2. When the value of a measured quantity is reported, an estimate of the expected error should be included.

3. Random experimental errors can be analyzed statistically if the measurement can be repeated a number of times.

4. Systematic errors must usually be estimated by educated guesswork.

5. The mean of a set of repeated measurements is a better estimate of the correct value of a variable than is a single measurement.

6. The probable random error in the mean of a set of repeated measurements can be determined statistically.

7. When a variable is calculated by substitution of measured quantities into a formula, the estimated errors in the measured quantities can be propagated through the calculation.

8. Another type of data reduction involves fitting a set of data to a formula. This can be done graphically or numerically by use of the least-squares (regression) procedure.

## Objectives

After studying the chapter, you should be able to:

1. identify probable sources of error in a physical chemistry experiment and classify the errors as systematic or random;

2. calculate the mean and standard deviation of a sample of numbers;

3. calculate the probable error in the measured value of a directly measured quantity;

4. carry out data reduction using mathematical formulas and do an error propagation calculation to determine the probable error in the final calculated quantity;

5. carry out data reduction using graphical methods and determine the probable error in quantities obtained from the graphs;

6. carry out data reduction numerically using least squares and other numerical methods and determine probable errors in quantities obtained by these methods.

## 11.1 Experimental Errors in Measured Quantities

Once we have obtained a value for a measured quantity, we should try to determine how accurate that value is, since experimental error is always present. If a measurement can be repeated a number of times and if the repetitions agree well with each other, the set of data is said to have good precision. If a measurement agrees well with the correct value, it is said to have good accuracy. It is tempting to assume that a set of repetitions of a measurement that has high precision also has high accuracy, but this can be a poor assumption.

We divide experimental errors into two categories: Systematic errors recur with the same direction and with the same magnitude on every repetition of an experiment, so they can affect the accuracy of a measurement without affecting the precision. Random errors do not have the same direction and magnitude every time, so they affect the precision as well as the accuracy. Systematic errors are generally produced by limitations in the apparatus, whereas random errors usually arise from limitations in the technique used to carry out the experiment.

EXAMPLE 11.1 A simple apparatus for measuring the melting temperature of a substance consists of a small bath containing a liquid in which the sample can be suspended in a small capillary tube held next to a thermometer. The bath is slowly heated and the thermometer reading at the time of melting of the sample is recorded. List some of the possible experimental error sources in this determination. Classify each as systematic or random and guess its relative magnitude.

## SOLUTION ▶

(a) Faulty thermometer calibration. This is systematic. With an inexpensive thermometer, this error might be as large as several tenths of a degree.

(b) Lack of thermal equilibration between the liquid of the bath, the sample, and the thermometer. If the experimental procedure is the same for all repetitions, this will be systematic. If the thermometer is larger than the sample, it will likely be heated more slowly than the sample if the heating is done too rapidly. This error will probably be less than $1^{\circ}$ C.

(c) Failure to read the thermometer correctly. This is random. There are two kinds of error here. The first is more of a blunder than an experimental error and amounts to counting the marks on the thermometer incorrectly and, for example, recording 87.5 °C instead of 88.5 °C, and so on. The other kind of error is due to parallax, or looking at the thermometer at some angle other than a right angle. This might produce an error of about two-tenths of a degree Celsius.

(d) Presence of impurities in the sample. This is systematic, since impurities that dissolve in the liquid always lower the melting point. If carefully handled samples of purified substances are used, this error should be negligible.

(e) Failure to observe the onset of melting. This error is variable in magnitude, although always in the same direction. If the heating is done slowly, it should be possible to reduce this error to a few tenths of a degree.

Some of the errors in this example can be minimized by reducing the rate of heating. This suggests a possible procedure: an initial rough determination establishes the approximate value, and a final heating is done with slow and careful heating near the melting point.

EXERCISE 11.1 ▶ List as many sources of error as you can for some of the following measurements. Classify as systematic or random and estimate the magnitude of each source of error.

(a) The measurement of the diameter of a copper wire with a micrometer caliper.

(b) The measurement of the length of a piece of glass tubing with a meter stick.

(c) The measurement of the mass of a porcelain crucible using a digital balance.

(d) The measurement of the mass of a silver chloride precipitate in a porcelain crucible using a digital balance.

(e) The measurement of the resistance of an electrical heater using a Wheatstone bridge.

(f) The measurement of the time required for an automobile to travel the distance between two highway markers 1 km apart, using a stopwatch.

![[11ae32185108bf58c91a8f591e34457b1a7fb8466e78135b7a3082570b5e3870.jpg]]

The usual approach to systematic errors is to make an educated guess about the inherent accuracy of the apparatus. For example, if we use a wooden meter stick we might conclude that its length is probably accurate to 0.2% or 0.3% because of shrinkage or swelling of the wood or poor calibration when the meter stick was manufactured. If we use a mercury-in-glass thermometer, we might conclude that it is accurate to about 0.3 °C because of faulty manufacture or calibration. Although it is useful to engage in educated guesswork, it is better to have some kind of objective way to estimate the magnitude of experimental errors. There are two principal ways to gain information about systematic errors. One is to modify the apparatus and repeat the measurement or to repeat the measurement with a different apparatus. For example, in making a voltage measurement with a potentiometer, one compares the voltage with that of a standard cell. One could see if the same result is obtained with a different standard cell. If the result is different, you can assume that at least one of the standard cells is contributing a systematic error that is likely as large as the difference in the values. Another possibility a change in the design of the apparatus. For example, the apparatus may include some insulation that minimizes unwanted heat transfer. If the measurement gives a different value when the insulation is improved, there was probably a systematic error at least as big as the change in the result. It is even better to use a totally different apparatus, possibly in a different laboratory. There have been cases in the literature in which some quantity was measured in one laboratory and a certain probable error was specified. When the measurement was made in a different laboratory a value was obtained that differed significantly from the first value, exposing the existence of systematic error in one or both of the measurements.

The other approach to the study of systematic errors is to use the same apparatus to measure a well-known quantity, observing the actual experimental error. For example, if you are measuring the melting temperature of an unknown substance, you could also measure the melting temperature of a known substance and compare your result with the accepted result. Any discrepancy could be due to systematic error, although if only one measurement is made you cannot separate the effects of systematic and random errors. These methods of estimating systematic errors are usually not available in physical chemistry laboratory courses. In this event, educated guesswork is nothing to be ashamed of.

## 11.2 Statistical Treatment of Random Errors

Statistics is the study of a large set of people, objects, or numbers, called a population. The population is not studied directly, because of its large size or inaccessibility. A subset from the population, called a sample, is studied and the likely properties of the population are inferred from the properties of the sample. If several repetitions of a measurement can be made, this set of measurements can be considered to be a sample from a population. The population is an imaginary set of infinitely many repetitions of the measurement. Statistical analysis can be used to study the properties of the sample and to infer likely properties of the population.

## Properties of a Population

The infinitely many members in a population of numerical quantities will be distributed among all values in some range according to some probability distribution. We have discussed probability distributions in Chapter 5. A probability density or probability distribution $f(x)$ is defined such that

$$
(\text { probability   of   values   of } x \text { between } x ^ {\prime} \text { and } x ^ {\prime} + d x) = f (x ^ {\prime}) d x\tag{11.1}
$$

If the probability distribution is normalized the total probability of all occurrences equals unity:

$$
\boxed {\int_ {a} ^ {b} f (x)   d x = 1  ,}\tag{11.2}
$$

where a is the smallest possible value of x and b is the largest possible value. For convenience we will sometimes assume that $a = -\infty$ and that $b = +\infty$ . This is generally not correct for measured quantities, but the probability of values of x with large magnitude is small so that this assumption will not introduce significant errors

The most important property of a population of numerical quantities is its mean value. If there are no systematic errors, the mean of the population of measurements will equal the correct value of the measured quantity, since random errors are equally likely in either direction and will cancel in taking the mean. If the probability distribution $f(x)$ is normalized the population mean $\mu$ is given by Eq. (5.69),

$$
\boxed {\mu = \int_ {a} ^ {b} x f (x) d x.}\tag{11.3}
$$

The population standard deviation is a measure of the spread of the distribution, and is given by Eq. (5.74)

$$
\boxed {\sigma_ {x} = \left[ \int_ {a} ^ {b} (x - \mu) ^ {2} f (x) d x \right] ^ {1 / 2},}\tag{11.4}
$$

where we add a subscript x to remind us that x is the variable being discussed.

EXERCISE 11.2 ▶ Show that the definition of the standard deviation in Eq. (11.4) is the same as that in Eq. (5.74). That is, show that

$$
\int_ {a} ^ {b} (x - \mu) ^ {2} f (x) d x = \int_ {a} ^ {b} x ^ {2} f (x) d x - \left(\int_ {a} ^ {b} x f (x) d x\right) ^ {2}.\tag{11.5}
$$

![[a791ebeab33d39177850e8461ebf3818ac96807ba04277122c805a29f2bbf1fe.jpg]]

We will assume that any population of experimental results is governed by the Gaussian probability distribution (also called the normal distribution), introduced in Chapter 5. The important properties of that distribution are as listed in that chapter:

1. A total of 68.3% of the members of the population have their values of x lying within one standard deviation of the mean: in the interval $\mu - \sigma_{x} < x < \mu + \sigma_{x}$ .

2. A total of 95% of the members of the population have their values of x lying within 1.96 standard deviations of the mean: in the interval $\mu - 1.96\sigma_{x} < x < \mu + 1.96\sigma_{x}$ .

3. The fraction of the population with value of x in the interval $\mu - x_{1} < x < \mu + x_{1}$ is $\operatorname{erf}(x_{1}/\sqrt{2}\sigma)$ where $\operatorname{erf}(\cdots)$ stands for the error function, discussed in Appendix G.

If a random experimental error arises as the sum of many contributions, the central limit theorem of statistics gives some justification for assuming that our experimental error will be governed by the Gaussian distribution. This theorem states that if a number of random variables (independent variables) $x_{1}, x_{2}, \ldots, x_{n}$ are governed by some probability distributions with finite means and finite standard deviations, then a linear combination (weighted sum) of them

$$
y = \sum_ {i = 1} ^ {n} a _ {i} x _ {i}\tag{11.6}
$$

is governed by a probability distribution that approaches a Gaussian distribution as n becomes large. If experimental errors arise from multiple sources, they should be at least approximately described by a Gaussian distribution.

There are other probability distributions that are used in statistics, including the binomial distribution, the Poisson distribution, and the Lorentzian distribution. $^{1}$ We will not discuss these distributions. However, all of them have properties that are qualitatively similar to those of the Gaussian distribution.

## Properties of a Sample

Our sample is a set of repetitions of a measurement, which we think of as being selected randomly from a large population of many imaginary repetitions. From this sample, we need to estimate the correct value of the measured quantity and the probable error in this estimate. We will assume that an average of our set of measurements gives the best estimate of the population mean, which is equal to the correct value if there are no systematic errors. There are several common averages. The median is a value such that half of the members of a set are greater than the median and half are smaller than the median. The mode is the value that occurs most frequently in a set. The mean of a set of N values is defined by Eq. (5.59)

$$
\boxed {\bar {x} = \frac {1}{N} \sum_ {i = 1} ^ {N} x _ {i},}\tag{11.7}
$$

where $x_{1}, x_{2}, \ldots$ are the members of the set. In a population governed by the Gaussian distribution, the population median, the population mode, and the population mean all have the same value. In a sample of finite size the median, mode, and mean are not necessarily equal to each other. The mean of a sample taken from a population is said by statisticians to be an unbiased estimate of the population mean. We will use the mean of a set of repetitions as our estimate of the population mean, which is equal to the correct value if systematic errors are absent.

The sample standard deviation is defined by

$$
\boxed {s _ {x} = \left[ \frac {1}{N - 1} \sum_ {i = 1} ^ {N} (x _ {i} - \bar {x}) ^ {2} \right] ^ {1 / 2},}\tag{11.8}
$$

where $\bar{x}$ is the sample mean. The square of the standard deviation is called the variance. In Eq. (11.8), every term in the sum is positive or zero, since it is the square of a real quantity. The standard deviation can vanish only if every member of the sample is equal to the mean, and otherwise must be positive. The larger the differences between members of the set, the larger the standard deviation will be. In most cases, about two-thirds of the members of a sample will have values between $\bar{x} - s$ and $\bar{x} + s$ .

It has been shown that if we use the N-1 denominator of Eq. (11.8) instead of a denominator equal to N then s is an unbiased estimate of the population standard deviation $\sigma$ . This has to do with the fact that in a sample of N members, there are N pieces of information, which means that there are N-1 independent pieces of information in addition to the mean, or N-1 degrees of freedom in addition to the mean. $^{2}$

EXAMPLE 11.2 Find the mean and the standard deviation of the set of numbers 32.41, 33.76, 32.91, 33.04, 32.75, 33.23.

SOLUTION ▶

$$
\begin{array}{r c l} \bar {x} & = & \frac {1}{6} (32.41 + 33.76 + 32.91 + 33.04 + 32.75 + 33.23) = 33.02 \\ s & = & \left\{\frac {1}{5} \left[ (0.39) ^ {2} + (0.74) ^ {2} + (- 0.11) ^ {2} + (0.02) ^ {2} + (0.27) ^ {2} + (0.21) ^ {2} \right] \right\} ^ {1 / 2} \\ & = & 0.41. \end{array}
$$

One of the six numbers lies below 32.61, and one lies above 33.43, so that two-thirds of them lie between $\bar{x} - s$ and $\bar{x} + s$ .

EXERCISE 11.3 ▶ Find the mean, $\bar{x}$ , and the sample standard deviation, s, for the following set of values: 2.876m, 2.881m, 2.864m, 2.879m, 2.872m, 2.889m, 2.869m. Determine how many values lie below $\bar{x} - s$ and how many lie above $\bar{x} + s$ .

## Numerical Estimation of Random Errors

A common practice among scientific workers is to make statements that have a 95% probability of being correct. Such a statement is said to be at the 95% confidence level. For example, we want to make a statement of the form

$$
\text { correct   value } = \mu = \bar {x} \pm \varepsilon\tag{11.9}
$$

that has a 95% chance of being right. That is, we want to state an interval $\bar{x} - \varepsilon < x < \bar{x} + \varepsilon$ that has a 95% chance of containing the correct value $\mu$ , which we do not know. We call such an interval the 95% confidence interval, and we call the positive number $\varepsilon$ the probable error at the 95% confidence level or the estimated error. If we knew the value of $\sigma$ , the population standard deviation, we could make this statement after a single measurement. Since a single measurement has a 95% change of being within $1.96\sigma$ of $\mu$ , we could say with 95% confidence that

$$
\mu = x \pm 1.96 \sigma ,\tag{11.10}
$$

where x is the outcome of our single measurement. If we have no opportunity to repeat our measurement, the only thing we can do is to make educated guess of the value of $\sigma$ .

However, let us assume that we can make N measurements of the same quantity. Think of our set of N measurements as only one possible set of N measurements from the same population. If we could take infinitely many sets of N measurements from our population, the means of these sets would themselves form a new population. If the original population is governed by a Gaussian distribution, the population of sample means will also be governed by a Gaussian distribution (although we do not prove this fact). The mean of this new population is the same as the mean of the original population, and $\sigma_{m}$ , the standard deviation of the population of sample means, is given by

$$
\sigma_ {m} = \frac {\sigma}{\sqrt {N}},\tag{11.11}
$$

where $\sigma$ is the standard deviation of the original population. The new population of sample means has a smaller spread than the original population, and its spread becomes smaller as N becomes larger. That is, the means of the sets of measurements cluster more closely about the population mean if the number of members of each sample is made larger. If N = 10, $\sigma_{m} = 0.3162\sigma$ , and if N = 100, $\sigma_{m} = 0.100\sigma$ . Most people intuitively agree with the notion that the average of a set of measurements is more likely to come close to the correct value than is a single measurement.

If we knew the standard deviation of the original population, we would now be able to write an expression for the expected error in the mean of a set of N measurements:

$$
\varepsilon = 1.96 \sigma_ {m} = \frac {1 .96 \sigma}{\sqrt {N}}.\tag{11.12}
$$

However, we do not know the population standard deviation. Since we use the sample standard deviation as our estimate of the population standard deviation, we could write as a first approximation

$$
\varepsilon = \frac {1 .96 s}{\sqrt {N}} \quad (\text { first   approximation }),\tag{11.13}
$$

where s is the sample standard deviation. However, there is better estimate. A statistically correct formula was derived by Gossett. $^{3}$ Gossett defined the Student t factor

$$
t = \frac {(\bar {x} - \mu) N ^ {1 / 2}}{s},\tag{11.14}
$$

where $\mu$ is the population mean, $\bar{x}$ is the sample mean, and s is the sample standard deviation. There is a different value of t for every sample. Although $\mu$ is not known, Gossett derived the probability distribution that t obeys. $^{4}$ From this distribution, which is called Student's t distribution, the maximum value of t corresponding to a given confidence level can be calculated for any value of N. The notation used is $t(\nu, 0.05)$ . The quantity $\nu$ is the number of degrees of freedom, equal to N - 1, and 0.05 represents the confidence level of 95%. Table 11.1 gives these values for various values of N and for four different confidence levels. Notice that as N becomes large the maximum Student t value for 95% confidence (also called 0.05 significance) approaches 1.96, the factor in Eq. (11.13). For fairly small values of N the Student t distribution corresponds to larger probability for large values of $x - \mu$ than does the Gaussian distribution. However, as N becomes large the Student t distribution approaches a Gaussian distribution. Unfortunately, some authors use a different notation for the critical value of t, such as $t_{\nu}(0.025)$ to represent the Student t factor for $\nu + 1$ data points at the 95% confidence level. $^{5}$

Using a value from Table 11.1, we can write a formula for the expected error in the mean at the 95% confidence level

$$
\boxed {\varepsilon = \frac {t (\nu , 0 .05) s}{\sqrt {N}}}\tag{11.15}
$$

for a sample of $\nu + 1$ members ( $N$ members).

TABLE 11.1 ▶ Some Values of Student's t Factor\*

<table><tr><td rowspan="2">Number of Degrees of Freedom $\nu$ </td><td colspan="4">Maximum Value of Student&#x27;s  $t$  Factor for the Significance Levels Indicated</td></tr><tr><td> $t(\nu, 0.60)$ </td><td> $t(\nu, 0.10)$ </td><td> $t(\nu, 0.05)$ </td><td> $t(\nu, 0.01)$ </td></tr><tr><td>1</td><td>1.376</td><td>6.314</td><td>12.706</td><td>63.657</td></tr><tr><td>2</td><td>1.061</td><td>2.920</td><td>4.303</td><td>9.925</td></tr><tr><td>3</td><td>0.978</td><td>2.353</td><td>3.182</td><td>5.841</td></tr><tr><td>4</td><td>0.941</td><td>2.132</td><td>2.776</td><td>4.604</td></tr><tr><td>5</td><td>0.920</td><td>2.015</td><td>2.571</td><td>4.032</td></tr><tr><td>6</td><td>0.906</td><td>1.943</td><td>2.447</td><td>3.707</td></tr><tr><td>7</td><td>0.896</td><td>1.895</td><td>2.365</td><td>3.499</td></tr><tr><td>8</td><td>0.889</td><td>1.860</td><td>2.306</td><td>3.355</td></tr><tr><td>9</td><td>0.883</td><td>1.833</td><td>2.262</td><td>3.250</td></tr><tr><td>10</td><td>0.879</td><td>1.812</td><td>2.228</td><td>3.169</td></tr><tr><td>11</td><td>0.876</td><td>1.796</td><td>2.201</td><td>3.106</td></tr><tr><td>12</td><td>0.873</td><td>1.782</td><td>2.179</td><td>3.055</td></tr><tr><td>13</td><td>0.870</td><td>1.771</td><td>2.160</td><td>3.012</td></tr><tr><td>14</td><td>0.868</td><td>1.761</td><td>2.145</td><td>2.977</td></tr><tr><td>15</td><td>0.866</td><td>1.753</td><td>2.131</td><td>2.947</td></tr><tr><td>16</td><td>0.865</td><td>1.746</td><td>2.120</td><td>2.921</td></tr><tr><td>17</td><td>0.863</td><td>1.740</td><td>2.110</td><td>2.898</td></tr><tr><td>18</td><td>0.862</td><td>1.734</td><td>2.101</td><td>2.878</td></tr><tr><td>19</td><td>0.861</td><td>1.729</td><td>2.093</td><td>2.861</td></tr><tr><td>20</td><td>0.860</td><td>1.725</td><td>2.086</td><td>2.845</td></tr><tr><td>21</td><td>0.859</td><td>1.721</td><td>2.080</td><td>2.831</td></tr><tr><td>22</td><td>0.858</td><td>1.717</td><td>2.074</td><td>2.819</td></tr><tr><td>23</td><td>0.858</td><td>1.714</td><td>2.069</td><td>2.807</td></tr><tr><td>24</td><td>0.857</td><td>1.711</td><td>2.064</td><td>2.797</td></tr><tr><td>25</td><td>0.856</td><td>1.708</td><td>2.060</td><td>2.787</td></tr><tr><td>26</td><td>0.856</td><td>1.706</td><td>2.056</td><td>2.479</td></tr><tr><td>27</td><td>0.855</td><td>1.703</td><td>2.052</td><td>2.771</td></tr><tr><td>28</td><td>0.855</td><td>1.701</td><td>2.048</td><td>2.763</td></tr><tr><td>29</td><td>0.854</td><td>1.699</td><td>2.045</td><td>2.756</td></tr><tr><td>30</td><td>0.854</td><td>1.697</td><td>2.042</td><td>2.750</td></tr><tr><td>40</td><td>0.851</td><td>1.684</td><td>2.021</td><td>2.704</td></tr><tr><td>60</td><td>0.848</td><td>1.671</td><td>2.000</td><td>2.660</td></tr><tr><td> $\infty$ </td><td>0.842</td><td>1.645</td><td>1.960</td><td>2.576</td></tr></table>

\* John A. Rice, Mathematical Statistics and Data Analysis, Wadsworth & Brooks/Cole, Pacific Grove, CA, 1988, p. 560

EXAMPLE 11.3 Assume that the melting temperature of calcium nitrate tetrahydrate, $\mathrm{Ca(NO_3)_2\cdot 4H_2O}$ , has been measured 10 times, and that the results are $42.70^{\circ}\mathrm{C}$ , $42.60^{\circ}\mathrm{C}$ , $42.78^{\circ}\mathrm{C}$ , $42.83^{\circ}\mathrm{C}$ , $42.58^{\circ}\mathrm{C}$ , $42.68^{\circ}\mathrm{C}$ , $42.65^{\circ}\mathrm{C}$ , $42.76^{\circ}\mathrm{C}$ , $42.73^{\circ}\mathrm{C}$ , and $42.71^{\circ}\mathrm{C}$ . Ignoring systematic errors, determine the $95\%$ confidence interval for the set of measurements.

SOLUTION ▶ Our estimate of the correct melting temperature is the sample mean:

$$
\begin{array}{r l} \bar {T} _ {m e l t} & = \frac {1}{10} (42.70 ^ {\circ} \mathrm{C} + 42.60 ^ {\circ} \mathrm{C} + 42.78 ^ {\circ} \mathrm{C} + 42.83 ^ {\circ} \mathrm{C} + 42.58 ^ {\circ} \mathrm{C} + 42.68 ^ {\circ} \mathrm{C} + \\ & \quad 42.65 ^ {\circ} \mathrm{C} + 42.76 ^ {\circ} \mathrm{C} + 42.73 ^ {\circ} \mathrm{C} + 42.71 ^ {\circ} \mathrm{C}) \\ & = 42.70 ^ {\circ} \mathrm{C} \end{array}
$$

The sample standard deviation is

$$
\begin{array}{r l} {s} & {= \left\{\frac {1}{9} [ (0.00 ^ {\circ} \mathrm{C}) ^ {2} + (0.10 ^ {\circ} \mathrm{C}) ^ {2} + (0.08 ^ {\circ} \mathrm{C}) ^ {2} + (0.13 ^ {\circ} \mathrm{C}) ^ {2} + (0.12 ^ {\circ} \mathrm{C}) ^ {2} + \right.} \\ & {\qquad \left. (0.02 ^ {\circ} \mathrm{C}) ^ {2} + (0.05 ^ {\circ} \mathrm{C}) ^ {2} + (0.16 ^ {\circ} \mathrm{C}) ^ {2} + (0.13 ^ {\circ} \mathrm{C}) ^ {2} + (0.01 ^ {\circ} \mathrm{C}) ^ {2} ] \right\} ^ {1 / 2}} \\ & {= 0.08 ^ {\circ} \mathrm{C}} \end{array}
$$

The value of $t(9, 0.05)$ is found from Table 11.1 to equal 2.26, so that

$$
\varepsilon = \frac {(2 .26) (0 .08 ^ {\circ} \mathrm{C})}{\sqrt {10}} = 0.06 ^ {\circ} \mathrm{C}.
$$

Therefore, at the 95% confidence level, $T_{melt} = 42.70^{\circ}C \pm 0.06^{\circ}C$ .

EXERCISE 11.4 Assume that the H–O–H bond angles in various crystalline hydrates have been measured to be $108^{\circ}$ , $109^{\circ}$ , $110^{\circ}$ , $103^{\circ}$ , $111^{\circ}$ , and $107^{\circ}$ . Give your estimate of the correct bond angle and its 95% confidence interval.

## Rejection of Discordant Data

Sometimes a repetition of a measurement yields a value that differs greatly from the other members of the sample (a discordant value). For example, say that we repeated the measurement of the melting temperature of $\mathrm{Ca(NO_{3})_{2}\cdot4H_{2}O}$ in the previous example one more time and obtained a value of $39.75^{\circ}C$ . If we include this eleventh data point, we get a sample mean of $42.43^{\circ}C$ and a sample standard deviation of $0.89^{\circ}C$ . Using the table of Student's t values, we obtain a value for $\varepsilon$ of $0.60^{\circ}C$ at the 95% confidence level. Some people think that the only honest thing to do is to report the melting temperature as $42.4\pm0.6^{\circ}C$ .

If we assume that our sample standard deviation of $0.89^{\circ}$ C is a good estimate of the population standard deviation, our data point of $39.75^{\circ}$ C is 3.01 standard deviations away from the mean. From the table of the error function in Appendix G, the probability of a randomly chosen member of a population differing from the mean by this much or more is 0.003, or 0.3%. There is considerable justification for asserting that such an improbable event was due not to random experimental errors but to some kind of a mistake, such as misreading a thermometer. If you assume this, you discard the suspect data point and recompute the mean and standard deviation just as though the discordant data point had not existed. Do not discard more than one data point from a set of data. If two or more apparently discordant data points occur in a set, you should regard it as a signal that the data simply have low precision.

There are several rules for deciding whether to discard a data point. Some people discard data points that are more than 2.7 standard deviations from the mean (this means 2.7 standard deviations calculated with the discordant point left in). This discards points that have less than a 1% chance of having arisen through normal experimental error. Pugh and Winslow $^{6}$ suggest that for a sample of N data points, a data point should be discarded if there is less than one chance in 2N that the point came from the same population. This rule discards more points than the first rule for a sample of 10 measurements, since it would discard a point lying 1.96 standard deviations from the mean in a sample of 10 measurements. Since you would expect such a point to occur once in 20 times, the probability that it would occur in a sample of 10 by random chance is fairly large.

TABLE 11.2 ▶ Critical Q Values at the 95% Confidence Level

<table><tr><td>N</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td><td>10</td><td>20</td><td>30</td></tr><tr><td>Q</td><td>0.97</td><td>0.84</td><td>0.72</td><td>0.63</td><td>0.58</td><td>0.53</td><td>0.50</td><td>0.47</td><td>0.36</td><td>0.30</td></tr></table>

There is a test called the Q test, in which Q is defined as the difference between an “outlying” data point and its nearest neighbor divided by the difference between the highest and the lowest values in the set:

$$
Q = \boxed {\frac {(\text { outlying   value }) - (\text { value   nearest   the   outlying   value })}{(\text { highest   value }) - (\text { lowest   value })}}\tag{11.16}
$$

An outlying data point is discarded if its value of Q of exceeds a certain critical value, which depends on the number of members in the sample. Table 11.2 contains the critical value of Q at the 95% confidence level for samples of N members. $^{7}$

EXERCISE 11.5 ▶ Apply the Q test to the 39.75 °C data point appended to the data set of Example 11.2.

## 11.3 Data Reduction and the Propagation of Errors

Many values that are obtained by measurement in a physical chemistry laboratory are used along with other values to calculate some quantity that is not directly measured. Such a calculation is call data reduction. An experimental error in a measured quantity will affect the accuracy of any quantity that is calculated from it. This is called propagation of errors.

## The Combination of Errors

Assume that we have measured two quantities, a and b, and have established a probable value and a 95% confidence interval for each:

$$
a = \bar {a} \pm \varepsilon_ {a}\tag{11.17a}
$$

$$
b = \bar {b} \pm \varepsilon_ {b},\tag{11.17b}
$$

where $\bar{a}$ is our probable value of a, perhaps from a single measurement or perhaps from a mean of several measurements, and $\varepsilon_{a}$ is our expected error in a, perhaps computed from Eq. (11.15) or perhaps obtained by educated guesswork. Analogous quantities are defined for b. Assume that we want to obtain a probable value and a 95% confidence interval for c, the sum of a and b. The probable value of c is the sum of $\bar{a}$ and $\bar{b}$ :

$$
\bar {c} = \bar {a} + \bar {b}.\tag{11.18}
$$

A simple estimate of the probable error in c is the sum of $\varepsilon_{a}$ and $\varepsilon_{b}$ , which corresponds to the assumption that the errors in the two quantities always add together:

$$
\varepsilon_ {c} = \varepsilon_ {a} + \varepsilon_ {b} \quad (\text { simple   preliminary   estimate }).\tag{11.19}
$$

However, Eq. (11.19) provides an overestimate, because there is some chance that errors in a and in b will be in opposite directions. If a and b are both governed by Gaussian distributions, mathematicians have shown that c is also governed by a Gaussian distribution, and that the probable error in c is given by

$$
\boxed {\varepsilon_ {c} = (\varepsilon_ {a} ^ {2} + \varepsilon_ {b} ^ {2}) ^ {1 / 2}.}\tag{11.20}
$$

This formula allows for the statistically correct probability of cancellation of errors.

EXAMPLE 11.4 Two lengths have been measured as $24.8 \, m \pm 0.4 \, m$ and $13.6 \, m \pm 0.3 \, m$ . Find the probable value of their sum and its probable error.

SOLUTION ▶ The probable value of the sum is $24.8 \, m + 13.6 \, m = 38.4 \, m$ , and the probable error is $\varepsilon = [(0.4 \, \text{m})^2 + (0.3 \, \text{m})^2]^{1/2} = 0.5 \, \text{m}$ . Therefore, the sum is reported as $38.4 \, m \pm 0.5 \, m$ .

EXERCISE 11.6 ▶ Two time intervals have been clocked as $56.57 \, s \pm 0.13 \, s$ and $75.12 \, s \pm 0.17 \, s$ . Find the probable value of their sum and its probable error.

## The Combination of Random and Systematic Errors

Statistics can be used to determine the probable error due to random errors if the measurements can be repeated. The probable error due to systematic errors can be estimated by apparatus modification or by guesswork. These errors combine in the same way as the errors in Eq. (11.20). If $\varepsilon_{r}$ is the probable error due to random errors and $\varepsilon_{s}$ is the probable error due to systematic errors, the total probable error is given by

$$
\boxed {\varepsilon_ {t} = (\varepsilon_ {s} ^ {2} + \varepsilon_ {r} ^ {2}) ^ {1 / 2}.}\tag{11.21}
$$

In using this formula, you must try to make your estimate of the systematic error conform to the same level of confidence as your random error. If you use the 95% confidence level for the random errors, do not estimate the systematic errors at the 50% confidence level, which is what most people instinctively tend to do when asked what they think a probable error is. You might make a first guess at your systematic errors and then double it to avoid this underestimation.

EXAMPLE 11.5 Assume that you estimate the total systematic error in the melting temperature measurement of Example 11.3 as 0.20°C at the 95% confidence level. Find the total expected error.

SOLUTION ▶

$$
\varepsilon_ {t} = [ (0.06 ^ {\circ} \mathrm{C}) ^ {2} + (0.20 ^ {\circ} \mathrm{C}) ^ {2} ] ^ {1 / 2} = 0.21 ^ {\circ} \mathrm{C}.
$$

Notice that if two sources of error combine additively and if one is much larger than the other, the smaller error makes a much smaller contribution after the errors are squared. If the error from one source is five times as large as the other, its contribution is 25 times as large, and the smaller error source can be neglected.

## Error Propagation in Data Reduction Using Mathematical Formulas

In the Dumas method for determining the molar mass of a volatile liquid, $^{8}$ one uses the formula

$$
M = \frac {w R T}{P V},\tag{11.22}
$$

where M is the molar mass, w is the mass of the sample of the substance contained in volume V at pressure P and temperature T, and R is the ideal gas constant. We think of Eq. (11.22) as being an example of a general formula,

$$
y = y (x _ {1}, x _ {2}, x _ {3}, \dots , x _ {n}).\tag{11.23}
$$

Let us assume that we have a 95% confidence interval for each of the independent variables $x_{1}, x_{2}, \cdots$ such that

$$
x _ {i} = \bar {x} _ {i} \pm \varepsilon_ {i} (i = 1, 2, \dots , n).\tag{11.24}
$$

Our problem is to take the uncertainties in $x_{1}$ , $x_{2}$ , and so on, and calculate the uncertainty in y, the dependent variable. This is called the propagation of errors. If the errors are not too large, we can take an approach based on a differential calculus. The fundamental equation of differential calculus is Eq. (7.9),

$$
d y = \left(\frac {\partial y}{\partial x _ {1}}\right) d x _ {1} + \left(\frac {\partial y}{\partial x _ {2}}\right) d x _ {2} + \left(\frac {\partial y}{\partial x _ {3}}\right) d x _ {3} + \dots + \left(\frac {\partial y}{\partial x _ {n}}\right) d x _ {n}.\tag{11.25}
$$

This equation gives an infinitesimal change in the dependent variable y due to arbitrary infinitesimal changes in the independent variables $x_{1}, x_{2}, x_{3}, \ldots, x_{n}$ .

If finite changes $\Delta x_{1}, \Delta x_{2}$ , and so on, are made in the independent variables, we could write as an approximation

$$
\Delta y \approx \left(\frac {\partial y}{\partial x _ {1}}\right) \Delta x _ {1} + \left(\frac {\partial y}{\partial x _ {2}}\right) \Delta x _ {2} + \dots + \left(\frac {\partial y}{\partial x _ {n}}\right) \Delta x _ {n}.\tag{11.26}
$$

If we had some known errors in $x_{1}$ , $x_{2}$ , and so on, we could use Eq. (11.26) to calculate a known error in y. Since all we have is probable errors in the independent variables and do not know whether the actual errors are positive or negative, one cautious way to proceed would be to assume that the worst might happen and that all the errors would add:

$$
\varepsilon_ {y} \approx \left| \left(\frac {\partial y}{\partial x _ {1}}\right) \varepsilon_ {1} \right| + \left| \left(\frac {\partial y}{\partial x _ {2}}\right) \varepsilon_ {2} \right| + \dots + \left| \left(\frac {\partial y}{\partial x _ {n}}\right) \Delta x _ {n} \right| (\text { first   estimate }),\tag{11.27}
$$

where $\varepsilon_{1}, \varepsilon_{2}, \cdots, \varepsilon_{n}$ , represent the expected errors in the independent variables and $\varepsilon_{y}$ represents the expected error in y. This equation overestimates the error in y because there is some probability that the errors in the x values will cancel instead of adding. An equation that incorporates the statistical probability of error cancellation is

$$
\varepsilon_ {y} \approx \left[ \left(\frac {\partial y}{\partial x _ {1}}\right) ^ {2} \varepsilon_ {1} ^ {2} + \left(\frac {\partial y}{\partial x _ {2}}\right) ^ {2} \varepsilon_ {2} ^ {2} + \dots + \left(\frac {\partial y}{\partial x _ {n}}\right) ^ {2} \varepsilon_ {n} ^ {2} \right] ^ {1 / 2} (\text {final formula})\tag{11.28}
$$

This equation is analogous to Eq. (11.21). It will be our working equation for the propagation of errors through formulas. Since it is based on a differential formula, it becomes more nearly exact if the errors are small.

EXAMPLE 11.6 (a) Find the expression for the propagation of errors for the Dumas molar mass determination.

(b) Apply this expression to the following set of data for n-hexane:

$$
T = 373.15 \pm 0.25 \mathrm{K}
$$

$$
V = 206.34 \pm 0.15 \mathrm{ml}
$$

$$
P = 760 \pm 0.2 \mathrm{torr}
$$

$$
w = 0.585 \pm 0.005 \mathrm{g}.
$$

SOLUTION ▶ (a) The analogue of Eq. (11.28) for our equa-

tion is

$$
\varepsilon_ {M} \approx \left[ \left(\frac {R T}{P V}\right) ^ {2} \varepsilon_ {w} ^ {2} + \left(\frac {w R}{P V}\right) ^ {2} \varepsilon_ {T} ^ {2} + \left(\frac {w R T}{P ^ {2} V}\right) ^ {2} \varepsilon_ {P} ^ {2} + \left(\frac {w R T}{P V ^ {2}}\right) ^ {2} \varepsilon_ {V} ^ {2} \right] ^ {1 / 2}
$$

Substituting the numerical values, we obtain

$$
M = \frac {(0 .585 \mathrm{g}) (0 .0820571 \mathrm{atmK} ^ {- 1} \mathrm{mol} ^ {- 1}) (373 .15 \mathrm{K})}{(1 .000 \mathrm{atm}) (0 .206341)} = 86.81 \mathrm{gmol} ^ {- 1}.
$$

We do not report the numerical calculation of the expected error, but the result is

$$
\begin{array}{r} \varepsilon_ {M} = 0.747 \mathrm{g} \mathrm{mol} ^ {- 1} \\ M = 86.8 \pm 0.7 \mathrm{g} \mathrm{mol} ^ {- 1}. \end{array}
$$

![[778aac109600dd745062339b62234dd8b2a2cc7edd9c0fec2389acadabd505d6.jpg]]

One significant digit suffices in an expected error. The digit 8 after the decimal point in the value of M in the previous example is not quite significant, but since the error is smaller than $1.0 \, g \, mol^{-1}$ , it provides a little information, and we include it. The accepted value is $86.17 \, g \, mol^{-1}$ , so that our expected error is larger than our actual error, as it should be about 95% of the time.

EXERCISE 11.7 ▶ In the cryoscopic determination of molar mass, $^{a}$ the molar mass in kg mol $^{-1}$ is given by

$$
M = \frac {w K _ {f}}{W \Delta T _ {f}} (1 - k _ {f} \Delta T _ {f}),
$$

where W is the mass of the solvent in kilograms, w is the mass of the unknown solute in kilograms, $\Delta T_{f}$ is the amount by which the freezing point of the solution is less than that of the pure solvent, and $K_{f}$ and $k_{f}$ are constants characteristic of the solvent. Assume that in a given experiment, a sample of an unknown substance was dissolved in benzene, for which $K_{f} = 5.12 \, K \, kg mol^{-1}$ and $k_{f} = 0.011 \, K^{-1}$ . For the following data, calculate M and its probable error:

$$
\begin{array}{r l} W & = 13.185 \pm 0.003 \mathrm{g} \\ w & = 0.423 \pm 0.002 \mathrm{g} \\ \Delta T _ {f} & = 1.263 \pm 0.020 \mathrm{K}. \end{array}
$$

(11.29)

TABLE 11.3 ▶ Experimental Vapor Pressures of Pure Ethanol at Various Temperature

<table><tr><td>t/°C</td><td>T/K</td><td>Vapor Pressure/torr</td><td>Expected Error/torr</td></tr><tr><td>25.00</td><td>298.15</td><td>55.9</td><td>3.0</td></tr><tr><td>30.00</td><td>303.15</td><td>70.0</td><td>3.0</td></tr><tr><td>35.00</td><td>308.15</td><td>93.8</td><td>4.2</td></tr><tr><td>40.00</td><td>313.15</td><td>117.5</td><td>5.5</td></tr><tr><td>45.00</td><td>318.15</td><td>154.1</td><td>6.0</td></tr><tr><td>50.00</td><td>323.15</td><td>190.7</td><td>7.6</td></tr><tr><td>55.00</td><td>328.15</td><td>241.9</td><td>8.0</td></tr><tr><td>60.00</td><td>333.15</td><td>304.15</td><td>8.8</td></tr><tr><td>65.00</td><td>338.15</td><td>377.9</td><td>9.5</td></tr></table>

![[c995f0c7ea57bc72b242a6db8f02a10bc83f2f52d82483d364d5a7dee936c05f.jpg]]  
Figure 11.1 ▶ The vapor pressure of ethanol as a function of temperature.

phase transition is

$$
\frac {d P}{d T} = \frac {\Delta H _ {m}}{T \Delta V _ {m}},\tag{11.30}
$$

where P is the pressure, $\Delta H_{m}$ is the molar enthalpy change of the phase transition, T is the absolute temperature, and $\Delta V_{m}$ is the molar volume change of the phase transition. If $\Delta V_{m}$ is known and the value of the derivative dP/dT can be determined, then the enthalpy change of vaporization can be calculated. The derivative dP/dT is the slope of the tangent line at the point being considered (see Chapter 4). After a smooth curve has been drawn as in Fig. 11.1, a tangent line can be constructed. Two line segments can be drawn parallel to the coordinate axes, forming a right triangle with the tangent line, as is shown in the figure.

## EXAMPLE 11.7 Determine the value of dP/dT from the triangle in Fig. 11.1

SOLUTION ▶ The slope of the tangent line is equal to the height of the triangle divided by its base (“rise” over “run”). This gives

$$
\frac {d P}{d T} = \frac {115 \mathrm{torr}}{20 .0 \mathrm{K}} = 5.75 \mathrm{torrK} ^ {- 1}\tag{11.31}
$$

## Numerical Differentiation

Drawing a graph and constructing a tangent by hand in is tedious. There are numerical procedures that can be carried out on a computer. The first procedure is “smoothing” data. The idea is that the mathematical function that the data should conform to is continuous and smooth, so that if we adjust the data points so that they lie closer to a smooth curve, we have probably reduced the experimental errors. One procedure is based on choosing polynomial functions that provide smoothed values of the function. If we have the set of data points $(x_{1}, y_{1}), (x_{2}, y_{2}), (x_{3}, y_{3})$ , and so on, such that the x values are equally spaced, a smoothed value for the dependent variable $y_{i}$ is given by $^{9}$

$$
y _ {i} = \frac {1}{35} \left[ 17 y _ {i} + 12 (y _ {i + 1} + y _ {i - 1}) - 3 (y _ {i + 2} + y _ {i - 2}) \right].\tag{11.32}
$$

This equation corresponds to the value of the 3rd-degree polynomial that most nearly fits the five data points included in the formula and is valid only for equally spaced values of $x$ . There are also similar formulas that involve a larger number of points.

We now define a set of differences, which are used to calculate numerical approximations to derivatives for a set of equally spaced data points. The first difference for the ith point is defined by

$$
\Delta y _ {i} = y _ {i + 1} - y _ {i}.\tag{11.33a}
$$

The second difference for the i th point is defined by

$$
\Delta^ {2} y _ {i} = \Delta y _ {i + 1} - \Delta y _ {i} = y _ {i + 2} - 2 y _ {i + 1} + y _ {i}.\tag{11.33b}
$$

The third difference for the $i$ th point is defined by

$$
\Delta^ {3} y _ {i} = \Delta^ {2} y _ {i + 1} - \Delta^ {2} y _ {i}.\tag{11.33c}
$$

Higher-order differences are defined in a similar way. For data sets of ordinary accuracy, the values of y in Eqs. (11.33a) should be the smoothed values given by Eq. (11.32). This set of differences for point number i involves only points with subscripts greater than or equal to i. Other schemes can be defined that use points on both sides of the ith data point.

A numerical value for the derivative dy/dx at the ith point is given by $^{10}$

$$
\left. \frac {d y}{d x} \right| _ {x = x _ {i}} = \frac {1}{w} \left(\Delta y _ {i} - \frac {1}{2} \Delta^ {2} y _ {i} + \frac {1}{3} \Delta^ {3} y _ {i} - \frac {1}{4} \Delta^ {4} y _ {i} + \dots\right),\tag{11.34}
$$

where $w$ is the spacing between values of $x$ :

$$
w = x _ {i + 1} - x _ {i}.\tag{11.35}
$$

Equation (11.34) is based on the Gregory–Newton interpolation formula. $^{11}$ The second derivative is given by

$$
\left. \frac {d ^ {2} y}{d x ^ {2}} \right| _ {x = x _ {i}} = \frac {1}{w ^ {2}} \left(\Delta^ {2} y _ {i} - \Delta^ {3} y _ {i} + \frac {11}{12} \Delta^ {4} y _ {i} - \frac {10}{12} \Delta^ {5} y _ {i} + \dots\right).\tag{11.36}
$$

EXAMPLE 11.8 Smooth the data of Table 11.3. Find the value of the derivative $dP/dT$ at $40^{\circ}\mathrm{C}$ and find the value of $\Delta H_{m}$ .

SOLUTION ▶ The data were entered into an Excel spreadsheet and smoothed. The first three differences were calculated, and the derivative was calculated for the $40^{\circ}$ C data point.

$$
\frac {d P}{d T} = 5.75 \mathrm{torrK} ^ {- 1}\tag{11.37}
$$

The enthalpy change of vaporization was calculated using the approximation

$$
\Delta V _ {m} = V _ {m} (g a s) - V _ {m} (l i q u i d) \approx V _ {m} (g a s) = \frac {R T}{P}\tag{11.38}
$$

$$
\Delta H _ {m} = T V _ {m} \frac {d P}{d T} = \frac {R T ^ {2}}{P} \frac {d P}{d T} = \frac {(8 .3145 \mathrm{JK} ^ {- 1} \mathrm{mol} ^ {- 1}) (313 .15 \mathrm{K}) ^ {2} (5 .75 \mathrm{torrK} ^ {- 1})}{119 .7 \mathrm{torr}} \tag {1}\tag{11.39}
$$

$$
= 39200 \mathrm{J} \mathrm{mol} ^ {- 1} = 39.2 \mathrm{kJ} \mathrm{mol} ^ {- 1}\tag{11.40}
$$

Notice that we did not use SI units for all quantities, but that the torr unit canceled, so that the correct answer was obtained.

EXERCISE 11.8 The rate of a first-order chemical reaction obeys the equation

$$
- \frac {d c}{d t} = k c,\tag{11.41}
$$

where c is the concentration of the reactant and k is a function of temperature called the rate constant. The following is a set of data for the following reaction at $25^{\circ}C.^{a}$

$$
\left(\mathrm{CH} _ {3}\right) _ {3} \mathrm{CBr} + \mathrm{H} _ {2} \mathrm{O} \rightarrow \left(\mathrm{CH} _ {3}\right) _ {3} \mathrm{COH} + \mathrm{HBr}
$$

$$
\begin{array}{l l} \text {Time / h} & [ (\mathbf {C H} _ {3}) _ {3} \mathbf {C B r} ] / \mathrm{mol} \mathrm{l} ^ {- 1} \\ 0 & 0.1051 \\ 5 & 0.0803 \\ 10 & 0.0614 \\ 15 & 0.0470 \\ 20 & 0.0359 \\ 25 & 0.0274 \\ 30 & 0.0210 \\ 35 & 0.0160 \\ 40 & 0.0123 \end{array}
$$

Smooth the data using Eq. (11.32). Using Excel, make a table of the first, second, third, and fourth differences. Use Eq. (11.34) to evaluate the derivative dc/dt at t = 20 h. Use this value to evaluate the rate constant.

## Linearization

In some cases, a variable obeys a mathematical relation that can be linearized. This means finding new variables such that the curve in a graph of our data is expected to be a line instead of some other curve. In our vapor pressure example, these variables are found by manipulation of the Clapeyron equation. We assume that the volume of the liquid is negligible compared to that of the gas, and that the gas is ideal:

$$
\Delta V _ {m} = V _ {m} (g a s) - V _ {m} (l i q u i d) \approx V _ {m} (g a s) \approx \frac {R T}{P}\tag{11.42}
$$

We also assume that $\Delta H_{m}$ is equal to a constant. After separation of variables and integration, we obtain the Clausius–Clapeyron equation

$$
\ln (P) = - \frac {\Delta H _ {m}}{R T} + C,\tag{11.43}
$$

where $C$ is a constant of integration.

EXERCISE 11.9 ▶ Multiply both sides of Eq. (11.30) by dT, separate the variables do an indefinite integration to obtain Eq. (11.43), using the stated assumptions.

Equation (11.43) represents a linear function if we use 1/T as the independent variable and $\ln(P)$ as the dependent variable. Figure 11.2 is a graph of the same data as Fig. 11.1, using these variables.

A straight line passing nearly through the points has been drawn in the figure. The expected errors in $\ln(P)$ were also plotted. They were obtained by use of Eq.

![[30ac5fda7fe17eb21c758a94e2c0fb182e5d3a945a0f534ef332d5d2da67b1b7.jpg]]  
Figure 11.2 ▶ The natural logarithm of the vapor pressure of ethanol as a function of the reciprocal of the absolute temperature.

![[a1b3b37201bc0e07150950e2541cc205bcf0c9b1f3f58442815d17b3419cf04a.jpg]]  
Figure 11.3 ▶ The lines of maximum and minimum slope in Figure 11.2.

(11.28), with $y = \ln(P)$ .

$$
\varepsilon (\ln (P)) = \varepsilon_ {y} = \left(\left(\frac {d y}{d P}\right) ^ {2} \varepsilon_ {P} ^ {2}\right) ^ {1 / 2} = \left| \left(\frac {d y}{d P}\right) \varepsilon_ {P} \right| = \frac {1}{P} \varepsilon_ {P}.\tag{11.44}
$$

EXERCISE 11.10 ▶ Calculate the expected error in $\ln(P)$ for a few data points in Table 11.3, using Eq. (11.44).

EXAMPLE 11.9 Find the enthalpy change of vaporization of ethanol from the graph in Fig. 11.2.

SOLUTION ▶ The necessary right triangle has been drawn in Fig. 11.2 and the coordinates of the vertices are given in the figure. If m is the slope, then

$$
\begin{array}{r c l} \Delta H _ {m} & = & - m R = - (- 4.87 \times 10 ^ {3} \mathrm{K}) (8.3145 \mathrm{JK} ^ {- 1} \mathrm{mol} ^ {- 1}) \\ & = & 40.5 \times 10 ^ {3} \mathrm{Jmol} ^ {- 1} = 40.5 \mathrm{kJmol} ^ {- 1}. \end{array}
$$

EXERCISE 11.11 ▶ Construct the graph of the data in Exercise 11.8. Do this by solving Eq. (11.41) to obtain

$$
\ln (c) = - k t + K.\tag{11.45}
$$

Find the value of the rate constant k.

## 11.5 Numerical Curve Fitting: The Method of Least Squares (Regression)

Graphical techniques have lost favor because of the availability of computers and software packages that make numerical procedures much less tedious than graphical techniques. Furthermore, numerical procedures are less subjective and are usually more accurate than graphical procedures. The method of least squares is a numerical procedure for finding a continuous function to represent a set of data points. Our data points are represented by ordered pairs of numbers, $(x_{1}, y_{1}), (x_{2}, y_{2}), (x_{3}, y_{3})$ , etc. where x is the independent variable. We assume that there is some function

$$
y = y (x)\tag{11.46}
$$

governing the behavior of y as a function of x, and that we know a family of functions to which the correct function belongs,

$$
y = f (x, a _ {1}, a _ {2}, \dots , a _ {p}),\tag{11.47}
$$

where the $a$ 's are parameters that have different values for different members of the family. We want to find the values of the parameters for the member of the assumed family that most nearly fits the data points. For example, a family of linear functions is

$$
y = m x + b,\tag{11.48}
$$

where the slope m and the intercept b are the parameters that have different values for different members of the family.

We define the residual for the ith data point as the difference between the measured value and the value of the function at that point:

$$
r _ {i} = y _ {i} - f (x _ {i}, a _ {1}, a _ {2}, \dots , a _ {p}).\tag{11.49}
$$

When a function has been chosen that fits the points well, these residuals will collectively be small. Under certain conditions, it has been shown by mathematicians that the best fit is obtained when the sum of the squares of the residuals is minimized. The method of finding the best curve to fit a set of data points by minimizing this sum is called the method of least squares. The method is also called regression. It was first applied by Sir Francis Galton (1822–1911), a famous geneticist who studied the sizes of plants and their offspring, and also the heights of fathers and sons. He found in both these cases that there was a correlation between the trait in the second generation and the earlier generation. However, he also found that the offspring tended to be closer to the mean of the trait than the earlier generation. He called this tendency “regression toward mediocrity” and it has also been called “regression toward the mean.” The name “regression” has stuck to the method.

We seek the minimum of R, the sum of the squares of the residuals,

$$
R = \sum_ {i = 1} ^ {N} \left[ y _ {i} - f (x _ {i}, a, a _ {2}, \dots , a _ {p}) \right] ^ {2},\tag{11.50}
$$

where $N$ is the number of data points. This minimum occurs where all of the partial derivatives of $R$ with respect to $a_1, a_2, \ldots, a_p$ vanish:

$$
\frac {\partial R}{\partial a _ {i}} = 0 \quad (i = 1, 2, \dots , p).\tag{11.51}
$$

This is a set of simultaneous equations, one for each parameter. For some families of functions, these simultaneous equations are nonlinear equations and are solved by successive approximations. $^{12}$ For linear functions or polynomial functions, the equations are linear equations, and we can solve them by the methods of Chapter 10.

In the method of linear least squares or linear regression, we find the linear function that best fits our points. If we have a nonlinear function, we might have a theory that produces a linear dependence (linearize) by changing variables. The family of linear functions is given by

$$
y = m x + b.\tag{11.52}
$$

We seek that value of the slope m and that value of the intercept b that give us the best fit to our data points (possibly after linearization). For the linear function of Eq. (11.52), the sum of the squares of the residuals is

$$
R = \sum_ {i = 1} ^ {N} (y _ {i} - m x _ {i} - b) ^ {2}.\tag{11.53}
$$

The simultaneous equations are

$$
\frac {\partial R}{\partial m} = 2 \sum_ {i = 1} ^ {N} (y _ {i} - m x _ {i} - b) (- x _ {i}) = 0\tag{11.54a}
$$

$$
{\frac {\partial R}{\partial b}} = 2 \sum_ {i = 1} ^ {N} (y _ {i} - m x _ {i} - b) (- 1) = 0.\tag{11.54b}
$$

This is a set of linear inhomogeneous simultaneous equations in m and b. We write them in the form

$$
S _ {x ^ {2}} m + S _ {x} b = S _ {x y}\tag{11.55a}
$$

$$
S _ {x} m + N b = S _ {y},\tag{11.55b}
$$

where

$$
S _ {x} = \sum_ {i = 1} ^ {N} x _ {i}\tag{11.56a}
$$

$$
S _ {y} = \sum_ {i = 1} ^ {N} y _ {i}\tag{11.56b}
$$

$$
S _ {x y} = \sum_ {i = 1} ^ {N} x _ {i} y _ {i}\tag{11.56c}
$$

$$
S _ {x ^ {2}} = \sum_ {i = 1} ^ {N} x _ {i} ^ {2}.\tag{11.56d}
$$

These linear inhomogeneous equations can be solved by any of the techniques of Chapter 10. Cramer's rule is the easiest method in this case. From Eqs. (10.4) and

(10.5),

$$
\boxed {m = \frac {1}{D} (N S _ {x y} - S _ {x} S _ {y})}\tag{11.57}
$$

$$
\boxed {b = \frac {1}{D} (S _ {x ^ {2}} S _ {y} - S _ {x} S _ {x y}),}\tag{11.58}
$$

where

$$
\boxed {D = N S _ {x ^ {2}} - S _ {x} ^ {2}}\tag{11.59}
$$

These are our working equations. The calculation of the four sums can be carried out by hand if there are not too many data points, but many handheld calculators carry out the calculation automatically, and we will describe how to do the calculation with the Excel spreadsheet later in this section.

EXAMPLE 11.10 Calculate the slope m and the intercept b for the least-squares line for the data in Table 11.3, using $\ln(P)$ as the dependent variable and 1/T as the independent variable. Calculate the enthalpy change of vaporization from the slope.

SOLUTION ▶ When the numerical work is done, the results are

$$
\begin{array}{r c l} {m} & {=} & {- 4854 \mathrm{K}} \\ {b} & {=} & {20.28} \\ {\Delta H _ {m}} & {=} & {- m R = (- 4854 \mathrm{K}) (8.3145 \mathrm{J} \mathrm{K} ^ {- 1} \mathrm{mol} ^ {- 1})} \\ & {=} & {40.36 \times 10 ^ {3} \mathrm{J} \mathrm{mol} ^ {- 1}.} \end{array}
$$

This value compares with the accepted value of $40.3 \times 10^{3}$ J mol $^{-1}$ , and is somewhat closer to the accepted value than the result obtained from the derivative dP/dT in an earlier example.

EXERCISE 11.12 ▶ The following data give the vapor pressure of water at various temperatures. $^{a}$

(a) Find the least-squares line for the data, using $\ln(P)$ for the dependent variable and 1/T for the independent variable. Calculate the four sums by hand. Find the molar enthalpy change of vaporization.

<table><tr><td>Temperature/°C</td><td>Vapor pressure/torr</td></tr><tr><td>0</td><td>4.579</td></tr><tr><td>5</td><td>6.543</td></tr><tr><td>10</td><td>9.209</td></tr><tr><td>15</td><td>12.788</td></tr><tr><td>20</td><td>17.535</td></tr><tr><td>25</td><td>23.756</td></tr></table>

(b) Verify your results using Excel.

![[2b76cbcc1e7a514880a7fdd106a66f2546b17466550977624ac316355b62471d.jpg]]

In some problems, it is not certain in advance what variables should be used for a linear least-squares fit. In the vapor pressure case, we had the Clausius-Clapeyron equation, Eq. (11.43), which indicated that $\ln(P)$ and 1/T were the variables that should produce a linear relationship. In the analysis of chemical rate data, it may be necessary to try two or more hypotheses to determine which gives the best fit. In a reaction involving one reactant, the concentration c of the reactant is given by Eq.(11.45) if there is no back reaction and if the reaction is a first-order reaction. If there is no back reaction and the reaction is a second-order reaction, the concentration of the reactant is given by

$$
\frac {1}{c} = k t + C,\tag{11.60}
$$

where k is the rate constant and C is a constant of integration. If there is no back reaction and the reaction is third order, the concentration c of the reactant is given by

$$
\frac {1}{2 c ^ {2}} = k t + C.\tag{11.61}
$$

If the order of a reaction is not known, it is possible to determine the order by trying different linear least-squares fits and finding which one most nearly fits the data. One way to see whether a given hypothesis produces a linear fit is to examine the residuals. Once the least-squares line has been found, m and b are known. The residuals can be calculated from

$$
r _ {i} = y _ {i} - m x _ {i} - b.\tag{11.62}
$$

If a given dependent variable and independent variable produce a linear fit, the points will deviate from the line only because of experimental error, and the residuals will be either positive or negative without any pattern. However, if there is a general curvature to the data points in a graph, the residuals will have the same sign near the ends of the graph and the other sign in the middle. This indicates that a different pair of variables should be tried or a nonlinear least-squares fit attempted.

EXAMPLE 11.11 The following is a fictitious set of data for the concentration of the reactant in a chemical reaction with one reactant. Determine whether the reaction is first, second, or third order. Find the rate constant and the initial concentration.

SOLUTION ▶ We first test for first order by attempting a linear fit using $\ln(c)$ as the dependent variable and t as the independent variable. The result is

$$
\begin{array}{r c l} {m} & {=} & {- 0.03504 \min ^ {- 1} = - k} \\ {b} & {=} & {- 0.1592 = \ln [ c (0) ]} \\ {c (0)} & {=} & {0.853 \mathrm{mol} 1 ^ {- 1}.} \end{array}
$$

The following set of residuals was obtained:

$$
\begin{array}{l l} r _ {1} = - 0.00109 & r _ {6} = 0.00634 \\ r _ {2} = 0.00207 & r _ {7} = - 0.00480 \\ r _ {3} = - 0.00639 & r _ {8} = 0.01891 \\ r _ {4} = - 0.00994 & r _ {9} = - 0.01859. \\ r _ {5} = 0.01348 \end{array}
$$

This is a good fit, with no pattern of general curvature shown in the residuals.

We test the hypothesis that the reaction is second order by attempting a linear fit using 1/c as the dependent variable and t as the independent variable. The result is

$$
\begin{array}{r c l} {m} & {=} & {0.1052 \mathrm{l} \mathrm{mol} ^ {- 1} = k} \\ {b} & {=} & {0.4846 \mathrm{l} \mathrm{mol} ^ {- 1} = \frac {1}{c (0)}} \\ {c (0)} & {=} & {2.064 \mathrm{mol} \mathrm{l} ^ {- 1}.} \end{array}
$$

The following set of residuals was obtained:

$$
\begin{array}{l l} r _ {1} = 0.3882 & r _ {6} = - 0.3062 \\ r _ {2} = 0.1249 & r _ {7} = - 0.1492 \\ r _ {3} = - 0.0660 & r _ {8} = - 0.0182 \\ r _ {4} = - 0.2012 & r _ {9} = 0.5634. \\ r _ {5} = - 0.3359 \end{array}
$$

This is not such a satisfactory fit as in part a, since the residuals show a general curvature, beginning with positive values, becoming negative, and then becoming positive again.

We now test the hypothesis that the reaction is third order by attempting a linear fit using $1 / (2c^2)$ as the dependent variable and $t$ as the independent variable. The results are

$$
\begin{array}{r c l} {m} & {=} & {0.3546 \mathrm{l} ^ {2} \mathrm{mol} ^ {- 2} \mathrm{min} ^ {- 1} = k} \\ {b} & {=} & {- 3.054 \mathrm{l} ^ {2} \mathrm{mol} ^ {- 2}.} \end{array}
$$

This is obviously a bad fit, since the intercept b should not be negative. The residuals are

$$
\begin{array}{l l} r _ {1} = 2.2589 & r _ {6} = - 2.0285 \\ r _ {2} = 0.8876 & r _ {5} = - 1.2927 \\ r _ {3} = - 0.2631 & r _ {8} = - 0.2121 \\ r _ {4} = - 1.1901 & r _ {9} = 3.8031. \\ r _ {5} = - 1.9531 \end{array}
$$

Again, there is considerable curvature. The reaction is apparently first order, with the rate constant and initial concentration given in part a of the solution.

In addition to inspecting the residuals, we can calculate the correlation coefficient, which gives information about the closeness of a least-squares fit. For linear least squares, the correlation coefficient is defined by

$$
\boxed {r = \frac {N S _ {x y} - S _ {x} S _ {y}}{[ (N S _ {x ^ {2}} - S _ {x} ^ {2}) (N S _ {y ^ {2}} - S _ {y} ^ {2}) ] ^ {1 / 2}},}\tag{11.63}
$$

where $S_x$ , $S_y$ , $S_{xy}$ , and $S_{x^2}$ are defined in Eq. (11.55a) and where

$$
S _ {y ^ {2}} = \sum_ {i = 1} ^ {N} y _ {i} ^ {2}.\tag{11.64}
$$

If the data points lie exactly on the least-squares line, the correlation coefficient will be equal to 1 if the slope is positive or to -1 if the slope is negative. If the data points are scattered randomly about the graph so that no least-squares line can be found, the correlation coefficient will equal zero. The magnitude of the correlation coefficient will be larger for a close fit than for a poor fit. In a fairly close fit, its magnitude might equal 0.99. Some software packages give the square of the correlation coefficient rather than the correlation coefficient itself.

EXAMPLE 11.12 Calculate the correlation coefficients for the three linear fits in the previous example.

```txt
SOLUTION ▶ Use of Eq. (11.63) gives the results:
(a) For the first-order fit, r = -0.9997.
(b) For the second-order fit, r = 0.9779.
(c) For the third-order fit, r = 0.9257.
Again, the first-order fit is the best.
```

EXERCISE 11.13 ▶ Do three linear least-squares fits on the data of Exercise 11.8. Calculate the correlation coefficients for the three fits and show that the reaction is first order. If you wish, you can use a spreadsheet such as Excel, which will plot the data and carry out the least-squares fit for you. The procedure is described later in this section.

The correlation coefficient is related to a quantity called the covariance, defined by $^{13}$

$$
s _ {x, y} = \frac {1}{N - 1} \sum_ {i - 1} ^ {N} (x _ {i} - \bar {x}) (y _ {i} - \bar {y}),\tag{11.65}
$$

where $\bar{x}$ is the average of the $x$ 's,

$$
\bar {x} = \frac {1}{N} S _ {x},\tag{11.66}
$$

and where $y$ is the average of the $y$ 's,

$$
\bar {y} = \frac {1}{N} S _ {y}.\tag{11.67}
$$

The covariance has the same general behavior as the correlation coefficient. If large values of x tend to occur with small values of y, the covariance will be negative, and if large values of x tend to occur with large values of y, the covariance will be positive. If there is no relationship between x and y, the covariance will equal zero.

## Error Propagation in Linear Least Squares

We discuss two cases: (1) the expected error in each value of the dependent variable is known, and (2) the expected error in these values is not known. In both cases, we assume that the errors in the values of the independent variable x are negligible.

![[4b16ff61b87d9e05b108a19f18f4bf67250054cc0415a349976be95a5c59d9f4.jpg]]

Case 1. Let the expected error in the value of $y_{i}$ be denoted by $\varepsilon_{i}$ . Equations for the slope and the intercept of the least-squares line are given in Eqs. (11.57) and (11.58). The $y$ 's can be considered to be independent variables, so we can apply Eq. (11.28). The expected error in the slope is given by

$$
\varepsilon_ {m} = \left[ \sum_ {i = 1} ^ {N} \left(\frac {\partial m}{\partial y _ {i}}\right) ^ {2} \varepsilon_ {i} ^ {2} \right] ^ {1 / 2} = \left[ \frac {1}{D ^ {2}} \sum_ {i = 1} ^ {N} (N x _ {i} - S _ {x}) ^ {2} \varepsilon_ {i} ^ {2} \right] ^ {1 / 2},\tag{11.68}
$$

where $D$ and $S_x$ are given in Eqs. (11.59) and (11.56d). In the case that all of the expected errors in the $y$ 's are equal to each other,

$$
\boxed {\varepsilon_ {m} = \left(\frac {N}{D}\right) ^ {1 / 2} \varepsilon_ {y},}\tag{11.69}
$$

where $\varepsilon_{y}$ is the value of all the $\varepsilon_{i}$ 's.

The expected error in the intercept is

$$
\varepsilon_ {b} = \left[ \sum_ {i = 1} ^ {N} \left(\frac {\partial b}{\partial y _ {i}}\right) ^ {2} \varepsilon_ {i} ^ {2} \right] ^ {1 / 2} = \left[ \frac {1}{D ^ {2}} \sum_ {i = 1} ^ {N} (S _ {x ^ {2}} - S _ {x} x _ {i}) ^ {2} \varepsilon_ {i} ^ {2} \right] ^ {1 / 2}.\tag{11.70}
$$

For the case that all of the $\varepsilon_{i}$ 's are assumed to be equal,

$$
\boxed {\varepsilon_ {b} = \left(\frac {S _ {x ^ {2}}}{D}\right) ^ {1 / 2} \varepsilon_ {y},}\tag{11.71}
$$

where $S_{x^2}$ is given in Eq. (11.56d).

EXERCISE 11.14 ▶

Verify Eqs. (11.69) and (11.71).

EXAMPLE 11.13 Assume instead of the given expected errors that the expected error in the logarithm of each vapor pressure in Table 11.3 is equal to 0.040. Find the expected error in the least-squares slope and in the enthalpy change of vaporization.

SOLUTION ▶ From the data,

$$
D = 1.327 \times 10 ^ {- 6} \mathrm{K} ^ {- 2}
$$

so that

$$
\begin{array}{r l} \varepsilon_ {m} & = \left(\frac {9}{1 .327 \times 10 ^ {- 6} \mathrm{K} ^ {- 2}}\right) ^ {1 / 2} (0.040) = 104 \mathrm{K} \\ \varepsilon_ {\triangle H _ {m}} & = R \varepsilon_ {m} = 870 \mathrm{Jmol} ^ {- 1} = 0.87 \mathrm{kJmol} ^ {- 1}. \end{array}
$$

EXERCISE 11.15 ▶ Assume that the expected error in the logarithm of each concentration in Example 11.10 is equal to 0.010. Find the expected error in the rate constant, assuming the reaction to be first order.

Case 2. If we do not have information about the expected errors in the dependent variable, we assume that the residuals are a sample from the population of actual experimental errors. This is a reasonable assumption if systematic errors can be ignored. The variance of the N residuals is given by

$$
s _ {r} ^ {2} = \frac {1}{N - 2} \sum_ {i = 1} ^ {N} r _ {i} ^ {2}.\tag{11.72}
$$

The standard deviation of the residuals is the square root of the variance:

$$
s _ {r} = \left(\frac {1}{N - 2} \sum_ {i = 1} ^ {N} r _ {i} ^ {2}\right) ^ {1 / 2}.\tag{11.73}
$$

This differs from Eq.(11.8) in that a factor of N - 2 occurs in the denominator instead of N - 1. The number of degrees of freedom is N - 2 because we have calculated two quantities, a least-squares slope and a least-squares intercept from the set of numbers, “consuming” two of the degrees of freedom. The mean of the residuals does not enter in the formula, because the mean of the residuals in a least-squares fit always vanishes.

EXERCISE 11.16 ▶ Sum the residuals in Example 11.11 and show that this sum vanishes in each of the three least-square fits.

Equation (11.73) provides an estimate of the standard deviation of the population of experimental errors. We assume that the errors in y are distributed according to the Student t distribution, so the expected error in y at the 95% confidence level is given by

$$
\boxed {\varepsilon_ {y} = t (\nu , 0.05) s _ {r},}\tag{11.74}
$$

where $t(v, 0.05)$ is the Student t factor for $\nu = N - 2$ ; the number of degrees of freedom for N data points after the slope and the intercept have been calculated. If there were a very large number of data points, the Student t distribution would approach the Gaussian distribution, and this factor would approach 1.96.

We can now write expressions similar to Eqs. (11.69) and (11.70) for the expected errors at the 95% confidence level:

$$
\varepsilon_ {m} = \left(\frac {N}{D}\right) ^ {1 / 2} t (\nu , 0.05) s _ {r}\tag{11.75}
$$

and

$$
\varepsilon_ {b} = \left(\frac {1}{D} \sum_ {i = 1} ^ {N} x _ {i} ^ {2}\right) ^ {1 / 2} t (\nu , 0.05) s _ {r}.\tag{11.76}
$$

The standard deviations of the slope and intercept are given by similar formulas without the Student t factor:

$$
s _ {m} = \left(\frac {1}{D} \sum_ {i = 1} ^ {N} x _ {i} ^ {2}\right) ^ {1 / 2} s _ {r}\tag{11.77}
$$

$$
s _ {b} = \left(\frac {N}{D}\right) ^ {1 / 2} s _ {r}.\tag{11.78}
$$

The slope and the intercept of a least-squares line are not independent of each other, since they are derived from the same set of data, and their covariance is given by $^{14}$

$$
C o v (m, b) = s _ {m, b} = \frac {- s _ {r} ^ {2} S _ {x}}{D}.\tag{11.79}
$$

EXAMPLE 11.14 Calculate the residuals for the linear least-squares fit of Example 11.10. Find their standard deviation and the probable error in the slope and in the enthalpy change of vaporization, using the standard deviation of the residuals.

SOLUTION ▶ Numbering the data points from the $25^{\circ}$ C point (number 1) to the $65^{\circ}$ C point (number 9), we find the residuals:

$$
\begin{array}{l l} r _ {1} = 0.0208 & r _ {6} = - 0.0116 \\ r _ {2} = - 0.0228 & r _ {7} = - 0.0027 \\ r _ {3} = 0.0100 & r _ {8} = 0.0054 \\ r _ {4} = - 0.0162 & r _ {9} = 0.0059. \\ r _ {5} = 0.0113 \end{array}
$$

The standard deviation of the residuals is found to be

$$
s _ {r} = 0.0154.
$$

Using the value of D from the previous example, the uncertainty in the slope is

$$
\varepsilon_ {m} = \left(\frac {9}{1 .327 \times 10 ^ {- 6} \mathrm{K} ^ {- 2}}\right) ^ {1 / 2} (2.365) (0.0154) = 94.9 \mathrm{K},
$$

where we have used the value of the Student's $t$ factor for seven degrees of freedom from Table 11.1. The uncertainty in the enthalpy change of vaporization is

$$
\varepsilon_ {\triangle H _ {m}} = R \varepsilon_ {m} = (8.3145 \mathrm{JK} ^ {- 1} \mathrm{mol} ^ {- 1}) (96.9 \mathrm{K}) = 789 \mathrm{Jmol} ^ {- 1}.
$$

EXERCISE 11.17 ▶ Assuming that the reaction in Exercise 11.12 is first order, find the expected error in the rate constant, using the residuals.

## Expected Errors in the Dependent Variable

If the linear least-squares method is used to find the line that best represents a set of data, this line can be used to predict a value for the dependent variable corresponding to any given value of the independent variable. We now consider the probable error in such a prediction. $^{15}$ Since the dependent variable y is a function of the slope m and the intercept b, we might try to apply Eq. (11.28):

$$
\varepsilon_ {y} = \left(\left(\frac {\partial y}{\partial m}\right) ^ {2} \varepsilon_ {m} ^ {2} + \left(\frac {\partial y}{\partial b}\right) ^ {2} \varepsilon_ {b} ^ {2}\right) ^ {1 / 2} \quad (\text { NOT   APPLICABLE }).\tag{11.80}
$$

However, this equation is incorrect, because m and b have been derived from the same set of data and are not independent of each other, as was assumed in obtaining Eq. (11.28).

The correct equation is obtained by including the covariance of m and b. We consider the standard deviation of y,

$$
s _ {y} ^ {2} = \left(\frac {\partial y}{\partial m}\right) ^ {2} s _ {m} ^ {2} + \left(\frac {\partial y}{\partial b}\right) ^ {2} s _ {b} ^ {2} + 2 \left(\frac {\partial y}{\partial m}\right) \left(\frac {\partial y}{\partial b}\right) s _ {m, b}\tag{11.81}
$$

$$
= x ^ {2} s _ {m} ^ {2} + s _ {b} ^ {2} + 2 x s _ {m, b},\tag{11.82}
$$

where $s_{m}$ is the standard deviation of m, $s_{b}$ is the standard deviation of b, and $s_{m,b}$ is the covariance of m and b. In this equation, x stands for the value of x for which we want the value of y. The expected error in y at the 95% confidence level is

$$
\varepsilon_ {y} = t (N - 2, 0.05) s _ {y}.\tag{11.83}
$$

If you want to determine a value of x for a given value of y, a similar analysis can be carried out, considering that for a given value of y, x is a function of m and b.

EXERCISE 11.18 ▶

(a) From the least-squares fit of Example 11.10, find the predicted value of the vapor pressure of ethanol at 70.0°C. Find the expected error in the natural logarithm of the vapor pressure. Compare the values of the three terms in Eq. (11.81). Find the expected error in the predicted value of the vapor pressure.

(b) From the least-squares fit of Example 11.10, find the predicted temperature at which the vapor pressure of ethanol is equal to 350.0 torr. Find the expected error in the reciprocal of the absolute temperature. Compare the values of the three terms analogous to those in Eq. (11.81).


## Carrying Out Least Squares Fits with Excel

The following instructions are written for Excel 2003 for Windows. If you have a later version or an earlier version of this spreadsheet, there might be small differences in the procedure. There are also small differences in Excel for the Macintosh computer. The Excel spreadsheet will carry out least squares fits in two different ways. You can carry out linear least squares in a worksheet, or you can carry out linear and various nonlinear least squares procedures on a graph. The advantage of the worksheet procedure is that expected errors in the slope and intercept of the linear fit are provided by the software. The disadvantage of the worksheet procedure is that nonlinear least squares fits apparently cannot be carried out.

## Doing Linear Least Squares Fits in a Worksheet

The first step in carrying out linear least squares fits in a worksheet after opening the worksheet is to enter the data points into columns of the worksheet. The values of the variable that will go on the x axis go into one column and the corresponding values of the variable that will go on the y axis go into another column. This column does not have to be immediately to the right of the first column as it does in making a graph. If necessary, use formulas to transform your original data into variables that will give a linear fit. Go to the Tools menu and select Data Analysis. If Data Analysis does not show up as one of the items on the menu, select Add-Ins. A list of tools should appear, and you should check Analysis ToolPak and click on OK. After you select Data Analysis, a list of techniques appears. Select Regression and click on OK. A window appears with several blanks. In the Input Y Range blank, type in the first and last cell addresses of the dependent variable, separated by a colon (:). If the values are in the first ten rows of column B, you type B1:B10. The software will change this to \$B\$1:\$B\$10 or you can type in the absolute addresses (with \$ signs). In the Input X Range blank, type in the cell addresses for the independent variable, such as A1:A10. In the Confidence Level blank, make sure that 95% is chosen. Choose 95% if it is not already chosen. You will probably want to see a list of the residuals, so check the Residuals box. If you want to see a plot of the residuals, check the Residuals Plot box. You can specify where you want to put the output. The output occupies several columns and several rows, so it is probably best to check the New Worksheet Ply box. Otherwise, specify a location on your worksheet for the upper left corner of the area where you want the output. Click on OK.

When you click on OK, the computer carries out the procedure and puts the output on the screen. A number of statistical parameters are exhibited. You can find the value of correlation coefficient and its square (in the R Square cell). At the bottom of the output are the parameters of the fit. There are columns labeled Coefficient, Standard Error, t Stat, P-Value, Lower 95%, and Upper 95%. There are two rows for the intercept and slope. The intercept row is labeled Intercept, and the slope row is labeled X Variable. The Coefficient column contains the parameter. The Standard Error column contains the error based on the standard deviation (about 68% confidence). The Lower 95% column contains the parameter decremented by the expected error at the 95% confidence level, and the Upper 95% column contains the parameter incremented by the expected error. To obtain the expected error, you will have to do a subtraction. You should look at the list of residuals to see it there is a systematic curvature in the data, which shows up with residuals having one sign at the ends of the fit and the other sign in the middle.

## Least Squares Fits on a Graph with Excel

With Excel, it appears that only linear least squares fits can be carried out on a worksheet, but various functions can be fit to your data on a graph. Unfortunately, residuals and expected errors in the parameters are not provided when you work from the graph. The correlation coefficient is provided. To begin a fit, you make the graph in the usual way, using the X-Y Scatter option. Do not choose the option that places a curve in the graph. When you finish the graph, go to the Chart menu and select Add Trendline. A window appears with two tab-like areas at the top. The Type tab should already be selected. You can choose from linear, polynomial, logarithmic, power, exponential, and moving average fits. If you choose polynomial, you must specify the degree (highest power) in the polynomial. After you select the type of fit, click on the Options tab. Click on the “Display Eq. on Chart” area and on the “Display R-Squared Value on Chart” area. If you want the displayed curve to extend past your first and last data points, click on Forecast and specify how far on the x axis your want the curve to extend in the forward and back directions. Click on OK and the computer carries out the curve fit. The least-squares curve, the equation of the fitting function and the square of the correlation coefficient appear on the graph. If you want more digits for the equation parameters or want scientific notation, double-click on the equation. A window appears. Click on Number. A window appears in which you can choose whether you want scientific notation or ordinary notation (click on “number”) and can specify the number of digits after the decimal point. Click on OK and look at your results.

## Some Warnings about Least-Squares Procedures

It is a poor idea to rely blindly on a numerical method. You should always determine whether your results are reasonable. It is possible to spoil your results by entering one number incorrectly or by failing to recognize a bad data point. Remember the first maxim of computing: "Garbage in, garbage out." You should always look at your correlation coefficient. A low magnitude usually indicates a problem. Another way to make sure that a linear least-squares procedure has given you a good result is to inspect the graph. If you carry out the fit on an Excel worksheet, you should also make the graph. If you have an incorrectly entered data point you will probably be able to tell by looking at the graph. If the data points show a general curvature, you will probably be able to tell that as well from the graph.

A final warning is that in making a change in variables in order to fit a set of data to a straight line rather than to some other function, you are changing the relative importance, or weight, of the various data points. $^{16}$ In analyzing reaction rate data, fitting $\ln(c)$ to a straight line $\ln(c) = -kt + C$ will not necessarily give the same value of k as will fitting c to the function $c = e^{C}e^{-kt}$ . We now discuss a way to compensate for this and also to compensate for errors of different sizes in different data points.

## Weighting Factors in Linear Least Squares

Consider the case that we want to make a linear least-squares fit to a set of data in which the probable errors in the values of the dependent variable are not all of the same size. In this case, instead of minimizing the sum of the squares of the residuals, it has been shown that one should minimize the sum of the squares of the residuals divided by the square of the standard deviation of the population of errors from which the residual is drawn. If $\sigma_{i}$ is the standard deviation of this population for data point number i, we should minimize $^{17}$

$$
R ^ {\prime} = \sum_ {i = 1} ^ {N} \frac {r _ {i} ^ {2}}{\sigma_ {i} ^ {2}} = \sum_ {i = 1} ^ {N} \frac {1}{\sigma_ {i} ^ {2}} (y _ {i} - m x _ {i} - b) ^ {2}.\tag{11.84}
$$

The factors $1/\sigma_{i}^{2}$ in the sum are called weighting factors. The effect of this weighting is to give a greater importance (greater weight) to those points that have smaller expected errors. $^{18}$ The standard deviations are generally unknown, so if we have expected error values for the different data points, we use the expected error $\varepsilon_{i}$ in place of the standard deviation $\sigma_{i}$ :

$$
R ^ {\prime} = \sum_ {i = 1} ^ {N} \frac {1}{\varepsilon_ {i} ^ {2}} (y _ {i} - m x _ {i} - b) ^ {2}\tag{11.85}
$$

We can now minimize $R'$ . The equations are very similar to Eqs. (11.54a)-(11.59), except that each sum includes the weighting factors. The results for the slope and intercept are

$$
m = \frac {1}{D ^ {\prime}} (S _ {1} ^ {\prime} S _ {x y} ^ {\prime} - S _ {x} ^ {\prime} S _ {y} ^ {\prime})\tag{11.86}
$$

$$
b = \frac {1}{D ^ {\prime}} (S _ {x ^ {2}} ^ {\prime} S _ {y} ^ {\prime} - S _ {x} ^ {\prime} S _ {x y} ^ {\prime}),\tag{11.87}
$$

where

$$
D ^ {\prime} = S _ {1} ^ {\prime} S _ {x ^ {2}} ^ {\prime} - S _ {x} ^ {\prime 2},\tag{11.88}
$$

and where

$$
S _ {1} ^ {\prime} = \sum_ {i = 1} ^ {N} \frac {1}{\sigma_ {i} ^ {2}}\tag{11.89}
$$

$$
S _ {x} ^ {\prime} = \sum_ {i = 1} ^ {N} \frac {x _ {i}}{\sigma_ {i} ^ {2}}\tag{11.90}
$$

$$
S _ {y} ^ {\prime} = \sum_ {i = 1} ^ {N} \frac {y _ {i}}{\sigma_ {i} ^ {2}}\tag{11.91}
$$

$$
S _ {x y} ^ {\prime} = \sum_ {i = 1} ^ {N} \frac {x _ {i} y _ {i}}{\sigma_ {i} ^ {2}}\tag{11.92}
$$

$$
S _ {x ^ {2}} ^ {\prime} = \sum_ {i = 1} ^ {N} \frac {x _ {i} ^ {2}}{\sigma_ {i} ^ {2}}.\tag{11.93}
$$

The standard deviations in these formulas could be replaced by the expected errors.

EXAMPLE 11.15 Find the least-squares line for the data of Table 11.3, assuming that the weighting factors are inversely proportional to the squares of the expected errors in the logarithms.

SOLUTION ▶ The expected errors in $\ln(P)$ were calculated by Eq. (11.44) from the expected errors in the pressures given in the table. These were substituted into Eqs. (11.86)–(11.88) in place of the $\sigma_{i}$ 's. The results were

$$
\begin{array}{r l} {m} & {= - 4872 \mathrm{K}} \\ {b} & {= 20.34} \end{array}
$$

These figures differ slightly from those of Example 11.9, and since the expected errors in the logarithms are not all equal to each other, these values are likely more nearly correct. The slope gives a value of the enthalpy change of vaporization

$$
\begin{array}{r c l} \Delta H _ {m} & = & - R m = - (8.3145 \mathrm{JK} ^ {- 1} \mathrm{mol} ^ {- 1}) (- 4872 \mathrm{Jmol} ^ {- 1}) \\ & = & 40501 \mathrm{Jmol} ^ {- 1} = 40.51 \mathrm{kJmol} ^ {- 1}. \end{array}\tag{11.94}
$$

In the following example, we see what an inaccurate point can do if the unweighted least-squares procedure is used.

EXAMPLE 11.16 Change the data set of Table 11.3 by adding a value of the vapor pressure at 70 °C of 421 torr ±40 torr. Find the least-squares line using both the unweighted and weighted procedures.

SOLUTION ▶ After the point was added, the unweighted procedure was carried out as in Example 11.10, and the weighted procedure was carried out as in Example 11.15. The results were: For the unweighted procedure,

$$
\begin{array}{r c l} m & = & \text { slope } = - 4752   \text { K } \\ b & = & \text { intercept } = 19.95. \end{array}
$$

For the weighted procedure,

$$
\begin{array}{r c l} m & = & \text { slope } = - 4855   \text { K } \\ b & = & \text { intercept } = 20.28. \end{array}
$$

The data point of low accuracy has done more damage in the unweighted procedure than in the procedure with weighting factors.

If the values of the original dependent variable have equal expected errors, an unweighted least-squares fit is appropriate if we use that variable in our procedure. However, if we take a function of the original variable in order to use a linear fit, then the original expected errors, which are all equal, will not generally produce equal errors in the new variable, and the weighted least-squares procedure is preferred.

This discussion suggests a possible procedure to use if you carry out a least squares fit and a few points lie a long way from the line: Carry out the fit a second time using weighting factors, utilizing the residuals from the first fit in place of the $\sigma_{i}$ 's of Eq. (11.88). This procedure should give a better fit than use of the unweighted procedure alone. If there is only one data point with a residual that is much larger in magnitude that the others, a reasonable procedure would be to calculate the standard deviation of the residuals after an initial fit and to disregard the data point if its residual is at least as large as the standard deviation of the residuals times 2.7, which correspond to a probability of less than 1% that the data point arose from experimental error.

## Linear Least Squares with Fixed Slope or Intercept

At times it is necessary to do a linear least-squares fit with the constraint that the slope or the intercept must have a specific value. For example, the Bouguer–Beer law states that the absorbance of a solution is proportional to the concentration of the colored substance. In fitting the absorbance of several solutions to their concentrations, one would specify that the intercept of the least-squares line had to be zero.

In the minimization of the sum of the squares of the residuals, one minimizes only with respect to the slope m if the intercept b is fixed. This is the same as given in Eq. (11.54a):

$$
\frac {d R}{d m} = 2 \sum_ {i = 1} ^ {N} (y _ {i} - m x _ {i} - b) (- x _ {i}) = 0.\tag{11.95}
$$

The solution to this is

$$
m = \frac {S _ {x y} - b S _ {x}}{S _ {x ^ {2}}}.\tag{11.96}
$$

If the slope m is required to have a fixed value, we have only one equation, which is the same as Eq. (11.54a).

$$
\frac {d R}{d b} = 2 \sum_ {i = 1} ^ {N} (y _ {i} ^ {\prime} - m x _ {i} - b) (- 1) = 0.\tag{11.97}
$$

The solution to this is

$$
b = \frac {S _ {y} - m S _ {x}}{N}.\tag{11.98}
$$

If the required slope is equal to zero, the resulting intercept is equal to the mean of the y values and can be calculated

$$
b = \frac {S _ {y}}{N} = \bar {y}.\tag{11.99}
$$

The Excel spreadsheet will carry out fits on a graph with the intercept required to have a specific value. After finishing the graph and selecting “Trendline,” click on the “Options” tab, and then click on the “Set intercept” box and specify 0 or another appropriate value for the intercept. You should include the equation for the curve and the square of the correlation coefficient.

EXERCISE 11.19 ▶ Using Excel or by hand calculation carry out a linear least squares fit on the following data, once with the intercept fixed at zero and one without specifying the intercept:

$$
\begin{array}{c c c c c c c} x & 0 & 1 & 2 & 3 & 4 & 5 \\ y & 0.10 & 0.98 & 2.00 & 2.99 & 4.02 & 4.98 \end{array}\tag{11.100}
$$

Compare your slopes and your correlation coefficients for the two fits.

## SUMMARY

We discussed several related techniques in this chapter. The first is the estimation of probable errors in directly measured quantities. We assumed the existence of a population of infinitely many repetitions of the measurement. If several repetitions of the measurement can be made, we considered this set of measurements to be a sample from the population. We took the sample standard deviation to be an unbiased estimate of the population standard deviation and the sample mean to be an estimate of the population mean (which is the correct value if systematic error is absent). The probable error in the mean was determined by a formula of Student.

If a formula is used to calculate values of some variable from measured values of other variables, it is necessary to propagate the errors in the measured quantities through the calculation. We provided a scheme to calculate the expected error in the dependent variable, based on the total differential of the dependent variable.

We also discussed graphical and numerical data reduction procedures. The most important numerical data reduction procedure is the least squares, or regression, method, which finds the best member of a family of functions to represent a set of data. We discussed the propagation of errors through this procedure and presented a version of the procedure in which different data points are given different weights, or importances, in the procedure.

## PROBLEMS

1. Assume that a sample of 10 sheets of paper has been selected randomly from a ream (500 sheets) of paper. Regard the ream as a population, even though it has only a finite number of members. The width and length of each sheet of the sample were measured, with the following results:

<table><tr><td>Sheet number</td><td>Width/in</td><td>Length/in</td></tr><tr><td>1</td><td>8.50</td><td>11.03</td></tr><tr><td>2</td><td>8.48</td><td>10.99</td></tr><tr><td>3</td><td>8.51</td><td>10.98</td></tr><tr><td>4</td><td>8.49</td><td>11.00</td></tr><tr><td>5</td><td>8.50</td><td>11.01</td></tr><tr><td>6</td><td>8.48</td><td>11.02</td></tr><tr><td>7</td><td>8.52</td><td>10.98</td></tr><tr><td>8</td><td>8.47</td><td>11.04</td></tr><tr><td>9</td><td>8.53</td><td>10.97</td></tr><tr><td>10</td><td>8.51</td><td>11.00</td></tr></table>

a) Calculate the sample mean length and its sample standard deviation, and the sample mean width and its sample standard deviation.

b) Give the expected ream mean length and width, and the expected error in each at the 95% confidence level.

c) Calculate the expected ream mean area from the width and length, and give the 95% confidence interval for the area.

d) Calculate the area of each sheet in the sample. Calculate from these areas the sample mean area and the standard deviation in the area.

e) Give the expected ream mean area and its 95% confidence interval from the results of part d.

f) Compare the results of parts c and e. Would you expect the two results to be identical? Why (or why not)?

2. The intrinsic viscosity $[\eta]$ of a set of solutions of polyvinyl alcohol is defined as the limit $^{19}$

$$
\lim _ {c \rightarrow 0} \left(\frac {1}{c} \ln \left(\frac {\eta}{\eta_ {0}}\right)\right),\tag{11.101}
$$

where c is the concentration of the polymer in grams per deciliter, $\eta$ is the viscosity of a solution of concentration c, and $\eta_{0}$ is the viscosity of the pure solvent (water in this case). The intrinsic viscosity and the viscosity-average molar mass are related by the formula

$$
[ \eta ] = (2.00 \times 10 ^ {- 4} \mathrm{dl} \mathrm{g} ^ {- 1}) \left(\frac {M}{M _ {0}}\right) ^ {0.76},\tag{11.102}
$$

where M is the molar mass and $M_{0} = 1 \, g \, mol^{-1}$ (1 dalton). Find the molar mass if $[\eta] = 0.86 \, dl \, g^{-1}$ . Find the expected error in the molar mass if the expected error in $[\eta]$ is $0.03 \, dl \, g^{-1}$ .

3. Assuming that the ideal gas law holds, find the amount in moles of nitrogen gas in a container if

$$
\begin{array}{l} P = 0.856 \mathrm{atm} \pm 0.003 \mathrm{atm} \\ V = 0.01785 \mathrm{m} ^ {3} \pm 0.00008 \mathrm{m} ^ {3} \\ T = 297.3 \mathrm{K} \pm 0.2 \mathrm{K}. \end{array}
$$

Find the expected error in the amount of nitrogen.

4. The van der Waals equation of state is

$$
\left(P + \frac {n ^ {2} a}{V ^ {2}}\right) (V - n b) = n R T
$$

For carbon dioxide, $a = 0.3640 \, Pa m^{6} mol^{-1}$ and $b = 4.267 \times 10^{-5} \, m^{3} mol^{-1}$ . Find the pressure of 0.500 mol of carbon dioxide if $V = 0.00256 \, m^{3}$ and $T = 298.0 \, K$ . Find the uncertainty in the pressure if the uncertainty in the volume is $0.00004 \, m^{3}$ and the uncertainty in the temperature is 0.5 K. Assume that the uncertainty in n is negligible. Find the pressure predicted by the ideal gas equation of state. Compare the difference between the two pressures you calculated and the expected error in the pressure.

5. The following is a set of student data on the vapor pressure of liquid ammonia, obtained in a physical chemistry laboratory course. Find the indicated enthalpy change of vaporization. Remember that the Kelvin temperature must be used.

<table><tr><td>Temperature/°C</td><td>Pressure/torr</td></tr><tr><td>-76.0</td><td>51.15</td></tr><tr><td>-74.0</td><td>59.40</td></tr><tr><td>-72.0</td><td>60.00</td></tr><tr><td>-70.0</td><td>75.10</td></tr><tr><td>-68.0</td><td>91.70</td></tr><tr><td>-64.0</td><td>112.75</td></tr><tr><td>-62.0</td><td>134.80</td></tr><tr><td>-60.0</td><td>154.30</td></tr><tr><td>-58.0</td><td>176.45</td></tr><tr><td>-56.0</td><td>192.90</td></tr></table>

a) Ignoring the systematic errors, find the 95% confidence interval for the enthalpy change of vaporization.

b) Assuming that the apparatus used to obtain the data in the previous problem was about like that found in most undergraduate physical chemistry laboratories, make a reasonable estimate of the systematic errors and find the 95% confidence interval for the enthalpy change of vaporization, including both systematic and random errors.

6. The vibrational contribution to the molar heat capacity of a gas of nonlinear molecules is given in statistical mechanics by the formula

$$
C _ {m} (\mathrm{vib}) = R \sum_ {i = 1} ^ {3 n - 6} \frac {u _ {1} ^ {2} e ^ {- u _ {i}}}{(1 - e ^ {- u _ {i}}) ^ {2}},
$$

where $u_{i} = h\nu_{i}/k_{B}T$ . Here $\nu_{i}$ is the frequency of the ith normal mode of vibration, of which there are 3n-6 if n is the number of nuclei in the molecule (assumed nonlinear), h is Planck's constant, $k_{B}$ is Boltzmann's constant, R is the gas constant, and T is the absolute temperature. The $H_{2}O$ molecule has three normal modes. If their frequencies are given by

$$
\begin{array}{l} v _ {1} = 4.78 \times 10 ^ {13} \mathrm{s} ^ {- 1} \pm 0.002 \times 10 ^ {13} \mathrm{s} ^ {- 1} \\ v _ {2} = 1.095 \times 10 ^ {14} \mathrm{s} ^ {- 1} \pm 0.004 \times 10 ^ {14} \mathrm{s} ^ {- 1} \\ v _ {3} = 1.126 \times 10 ^ {14} \mathrm{s} ^ {- 1} \pm 0.004 \times 10 ^ {14} \mathrm{s} ^ {- 1} \end{array}
$$

calculate the vibrational contribution to the heat capacity of $H_{2}O$ vapor at 500 K and find the 95% confidence interval.

7. Water rises in a clean glass capillary tube to a height h given by

$$
h + \frac {r}{3} = \frac {2 \gamma}{\rho g r},
$$

where r is the radius of the tube, $\rho$ is the density of water, equal to 998.2 kg m $^{-3}$ at 20 °C, g is the acceleration due to gravity, equal to 9.80 m s $^{-2}$ , h is the height to the bottom of the meniscus, and $\gamma$ is the surface tension of the water. The term r/3 corrects for the liquid above the bottom of the meniscus.

a) If water at $20^{\circ}$ C rises to a height h of 29.6 mm in a tube of radius r = 0.500 mm, find the value of the surface tension of water at this temperature.

b) If the height h is uncertain by 0.4 mm and the radius of the capillary tube is uncertain by 0.02 mm, find the uncertainty in the surface tension.

c) The acceleration due to gravity varies with latitude. At the poles of the earth it is equal to $9.83 \, m s^{-2}$ . Find the error in the surface tension of water due to using this value rather than $9.80 \, m s^{-2}$ , which applies to latitude $39^{\circ}$ .

8. The nth moment of a probability distribution is defined by

$$
M _ {n} = \int (x - \mu) ^ {n} f (x) d x.
$$

The second moment is the variance, or square of the standard deviation. Show that for the Gaussian distribution, $M_{3} = 0$ , and find the value of $M_{4}$ . For this distribution, the limits of integration are $-\infty$ and $+\infty$ .

9. Vaughan $^{20}$ obtained the following data for the dimerization of butadiene at $326^{\circ}$ C.

```csv
Time/min Partial pressure of butadiene/atm
0 to be deduced
3.25 0.7961
8.02 0.7457
12.18 0.7057
17.30 0.6657
24.55 0.6073
33.00 0.5573
42.50 0.5087
55.08 0.4585
68.05 0.4173
90.05 0.3613
119.00 0.3073
259.50 0.1711
373.00 0.1081
```

Determine whether the reaction is first, second, or third order, using the least-squares method. Find the rate constant and its 95% confidence interval, ignoring systematic errors. Find the initial pressure of butadiene.

10. Make a graph of the partial pressure of butadiene as a function of time, using the data in the previous problem. Find the slope of the tangent line at 33.00 min and deduce the rate constant from it. Compare with the result from the previous problem.

<table><tr><td>Time/min</td><td>Concentration/mol l $^{-1}$ </td></tr><tr><td>0</td><td>0.500</td></tr><tr><td>2</td><td>0.349</td></tr><tr><td>4</td><td>0.267</td></tr><tr><td>6</td><td>0.217</td></tr><tr><td>8</td><td>0.182</td></tr><tr><td>10</td><td>0.157</td></tr><tr><td>12</td><td>0.139</td></tr><tr><td>14</td><td>0.124</td></tr><tr><td>16</td><td>0.112</td></tr><tr><td>18</td><td>0.102</td></tr><tr><td>20</td><td>0.093</td></tr></table>

11. The following are (contrived) data for a chemical reaction of one substances.

a) Assume that there is no appreciable back reaction and determine the order of the reaction and the value of the rate constant.

b) If you use Excel, find the expected error in the rate constant at the 95% confidence level.

c) Smooth the data. Find the value of the derivative dc/dt at t = 10 min., using the first, second, and third differences. Find the value of the rate constant from this value and compare it with your value from part a.

12. Use Eq. (11.32) to “smooth” the data given in Example 11.11. Using the smoothed data and Eq. (11.34) find the derivative dc/dt at t = 25 min. Find the rate constant.

13. If a capacitor of capacitance C is discharged through a resistor of resistance R the voltage on the capacitor follows the formula

$$
V (t) = V (0) e ^ {- t / R C}\tag{11.103}
$$

The following are data on the voltage as a function of time for the discharge of a capacitor through a resistance of $102 \, k\Omega$ .

<table><tr><td>t/s</td><td>V/s</td></tr><tr><td>0.00</td><td>1.00</td></tr><tr><td>0.020</td><td>0.819</td></tr><tr><td>0.040</td><td>0.670</td></tr><tr><td>0.060</td><td>0.549</td></tr><tr><td>0.080</td><td>0.449</td></tr><tr><td>0.100</td><td>0.368</td></tr><tr><td>0.120</td><td>0.301</td></tr><tr><td>0.140</td><td>0.247</td></tr><tr><td>0.160</td><td>0.202</td></tr><tr><td>0.180</td><td>0.165</td></tr><tr><td>0.200</td><td>0.135</td></tr></table>

Find the capacitance and its expected error.

14. The Bouguer–Beer law (sometimes called the Lambert–Beer law) states A = abc, where A is the of a solution, defined as $\log_{10}(I_{0}/I)$ where $I_{0}$ is the incident intensity of light at the appropriate wavelength and I is the transmitted intensity; b is the length of the cell through which the light passes; and c is the concentration of the absorbing substance. The coefficient a is called the molar absorptivity if the concentration is in moles per liter. The following is a set of data for the absorbance of a set of solutions of disodium fumarate at a wavelength of 250 nm. Using a linear least-squares fit with intercept set equal to zero, find the value of the absorptivity a if b = 1.000 cm. For comparison, carry out the fit without specifying zero intercept.

$$
\begin{array}{c c} A & c (\mathrm{mol} \mathrm{l} ^ {- 1}) \\ 0.1425 & 1.00 \times 10 ^ {- 4} \\ 0.2865 & 2.00 \times 10 ^ {- 4} \\ 0.4280 & 3.00 \times 10 ^ {- 4} \\ 0.5725 & 4.00 \times 10 ^ {- 4} \\ 0.7160 & 5.00 \times 10 ^ {- 4} \\ 0.8575 & 6.00 \times 10 ^ {- 4} \end{array}
$$

# Additional Reading

Here is a list of some books that are useful sources for further study in mathematics to be used in chemistry. No attempt has been made to be comprehensive. Some of the books are out of print, but should be available in college and university libraries.

## Books on Mathematics for Science

▶ Donald A. McQuarrie, Mathematical Methods for Scientists and Engineers, University Science Books, New York, 2003. This is an ambitious book, with over 1000 pages. The author is well known for writing clear and useful books.

▶ Philip M. Morse and Herman Feshbach, Methods of Theoretical Physics, McGraw-Hill, New York, 1953. This book comes in two parts and is a complete survey of all of the mathematics that a scientist might need. It is out of print, but should be found in almost any college or university library.

▶ Clifford E. Swartz, Used Math for the First Two Years of College Science, AAPT, College Park, MD, 1993. This book is a survey of various mathematical topics at the beginning college level.

## Calculus Textbooks

▶ Thomas H. Barr, Vector Calculus, 2nd ed., Prentice Hall, Upper Saddle River, NJ, 2000. This is a textbook for a third-semester calculus course that emphasizes vector calculus.

Wilfred Kaplan, Advanced Calculus, 5th ed., Addison-Wesley, Reading, MA, 2003. This is a text for a calculus course beyond the first year. It discusses infinite series and Fourier series.

▶ H. M. Schey, Div, Grad, Curl, and All That: An Informal Text on Vector Calculus, Norton, 1996

James Stewart, Calculus, 5th ed., Brooks/Cole, Pacific Grove, CA, 2003. This is a calculus textbook that uses some examples from physics in its discussions. You can read about coordinate systems, vectors, and complex numbers in almost any calculus textbook, including this one.

## Books on Numerical Analysis

▶ Richard L. Burden and J. Douglas Faires, Numerical Analysis, 4th ed., Brooks/Cole, 2001. This is a standard numerical analysis textbook at the advanced 360

undergraduate level. It contains explicit algorithms that can easily be converted into computer programs. out of print

## Advanced Mathematics Books

▶ Dean G. Duffy, Transform Methods for Solving Partial Differential Equations, 2nd ed., Chapman and Hall/CRC Press, Boca Raton, 2004. This book is a textbook for engineering students and focuses on practical applications.

J. F. James, A Student's Guide to Fourier Transforms, with Applications to Physics and Engineering, Cambridge Univ. Press, Cambridge, UK, 2002. This book is designed to teach the subject to a student without previous knowledge of Fourier transforms. It contains a description of the fast Fourier transform method and a computer program in BASIC to carry out the transformation.

▶ Erwin Kreyszig, Advanced Engineering Mathematics, 8th ed., Wiley, New York, 1999. This book is meant for engineers. It emphasizes applications rather than mathematical theory in a way that is useful to chemists.

▶ David L. Powers, Boundary Value Problems, Harcourt/Academic Press, New York, 1999. This book includes a 40-page chapter on Fourier series and integrals.

## Books on Experimental Data Analysis

▶ P. R. Bevington and D. K. Robinson, Data Reduction and Error Analysis for the Physical Sciences, 2nd ed., McGraw-Hill, New York, 1992. This is a very nice book, which includes a lot of useful things, including a discussion of different probability distributions, including the Gaussian distribution, and a discussion of weighted least-squares procedures.

▶ Carl W. Garland, Joseph W. Nibler, and David P. Shoemaker, Experiments in Physical Chemistry, 7th ed., McGraw-Hill, New York, 2003. This is a standard physical chemistry laboratory textbook and contains a good section on the treatment of experimental errors as well as most of the experiments commonly done in physical chemistry courses.

▶ John A. Rice, Mathematical Statistics and Data Analysis, 2nd ed., Duxbury Press, 1985. This is a standard textbook for mathematical statistics. It includes numerous examples from experimental chemistry and is a good reference for chemists.

## Computer Books

▶ E. J. Billo, Microsoft Excel for Chemists: A Comprehensive Guide, 2nd ed., Wiley, New York, 2001. This is a much more useful guide to Excel than the manual provided by the manufacturer.

▶ Robert de Levie, How to Use Excel in Analytical Chemistry and in General Scientific Data Analysis, Cambridge University Press, 2001.

▶ Robert de Levie, Advanced Excel for Scientific Data Analysis, Oxford University Press, 2004. This book is available in both paperback and hardbound editions.

▶ Dermot Diamond and Venita C. A. Hanratty, Spreadsheet Applications in Chemistry Using Microsoft Excel, Wiley Interscience, New York, 1997. This is a comprehensive introduction to the use of Excel for chemists.

▶ Erwin Kreyszig and E. J. Norminton, Mathematica Computer Manual to Accompany Advanced Engineering Mathematics, 8th ed., Wiley, New York, 2001.

▶ Stephen Wolfram, The Mathematica Book, 5th ed., Wolfram Media, 2003. This is a textbook that provides a complete introduction to the use of Mathematica, written by its inventor.

## Problem-Solving and Problem Books

▶ G. Polya, How to Solve It, A New Aspect of Mathematical Method, 2nd ed., Princeton Univ. Press, Princeton, NJ, 1957. This small book is out of print but it should be in every college or university library. It contains a detailed discussion of general methods of solving problems.

▶ C. R. Metz, 2000 Solved Problems in Physical Chemistry, McGraw-Hill, New York, 1990. This is a good source of practice problems in physical chemistry.

## Mathematical Tables

▶ Milton Abramowitz and Irene A. Stegun, Eds., Handbook of Mathematical Functions with Formulas, Graphs and Mathematical Tables, National Bureau of Standards Applied Mathematics Series No. 55, U.S. Government Printing Office, Washington, DC, 1964. This large but inexpensive book contains a variety of different things, including integrals and useful formulas.

▶ A. Erdélyi, Ed., Tables of Integral Transforms, Vols. I and II, McGraw-Hill, New York, 1954. This set of two volumes contains a brief introduction of several types of integral transforms, with extensive tables of transforms of specific functions.

▶ Herbert B. Dwight, Tables of Integrals and Other Mathematical Data, 4th ed., Macmillan Co., New York, 1962. This book is out of print, but if you can find a used copy, you will find that it is a very useful compilation of formulas, including trigonometric identities, derivatives, infinite series, and definite and indefinite integrals.

I. S. Gradshteyn and I. M. Ryzhik, Tables of Integrals, Series and Products, 4th ed., prepared by Yu. V. Geronimus and M. Yu. Tseytlin, translated by Alan Jeffreys, Academic Press, New York, 1965. This is a large book with lots of definite and indefinite integrals in it. It is out of print but should be available in college and university libraries.

The Handbook of Chemistry and Physics, CRC Publishing Co., Boca Raton, FL, with various editors and various editions, contains various mathematical tables.

# Values of Physical Constants $^{1}$

Avogadro's constant,

$$
N _ {\mathrm{Av}} = 6.02214 \times 10 ^ {23} \mathrm{mol} ^ {- 1}.
$$

Molar ideal gas constant,

$$
\begin{array}{r l} R & = 8.3145 \mathrm{JK} ^ {- 1} \mathrm{mol} ^ {- 1} = 0.082056 \text {liter atm K} ^ {- 1} \mathrm{mol} ^ {- 1} \\ & = 1.9872 \mathrm{calK} ^ {- 1} \mathrm{mol} ^ {- 1}. \end{array}
$$

The magnitude of an electron's charge,

$$
e = 1.602177 \times 10 ^ {- 19} \mathrm{C}.
$$

Planck's constant,

$$
h = 6.62608 \times 10 ^ {- 34} \mathrm{Js}.
$$

Boltzmann's constant,

$$
k _ {B} = 1.38066 \times 10 ^ {- 23} \mathrm{JK} ^ {- 1}.
$$

The rest-mass of an electron,

$$
m _ {e} = 9.10939 \times 10 ^ {- 31} \mathrm{kg}.
$$

The rest-mass of a proton,

$$
m _ {p} = 1.672623 \times 10 ^ {- 27} \mathrm{kg}.
$$

The rest-mass of a neutron,

$$
m _ {n} = 1.674929 \times 10 ^ {- 27} \mathrm{kg}.
$$

The speed of light (exact value, used to define the standard meter),

$$
c = 2.99792458 \times 10 ^ {8} \mathrm{ms} ^ {- 1} = 2.99792458 \times 10 ^ {10} \mathrm{cm} \mathrm{s} ^ {- 1}.
$$

The acceleration due to gravity near the earth's surface (varies slightly with latitude. This value applies near the latitude of Washington, DC, USA, or Madrid, Spain),

$$
g = 9.80 \mathrm{ms} ^ {- 7}.
$$

The gravitational constant,

$$
\mathrm{G} = 6.673 \times 10 ^ {- 11} \mathrm{m} ^ {3} \mathrm{s} ^ {- 2} \mathrm{kg} ^ {- 1}.
$$

The permittivity of a vacuum,

$$
\epsilon_ {0} = 8.8545187817 \times 10 ^ {- 12} \mathrm{C} ^ {2} \mathrm{N} ^ {- 1} \mathrm{m} ^ {- 2}.
$$

The permeability of a vacuum (exact value, by definition),

$$
\mu_ {0} = 4 \pi \times 10 ^ {- 7} \mathrm{NA} ^ {- 2}.
$$

## Some Conversion Factors

```txt
1 pound = 1lb = 0.4535924 kg
```

```txt
1 inch = 1 in = 0.0254 m (exact value by definition)
```

```txt
1 calorie = 1 cal = 4.184 J (exact value by definition)
```

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
1 electron volt = 1 eV = 1.60219 × 10$^{-19}$J
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
1 erg =  $10^{-7}$  J (exact value by definition)
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
1 atm = 760 torr = 101, 325 N m $^{-2}$  = 101, 325 pascal (Pa) (exact values by definition)
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
1 atomic mass unit = 1 u = 1.66054 × 10$^{-27}$ kg
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
1 horsepower = 1 hp = 745.700 watt = 745.700 J s $^{-1}$
</div>

# Some Mathematical Formulas and Identities

1. The arithmetic progression of the first order to n terms,

$$
\begin{array}{r l} a + (a + d) + (a + 2 d) + \dots + [ a + (n - 1) d ] & = n a + \frac {1}{2} n (n - 1) d \\ & = \frac {n}{2} (1 \text {st term} + n \text {th term}). \end{array}
$$

2. The geometric progression to $n$ terms,

$$
a + a r + a r ^ {2} + \dots + a r ^ {n - 1} = \frac {a (1 - r ^ {n})}{1 - r}.
$$

3. The definition of the arithmetic mean of $a_{1}, a_{2}, \ldots, a_{n}$ ,

$$
\frac {1}{n} (a _ {1} + a _ {2} + \dots + a _ {n}).
$$

4. The definition of the geometric mean of $a_1, a_2, \ldots, a_n$ ,

$$
\bar {a} _ {G} = (a _ {1} a _ {2} \dots a _ {n}) ^ {1 / n}.
$$

5. The definition of the harmonic mean of $a_1, a_2, \ldots, a_n$ : If $\bar{a}_{\mathrm{H}}$ is the harmonic mean, then

$$
\frac {1}{\bar {a} _ {H}} = \frac {1}{n} \left(\frac {1}{a _ {1}} + \frac {1}{a _ {2}} + \frac {1}{a _ {3}} + \dots + \frac {1}{a _ {n}}\right).
$$

6. If

$$
a _ {0} + a _ {1} x + a _ {2} x ^ {2} + a _ {3} x ^ {3} + \dots + a _ {n} x ^ {n} = b _ {0} + b _ {1} x + b _ {2} x ^ {2} + b _ {3} x ^ {3} + \dots + b _ {n} x ^ {n}
$$

for all values of $x$ , then

$$
a _ {0} = b _ {0}, \quad a _ {1} = b _ {1} \quad a _ {2} = b _ {2}, \dots , a _ {n} = b _ {n}.
$$

## Trigonometric Identities

7. $\sin^2 (x) + \cos^2 (x) = 1.$

8. $\tan (x) = \frac{\sin(x)}{\cos(x)}.$

9. $\operatorname{ctn}(x) = \frac{1}{\tan(x)}$ .

10. $\sec (x) = \frac{1}{\cos(x)}$ .

11. $\csc (x) = \frac{1}{\sin(x)}$ .

12. $\sec^2 (x) - \tan^2 (x) = 1.$

13. $\csc^2 (x) - \operatorname {ctn}^2 (x) = 1.$

14. $\sin (x + y) = \sin (x)\cos (y) + \cos (x)\sin (y).$

15. $\cos (x + y) = \cos (x)\cos (y) - \sin (x)\sin (y).$ 16.

16. $\sin (2x) = 2\sin (x)\cos (x).$

17. $\cos (2x) = \cos^2 (x) - \sin^2 (x) = 1 - 2\sin^2 (x).$

18. $\tan (x + y) = \frac{\tan(x) + \tan(y)}{1 - \tan(x)\tan(y)}$

19. $\tan (2x) = \frac{2\tan(x)}{1 - \tan^2(x)}.$

20. $\sin (x) = \frac{1}{2i} (e^{ix} - e^{-ix})$

21. $\cos (x) = \frac{1}{2} (e^{ix} + e^{-ix})$

$$
\sin (x) = - \sin (- x).
$$

23. $\cos (x) = \cos (-x)$ .

$$
\tan (x) = - \tan (- x)
$$

25. $\sin (ix) = i\sinh (x)$

26. $\cos (ix) = \cosh (x)$ .

27. $\tan (ix) = i\tanh (x)$

28. $\sin (x\pm iy) = \sin (x)\cosh (y)\pm i\cos (x)\sinh (y).$

29. $\cos (x\pm iy) = \cos (x)\cosh (y)\mp i\sin (x)\sinh (y).$

30. $\cosh (x) = \frac{1}{2} (e^x + e^{-x})$ .

31. $\sinh (x) = \frac{1}{2} (e^x - e^{-x})$ .

32. $\tanh (x) = \frac{\sinh(x)}{\cosh(x)}.$

33. $\operatorname{sech}(x) = \frac{1}{\cosh(x)}$ .

34. $\operatorname{csch}(x) = \frac{1}{\sinh(x)}$ .

35. $\operatorname{ctnh}(x) = \frac{1}{\tanh(x)}$ .

36. $\cosh^2 (x) - \sinh^2 (x) = 1.$

37. $\tanh^2 (x) + \operatorname{sech}^2 (x) = 1.$

38. $\operatorname{ctnh}^2 (x) - \operatorname{scsh}^2 (x) = 1.$

39. $\sinh (x) = -\sinh (-x)$ .

40. $\cosh (x) = \cosh (-x)$ .

41. $\tanh (-x) = -\tanh (-x)$ .

42. Relations obeyed by any triangle with angle A opposite side a, angle B opposite side b, and angle C opposite side c:

a) $A + B + C = 180^{\circ} = \pi \mathrm{rad}$

b) $c^2 = a^2 + b^2 - 2ab\cos (C)$

c) $\frac{a}{\sin(A)} = \frac{b}{\sin(B)} = \frac{c}{\sin(C)}.$

## Infinite Series

![[1abad0f79657d6cd4bec7c7491c82fa92255752391b3793202df20f8afbbde55.jpg]]

## C.1 Series with Constant Terms

1. $1 + \frac{1}{2} + \frac{1}{3} + \frac{1}{4} + \cdots = \infty.$

2. $1 + \frac{1}{2^{2}} + \frac{1}{3^{2}} + \frac{1}{4^{2}} + \cdots = \frac{\pi^{2}}{6}.$

3. $1 + \frac{1}{2^{4}} + \frac{1}{3^{4}} + \frac{1}{4^{4}} + \cdots = \frac{\pi^{4}}{90}.$

4. $1 + \frac{1}{2^{p}} + \frac{1}{3^{p}} + \frac{1}{4^{p}} + \cdots = \zeta(p)$ .

The function $\zeta(p)$ is called the Riemann zeta function. $^{1}$

5. $1 - \frac{1}{2} + \frac{1}{3} - \frac{1}{4} + \cdots = \ln(2)$ .

6. $1 - \frac{1}{2^{p}} + \frac{1}{3^{p}} + \frac{1}{4^{p}} + \cdots = (1 - \frac{2}{2^{p}})\zeta(p).$

## C.2 Power Series

7. Maclaurin's series. If there is a power series in $x$ for $f(x)$ , it is

$$
f (x) = f (0) + \left. \frac {d f}{d x} \right| _ {x = 0} x = \frac {1}{2 !} \left. \frac {d ^ {2} f}{d x ^ {2}} \right| _ {x = 0} x ^ {2} = \frac {1}{3 !} \left. \frac {d ^ {3} f}{d x ^ {3}} \right| _ {x = 0} x ^ {3} + \dots .
$$

8. Taylor's series. If there is a power series in $x - a$ for $f(x)$ , it is

$$
f (x) = f (a) + \frac {d f}{d x} \bigg | _ {x = a} (x - a) + \frac {1}{2 !} \left. \frac {d ^ {2} f}{d x ^ {2}} \right| _ {x = a} (x - a ^ {2}) + \dots .
$$

In Eqs. (7) and (8), $\left.\frac{df}{dx}\right|_{x = a}$ means the value of the derivative $df / dx$ evaluated at $x = a$ .

9. If, for all values of x,

$$
a _ {0} + a _ {1} x + a _ {2} x ^ {2} + a _ {3} x ^ {3} + \dots = b _ {0} + b _ {1} x + b _ {2} x ^ {2} + b _ {3} x ^ {3} + \dots
$$

then $a_0 = b_0, a_1 = b_1, a_2 = b_2$ , etc.

10. The reversion of a series. If

$$
y = a x + b x ^ {2} + c x ^ {3} + \dots
$$

and

$$
x = A y + B y ^ {2} + C y ^ {3} + \dots ,
$$

then

$$
A = \frac {1}{a}, \quad B = - \frac {b}{a ^ {3}}, \quad C = \frac {1}{a ^ {5}} (2 b ^ {2} - a c),
$$

$$
D = \frac {1}{a ^ {7}} (5 a b c - a ^ {2} d - 5 b ^ {3}), \quad \mathrm{etc.}
$$

See Dwight, Table of Integrals and Other Mathematical Data (cited above), for more coefficients.

11. Powers of a series. If

$$
S = a + b x + c x ^ {2} + d x ^ {3} + \dots ,
$$

then

$$
\begin{array}{r l} {S ^ {2}} & {= a ^ {2} + 2 a b x + (b ^ {2} + 2 a c) x ^ {2} + 2 (a d + b c) x ^ {3}} \\ & {+ (c ^ {2} + 2 a e + 2 b d) x ^ {4} + 2 (a f + b e + c d) x ^ {5} + \dots} \end{array}
$$

$$
S ^ {1 / 2} = a ^ {1 / 2} \left[ 1 + \frac {b}{2 a} x + (\frac {2}{2 a} - \frac {b ^ {2}}{8 a ^ {2}}) x ^ {2} + \dots \right]
$$

$$
S ^ {- 1} = a ^ {- 1} \left[ 1 - \frac {b}{a} x + \left(\frac {b ^ {2}}{a ^ {2}} - \frac {c}{a}\right) x ^ {2} + \left(\frac {2 b c}{a ^ {2}} - \frac {d}{a} - \frac {b ^ {3}}{a ^ {3}}\right) x ^ {3} + \dots \right].
$$

12. $\sin (x) = x - \frac{x^3}{3!} +\frac{x^5}{5!} -\frac{x^7}{7!} +\dots .$

13. $\cos (x) = 1 - \frac{x^2}{2!} +\frac{x^4}{4!} -\frac{x^6}{6!} +\dots .$

$$
\sin (\theta + x) = \sin (\theta) + x \cos (\theta) - \frac {x ^ {2}}{2 !} \sin (\theta) - \frac {x ^ {3}}{3 !} \cos (\theta) + \dots .
$$

$$
\cos (\theta + x) = \cos (\theta) - x \sin (\theta) - \frac {x ^ {2}}{2 !} \cos (\theta) + \frac {x ^ {3}}{3 !} \sin (\theta) + \dots .
$$

16. $\sin^{-1}(x)=x+\frac{x^{3}}{2\cdot3}+\frac{1\cdot3x^{5}}{2\cdot4\cdot5}+\frac{1\cdot3\cdot5x^{7}}{2\cdot4\cdot6\cdot7}+\cdots$ , where $x^{2}<1$ . The series gives the principal value, $-\pi/2<\sin^{-1}(x)<\pi/2$ .

17. $\cos^{-1}(x)=\frac{\pi}{2}-\left(x+\frac{x^{3}}{2\cdot3}+\frac{1\cdot3x^{5}}{2\cdot4\cdot5}+\cdots\right)$ , where $x^{2}<1$ . The series gives the principal value, $0<\cos^{-1}(x)<\pi$ .

$$
e ^ {x} = 1 + x + \frac {x ^ {2}}{2 !} + \frac {x ^ {3}}{3 !} + \frac {x ^ {4}}{4 !} + \dots (x ^ {2} <   \infty).
$$

$$
19. a ^ {x} = e ^ {x \ln (a)} = 1 + x \ln (a) + \frac {(x \ln (a)) ^ {2}}{2 !} + \dots .
$$

$$
\ln (1 + x) = x - \frac {x ^ {2}}{2} + \frac {x ^ {3}}{3} - \frac {x ^ {4}}{4} \dots (x ^ {2} <   1 \text { and } x = 1).
$$

$$
\ln (1 - x) = - \left(x + \frac {x ^ {2}}{2} + \frac {x ^ {3}}{3} + \frac {x ^ {4}}{4} + \dots\right) \left(x ^ {2} <   1 \text {   and   } x = - 1\right).
$$

$$
\sinh (x) = x + \frac {x ^ {3}}{3 !} + \frac {x ^ {5}}{5 !} + \frac {x ^ {7}}{7 !} + \dots (x ^ {2} <   \infty).
$$

$$
\cosh (x) = 1 + \frac {x ^ {2}}{2 !} + \frac {x ^ {4}}{4 !} + \frac {x ^ {6}}{6 !} + \dots (x ^ {2} <   \infty).
$$

# A Short Table of Derivatives

In the following list, $a$ , $b$ , and $c$ are constants, and $e$ is the base of natural logarithms.

1. $\frac{d}{dx} (au) = a\frac{du}{dx}$ .

2. $\frac{d}{dx} (uv) = u\frac{dv}{dx} + v\frac{du}{dx}$ .

3. $\frac{d}{dx} (uvw) = uv\frac{dw}{dx} +uw\frac{dv}{dx} +vw\frac{du}{dx}$

4. $\frac{d(x^n)}{dx} = nx^{n - 1}$

5. $\frac {d}{d x} \left(\frac {u}{v}\right) = \frac {1}{v} \frac {d u}{d x} - \frac {u}{v ^ {2}} \frac {d v}{d x} = \frac {1}{v ^ {2}} \left(v \frac {d u}{d x} - u \frac {d v}{d x}\right).$

6. $\frac{d}{dx}f(u)=\frac{df}{du}\frac{du}{dx}$ , where f is some differentiable function of u and u is some differentiable function of x (the chain rule).

7. $\frac{d^2}{dx^2} f(u) = \frac{df}{du}\frac{d^2u}{dx^2} +\frac{d^2f}{du^2}\left(\frac{du}{dx}\right)^2.$

8. $\frac{d}{dx}\sin (ax) = a\cos (ax).$

9. $\frac{d}{dx}\cos (ax) = -a\sin (ax).$

10. $\frac{d}{dx}\tan (ax) = a\sec^2 (ax).$

11. $\frac{d}{dx}\mathrm{ctn}(ax) = -a\csc^2 (ax).$

12. $\frac{d}{dx}\sec (ax) = a\sec (ax)\tan (ax).$

13. $\frac{d}{dx}\csc (ax) = -a\csc (ax)\mathrm{ctn}(ax).$

14. $\frac{d}{dx}\sin^{-1}\left(\frac{x}{a}\right) = \frac{1}{\sqrt{a^2 - x^2}}$ if $x / a$ is in the first or fourth quadrant $= \frac{-1}{\sqrt{a^2 - x^2}}$ if $x / a$ is in the second or third quadrant.

15. $\frac{d}{dx}\cos^{-1}\left(\frac{x}{a}\right) = \frac{-1}{\sqrt{a^2 - x^2}}$ if $x / a$ is in the first or second quadrant $= \frac{1}{\sqrt{a^2 - x^2}}$ if $x / a$ is in the third or fourth quadrant.

16. $\frac{d}{dx}\tan^{-1}\left(\frac{x}{a}\right) = \frac{a}{a^2 + x^2}.$

17. $\frac{d}{dx}\mathrm{ctn}^{-1}\left(\frac{x}{a}\right) = \frac{-a}{a^2 + x^2}.$

18. $\frac{d}{dx} e^{ax} = ae^{ax}$ .

19. $\frac{d}{dx} a^x = a^x\ln (a).$

20. $\frac{d}{dx} a^{cx} = ca^{cx}\ln (a).$

21. $\frac{d}{dx} u^y = yu^{y - 1}\frac{d}{dx} +u^y\ln (u)\frac{d}{dx}.$

22. $\frac{d}{dx} x^{x} = x^{x}[1 + \ln (x)].$

23. $\frac{d}{dx}\ln (ax) = \frac{1}{x}.$

24. $\frac{d}{dx}\log_a(x) = \frac{\log_a(a)}{x}$ .

25. $\frac{d}{dq}\int_{p}^{q}f(x)dx = f(q)$ if $p$ is independent of $q$ .

26. $\frac{d}{dq}\int_{p}^{q}f(x)dx = -f(p)$ if $q$ is independent of $p$ .

# A Short Table of Indefinite Integrals

In the following, an arbitrary constant of integration is to be added to each equation. a, b, c, g, and n are constants.

1. $\int dx = x$ .

2. $\int x dx = \frac{x^2}{2}$ .

3. $\int \frac{1}{x} dx = \ln (|x|)$ Do not integrate from negative to positive values of $x$ .

4. $\int x^n dx = \frac{x^{n + 1}}{n + 1}$ , where $n \neq -1$ .

5. $\int (a + bx)^n dx = \frac{(a + bx)^{n + 1}}{b(n + 1)}.$

6. $\int \frac{1}{(a + bx)} dx = \frac{1}{b}\ln (|a + bx|)$ .

7. $\int \frac {1}{(a + b x) ^ {n}} d x = \frac {- 1}{(n - 1) b (a + b x) ^ {n - 1}}.$

8. $\int \frac{x}{(a + bx)} dx = \frac{1}{b^2} [(a + bx) - a\ln (|a + bx|)].$

9. $\int \frac{a + bx}{c + gx} dx = \frac{bx}{g} +\frac{ag - bc}{g^2}\ln (|c + gx|).$

10. $\int \frac{1}{(a + bx)(c + gx)} dx = \frac{1}{ag - bc}\ln \left(\left|\frac{c + gx}{a + bx}\right|\right)$ .

11. $\int \frac{1}{a^2 + x^2} dx = \frac{1}{a}\tan^{-1}\left(\frac{x}{a}\right).$

12. $\int \frac{x}{(a^2 + x^2)^2} dx = \frac{-1}{2(a^2 + x^2)}.$

13. $\int \frac{x}{(a^2 + x^2)} dx = \frac{1}{2}\ln (a^2 +x^2).$

14. $\int \frac{1}{(a^2 - b^2x^2)} dx = \frac{1}{2ab} \ln \left( \left| \frac{a + bx}{a - bx} \right| \right)$ .

15. $\int \frac{x}{(a^2 - x^2)} dx = -\frac{1}{2}\ln (|a^2 - x^2|)$ .

16. $\int \frac{x^{1 / 2}}{(a^2 + b^2x)} dx = \frac{2x^{1 / 2}}{b^2} -\frac{2a}{b^3}\tan^{-1}\left(\frac{bx^{1 / 2}}{a}\right).$

17. $\int \frac{1}{(a + bx^2)^{\rho / 2}} dx = \frac{-2}{(p - 2)b(a + bx)^{(\rho - 2) / 2}}.$

18. $\int \frac{1}{(x^2 + a^2)^{1/2}} dx = \ln (x + (x^2 + a^2)^{1/2}).$

19. $\int \frac {x}{(x ^ {2} + a ^ {2}) ^ {1 / 2}} d x = (x ^ {2} + a ^ {2}) ^ {1 / 2}.$

20. $\int \frac{1}{(x^2 - a^2)^{1/2}} dx = \ln (x + (x^2 - a^2)^{1/2}).$

21. $\int \frac{x}{(x^2 - a^2)^{1 / 2}} dx = (x^2 - a^2)^{1 / 2}.$

22. $\int \sin (ax)dx = -\frac{1}{a}\cos (ax).$

23. $\int \sin (a + bx)dx = -\frac{1}{b}\cos (a + bx).$

24. $\int x\sin (x)dx = \sin (x) - x\cos (x).$

25. $\int x^{2}\sin (x)dx = 2x\sin (x) - (x^{2} - 2)\cos (x).$

26. $\int \sin^2 (x)dx = \frac{x}{2} -\frac{\sin(2x)}{4} = \frac{x}{2} -\frac{\sin(x)\cos(x)}{2}.$

27. $\int x\sin^2 (x)dx = \frac{x^2}{4} -\frac{x\sin(2x)}{4} -\frac{\cos(2x)}{8}.$

28. $\int \frac{1}{1 + \sin(x)} dx = -\tan \left(\frac{\pi}{4} -\frac{x}{2}\right).$

29. $\int \cos (ax)dx = \frac{1}{a}\sin (ax).$

30. $\int \cos (a + bx)dx = \frac{1}{b}\sin (a + bx).$

31. $\int x\cos (x)dx = \cos (x) + x\sin (x).$

32. $\int x^{2}\cos (x)dx = 2x\cos (x) + (x^{2} - 2)\sin (x).$

33. $\int \cos^2 (x)dx = \frac{x}{2} +\frac{\sin(2x)}{4} = \frac{x}{2} +\frac{\sin(x)\cos(x)}{2}.$

34. $\int x\cos^2 (x)dx = \frac{x^2}{4} +\frac{x\sin(2x)}{4} +\frac{\cos(2x)}{8}.$

35. $\int \frac{1}{1 + \cos(x)} dx = \tan \left(\frac{x}{2}\right)$ .

36. $\int \sin (x)\cos (x)dx = \frac{\sin^2(x)}{2}.$

37. $\int \sin^2 (x)\cos^2 (x)dx = \frac{1}{8}\left[x - \frac{\sin(4x)}{4}\right].$

38. $\int \sin^{-1}\left(\frac{x}{a}\right)dx = x\sin^{-1}\left(\frac{x}{a}\right) + (a^2 -x^2)^{1 / 2}.$

39. $\int [\sin^{-1}\left(\frac{x}{a}\right)]^2 dx = x[\sin^{-1}\left(\frac{x}{a}\right)]^2 - 2x + 2(a^2 - x^2)^{1/2}\sin^{-1}\left(\frac{x}{a}\right)$ .

40. $\int \cos^{-1}\left(\frac{x}{a}\right)dx = x\cos^{-1}\left(\frac{x}{a}\right) - (a^2 -x^2)^{1 / 2}.$

41. $\int [\cos^{-1}\left(\frac{x}{a}\right)]^2 dx = x[\cos^{-1}\left(\frac{x}{a}\right)]^2 - 2x - 2(a^2 - x^2)^{1/2} \cos^{-1}\left(\frac{x}{a}\right)$ .

42. $\int \tan^{-1}\left(\frac{x}{a}\right)dx = x\tan^{-1}\left(\frac{x}{a}\right) - \frac{a}{2}\ln (a^2 +x^2).$

43. $\int x\tan^{-1}\left(\frac{x}{a}\right)dx = \frac{1}{2} (x^2 +a^2)\tan^{-1}\left(\frac{x}{a}\right) - \frac{ax}{2}.$

44. $\int e^{ax}dx = \frac{1}{a} e^{ax}$

45. $\int a^r dx = \frac{a^x}{\ln(a)}.$

46. $\int xe^{ax} dx = e^{ax}\left(\frac{x}{a} - \frac{1}{a^2}\right)$ .

47. $\int x^{2}e^{ax}dx = e^{ax}\left[\frac{x^{2}}{a} -\frac{2x}{a^{2}} +\frac{2}{a^{3}}\right].$

48. $\int e^{ax}\sin (x)dx = \frac{e^{ax}}{a^2 + 1} [a\sin (x) - \cos (x)].$

49. $\int e^{ax}\cos (x)dx = \frac{e^{ax}}{a^2 + 1} [a\cos (x) + \sin (x)].$

50. $\int e ^ {a x} \sin^ {2} (x) d x = \frac {e ^ {a x}}{a ^ {2} + 4} \left[ a \sin^ {2} (x) - 2 \sin (x) \cos (x) + \frac {2}{a} \right].$

51. $\int \ln (ax)dx = x\ln (ax) - x.$

52. $\int x\ln (x)dx = \frac{x^2}{2}\ln (x) - \frac{x^2}{4}.$

53. $\int \frac{\ln(ax)}{x} dx = \frac{1}{2} [\ln (ax)]^2.$

54. $\int \frac{1}{x\ln(x)} dx = \ln (|\ln (x)|)$ .

55. $\int \tan (ax)dx = \frac{1}{a}\ln (|\sec (ax)|) = -\frac{1}{a}\ln (|\cos (ax)|)$ .

56. $\int \cot (ax)dx = \frac{1}{a}\ln (|\sin (ax)|).$

# A Short Table of Definite Integrals

In the following list, a, b, m, n, p, and r are constants.

$$
\int_ {0} ^ {\infty} x ^ {n - 1} e ^ {- x} d x = \int_ {0} ^ {1} \left[ \ln \left(\frac {1}{x}\right) \right] ^ {- 1} d x = \Gamma (n) \quad (n > 0).
$$

The function $\Gamma(n)$ is called the gamma function. It has the following properties: for any $n > 0$ ,

$$
\Gamma (n + 1) = n \Gamma (n).
$$

for any integral value of n > 0,

$$
\Gamma (n) = (n - 1)!
$$

for $n$ not an integer,

$$
\Gamma (n) \Gamma (1 - n) = \frac {\pi}{\sin (n \pi)}
$$

$$
\Gamma \left(\frac {1}{2}\right) = \sqrt {\pi}.
$$

2. $\int_0^\infty \frac{1}{1 + x + x^2} dx = \frac{\pi}{3\sqrt{3}}.$

3. $\int_0^\infty \frac{x^{p - 1}}{(1 + x)^\rho} dx = \frac{\pi}{\sin(p\pi)}$ $(0 <   p <   1)$

$$
\int_ {0} ^ {\infty} \frac {x ^ {p - 1}}{a + x} d x = \frac {\pi a ^ {p - 1}}{\sin (p \pi)} \quad (0 <   p <   1).
$$

5. $\int_{0}^{\infty}\frac{x^{p}}{(1 + ax)^{2}} dx = \frac{p\pi}{a^{\rho + 1}\sin(p\pi)}.$

6. $\int_0^\infty \frac{1}{1 + x^p} dx = \frac{\pi}{p\sin(\pi / p)}.$

$$
\int_ {0} ^ {\pi / 2} \sin^ {2} (m x) d x = \int_ {0} ^ {\pi / 2} \cos^ {2} (m x) d x = \frac {\pi}{4} (m = 1, 2, \dots).
$$

$$
\int_ {0} ^ {\pi} \sin^ {2} (m x) d x = \int_ {0} ^ {\pi} \cos^ {2} (m x) d x = \frac {\pi}{2} (m = 1, 2, \dots).
$$

$$
\int_ {0} ^ {\pi / 2} \tan^ {p} (x) d x = \int_ {0} ^ {\pi / 2} \operatorname{ctn} ^ {p} (x) d x = \frac {\pi}{2 \cos (p \pi / 2)} (p ^ {2} <   1).
$$

10. $\int_0^{\pi /2}\frac{x}{\tan(x)} dx = \frac{\pi}{2}\ln (2).$

$$
\int_ {0} ^ {\pi / 2} \sin^ {p} (x) \cos^ {p} (x) d x = \frac {\Gamma ((p + 1) / 2) \Gamma ((q + 1) / 2)}{2 \Gamma ((p + q) / 2 + 1)} (p + 1 > 0, q + 1 > 0).
$$

$$
\int_ {0} ^ {\pi} \sin (m x) \sin (n x)   d x = \left\{ \begin{array}{l l} 0 & \text { if } m \neq n \\ \frac {\pi}{2} & \text { if } m = n \end{array} \right. (m, n \text {   integers }).
$$

13. $\int_{0}^{\pi}\cos (mx)\cos (nx)dx = \left\{ \begin{array}{ll}0 & \text{if } m\neq n\\ \frac{\pi}{2} & \text{if } m = n \end{array} \right.$ $(m,n$ integers).

14. $\int_0^\pi \sin (mx)\sin (nx)dx$

$$
= \left\{ \begin{array}{c l} 0 & \text {if m = n} \\ 0 & \text {if m\neq n and m + n is even} \\ \frac {2 m}{m ^ {2} - n ^ {2}} & \text {if m\neq n and m + n is odd (m,n integers).} \end{array} \right.
$$

15. $\int_0^\infty \sin \left(\frac{\pi x^2}{2}\right)dx = \int_0^\infty \cos \left(\frac{\pi x^2}{2}\right)dx = 1 / 2.$

$$
\int_ {0} ^ {\infty} \sin (x ^ {p}) d x = \Gamma \left(1 + \frac {1}{p}\right) \sin \left(\frac {\pi}{2 p}\right) \quad (p > 1).
$$

$$
\int_ {0} ^ {\infty} \cos (x ^ {p}) d x = \Gamma \left(1 + \frac {1}{p}\right) \cos \left(\frac {\pi}{2 p}\right) \quad (p > 1).
$$

18. $\int_{0}^{\infty}\frac{\sin(mx)}{x} dx = \left\{ \begin{array}{ll}\frac{\pi}{2} & \text{if } m > 0\\ 0 & \text{if } m = 0\\ -\frac{\pi}{2} & \text{if } m <   0 \end{array} \right.$

$$
\int_ {0} ^ {\infty} \frac {\sin (m x)}{x ^ {\rho}} d x = \frac {\pi m ^ {p - 1}}{2 \sin (p \pi / 2) \Gamma (p)} \quad (0 <   p <   2, m > 0). \tag {19}
$$

20. $\int_0^\infty e^{-ax}dx = \frac{1}{a}$ $(a > 0)$ .

21. $\int_0^\infty xe^{-ax}dx = \frac{1}{a^2}$ $(a > 0)$ .

22. $\int_0^\infty x^2 e^{-ax}dx = \frac{2}{a^3}$ $(a > 0)$ .

23. $\int_0^\infty x^{1 / 2}e^{-ax}dx = \frac{\sqrt{\pi}}{2a^{3 / 2}} (a > 0).$

24. $\int_0^\infty e^{-r^2 x^2}dx = \frac{\sqrt{\pi}}{2r}$ $(r > 0)$ .

25. $\int_0^\infty xe^{-r^2 x^2}dx = \frac{1}{2r^2}$ $(r > 0)$ .

26. $\int_0^\infty x^2 e^{-r^2 x^2}dx = \frac{\sqrt{\pi}}{4r^3}$ $(r > 0)$ .

27. $\int_0^\infty r^{2n + 1}e^{-r^2 x^2}dx = \frac{n!}{2r^{2n + 2}}\quad (r > 0,n = 1,2,\dots).$

28. $\int_0^\infty x^{2n}e^{-r^2 x^2}dx = \frac{(1)(3)(5)\cdots(2n - 1)}{2^{n + 1}r^{2n + 1}}\sqrt{\pi}$ $(r > 0,n = 1,2,\dots)$

$$
\int_ {0} ^ {\infty} x ^ {a} e ^ {- (r x) ^ {b}} d x = \frac {1}{b r ^ {a + 1}} \Gamma \left(\frac {a + 1}{b}\right) \quad (a + 1 > 0, r > 0, b > 0).
$$

30. $\int_0^\infty \frac{e^{-ax} - e^{-bx}}{x} dx = \ln \left(\frac{b}{a}\right).$

31. $\int_{0}^{\infty} e^{-ax} \sin(mx) dx = \frac{m}{a^2 + m^2} \quad (a > 0)$ .

32. $\int_0^\infty xe^{-ax}\sin (mx)dx = \frac{2am}{(a^2 + m^2)^2}\quad (a > 0).$

33. $\int_{0}^{\infty} x^{p-1} e^{-ax} \sin(mx) dx = \frac{\Gamma(p) \sin(p\theta)}{(a^2 + m^2)^{p/2}} (a > 0, p > 0, m > 0)$ , where $\sin(\theta) = m/r, \cos(\theta) = a/r, r = (a^2 + m^2)^{1/2}$ .

34. $\int_0^\infty e^{-ax}\cos (mx)dx = \frac{a}{a^2 + m^2}$ $(a > 0)$ .

35. $\int_{0}^{\infty} x e^{-ax} \cos(mx) dx = \frac{a^{2} - m^{2}}{(a^{2} + m^{2})^{2}} (a > 0)$ .

36. $\int_{0}^{\infty} x^{p-1} e^{-ax} \cos(mx) dx = \frac{\Gamma(p) \cos(p\theta)}{(a^2 + m^2)^{\rho/2}} \quad (a > 0, p > 0)$ , where $\theta$ is the same as given in Eq. (33).

37. $\int_{0}^{\infty}\frac{e^{-ax}}{x}\sin (mx)dx = \tan^{-1}\left(\frac{m}{a}\right)\quad (a > 0).$

38. $\int_{0}^{\infty}\frac{e^{-ax}}{x} [\cos (mx) - \cos (nx)]dx = \frac{1}{2}\ln \left(\frac{a^2 + n^2}{a^2 + m^2}\right)\quad (a > 0).$

39. $\int_{0}^{\infty} e^{-ax} \cos^{2}(mx) dx = \frac{a^{2} + 2m^{2}}{a(a^{2} + 4m^{2})} (a > 0)$ .

40. $\int_0^\infty e^{-ax}\sin^2 (mx)dx = \frac{2m^2}{a(a^2 + 4m^2)}\quad (a > 0).$

$$
\int_ {0} ^ {1} \left[ \ln \left(\frac {1}{x}\right) \right] ^ {q} d x = \Gamma (q + 1) \quad (q + 1 > 0). \tag {41.}
$$

$$
\int_ {0} ^ {1} x ^ {p} \ln \left(\frac {1}{x}\right) d x = \frac {1}{(p + 1) ^ {2}} \quad (p + 1 > 0). \tag {42.}
$$

$$
\int_ {0} ^ {1} x ^ {p} \left[ \ln \left(\frac {1}{x}\right) \right] ^ {q} d x = \frac {\Gamma (q + 1)}{(p + 1) ^ {q + 1}} \quad (p + 1 > 0, q + 1 > 0). \tag {43.}
$$

44. $\int_0^1\ln (1 - x)dx = -1.$

45. $\int_0^1 x\ln (1 - x)dx = \frac{-3}{4}.$

46. $\int_0^1\ln (1 + x)dx = 2\ln (2) - 1.$

47. $\int_{0}^{\infty} e^{-ax^2} \cos(kx) dx = \frac{\sqrt{\pi}}{2\sqrt{a}} e^{-k^2/(4a)}$ .

![[dec62a1331dfa154d8da84e2469f3cc4952fc9763c931fb9f4738e2b460f1a28.jpg]]

# Some Integrals with Exponentials in the Integrands: The Error Function

We begin with the integral

$$
\int_ {0} ^ {\infty} e ^ {- x ^ {2}} d x = 1.
$$

We compute the value of this integral by a trick, squaring the integral and changing variables:

$$
I ^ {2} = \left[ \int_ {0} ^ {\infty} e ^ {- x ^ {2}} d x \right] ^ {2} = \int_ {0} ^ {\infty} e ^ {- x ^ {2}} d x \int_ {0} ^ {\infty} e ^ {- y ^ {2}} d y = \int_ {0} ^ {\infty} \int_ {0} ^ {\infty} e ^ {- (x ^ {2} + y ^ {2})} d x d y.
$$

We now change to polar coordinates,

$$
\begin{array}{l} I ^ {2} = \int_ {0} ^ {\pi / 2} \int_ {0} ^ {\infty} e ^ {- \rho^ {2}} \rho d \rho d \phi = \frac {\pi}{2} \int_ {0} ^ {\infty} e ^ {- \rho^ {2}} \rho d \rho \\ = \frac {\pi}{2} \int_ {0} ^ {\infty} \frac {1}{2} e ^ {- z} d z = \frac {\pi}{4}. \end{array}
$$

Therefore,

$$
I = \int_ {0} ^ {\infty} e ^ {- x ^ {2}} d x = \frac {\sqrt {\pi}}{2}
$$

and

$$
\boxed {\int_ {0} ^ {\infty} e ^ {- a x ^ {2}} d x = \frac {1}{2} \sqrt {\frac {\pi}{a}}}\tag{A.1}
$$

Another trick can be used to obtain the integral,

$$
\int_ {0} ^ {\infty} x ^ {2 n} e ^ {- a x ^ {2}} d x,
$$

where $n$ is an integer. For $n = 1$ ,

$$
\begin{array}{r l} \int_ {0} ^ {\infty} x ^ {2} e ^ {- a x ^ {2}} d x & = - \int_ {0} ^ {\infty} \frac {d}{d a} \left[ e ^ {- a x ^ {2}} \right] d x = - \frac {d}{d a} \int_ {0} ^ {\infty} e ^ {- a x ^ {2}} d x \\ & = - \frac {d}{d a} \left[ \frac {1}{2} \sqrt {\frac {\pi}{a}} \right] = \frac {1}{4 a} \sqrt {\frac {\pi}{a}} = \frac {\pi^ {1 / 2}}{4 a ^ {3 / 2}}. \end{array}\tag{A.2}
$$

For $n$ an integer greater than unity,

$$
\int_ {0} ^ {\infty} x ^ {2 n} e ^ {- a x ^ {2}} d x = (- 1) ^ {n} - \frac {d ^ {n}}{d a ^ {n}} \left[ \frac {1}{2} \sqrt {\frac {\pi}{a}} \right].\tag{A.3}
$$

Equations (A.2) and (A.3) depend on the interchange of the order of differentiation and integration. This can be done if an improper integral is uniformly convergent. The integral in Eq. (A.1) is uniformly convergent for all real values of a greater than zero. Similar integrals with odd powers of x are easier. By the method of substitution,

$$
\int_ {0} ^ {\infty} x e ^ {- a x ^ {2}} d x = \frac {1}{2 a} \int_ {0} ^ {\infty} e ^ {- y} d y = \frac {1}{2 a}.\tag{A.4}
$$

We can apply the trick of differentiating under the integral sign just as in Eq. (A.3) to obtain

$$
\int_ {0} ^ {\infty} x ^ {2 n + 1} e ^ {- a x ^ {2}} d x = (- 1) ^ {n} \frac {d ^ {n}}{d a ^ {n}} \left(\frac {1}{2 a}\right).\tag{A.5}
$$

The integrals with odd powers of x are related to the gamma function, defined in Appendix G. For example,

$$
\int_ {0} ^ {\infty} x ^ {2 n + 1} e ^ {- x ^ {2}} d x = \frac {1}{2} \int_ {0} ^ {\infty} y ^ {n} e ^ {- y} d y = \frac {1}{2} \Gamma (n + 1).\tag{A.6}
$$

## The Error Function

The indefinite integral

$$
\int e ^ {- x ^ {2}} d x
$$

has never been expressed as a closed form (a formula not involving an infinite series or something equivalent). The definite integral for limits other than 0 and $\infty$ is not obtainable in closed form. Because of the frequent occurrence of such definite integrals, tables of numerical approximations have been generated. $^{1}$ One form in which the tabulation is done is as the error function, denoted by $\operatorname{erf}(x)$ and defined by

$$
\operatorname{erf} (x) = \frac {2}{\sqrt {\pi}} \int_ {0} ^ {\infty} e ^ {- t ^ {2}} d t.
$$

As you can see from Eq. (A.1),

$$
\lim _ {x \to \infty} \operatorname{erf} (x) = 1.
$$

The name “error function” is chosen because of its frequent use in probability calculations involving the Gaussian probability distribution. Another form giving the same information is the normal probability integral $^{2}$

$$
\frac {1}{\sqrt {2 \pi}} \int_ {- x} ^ {x} e ^ {- t ^ {2} / 2} d t.
$$

Values of the Error Function

$$
\operatorname{erf} (x) = \frac {2}{\sqrt {\pi}} \int_ {0} ^ {x} e ^ {- t ^ {2}} d t ^ {*}
$$

<table><tr><td>x</td><td></td><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td></tr><tr><td>0.0</td><td>0.0</td><td>000</td><td>113</td><td>226</td><td>338</td><td>451</td><td>564</td><td>676</td><td>789</td><td>901</td><td>*013</td></tr><tr><td>0.1</td><td>0.1</td><td>125</td><td>236</td><td>348</td><td>459</td><td>569</td><td>680</td><td>790</td><td>900</td><td>*009</td><td>*118</td></tr><tr><td>0.2</td><td>0.2</td><td>227</td><td>335</td><td>443</td><td>550</td><td>657</td><td>763</td><td>869</td><td>974</td><td>*079</td><td>*183</td></tr><tr><td>0.3</td><td>0.3</td><td>286</td><td>389</td><td>491</td><td>593</td><td>694</td><td>794</td><td>893</td><td>992</td><td>*090</td><td>*187</td></tr><tr><td>0.4</td><td>0.4</td><td>284</td><td>380</td><td>475</td><td>569</td><td>662</td><td>755</td><td>847</td><td>937</td><td>*027</td><td>*117</td></tr><tr><td>0.5</td><td>0.5</td><td>205</td><td>292</td><td>379</td><td>465</td><td>549</td><td>633</td><td>716</td><td>798</td><td>879</td><td>959</td></tr><tr><td>0.6</td><td>0.6</td><td>039</td><td>117</td><td>194</td><td>270</td><td>346</td><td>420</td><td>494</td><td>566</td><td>638</td><td>708</td></tr><tr><td>0.7</td><td></td><td>778</td><td>847</td><td>914</td><td>981</td><td>*047</td><td>*112</td><td>*175</td><td>*238</td><td>*300</td><td>*361</td></tr><tr><td>0.8</td><td>0.7</td><td>421</td><td>480</td><td>538</td><td>595</td><td>651</td><td>707</td><td>761</td><td>814</td><td>867</td><td>918</td></tr><tr><td>0.9</td><td></td><td>969</td><td>*019</td><td>*068</td><td>*116</td><td>*163</td><td>*209</td><td>*254</td><td>*299</td><td>*342</td><td>*385</td></tr><tr><td>1.0</td><td>0.8</td><td>427</td><td>468</td><td>508</td><td>548</td><td>586</td><td>624</td><td>661</td><td>698</td><td>733</td><td>768</td></tr><tr><td>1.1</td><td></td><td>802</td><td>835</td><td>868</td><td>900</td><td>931</td><td>961</td><td>991</td><td>*020</td><td>*048</td><td>*076</td></tr><tr><td>1.2</td><td>0.9</td><td>103</td><td>130</td><td>155</td><td>181</td><td>205</td><td>229</td><td>252</td><td>275</td><td>297</td><td>319</td></tr><tr><td>1.3</td><td></td><td>340</td><td>361</td><td>381</td><td>400</td><td>419</td><td>438</td><td>456</td><td>473</td><td>490</td><td>507</td></tr><tr><td>1.4</td><td>0.95</td><td>23</td><td>39</td><td>54</td><td>69</td><td>83</td><td>97</td><td>*11</td><td>*24</td><td>*37</td><td>*49</td></tr><tr><td>1.5</td><td>0.96</td><td>61</td><td>73</td><td>84</td><td>95</td><td>*06</td><td>*16</td><td>*26</td><td>*36</td><td>*45</td><td>*55</td></tr><tr><td>1.6</td><td>0.97</td><td>63</td><td>72</td><td>80</td><td>88</td><td>96</td><td>*04</td><td>*11</td><td>*18</td><td>*25</td><td>*32</td></tr><tr><td colspan="12">Continued on next page</td></tr><tr><td>1.7</td><td>0.98</td><td>38</td><td>44</td><td>50</td><td>56</td><td>61</td><td>67</td><td>72</td><td>77</td><td>82</td><td>86</td></tr><tr><td>1.8</td><td></td><td>91</td><td>95</td><td>99</td><td>*03</td><td>*07</td><td>*11</td><td>*15</td><td>*18</td><td>*22</td><td>*25</td></tr><tr><td>1.9</td><td>0.99</td><td>28</td><td>31</td><td>34</td><td>37</td><td>39</td><td>42</td><td>44</td><td>47</td><td>49</td><td>51</td></tr><tr><td>2.0</td><td>0.995</td><td>32</td><td>52</td><td>72</td><td>91</td><td>*09</td><td>*26</td><td>*42</td><td>*58</td><td>*73</td><td>*88</td></tr><tr><td>2.1</td><td>0.997</td><td>02</td><td>15</td><td>28</td><td>41</td><td>53</td><td>64</td><td>75</td><td>85</td><td>95</td><td>*05</td></tr><tr><td>2.2</td><td>0.998</td><td>14</td><td>22</td><td>31</td><td>39</td><td>46</td><td>54</td><td>61</td><td>67</td><td>74</td><td>80</td></tr><tr><td>2.3</td><td></td><td>86</td><td>91</td><td>97</td><td>*02</td><td>*06</td><td>*11</td><td>*15</td><td>*20</td><td>*24</td><td>*28</td></tr><tr><td>2.4</td><td>0.999</td><td>31</td><td>35</td><td>38</td><td>41</td><td>44</td><td>47</td><td>50</td><td>52</td><td>55</td><td>57</td></tr><tr><td>2.5</td><td></td><td>59</td><td>61</td><td>63</td><td>65</td><td>67</td><td>69</td><td>71</td><td>72</td><td>74</td><td>75</td></tr><tr><td>2.6</td><td></td><td>76</td><td>78</td><td>79</td><td>80</td><td>81</td><td>82</td><td>83</td><td>84</td><td>85</td><td>86</td></tr><tr><td>2.7</td><td></td><td>87</td><td>87</td><td>88</td><td>89</td><td>89</td><td>90</td><td>91</td><td>91</td><td>92</td><td>92</td></tr><tr><td>2.8</td><td>0.9999</td><td>25</td><td>29</td><td>33</td><td>37</td><td>41</td><td>44</td><td>48</td><td>51</td><td>54</td><td>56</td></tr><tr><td>2.9</td><td></td><td>59</td><td>61</td><td>64</td><td>66</td><td>68</td><td>70</td><td>72</td><td>73</td><td>75</td><td>77</td></tr></table>

\* From Eugene Jahnke and Fritz Emde, Tables of Functions, Dover Publications, New York, 1945, p. 24.

To use this table, obtain the first digits of $\text{erf}(x)$ from column 2 and the remaining digits from the appropriate column. Entries marked with \* correspond to the value in the next lower row of column 2.

## Index

abelian group, 294  
abscissa, 93  
absolute address in Excel, 66  
absolute maximum, 111  
absolute value of a complex number, 47  
of a scalar quantity, 6  
absorbance, 359  
absorptivity, 359  
acceleration, 122  
acceleration due to gravity, 123  
accuracy, 319  
addition of vectors, 33  
algebra, 22, 52  
matrix, 282  
operator, 271  
algebraic irrational number, 7  
algebraic irrational numbers, 2  
algorithm, 52  
ammonia molecule, 294  
amplitude, 256  
analytic function, 166  
antiderivative, 123  
antilogarithm, 8  
antisymmetric, 291  
arcsine function, 30  
Argand diagram, 46  
Argand plane, 46  
argument of a complex number, 47  
assignment operator, 74  
associative, 5, 45, 271, 284  
atmosphere (unit of pressure), 13  
augmented matrix, 310  
average mean, 145 median, 145 mode, 145 Avogadro's constant, 4

bar-graph approximation, 142  
base of logarithms, 7  
base of natural logarithms, e, 3  
basis functions, 165  
basis of a representation of a group, 298  
beating, 249  
bell-curve, 96  
binomial distribution, 323  
Bohr radius, 55, 119, 280  
Born-Oppenheimer approximation, 281  
Bouger-Beer law, 359  
boundary conditions, 240, 256

Cartesian components, 32, 38  
Cartesian coordinates, 32, 37  
cells in Mathematica, 72  
Celsius temperature scale, 13  
central limit theorem, 323  
chain rule, 105, 201, 373  
change of variables, 136  
changing variables in multiple integrals, 214  
character, 299  
characteristic equation, 239  
circular frequency, 242  
circular trigonometric functions, 24  
Clapeyron equation, 333  
classical mechanics, 123, 237  
Clausius-Clapeyron equation, 337  
closed system, 193  
coefficients of a series, 165  
cofactor, 290  
colligative properties, 171  
column vector, 282  
column vectors, 297, 306  
common logarithms, 7  
commutative, 5, 45, 272, 284  
commutator, 272  
commute, 7  
complementary equation, 247  
complementary function, 247  
completeness, 173, 177  
complex conjugate, 177  
complex conjugate of a complex number, 48  
complex number, 45  
absolute value, 47  
cube root, 51  
magnitude, 47  
modulus, 47  
phase or argument, 47  
polar representation, 47  
complex numbers, 3  
complex plane, 46  
components, 32  
Cartesian, 38  
composite function, 105  
confidence interval, 325  
confidence level, 325  
conservation of energy, 243  
conservative system, 243  
constant of integration, 133  
constrained maximum, 227  
constrained minimum, 227  
constraint, 227  
constructive interference, 258  
continuity, 191

continuous function, 91  
convergence  
in an interval, 165  
of a power series, 169  
of a series, 160  
of an improper integral, 135  
uniform, 165  
convergence of a series  
tests for, 163  
conversion factor, 17  
convolution theorem, 181  
coordinates  
Cartesian, 37  
orthogonal, 221  
plane polar, 32  
correlation coefficient, 343  
covariance, 344, 347  
Cramer's rule, 340  
critical damping, 245  
cross product of two vectors, 42  
cube root, 6  
cube root of a complex number, 51  
cubic equation, 58  
curl, 220  
in orthogonal coordinates, 224  
curl of the gradient, 221  
curvature of a function, 110  
curve fitting  
numerical, 339  
cusp, 100  
cycle rule, 200  
cyclic process, 210  
cylindrical polar coordinates, 40  

damped harmonic oscillator, 243  
damping  
critical, 245  
greater than critical, 244  
less than critical, 244  
data reduction, 318, 329  
definite integral, 126, 133  
degree (measure of an angle), 25  
degree of a polynomial equation, 58  
degrees of freedom, 324  
del, 218 $\nabla$ , 218  
DeMoivre's formula, 47  
dependent variable, 25, 90  
derivative, 99, 108  
higher-order, 108  
partial, 193  
derivative identities, 104  
derivative operators, 270  
Descartes, Rene duPerron, 32  
destructive interference, 258  
determinant, 216  
Slater, 292  
triangular, 291  
determinant properties, 290  
determinants, 289  
diagonal elements of a matrix, 285  
diagonal matrix, 288  
Dieterici equation of state, 63, 88  
difference, 94 $\Delta$ , symbol for, 94  
difference of two operators, 271  
differentiability, 100

differential, 103, 194
exact, 202
inexact, 202
differential equation, 235
differential equations
partial, 253
dimension of a representation of a group, 298
direct sum, 299
discontinuities, 92
discordant data, 328
discriminant, 59
distribution function, 147
distributive, 5, 45, 272, 284
div (divergence operator), 219
divergence, 219
in orthogonal coordinates, 223
of a series, 160
of an improper integral, 135
dot product, 35
double equal sign in Mathematica, 77
double integral, 210
as a volume, 211

e, base of natural logarithms, 8
eigenfunction, 270
eigenfunctions, 177
of symmetry operators, 281
eigenvalue, 270, 281, 311
eigenvalue equation, 270
eigenvector, 311
electric field, 44
enantiomorphs, 118
English units of measurement, 13
entropy
absolute, 156
equation
operator, 271
equation of continuity, 219
equation of motion, 237
equations of motion, 235
equilibrium thermodynamic state, 210
error function, 150, 385
error propagation
in least squares, 344
estimated error, 325
Euler reciprocity relation, 199, 203, 251
Euler's formula, 47
Euler's method, 260
Euler, Leonhard, 9
even function, 26, 131
exact differential, 202, 251
exact differential equation, 251
Excel spreadsheet, 65
expand, 166
expanding by minors, 289
expectation value, 301
exponent, 6
exponential, 10
extremum, 110, 224

factor-label method, 17
factorial, 63, 102
faithful representation of a group, 298
Faltung theorem, 181
family of functions, 93, 240
fast Fourier transform, 182
finite series, 159
first difference, 335

first maxim of computing, 108, 350  
first-order chemical reaction, 250  
flexible string, 254  
force on a charged object, 44  
formal solution, 260  
Fourier cosine series, 175  
Fourier cosine transform, 181  
Fourier integral, 180  
Fourier series, 172  
with complex basis functions, 177  
Fourier sine series, 175  
Fourier sine transform, 181  
Fourier transforms, 180  
Fourier, Jean Baptiste Joseph, 172  
free induction decay, 182  
frequency, 242, 257  
friction constant, 243  
function, 25, 90  
analytic, 166  
function of several variables, 190  
functional, 127  
functional series, 165  
functions  
basis, 165  
periodic, 172  
fundamental, 257  
fundamental equation of differential calculus, 194-331  
fundamental theorem of integral calculus, 126  

Galton, Sir Francis, 339  
gamma function, 379  
gas kinetic theory, 146  
Gauss elimination, 310  
Gauss quadrature, 144  
Gauss, Karl Friedrich, 96  
Gauss-Jordan elimination, 285  
Gaussian distribution, 149  
Gaussian functions, 96  
gaussian probability distribution, 323  
general solution to a differential equation, 240  
geometric series, 161  
Gibbs phenomenon, 176  
Gibbs, Josiah Willard, 176  
Goal Seek command in Excel, 78  
Gossett, William Sealy, 326  
grad (gradient operator), 218  
grad (measure of an angle), 25  
gradient, 217  
in orthogonal coordinates, 222  
gradient of the divergence, 221  
graphical method for solving an equation, 64  
graphical representation of functions, 93  
Gregory-Newton interpolation formula, 335  
group, 294  

half-life, 11  
half-time, 11  
Hamiltonian operator, 281  
harmonic oscillator, 238  
harmonic oscillators, 115  
harmonic series, 163  
harmonics, 257  
hermitian conjugate, 288  
hermitian matrix, 288  
homogeneous linear differential equation, 238  
homogeneous linear equations, 83

homomorphic representation of a group, 298
Hooke, Robert, 238
hyperbolic trigonometric functions, 30

ideal gas, 52, 194
ideal gas constant, 19, 52
ideal gas equation, 191, 194
identities for partial derivatives, 198
identity, 6, 25
identity operator, 271, 275
imaginary axis, 46
imaginary numbers, 3
imaginary part of a complex number, 3, 45
imaginary unit, 44
imaginary unit, i, 3
improper integral, 134
convergence, 135
divergence, 135
improper rotation, 277
inconsistent equations, 81
indefinite integral, 126, 133
independent equations, 81
independent variable, 25, 90
inexact differential, 202
inexact pfaffian differential equation, 252
infinite series, 159
infinity, 29
inflection point, 99, 111
inhomogeneous equation, 247
inhomogeneous simultaneous equations, 79
inhomogeneous term, 247
initial conditions, 240, 241, 256
integers, 2
integral
definite, 126
improper, 134
indefinite, 126
line, 206
path, 206
trapezoidal approximation, 142
integral calculus
fundamental theorem of, 126
f, 126
integral sign, 126
integral transform, 180
integrals
multiple, 210
integrand, 126
integrating factor, 205, 252
integration by parts, 137
integration, numerical, 141
intercept, 94
interference, 172, 258
interferometer, 182
interval of convergence, 169
inverse of a matrix, 285
inverse of an operator, 273
inverse sine function, 30
inverse trigonometric functions, 29
inversion operator, 275
irrational number, 2
algebraic, 7
transcendental, 7
irreducible representation of a group, 298
isomorphic representation of a group, 298
iterative procedure, 106

jacobian, 216

kinetic energy, 242
Kronecker delta, 173, 285

L'Hôpital, rule of, 114
Lagrange, Joesph Louis, 228
Lambert-Beer law, 359
Laplace transform, 182
    use to solve a differential equation, 258
Laplace, Pierre Simon, 182
laplacian, 220
least squares, 339
    with weighting factors, 350
least-squares fit
    with Excel, 348
left-handed coordinate system, 37
limit, 27
limits of integration, 126
limits, mathematical, 113
line integral, 206
linear combination, 238, 258, 323
linear dependence, 83, 246, 308
linear differential equation, 238
linear equation, 58
linear function, 94
linear functions, 340
linear least squares, 340
    with fixed slope or intercept, 353
linear regression, 340
linear simultaneous equations, 79
linearization, 63, 337, 340
local maximum, 111, 225
local minimum, 111, 225
logarithms, 7
logarithms, natural, 9
Lorentzian distribution, 323 $\nabla^{2}$ , 220

Maclaurin series, 166
magnetic induction (magnetic field), 44
magnitude, 22
    of a complex number, 47
    of a scalar quantity, 6
    of a vector
    three-dimensional, 38
magnitude of a vector, 32
Mathematica, 71
Mathematica statements
    Apart, 76
    Clear, 74
    Eliminate, 84, 314
    Expand, 75
    Factor, 75
    FindRoot, 77
    NSolve, 77
    Simplify, 75
    Solve, 77
    Together, 76
mathematical function, 25
mathematical identity, 6, 25
mathematical limit, 27
mathematical operations on series, 178
mathematical operator, 269
matrix, 282
    adjoint, 288
    associate, 288
    block-diagonal, 299
    diagonal, 288

hermitian, 288  
inverse, 285  
nonsingular, 309  
orthogonal, 288  
singular, 288  
transpose, 288  
triangular, 288  
unitary, 288  
matrix algebra, 282  
matrix eigenvalue problem, 311  
matrix elements, 282  
matrix multiplication, 283  
maximum  
constrained, 227  
local, 225  
relative, 225  
maximum or minimum value of a function of several variables, 224  
maximum value of a function, 110  
Maxwell relations, 200  
mean, 322, 324  
mean (type of average), 145  
mean value, 322  
mean value theorem, 153  
measure of an angle, 25  
mechanics  
classical, 237  
quantum, 177  
median, 324  
median (type of average), 145  
method of substitution, 136  
minimum  
constrained, 227  
local, 225  
minimum value of a function, 110  
minors  
expanding by, 289  
mixed second partial derivatives, 199  
MKS system of units, 11  
mode, 324  
mode (type of average), 145  
model system, 238, 254  
modulus of a complex number, 47  
molar concentrations, 59  
moment of a probability distribution, 357  
moment of inertia, 233  
multiple integral, 210  
multiplication operators, 270  
multiplier undetermined, 228

Napier, John, 9  
natural logarithms, 9  
Newton's laws of motion, 237  
Newton's method, 106  
Newton's second law of motion, 235  
Newton, Sir Isaac, 237  
Newton-Raphson method, 106  
Newtonian mechanics, 123  
nodes, 257  
nonequivalent representations of a group, 299  
normal distribution, 149, 323  
normal probability integral, 385  
normalization, 96, 146, 147, 177, 214, 322  
notebook in Mathematica, 71  
null (zero) matrix, 288  
null operator, 272

null vector, 42
numerical integration, 141

octant, 37
odd function, 26, 131
one-to-one correspondence, 297
operator, 217
assignment, 74
mathematical, 269
operator algebra, 271
operator equation, 271
operators
difference, 271
inverse, 273
inversion, 275
powers of, 273
product of, 271
quantum mechanical, 177, 274
reflection, 276
rotation, 276
sum of, 271

orbital, 119
orbitals, 292
order
of a chemical reaction rate, 342
of a differential equation, 238
of a group, 298
of a rate law, 140
ordered pairs, 90
ordinary differential equation, 238
ordinary differential equations, 253
ordinate, 93
Origin, 31
orthogonal coordinates, 221
orthogonal matrix, 288
orthogonality, 173, 177
orthogonality of vectors, 35
overdetermined system of equations, 306
overtones, 257

panel, 142
parabola, 95
parallax, 320
parameters, 23, 93
partial derivative, 193
partial differential equations, 253
partial fractions, 76, 138
partial integration, 137
partial sum, 159
particular solution, 240
partition function, 162
path integral, 206
path-independent, 207
Pauli exclusion principle, 292
Pauli, Wolfgang, 292
period, 241, 257
periodic functions, 26, 172
perturbation method, 166
pfaffian form, 202, 251
phase of a complex number, 47
pi, π, 2
piecewise continuous, 92
pivot element, 287
planimeter, 129
point group, 296
point symmetry operators, 275, 296
Poisson distribution, 323

polar coordinates, 32, 214  
cylindrical, 40  
spherical, 39  

polar representation of a complex number, 47  
polynomial, 94  

polynomial equation, 58  
degree, 58  

polynomials, 138  

population, 148, 322  

position vector, 32, 38, 122  

potential energy, 243  

power series, 166  

powers, 6  

powers of an operator, 273  

precision, 319  

pressure virial equation of state, 171  

principal values, 30  

probability, 145  

probability density, 147, 322  

probability distribution, 147, 322  

probable error, 325  

problem solving, 52  

product  
of a matrix and a scalar, 283  
of a scalar and a vector, 35, 41  
of two matrices, 283  
of two operators, 271  

projection, 39  

propagation of errors, 329, 331  

proper rotation, 277  

Pythagoras, theorem of, 27  
three-dimensional, 38  

Q test, 329  

quadratic equation, 58  

quadratic formula, 59  

quadratic function, 95  

quantum mechanics, 220, 254  
operators, 274  

quartic equation, 58  

radian (measure of an angle), 25  
radiant spectral emittance, 112  
radioactive decay, 104  
radius of convergence, 169  
random errors, 319  
random variables, 323  

Rankine temperature scale, 19  
rate constant, 140, 250, 336  
rate law, 140  
order, 140  

rational numbers, 2  
real axis, 46  
real numbers, 2, 22  
real part of a complex number, 3, 45  
real variables, 22  
reciprocal identity, 198  
reciprocal of a complex number, 45  
reducible representation of a group, 298  
reflection operator, 276  
regression, 339  
relative address in Excel, 66  
relative maximum, 111, 225  
relative minimum, 111  
relativity, 151  
relaxation time, 11  
replacement operator in Mathematica, 263  
representation of a function, 91

representation of a group, 296, 298  
residuals, 339  
reversible process, 210  
right triangle, 24  
right-hand rule, 42  
right-handed coordinate system, 37  
root-mean-square (rms), 146  
roots, 6  
roots to an equation, 58  
rot (curl operator), 220  
rotation  
improper, 277  
proper, 276  
rotation operators, 276  
round-off error, 16  
row operation, 286  
row operations, 310  
row vector, 282  
rules  
for integrals, 129  
for significant digits, 15  
Runge-Kutta method, 261  

saddle point, 226  
sample, 322  
scalar product  
of two functions, 173, 177  
scalar product of two vectors, 35, 41  
scalars, 3, 22, 282  
Schoenflies symbol, 296  
scientific notation, 4  
second difference, 335  
second partial derivatives, 199  
second-order chemical reaction, 250  
second-order reaction, 343  
secular equation, 313, 317  
separation of variables, 249, 255  
sequence, 159  
series, 159  
constant, 159  
Fourier, 172  
functional, 165  
geometric, 161  
Maclaurin, 166  
mathematical operations on, 178  
power, 166  

shifting theorem, 183  
SI, System of International Units, 11  
sign (positive or negative), 22  
significant digits, 3  
similarity transformation, 298  
Simpson's five-eighths rule, 143  
Simpson's one-third rule, 143  
Simpson's rule, 143  
single-valued, 91  
singular matrix, 288  
Slater determinant, 292  
slope, 94  
smoothed data, 335  
solute, 172  
solution  
general, 240  
of a differential equation, 236  
particular, 240  
solutions to an equation, 58  
specific heat capacity, 20  
spherical polar coordinates, 39

spreadsheet, 65  
spring constant, 238  
square integrable, 181  
square matrix, 282  
square root, 6  
square root of a complex number, 51  
standard deviation, 96, 148, 322  
of a sample, 324  
standard normal distribution, 149  
standing wave, 257  
state functions, 204  
statistical mechanics, 115, 162, 356  
stiff differential equations, 261  
stoichiometric concentration, 59, 80  
stream lines, 219  
Student (pseudonym for William Sealy Gossett), 326  
Student t factor, 326  
Student's t distribution, 326  
substitution, method of, 136  
successive approximations, 62 $\Sigma$ , 125  
sum, 125  
partial, 159  
sum of two matrices, 282  
sum of two operators, 271  
summation index, 125  
superposition, 258  
symbolic mathematics, 22  
symmetric matrix, 288  
symmetry element, 276  
symmetry operators, 270, 275  
operation on functions, 279  
System of International Units  
base units, 12  
overview, 11  
systematic errors, 319  

tangent to a curve, 98  
Taylor series, 166  
tesla, 44  
Tesla, Nikola, 44  
third derivative, 108  
third difference, 335  
third-order reaction, 342, 343  
torr (unit of pressure), 13  
totally symmetric representation of a group, 299  
trace (spur) of a matrix, 288  
transcendental equations, 60  
transcendental irrational numbers, 2, 7  
transform  
Fourier, 180  
integral, 180  
Laplace, 182  
transformation of coordinates, 33, 39  
transition-state theory, 226  
transpose of a matrix, 288  
traveling wave, 258  
trial solution, 239, 255  
trial value, 77  
triangular determinant, 291  
triangular matrix, 288  
trigonometric functions, 24  
hyperbolic, 30  
inverse, 29  
properties, 28  
triple integral, 213

## Index

trivial solution, 83, 311
two-dimensional vector, 32

undefined, 29  
undetermined multiplier, 228  
unfaithful representation of a group, 298  
uniform convergence, 165, 179  
uniform harmonic motion, 241  
unit vectors, 35, 38  
unitary matrix, 288

van der Waals equation of state, 20, 23, 120, 156  
variable  
    dependent, 25  
    independent, 25  
variable-change identity, 198  
variables in Mathematica, 74  
variance, 324  
variation of parameters, 248  
vector, 22, 31  
    magnitude, 32

null, 42  
position, 32, 38  
scalar product, 35  
three-dimensional, 39  
two-dimensional, 32  
unit, 35, 38  
vector addition, 33  
vector derivative operators, 217  
vector derivatives  
in other coordinate systems, 221  
vector product of two vectors, 42  
velocity, 122  
virial coefficients, 170, 231  
virial equation of state, 170  
virial series, 170  
vorticity, 220

wavelength, 257
weak acid, 59
weighting factors, 351
weighting function, 153