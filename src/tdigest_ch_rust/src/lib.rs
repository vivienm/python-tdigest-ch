use pyo3::{
    exceptions::{PyRuntimeError, PyValueError},
    prelude::*,
    types::PyBytes,
};

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

    fn add_many(&mut self, py: Python, value: f32, count: usize) {
        py.allow_threads(|| self.inner.insert_many(value, count));
    }

    fn clear(&mut self, py: Python) {
        py.allow_threads(|| self.inner.clear());
    }

    fn copy(&self, py: Python) -> Self {
        py.allow_threads(|| Self {
            inner: self.inner.clone(),
        })
    }

    #[staticmethod]
    fn from_json(py: Python, data: &[u8]) -> PyResult<Self> {
        py.allow_threads(|| {
            let inner: tdigest_ch::TDigest = serde_json::from_slice(data).map_err(|e| {
                PyValueError::new_err(format!("Failed to deserialize TDigest: {}", e))
            })?;
            Ok(TDigest {
                inner: inner.into(),
            })
        })
    }

    fn is_equal(&self, py: Python, other: &TDigest) -> bool {
        py.allow_threads(|| self.inner == other.inner)
    }

    fn quantile(&mut self, py: Python, q: f64) -> f32 {
        py.allow_threads(|| self.inner.quantile(q))
    }

    fn to_json(&self, py: Python) -> PyResult<PyObject> {
        let data = py.allow_threads(|| {
            serde_json::to_vec(&self.inner)
                .map_err(|e| PyRuntimeError::new_err(format!("Failed to serialize TDigest: {e}")))
        })?;
        Ok(PyBytes::new(py, &data).into())
    }

    fn update_digest(&mut self, py: Python, other: &TDigest) {
        py.allow_threads(|| {
            self.inner |= &other.inner;
        });
    }

    fn update_vec(&mut self, py: Python, values: Vec<f32>) {
        py.allow_threads(|| self.inner.extend(values.into_iter()));
    }
}

#[pymodule]
fn _rust(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<TDigest>()?;
    Ok(())
}
