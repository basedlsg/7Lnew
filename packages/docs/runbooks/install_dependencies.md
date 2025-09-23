# Installing PyTorch and Torch Geometric with CUDA Support

This guide provides instructions on how to install PyTorch and Torch Geometric with CUDA support.

## 1. Check CUDA Availability

Before installing PyTorch and Torch Geometric with CUDA support, ensure that CUDA is available on your system.

1.  **Check NVIDIA Driver Installation:**

    ```bash
    nvidia-smi
    ```

    If the NVIDIA driver is installed correctly, this command will display information about your GPU and the installed driver version. If the command is not found or displays an error, proceed to the next section to install the drivers.

2.  **Verify CUDA Toolkit:**

    If `nvidia-smi` shows the driver version, you can also check if the CUDA Toolkit is installed.

    ```bash
    nvcc --version
    ```

    If CUDA Toolkit is installed, this command will display the CUDA version.

## 2. Install NVIDIA Drivers (If Necessary)

If the NVIDIA drivers are not installed, follow these steps:

1.  **Identify Your GPU:**

    Determine the model of your NVIDIA GPU.

2.  **Download Drivers:**

    Visit the [NVIDIA Driver Downloads](https://www.nvidia.com/Download/index.aspx) page and select your GPU model and operating system to download the appropriate drivers.

3.  **Install Drivers:**

    Follow the installation instructions provided on the NVIDIA website. Typically, this involves running the downloaded executable and following the on-screen prompts.

4.  **Verify Installation:**

    After installation, run `nvidia-smi` again to ensure the drivers are correctly installed.

## 3. Install PyTorch with CUDA Support

1.  **Create a Virtual Environment (Recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\\Scripts\\activate  # On Windows
    ```

2.  **Install PyTorch:**

    Visit the [PyTorch website](https://pytorch.org/) to get the specific installation command for your system and CUDA version.  For example:

    ```bash
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    ```

    Replace `cu118` with the appropriate CUDA version if needed.

3.  **Verify PyTorch Installation:**

    ```python
    import torch
    print(torch.cuda.is_available())
    ```

    This should print `True` if PyTorch is using CUDA.

## 4. Install Torch Geometric

1.  **Install Dependencies:**

    ```bash
    pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-${torch.__version__}.html
    ```

2.  **Install Torch Geometric:**

    ```bash
    pip install torch-geometric
    ```

3.  **Verify Torch Geometric Installation:**

    ```python
    import torch
    from torch_geometric.nn import GCNConv

    # Example usage
    in_channels = 16
    out_channels = 32
    gcn_conv = GCNConv(in_channels, out_channels)

    print(gcn_conv)
    ```

    This will print the GCNConv layer information if the installation was successful.

Now you have successfully installed PyTorch and Torch Geometric with CUDA support.