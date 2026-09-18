from __future__ import annotations

import base64
import os
import re
from dataclasses import dataclass

from bip_utils import (
    Bip39MnemonicGenerator,
    Bip39SeedGenerator,
    Bip39WordsNum,
    Bip44,
    Bip44Changes,
    Bip44Coins,
    Bip84,
    Bip84Coins,
)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

KEY_LEN = 32
IV_LEN = 12
TAG_LEN = 16

DERIVATION_PATHS: dict[str, str] = {
    'ETH': "m/44'/60'/0'/0/0",
    'BSC': "m/44'/60'/0'/0/0",
    'BTC': "m/84'/0'/0'/0/0",
    'TRX': "m/44'/195'/0'/0/0",
    'SOL': "m/44'/501'/0'/0'",
}

ALL_CHAINS: tuple[str, ...] = ('ETH', 'BSC', 'BTC', 'TRX', 'SOL')

_master_key: bytes | None = None


@dataclass(frozen=True)
class DerivedWallet:
    chain: str
    address: str
    derivation_path: str


@dataclass(frozen=True)
class DerivedSecretKey:
    chain: str
    address: str
    derivation_path: str
    private_key: str


class CryptoNotReadyError(RuntimeError):
    pass


def load_master_key(raw_key: str) -> None:
    global _master_key
    if _master_key is not None:
        return

    if not re.fullmatch(r'[0-9a-fA-F]{64}', raw_key):
        raise RuntimeError('Crypto master key invalid: must be 64-char hex (32 bytes)')

    key = bytes.fromhex(raw_key)
    if len(key) != KEY_LEN:
        raise RuntimeError(f'Crypto master key invalid: got {len(key)} bytes, expected {KEY_LEN}')

    _master_key = key


def is_crypto_ready() -> bool:
    return _master_key is not None and len(_master_key) == KEY_LEN


def generate_mnemonic() -> str:
    return str(Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12))


def derive_all_addresses(mnemonic: str) -> list[DerivedWallet]:
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

    eth_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
    eth_addr = (
        eth_ctx.Purpose()
        .Coin()
        .Account(0)
        .Change(Bip44Changes.CHAIN_EXT)
        .AddressIndex(0)
        .PublicKey()
        .ToAddress()
    )

    btc_ctx = Bip84.FromSeed(seed_bytes, Bip84Coins.BITCOIN)
    btc_addr = (
        btc_ctx.Purpose()
        .Coin()
        .Account(0)
        .Change(Bip44Changes.CHAIN_EXT)
        .AddressIndex(0)
        .PublicKey()
        .ToAddress()
    )

    trx_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.TRON)
    trx_addr = (
        trx_ctx.Purpose()
        .Coin()
        .Account(0)
        .Change(Bip44Changes.CHAIN_EXT)
        .AddressIndex(0)
        .PublicKey()
        .ToAddress()
    )

    sol_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.SOLANA)
    sol_addr = (
        sol_ctx.Purpose()
        .Coin()
        .Account(0)
        .Change(Bip44Changes.CHAIN_EXT)
        .AddressIndex(0)
        .PublicKey()
        .ToAddress()
    )

    return [
        DerivedWallet(chain='ETH', address=eth_addr, derivation_path=DERIVATION_PATHS['ETH']),
        DerivedWallet(chain='BSC', address=eth_addr, derivation_path=DERIVATION_PATHS['BSC']),
        DerivedWallet(chain='BTC', address=btc_addr, derivation_path=DERIVATION_PATHS['BTC']),
        DerivedWallet(chain='TRX', address=trx_addr, derivation_path=DERIVATION_PATHS['TRX']),
        DerivedWallet(chain='SOL', address=sol_addr, derivation_path=DERIVATION_PATHS['SOL']),
    ]


def derive_all_private_keys(mnemonic: str) -> list[DerivedSecretKey]:
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

    eth_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
    eth_node = (
        eth_ctx.Purpose()
        .Coin()
        .Account(0)
        .Change(Bip44Changes.CHAIN_EXT)
        .AddressIndex(0)
    )
    eth_addr = eth_node.PublicKey().ToAddress()
    eth_pk = eth_node.PrivateKey().Raw().ToHex()

    btc_ctx = Bip84.FromSeed(seed_bytes, Bip84Coins.BITCOIN)
    btc_node = (
        btc_ctx.Purpose()
        .Coin()
        .Account(0)
        .Change(Bip44Changes.CHAIN_EXT)
        .AddressIndex(0)
    )
    btc_addr = btc_node.PublicKey().ToAddress()
    btc_pk = btc_node.PrivateKey().Raw().ToHex()

    trx_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.TRON)
    trx_node = (
        trx_ctx.Purpose()
        .Coin()
        .Account(0)
        .Change(Bip44Changes.CHAIN_EXT)
        .AddressIndex(0)
    )
    trx_addr = trx_node.PublicKey().ToAddress()
    trx_pk = trx_node.PrivateKey().Raw().ToHex()

    sol_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.SOLANA)
    sol_node = (
        sol_ctx.Purpose()
        .Coin()
        .Account(0)
        .Change(Bip44Changes.CHAIN_EXT)
        .AddressIndex(0)
    )
    sol_addr = sol_node.PublicKey().ToAddress()
    sol_pk = sol_node.PrivateKey().Raw().ToHex()

    return [
        DerivedSecretKey(
            chain='ETH',
            address=eth_addr,
            derivation_path=DERIVATION_PATHS['ETH'],
            private_key=eth_pk,
        ),
        DerivedSecretKey(
            chain='BSC',
            address=eth_addr,
            derivation_path=DERIVATION_PATHS['BSC'],
            private_key=eth_pk,
        ),
        DerivedSecretKey(
            chain='BTC',
            address=btc_addr,
            derivation_path=DERIVATION_PATHS['BTC'],
            private_key=btc_pk,
        ),
        DerivedSecretKey(
            chain='TRX',
            address=trx_addr,
            derivation_path=DERIVATION_PATHS['TRX'],
            private_key=trx_pk,
        ),
        DerivedSecretKey(
            chain='SOL',
            address=sol_addr,
            derivation_path=DERIVATION_PATHS['SOL'],
            private_key=sol_pk,
        ),
    ]


def encrypt_mnemonic(plaintext: str) -> str:
    if _master_key is None:
        raise CryptoNotReadyError('Crypto service not ready')
    if not plaintext:
        raise ValueError('encrypt_mnemonic: plaintext must be non-empty')

    iv = os.urandom(IV_LEN)
    aesgcm = AESGCM(_master_key)
    ct_with_tag = aesgcm.encrypt(iv, plaintext.encode('utf-8'), None)
    tag = ct_with_tag[-TAG_LEN:]
    ct = ct_with_tag[:-TAG_LEN]
    return base64.b64encode(iv + ct + tag).decode('ascii')


def decrypt_mnemonic(blob: str) -> str:
    if _master_key is None:
        raise CryptoNotReadyError('Crypto service not ready')
    if not blob:
        raise ValueError('decrypt_mnemonic: blob must be non-empty')

    raw = base64.b64decode(blob)
    if len(raw) < IV_LEN + TAG_LEN + 1:
        raise ValueError('decrypt_mnemonic: blob too short')

    iv = raw[:IV_LEN]
    tag = raw[-TAG_LEN:]
    ct = raw[IV_LEN:-TAG_LEN]
    aesgcm = AESGCM(_master_key)
    try:
        return aesgcm.decrypt(iv, ct + tag, None).decode('utf-8')
    except Exception as exc:
        raise ValueError('decrypt_mnemonic: authentication failed') from exc
