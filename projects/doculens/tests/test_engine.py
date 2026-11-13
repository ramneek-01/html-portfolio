from doculens.engine import DocumentIndex

def test_split_empty_and_overlap():
    assert DocumentIndex.split("")==[]
    chunks=DocumentIndex.split(" ".join(f"w{i}" for i in range(250)),100,20)
    assert len(chunks)==3 and "w80" in chunks[0] and "w80" in chunks[1]

def test_retrieval_and_persistence(tmp_path):
    d=tmp_path/"docs";d.mkdir();(d/"ml.txt").write_text("Machine learning models require monitoring for data drift.")
    idx=DocumentIndex();assert idx.ingest(str(d))>=1
    assert idx.search("monitoring data drift")[0]["source"]=="ml.txt"
    idx.save(str(tmp_path/"idx"))
    assert DocumentIndex.load(str(tmp_path/"idx")).search("data drift")
