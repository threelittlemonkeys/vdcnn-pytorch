import sys
import re
import time
from model import *
from utils import *
from os.path import isfile

def load_data():
    data = []
    batch_x = []
    batch_y = []
    print("loading data...")
    word_to_idx = load_word_to_idx(sys.argv[2])
    tag_to_idx = load_tag_to_idx(sys.argv[3])
    fo = open(sys.argv[4], "r")
    for line in fo:
        line = line.strip()
        seq = [int(i) for i in line.split(" ")][:SEQ_LEN]
        label = seq.pop()
        pad = [PAD_IDX] * (SEQ_LEN - len(seq))
        batch_x.append(seq + pad)
        batch_y.append(label)
        if len(batch_x) == BATCH_SIZE:
            data.append((LongTensor(batch_x), LongTensor(batch_y))) # append a mini-batch
            batch_x = []
            batch_y = []
    fo.close()
    print("data size: %d" % (len(data) * BATCH_SIZE))
    print("batch size: %d" % BATCH_SIZE)
    return data, word_to_idx, tag_to_idx

def train():
    num_epochs = int(sys.argv[5])
    data, word_to_idx, tag_to_idx = load_data()
    model = vdcnn(len(word_to_idx), len(tag_to_idx))
    optim = torch.optim.SGD(model.parameters(), lr = LEARNING_RATE, weight_decay = WEIGHT_DECAY)
    epoch = load_checkpoint(sys.argv[1], model) if isfile(sys.argv[1]) else 0
    filename = re.sub("\.epoch[0-9]+$", "", sys.argv[1])
    print(model)
    print("training model...")
    for i in range(epoch + 1, epoch + num_epochs + 1):
        loss_sum = 0
        timer = time.time()
        for x, y in data:
            model.zero_grad()
            loss = F.nll_loss(model(x), y) # forward pass and compute loss
            loss.backward() # compute gradients
            optim.step() # update parameters
            loss = scalar(loss)
            loss_sum += loss
        timer = time.time() - timer
        loss_sum /= len(data)
        if i % SAVE_EVERY and i != epoch + num_epochs:
            save_checkpoint("", "", i, loss_sum, timer)
        else:
            save_checkpoint(filename, model, i, loss_sum, timer)

if __name__ == "__main__":
    if len(sys.argv) != 6:
        sys.exit("Usage: %s model word_to_idx tag_to_idx training_data num_epoch" % sys.argv[0])
    print("cuda: %s" % CUDA)
    train()
