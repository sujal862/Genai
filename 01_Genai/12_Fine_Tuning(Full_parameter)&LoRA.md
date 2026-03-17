# Fine-Tuning in LLMs — Simple Notes

## 1. Core Idea

Large Language Models (LLMs) are trained using **Next Token Prediction**.

The model does **not learn to output the entire sentence at once**.
Instead, it learns to **predict the next word (token) given previous words**.

So training objective:

```
previous tokens  →  predict next token
```

---

# 2. Example Sentence

Sentence:

```
I love coding
```

Assume tokenization gives:

```
[11, 22, 33]
```

Meaning:

```
11 → I
22 → love
33 → coding
```

Training pairs become:

| Input  | Target |
| ------ | ------ |
| I      | love   |
| I love | coding |

In token form:

```
Input  : [11,22]
Target : [22,33]
```

Meaning the model learns:

```
I → predict "love"
love → predict "coding"
```

---

# 3. Another Example (Longer Sentence)

Sentence:

```
The best place to learn GenAI IS ChaiCode Cohort
```

Example tokens:

```
[1,2,3,4,5,10]
```

Training format:

```
Input  : [1,2,3,4,5]
Target : [2,3,4,5,10]
```

Model learns:

```
1 → 2
2 → 3
3 → 4
4 → 5
5 → 10
```

So it always predicts **the next token in the sequence**.

---

# 4. What Happens During Training

For every position in the sequence:

```
previous tokens → model predicts next token
```

Example:

```
I → love
I love → coding
```

The model prediction is compared with the **correct next token**,and **loss is calculated** to improve the model.

---

# 5. What Happens During Training (Loss & Weight Update)

During training, the model predicts the **next token** for each position in the sequence.

Example:

```
I → love
I love → coding
```

The model first makes a prediction.
Then the predicted token is compared with the **correct next token**.

A **loss value** is calculated to measure how wrong the prediction was.

This loss is then used to **adjust the model's weights (parameters)** using backpropagation and optimization algorithms.

Goal of training:

```
reduce loss → improve next token prediction
```

By repeating this process on large datasets, the model gradually learns language patterns and becomes better at predicting the next token.



2nd method to train : 

# LoRA :
LoRA (Low Rank Adaptation) 

LoRA ek efficient fine-tuning method hai jisme base model ke original weights freeze kar diye jate hain.

Model ke andar small adapter matrices (A and B) add kiye jate hain jo train hote hain.

Full model train karne ke bajaye sirf ye small parameters update hote hain.

Isse GPU memory, training time aur storage bahut kam lagta hai.

Final weight effectively hota hai: W + (A × B).

Isi wajah se LoRA se large LLMs ko easily fine-tune kiya ja sakta hai even on limited hardware.