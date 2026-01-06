"""
Script pour créer un utilisateur admin dans la base de données
Usage: python create_admin.py
"""

import sys
from pathlib import Path
from datetime import datetime

# Ajouter le dossier racine au path Python
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from database import engine, create_db_and_tables
from models.admin import Admin
from core.security import hash_password
from sqlmodel import Session, select


def create_admin_user(username: str, password: str):
    """
    Crée un utilisateur admin dans la base de données

    Args:
        username: Nom d'utilisateur de l'admin
        password: Mot de passe en clair (sera hashé automatiquement)
    """
    # Créer les tables si elles n'existent pas
    create_db_and_tables()

    with Session(engine) as session:
        # Vérifier si l'utilisateur existe déjà
        existing_admin = session.exec(
            select(Admin).where(Admin.username == username)
        ).first()

        if existing_admin:
            print(f"❌ L'utilisateur '{username}' existe déjà dans la base de données.")
            print(f"   ID: {existing_admin.id}")
            print(f"   Actif: {existing_admin.is_active}")
            print(f"   Admin: {existing_admin.is_admin}")
            return False

        # Hasher le mot de passe
        hashed_password = hash_password(password)

        # Créer le nouvel admin
        new_admin = Admin(
            username=username,
            hashed_password=hashed_password,
            is_active=True,    # L'utilisateur est actif
            is_admin=True,     # L'utilisateur est admin
            created_at=datetime.utcnow()  # Date de création
        )

        # Ajouter à la session et sauvegarder
        session.add(new_admin)
        session.commit()
        session.refresh(new_admin)

        print(f"✅ Utilisateur admin créé avec succès!")
        print(f"   Username: {new_admin.username}")
        print(f"   ID: {new_admin.id}")
        print(f"   Actif: {new_admin.is_active}")
        print(f"   Admin: {new_admin.is_admin}")
        return True


if __name__ == "__main__":
    # Informations de l'admin à créer
    ADMIN_USERNAME = "ossinga"
    ADMIN_PASSWORD = "GWHOAMI13KK"

    print("=" * 50)
    print("Création d'un utilisateur admin")
    print("=" * 50)
    print(f"Username: {ADMIN_USERNAME}")
    print("=" * 50)

    try:
        success = create_admin_user(ADMIN_USERNAME, ADMIN_PASSWORD)
        if success:
            print("\n✅ L'admin peut maintenant se connecter avec ces identifiants.")
        else:
            print("\n⚠️  Aucun changement effectué.")
    except Exception as e:
        print(f"\n❌ Erreur lors de la création de l'admin: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
