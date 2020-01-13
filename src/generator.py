from keras.models import Model
import os
import numpy as np
from src.data_loader import load_dictionary
from keras.layers import Input, Flatten, concatenate
from keras.layers.core import Dense, Reshape
from keras.layers.embeddings import Embedding
from keras.layers.normalization import BatchNormalization
from keras.models import Sequential, Model
from keras.layers.advanced_activations import PReLU

model = ...  # include here your original model

layer_name = 'my_layer'
intermediate_layer_model = Model(inputs=model.input,
                                 outputs=model.get_layer(layer_name).output)
intermediate_output = intermediate_layer_model.predict(data)


class EnhancedModelGenerator(object):
    def __init__(self,config):
        self.config = config
        self.condition_model = None
        self.drug_model = None
        self.concept2id = load_dictionary(config.dictionary.concept2id_dictionary)
        self.build_condition_model()
        self.build_drug_model()
        self.load_condition_model_weights()
        self.load_drug_model_weights()

    def build_condition_model(self):
        n2v_input_1 = Input(shape=(1,))
        n2v_emb_layer_1 = Embedding(len(self.concept2id)+1, 128, input_length=1, name="n2vembedding_1", trainable=False) 
        n2v_emb_1 = n2v_emb_layer_1(n2v_input_1)
        n2v_emb_1 = Flatten()(n2v_emb_1)

        glove_input_1 = Input(shape=(1,))
        glove_emb_layer_1 = Embedding(len(self.concept2id)+1, 128, input_length=1, name="gloveembedding_1", trainable=False) 
        glove_emb_1 = glove_emb_layer_1(glove_input_1)
        glove_emb_1 = Flatten()(glove_emb_1)
        
        concat_emb_1 = concatenate([n2v_emb_1, glove_emb_1])
        MLP_layer_1_1 = Dense(196, use_bias=False, name="mlp11")(concat_emb_1)
        MLP_layer_1_1 = BatchNormalization(name="batchnorm11")(MLP_layer_1_1)
        MLP_layer_1_1 = PReLU(name="prelu11")(MLP_layer_1_1)
        MLP_layer_1_2 = Dense(128, use_bias=False,name="mlp12")(MLP_layer_1_1)
        MLP_layer_1_2 = BatchNormalization(name="batchnorm12")(MLP_layer_1_2)
        MLP_layer_1_2 = PReLU(name="mlp12")(MLP_layer_1_2)

        self.condition_model = Model(inputs=[n2v_input_1, glove_input_1], outputs=MLP_layer_1_2)
        
    def load_condition_model_weights(self):

        self.condition_model.load_weights(os.path.join(self.config.callbacks.checkpoint_dir, 
        '%s-{epoch:02d}-{val_loss:.2f}.hdf5' % self.config.exp.name), by_name=True)


    def build_drug_model(self):
        n2v_input_2 = Input(shape=(1,))
        n2v_emb_layer_2 = Embedding(len(self.concept2id)+1, 128, input_length=1, name="n2vembedding_2", trainable=False) 
        n2v_emb_2 = n2v_emb_layer_2(n2v_input_2)
        n2v_emb_2 = Flatten()(n2v_emb_2)

        glove_input_2 = Input(shape=(1,))
        glove_emb_layer_2 = Embedding(len(self.concept2id)+1, 128, input_length=1, name="gloveembedding_2", trainable=False) 
        glove_emb_2 = glove_emb_layer_2(glove_input_2)
        glove_emb_2 = Flatten()(glove_emb_2)

        concat_emb_2 = concatenate([n2v_emb_2, glove_emb_2])
        MLP_layer_2_1 = Dense(196, use_bias=False, name="mlp21")(concat_emb_2)
        MLP_layer_2_1 = BatchNormalization(name="batchnorm21")(MLP_layer_2_1)
        MLP_layer_2_1 = PReLU(name="prelu21")(MLP_layer_2_1)
        MLP_layer_2_2 = Dense(128, name="mlp22")(MLP_layer_2_1)
        MLP_layer_2_2 = BatchNormalization(name="batchnorm22")(MLP_layer_2_2)
        MLP_layer_2_2 = PReLU(name="prelu22")(MLP_layer_2_2)

        self.drug_model = Model(inputs=[n2v_input_2, glove_input_2], outputs=MLP_layer_2_2)
        
    def load_drug_model_weights(self):

        self.drug_model.load_weights(os.path.join(self.config.callbacks.checkpoint_dir, 
        '%s-{epoch:02d}-{val_loss:.2f}.hdf5' % self.config.exp.name), by_name=True)
    
    def generate_enhanced_rep(self, savedir):

        condition_representations = self.condition_model.predict(range(1, len(self.concept2id)+1))
        drug_representations = self.drug_model.predict(range(1, len(self.concept2id)+1))

        enhanced_rep_matrix = np.zeros((len(self.concept2id), 128))

        # enhanced_rep_matrix

        # save to the savedir

        pass

    