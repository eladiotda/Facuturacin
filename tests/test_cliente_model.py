from app import create_app
from app.models import Cliente


def test_cliente_model_is_registered():
    app = create_app("testing")

    with app.app_context():
        cliente_table = Cliente.__table__

        assert cliente_table.name == "clientes"
        assert "correo" in cliente_table.columns
        assert cliente_table.columns["correo"].unique is True
