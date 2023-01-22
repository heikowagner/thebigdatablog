import keras.utils as ku
import numpy as np

class PasswordBatchGenerator(ku.Sequence) :
  
  def __init__(self, X_train, labels, batch_size) :
    self.X_train = X_train
    self.labels = labels
    self.batch_size = batch_size
    
    
  def __len__(self) :
    return (np.ceil(self.X_train.shape[0] / float(self.batch_size))).astype(np.int32)
  
  
  def __getitem__(self, idx) :
    batch_x = self.X_train[idx * self.batch_size : (idx+1) * self.batch_size]
    batch_y = self.labels[idx * self.batch_size : (idx+1) * self.batch_size]
    
    return (batch_x,batch_y)