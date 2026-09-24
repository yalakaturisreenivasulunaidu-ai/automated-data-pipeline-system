import pandas as pd

from pipeline.transform import Transformer


CONFIG = {
    "transform": {
        "drop_duplicates": True,
        "dropna_columns": ["order_id", "amount"],
        "derived_columns": {"total_with_tax": "amount * 1.08"},
    }
}


def make_df():
    return pd.DataFrame(
        {
            "Order Id": [1, 2, 2, 3],
            "Amount": [100.0, None, 50.0, 50.0],
        }
    )


def test_clean_column_names():
    t = Transformer(CONFIG)
    df = t.transform(make_df())
    assert "order_id" in df.columns
    assert "amount" in df.columns


def test_drops_duplicates_and_nulls():
    t = Transformer(CONFIG)
    df = t.transform(make_df())
    # row with null amount (order_id 2, first occurrence) is dropped,
    # and the duplicate order_id/amount pair (3, 50.0) vs (2, 50.0) is fine
    assert df["amount"].isnull().sum() == 0
    assert len(df) == len(df.drop_duplicates())


def test_derived_column_added():
    t = Transformer(CONFIG)
    df = t.transform(make_df())
    assert "total_with_tax" in df.columns
    row = df[df["order_id"] == 1].iloc[0]
    assert round(row["total_with_tax"], 2) == round(100.0 * 1.08, 2)


def test_empty_input_raises():
    t = Transformer(CONFIG)
    empty_df = pd.DataFrame({"order_id": [], "amount": []})
    try:
        t.transform(empty_df)
        assert False, "expected ValueError on empty result"
    except ValueError:
        pass
