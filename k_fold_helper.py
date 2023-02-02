'''
This class impliments a cross validation with a stratified split.
'''
from sklearn.model_selection import StratifiedKFold, train_test_split

class StratifiedKFold3(StratifiedKFold):

    def split(self, X, y, groups=None):
        s = super().split(X, y, groups)
        for train_indxs, test_indxs in s:
            y_train = y[train_indxs]
            train_indxs, cv_indxs = train_test_split(train_indxs,stratify=y_train, test_size=(1 / (self.n_splits - 1)))
            yield train_indxs, cv_indxs, test_indxs