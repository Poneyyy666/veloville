"""Authentification et autorisation.

À compléter : vérification d'un mot de passe contre son hachage bcrypt, création et
décodage du JWT (secret et algorithme lus dans l'environnement),
dépendances utilisateur_courant() et exiger_role("exploitant").
"""
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from api.config import JWT_ALGORITHM, JWT_EXPIRE_MINUTES, JWT_SECRET


def hash_password(plain_password: str) -> str:
    """Hache un mot de passe avant son stockage."""

    # gensalt() crée un sel aléatoire intégré au hash bcrypt.
    salt = bcrypt.gensalt()

    # hashpw() calcule le hash.
    hashed = bcrypt.hashpw(
        plain_password.encode("utf-8"),
        salt,
    )

    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie le mot de passe reçu contre le hash stocké."""

    # checkpw() compare sans déchiffrer le mot de passe enregistré.
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def create_access_token(username: str, role: str) -> str:
    """Crée un JWT signé contenant identité et rôle."""

    now = datetime.now(timezone.utc)
    expiration = now + timedelta(minutes=JWT_EXPIRE_MINUTES)

    payload = {
        # sub identifie l'utilisateur.
        "sub": username,

        # role est un claim applicatif visible dans le JWT.
        "role": role,

        # iat indique quand le token a été généré.
        "iat": now,

        # exp fixe la date d'expiration.
        "exp": expiration,
    }

    # encode() signe le payload avec le secret du serveur.
    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    """Vérifie signature et expiration puis retourne le payload."""

    # decode() refuse les tokens modifiés, mal signés ou expirés.
    return jwt.decode(
        token,
        JWT_SECRET,
        algorithms=[JWT_ALGORITHM],
    )
