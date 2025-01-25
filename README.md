# Godcoin

Godcoin is a simple blockchain-based cryptocurrency designed to provide an easy-to-understand introduction to blockchain technology. It includes core features such as wallet creation, transactions, mining, and a proof-of-work consensus mechanism. Built with Python using Flask, this project provides a web interface to interact with the blockchain.

## Features

- **Blockchain**: A basic implementation of a blockchain with proof-of-work.
- **Wallet Creation**: Generate unique public/private key pairs.
- **Transactions**: Send and receive coins across the blockchain.
- **Mining**: Mine new blocks and receive a reward in the form of Godcoins.
- **Web Interface**: A simple Flask-based frontend for interacting with the blockchain and wallets.

## Table of Contents

- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [How to Mine Godcoins](#how-to-mine-godcoins)
- [Wallets](#wallets)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Installation

To get started with Godcoin, follow the instructions below:

1. Clone the repository:

   ```bash
   git clone https://github.com/godwingino/Godcoin.git
   cd Godcoin

## Running the Application

To run the application, execute the following command:

```bash
python app.py

## API Endpoints

The following API endpoints are available in the application:

### `/`
- **Method**: `GET`
- **Description**: Displays the home page with the list of wallets and the option to create new wallets.

### `/wallet/<address>`
- **Method**: `GET`
- **Description**: Displays the details of a specific wallet, including balance and transactions.

### `/wallet/new`
- **Method**: `GET`
- **Description**: Generates a new wallet and returns the associated public/private key pair.

### `/balance/<address>`
- **Method**: `GET`
- **Description**: Retrieves the balance of a specific wallet.

### `/transaction/new`
- **Method**: `POST`
- **Description**: Creates a new transaction. The request body should include `sender`, `recipient`, and `amount` fields.

### `/mine`
- **Method**: `GET`
- **Description**: Mines a new block and rewards the miner with 50 Godcoins. The miner's address must be provided as a query parameter (`miner_address`).

### `/chain`
- **Method**: `GET`
- **Description**: Displays the entire blockchain.

## How to Mine Godcoins

To mine Godcoins, you must send a request to the `/mine` endpoint, passing your public address as a query parameter:

```bash
http://127.0.0.1:5000/mine?miner_address=<YOUR_PUBLIC_KEY>
Upon successfully mining a new block, you will receive a reward of 50 Godcoins.
Wallets
A wallet in Godcoin is represented by a pair of public and private keys. The public key is used to receive coins, while the private key should be kept secure as it is used to sign transactions.

To create a new wallet, use the /wallet/new endpoint, which will generate and return a new public/private key pair.

Contributing
We welcome contributions to the project! If you would like to contribute, follow the steps below:

Fork the repository on GitHub.
Create a new branch (git checkout -b feature-branch).
Make your changes and commit them (git commit -am 'Add feature').
Push your changes to your fork (git push origin feature-branch).
Open a pull request on GitHub.
License
This project is licensed under the MIT License. See the LICENSE file for more details.

Acknowledgments
The blockchain implementation is inspired by Bitcoin's proof-of-work mechanism.
Thanks to Flask for providing a lightweight framework for building the web interface.
This project is a personal initiative to explore and learn about blockchain technology.
