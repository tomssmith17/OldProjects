# Libraries
import pandas as pd
import matplotlib as plt
from sklearn.datasets import make_blobs
import sklearn as skl
import tensorflow as tf
from sklearn.model_selection import train_test_split

#%%

# Generate dummy dataset
X, y = make_blobs(n_samples=1000, centers=2, n_features=2, random_state=78)

# Creating a DataFrame with the dummy data
df = pd.DataFrame(X, columns=["Feature 1", "Feature 2"])
df["Target"] = y

# Plotting the dummy data
df.plot.scatter(x="Feature 1", y="Feature 2", c="Target", colormap="winter")

#%%
#Use sklearn to split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=78)

#%%
# Create scaler instance
X_scaler = skl.preprocessing.StandardScaler()

# Fit the scaler
X_scaler.fit(X_train)

# Scale the data
X_train_scaled = X_scaler.transform(X_train)
X_test_scaled = X_scaler.transform(X_test)

#%%
# Create the Keras Sequential model
nn_model = tf.keras.models.Sequential()   #stores the entire architecture of the neural network model
# Add our first Dense layer, including the input layer
nn_model.add(tf.keras.layers.Dense(units=1, activation="relu", input_dim=2))
# input_dim == # inputs used in the model
# units == # neurons in the hidden layer
# activation == specify activation function to use, relu for nonlinear relationships

# NN consists of 1 hidden layer with 1 neuron

# Add the output layer that uses a probability activation function
nn_model.add(tf.keras.layers.Dense(units=1, activation="sigmoid"))

# Check the structure of the Sequential model
nn_model.summary()

#%%
#compiling the model == informing the model how it should learn and train
#optimization function == shapes and molds a NN model while it is being trained to ensure that if performs to the best of its ability
#loss metric == used by ML algorithms to score performance of the model through each iteration and epoch by evaluating inaccuracy of a single input
#%%
# Compile the Sequential model together and customize metrics
nn_model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

#%%
# train/fit our Keras model using the 'fit' function

# Fit the model to the training data
fit_model = nn_model.fit(X_train_scaled, y_train, epochs=100)

#NN selects random weights to start training the model, meaning each NN model is different

#%%
# visualize our model's loss over the full 100 epochs
# Create a DataFrame containing training history
history_df = pd.DataFrame(fit_model.history, index=range(1,len(fit_model.history["loss"])+1))
#%%
# Plot the loss
history_df.plot(y="loss")

# Plot the accuracy
history_df.plot(y="accuracy")

#%%
# Evaluate the model using the test data
model_loss, model_accuracy = nn_model.evaluate(X_test_scaled,y_test,verbose=2)
print(f"Loss: {model_loss}, Accuracy: {model_accuracy}")

#%%
# Predict the classification of a new set of blob data
new_X, new_Y = make_blobs(n_samples=10, centers=2, n_features=2, random_state=78)

nn_model.predict_classes(new_X)
