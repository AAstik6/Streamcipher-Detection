# Streamcipher Detection using Neural Networks

This project focuses on identifying stream ciphers (like **RC4**, **Trivium**, and **ESPRESSO**) using machine learning, particularly neural networks. It is part of a broader cryptography research and learning initiative.

## 🔍 Project Goals
- Generate keystream samples for different stream ciphers
- Train neural network models (ANN / CNN) to classify ciphers
- Apply OpenMax for open-set recognition

## 🧠 Ciphers Used
- RC4
- Trivium
- Espresso

## 🛠 Technologies
- Python 3.10
- TensorFlow / Keras
- NumPy, Pandas
- Git, Google Colab (optional)

## 📁 Folder Structure
## 🚀 How to Run

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Train the model:
    ```bash
    python train_model.py
    ```

3. Test the model:
    ```bash
    python test_model.py
    ```

## 📊 Results

Model achieved accuracy of `XX%` on `8-byte` / `24-byte` / `32-byte` keystream classification (replace with your result).

## 📌 Future Work

- Integrate additional ciphers
- Use attention-based models (like Transformers)
- Explore cryptographic adversarial attacks

## 🧑‍💻 Author
**Aastik Sharma**  
GitHub: [@AAstik6](https://github.com/AAstik6)

---

## 📄 Research Paper

This project is documented in a full research paper:

**Title:** Stream Cipher Classification Using AI: A Neural Network-Based Approach  
**Author:** Aastik Sharma  
**Institute:** Maharaja Agrasen Institute of Technology, India  
**Supervisor:** Mr. Girish Mishra, DRDO  
**Status:** Intern Research Work

👉 [Click here to read the paper (PDF)](Stream Cipher Classification Using Neural Networks, R-Paper.pdf)
