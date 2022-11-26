# Praktikum-2-KOMNUM

### Question

Salah satu kelemahan dari metode Trapezoidal adalah kita harus menggunakan jumlah interval yang besar untuk memperoleh akurasi yang diharapkan. Buatlah sebuah program komputer untuk menjelaskan bagaimana metode Integrasi Romberg dapat mengatasi kelemahan tersebut.

### Trapezoidal rule

Trapezoidal Rule is a rule that evaluates the area under the curves by dividing the total area into smaller trapezoids rather than using rectangles. This integration works by approximating the region under the graph of a function as a trapezoid, and it calculates the area. This rule takes the average of the left and the right sum.

##### Trapezoidal Rule Formula 
Let f(x) be a continuous function on the interval [a, b]. Now divide the intervals [a, b] into n equal subintervals with each of width,  
$\Delta x = \frac{b - a}{n}$ Such that, $a = x_0 < x_1 < x_2 < x_3 < . . . < x_n = b$

Then the Trapezoidal Rule formula for area approximating the definite integral $∫_a^b f(x)dx$ is given by:       

$$∫_a^b f(x)dx \approx Tn = \frac{\Delta x}{2} [f(x_0) + 2f(x_1) + 2f(x_2) + … + 2f(x_{n − 1}) + f(x_n)]$$

Where, $x_i = a+iΔx$
If $n \to \infty$, R.H.S of the expression approaches the definite integral $∫_a^b f(x)dx$.

### Richardson Extrapolation

Richardson Extrapolation is a method for boosting the accuracy of certain numerical procedures. This one does the elimination of errors. Though it can only remove errors of the form:

$$E(h) = Ch^p$$

where $C$ a constant and $p$ is the exponent of the error term

### Romberg Integration

Romberg intergation combines the Composite Trapezoidal Rule with Richardson Extrapolation.

Below is the overview of the integration process:
Let $R_{i-1} = I_i$

1. Starts with the computation of one panel and two panels via Composite Trapezoidal Rule

$$ 
    \begin{align*}
    R_{1,1} = I_1 \\
    R_{2,1} = I_2 
    \end{align*} 
$$
    
2. We get the leading error term $C_1h^2$ then eliminate by Richardson Extrapolation using p = 2 
    (since that is the exponent of the error)

$$ 
    \begin{align*}
    R_{2,2} &= \frac{2^2 R_{2,1} - R_{1,1}}{2^2-1}\\
    &= \frac{4}{3} R_{2,1} - \frac{1}{3} R_{1,1} 
    \end{align*}
$$

3. Get the leading error term $C_2h^4$ then eliminate by
Richardson Extrapolation using p = 4

4. We do this until it converges to the wanted solution

this is exactly what we are doing

$$ 
    \begin{align*}
    &R_{1,1} \\
    & \text{ $ $ $ $ $ $ $ $ $ $ $ $ $\searrow$} \\
    &R_{2,1} \rightarrow R_{2,2} \\
    &\text{ $ $ $ $ $ $ $ $ $ $ $ $ $\searrow$ $ $ $ $ $ $ $ $ $ $ $ $ $\searrow$} \\
    &R_{3,1} \rightarrow R_{3,2} \rightarrow R_{3,3} \\
    &\text{ $ $ $ $ $\vdots$ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $\vdots$
    $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $\vdots$ $ $ $ $ $ $ $\ddots$} \\
    &R_{n,1} \rightarrow R_{n,2} \rightarrow R_{n,3} \cdots R_{n,n}\\
    \end{align*}
$$

This tells us that we need to compute where the two arrows are from to compute where the two arrows are pointing at. The most accurate estimate of the integral is always the last diagonal term of the array. This process is continued until the difference between two successive diagonal terms becomes sufficiently small.

The overview above can be summarized into the formula:

$$ 
    \begin{align*}
    R_{i,j} = R_{i,j} &= CTR(h_i) &: \text{if i = 1} \\
    R_{i,j} &= \frac{4^{j-1} R_{i, j-1} - R_{i-1, j-1}}{4^{j-1} - 1} &: \text{if i>1}
    \end{align*}
$$

\*note: $h = \frac{b - a}{2^{i-1}}$ ; CTR means Composite Trapezoidal Rule

### Impementatation in Python

main function

    def main():
        a = 0       # lower boundary
        b = math.pi # upper boundary
        iter = 4    # number of iteration

        result = romberg(a, b, iter)
        print("R({},{}) = {}".format(iter, iter, result))

    if __name__ == "__main__":
        main()

Romberg function
    
    def romberg(a, b, iter):
        matrix = [] # matrix to store the romberg value
        # making empty 4 by 4 matrix
        for _ in range(0, iter): 
            matrix.append([None for _ in range(0, iter)])
        
        section = 1 # the number of section for CTR
        iteration = 0 # iteration of the while loop

        while (section < 2**iter):

            # getting the evenly spread points
            points = np.linspace(a, b, section + 1) 
            matrix[iteration][0] = CTR(points) 

            section *= 2 # increment the section by times 2
            iteration += 1 # increment the iteration by 1

        # calculating Romberg Integration 
        for i in range(1, iter):
            for j in range(1, iter):
                if (i < j):
                    continue
                # Romberg formula
                temp = (4**(j) * matrix[i][j - 1] - matrix[i - 1][j - 1]) / (4**(j) - 1)
                matrix[i][j] = temp

        return matrix[iter - 1][iter - 1]


CTR function

    def CTR(points: np.ndarray) -> float:
        h = points[1] - points[0]
        if(points.size < 2): 
            return -1
        else:
            temp = 0
            for i in range(1, points.size - 1):
                temp += f(points[i])
            return h / 2 * (f(points[0]) + 2 * temp + f(points[points.size - 1]))

Integration tested

$$\int_0^4 \sin{x} dx$$

    def f(x):
        return math.sin(x)

output:

    R(4,4) = 2.0000055499796705

