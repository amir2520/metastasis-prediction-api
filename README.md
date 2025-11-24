# End-to-End MLOps Platform for Metastasis Prediction

A production-grade machine learning system for predicting cancer metastasis from gene mutation data, built with microservices architecture and automated deployment on Google Cloud Platform.

## 🎯 Project Overview

This project demonstrates a complete MLOps pipeline that separates concerns into three independent microservices:
- **Training Service**: Automated model training with experiment tracking
- **MLflow Server**: Centralized experiment tracking and model registry
- **Inference API**: Production-ready REST API for predictions

The system processes gene mutation data to predict metastasis probability using custom scikit-learn pipelines with advanced preprocessing and automated hyperparameter optimization.

> **Note**: This is a demonstration project showcasing production MLOps architecture and best practices. The GCP infrastructure is not currently running to avoid ongoing costs.

## 🏗️ Architecture

```
┌─────────────────────┐
│   Training Service  │
│  (Docker Container) │
│                     │
│  • Hydra Config     │
│  • Custom Pipelines │
│  • Auto HP Tuning   │
└──────────┬──────────┘
           │
           │ Logs experiments
           ▼
┌─────────────────────┐
│   MLflow Server     │
│  (Docker Container) │
│                     │
│  • Experiment Track │
│  • Model Registry   │
│  • Version Control  │
└──────────┬──────────┘
           │
           │ Loads best model
           ▼
┌─────────────────────┐
│  Inference API      │
│  (Docker Container) │
│                     │
│  • FastAPI Server   │
│  • Model Serving    │
│  • REST Endpoints   │
└─────────────────────┘
```

All services designed for deployment on GCP Compute Engine VMs with internal VPC networking for secure service-to-service communication.

## ✨ Key Features

### Microservices Architecture
- **Separation of Concerns**: Training, tracking, and inference as independent services
- **Containerization**: Each service runs in its own Docker container
- **Cloud-Native**: Designed for GCP deployment with infrastructure automation
- **Internal Networking**: Secure VPC communication between services

### Training Pipeline
- **Modular Configuration**: Hydra dataclass-based config store for composable pipeline components
- **Custom Transformers**: Gene mutation preprocessing using sklearn's BaseEstimator and TransformerMixin
- **Automated Hyperparameter Tuning**: Hydra sweep across multiple YAML configurations for different model architectures
- **Experiment Tracking**: All runs logged to MLflow with metrics, parameters, and artifacts
- **Model Versioning**: Best models automatically tagged based on F1 score optimization

### ML Pipeline Components
- Gene mutation text preprocessing
- TF-IDF vectorization for mutation patterns
- Dimensionality reduction (PCA, NMF)
- SMOTE for handling class imbalance
- Multiple classifier architectures (Logistic Regression, Random Forest, SVM)

### MLflow Integration
- Centralized experiment tracking across all training runs
- Model registry with versioning (best_v1, best_v2, ..., best_v10)
- Artifact storage for trained models and preprocessing pipelines
- Metric comparison

### Inference API
- **FastAPI** REST endpoints with automatic OpenAPI documentation
- **Pydantic** validation for type-safe request/response handling
- Automatic model loading from MLflow registry
- Returns probability predictions for metastasis classification

### Infrastructure Automation
- **Makefile-driven workflow**: Single command builds, deployments, and teardowns
- **Docker containerization**: Consistent environments across development and production
- **GCP VM automation**: Automated provisioning and configuration via startup scripts
- **One-command deployment**: From code to running infrastructure with minimal manual intervention

## 🛠️ Technology Stack

### Machine Learning
- **scikit-learn**: Core ML framework and pipeline architecture
- **imbalanced-learn**: SMOTE for class imbalance handling
- **pandas/numpy**: Data manipulation and numerical computing

### MLOps & Infrastructure
- **MLflow**: Experiment tracking and model registry
- **Hydra**: Configuration management and hyperparameter optimization
- **FastAPI**: High-performance REST API framework
- **Pydantic**: Data validation and settings management
- **Docker**: Application containerization
- **GCP Compute Engine**: Virtual machine hosting
- **GCP Artifact Registry**: Docker image storage and distribution

### Development & Automation
- **Make**: Build automation and deployment orchestration
- **Poetry**: Dependency management with pyproject.toml
- **Git**: Version control

## 📁 Repository Structure

This repository contains the **inference API** component of the MLOps platform:

```
metastasis-prediction-api/
├── src/
│   └── server.py          # FastAPI application
├── Dockerfile             # Container definition
├── Makefile              # Deployment automation
├── pyproject.toml        # Poetry dependencies
├── startup-script.sh     # GCP VM startup configuration
└── README.md            # This file
```

**Related Repositories:**
- Training Service: *[https://github.com/amir2520/liver_metas]*
- MLflow Server

> **Note**: This is part of a multi-repository MLOps system. Each microservice is maintained in its own repository for independent deployment and versioning.

## 🚀 Deployment Overview

The system was designed with full automation for GCP deployment:

1. **Build**: Docker images built locally or in CI/CD
2. **Push**: Images pushed to GCP Artifact Registry
3. **Deploy**: VMs provisioned with startup scripts that pull and run containers
4. **Network**: Internal VPC networking configured for service communication
5. **Access**: SSH tunnels for secure access to services

All steps automated via Makefiles for reproducible infrastructure.

## 🔐 Design Decisions

### Why Microservices?
- **Independent Scaling**: Training runs are resource-intensive but intermittent; API needs constant availability
- **Technology Flexibility**: Each service can use different resource requirements
- **Fault Isolation**: API remains available even if training service fails
- **Deployment Independence**: Update one service without redeploying others

### Why Hydra for Configuration?
- **Composability**: Mix and match preprocessing, models, and hyperparameters
- **Reproducibility**: Each experiment configuration saved as YAML
- **Sweep Capability**: Built-in grid/random search across configurations
- **Type Safety**: Dataclass-based configs catch errors early

### Why MLflow?
- **Experiment Tracking**: Compare dozens of model runs easily
- **Model Registry**: Version control for trained models
- **Artifact Storage**: Keep models and preprocessing pipelines together
- **Production Integration**: Load models directly into serving API

## 📈 Example Results

The pipeline was used to train and compare multiple model architectures:

- **Multiple model configurations** tested with different preprocessing and hyperparameters
- **F1 score optimization** for balanced precision/recall on imbalanced medical data
- **Automated model selection** based on validation metrics
- **Version tracking** for reproducibility and rollback capability

## 🚧 Project Status

**Completed:**
- ✅ Microservices architecture design and implementation
- ✅ Training pipeline with Hydra configuration system
- ✅ Custom sklearn transformers for gene mutation processing
- ✅ MLflow integration for experiment tracking
- ✅ FastAPI inference service
- ✅ Docker containerization for all services
- ✅ GCP deployment automation with Makefiles
- ✅ Internal VPC networking configuration


## 📧 Contact

**Amir Fatemi**
- Email: [hossein.fatemi85@gmail.com](mailto:hossein.fatemi85@gmail.com)
- LinkedIn: [linkedin.com/in/amirfatemi2520](https://www.linkedin.com/in/amirfatemi2520/)
- GitHub: [github.com/amir2520](https://github.com/amir2520)

---

*This project demonstrates production-grade MLOps practices including microservices architecture, experiment tracking, automated deployment, and infrastructure as code.*