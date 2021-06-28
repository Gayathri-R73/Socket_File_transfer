import torch
import torchvision
from torch.utils.data import DataLoader
#transfrom = torchvision.transforms.Compose([torchvision.transforms.ToTensor(),
#torchvision.transforms.Normalize((0.5,),(0.5,)))
#train_ts = torchvision.datasets.MNIST(root='./data',train=True,download=True,transform=transfrom)
#test_ts = torchvision.datasets.MNIST(root='./data',train=True,download=True,transform=transfrom)
#train_dl = DataLoader(train_ts,batch_size=32,shuffle=True,drop_last=False)
#test_dl = DataLoader(test_ts,batch_size=64,shuffle=True,drop_last=False)
class CNN_NET(torch.nn.Module):
    def __init__(self):
        super(CNN_NET,self).__init__()
        self.cnn_layers = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels=1,out_channels=8,kernel_size=3,padding=1,stride=1),
            torch.nn.MaxPool2d(kernel_size=2,stride=2),
            torch.nn.ReLU(),
            torch.nn.Conv2d(in_channels=8,out_channels=32,kernel_size=3,padding=1,stride=1),
            torch.nn.MaxPool2d(kernel_size=2,stride=2),
            torch.nn.ReLU(),
        )
        self.fc_layers = torch.nn.Sequential(
            torch.nn.Linear(7*7*32,200),
            torch.nn.ReLU(),
            torch.nn.Linear(200,100),
            torch.nn.ReLU(),
            torch.nn.Linear(100,10),
            torch.nn.LogSoftmax(dim=1)
        )

    def forward(self,x):
        out = self.cnn_layers(x)
        out = out.view(-1,7*7*32)
        out = self.fc_layers(out)
        return out


#model = CNN_NET()
#loss_fn = torch.nn.CrossEntropyLoss()
#optimizer = torch.optim.Adam(model.parameters(),lr=1e-3)
#for s in range(5):
#    print ('run in step:{}'.format(s))
#    for i,(x_train,y_train) in enumerate(train_dl):
#        y_pred = model.forward(x_train)
#        train_loss = loss_fn(y_pred,y_train)
#        if (i+1)%100 == 0:
#            print (i+1,train_loss.item())
#        optimizer.zero_grad()
#        train_loss.backward()
#        optimizer.step()

#total = 0
#correct_count = 0


#model.eval()
#for test_images,test_labels in test_dl:
#    with torch.no_grad():
#        pred_labels = model(test_images)
#    predicted = torch.max(pred_labels,1)[1]
#    correct_count  += (predicted == test_labels).sum()
#    total += len(test_labels)
#print (correct_count.detach().numpy(),total)

#print ('total acc:{}'.format(correct_count.detach().numpy()/total))
#torch.save(model,'./cnn_mnist_model.h5')