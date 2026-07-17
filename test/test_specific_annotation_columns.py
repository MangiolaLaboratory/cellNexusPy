import pandas as pd

from cellnexuspy import (
    SAMPLE_DATABASE_URL,
    get_metadata,
    get_pseudobulk,
    get_specific_annotation_columns,
    keep_quality_cells,
    keep_specific_annotation_columns,
)


def _controlled_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "sample_id": ["s1", "s1", "s1", "s2", "s2"],
            "cell_type_unified_ensemble": ["T", "T", "B", "T", "B"],
            "batch": ["s1", "s1", "s1", "s2", "s2"],
            "ct_flag": ["s1__T", "s1__T", "s1__B", "s2__T", "s2__B"],
            "cell_noise": ["c1", "c2", "c3", "c4", "c5"],
            "cell_id": ["c1", "c2", "c3", "c4", "c5"],
        }
    )


def test_get_specific_annotation_columns_keeps_fd_columns_and_drops_cell_level():
    df = _controlled_df()

    assert sorted(get_specific_annotation_columns(df, "sample_id")) == sorted(
        ["sample_id", "batch"]
    )
    assert get_specific_annotation_columns(
        df, "sample_id", include_query_columns=False
    ) == ["batch"]
    assert sorted(
        get_specific_annotation_columns(
            df, ["sample_id", "cell_type_unified_ensemble"]
        )
    ) == sorted(
        ["sample_id", "cell_type_unified_ensemble", "batch", "ct_flag"]
    )
    assert sorted(
        get_specific_annotation_columns(
            df,
            ["sample_id", "cell_type_unified_ensemble"],
            include_query_columns=False,
        )
    ) == sorted(["batch", "ct_flag"])
    assert "cell_noise" not in get_specific_annotation_columns(
        df, ["sample_id", "cell_type_unified_ensemble"]
    )


def test_get_specific_annotation_columns_works_on_lazy_sample_database():
    _, meta = get_metadata(parquet_url=SAMPLE_DATABASE_URL)
    cols = get_specific_annotation_columns(meta, "sample_id", sample_n=2000)
    assert isinstance(cols, list)
    assert "sample_id" in cols
    assert "cell_id" not in cols


def test_keep_specific_annotation_columns_selects_keys_and_fd_columns():
    df = _controlled_df()
    out = keep_specific_annotation_columns(
        df, ["sample_id", "cell_type_unified_ensemble"]
    )
    assert all(
        c in out.columns
        for c in [
            "sample_id",
            "cell_type_unified_ensemble",
            "batch",
            "ct_flag",
        ]
    )
    assert "cell_id" not in out.columns
    assert len(out) == df[["sample_id", "cell_type_unified_ensemble"]].drop_duplicates().shape[0]


def test_keep_specific_annotation_columns_preserves_sample_grain_user_columns():
    _, meta = get_metadata(parquet_url=SAMPLE_DATABASE_URL)
    df = (
        meta.limit(500)
        .fetchdf()
        .assign(
            my_sample_annotation=lambda x: "ann_" + x["sample_id"].astype(str),
            my_cell_noise=lambda x: x["cell_id"],
        )
    )
    coldata_like = keep_specific_annotation_columns(
        df, ["sample_id", "cell_type_unified_ensemble"]
    )
    assert "my_sample_annotation" in coldata_like.columns
    assert "my_cell_noise" not in coldata_like.columns
    assert "cell_id" not in coldata_like.columns


def test_get_pseudobulk_preserves_sample_grain_user_columns():
    _, meta = get_metadata(parquet_url=SAMPLE_DATABASE_URL)
    file_id = (
        keep_quality_cells(meta)
        .project("file_id_cellNexus_pseudobulk")
        .limit(1)
        .fetchdf()["file_id_cellNexus_pseudobulk"]
        .iloc[0]
    )
    df = (
        keep_quality_cells(meta)
        .filter(f"file_id_cellNexus_pseudobulk = '{file_id}'")
        .fetchdf()
        .assign(my_sample_annotation=lambda x: "ann_" + x["sample_id"].astype(str))
    )
    adata = get_pseudobulk(df)
    assert "my_sample_annotation" in adata.obs.columns
