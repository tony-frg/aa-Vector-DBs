import importlib
from typing import Optional

import numpy as np
import numpy.typing as npt
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings


class MyCustomEmbeddingFunction(EmbeddingFunction[Documents]):
    """
    An embedding function class that uses a transformer-based model for generating embeddings.

    This class leverages the Hugging Face `transformers` library and PyTorch to compute
    embeddings from input texts. It supports pooling strategies and L2 normalization for
    the generated embeddings.

    Args:
        model_name (str): The name of the pretrained model to use. Defaults to "thenlper/gte-base".
        cache_dir (Optional[str]): Directory for caching the model files. If None, the default cache
            directory of Hugging Face models will be used.

    Raises:
        ValueError: If `transformers` or `torch` libraries are not installed.
    """

    def __init__(
        self,
        model_name: str = "thenlper/gte-base",
        cache_dir: Optional[str] = None,
    ):
        try:
            from transformers import AutoModel, AutoTokenizer

            self._torch = importlib.import_module("torch")
            self._F = importlib.import_module("torch.nn.functional")
            self._tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
            self._model = AutoModel.from_pretrained(model_name, cache_dir=cache_dir)
        except ImportError:
            raise ValueError(
                "The transformers and/or pytorch python package is not installed. "
                "Please install them with `pip install transformers` and `pip install torch`"
            )

        # Disable parallelism to prevent threading issues during tokenization
        import os

        os.environ["TOKENIZERS_PARALLELISM"] = "false"

    @staticmethod
    def _average_pool(last_hidden_states: npt.NDArray, attention_mask: npt.NDArray) -> npt.NDArray:
        """
        Performs average pooling over the token embeddings, using the attention mask to ignore padding.

        Args:
            last_hidden_states (npt.NDArray): The output hidden states from the transformer model.
            attention_mask (npt.NDArray): The attention mask indicating which tokens are padding.

        Returns:
            npt.NDArray: The average-pooled embeddings.
        """
        last_hidden = last_hidden_states * attention_mask[..., None]
        return last_hidden.sum(axis=1) / attention_mask.sum(axis=1)[..., None]

    @staticmethod
    def _normalize(vector: npt.NDArray) -> npt.NDArray:
        """
        Normalizes a vector to unit length using L2 norm.

        Args:
            vector (npt.NDArray): The input vector to normalize.

        Returns:
            npt.NDArray: The normalized vector with unit length.
        """
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return vector / norm

    def __call__(self, texts: Documents) -> Embeddings:
        """
        Generates embeddings for a list of texts.

        This method tokenizes the input texts, computes embeddings using the transformer model,
        applies average pooling, and then normalizes the resulting vectors.

        Args:
            texts (Documents): A list of strings representing the documents to be embedded.

        Returns:
            Embeddings: A list of normalized embeddings, each represented as a list of floats.
        """
        inputs = self._tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=512)
        attention_mask = inputs["attention_mask"]

        with self._torch.no_grad():
            outputs = self._model(**inputs)

        # Perform average pooling
        embeddings = self._average_pool(outputs.last_hidden_state.numpy(), attention_mask.numpy())

        # Normalize embeddings
        embeddings = np.array([self._normalize(e) for e in embeddings])

        # Convert embeddings to a list for compatibility with ChromaDB
        return embeddings.tolist()
