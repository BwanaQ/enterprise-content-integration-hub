from sqlalchemy import select

from app.db.models.integration import Integration
from app.db.session import SessionLocal


def test_create_and_read_integration():
    db = SessionLocal()

    try:
        integration = Integration(
            name="Test CMS",
            system_type="cms",
            base_url="https://cms.example.com",
        )

        db.add(integration)
        db.commit()
        db.refresh(integration)

        result = db.execute(
            select(Integration).where(
                Integration.id == integration.id
            )
        )

        saved_integration = result.scalar_one()

        assert saved_integration.name == "Test CMS"
        assert saved_integration.system_type == "cms"
        assert saved_integration.base_url == "https://cms.example.com"
        assert saved_integration.is_active is True

    finally:
        db.close()