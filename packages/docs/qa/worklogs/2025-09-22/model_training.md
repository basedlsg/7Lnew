# Model Training Progress - 2025-09-22

## Data Preparation

The data preparation steps involve generating synthetic data of impossible towers using [src/data_gen/make_dataset.py](src/data_gen/make_dataset.py). This data is then processed and formatted for training.

**Current Status:** Blocked due to missing dependencies. User is actively working on resolving the dependency issues.

## Model Architecture

The model architecture is based on [model/model.py](model/model.py) and uses a deep neural network to predict the stability of impossible towers. The architecture includes convolutional layers for feature extraction and fully connected layers for classification.

**Current Status:** Blocked due to missing dependencies. User is actively working on resolving the dependency issues.

## Loss Function and Optimizer

The model is trained using a cross-entropy loss function and optimized with Adam.

**Current Status:** Blocked due to missing dependencies. User is actively working on resolving the dependency issues.

## Training Loop

The training loop involves iterating over the dataset, calculating the loss, and updating the model weights. The training is performed on Vertex AI using [src/model/train_vertex/trainer.py](src/model/train_vertex/trainer.py).

**Current Status:** Blocked due to missing dependencies. User is actively working on resolving the dependency issues.

## Overall Status

The data preparation and model training steps are currently blocked due to missing dependencies.