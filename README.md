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
├── shors.py               
├── merchant.html          
├── user.html              
├── models/                
│   ├── bank.py            
│   ├── user.py            
│   ├── merchant.py        
│   └── blockchain.py     
├── scripts/               
│   ├── bank_system.py    
│   ├── upi_machine.py     
│   └── user_device.py     
├── utils/                
│   └── helpers.py         
└── tasks/                
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


