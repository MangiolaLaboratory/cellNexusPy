import anndata as ad
import numpy as np
import pandas as pd

import cellnexuspy


def test_main_assay_is_stored_in_x(monkeypatch, tmp_path):
    metadata = pd.DataFrame(
        {
            "atlas_id": ["atlas"],
            "file_id_cellNexus_single_cell": ["file.h5ad"],
        }
    )
    counts = np.array([[1, 2]], dtype=float)

    def fake_sync_assay_files(*, subdir, **kwargs):
        yield subdir, tmp_path / "file.h5ad"

    def fake_filter_single_cell(file, data):
        return ad.AnnData(
            X=counts.copy(),
            obs=pd.DataFrame(index=["cell"]),
            var=pd.DataFrame(index=["gene1", "gene2"]),
        )

    monkeypatch.setattr(cellnexuspy, "sync_assay_files", fake_sync_assay_files)
    monkeypatch.setattr(cellnexuspy, "filter_single_cell", fake_filter_single_cell)

    result = cellnexuspy._anndata_constructor(
        metadata, assays="counts", cache_directory=tmp_path
    )

    np.testing.assert_array_equal(result.X, counts)
    np.testing.assert_array_equal(result.layers["counts"], counts)
