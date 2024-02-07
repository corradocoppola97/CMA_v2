import torch
import torch.nn as nn
import torchvision.models.resnet

class FNN(nn.Module):

    def __init__(self,layers):
        super(FNN,self).__init__()
        self.layers = layers
        self.g = nn.Sigmoid()

    def forward(self,x):
        return self.layers(x).flatten()

    def set_no_grad(self):
        for p in self.parameters():
            p.requires_grad = False

    def get_w(self):
        W = []
        for param in (self.parameters()):
            W.append(param.ravel().detach())
        ww = torch.cat(W)
        return ww

    def get_grad(self):
        gW = []
        for param in self.parameters():
            gW.append(param.grad.view(-1))
        g_ww = torch.cat(gW)
        return g_ww

    def update_w(self,alfa):
        with torch.no_grad():
            for p in self.parameters():
                new_val = p - alfa*p.grad
                p.copy_(new_val)

    def set_w(self,w):
        with torch.no_grad():
            idx = 0
            for param in self.parameters():
                param.data = w[idx:idx + param.numel()].reshape(param.shape)
                idx += param.numel()



class ResidualNetwork(nn.Module):

    def __init__(self,resnet_type,num_classes):
        super(ResidualNetwork, self).__init__()
        self.mod = eval('torchvision.models.resnet.'+resnet_type+'(pretrained=True)')
        self.mod.fc = nn.Linear(self.mod.fc.in_features,num_classes)

    def forward(self, x):
        x = x.float()
        return self.mod(x)

    def set_no_grad(self):
        for p in self.mod.parameters():
            p.requires_grad = False

    def get_w(self):
        W = []
        for param in (self.mod.parameters()):
            W.append(param.ravel().detach())
        ww = torch.cat(W)
        return ww

    def get_grad(self):
        gW = []
        for param in self.mod.parameters():
            gW.append(param.grad.view(-1))
        g_ww = torch.cat(gW)
        return g_ww

    def update_w(self, alfa):
        with torch.no_grad():
            for p in self.mod.parameters():
                new_val = p - alfa * p.grad
                p.copy_(new_val)

    def set_w(self, w):
        with torch.no_grad():
            idx = 0
            for param in self.mod.parameters():
                param.data = w[idx:idx + param.numel()].reshape(param.shape)
                idx += param.numel()


