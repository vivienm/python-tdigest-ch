use pyo3::prelude::*;

#[pyclass]
struct TDigest {
    inner: tdigest_ch::TDigest,
}

#[pymethods]
impl TDigest {
    #[new]
    fn new(py: Python) -> Self {
        py.allow_threads(|| TDigest {
            inner: tdigest_ch::TDigest::default(),
        })
    }

    fn __bool__(&self, py: Python) -> bool {
        py.allow_threads(|| !self.inner.is_empty())
    }

    fn __len__(&self, py: Python) -> usize {
        py.allow_threads(|| self.inner.len())
    }

    fn add(&mut self, py: Python, value: f32) {
        py.allow_threads(|| self.inner.insert(value));
    }

    fn clear(&mut self, py: Python) {
        py.allow_threads(|| self.inner.clear());
    }

    fn copy(&self, py: Python) -> Self {
        py.allow_threads(|| Self {
            inner: self.inner.clone(),
        })
    }

    fn is_equal(&self, py: Python, other: &TDigest) -> bool {
        py.allow_threads(|| self.inner == other.inner)
    }

    fn quantile(&mut self, py: Python, q: f64) -> f32 {
        py.allow_threads(|| self.inner.quantile(q))
    }

    fn update_digest(&mut self, py: Python, other: &TDigest) {
        py.allow_threads(|| {
            self.inner |= &other.inner;
        });
    }

    fn update_sequence(&mut self, py: Python, values: Vec<f32>) {
        py.allow_threads(|| self.inner.extend(values.into_iter()));
    }
}

#[pymodule]
fn _rust(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<TDigest>()?;
    Ok(())
}
