from app import create_app
from app.models import Producto


def test_producto_model_is_registered():
    app = create_app("testing")

    with app.app_context():
        producto_table = Producto.__table__

        assert producto_table.name == "productos"
        assert "precio" in producto_table.columns
        assert producto_table.columns["nombre"].unique is True
