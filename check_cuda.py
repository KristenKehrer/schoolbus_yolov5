import torch


# This just checks that PyTorch can use CUDA (my GPU is working :) )
print('cuda.is_available(): ' + str(torch.cuda.is_available()))
