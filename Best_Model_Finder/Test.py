import unittest
from Best_model import BestModel
from sklearn.datasets import make_classification


class TestBestModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # Generate random classification data for testing
        cls.x_train, cls.y_train = make_classification(n_samples=1000, n_features=10, n_classes=2)
        cls.x_test, cls.y_test = make_classification(n_samples=100, n_features=10, n_classes=2)
        cls.file_object: str = 'test.log'

    def test_find_best_pipeline(self) -> None:
        # Test that the best pipeline is not None
        model: BestModel = BestModel(self.x_train, self.y_train, self.x_test, self.y_test, self.file_object)
        best_pipeline = model.find_best_pipeline()
        self.assertIsNotNone(best_pipeline)

    def test_train_best_model(self) -> None:
        # Test that the best model can be trained without errors
        model: BestModel = BestModel(self.x_train, self.y_train, self.x_test, self.y_test, self.file_object)
        model.find_best_pipeline()
        model.train_best_model()

    def test_evaluate_best_model(self) -> None:
        # Test that the best model can be evaluated on the test set without errors
        model: BestModel = BestModel(self.x_train, self.y_train, self.x_test, self.y_test, self.file_object)
        model.find_best_pipeline()
        model.train_best_model()
        accuracy: float = model.evaluate_best_model()
        self.assertIsInstance(accuracy, float)
        self.assertGreaterEqual(accuracy, 0.0)
        self.assertLessEqual(accuracy, 1.0)

    def test_save_load_model(self) -> None:
        # Test that the trained model can be saved and loaded without errors
        model: BestModel = BestModel(self.x_train, self.y_train, self.x_test, self.y_test, self.file_object)
        model.find_best_pipeline()
        model.train_best_model()
        model.save_model('test_model.joblib')
        loaded_model: BestModel = BestModel(self.x_train, self.y_train, self.x_test, self.y_test, self.file_object)
        loaded_model.load_model('test_model.joblib')
        loaded_accuracy: float = loaded_model.evaluate_best_model()
        self.assertIsInstance(loaded_accuracy, float)
        self.assertGreaterEqual(loaded_accuracy, 0.0)
        self.assertLessEqual(loaded_accuracy, 1.0)


if __name__ == '__main__':
    unittest.main()
