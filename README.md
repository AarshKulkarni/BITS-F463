# Quantum-Secured UPI Payment Gateway

A centralized UPI (Unified Payments Interface) payment gateway implementation featuring blockchain technology, quantum cryptography, and Shor's algorithm simulation for enhanced security.

##  Overview

This project implements a secure digital payment system that combines:
- **Blockchain Technology** for immutable transaction records
- **Quantum Cryptography** using Shor's algorithm for enhanced security
- **UPI Payment Gateway** for seamless digital transactions
- **Multi-bank Support** with user and merchant management
- **Web-based Interface** for merchants and users

##  Architecture

The system consists of several interconnected components:

### Core Models
- **Bank**: Manages users, merchants, and transactions
- **User**: Individual account holders with UPI capabilities
- **Merchant**: Business entities accepting payments
- **Blockchain**: Immutable ledger for transaction records

### Network Components
- **UPI Machine**: Central payment processing server (Port 5001)
- **Bank System**: Backend banking operations (Port 8080)
- **User Device**: Client-side payment interface

### Security Features
- **Quantum Cryptography**: Shor's algorithm implementation using Cirq
- **Blockchain Validation**: SHA-256 hashing for transaction integrity
- **Secure Authentication**: PIN and password-based user verification

##  Project Structure

```
├── main.py                 # Main application entry point
├── shors.py               # Shor's algorithm implementation with Cirq
├── merchant.html          # Merchant QR code portal interface
├── user.html             # User payment interface
├── models/               # Core data models
│   ├── bank.py           # Bank management system
│   ├── user.py           # User account model
│   ├── merchant.py       # Merchant account model
│   └── blockchain.py     # Blockchain implementation
├── scripts/              # Network and system scripts
│   ├── bank_system.py    # Banking server
│   ├── upi_machine.py    # UPI processing server
│   └── user_device.py    # Client device simulator
├── utils/                # Utility functions
│   └── helpers.py        # Helper functions (hashing, etc.)
└── tasks/                # Project documentation
```

## Installation

### Prerequisites
- Python 3.8+
- Cirq (for quantum computing simulation)
- Standard Python libraries (hashlib, json, socket, time)

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd BITS-F463
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install cirq numpy
   ```

##  Usage

### Starting the System

1. **Start the Bank System Server:**
   ```bash
   python scripts/bank_system.py
   ```

2. **Start the UPI Machine (in a new terminal):**
   ```bash
   python scripts/upi_machine.py
   ```

3. **Open the Web Interfaces:**
   - Merchant Portal: Open `merchant.html` in a web browser
   - User Portal: Open `user.html` in a web browser


