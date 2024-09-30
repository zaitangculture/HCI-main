import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset

# 数据准备
def create_dataset():
    X = torch.randn(100, 10)  # 100个样本，每个样本有10个特征
    y = torch.randint(0, 2, (100,))  # 100个标签，值为0或1
    dataset = TensorDataset(X, y)
    dataloader = DataLoader(dataset, batch_size=10, shuffle=True)
    return dataloader

# 定义模型
class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(10, 50)
        self.fc2 = nn.Linear(50, 2)
    
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# 训练模型
def train_model(model, dataloader, criterion, optimizer, num_epochs=5):
    for epoch in range(num_epochs):
        for batch_X, batch_y in dataloader:
            # 前向传播
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            
            # 反向传播和优化
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# 测试模型
def test_model(model):
    test_X = torch.randn(20, 10)
    test_y = torch.randint(0, 2, (20,))
    with torch.no_grad():
        test_outputs = model(test_X)
        _, predicted = torch.max(test_outputs, 1)
    print(f'Predicted: {predicted}')
    print(f'True Labels: {test_y}')

# 主函数
def main():
    dataloader = create_dataset()
    model = SimpleNet()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    
    train_model(model, dataloader, criterion, optimizer, num_epochs=5)
    test_model(model)

if __name__ == '__main__':
    main()
