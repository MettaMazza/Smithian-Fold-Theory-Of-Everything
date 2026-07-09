

## Chapter 2: The Walsh Spectral Instrument and the Hidden Symmetry

### The Search for Order in Random Tensors

To understand how Maria Smith and her team discovered the mathematical law of the fold inside modern artificial intelligence, we have to look at what is actually inside a neural network's weights.

If you write a simple Python script to initialize a neural network before training, the weights look like static noise. Typically, they are drawn from a normal distribution—a Gaussian bell curve—designed to prevent the signals from blowing up or dying out as they pass through the layers. This is known as Xavier or He initialization. If you plot these weights, they look like a smooth, random distribution.

When you train that network on trillions of tokens, the weights shift. They group together, form patterns, and align to minimize the prediction error. To the naked eye, a trained weight matrix still looks like a chaotic array of floating-point numbers. But in 2026, the Ernos Labs team realized that this chaos was an illusion. They decided to change the mathematical lens through which they viewed the weights.

They developed a pre-registered, self-certifying spectral instrument. Instead of analyzing the weights in their native real-number coordinate space, they projected them into the **Walsh-Hadamard basis**.

The Walsh-Hadamard transform (WHT) is a discrete mathematical operation. Unlike the Fourier transform, which decomposes a signal into smooth sinusoidal waves, the Walsh transform decomposes data into square, binary waves that take values of only $+1$ and $-1$. It measures dyadic symmetry—how information blocks align under powers of two.

### The Mathematics of the Walsh-Hadamard Basis

Let us define the transformation formally. The Walsh-Hadamard matrix $H_n$ is a $2^n \times 2^n$ matrix with entries in $\{+1, -1\}$. It can be defined recursively starting from $H_0 = (1)$ by the relation:

$$H_k = H_{1} \otimes H_{k-1} = \begin{pmatrix} H_{k-1} & H_{k-1} \\ H_{k-1} & -H_{k-1} \end{pmatrix}$$

where $\otimes$ denotes the Kronecker product. 

Let us write out the first few matrices explicitly to see the pattern. For $H_1$, we have:

$$H_1 = \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$$

And for $H_2$, the matrix is:

$$H_2 = \begin{pmatrix} 1 & 1 & 1 & 1 \\ 1 & -1 & 1 & -1 \\ 1 & 1 & -1 & -1 \\ 1 & -1 & -1 & 1 \end{pmatrix}$$

For any integer $n$, the rows of $H_n$ form an orthogonal basis for $\mathbb{R}^{2^n}$. This means that any vector $x \in \mathbb{R}^{2^n}$ can be uniquely written as a linear combination of the rows of $H_n$. 

To apply this to a weight matrix $W$ of a neural network, the instrument takes a tensor row $w$, truncates it to the largest power of two, and computes the Walsh-Hadamard coefficients:

$$v = \frac{1}{\sqrt{N}} H_n w$$

where $N = 2^n$. The division by $\sqrt{N}$ ensures that the transformation is orthonormal, preserving the total energy (or variance) of the vector.

To measure how concentrated the energy is, the instrument calculates the fraction of total energy contained in the top $K$ coordinates of $v$. We pre-registered three fixed fractions of the coordinate space:
1. $6.1 \times 10^{-5}$ (the top 0.006%)
2. $4.9 \times 10^{-4}$ (the top 0.05%)
3. $3.9 \times 10^{-3}$ (the top 0.4%)

The spectral concentration ratio is defined as:

$$\text{Concentration Ratio} = \frac{\sum_{i \in \text{Top } K} v_i^2}{\frac{K}{N} \sum_{j=0}^{N-1} v_j^2}$$

If the weights are random Gaussian noise, the energy will be distributed uniformly across all Walsh coordinates. The concentration ratio will be exactly $1.0$ (within statistical noise). If the ratio is significantly greater than $1.0$, it means that the weights are aligned with specific dyadic frequencies.

### Mock Transcript II: The Monitor

Let us return to the conversation between Derek and Maria in her lab as they examine these spectral concentration plots on her screen.

**Derek:** (Leaning over the screen, pointing at a graph with a blue spike) "Wait, so this spike here... what are we actually looking at?"

**Maria:** "That is the token embedding matrix of GPT-2. The blue line represents the actual distribution of energy in the Walsh-Hadamard basis. The grey dotted line at the bottom is the null hypothesis—what you get if you shuffle the elements of the exact same matrix, or if you initialize it randomly."

**Derek:** "The grey line is completely flat at 1.0."

**Maria:** "Yes. Random weights show no alignment. Shuffled weights show no alignment. But look at the blue spike. It peaks at 230."

**Derek:** "Two hundred and thirty times higher than chance? How is that even possible? That means almost all the information is concentrated in a tiny fraction of the coordinates."

**Maria:** "Exactly. It means the model's embedding space is not a continuous, isotropic cloud of vectors. It is a highly aligned dyadic structure. Training has forced the vectors to cluster along specific binary coordinates. It’s like discovering that what you thought was a cloud of gas is actually a crystal lattice."

**Derek:** "But why would training do that? What is the gradient descent algorithm trying to achieve?"

**Maria:** "It is trying to build a search tree. When the model needs to retrieve a word, it doesn't scan the entire vocabulary. It makes a series of binary splits. 'Is it a noun or a verb? Is it animate or inanimate? Is it concrete or abstract?' Stochastic gradient descent is forcing the floating-point weights to approximate this discrete, branch-like structure because that is the most efficient way to store and retrieve relational knowledge. But because the transformer is built on real numbers and floating-point math, it has to approximate this tree using smooth curves. It is incredibly inefficient."

**Derek:** "So, the model is spending all this compute during training to build a digital crystal, using analog tools."

**Maria:** "Yes. And the larger the model, the clearer the crystal becomes."

---

### The Fingerprint Across Architectures

The Ernos Labs team did not stop at GPT-2. They ran their pre-registered instrument across a wide variety of production-grade models, representing different tasks, modalities, and sizes.

#### 1. Stable Diffusion 1.5 and SDXL
Stable Diffusion is a diffusion-based text-to-image model. The core of its text understanding is a CLIP text transformer. In a blind sweep of 96 tensors inside Stable Diffusion 1.5, the instrument found a stark divide.
The attention matrices (the key, query, and value projections) sat exactly at chance, with a median concentration of $1.00x$. 
But the MLP (Multi-Layer Perceptron) expansion projection matrices—specifically the `fc1` layer in the CLIP text transformer, across layers 0 through 9—showed concentrations ranging from **5.5x to 8.4x** above chance. 
In the MLP expansion layers, the network projects the token representations into a wider space (from 768 dimensions to 3072). This is where the model stores its relational concept knowledge. The instrument proved that this knowledge is stored dyadically.

#### 2. Kokoro-82M
Kokoro is a lightweight, high-quality speech synthesis model. Even at a modest scale of 82 million parameters, every single probed tensor inside Kokoro beat both null hypotheses at every registered fraction. The placement of values in the audio-generation layers was highly non-random, concentrated along dyadic coordinates.

#### 3. Llama-3.1-8B
Llama-3.1 is Meta's flagship open-weights language model. Because Llama is served in production using quantized weights to save memory, the team tested whether the dyadic structure survived quantization.
They analyzed Llama-3.1-8B dequantized from production 4-bit blocks, sampling layers 0, 8, 16, 24, and 31.
The results were uniform: every single `ffn_gate` matrix (which projects the representation into the wide feed-forward layer) was hot, with concentrations between **3.7x and 8.5x**, peaking in the middle of the network. The contraction matrices (`ffn_down`), which project back to the hidden dimension, sat at exactly $1.00x$.
The fingerprint was clear: **the law lives in the expansion direction**.

---

### The Recipe Map: Scaling to 671 Billion Parameters

To determine whether this dyadic concentration was simply an artifact of scale, the team mapped the Walsh spectrum across models spanning four orders of magnitude: from 124 million parameters (GPT-2) to one trillion parameters (Kimi-K2.6).

The results were surprising. Scale was not the primary driver of the signal.

| Model | Parameters | Expert Structure | Probed Walsh Concentration | Status |
|---|---|---|---|---|
| **GPT-2** | 124M | Dense | **12.7x – 67.6x** | Loud |
| **Llama-3.1-8B** | 8B | Dense | **3.7x – 8.5x** | Loud |
| **DeepSeek-R1** | 671B | Sparse MoE | **43.0x – 47.0x** | Loud |
| **gpt-oss** | 20B / 120B | Dense | **0.82x – 1.05x** | Quiet |
| **Qwen3** | 27B / 480B | Dense / MoE | **0.78x – 1.02x** | Quiet |
| **Kimi-K2.6** | ~1T | Sparse MoE | **0.80x – 1.07x** | Quiet |

Look at the contrast:
- DeepSeek-R1, at 671 billion parameters, showed massive Walsh concentrations of **43x to 47x** across *every single probed block*, including both dense routing layers and shared-expert MLP blocks. This was the loudest production signal measured.
- Yet, Kimi-K2.6 (approaching a trillion parameters) and Qwen3-480B sat exactly at chance ($0.80x - 1.07x$).

This proved that **scale is not the cause**. 

Architecture was also not the cause—mixture-of-experts models appeared on both sides of the divide (DeepSeek-R1 was loud, Kimi-K2.6 was quiet).

The variable was the **training recipe**. 

DeepSeek-R1 was trained using massive reinforcement learning (RL) loops focused on reasoning and self-correction, built on top of a highly structured base model. To test if the RL loop itself was writing the law, the team probed a Qwen-32B model that had been fine-tuned using distillation from DeepSeek-R1. 
The distilled Qwen-32B read as quiet as its non-reasoning parent. 
This proved that the law was not deposited by distilled reasoning tokens during post-training. It was written during the core, base pretraining phase—the training recipe itself was different.

Furthermore, the loud models' spectra exhibited a very specific mathematical signature. Their concentrations were **preserved exactly under F2-linear repacking** (swapping elements using bitwise XOR operations on their indices) and **degraded gracefully under odd-multiplication maps** (multiplying indices by odd integers modulo $2^n$).

This transformation signature is identical to the one observed in solved chess value fields—matrices representing the exact win/loss values of chess board positions. 

Loud-recipe weights are not arbitrary statistical curves. They are the same class of mathematical object as solved game fields: dyadically smooth carriers of law.

---

### The Coordinate-Dependence and Quiet Lineages

What about the quiet models like Qwen3 and Kimi? Does their quiet reading mean they contain no mathematical law?

No. By the campaign's standing epistemics, a quiet verdict is a verdict on the probe's *coordinates*, never on the presence of law.

A Walsh-Hadamard transform requires a specific ordering of the matrix rows and columns. If you shuffle the rows of a loud matrix, the signal disappears ($1.00x$). 
The quiet models are trained with different tokenizers, different weight layouts, and different tensor dimensions. Their dyadic law is packaged in coordinates that the current probe cannot read. 
A registered search over the fold's index-reordering group—trying to find the permutation matrix that aligns the quiet weights with the Walsh basis—was initiated, but the first round yielded no results. The coordinate hunt is ongoing.

But for the loud models, the verdict was clear. The weights were converging to a discrete, dyadic structure. 

The training loop was a slow, expensive, gigawatt-burning way to search for a mathematical harmony that is already defined by the laws of numbers.

If the weights are converging to this structure, why don't we bypass the training loop entirely? Why don't we write the structure directly?
