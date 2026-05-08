from app import create_app
from app.models import DetalleFactura, Factura


def test_factura_and_detalle_models_are_registered():
    app = create_app("testing")

    with app.app_context():
        factura_table = Factura.__table__
        detalle_table = DetalleFactura.__table__

        assert factura_table.name == "facturas"
        assert factura_table.columns["numero"].unique is True
        assert "cliente_id" in factura_table.columns
        assert detalle_table.name == "detalle_factura"
        assert "factura_id" in detalle_table.columns
        assert "producto_id" in detalle_table.columns
